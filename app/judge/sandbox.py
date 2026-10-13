"""进程沙箱：超时看门狗 + 内存限额 + 杀整棵进程树。

两条铁律（踩过的坑，写死在这里）：
1. 输入输出**一律字节模式**。绝不用 `subprocess.run(input=..., text=True)`：
   Windows 上文本模式会把 `\\r\\n` 二次翻译成 `\\r\\r\\n`，造出假结论。
2. 超时后必须**杀整棵进程树**，否则用户代码起的子进程会残留，
   下一步删临时目录就会失败。

跨平台（2026-10-13 加 Linux 支持，为了能部署到免费云平台）
----------------------------------------------------------
- **Windows**：Job Object 限内存（`JOB_OBJECT_LIMIT_PROCESS_MEMORY`）+ `taskkill /F /T`
- **Linux**：`resource.setrlimit` 在子进程里自限内存（preexec_fn）+
  `os.killpg` 杀整个进程组（配合 `start_new_session=True` → setsid）
- 内存峰值：Windows 从 Job Object 读；Linux **运行期间用采样线程**读
  `/proc/<pid>/status` 的 VmHWM（进程退出后 /proc 条目消失，事后读只会得到 0
  → 三条证据里的 `near_limit` 永远不成立 → **MLE 被误判成 RE**）

Linux 上 setrlimit 的效果和 Windows 不同：超限时分配失败会让 Python 抛
MemoryError（跟 Windows 那条实测结论一样），所以 MLE 的三条证据判据通用。
而且正因为它是**软限制**（进程自己抛异常退出，不是被内核秒杀），
退出前有充裕的采样窗口，5ms 的采样几乎不会漏。
"""
from __future__ import annotations

import ctypes
import os
import shutil
import signal
import subprocess
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

# ---------------- Windows 常量 ----------------
JobObjectExtendedLimitInformation = 9
JOB_OBJECT_LIMIT_PROCESS_MEMORY = 0x00000100
JOB_OBJECT_LIMIT_JOB_MEMORY = 0x00000200
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000

CREATE_NEW_PROCESS_GROUP = 0x00000200
CREATE_NO_WINDOW = 0x08000000

_IS_WINDOWS = os.name == "nt"


# ---------------- Win32 结构体 ----------------
class _IO_COUNTERS(ctypes.Structure):
    _fields_ = [
        ("ReadOperationCount", ctypes.c_ulonglong),
        ("WriteOperationCount", ctypes.c_ulonglong),
        ("OtherOperationCount", ctypes.c_ulonglong),
        ("ReadTransferCount", ctypes.c_ulonglong),
        ("WriteTransferCount", ctypes.c_ulonglong),
        ("OtherTransferCount", ctypes.c_ulonglong),
    ]


class _JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_int64),
        ("PerJobUserTimeLimit", ctypes.c_int64),
        ("LimitFlags", ctypes.c_uint32),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", ctypes.c_uint32),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", ctypes.c_uint32),
        ("SchedulingClass", ctypes.c_uint32),
    ]


class _JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation", _JOBOBJECT_BASIC_LIMIT_INFORMATION),
        ("IoInfo", _IO_COUNTERS),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]


kernel32 = ctypes.WinDLL("kernel32", use_last_error=True) if _IS_WINDOWS else None

if kernel32:
    kernel32.CreateJobObjectW.restype = ctypes.c_void_p
    kernel32.CreateJobObjectW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p]

    kernel32.SetInformationJobObject.restype = ctypes.c_int
    kernel32.SetInformationJobObject.argtypes = [
        ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32]

    kernel32.AssignProcessToJobObject.restype = ctypes.c_int
    kernel32.AssignProcessToJobObject.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    kernel32.QueryInformationJobObject.restype = ctypes.c_int
    kernel32.QueryInformationJobObject.argtypes = [
        ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32,
        ctypes.POINTER(ctypes.c_uint32)]

    kernel32.TerminateJobObject.restype = ctypes.c_int
    kernel32.TerminateJobObject.argtypes = [ctypes.c_void_p, ctypes.c_uint32]

    kernel32.CloseHandle.restype = ctypes.c_int
    kernel32.CloseHandle.argtypes = [ctypes.c_void_p]


class JobObject:
    """一个 Job 句柄 + 内存上限。子进程 assign 后，它起的子孙也自动在同一个 Job 里。"""

    def __init__(self, memory_limit_bytes: int | None = None, kill_on_close: bool = True):
        if not kernel32:
            raise OSError("Job Object 仅在 Windows 可用")
        self.handle = kernel32.CreateJobObjectW(None, None)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        self.memory_limit_bytes = int(memory_limit_bytes or 0)

        flags = 0
        if self.memory_limit_bytes:
            flags |= JOB_OBJECT_LIMIT_PROCESS_MEMORY
        if kill_on_close:
            flags |= JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE

        info = _JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        info.BasicLimitInformation.LimitFlags = flags
        if self.memory_limit_bytes:
            info.ProcessMemoryLimit = ctypes.c_size_t(self.memory_limit_bytes)

        if not kernel32.SetInformationJobObject(
                self.handle, JobObjectExtendedLimitInformation,
                ctypes.byref(info), ctypes.sizeof(info)):
            err = ctypes.get_last_error()
            self.close()
            raise ctypes.WinError(err)

    def assign(self, proc: subprocess.Popen) -> bool:
        handle = getattr(proc, "_handle", None)
        if handle is None:
            return False
        return bool(kernel32.AssignProcessToJobObject(self.handle, ctypes.c_void_p(int(handle))))

    def peak_memory_bytes(self) -> int:
        info = _JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        ret_len = ctypes.c_uint32(0)
        ok = kernel32.QueryInformationJobObject(
            self.handle, JobObjectExtendedLimitInformation,
            ctypes.byref(info), ctypes.sizeof(info), ctypes.byref(ret_len))
        return int(info.PeakProcessMemoryUsed) if ok else 0

    def terminate(self) -> None:
        if self.handle:
            kernel32.TerminateJobObject(self.handle, 1)

    def close(self) -> None:
        if self.handle:
            kernel32.CloseHandle(self.handle)
            self.handle = None


# ---------------- 运行结果 ----------------
@dataclass
class RunResult:
    exit_code: int = 0
    stdout: bytes = b""
    stderr: bytes = b""
    time_ms: int = 0
    mem_kb: int = 0
    timed_out: bool = False
    mem_exceeded: bool = False
    truncated: bool = False           # 输出超上限被截断
    job_assigned: bool = False        # Job Object 是否成功挂上（挂不上就没有内存上限）
    raw_note: str = field(default="", repr=False)


def _taskkill() -> str:
    root = os.environ.get("SystemRoot", r"C:\Windows")
    p = os.path.join(root, "System32", "taskkill.exe")
    return p if os.path.exists(p) else "taskkill"


def kill_tree(proc: subprocess.Popen) -> None:
    """杀整棵进程树。

    Windows：taskkill /F /T；Linux：把整个进程组干掉（子进程用
    start_new_session=True 起，所以 pgid == pid）。
    两条路都失败才退回 proc.kill()。
    """
    if _IS_WINDOWS:
        try:
            subprocess.run([_taskkill(), "/F", "/T", "/PID", str(proc.pid)],
                           capture_output=True, timeout=5,
                           creationflags=CREATE_NO_WINDOW)
        except Exception:
            pass
    else:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except Exception:
            pass
    try:
        proc.kill()
    except Exception:
        pass


# --------------------------------------------------------------------- #
# Linux 内存限额：在 fork 之后、exec 之前把 rlimit 设好
# --------------------------------------------------------------------- #
def _linux_rlimit_fn(mem_bytes: int | None):
    """返回一个能塞给 subprocess.Popen(preexec_fn=...) 的函数。

    在子进程里执行，所以这里只能碰 os / resource 这类 async-signal-safe 的东西。
    """
    if not mem_bytes:
        return None

    def _apply() -> None:  # pragma: no cover - 在子进程里跑
        import resource
        n = int(mem_bytes)
        # AS = 地址空间总上限，最接近 Windows 的「进程内存限额」语义
        try:
            resource.setrlimit(resource.RLIMIT_AS, (n, n))
            return
        except (ValueError, OSError):
            pass
        # 有些内核不许设 RLIMIT_AS，退一步用 DATA 段（覆盖大多数爆内存场景）
        try:
            resource.setrlimit(resource.RLIMIT_DATA, (n, n))
        except (ValueError, OSError):
            pass
        # 顺带限制单文件大小，防写爆磁盘
        try:
            resource.setrlimit(resource.RLIMIT_FSIZE, (64 * 1024 * 1024,) * 2)
        except (ValueError, OSError):
            pass

    return _apply


def _linux_peak_kb(pid: int) -> int:
    """读 /proc/<pid>/status 的 VmHWM（进程自身的历史峰值常驻内存），单位 KB。

    ★ 进程一退出 `/proc/<pid>` 就没了，**事后读只会得到 0**。
    所以调用方必须在进程存活期间采，见下面的 `_PeakSampler`。
    """
    try:
        with open("/proc/%d/status" % pid, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith("VmHWM:"):
                    return int(line.split()[1])
    except Exception:
        pass
    return 0


def _children_rss_kb() -> int:
    """所有**已回收**子进程里出现过的最大 RSS，单位 KB。

    Linux 上 `ru_maxrss` 的单位是 KB（macOS 是字节，别搞混）。
    它是单调不减的「历史最大值」，所以只能当兜底、不能单独用作某次运行的峰值。
    """
    try:
        import resource
        return int(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    except Exception:
        return 0


_SAMPLE_INTERVAL_S = 0.005


class _PeakSampler(threading.Thread):
    """在子进程运行期间不停采 `/proc/<pid>/status` 的 VmHWM，记住最大值。

    ★ 为什么必须采样，而不是运行前/后各读一次（这是踩过的真坑）：
      - 运行**前**读：进程刚 exec，还没分配内存 → 读到极小值
      - 运行**后**读：进程已退出，`/proc/<pid>` 条目消失 → 读到 0
      两者取 max 仍是 0 → MLE 判据的 `near_limit` 永远不成立
      → **内存超限被误判成 RE**（CI 上实测：`RE 峰值 0 MB / 限额 128 MB`）

    ★ 为什么 5ms 的采样间隔也够（不会漏掉中间尖峰）：
      VmHWM 是进程**自身的历史峰值**、单调不减，不是瞬时值。
      只要进程存活期间采到**任意一次**，拿到的就是「截至那一刻的历史最高」。
      再加上 Linux 的 `RLIMIT_AS` 是软限制 —— 分配失败时进程会自己抛
      MemoryError 后正常退出（不是被内核秒杀），退出前有充裕的采样窗口。

    进程存活短于一个采样间隔的极端情况，由 `run()` 里的 rusage 兜底补上。
    """

    def __init__(self, pid: int, interval: float = _SAMPLE_INTERVAL_S) -> None:
        super().__init__(daemon=True)
        self.pid = pid
        self.interval = interval
        self.peak_kb = 0
        self._stop = threading.Event()

    def run(self) -> None:  # pragma: no cover - 线程体
        while not self._stop.is_set():
            kb = _linux_peak_kb(self.pid)
            if kb > self.peak_kb:
                self.peak_kb = kb
            self._stop.wait(self.interval)

    def stop(self) -> int:
        self._stop.set()
        self.join(timeout=1.0)
        return self.peak_kb


# stderr 里出现这些字样，基本可以确认是「被内存掐住」而不是别的崩溃。
# 覆盖 Python（MemoryError）与 C/C++（分配失败信息），P2 接 gcc 后也用得上。
_OOM_MARKERS = (
    b"MemoryError",
    b"can't allocate memory",
    b"cannot allocate memory",
    b"Cannot allocate memory",
    b"std::bad_alloc",
    b"Out of memory",
    b"out of memory",
)


def _looks_like_oom(stderr: bytes) -> bool:
    if not stderr:
        return False
    return any(m in stderr for m in _OOM_MARKERS)


def memory_exceeded(*, peak_bytes: int, mem_bytes: int | None, exit_code: int,
                    timed_out: bool, stdout: bytes, stderr: bytes) -> bool:
    """这次运行算不算**内存超限（MLE）**。纯函数 —— 输入即全部依据，不碰进程。

    ★ 为什么单独抽出来：判据本身很容易写错，而它错了的表现是「静默判错 verdict」，
    只在特定平台的特定场景下暴露（Linux 上就漏判过一次）。
    抽成纯函数之后，`tools/selftest_sandbox.py` 可以直接对判据矩阵下断言，
    不必依赖「真跑到那个平台」。

    两条**独立**的证据链，任一条成立即判 MLE：

    - **链 A（直接）**：stderr 里明确说了内存不够。
      Linux 的 RLIMIT_AS 触发时 Python 抛 MemoryError 并打印 traceback —— 最硬的证据。
      ⚠️ 不能只靠峰值比例：Linux 限的是**地址空间**（RLIMIT_AS），
      而 VmHWM 量的是**实际驻留**（RSS），两个不是同一个量纲 ——
      地址空间打满时 RSS 往往只到八成就上不去了
      （CI 实测 51 MB / 64 MB 限额，比值 0.80 < 0.9，只靠比例会漏判成 RE）。

    - **链 B（间接）**：峰值顶到限额附近 + 异常结束 + 没有正常输出。
      这一条是为 Windows 准备的：Job Object 的进程内存限额**不杀进程**，
      而是让那次分配失败 —— Python 抛 MemoryError、以退出码 1 结束，
      峰值稳定停在限额的 ~99%，stdout 为空。
      ⚠️「没有输出」必须一起看：机器有负载时进程可能没跑到峰值就被别的原因带崩。
    """
    if not mem_bytes:
        return False                      # 没设限额就无从谈超限
    if not ((exit_code != 0) or timed_out):
        return False                      # 正常跑完的不算
    if _looks_like_oom(stderr):
        return True                       # 链 A
    return peak_bytes >= mem_bytes * 0.9 and not stdout.strip()   # 链 B


def run(cmd: list[str], *, stdin_bytes: bytes = b"", cwd: str | Path | None = None,
        env: dict[str, str] | None = None, time_limit_ms: int = 1000,
        memory_limit_mb: int = 256, max_output_bytes: int = 1048576,
        kill_grace_ms: int = 300) -> RunResult:
    """跑一个受控子进程。

    - 超时：墙钟看门狗，超了杀整树
    - 内存：Job Object 限额（超了系统直接杀进程），峰值内存读回
    - 输出：超 max_output_bytes 截断并打标
    """
    full_env = os.environ.copy()
    if env:
        full_env.update(env)

    if _IS_WINDOWS:
        flags = CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW
        popen_kw: dict = {"creationflags": flags}
    else:
        # 新会话 = 新进程组，超时时能 killpg 一锅端
        popen_kw = {"start_new_session": True}
        # 内存限额只能在这里塞进子进程（fork 后 exec 前生效）
        rl = _linux_rlimit_fn(memory_limit_mb * 1024 * 1024 if memory_limit_mb else None)
        if rl:
            popen_kw["preexec_fn"] = rl

    t0 = time.perf_counter()

    proc = subprocess.Popen(
        [str(c) for c in cmd],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(cwd) if cwd else None,
        env=full_env,
        **popen_kw,
    )

    job: JobObject | None = None
    note = ""
    sampler: _PeakSampler | None = None
    rss_before = 0
    try:
        mem_bytes = memory_limit_mb * 1024 * 1024 if memory_limit_mb else None

        # Windows 才需要显式挂 Job Object；Linux 的限额已经在 preexec 里设好
        if _IS_WINDOWS:
            try:
                job = JobObject(memory_limit_bytes=mem_bytes)
                if not job.assign(proc):
                    note = "Job Object 挂载失败，本次无内存上限"
            except OSError as e:
                job = None
                note = f"Job Object 不可用（{e}），本次无内存上限"

        # Linux：进程一退出 /proc/<pid> 就没了，必须从这一刻起持续采样。
        # （运行前/后各读一次会双双读到 0，见 _PeakSampler 的说明）
        if not _IS_WINDOWS:
            rss_before = _children_rss_kb()
            sampler = _PeakSampler(proc.pid)
            sampler.start()

        timed_out = False
        out = err = b""
        try:
            out, err = proc.communicate(
                input=stdin_bytes, timeout=max(0.05, time_limit_ms / 1000.0))
        except subprocess.TimeoutExpired:
            timed_out = True
            kill_tree(proc)
            try:
                out, err = proc.communicate(timeout=max(0.2, kill_grace_ms / 1000.0))
            except subprocess.TimeoutExpired:
                try:
                    proc.kill()
                    out, err = proc.communicate(timeout=1.0)
                except Exception:
                    out, err = b"", b""

        elapsed_ms = int((time.perf_counter() - t0) * 1000)

        if _IS_WINDOWS:
            peak_bytes = job.peak_memory_bytes() if job else 0
        else:
            peak_kb = sampler.stop() if sampler is not None else _linux_peak_kb(proc.pid)
            # 兜底：采样一次都没赶上（进程存活时间短于采样间隔）时，
            # 看本次是否**刷新了**「子进程最大 RSS」记录：
            #   - 刷新了（after > before）→ 这一次的历史峰值就是它，采信
            #   - 没刷新 → 读到的是别的用例留下的旧值，必须丢掉
            #     （否则会拿上一个用例的峰值来判这一个用例，造成假 MLE）
            if peak_kb == 0:
                rss_after = _children_rss_kb()
                if rss_after > rss_before:
                    peak_kb = rss_after
            peak_bytes = peak_kb * 1024
        exit_code = proc.returncode if proc.returncode is not None else -1

        # 判 MLE —— 判据在 `memory_exceeded()` 里（纯函数，可被直接断言），
        # 两条独立证据链的推导与踩坑记录都写在那个函数的 docstring 里。
        mem_exceeded = memory_exceeded(
            peak_bytes=peak_bytes, mem_bytes=mem_bytes, exit_code=exit_code,
            timed_out=timed_out, stdout=out, stderr=err)

        truncated = False
        if max_output_bytes:
            if len(out) > max_output_bytes:
                out = out[:max_output_bytes]
                truncated = True
            if len(err) > max_output_bytes:
                err = err[:max_output_bytes]

        return RunResult(
            exit_code=exit_code,
            stdout=out,
            stderr=err,
            time_ms=elapsed_ms,
            mem_kb=peak_bytes // 1024,
            timed_out=timed_out,
            mem_exceeded=mem_exceeded,
            truncated=truncated,
            job_assigned=(job is not None and not note) if _IS_WINDOWS else bool(mem_bytes),
            raw_note=note,
        )
    finally:
        if sampler is not None and sampler.is_alive():
            # 异常路径上采样线程可能还在转（正常路径已经 stop 过了）
            sampler.stop()
        if job:
            # KILL_ON_JOB_CLOSE：关句柄时连带清掉残留子孙进程
            job.close()
        if proc.poll() is None:
            kill_tree(proc)


def rmtree_force(path: str | Path) -> bool:
    """删目录。Windows 上文件被占用会失败 —— 重试几次再放弃。"""
    p = Path(path)
    if not p.exists():
        return True
    for _ in range(3):
        try:
            shutil.rmtree(p)
            return True
        except Exception:
            time.sleep(0.1)
    shutil.rmtree(p, ignore_errors=True)
    return not p.exists()


def clean_tmp_root(tmp_root: str | Path) -> int:
    """清掉上一次留下的判题临时目录（崩溃兜底）。返回删掉的个数。"""
    root = Path(tmp_root)
    if not root.exists():
        return 0
    n = 0
    for child in root.iterdir():
        if child.is_dir():
            rmtree_force(child)
            n += 1
    return n
