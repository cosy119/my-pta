"""首次启动写入种子题（幂等，按标题判重）。

这些题的期望输出全是手算核过的，不是「应该输出」。
P0 阶段它们同时也是判题器的自检样本。

分值模型（对齐 PTA）：
- 每题有 `total_score`（满分）
- 每个测试点有 `points`；不写就按满分**均分**（余数给前面的测试点）
- 得分 = 通过的测试点分值之和
"""
from __future__ import annotations

from . import db, scoring
from .question_types import infer as infer_question_type
from .problems_bank import BANK_PROBLEMS
from .problems_bank_cpp_prog import CPP_PROG_PROBLEMS
from .problems_bank_cpp_theory import CPP_THEORY_PROBLEMS
from .problems_bank_cpp_theory2 import CPP_THEORY2_PROBLEMS
from .problems_bank_cpp_tricks import CPP_TRICKS_PROBLEMS
from .problems_bank_ds import DS_PROBLEMS
from .problems_bank_ds_prog import DS_PROG_PROBLEMS
from .problems_bank_ds_theory import DS_THEORY_PROBLEMS
from .problems_bank_ds_tricks import DS_TRICKS_PROBLEMS
from .problems_bank_linux import LINUX_PROBLEMS
from .problems_bank_py_prog import PY_PROG_PROBLEMS
from .problems_bank_py_theory import PY_THEORY_PROBLEMS
from .problems_bank_py_theory2 import PY_THEORY2_PROBLEMS
from .problems_bank_py_tricks import PY_TRICKS_PROBLEMS

# 四条学习线。`subject` 是**学科维度**（不是语言）：
#   python → Python 线（解释执行）
#   ds     → 数据结构线（C / C++ 编译执行，教材是 C 语言版）
#   cpp    → C++ 基础线（郑莉《C++语言程序设计》第5版，12 讲）
#   linux  → Linux 线（理论题：选择 / 判断 / 命令填空）
SUBJECT_LABELS = {
    "python": "Python 快乐编程基础入门",
    "ds": "数据结构（C 语言版）",
    "cpp": "C++ 基础（语言程序设计）",
    "linux": "Linux 系统应用与开发",
}

# 核心题（平台自检用，也当入门题）
CORE_PROBLEMS: list[dict] = [
    {
        "title": "A+B 问题",
        "line": "python",
        "difficulty": 1,
        "total_score": 10,
        "source_section": "第 02 讲 · 编程基础",
        "tags": ["入门", "算术", "标准输入"],
        "statement_md": "读入两个整数，输出它们的和。\n\n这是最经典的入门题，用来确认输入输出通道是否通了。",
        "input_format": "一行，两个整数 `a` 和 `b`，用空格分隔。",
        "output_format": "一行，一个整数，表示 `a + b`。",
        "constraints_md": "-10^9 ≤ a, b ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "standard",
        "origin": "manual",
        "status": "published",
        "reference_solution": (
            "import sys\n\n"
            "a, b = map(int, sys.stdin.read().split())\n"
            "print(a + b)\n"
        ),
        "alt_solution": (
            "import sys\n"
            "\n"
            "v = sys.stdin.readline().split()\n"
            "sys.stdout.write(str(int(v[0]) + int(v[1])) + \"\\n\")\n"
        ),
        "cases": [
            {"stdin": "1 2\n", "expected_stdout": "3\n", "is_sample": 1,
             "kind": "sample", "explanation": "1 + 2 = 3"},
            {"stdin": "-5 3\n", "expected_stdout": "-2\n", "is_sample": 1,
             "kind": "sample", "explanation": "负数相加：-5 + 3 = -2"},
            {"stdin": "0 0\n", "expected_stdout": "0\n", "kind": "manual"},
            {"stdin": "1000000000 1000000000\n", "expected_stdout": "2000000000\n",
             "kind": "manual", "explanation": "上界：Python 整数无上限，不会溢出"},
            {"stdin": "-1000000000 -1000000000\n", "expected_stdout": "-2000000000\n",
             "kind": "manual"},
        ],
    },
    {
        "title": "区间求和",
        "line": "python",
        "difficulty": 2,
        "total_score": 20,
        "source_section": "第 03 讲 · 流程控制语句",
        "tags": ["数学", "公式", "性能"],
        "statement_md": (
            "给定若干组整数区间，对每组求区间内所有整数的和。\n\n"
            "看着简单，但**直接用循环累加会超时** —— 区间可能有 10^9 个数。"
        ),
        "input_format": (
            "第一行一个整数 `n`，表示区间个数。\n\n"
            "随后 `n` 行，每行两个整数 `a` `b`（保证 `a ≤ b`）。\n\n"
            "输入中可能有空行，按空白字符分割处理即可。"
        ),
        "output_format": "`n` 行，每行一个整数，表示区间 [a, b] 内所有整数之和。",
        "constraints_md": (
            "- n ≤ 10^5\n"
            "- -10^9 ≤ a ≤ b ≤ 10^9\n"
            "- 时间限制 400 ms —— 提示：用等差数列求和公式"
        ),
        "time_limit_ms": 400,
        "memory_limit_mb": 256,
        "checker": "standard",
        "origin": "manual",
        "status": "published",
        "reference_solution": (
            "import sys\n\n\n"
            "def main():\n"
            "    data = sys.stdin.read().split()\n"
            "    if not data:\n"
            "        return\n"
            "    n = int(data[0])\n"
            "    p = 1\n"
            "    out = []\n"
            "    for _ in range(n):\n"
            "        a = int(data[p])\n"
            "        b = int(data[p + 1])\n"
            "        p += 2\n"
            "        out.append((a + b) * (b - a + 1) // 2)\n"
            "    sys.stdout.write('\\n'.join(map(str, out)) + '\\n')\n\n\n"
            "main()\n"
        ),
        "alt_solution": (
            "import sys\n"
            "\n"
            "\n"
            "def main():\n"
            "    d = sys.stdin.read().split()\n"
            "    if not d:\n"
            "        return\n"
            "    n = int(d[0])\n"
            "    out = []\n"
            "    i = 1\n"
            "    while i < 1 + 2 * n:\n"
            "        a = int(d[i])\n"
            "        b = int(d[i + 1])\n"
            "        i += 2\n"
            "        out.append(b * (b + 1) // 2 - (a - 1) * a // 2)\n"
            "    sys.stdout.write(\"\\n\".join(map(str, out)) + \"\\n\")\n"
            "\n"
            "\n"
            "main()\n"
        ),
        "cases": [
            {"stdin": "1\n3 5\n", "expected_stdout": "12\n", "is_sample": 1,
             "kind": "sample", "explanation": "3 + 4 + 5 = 12"},
            {"stdin": "1\n-5 -3\n", "expected_stdout": "-12\n", "is_sample": 1,
             "kind": "sample", "explanation": "(-5) + (-4) + (-3) = -12"},
            {"stdin": "2\n1 1\n-3 -1\n", "expected_stdout": "1\n-6\n", "kind": "manual",
             "explanation": "单元素区间 1；以及 (-3)+(-2)+(-1) = -6"},
            {"stdin": "1\n0 0\n", "expected_stdout": "0\n", "kind": "manual"},
            {"stdin": "1\n-1000000000 1000000000\n", "expected_stdout": "0\n",
             "kind": "manual", "explanation": "对称区间，正负抵消得 0"},
        ],
    },
    {
        "title": "求平均值",
        "line": "python",
        "difficulty": 1,
        "total_score": 10,
        "source_section": "第 05 讲 · 列表与元组",
        "tags": ["算术", "浮点", "容差判题"],
        "statement_md": (
            "读入 `n` 个整数，输出它们的平均值。\n\n"
            "这题**不限制小数位数** —— 判题时按容差（1e-6）比较，"
            "你输出 `2`、`2.0` 还是 `2.000000` 都算对。"
        ),
        "input_format": "第一行一个整数 `n`。\n\n第二行 `n` 个整数，用空格分隔。",
        "output_format": "一行，平均值。小数位数不限。",
        "constraints_md": "- 1 ≤ n ≤ 1000\n- 每个数的绝对值 ≤ 10^9",
        "time_limit_ms": 1000,
        "memory_limit_mb": 256,
        "checker": "float",
        "float_eps": 1e-6,
        "origin": "manual",
        "status": "published",
        "reference_solution": (
            "import sys\n\n"
            "data = sys.stdin.read().split()\n"
            "n = int(data[0])\n"
            "nums = [int(x) for x in data[1:1 + n]]\n"
            "print(sum(nums) / n)\n"
        ),
        "alt_solution": (
            "import sys\n"
            "from functools import reduce\n"
            "\n"
            "d = sys.stdin.read().split()\n"
            "n = int(d[0])\n"
            "total = reduce(lambda acc, x: acc + int(x), d[1:1 + n], 0)\n"
            "sys.stdout.write(str(total / n) + \"\\n\")\n"
        ),
        "cases": [
            {"stdin": "3\n1 2 3\n", "expected_stdout": "2\n", "is_sample": 1,
             "kind": "sample", "explanation": "1+2+3 = 6，6/3 = 2"},
            {"stdin": "3\n1 1 2\n", "expected_stdout": "1.3333333333333333\n",
             "is_sample": 1, "kind": "sample", "explanation": "4/3 = 1.333333…（看你保留几位）"},
            {"stdin": "1\n-5\n", "expected_stdout": "-5\n", "kind": "manual"},
            {"stdin": "4\n-1 -2 -3 -4\n", "expected_stdout": "-2.5\n", "kind": "manual"},
            {"stdin": "2\n0 0\n", "expected_stdout": "0\n", "kind": "manual"},
        ],
    },
]


# 全部种子题 = 核心题 + 四条线的题库（含各线的技巧特训章与理论题章）
# 顺序就是前端默认展示顺序：Python → 数据结构 → C++ 基础 → Linux
SEED_PROBLEMS: list[dict] = (CORE_PROBLEMS + BANK_PROBLEMS
                             + PY_TRICKS_PROBLEMS + PY_THEORY_PROBLEMS + PY_THEORY2_PROBLEMS
                             + PY_PROG_PROBLEMS
                             + DS_PROBLEMS + DS_TRICKS_PROBLEMS + DS_THEORY_PROBLEMS
                             + DS_PROG_PROBLEMS
                             + CPP_TRICKS_PROBLEMS
                             + CPP_THEORY_PROBLEMS + CPP_THEORY2_PROBLEMS + CPP_PROG_PROBLEMS
                             + LINUX_PROBLEMS)



def ensure() -> int:
    """写种子题。返回新增条数（已存在则跳过，可反复调用）。

    ★ 整批走一个事务（db.bulk）：逐条 db.insert 会每条新开一次连接，
      320 道题 ≈ 1050 条 INSERT 实测 78 秒，云端冷启动顶掉健康检查。同批改一次提交。
    """
    added = 0
    with db.bulk() as conn:
        for raw in SEED_PROBLEMS:
            spec = dict(raw)
            cases = spec.pop("cases", [])
            # alt_solution 是「第二套独立实现」，只在 tools/verify_bank.py 里对拍用，
            # 平台运行不需要，所以不入库。
            spec.pop("alt_solution", None)
            title = spec["title"]
            if db.query_one("SELECT id FROM problems WHERE title = ?", (title,), conn=conn):
                continue

            spec["tags"] = db.jdumps(spec.get("tags", []))
            # 选择题的选项也存 JSON（空数组 = 不是选择题，前端据此决定渲染成选项还是编辑器）
            spec["choices"] = db.jdumps(spec.get("choices", []) or [])
            spec["question_type"] = infer_question_type(raw)
            spec["created_at"] = db.now_iso()
            # 没写 subject 的一律归 Python 线（核心题与早期题库都没写）
            spec.setdefault("subject", "python")
            spec.setdefault("status", "published")
            spec.setdefault("origin", "manual")
            spec.setdefault("checker", "standard")
            spec.setdefault("ref_interpreter", "py313")
            spec["total_score"] = int(spec.get("total_score") or 100)

            # 测试点分值：写了就用写的；没写就按满分均分（余数给前面的测试点）
            pts = scoring.normalize_points([c.get("points", 0) for c in cases],
                                           spec["total_score"])

            pid = db.insert("problems", spec, conn=conn)
            for i, c in enumerate(cases):
                db.insert("testcases", {
                    "problem_id": pid,
                    "ord": i,
                    "kind": c.get("kind", "manual"),
                    "stdin": c.get("stdin", ""),
                    "expected_stdout": c.get("expected_stdout", ""),
                    "is_sample": c.get("is_sample", 0),
                    "points": int(pts[i] if i < len(pts) else 0),
                    "explanation": c.get("explanation", ""),
                }, conn=conn)
            added += 1
    return added


def sync_question_types() -> int:
    """给老库补显式题型；种子题按题库定义同步，人工题保留已标注类型。"""
    seeded = {p["title"]: infer_question_type(p) for p in SEED_PROBLEMS}
    updated = 0
    for row in db.query(
            "SELECT id, title, line, choices, reference_solution, question_type FROM problems"):
        current = row.get("question_type") or ""
        wanted = seeded.get(row["title"])
        if wanted is None and not current:
            wanted = infer_question_type(row)
        if wanted is not None and current != wanted:
            db.execute("UPDATE problems SET question_type=? WHERE id=?", (wanted, row["id"]))
            updated += 1
    return updated


_LETTERS = "ABCDEFGH"


def backfill_choice_alts() -> int:
    """选择题：把**选项正文**补成可接受答案（幂等）。

    为什么需要
    ----------
    题库里单选题的期望值只有选项字母（`|B`），但界面上「点选一个选项」这种
    交互天然会想提交**选项正文**（「调用 compress（老式 .Z 格式）压缩」）。
    两种写法都是合理的，只认一种必然踩坑：
    前端点得再对也会被判 WA，而且看起来像判题器坏了。

    所以这里把字母对应的正文作为 `|` 备选追加进去 —— `oneof` 口径下
    两条路都通；判断题（对/错）的正文本来就是答案，跳过。
    """
    n = 0
    rows = db.query(
        "SELECT id, choices, question_type FROM problems "
        "WHERE line = 'text' AND COALESCE(choices, '[]') NOT IN ('[]', '')")
    for r in rows:
        choices = db.jloads(r["choices"], [])
        if len(choices) < 2 or r["question_type"] in ("true_false", "multiple_choice"):
            continue
        for c in db.query("SELECT id, expected_stdout FROM testcases WHERE problem_id = ?",
                          (r["id"],)):
            expected = c["expected_stdout"] or ""
            alts = [ln[1:].strip() for ln in expected.splitlines() if ln.startswith("|")]
            if not alts:
                continue
            add: list[str] = []
            for a in alts:
                up = a.strip().upper()
                if len(up) == 1 and up in _LETTERS[:len(choices)]:
                    txt = str(choices[_LETTERS.index(up)]).strip()
                    if txt and txt not in alts and txt not in add:
                        add.append(txt)
            if not add:
                continue          # 已经补过 → 幂等
            new = expected if expected.endswith("\n") else expected + "\n"
            new += "\n".join("|" + a for a in add) + "\n"
            db.execute("UPDATE testcases SET expected_stdout = ? WHERE id = ?", (new, c["id"]))
            n += 1
    return n


def _seed_specs() -> dict[str, tuple[int, list[int], str, str]]:
    """把 SEED_PROBLEMS 整理成 {标题: (满分, 逐点分值, 讲次, 学科)}，供升级时对账。"""
    out: dict[str, tuple[int, list[int], str, str]] = {}
    for raw in SEED_PROBLEMS:
        spec = dict(raw)
        cases = spec.pop("cases", [])
        total = int(spec.get("total_score") or 100)
        pts = scoring.normalize_points([c.get("points", 0) for c in cases], total)
        out[spec["title"]] = (total, pts, spec.get("source_section", ""),
                              spec.get("subject", "python"))
    return out


def backfill_points() -> int:
    """老库升级：让每道题的满分 / 测试点分值 / 对应讲次与 SEED 保持一致（幂等）。

    分两种情况：
    - **种子题**（标题在 SEED_PROBLEMS 里）：SEED 是权威，满分、逐点分值、讲次都按它同步。
      这样我改了题库设计（加题、调分值、改顺序），老库重启后就能跟上。
    - **其它题**：只在测试点分值**全为 0**（建题时没写）时，按满分均分兜底；
      已经有分值的一律不动，免得把人工设定冲掉。

    返回本次调整过的题目数。
    """
    fixed = 0
    specs = _seed_specs()

    for p in db.query(
            "SELECT id, title, total_score, source_section, subject FROM problems"):
        rows = db.query(
            "SELECT id, points FROM testcases WHERE problem_id=? ORDER BY ord, id",
            (p["id"],))
        if not rows:
            continue
        raw = [int(r["points"] or 0) for r in rows]

        if p["title"] in specs:
            want_total, want_pts, want_section, want_subject = specs[p["title"]]
            if len(want_pts) != len(rows):
                # 测试点数变了（SEED 增删了用例），按新数量重新均分
                want_pts = scoring.distribute_points(want_total, len(rows))
            same = (int(p["total_score"] or 0) == want_total
                    and raw == want_pts
                    and (p["source_section"] or "") == want_section
                    and (p["subject"] or "") == want_subject)
            if same:
                continue
            db.execute(
                "UPDATE problems SET total_score=?, source_section=?, subject=? WHERE id=?",
                (want_total, want_section, want_subject, p["id"]))
            for r, pt in zip(rows, want_pts):
                db.execute("UPDATE testcases SET points=? WHERE id=?", (pt, r["id"]))
            fixed += 1
            continue

        total = int(p["total_score"] or 0)
        if total <= 0:
            total = 100
            db.execute("UPDATE problems SET total_score=? WHERE id=?", (total, p["id"]))
        if sum(raw) > 0:
            continue
        for r, pt in zip(rows, scoring.distribute_points(total, len(rows))):
            db.execute("UPDATE testcases SET points=? WHERE id=?", (pt, r["id"]))
        fixed += 1
    return fixed


def backfill_legacy_scores() -> int:
    """把「打分制之前」的老提交换算成新口径（幂等）。

    老记录里 `score` 存的是**通过个数**、`max_score` 是 0。
    这里按当时的 passed/total 比例换算成得分，`max_score` 取题目当前满分 ——
    纯换算，不改判定，也不动 passed/total 本身。
    """
    rows = db.query("""
        SELECT s.id, s.passed, s.total, p.total_score
        FROM submissions s JOIN problems p ON p.id = s.problem_id
        WHERE COALESCE(s.max_score, 0) = 0 AND COALESCE(s.total, 0) > 0
    """)
    for r in rows:
        full = int(r["total_score"] or 100)
        total = int(r["total"] or 0)
        passed = int(r["passed"] or 0)
        score = int(round(full * passed / total)) if total else 0
        db.execute("UPDATE submissions SET max_score=?, score=? WHERE id=?",
                   (full, score, r["id"]))
    return len(rows)
