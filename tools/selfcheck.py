# -*- coding: utf-8 -*-
"""P0 自检：不开 Web 服务，直接验证判题内核。

跑法：
  D:\\Pythontools\\Python\\python.exe -X utf8 tools\\selfcheck.py

这是一份「真跑出证据」的脚本 —— 它不假设任何东西，全部靠真实进程的输出说话。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import config, db, seed, scoring              # noqa: E402
from app.judge import sandbox                          # noqa: E402
from app.judge.compare import compare                  # noqa: E402
from app.judge.runner_python import PythonRunner       # noqa: E402
from app.judge.runner_base import Limits               # noqa: E402
from app.judge.worker import get_worker                # noqa: E402

_ok: list[str] = []
_bad: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    (_ok if ok else _bad).append(name)
    print(("  [OK]   " if ok else "  [FAIL] ") + name + (("  -- " + str(detail)) if detail else ""))


def norm(b: bytes) -> str:
    return b.decode("utf-8", "replace").replace("\r\n", "\n")


cfg = config.get()
PY313 = cfg.interpreter_path("py313")
PY314 = cfg.interpreter_path("py314")

print("=" * 72)
print("P0 自检 | pta 根 =", ROOT)
print("=" * 72)

# ---------------------------------------------------------------- 1 配置
print("\n[1] 配置与解释器")
check("settings.toml 存在", cfg.config_path.exists(), cfg.config_path)
check("py313 解释器存在", Path(PY313).exists(), PY313)
check("py314 解释器存在", Path(PY314).exists(), PY314)
# 注意是 endswith(".db") 而不是 "pta.db" —— 测试库会叫 _bank_test.db，
# 卡死具体文件名会让「换库跑自检」这条路直接失败（那才是真正要保障的能力）
check("数据库路径可定位", str(cfg.db_path).endswith(".db"), cfg.db_path)
check("临时判题目录可定位", str(cfg.tmp_judge).endswith("judge"), cfg.tmp_judge)

# ---------------------------------------------------------------- 2 数据库
print("\n[2] 数据库")
dbp = db.init_db()
check("建表成功", dbp.exists(), f"{dbp}  {dbp.stat().st_size} 字节")
tables = [r["name"] for r in db.query(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
check("表数量 >= 9", len(tables) >= 9, ", ".join(tables))
first = seed.ensure()
second = seed.ensure()
check("种子题幂等（第二次返回 0）", second == 0, f"首次新增 {first}，第二次 {second}")
n_prob = db.query_one("SELECT COUNT(*) AS n FROM problems")["n"]
n_case = db.query_one("SELECT COUNT(*) AS n FROM testcases")["n"]
check("种子题数量正确", n_prob >= 2, f"题目 {n_prob} 道 / 用例 {n_case} 条")

# ---------------------------------------------------------------- 3 沙箱
print("\n[3] 沙箱（Job Object + 看门狗）")

r = sandbox.run([PY313, "-X", "utf8=1", "-c", "print('hi')"], time_limit_ms=5000)
check("普通运行退出码为 0", r.exit_code == 0, f"exit={r.exit_code}")
check("stdout 内容正确", norm(r.stdout) == "hi\n", repr(r.stdout))
check("Job Object 挂载成功", r.job_assigned, r.raw_note or "已挂载")

r = sandbox.run([PY313, "-X", "utf8=1", "-c", "print('中文测试')"], time_limit_ms=5000)
check("中文 UTF-8 输出正确", norm(r.stdout) == "中文测试\n", repr(r.stdout))

r = sandbox.run([PY313, "-X", "utf8=1", "-c", "while True: pass"], time_limit_ms=800)
check("死循环被判超时", r.timed_out, f"墙钟 {r.time_ms} ms（限额 800）")

r = sandbox.run([PY313, "-X", "utf8=1", "-c", "print(1//0)"], time_limit_ms=5000)
check("异常退出被判非零", r.exit_code != 0, f"exit={r.exit_code}")

big = ("x = []\n"
       "for _ in range(20):\n"
       "    x.append(b' ' * (10 * 1024 * 1024))\n"
       "print('跑完了', len(x))\n")
r = sandbox.run([PY313, "-X", "utf8=1", "-c", big], time_limit_ms=20000,
                memory_limit_mb=64)
check("爆内存被判为超限（MLE 而非 RE）",
      r.mem_exceeded and "跑完了" not in norm(r.stdout),
      f"峰值={r.mem_kb // 1024} MB / 限额 64 MB，超限标记={r.mem_exceeded}，exit={r.exit_code}")

# 进程树清理：起的子进程不能残留
r = sandbox.run([PY313, "-X", "utf8=1", "-c",
                 "import subprocess,sys;subprocess.run([sys.executable,'-c','pass']);print('done')"],
                time_limit_ms=8000)
check("能跑起孙进程并正常结束", norm(r.stdout).strip() == "done", repr(r.stdout))

# ---------------------------------------------------------------- 4 比对
print("\n[4] 输出比对（4 种口径）")

check("standard: 行尾空格被忽略",
      compare("a  \nb\n", "a\nb\n").ok)
check("standard: 末尾空行被忽略",
      compare("a\nb\n\n\n", "a\nb\n").ok)
check("standard: 真错判 WA",
      not compare("a\nb\n", "a\nc\n").ok)
check("standard: 中间空行不同 -> WA",
      not compare("a\n\nb\n", "a\nb\n").ok)
check("ignore_trailing: 行尾空格忽略",
      compare("a  \nb\n", "a\nb\n", "ignore_trailing").ok)
check("token: 全空白折叠",
      compare("1  2\n3\n", "1 2 3", "token").ok)
check("float: 容差内通过",
      compare("0.3333333\n", "0.33333334\n", "float", 1e-5).ok)
check("float: 超容差判错",
      not compare("1.0\n", "1.1\n", "float", 1e-6).ok)
cp = compare("a b\n", "a  \n b\n")
check("内容对但空白乱 -> PE", (not cp.ok) and cp.kind == "pe", cp.kind)
check("CRLF 与 LF 视为一致",
      compare("a\r\nb\r\n", "a\nb\n").ok)

# ---------------------------------------------------------------- 5 runner
print("\n[5] PythonRunner")

runner = PythonRunner(PY313, "py313")
wd = Path(cfg.tmp_judge) / "selfcheck_runner"
sandbox.rmtree_force(wd)
wd.mkdir(parents=True, exist_ok=True)

ok, msg = runner.prepare("def f(:\n    pass\n", wd)
check("语法错被 prepare 拦下", (not ok) and "SyntaxError" in msg, msg.splitlines()[-1] if msg else "")

ok, msg = runner.prepare("a, b = map(int, input().split())\nprint(a + b)\n", wd)
check("正常代码 prepare 通过", ok, msg)

res = runner.run_case(wd, b"3 4\n", Limits(time_ms=3000, memory_mb=128))
check("run_case 正常返回", res.verdict == "OK", res.verdict)
check("run_case 输出正确", norm(res.stdout).strip() == "7", repr(res.stdout))
sandbox.rmtree_force(wd)

base = runner.startup_baseline_ms()
check("能测出解释器启动基线", base > 0, f"{base} ms")

# ---------------------------------------------------------------- 6 端到端
print("\n[6] 端到端判题（直接调 worker.judge）")

w = get_worker()
pid = db.query_one("SELECT id FROM problems WHERE title = ?", ("A+B 问题",))["id"]


def submit_and_judge(code: str, interpreter: str = "py313") -> dict:
    sid = db.insert("submissions", {
        "problem_id": pid, "lang": "python", "interpreter": interpreter,
        "code": code, "verdict": "pending", "created_at": db.now_iso(),
    })
    w.judge(sid)
    return db.query_one("SELECT * FROM submissions WHERE id = ?", (sid,))


s = submit_and_judge("import sys\na, b = map(int, sys.stdin.read().split())\nprint(a + b)\n")
check("正确解判 AC", s["verdict"] == "AC", f"{s['verdict']} {s['passed']}/{s['total']}")

s = submit_and_judge("import sys\na, b = map(int, sys.stdin.read().split())\nprint(a - b)\n")
check("错误解判 WA", s["verdict"] == "WA", f"{s['verdict']} {s['passed']}/{s['total']}  {s['message'][:50]}")

s = submit_and_judge("import sys\nprint(1 // 0)\n")
check("除零判 RE", s["verdict"] == "RE", f"{s['verdict']}  {s['message'][:60]}")

s = submit_and_judge("while True:\n    pass\n")
check("死循环判 TLE", s["verdict"] == "TLE", f"{s['verdict']}  {s['message'][:60]}")

s = submit_and_judge("def f(:\n    pass\n")
check("语法错判 CE", s["verdict"] == "CE", f"{s['verdict']}  {s['message'].splitlines()[-1][:50]}")

s = submit_and_judge("x = []\nfor _ in range(40):\n    x.append(b' ' * (10 * 1024 * 1024))\n"
                     "print('done')\n")
check("爆内存判 MLE（不是 RE）", s["verdict"] == "MLE",
      f"{s['verdict']} 峰值 {s['mem_kb'] // 1024} MB / 限额 {db.query_one('SELECT memory_limit_mb m FROM problems WHERE id=?', (pid,))['m']} MB")

ac_sub = db.query_one("SELECT id FROM submissions WHERE verdict='AC' ORDER BY id DESC LIMIT 1")
n_ac_cases = len(db.query("SELECT id FROM submission_cases WHERE submission_id = ?",
                          (ac_sub["id"],))) if ac_sub else 0
check("AC 那次写入了全部 5 条用例明细", n_ac_cases == 5, f"{n_ac_cases} 条")

# 双解释器：同一份代码两边都判一遍
s13 = submit_and_judge("import sys\na, b = map(int, sys.stdin.read().split())\nprint(a + b)\n", "py313")
s14 = submit_and_judge("import sys\na, b = map(int, sys.stdin.read().split())\nprint(a + b)\n", "py314")
check("3.13 判 AC", s13["verdict"] == "AC", s13["verdict"])
check("3.14（Thonny 环境）判 AC", s14["verdict"] == "AC", s14["verdict"])

# ---------------------------------------------------------------- 7 评分
print("\n[7] 评分：分值 / 部分正确 / 进度 / 历史")


def judge_code(problem_id: int, code: str, interpreter: str = "py313") -> dict:
    """指定题目提交并同步判完（评分节专用）。"""
    sid = db.insert("submissions", {
        "problem_id": problem_id, "lang": "python", "interpreter": interpreter,
        "code": code, "verdict": "pending", "created_at": db.now_iso()})
    get_worker().judge(sid)
    return db.query_one("SELECT * FROM submissions WHERE id=?", (sid,))


# --- 分值分配 ---
check("100 分 5 个测试点 → 全 20", scoring.distribute_points(100, 5) == [20] * 5)
check("100 分 6 个测试点 → 余数给前面",
      scoring.distribute_points(100, 6) == [17, 17, 17, 17, 16, 16])
check("10 分 3 个测试点 → [4,3,3]", scoring.distribute_points(10, 3) == [4, 3, 3])
check("分值总和恒等于满分（1~12 个点 × 10/20/100 分）",
      all(sum(scoring.distribute_points(t, n)) == t
          for t in (10, 20, 100) for n in range(1, 13)))
check("测试点分值全 0 → 按满分均分兜底",
      scoring.normalize_points([0, 0, 0, 0], 100) == [25, 25, 25, 25])
check("已有分值 → 原样采用（不覆盖人工设定）",
      scoring.normalize_points([30, 30, 40], 100) == [30, 30, 40])

# --- 测试点分值真的落库了 ---
sc_p = db.query_one("SELECT id, total_score FROM problems WHERE title = 'A+B 问题'")
sc_pts = [r["points"] for r in db.query(
    "SELECT points FROM testcases WHERE problem_id=? ORDER BY ord, id", (sc_p["id"],))]
check("测试点分值落库且合计 = 题目满分",
      sum(sc_pts) == sc_p["total_score"], f"{sc_pts} 合计 {sum(sc_pts)} / 满分 {sc_p['total_score']}")

# --- 部分正确 ---
PARTIAL_CODE = ("import sys\n"
                "a, b = map(int, sys.stdin.read().split())\n"
                "print(a + b if abs(a) < 10**6 else 0)\n")
sp = judge_code(sc_p["id"], PARTIAL_CODE)
expect_partial = sum(sc_pts[:3])
check("部分正确：得分 = 通过的测试点分值之和（不是「通过几个」）",
      sp["score"] == expect_partial and sp["score"] != sp["passed"],
      f"score={sp['score']} 期望={expect_partial} passed={sp['passed']}")
check("部分正确：max_score = 满分", sp["max_score"] == sc_p["total_score"])
check("部分正确被识别出来", scoring.is_partial(sp["score"], sp["max_score"]))
check("状态文案 = 「部分正确」",
      scoring.verdict_label(sp["verdict"], sp["score"], sp["max_score"]) == "部分正确",
      scoring.verdict_label(sp["verdict"], sp["score"], sp["max_score"]))

sp_cases = db.query("SELECT ord, verdict, points, earned FROM submission_cases "
                    "WHERE submission_id=? ORDER BY ord", (sp["id"],))
check("逐点明细带 points / earned",
      all(c["points"] > 0 for c in sp_cases)
      and sum(c["earned"] for c in sp_cases) == sp["score"],
      f"{[(c['ord'], c['points'], c['earned']) for c in sp_cases]}")

# --- 满分 / 零分 ---
sf = judge_code(sc_p["id"], "import sys\na, b = map(int, sys.stdin.read().split())\nprint(a + b)\n")
check("全对：得分 = 满分、判定 AC",
      sf["score"] == sc_p["total_score"] and sf["verdict"] == "AC",
      f"{sf['verdict']} {sf['score']}/{sf['max_score']}")

sz = judge_code(sc_p["id"], "print(1)\n")
check("全错：得分 0", sz["score"] == 0, f"score={sz['score']}")

# --- 每题进度 ---
m = db.query_one("SELECT * FROM mastery WHERE problem_id=?", (sc_p["id"],))
check("best_score 不被后来的低分冲掉", m["best_score"] == sc_p["total_score"],
      f"best={m['best_score']}")
check("best_submission_id 指向最高分那次", m["best_submission_id"] == sf["id"],
      f"best={m['best_submission_id']} 满分那次={sf['id']}")
check("last_submission_id 指向最后一次", m["last_submission_id"] == sz["id"],
      f"last={m['last_submission_id']} 最后={sz['id']}")
check("solved_at 记录了首次满分时间", bool(m["solved_at"]), m["solved_at"])

# --- 历史 ---
hist = db.query("SELECT id, score, max_score FROM submissions WHERE problem_id=? "
                "ORDER BY id DESC", (sc_p["id"],))
check("每次提交都留档（>=3 条）", len(hist) >= 3, f"{len(hist)} 条")
check("历史每条都带 score/max_score", all(h["max_score"] > 0 for h in hist))
check("详情接口能取回可回填的代码",
      (db.query_one("SELECT code FROM submissions WHERE id=?", (sz["id"],)) or {}).get("code")
      == "print(1)\n")

# ---------------------------------------------------------------- 收尾
print("\n" + "=" * 72)
print(f"通过 {len(_ok)} 项，失败 {len(_bad)} 项")
if _bad:
    print("失败清单：")
    for b in _bad:
        print("  -", b)
print("=" * 72)
sys.exit(1 if _bad else 0)
