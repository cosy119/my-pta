"""端到端过一遍 HTTP 接口：三道题各走一次「提交 -> 轮询 -> 拿结果」。

★ 只对着**测试库**（data/_bank_test.db）跑，绝不碰用户的真实进度。
  验证的是前端真正会走的那条路：
    POST /api/submissions  ->  GET /api/submissions/<id>?with_cases=1
  再加上 GET /api/catalog /api/problems 的分类字段。

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


print(f"== 端到端验证 -> {BASE} ==")

# ---------------------------------------------------------------- 1. 目录
cat = req("/api/catalog")
keys = [s["key"] for s in cat["subjects"]]
check("catalog 三科目齐全且有序", keys == ["python", "ds", "linux"], str(keys))
check("catalog 总分 = 2615", cat["user_max_score"] == 2615, str(cat["user_max_score"]))
ds = [s for s in cat["subjects"] if s["key"] == "ds"][0]
check("ds 题数 31 / 4 个分组", ds["total"] == 31 and len(ds["sections"]) == 4,
      f"{ds['total']} 题 / {len(ds['sections'])} 组")
linux = [s for s in cat["subjects"] if s["key"] == "linux"][0]
check("linux 题数 117 / 16 个分组", linux["total"] == 117 and len(linux["sections"]) == 16,
      f"{linux['total']} 题 / {len(linux['sections'])} 组")

# ---------------------------------------------------------------- 2. 列表字段
items = req("/api/problems?subject=ds")["items"]
check("?subject=ds 只回 ds", all(p["subject"] == "ds" for p in items), f"{len(items)} 题")
check("编程题 langs 给了 C 与 C++ 两条路",
      [l["lang"] for l in items[0]["langs"]] == ["cpp", "c"], str(items[0]["langs"]))
check("列表按讲次排序", items[0]["source_section"].startswith("第 02 讲"), items[0]["source_section"])

lin = req("/api/problems?subject=linux")["items"]
check("Linux 理论题 is_choice 有值", any(p["is_choice"] for p in lin))
check("Linux 理论题 langs 为空（不用选语言）", lin[0]["langs"] == [], str(lin[0]["langs"]))

# ---------------------------------------------------------------- 3. 数据结构：同一题 C 与 C++ 各交一次
p57 = req("/api/problems/57")
check("题目详情带 subject_label", p57["subject_label"] == "数据结构（C 语言版）", p57["subject_label"])
check("题目详情不外泄参考解", "reference_solution" not in p57)
check("样例已给（题面要用）", len(p57["samples"]) >= 1, f"{len(p57['samples'])} 个")

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
r_cpp = submit(57, CPP, "cpp", "gpp")
print("  C++ ->", r_cpp["verdict"], r_cpp["score"], "/", r_cpp["max_score"],
      f"{r_cpp['passed']}/{r_cpp['total']}")
check("C++ 提交拿到 AC", r_cpp["verdict"] == "AC" and r_cpp["score"] == r_cpp["max_score"])

r_c = submit(57, C, "c", "gcc")
print("  C   ->", r_c["verdict"], r_c["score"], "/", r_c["max_score"],
      f"{r_c['passed']}/{r_c['total']}")
check("C 提交拿到 AC（同一道题、不同编译器）",
      r_c["verdict"] == "AC" and r_c["score"] == r_c["max_score"])

# 两套语言各有一份自己的提交记录
subs = req("/api/submissions?problem_id=57&limit=10")["items"]
langs = {s["lang"] for s in subs}
check("两条提交分别记成 cpp / c", langs == {"cpp", "c"}, str(langs))
check("逐测试点明细在（前端要展开）", len(r_c["cases"]) == 5, f"{len(r_c['cases'])} 个")
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
r_bad = submit(57, BROKEN, "cpp", "gpp")
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
p57row = [x for x in prog["items"] if x["id"] == 57][0]
check("进度取历史最高分（后面那次只拿 9 分，不影响 15）",
      p57row["best_score"] == 15 and p57row["solved_at"],
      f"best={p57row['best_score']}")
check("满分题计入「已解决」", prog["solved"] >= 1 and p57row["solved_at"] != "",
      f"solved={prog['solved']} attempted={prog['attempted']}")
me = req("/api/me")
check("my score = 已解决题目的满分之和（15 + 主观题）", me["score"] >= 15, str(me["score"]))
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
r_ce = submit(57, "#include <cstdio>\nint main(){ 这不是C++ }", "cpp", "gpp")
check("CE 带编译器原话", r_ce["verdict"] == "CE" and bool(r_ce.get("message")
      or r_ce.get("compile_output")), (r_ce.get("message") or "")[:60])

print(f"\n== {OK} 项通过 / {BAD} 项失败 ==")
sys.exit(1 if BAD else 0)
