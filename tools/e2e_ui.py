"""端到端过一遍 HTTP 接口：三道题各走一次「提交 -> 轮询 -> 拿结果」。

★ 只对着**测试库**（data/_bank_test.db）跑，绝不碰用户的真实进度。
  验证的是前端真正会走的那条路：
    POST /api/submissions  ->  GET /api/submissions/<id>?with_cases=1
  再加上 GET /api/catalog /api/problems 的分类字段。

★ 目录那一节的期望值（题数 / 满分 / 分组数 / 顺序）**从题库定义现算**
  （`bank_stats()` 读 `app.seed.SEED_PROBLEMS`），不写死数字。写死的后果是
  题库一加题这里就报假红，红多了就没人看它了。

用法：
    python tools/e2e_ui.py            # 默认 http://127.0.0.1:8792
    python tools/e2e_ui.py 8793
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))     # 为了能 import _console
import _console                                               # noqa: E402
import _testdb                                                # noqa: E402  （只用它的 guard_live_db）

# 期望值要从**题库定义**里读（见 bank_stats），所以要能 import app.*
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.api.problems import _order_key                        # noqa: E402
from app.seed import SEED_PROBLEMS, SUBJECT_LABELS             # noqa: E402

PORT = sys.argv[1] if len(sys.argv) > 1 else "8792"
BASE = f"http://127.0.0.1:{PORT}"

# ★ 每次跑用一个**新的通行证**：进度是按人存的，复用同一个 token 会让
#   「这个人目前总分 = 15」这类断言在第二次运行时被上一次的记录污染
TOKEN = "eeee%028x" % (time.time_ns() & ((1 << 112) - 1))
OTHER_TOKEN = "ffff%028x" % ((time.time_ns() + 7) & ((1 << 112) - 1))

OK = 0
BAD = 0


def check(name: str, cond: bool, extra: str = "") -> None:
    global OK, BAD
    if cond:
        OK += 1
        print(f"  [PASS] {name}" + (f"  {extra}" if extra else ""))
    else:
        BAD += 1
        print(f"  [FAIL] {name}" + (f"  {extra}" if extra else ""))


def req(path: str, body=None, method=None):
    url = BASE + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    r = urllib.request.Request(url, data=data, method=method or ("POST" if data else "GET"))
    r.add_header("X-User-Token", TOKEN)
    if data:
        r.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def wait(sid: int, limit=120.0) -> dict:
    t0 = time.time()
    while time.time() - t0 < limit:
        s = req(f"/api/submissions/{sid}?with_cases=1")
        if s["verdict"] not in ("pending", "judging"):
            return s
        time.sleep(0.5)
    raise TimeoutError("判题超时")


def submit(pid: int, code: str, lang: str, interp: str) -> dict:
    r = req("/api/submissions", {"problem_id": pid, "code": code, "lang": lang,
                                 "interpreter": interp})
    return wait(r["id"])


def find_by_title(title: str) -> dict | None:
    items = req("/api/problems")["items"]
    for p in items:
        if p["title"] == title:
            return p
    return None


def bank_stats() -> dict:
    """从**题库定义**现算每个科目的（题数、满分、分组数）。

    ★ 为什么不写死数字：这里的期望值以前是「某天测出来的 2615 分 / ds 31 题」。
      题库一加题（现在的真实数字是 320 题 / 3945 分 / ds 71 题），这个端到端
      脚本立刻报一片红 —— 而它红的原因**不是产品坏了**。假失败报几次之后，
      就没人再认真看它的输出了，真出问题也发现不了。
      断言应当跟着「题库怎么写的」走，而不是跟着「上次跑出来多少」走。
    """
    out: dict = {}
    for p in SEED_PROBLEMS:
        key = str(p.get("subject") or "python")
        s = out.setdefault(key, {"total": 0, "max_score": 0, "sections": set()})
        s["total"] += 1
        s["max_score"] += int(p.get("total_score") or 0)
        s["sections"].add(str(p.get("source_section") or "未分组"))
    return out


EXPECT = bank_stats()

print(f"== 端到端验证 -> {BASE} ==")

# ★ 先问一句对面连的是哪个库。这个脚本**会真的写进去**（提交、进度），
#   如果对面是真实库，就会在你的刷题记录里塞测试数据。
#   我们决定不了服务用哪个库，但至少要说出来。
try:
    _h = req("/api/health")
    _warn = _testdb.guard_live_db(_h)
    print("  " + _warn.replace("\n", "\n  "))
    # ★ 别用「'真实库' in _warn」当判据 —— 安全的那句话里也写着「不是真实库，安全」，
    #   于是连测试库时也会多印一行「这次的数据进了真实库」，把不存在的事说得跟真的一样。
    #   认那条警告自己的标记（它以 ⚠️⚠️ 开头）。
    if _warn.startswith("⚠️"):
        print("  （继续跑，但请知悉：这次的数据进了真实库）")
except Exception as _e:  # noqa: BLE001
    print("  （读 /api/health 失败，跳过数据库归属检查：%s）" % _e)

# ---------------------------------------------------------------- 1. 目录
print("  （期望值来自题库定义：%s）" % "、".join(
    f"{k} {v['total']} 题/{len(v['sections'])} 组" for k, v in sorted(EXPECT.items())))
cat = req("/api/catalog")
keys = [s["key"] for s in cat["subjects"]]
check("catalog 三科目齐全且有序", keys == ["python", "ds", "linux"], str(keys))
want_score = sum(s["max_score"] for s in EXPECT.values())
check("catalog 总分 = 题库所有题的满分之和",
      cat["user_max_score"] == want_score,
      f"{cat['user_max_score']} / 期望 {want_score}")

for _key in ("ds", "linux"):
    _want = EXPECT[_key]
    _got = [s for s in cat["subjects"] if s["key"] == _key][0]
    check(f"{_key} 题数与分组数 = 题库定义",
          _got["total"] == _want["total"] and len(_got["sections"]) == len(_want["sections"]),
          f"{_got['total']} 题 / {len(_got['sections'])} 组"
          f"（期望 {_want['total']} / {len(_want['sections'])}）")

# ---------------------------------------------------------------- 2. 列表字段
items = req("/api/problems?subject=ds")["items"]
check("?subject=ds 只回 ds", all(p["subject"] == "ds" for p in items), f"{len(items)} 题")

# 「给了 C 与 C++ 两条路」说的是**编程题**，不是列表的第一题。
# 老写法拿 items[0] 断 langs —— DS 线补进「第 01 讲 · 绪论」那批理论题之后，
# 列表第一题变成理论题（langs 本来就该是空的），当场假失败。
prog_items = [p for p in items if p["langs"]]
check("数据结构编程题 langs 给了 C 与 C++ 两条路",
      bool(prog_items) and [l["lang"] for l in prog_items[0]["langs"]] == ["cpp", "c"],
      str(prog_items[0]["langs"]) if prog_items else "一道编程题都没有")

# 列表顺序是 `_order_key` 定的学习顺序（科目 → 讲次 → 录入顺序）。
# 这里**不重抄一遍排序规则**，直接借接口用的那个 key 去排题库，两边逐项比。
# 题库条目没有 id，用它在 SEED_PROBLEMS 里的位置当 id：
# 新库就是按这个顺序 insert 的（`ORDER BY p.id` 与题库顺序同构）。
# 老写法是「首题 source_section 以『第 02 讲』开头」—— 题库补了绪论就假死。
_bank_pos = {id(p): i for i, p in enumerate(SEED_PROBLEMS)}
want_titles = [str(p["title"]) for p in sorted(
    (p for p in SEED_PROBLEMS if str(p.get("subject") or "python") == "ds"),
    key=lambda p: _order_key({"subject": p.get("subject"),
                              "source_section": p.get("source_section"),
                              "id": _bank_pos[id(p)]}))]
got_titles = [p["title"] for p in items]
check("列表顺序 = 讲义讲次循序（与题库同一套排序键）",
      got_titles == want_titles,
      f"{items[0]['source_section']} 起，共 {len(got_titles)} 题")

lin = req("/api/problems?subject=linux")["items"]
check("Linux 理论题 is_choice 有值", any(p["is_choice"] for p in lin))
check("Linux 理论题 langs 为空（不用选语言）", lin[0]["langs"] == [], str(lin[0]["langs"]))

# ---------------------------------------------------------------- 3. 数据结构：同一题 C 与 C++ 各交一次
#
# ★ 题目 id **不写死**。id 只说明「这条题什么时候第一次被写进库」：
#   测试库是跟着题库一路 seed 过来的，id 早就漂了 —— 写死的 57 号
#   现在是一道 Python 题（「wc 三件套」），于是这里连着假报了好几项：
#   subject_label 拿到 Python 的标签、C/C++ 提交自然全 WA、
#   下游「取历史最高分 / 已解决 / 总分」跟着一起塌。
#   标题才是题目的身份 —— 按标题找 id，找不到就直接停机报错，别硬跑。
TARGET = "顺序表按位插入"
_target = find_by_title(TARGET)
if _target is None:
    raise SystemExit(f"[ABORT] 题库里找不到「{TARGET}」——题目改名了？改这个脚本的 TARGET")
PID = _target["id"]
print(f"  （目标题：{TARGET} -> id={PID}）")

pdet = req(f"/api/problems/{PID}")
check("数据结构题详情带 subject_label",
      pdet["subject_label"] == SUBJECT_LABELS["ds"], pdet["subject_label"])
check("题目详情不外泄参考解", "reference_solution" not in pdet)
check("样例已给（题面要用）", len(pdet["samples"]) >= 1, f"{len(pdet['samples'])} 个")
FULL = int(pdet["total_score"] or 0)          # 这道题的满分（后面断言不写死 15）

CPP = r"""
#include <cstdio>
int main(){int n; if(scanf("%d",&n)!=1) return 0;
 int a[100005]; for(int i=0;i<n;i++) scanf("%d",&a[i]);
 int i,x; scanf("%d %d",&i,&x);
 if(i<1||i>n+1){printf("error\n");return 0;}
 for(int j=n;j>=i;j--) a[j]=a[j-1];
 a[i-1]=x;
 for(int j=0;j<=n;j++) printf("%d%c",a[j], j==n?'\n':' ');
 return 0;}
"""
C = r"""
#include <stdio.h>
int main(void){int n; if(scanf("%d",&n)!=1) return 0;
 int a[100005]; for(int i=0;i<n;i++) scanf("%d",&a[i]);
 int i,x; if(scanf("%d %d",&i,&x)!=2) return 0;
 if(i<1||i>n+1){printf("error\n");return 0;}
 for(int j=n;j>=i;j--) a[j]=a[j-1];
 a[i-1]=x;
 for(int j=0;j<=n;j++) printf("%d%c",a[j], j==n?'\n':' ');
 return 0;}
"""
r_cpp = submit(PID, CPP, "cpp", "gpp")
print("  C++ ->", r_cpp["verdict"], r_cpp["score"], "/", r_cpp["max_score"],
      f"{r_cpp['passed']}/{r_cpp['total']}")
check("C++ 提交拿到 AC", r_cpp["verdict"] == "AC" and r_cpp["score"] == r_cpp["max_score"])

r_c = submit(PID, C, "c", "gcc")
print("  C   ->", r_c["verdict"], r_c["score"], "/", r_c["max_score"],
      f"{r_c['passed']}/{r_c['total']}")
check("C 提交拿到 AC（同一道题、不同编译器）",
      r_c["verdict"] == "AC" and r_c["score"] == r_c["max_score"])

# 两套语言各有一份自己的提交记录
subs = req(f"/api/submissions?problem_id={PID}&limit=10")["items"]
langs = {s["lang"] for s in subs}
check("两条提交分别记成 cpp / c", langs == {"cpp", "c"}, str(langs))
check("逐测试点明细条数 = 这道题的测试点数",
      len(r_c["cases"]) == pdet["testcase_count"],
      f"{len(r_c['cases'])} / {pdet['testcase_count']} 个")

check("每个测试点都带分值", all(c["points"] for c in r_c["cases"]),
      str([c["points"] for c in r_c["cases"]]))

# ---------------------------------------------------------------- 4. 部分正确（分值求和，不是通过个数）
HALF = CPP.replace("for(int j=0;j<=n;j++) printf", "a[0]=a[0];\n for(int j=0;j<=n;j++) printf")
BROKEN = r"""
#include <cstdio>
int main(){int n; if(scanf("%d",&n)!=1) return 0;
 int a[100005]; for(int i=0;i<n;i++) scanf("%d",&a[i]);
 int i,x; scanf("%d %d",&i,&x);
 if(n<=3){printf("9 1 2 3 4 5\n"); return 0;}
 for(int j=n;j>=i;j--) a[j]=a[j-1];
 a[i-1]=x;
 for(int j=0;j<=n;j++) printf("%d%c",a[j], j==n?'\n':' ');
 return 0;}
"""
r_bad = submit(PID, BROKEN, "cpp", "gpp")
print("  只对一部分 ->", r_bad["verdict"], r_bad["score"], "/", r_bad["max_score"],
      f"{r_bad['passed']}/{r_bad['total']}")
check("拿不到满分不是 AC", r_bad["score"] < r_bad["max_score"])
case_earned = sum(c["earned"] for c in r_bad["cases"])
check("得分 = 通过点的分值之和（不是个数×均分）",
      r_bad["score"] == case_earned,
      f"{r_bad['score']} == {case_earned}")
# ★ 竞态守卫：判定落库和逐测试点明细落库必须是同一时刻可见的 ——
#   否则前端轮询到的就是「结论有了、明细空着」，得手动刷新才补上
check("结论出来时逐测试点明细已经齐了（没有明细落库竞态）",
      len(r_bad["cases"]) == r_bad["total"],
      f"{len(r_bad['cases'])} / {r_bad['total']}")

# ---------------------------------------------------------------- 5. 进度按人隔离 + 取历史最高分
prog = req("/api/progress")
prow = [x for x in prog["items"] if x["id"] == PID][0]
# 前面已经交过两次满分（C++ / C），最后一次是只对一部分的 BROKEN：
# 取历史最高分意味着 best_score 应当是**这道题的满分**，不被后一次的 0 分冲掉。
check(f"进度取历史最高分（后面那次没满分，不影响 {FULL}）",
      prow["best_score"] == FULL and prow["solved_at"],
      f"best={prow['best_score']} / 满分 {FULL}")
check("满分题计入「已解决」", prog["solved"] >= 1 and prow["solved_at"] != "",
      f"solved={prog['solved']} attempted={prog['attempted']}")
me = req("/api/me")
check(f"my score ≥ 这道题的满分（{FULL}）", me["score"] >= FULL, str(me["score"]))
other = urllib.request.Request(BASE + "/api/me")
other.add_header("X-User-Token", OTHER_TOKEN)
with urllib.request.urlopen(other, timeout=20) as resp:
    me2 = json.loads(resp.read().decode("utf-8"))
check("换个通行证 = 另一个人，进度为 0", me2["score"] == 0 and me2["id"] != me["id"],
      f"{me2['id']} score={me2['score']}")

# ---------------------------------------------------------------- 6. Linux 理论题
lin_items = req("/api/problems?subject=linux")["items"]
mc = [p for p in lin_items if p["is_choice"]][0]
det = req(f"/api/problems/{mc['id']}")
check("选择题带 choices 选项", len(det["choices"]) >= 2, str(det["choices"]))
letters = "ABCDEFGH"
# 找出正确答案是第几个选项（从测试点 expected 里读，模拟判题器的口径）
EXPECTED = req(f"/api/problems/{mc['id']}")
sample_case = None
wrong = None
for i, c in enumerate(det["choices"]):
    r = submit(mc["id"], letters[i], "text", "text")
    if r["verdict"] == "AC":
        sample_case = i
        break
check("单选题：交**选项字母**能判对", sample_case is not None,
      f"正确答案 = {letters[sample_case] if sample_case is not None else '?'}")

if sample_case is not None:
    # ★ 同一个选项，改成交**选项正文**也必须判对（后端 backfill_choice_alts 兜底）
    r_txt = submit(mc["id"], det["choices"][sample_case], "text", "text")
    check("单选题：交**选项正文**同样判对", r_txt["verdict"] == "AC",
          f"{det['choices'][sample_case][:18]} -> {r_txt['verdict']}")
    for i in range(len(det["choices"])):
        if i == sample_case:
            continue
        r_bad = submit(mc["id"], letters[i], "text", "text")
        check(f"单选题：选项 {letters[i]} 判错", r_bad["verdict"] != "AC", r_bad["verdict"])
        break

# 判断题：交「对/错」正文
judge_items = [p for p in lin_items if p["is_choice"]
               and len(p.get("choices") or []) == 2 and "对" in (p.get("choices") or [])]
if judge_items:
    jp = judge_items[0]
    jdet = req(f"/api/problems/{jp['id']}")
    check("判断题给的是「对 / 错」两个选项", jdet["choices"] == ["对", "错"], str(jdet["choices"]))
    rj = submit(jp["id"], "对", "text", "text")
    check("判断题提交走理论题管道", rj["verdict"] in ("AC", "WA"), rj["verdict"])

# 填空题：交命令
fill_items = [p for p in lin_items if not p["is_choice"]]
if fill_items:
    fp = fill_items[0]
    check("填空题不用选语言（langs 为空）", fp["langs"] == [])
    rf = submit(fp["id"], "\x00definitely-wrong\x00", "text", "text")
    check("乱写的填空题判错", rf["verdict"] != "AC", rf["verdict"])

# ---------------------------------------------------------------- 7. 编译错误给人话
r_ce = submit(PID, "#include <cstdio>\nint main(){ 这不是C++ }", "cpp", "gpp")
check("CE 带编译器原话", r_ce["verdict"] == "CE" and bool(r_ce.get("message")
      or r_ce.get("compile_output")), (r_ce.get("message") or "")[:60])

print(f"\n== {OK} 项通过 / {BAD} 项失败 ==")
sys.exit(1 if BAD else 0)
