"""进程沙箱：超时看门狗 + Job Object 限内存 + 杀整棵进程树。

为什么手写 Job Object：本机没有 psutil，也没有 pywin32，所以只能走 ctypes。
威胁模型是「防手滑」（死循环、爆内存、乱写文件），不是防恶意代码 ——
所以用 Job Object + 独立临时目录 + 墙钟超时，不追求内核级隔离。

两条铁律（踩过的坑，写死在这里）：
1. 输入输出**一律字节模式**。绝不用 `subprocess.run(input=..., text=True)`：
   Windows 上文本模式会把 `\\r\\n` 二次翻译成 `\\r\\r\\n`，造出假结论。
2. 超时后必须**杀整棵进程树**（`taskkill /F /T`），否则用户代码起的子进程会残留，
   下一步删临时目录就会失败。
"""
from __future__ import annotations

import ctypes
import os
import shutil
import subprocess
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
    """杀整棵进程树。taskkill 失败就退回 proc.kill()。"""
    try:
        subprocess.run([_taskkill(), "/F", "/T", "/PID", str(proc.pid)],
                       capture_output=True, timeout=5,
                       creationflags=CREATE_NO_WINDOW if _IS_WINDOWS else 0)
    except Exception:
        pass
    try:
        proc.kill()
    except Exception:
        pass


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

    flags = (CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW) if _IS_WINDOWS else 0
    t0 = time.perf_counter()

    proc = subprocess.Popen(
        [str(c) for c in cmd],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(cwd) if cwd else None,
        env=full_env,
        creationflags=flags,
    )

    job: JobObject | None = None
    note = ""
    try:
        mem_bytes = memory_limit_mb * 1024 * 1024 if memory_limit_mb else None
        try:
            job = JobObject(memory_limit_bytes=mem_bytes)
            if not job.assign(proc):
                note = "Job Object 挂载失败，本次无内存上限"
        except OSError as e:
            job = None
            note = f"Job Object 不可用（{e}），本次无内存上限"

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

        peak_bytes = job.peak_memory_bytes() if job else 0
        exit_code = proc.returncode if proc.returncode is not None else -1

        # 实测结论（别改成 `peak >= limit`）：Job Object 的进程内存限额**不会**直接杀进程，
        # 而是让那次分配失败 —— 于是 Python 抛 MemoryError、以退出码 1 结束，
        # 峰值稳定停在限额的 ~99%。所以判据是「峰值接近限额」+「进程异常结束」。
        # 纯 `peak >= limit` 永远差一点点，会漏判成一无是处的 RE。
        mem_exceeded = bool(
            job and mem_bytes
            and peak_bytes >= mem_bytes * 0.9
            and (exit_code != 0 or timed_out)
        )

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
            job_assigned=job is not None and not note,
            raw_note=note,
        )
    finally:
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
