"""题目接口：列表 / 详情 / 平台元信息。

★ 多用户（2026-10-13）：题库是**大家共用**的，进度（mastery）是**每人一份**。
  所有带进度的接口都按 `X-User-Token` 过滤。
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request

from .. import config, db, users
from ..question_types import LABELS as QUESTION_TYPE_LABELS
from ..section_order import build_ranks, rank_of, ranks_from_db
from ..seed import SUBJECT_LABELS

router = APIRouter(prefix="/api", tags=["problems"])

# 科目展示顺序：Python → 数据结构 → C++ → Linux
SUBJECT_ORDER = {"python": 0, "ds": 1, "cpp": 2, "linux": 3}

# 题目的语言选项：由 `line` 推导出「这道题能用哪些语言提交」
# ★ 数据结构线是重点：`cpp` 表示**编译型**，学生可以用 C **或** C++ 交，
#   两条路走不同的编译器（见 app/judge/runner_cpp.py）
LANG_OPTIONS = {
    "python": [{"lang": "python", "label": "Python", "hint": "解释执行"}],
    "cpp": [
        {"lang": "cpp", "label": "C++ (g++)", "hint": "-std=c++17"},
        {"lang": "c", "label": "C (gcc)", "hint": "-std=gnu11"},
    ],
    "c": [{"lang": "c", "label": "C (gcc)", "hint": "-std=gnu11"}],
    "text": [],
}


def current_user(request: Request) -> dict:
    """从 X-User-Token 解析当前用户（首见即注册）。"""
    return users.resolve(request.headers.get("x-user-token")) or {}


def lang_options_for(line: str) -> list[dict]:
    return LANG_OPTIONS.get(str(line or "python").lower(), LANG_OPTIONS["python"])


def _subject_key(subject) -> int:
    return SUBJECT_ORDER.get(str(subject or "python"), 9)


#: `/api/problems` 支持的排序方式。
#:   chapter         —— 按章节（教学路径：科目 → 分节序号 → 组内难度 → 录入序），**默认**
#:   difficulty      —— 按难度（易 → 难）：科目 → 难度 → 分节序号 → 录入序
#:   difficulty_desc —— 按难度（难 → 易）：科目 → 难度倒序 → 分节序号 → 录入序
#: ★ 前端 `web/index.html::SORT_MODES` 的 key 必须是这里的子集，
#:   `tools/check_sort_modes.py` 守这条。
SORT_MODES = ("chapter", "difficulty", "difficulty_desc")
DEFAULT_SORT = "chapter"


def _difficulty_of(row: dict) -> int:
    """难度取值，脏数据一律当 1（最易），避免排序时 TypeError。"""
    try:
        return int(row.get("difficulty") or 1)
    except (TypeError, ValueError):
        return 1


# 分节教学序号的缓存：{ (subject, section) -> rank }
# 题目表变动不频繁，但 /api/problems 每次请求都要排序，所以缓存一份。
_RANKS_CACHE: dict[tuple[str, str], int] | None = None
_RANKS_STAMP: tuple | None = None


class _FastRanks:
    """进程级快取：给「只想要序号表、不关心戳」的调用方用。

    ★ `_section_ranks()` 每次调用都要打两次库（算戳 + 重建），
      在排序这种「逐题调用」的场景里就是 1440 倍开销。
      这里只缓存结果本身、不做失效检测 —— 题目表变动不频繁，
      真变了重启后端即可（Render 每次部署本来就是新进程）。
    """

    _data: dict | None = None

    @classmethod
    def get(cls) -> dict:
        if cls._data is None:
            cls._data = _section_ranks()
        return cls._data

    @classmethod
    def reset(cls) -> None:
        cls._data = None


_RANKS_FAST = _FastRanks


def _section_ranks() -> dict[tuple[str, str], int]:
    """算出每个分节的「教学路径序号」。

    ★ 为什么不用 `lecOf()`（从分节名抠「第 N 讲」）：
      没有讲次号的分组（C++ 线的「C++ 编程 · X」、Linux 线的「命令特训 · X」）
      一律返回 0，会被挤到所有讲次**前面**，彼此再按拼音排 —— 学习路径全乱。
      详见 `app/section_order.py`。
    """
    global _RANKS_CACHE, _RANKS_STAMP
    # ★ 戳用**轻量查询**：只取「已发布题数 + 最大 id + 难度总和」。
    #   早先用 GROUP BY 算戳（题数/均难/最小 id），每次调用 74ms ——
    #   而排序时会逐题调用，等于把接口从 0.4 秒拖到 64 秒。
    light = db.query("""
        SELECT COUNT(*) AS n, COALESCE(MAX(id), 0) AS mx,
               COALESCE(SUM(COALESCE(difficulty, 0)), 0) AS ds
        FROM problems WHERE status='published'
    """)[0]
    stamp = (light["n"], light["mx"], light["ds"])
    if _RANKS_CACHE is not None and _RANKS_STAMP == stamp:
        return _RANKS_CACHE

    rows = db.query("""
        SELECT subject, source_section AS sec, COUNT(*) AS n,
               AVG(difficulty) AS av, MIN(id) AS mn
        FROM problems WHERE status='published'
        GROUP BY subject, source_section
    """)
    pairs = {(r["subject"] or "python", r["sec"] or "") for r in rows}
    stats = {(r["subject"] or "python", r["sec"] or ""): float(r["av"] or 0) for r in rows}
    _RANKS_CACHE = build_ranks(pairs, stats)
    _RANKS_STAMP = stamp
    return _RANKS_CACHE


def section_ranks_payload() -> dict[str, dict[str, int]]:
    """把分节序号摊成 ``{科目: {分节名: 序号}}``，方便前端直接 JSON 化。"""
    out: dict[str, dict[str, int]] = {}
    for (subject, section), rank in sorted(_section_ranks().items(), key=lambda kv: kv[1]):
        out.setdefault(subject, {})[section] = int(rank)
    return out


def _order_key(row: dict, ranks: dict | None = None) -> tuple:
    """学习顺序：科目 → 分节教学路径 → **难度** → 录入顺序。

    ★ 为什么组内用 `difficulty` 而不是 `id`：
      用户要「按难易程度排」，同一分节内就该从易到难。
      同难度时用 `id` 兜底，保证顺序稳定（不会因为难度的细微调整而抖动）。

    ★ `ranks` **强烈建议提前算好传进来**：
      不传时走下面的进程级快取（几乎零成本）；
      但如果每次都现查库（`_section_ranks()` 里那两次 SQL），
      逐题调用 1440 次就是 **60 秒** —— 早期版本真踩过这个坑。
    """
    subject = str(row.get("subject") or "python")
    section = str(row.get("source_section") or "")
    if ranks is None:
        ranks = _RANKS_FAST.get()
    rank = rank_of(ranks, subject, section)
    return (_subject_key(subject), rank, _difficulty_of(row), row["id"])


def _difficulty_key(row: dict, ranks: dict | None = None, desc: bool = False) -> tuple:
    """难度序：科目 → 难度 → 分节教学路径 → 录入序。

    ★ 与 `_order_key` 的差别只在**难度提到分节之前**：
      章节序是「跟着教材走」（同一节内由易到难），
      难度序是「横着刷题」（全科最容易的先做，同难度再按教材顺序）。

    ★ 同难度为什么还要回落 `rank` + `id`：
      只按难度排，同难度内顺序由 Python 的稳定排序决定 —— 取决于 SQL 出来的
      原始顺序（`ORDER BY p.id`），结果是「按录入序」。这能跑，但一旦将来改了
      上游查询的顺序，同难度内的排列就会悄悄变。显式写死 `rank, id` 才稳。
    """
    subject = str(row.get("subject") or "python")
    if ranks is None:
        ranks = _RANKS_FAST.get()
    diff = _difficulty_of(row)
    rank = rank_of(ranks, subject, row.get("source_section"))
    return (_subject_key(subject), -diff if desc else diff, rank, row["id"])


def _sort_key(row: dict, ranks: dict | None = None, mode: str = DEFAULT_SORT) -> tuple:
    """统一入口：按 mode 选排序键。默认 `chapter` = 原来的行为，一字不改。"""
    if mode == "difficulty":
        return _difficulty_key(row, ranks, desc=False)
    if mode == "difficulty_desc":
        return _difficulty_key(row, ranks, desc=True)
    return _order_key(row, ranks)


@router.get("/me")
def me(user: dict = Depends(current_user)):
    """当前身份 + 这个人自己的进度概况。前端启动时拉一次。"""
    uid = int(user.get("id") or 0)
    s = users.summary(uid)
    return {
        "id": uid,
        "nickname": user.get("nickname") or "",
        "token": (user.get("token") or "")[:8] + "…",   # 只回前 8 位，别把整串 token 到处传
        "attempts": s["attempts"],
        "accepted": s["accepted"],
        "score": s["score"],
        "max_score": s["max_score"],
    }


@router.post("/me")
def rename_me(body: dict, user: dict = Depends(current_user)):
    """给这份进度起个名字，方便在界面上认出来。"""
    users.rename(int(user.get("id") or 0), str(body.get("nickname") or ""))
    return {"ok": True}


@router.get("/meta")
def meta():
    """前端启动时拉一次：可选语言、解释器、平台信息。"""
    cfg = config.get()
    interps = cfg.interpreters
    langs = [
        {
            "lang": "python",
            "label": "Python",
            "default": interps.get("default", "py313"),
            "interpreters": [
                {"key": "py313",
                 "label": "Python 3.13.14（讲义实测环境）",
                 "path": interps.get("py313", "")},
                {"key": "py314",
                 "label": "Python 3.14.4（Thonny 自带）",
                 "path": interps.get("py314", "")},
            ],
        },
        {
            # ★ 数据结构线：同一道题 C 和 C++ 都能交，走不同的编译器
            "lang": "cpp",
            "label": "C++ (g++)",
            "default": "gpp",
            "interpreters": [
                {"key": "gpp", "label": "g++ -std=c++17",
                 "path": cfg.compiler_path("gpp")},
            ],
        },
        {
            "lang": "c",
            "label": "C (gcc)",
            "default": "gcc",
            "interpreters": [
                {"key": "gcc", "label": "gcc -std=gnu11",
                 "path": cfg.compiler_path("gcc")},
            ],
        },
        {
            # 理论题（选择 / 判断 / 填空）：提交内容即答案，不需要任何运行时
            "lang": "text",
            "label": "文本答案",
            "default": "text",
            "interpreters": [],
        },
    ]
    return {
        "langs": langs,
        "question_types": [{"key": k, "label": v} for k, v in QUESTION_TYPE_LABELS.items()],
        "subjects": [{"key": k, "label": v} for k, v in SUBJECT_LABELS.items()],
        # ★ 分节教学路径序号：前端按它排分组顺序，静态站从 problems.json 取同一份
        "section_ranks": section_ranks_payload(),
        "port": cfg.port,
        "db": str(cfg.db_path),
        "paths": {
            "settings": str(cfg.config_path),
            "tmp_judge": str(cfg.tmp_judge),
        },
        "limits": {
            "default_time_limit_ms": cfg.default_time_limit_ms,
            "default_memory_limit_mb": cfg.default_memory_limit_mb,
            "max_output_bytes": cfg.max_output_bytes,
        },
    }


@router.get("/catalog")
def catalog(user: dict = Depends(current_user)):
    """科目目录：科目 → 分组（讲次 / 实验 / 基础命令）→ 题数与我的进度。

    前端主界面（题集广场）用它渲染卡片和进度条，一次请求就够，
    不用把整个题库拉下来再自己聚合。
    """
    uid = int(user.get("id") or 0)
    rows = db.query("""
        SELECT p.subject, p.line, p.source_section, p.total_score, p.difficulty,
               COALESCE(m.best_score, 0) AS best_score,
               m.solved_at               AS solved_at,
               COALESCE(m.attempts, 0)   AS attempts
        FROM problems p
        LEFT JOIN mastery m ON m.problem_id = p.id AND m.user_id = ?
        WHERE p.status = 'published'
    """, (uid,))

    subs: dict[str, dict] = {}
    for r in rows:
        key = str(r["subject"] or "python")
        s = subs.setdefault(key, {
            "key": key,
            "label": SUBJECT_LABELS.get(key, key),
            "total": 0, "solved": 0, "attempted": 0,
            "score": 0, "max_score": 0,
            "difficulty": {}, "lines": {},
            "sections": {},
        })
        s["total"] += 1
        s["score"] += int(r["best_score"] or 0)
        s["max_score"] += int(r["total_score"] or 0)
        if r["solved_at"]:
            s["solved"] += 1
        if int(r["attempts"] or 0) > 0:
            s["attempted"] += 1
        s["difficulty"][str(r["difficulty"] or 1)] = \
            s["difficulty"].get(str(r["difficulty"] or 1), 0) + 1
        s["lines"][str(r["line"] or "python")] = \
            s["lines"].get(str(r["line"] or "python"), 0) + 1

        # 分组名：优先用讲义讲次（「第 03 讲 · 流程控制语句」），
        # 没有讲次号的（基础命令 / 实验 N）就按 section 原文分组
        sec = str(r["source_section"] or "未分组")
        g = s["sections"].setdefault(sec, {
            "name": sec, "total": 0, "solved": 0, "score": 0, "max_score": 0,
        })
        g["total"] += 1
        g["score"] += int(r["best_score"] or 0)
        g["max_score"] += int(r["total_score"] or 0)
        if r["solved_at"]:
            g["solved"] += 1

    out = []
    ranks = _section_ranks()
    for key, s in subs.items():
        secs = list(s.pop("sections").values())
        # 组内顺序：按**分节教学路径**（讲次线 → 编程册 → 技巧特训 …）
        secs.sort(key=lambda x: rank_of(ranks, key, x["name"]))
        s["sections"] = secs
        out.append(s)
    out.sort(key=lambda x: _subject_key(x["key"]))
    return {"subjects": out, "user_score": sum(x["score"] for x in out),
            "user_max_score": sum(x["max_score"] for x in out)}


@router.get("/problems")
def list_problems(line: str | None = None, status: str | None = None,
                  subject: str | None = None, q: str | None = None,
                  question_type: str | None = None,
                  sort: str | None = None,
                  user: dict = Depends(current_user)):
    # 排序方式：默认按章节，可选按难度（易→难 / 难→易）
    mode = (sort or DEFAULT_SORT).strip().lower()
    if mode not in SORT_MODES:
        raise HTTPException(
            status_code=400,
            detail="未知排序方式：%s（可选：%s）" % (sort, " / ".join(SORT_MODES)))
    uid = int(user.get("id") or 0)
    sql = """
        SELECT p.id, p.subject, p.line, p.question_type, p.title, p.difficulty, p.tags,
               p.origin, p.status, p.choices,
               p.total_score,
               p.source_section, p.source_anchor, p.created_at,
               COALESCE(m.attempts, 0)   AS attempts,
               COALESCE(m.ac_count, 0)   AS ac_count,
               COALESCE(m.level, 0)      AS level,
               COALESCE(m.best_score, 0) AS best_score,
               COALESCE(m.is_starred, 0) AS is_starred,
               COALESCE(m.last_verdict, '') AS last_verdict,
               m.solved_at               AS solved_at,
               (SELECT COUNT(*) FROM testcases t WHERE t.problem_id = p.id) AS testcase_count
        FROM problems p
        LEFT JOIN mastery m ON m.problem_id = p.id AND m.user_id = ?
        WHERE 1 = 1
    """
    params: list = [uid]
    if line:
        sql += " AND p.line = ?"
        params.append(line)
    if subject:
        sql += " AND p.subject = ?"
        params.append(subject)
    if question_type:
        if question_type not in QUESTION_TYPE_LABELS:
            raise HTTPException(status_code=400, detail="未知题型")
        sql += " AND p.question_type = ?"
        params.append(question_type)
    if status:
        sql += " AND p.status = ?"
        params.append(status)
    if q:
        sql += " AND (p.title LIKE ? OR p.tags LIKE ?)"
        params += [f"%{q}%", f"%{q}%"]
    sql += " ORDER BY p.id ASC"

    rows = db.query(sql, params)
    ranks = _section_ranks()          # ★ 只算一次：逐题调用会打 1440 次库
    for r in rows:
        r["tags"] = db.jloads(r["tags"], [])
        r["choices"] = db.jloads(r["choices"], [])
        r["is_choice"] = bool(r["choices"])
        r["score_label"] = "%d/%d" % (r["best_score"] or 0, r["total_score"] or 0)
        r["solved"] = bool(r["solved_at"])
        r["langs"] = lang_options_for(r["line"])
    rows.sort(key=lambda r: _sort_key(r, ranks, mode))   # 默认章节序，可按难度
    return {"items": rows, "total": len(rows), "sort": mode}


@router.get("/problems/{pid}")
def get_problem(pid: int, user: dict = Depends(current_user)):
    uid = int(user.get("id") or 0)
    p = db.query_one("SELECT * FROM problems WHERE id=?", (pid,))
    if not p:
        raise HTTPException(status_code=404, detail="题目不存在")

    p["tags"] = db.jloads(p["tags"], [])
    p["choices"] = db.jloads(p["choices"], [])
    p["is_choice"] = bool(p["choices"])
    # 这道题能用哪些语言提交（数据结构线 = C / C++ 二选一）
    p["langs"] = lang_options_for(p["line"])
    p["subject_label"] = SUBJECT_LABELS.get(str(p["subject"] or "python"), "")
    p["samples"] = db.query(
        "SELECT id, ord, stdin, expected_stdout, explanation FROM testcases "
        "WHERE problem_id = ? AND is_sample = 1 ORDER BY ord, id", (pid,))

    cnt = db.query_one(
        "SELECT COUNT(*) AS n, SUM(CASE WHEN is_sample = 0 THEN 1 ELSE 0 END) AS hidden, "
        "       SUM(COALESCE(points, 0)) AS pts "
        "FROM testcases WHERE problem_id = ?", (pid,))
    p["testcase_count"] = (cnt or {}).get("n", 0) or 0
    p["hidden_count"] = (cnt or {}).get("hidden", 0) or 0

    # 测试点分值：库里可能是 0（老数据），用题目满分兜底算一份展示用
    from .. import scoring
    raw = db.query("SELECT points FROM testcases WHERE problem_id=? ORDER BY ord, id", (pid,))
    p["case_points"] = scoring.normalize_points([r["points"] for r in raw],
                                                int(p["total_score"] or 100))
    p["points_sum"] = sum(p["case_points"])

    # ---------- 每题进度 + 历史（★ 只看当前用户的） ----------
    m = db.query_one("SELECT * FROM mastery WHERE user_id=? AND problem_id=?",
                     (uid, pid)) or {}
    p["mastery"] = m
    p["best_score"] = int(m.get("best_score") or 0)
    p["solved_at"] = m.get("solved_at") or ""
    p["solved"] = bool(p["solved_at"])

    # 打开题目时回填用的「最后一次提交」（自己的）
    p["last_submission"] = None
    if m.get("last_submission_id"):
        p["last_submission"] = db.query_one(
            "SELECT id, verdict, score, max_score, passed, total, lang, interpreter, "
            "       code, created_at, judged_at FROM submissions WHERE id=? AND user_id=?",
            (m["last_submission_id"], uid))

    # 历史提交（每次提交都留档，默认给最近 50 条；★ 只看自己的）
    p["history"] = db.query(
        "SELECT id, verdict, score, max_score, passed, total, lang, interpreter, "
        "       time_ms, mem_kb, created_at, judged_at "
        "FROM submissions WHERE user_id=? AND problem_id=? ORDER BY id DESC LIMIT 50",
        (uid, pid))

    p["history_count"] = (db.query_one(
        "SELECT COUNT(*) AS n FROM submissions WHERE user_id=? AND problem_id=?",
        (uid, pid)) or {}).get("n", 0)

    # 参考解不外传（留着自己判题和日后回看用）
    p.pop("reference_solution", None)
    return p


@router.get("/lectures")
def list_lectures(line: str | None = None):
    """讲义索引（P3 出题用；先给个读接口，方便前端展示回链目标）。"""
    sql = "SELECT id, path, line, title, scanned_at FROM lectures"
    params: list = []
    if line:
        sql += " WHERE line = ?"
        params.append(line)
    return {"items": db.query(sql + " ORDER BY id", params)}
