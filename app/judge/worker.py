"""判题执行器：后台单线程 + 队列。

为什么是单线程：本机可用内存只有 2~4 GB，判题要起子进程，并发会成倍吃内存，
而且判题是重活、不能塞进 uvicorn 的事件循环里。

每份提交一个独立临时目录，判完就删；prepare 失败（编译/语法错）时所有用例统一判 CE。
"""
from __future__ import annotations

import queue
import threading
import time
import traceback
from pathlib import Path

from .. import config, db, scoring, users
from . import sandbox
from .compare import compare
from .runner_base import Limits
from .runner_python import PythonRunner

# stdout/stderr 落库时的截断长度（完整的没地方放，样例一般很小）
_STORE_LIMIT = 8000


def build_runner(lang: str, interpreter: str, cfg):
    """按语言挑 runner。P0 只有 Python；C/C++ 与 Shell 在 P2/P4 接。"""
    if lang in ("python", "py"):
        label = interpreter or "py313"
        return PythonRunner(cfg.interpreter_path(label), label)
    raise ValueError(f"暂不支持的语言：{lang}")


class JudgeWorker:
    def __init__(self, cfg=None):
        self.cfg = cfg or config.get()
        self.q: "queue.Queue[int]" = queue.Queue()
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()

    # ---------- 生命周期 ----------
    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, name="judge-worker", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        self.q.put(-1)

    def submit(self, submission_id: int) -> None:
        self.q.put(int(submission_id))

    def pending(self) -> int:
        return self.q.qsize()

    # ---------- 主循环 ----------
    def _loop(self) -> None:
        while not self._stop.is_set():
            try:
                sid = self.q.get(timeout=1.0)
            except queue.Empty:
                continue
            if sid == -1:
                break
            try:
                self.judge(sid)
            except Exception:
                tb = traceback.format_exc()
                try:
                    db.update("submissions",
                              {"verdict": "IE", "message": tb[-1500:], "judged_at": db.now_iso()},
                              "id=?", (sid,))
                except Exception:
                    pass
            finally:
                self.q.task_done()

    # ---------- 判一份提交 ----------
    def judge(self, sid: int) -> None:
        sub = db.query_one("SELECT * FROM submissions WHERE id=?", (sid,))
        if not sub:
            return
        prob = db.query_one("SELECT * FROM problems WHERE id=?", (sub["problem_id"],))
        if not prob:
            db.update("submissions", {"verdict": "IE", "message": "题目不存在"},
                      "id=?", (sid,))
            return
        # 判完写 mastery 时要按「这次提交是谁的」来记账
        prob["_uid"] = int(sub["user_id"] or 0)

        cases = db.query(
            "SELECT * FROM testcases WHERE problem_id=? ORDER BY ord, id",
            (sub["problem_id"],))
        total = len(cases)
        if not total:
            db.update("submissions", {"verdict": "IE", "message": "这道题还没有测试用例"},
                      "id=?", (sid,))
            return

        cfg = self.cfg
        t0 = time.perf_counter()

        # 每份提交一个干净目录：残留先删，再建
        workdir = Path(cfg.tmp_judge) / f"sub_{sid}"
        sandbox.rmtree_force(workdir)
        workdir.mkdir(parents=True, exist_ok=True)

        limits = Limits(
            time_ms=int(prob["time_limit_ms"] or cfg.default_time_limit_ms),
            memory_mb=int(prob["memory_limit_mb"] or cfg.default_memory_limit_mb),
            max_output_bytes=cfg.max_output_bytes,
            kill_grace_ms=cfg.kill_grace_ms,
        )
        checker = prob["checker"] or "standard"
        eps = float(prob["float_eps"] or 1e-6)
        total_score = int(prob["total_score"] or 100)

        try:
            runner = build_runner(sub["lang"], sub["interpreter"], cfg)
        except ValueError as e:
            db.update("submissions", {"verdict": "IE", "message": str(e)}, "id=?", (sid,))
            sandbox.rmtree_force(workdir)
            return

        db.update("submissions", {"verdict": "judging"}, "id=?", (sid,))

        rows: list[tuple] = []
        try:
            ok, msg = runner.prepare(sub["code"] or "", workdir)
            if not ok:
                # 编译/语法错：所有测试点统一 CE，一分不给；错误原文放 message
                g = scoring.grade([c["points"] for c in cases], [], total_score)
                for i, c in enumerate(cases):
                    rows.append((sid, c["id"], i, "CE", g["points"][i], 0,
                                 0, 0, "", msg[:_STORE_LIMIT],
                                 c["expected_stdout"] or "", c["stdin"] or "", -1, msg[:1000]))
                self._finish(sid, "CE", 0, total, 0, 0, msg[:1500], prob, t0,
                             score=0, max_score=g["max_score"])
            else:
                passed = 0
                total_ms = 0
                max_mem = 0
                overall = "AC"
                first_fail = ""
                ce_or_ie = ""
                verdicts: list[str] = []
                details: list[str] = []
                per_case: list[tuple] = []

                for i, c in enumerate(cases):
                    stdin_bytes = (c["stdin"] or "").encode("utf-8")
                    res = runner.run_case(workdir, stdin_bytes, limits)

                    if res.verdict == "OK":
                        cmp = compare(c["expected_stdout"] or "", res.stdout, checker, eps)
                        if cmp.ok:
                            v = "AC"
                            detail = cmp.detail
                        else:
                            v = "PE" if cmp.kind == "pe" else "WA"
                            detail = cmp.detail
                    else:
                        v = res.verdict
                        detail = res.detail
                        if v in ("CE", "IE"):
                            ce_or_ie = res.detail or res.stdout.decode("utf-8", "replace")

                    verdicts.append(v)
                    details.append(detail or "")
                    per_case.append((c, res))

                    if v == "AC":
                        passed += 1
                    elif overall == "AC":
                        overall = v
                        first_fail = detail

                    total_ms += res.time_ms
                    max_mem = max(max_mem, res.mem_kb)

                # ★ 得分 = 通过的测试点分值之和（不是「通过几个」）
                g = scoring.grade([c["points"] for c in cases], verdicts, total_score)

                for i, (c, res) in enumerate(per_case):
                    rows.append((
                        sid, c["id"], i, verdicts[i], g["points"][i], g["earned"][i],
                        res.time_ms, res.mem_kb,
                        res.stdout.decode("utf-8", "replace")[:_STORE_LIMIT],
                        res.stderr.decode("utf-8", "replace")[:_STORE_LIMIT],
                        c["expected_stdout"] or "", c["stdin"] or "",
                        res.exit_code, details[i][:1000],
                    ))

                message = first_fail or ce_or_ie
                self._finish(sid, overall, passed, total, total_ms, max_mem, message, prob, t0,
                             score=g["score"], max_score=g["max_score"])
        finally:
            db.executemany(
                "INSERT INTO submission_cases "
                "(submission_id, case_id, ord, verdict, points, earned, time_ms, mem_kb, "
                " stdout, stderr, expected, stdin, exit_code, detail) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                rows)
            sandbox.rmtree_force(workdir)

    # ---------- 汇总写回 ----------
    def _finish(self, sid: int, verdict: str, passed: int, total: int,
                time_ms: int, mem_kb: int, message: str, prob: dict, t0: float,
                score: int = 0, max_score: int = 0) -> None:
        judge_ms = int((time.perf_counter() - t0) * 1000)
        db.update("submissions", {
            "verdict": verdict,
            "score": int(score),
            "max_score": int(max_score),
            "passed": passed,
            "total": total,
            "time_ms": time_ms,
            "mem_kb": mem_kb,
            "message": (message or "")[:2000],
            "judged_at": db.now_iso(),
            "judge_ms": judge_ms,
        }, "id=?", (sid,))
        self._update_mastery(int(prob["id"]), verdict, int(score), int(max_score), sid,
                             int(prob.get("_uid") or 0))

    def _update_mastery(self, problem_id: int, verdict: str, score: int,
                        max_score: int, sid: int, user_id: int = 0) -> None:
        """更新**这个人**在这道题上的进度：最高分、最后提交、首次满分时间。

        best_submission_id / last_submission_id 是「打开题目自动回填代码」的依据：
        - last_*  → 回填你上次写的
        - best_*  → 回填你得最高分的那版（想找回最好解法时用）
        """
        uid = int(user_id or 0)
        if not uid:
            # 兜底：老提交（迁移前）或脚本直接塞的记录可能没 user_id
            # → 归到「本机用户」，不能让 FK 约束把判题搞崩
            uid = users.user_id_of(None)
        row = db.query_one("SELECT * FROM mastery WHERE user_id=? AND problem_id=?",
                           (uid, problem_id))
        now = db.now_iso()
        solved = verdict == "AC"

        if row:
            attempts = (row["attempts"] or 0) + 1
            ac_count = (row["ac_count"] or 0) + (1 if solved else 0)

            prev_best = int(row["best_score"] or 0)
            # 严格更高 → 换；同分且非零 → 也换成最新那次
            # （回填时想拿到「最近那版最好的解法」，而不是很久以前那版）
            better = score > prev_best or (score == prev_best and score > 0)
            if row["best_submission_id"] is None or better:
                best_sid = sid
            else:
                best_sid = row["best_submission_id"]
            best_score = max(prev_best, score)

            solved_at = row["solved_at"] or (now if solved else "")
            level = 2 if ac_count >= 2 else (1 if (best_score > 0 or attempts >= 2) else 0)

            db.execute("""
                UPDATE mastery SET attempts=?, ac_count=?, best_score=?,
                    best_submission_id=?, last_submission_id=?, last_verdict=?,
                    last_at=?, solved_at=?, level=?
                WHERE user_id=? AND problem_id=?
            """, (attempts, ac_count, best_score, best_sid, sid, verdict,
                  now, solved_at, level, uid, problem_id))
        else:
            db.insert("mastery", {
                "user_id": uid,
                "problem_id": problem_id,
                "attempts": 1,
                "ac_count": 1 if solved else 0,
                "best_score": score,
                "best_submission_id": sid,
                "last_submission_id": sid,
                "last_verdict": verdict,
                "last_at": now,
                "solved_at": now if solved else "",
                "level": 1 if score > 0 else 0,
            })


# ---------------- 模块级单例 ----------------
_worker: JudgeWorker | None = None
_lock = threading.Lock()


def get_worker() -> JudgeWorker:
    global _worker
    with _lock:
        if _worker is None:
            _worker = JudgeWorker()
        return _worker
