"""理论题自测：答案判得**准**，不只是判得**过**。

为什么必须单独测这一层
----------------------
`verify_bank.py` 只证明了一件事：**把正确答案交上去，能判过**。
但理论题真正的风险在另一个方向 —— **答案口径太宽**。

举例：一道单选题期望值是 `|B`。如果归一化写错了（比如把 `B` 和 `C` 都映射成同一个值），
或者 `oneof` 比较时把「任意一边为空」也算通过，那么这道题**谁来交都是满分** ——
而 `verify_bank` 依然会报「全部通过 ✅」。

所以这里从反方向验一遍：**错的必须判错**。

检查项
------
1. **单选题**：正确选项 AC；**其余每个选项都必须 WA**（逐个试，不能只试一个）
1b. **多选题**：正确答案 AC 判过；**选项集合的所有其它子集**（含只选一个、
    多选一个）全部 WA —— 漏选/多选都算错；同一组答案写反顺序也认
2. **判断题**：`对` / `正确` / `√` / `T` / `是` 都 AC；`错` / `×` / `F` 都 WA
3. **命令填空题**：多种等价写法（选项顺序颠倒、空格多少、`-l -a` 与 `-la`）都 AC
4. **命令填空题**：形近但**错误**的命令必须 WA（`head -n +100` 之类）
5. **空答案**：判 WA，且判题器不能崩
6. **反向涂写**：交一整段无关文字 → WA
7. **全库扫一遍**：每道选择题的正确答案必须**真的落在选项范围里**，
   且期望值里的可接受答案**不含**其它选项的字母（防串行写错）

用法
----
    python tools/selftest_theory.py
"""
from __future__ import annotations

import os
import re
import sys
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

import _console                                                   # noqa: E402
import _testdb                                                   # noqa: E402  ★ 别让自检写进真实库
from app.judge.compare import compare, oneof_alternatives   # noqa: E402
from app.judge.runner_text import TextRunner, normalize_answer  # noqa: E402
from app.problems_bank_linux import LINUX_PROBLEMS           # noqa: E402

PASSED: list[str] = []
FAILED: list[str] = []

_QUESTIONS = re.compile(r"^[A-H]$")


def check(name: str, ok: bool, detail: str = "") -> None:
    (PASSED if ok else FAILED).append(name)
    print("%s %s%s" % ("✅" if ok else "❌", name, ("  → " + detail) if detail else ""))
    sys.stdout.flush()


def judge(prob: dict, submitted: str) -> bool:
    """完整走一遍真判题链路：TextRunner 归一化 → oneof 比对。"""
    runner = TextRunner()
    runner.prepare(submitted, Path("."))
    res = runner.run_case(Path("."), b"", None)  # type: ignore[arg-type]
    exp = prob["cases"][0]["expected_stdout"]
    return compare(exp, res.stdout, prob.get("checker") or "standard").ok


def find(keyword: str) -> dict | None:
    for p in LINUX_PROBLEMS:
        if keyword in p["title"]:
            return p
    return None


def main() -> int:
    print("=" * 78)
    print("理论题自测：正确答案判过 + 错误答案判错")
    print("题目库：Linux 线 %d 题" % len(LINUX_PROBLEMS))
    print("=" * 78)

    # ---------- 1 · 单选题：其余选项必须判错 ----------
    #   ★ 多选题也是「有选项」的题，但判法不同（正确选项不止一个），
    #     所以先按 question_type 分开，单选走这一节、多选走 1b。
    choice_probs = [p for p in LINUX_PROBLEMS
                    if p.get("choices") and p["choices"] != ["对", "错"]]
    mc_probs = [p for p in choice_probs if p.get("question_type") != "multiple_choice"]
    multi_probs = [p for p in choice_probs if p.get("question_type") == "multiple_choice"]
    bad_mc: list[str] = []
    for p in mc_probs:
        letters = "ABCDEFGH"
        right = oneof_alternatives(p["cases"][0]["expected_stdout"])[0].strip().upper()
        if right not in letters[:len(p["choices"])]:
            bad_mc.append("%s（正确答案 %r 不在 %d 个选项里）"
                          % (p["title"], right, len(p["choices"])))
            continue
        if not judge(p, right):
            bad_mc.append("%s（正确答案 %s 竟然判不过）" % (p["title"], right))
            continue
        for L in letters[:len(p["choices"])]:
            if L == right:
                continue
            if judge(p, L):
                bad_mc.append("%s（错误选项 %s 被误判为对）" % (p["title"], L))
    check("单选题 %d 道：正确答案判过、其余选项全部判错" % len(mc_probs),
          not bad_mc, "; ".join(bad_mc[:3]))

    # ---------- 1b · 多选题：正确答案判过，**其它任何字母组合**都必须判错 ----------
    #   ★ 这里不做「抽查」，直接把选项集合的所有子集穷举一遍：
    #     多选题最怕的不是「答案判不过」，而是「漏选也判对」——
    #     只选一半就能 AC 的话，这道题等于白出。
    bad_multi: list[str] = []
    for p in multi_probs:
        n = len(p["choices"])
        letters = "ABCDEFGH"[:n]
        right = oneof_alternatives(p["cases"][0]["expected_stdout"])[0].strip().upper()
        if len(right) < 2 or any(L not in letters for L in right):
            bad_multi.append("%s（正确答案 %r 不是两个以上的有效选项）" % (p["title"], right))
            continue
        if len(set(right)) != len(right):
            bad_multi.append("%s（答案里有重复字母 %r）" % (p["title"], right))
            continue
        if not judge(p, right):
            bad_multi.append("%s（正确答案 %s 竟然判不过）" % (p["title"], right))
            continue
        right_set = set(right)
        for k in range(1, n + 1):
            for combo in combinations(letters, k):
                if set(combo) == right_set:
                    continue
                got = "".join(combo)
                if judge(p, got):
                    bad_multi.append("%s（错误组合 %s 被误判为对）" % (p["title"], got))
        # 同一组正确答案、顺序写反 → 也要认（工厂对 ≤3 个字母会列全排列）
        if len(right) <= 3 and not judge(p, right[::-1]):
            bad_multi.append("%s（同一组答案换个顺序 %s 判不过）" % (p["title"], right[::-1]))
    check("多选题 %d 道：答案判过、其它字母组合全判错、顺序写反也认" % len(multi_probs),
          bool(multi_probs) and not bad_multi, "; ".join(bad_multi[:3]))

    # ---------- 2 · 判断题的各种写法 ----------
    tf_probs = [p for p in LINUX_PROBLEMS if p.get("choices") == ["对", "错"]]
    true_p = next((p for p in tf_probs
                   if oneof_alternatives(p["cases"][0]["expected_stdout"])[0] == "对"), None)
    false_p = next((p for p in tf_probs
                    if oneof_alternatives(p["cases"][0]["expected_stdout"])[0] == "错"), None)

    ok_variants = True
    detail = ""
    if true_p:
        for w in ("对", "正确", "√", "T", "是", "true", "对。", " 对 "):
            if not judge(true_p, w):
                ok_variants = False
                detail += "「%s」应判对却被判错 " % w
        for w in ("错", "×", "F", "否", "false"):
            if judge(true_p, w):
                ok_variants = False
                detail += "「%s」应判错却被判对 " % w
    else:
        ok_variants = False
        detail = "题库里找不到答案为「对」的判断题"
    check("判断题：`对/正确/√/T/是` 都认，`错/×/F/否` 都拒", ok_variants, detail.strip())

    if false_p:
        ok2 = all(judge(false_p, w) for w in ("错", "错误", "×", "F", "否"))
        ok2 = ok2 and not any(judge(false_p, w) for w in ("对", "正确", "√", "T", "是"))
        check("判断题（答案为「错」的那道）方向没写反", ok2)
    else:
        check("判断题（答案为「错」的那道）方向没写反", False, "题库里没有答案为「错」的判断题")

    # ---------- 3 · 命令填空题的宽容度 ----------
    p_ls = find("列出目录下所有条目")
    ok_eq = bool(p_ls) and all(judge(p_ls, w) for w in (
        "ls -la /etc",
        "ls -al /etc",          # 选项顺序颠倒
        "ls  -l   -a   /etc",   # 空格多少
        "ls -l -a /etc",        # 分开写
        "ls -lah /etc",         # 多一个 -h
        "ls -lA /etc",          # 用 -A
    ))
    check("填命令：`-la` / `-al` / `-l -a` / `-lah` 都算同一条",
          ok_eq, "" if ok_eq else "有一种等价写法被判错")

    # ---------- 4 · 形近但错误的命令必须判错 ----------
    wrong_cases = [
        ("列出目录下所有条目", "cd /etc"),                    # 完全跑偏
        ("列出目录下所有条目", "ls /etc"),                    # 少 -la，不是长格式
        ("取从第 100 行到末尾", "head -n +100 a.log"),        # ★ 经典错误：该用 tail
        ("取除最后 10 行外的全部内容", "tail -n 10 a.log"),   # ★ 与正确答案差在 +/- 和命令
        ("取文件的前 50 行", "tail -n 50 a.log"),             # 前后颠倒
        ("一步回到上一个目录", "cd .."),                       # 与 cd - 语义不同
        ("一次性创建多级目录", "mkdir data/2026/10/report"),   # 漏 -p
        ("打包并 gzip 压缩", "tar -Zcvf project.tar.gz ~/project"),  # 大写 Z
    ]
    bad_wrong: list[str] = []
    for kw, ans in wrong_cases:
        p = find(kw)
        if p is None:
            bad_wrong.append("找不到题目「%s」" % kw)
            continue
        if judge(p, ans):
            bad_wrong.append("《%s》把错误答案 %r 判成了对" % (p["title"], ans))
    check("填命令：%d 个形近错误答案全部判错" % len(wrong_cases),
          not bad_wrong, "; ".join(bad_wrong[:3]))

    # ---------- 5 · 空答案 / 乱写 ----------
    sample = mc_probs[0]
    check("空答案判错（且不崩）",
          (not judge(sample, "")) and (not judge(sample, "   \n  ")))
    check("整段无关文字判错",
          not judge(sample, "我觉得这道题应该选一个我喜欢的字母，随便写点什么好了"))

    # ---------- 6 · 归一化函数本身的几个边界 ----------
    check("答案归一化：`b` → `B`、`B.` → `B`、`选 B` → `B`",
          normalize_answer("b") == "B"
          and normalize_answer("B.") == "B"
          and normalize_answer("选 B") == "B"
          and normalize_answer("  A、 ") == "A")
    check("答案归一化不误伤命令（`ls -la /etc` 原样保留）",
          normalize_answer("ls -la /etc") == "ls -la /etc")
    # ★ 回归：早期版本把首尾标点一律剥掉，结果命令答案的**最后一个字符被吃掉**
    #   （`cd ../..` → `cd ../`），三道填空题的参考答案永远判不过自己
    check("答案末尾的点号 / 引号不能被吃掉",
          normalize_answer("cd ../..") == "cd ../.."
          and normalize_answer('echo -n "hello everyone!"') == 'echo -n "hello everyone!"'
          and normalize_answer("dnf provides '*/ls'") == "dnf provides '*/ls'")

    # ---------- 8 · 全库扫：每道题的参考答案必须能判过它自己的期望值 ----------
    # 这是最强的一条不变量：题库里 reference_solution 就是 answers[0]，
    # 它跟期望值里的第一条可选答案**必然**是同一个东西 ——
    # 判不过就说明「归一化 / 比对」这一层动了不该动的东西
    bad: list[str] = []
    for p in LINUX_PROBLEMS:
        c = p["cases"][0]
        if not compare(c["expected_stdout"], normalize_answer(p["reference_solution"]),
                       p.get("checker"), 1e-6):
            bad.append(p["title"])
    check("全库扫：%d 道理论题的参考答案都能判过自己" % len(LINUX_PROBLEMS),
          not bad, "、".join(bad[:4]))

    # ---------- 9 · 全库扫：期望值的每一条备选答案都要能判过 ----------
    bad2: list[str] = []
    for p in LINUX_PROBLEMS:
        c = p["cases"][0]
        alts = oneof_alternatives(c["expected_stdout"])
        for a in alts:
            if not compare(c["expected_stdout"], normalize_answer(a),
                           p.get("checker"), 1e-6):
                bad2.append("%s → %r" % (p["title"], a))
    check("全库扫：期望值里的每条可接受答案都判得过", not bad2,
          "；".join(bad2[:3]))

    # ---------- 10 · 全库扫：形近错误答案仍然要判错 ----------
    # 宽容口径不能宽到「什么都算对」
    bad3: list[str] = []
    for p in LINUX_PROBLEMS:
        c = p["cases"][0]
        alts = [a.strip() for a in oneof_alternatives(c["expected_stdout"])]
        if not alts:
            continue
        ctr = "\u0000zz-" + alts[0] + "-zz\u0000"
        if compare(c["expected_stdout"], normalize_answer(ctr), p.get("checker"), 1e-6):
            bad3.append(p["title"])
    check("全库扫：乱写 / 加料的答案仍然判错", not bad3, "、".join(bad3[:4]))

    # ---------- 7 · 全库扫：正确答案必须落在选项范围内 ----------
    issues: list[str] = []
    for p in mc_probs:
        alts = oneof_alternatives(p["cases"][0]["expected_stdout"])
        right = alts[0].strip().upper() if alts else ""
        # 期望值里除正确项外，不该出现别的单字母选项（防串行写错）
        others = [a for a in alts[1:] if _QUESTIONS.match(a.strip().upper())]
        if others:
            issues.append("%s 的期望值里出现了多余选项 %s" % (p["title"], others))
    check("全库扫：%d 道选择题的正确答案都唯一且在范围内" % len(mc_probs),
          not issues, "; ".join(issues[:2]))

    print("=" * 78)
    print("通过 %d 项，失败 %d 项" % (len(PASSED), len(FAILED)))
    if FAILED:
        print("★ 失败项：%s" % "、".join(FAILED))
    else:
        print("全部通过 ✅")
    print("=" * 78)
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
