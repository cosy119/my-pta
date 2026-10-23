# -*- coding: utf-8 -*-
"""出题提速套件：把「expected_stdout 从哪来」自动化。

原来每加一族编程题的固定开销
--------------------------
1. 手写一个 node oracle（另一套语言、另一套算法）预先算期望输出；
2. 把算出的 expected_stdout 逐个誊进题库；
3. 誊错一个字符就等 verify_bank 全量跑 5 分钟才暴露。

本套件的新流程
--------------
题库模块里编程题的 `expected_stdout` 直接写 `None` 占位，其余照旧写齐
（题面、参考解、**换了一套算法的 alt_solution**、每组 stdin、解释）：

    {"stdin": "10\n", "expected_stdout": None, "kind": "manual",
     "explanation": "1010 → 2 个 1"},

然后：

    python tools/family_kit.py derive app/problems_bank_py_next.py

套件会把每道题的**参考解和 alt 解各跑一遍全部测试点**：
- 两边都正常结束且**逐字节一致** → 这个一致输出就是 expected_stdout，
  自动回填进源文件（None 占位处原位替换）；
- 两边不一致 / 有一边跑炸 → 打印双方输出，退出码 1，**一个字都不改**。

为什么这不算「自己给自己判卷」
------------------------------
老流程的保险是「第三套实现」（node oracle） vs 参考解；
新流程的保险是「第二套实现」（alt 解） vs 参考解 —— 前提不变：
**alt 解必须换算法或换 API，不许照抄参考解改改变量名**。
套件会拒绝 ref/alt 源码相同的题（抄懒了当场拦下）。
两套实现由同一颗脑子写出，仍可能共享「题意读错」的盲区 —— 所以
`derive` 会把每组输出打印出来供人过目，诡异的数一眼就能看出来。

子命令
------
    derive <模块路径> [--var LIST名]   对撞 + 回填 expected_stdout（默认）
    check  <模块路径> [--var LIST名]   只复核：重跑两套解撞已有 expected，不改文件

约定
----
- 模块里**题目列表**自动探测：任何「元素是含 title+cases 的 dict」的 list 属性；
  有多个时用 --var 指定。
- 回填按「文件中 `"expected_stdout": None` 的出现顺序」= 模块遍历顺序
  （题库列表都是字面量，顺序天然一致；对不上就中止，绝不瞎猜）。
- 理论题（无 cases 字段）自动跳过。
"""
from __future__ import annotations

import importlib
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

RUN_TIMEOUT_S = 10          # 单个测试点超时（出题用的解不该有指数级实现）


def _run_solution(code: str, stdin: str, workdir: Path) -> tuple[str | None, str | None]:
    """跑一套解，返回 (stdout, 错误说明)。错误说明非 None 即失败。"""
    src = workdir / "main.py"
    src.write_text(code, encoding="utf-8")
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8",
               NO_PROXY="127.0.0.1,localhost")
    try:
        r = subprocess.run([sys.executable, str(src)], input=stdin.encode("utf-8"),
                           capture_output=True, timeout=RUN_TIMEOUT_S, env=env,
                           cwd=workdir)
    except subprocess.TimeoutExpired:
        return None, "超时（>%ds）—— 出题用的解不该这么慢" % RUN_TIMEOUT_S
    if r.returncode != 0:
        return None, "退出码 %d\n%s" % (r.returncode,
                                        r.stderr.decode("utf-8", "replace")[-300:])
    # ★ Windows 管道会把 \n 翻译成 \r\n —— 与判题端 compare 同款归一成 \n，
    #   库里 expected 统一存 \n 形态（judge/compare.py::_norm 一回事）。
    return r.stdout.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n"), None


def _find_problem_lists(mod) -> dict[str, list]:
    """自动探测模块里「长得像题库列表」的属性。"""
    out = {}
    for name in dir(mod):
        if name.startswith("_"):
            continue
        val = getattr(mod, name)
        if not isinstance(val, list) or not val:
            continue
        if all(isinstance(p, dict) and "title" in p and "cases" in p for p in val):
            out[name] = val
    return out


def _prog_problems(lists: dict[str, list]) -> list[dict]:
    """挑出编程题（有 cases 且 line 不是 text）。理论题没有 cases，自然被排除。"""
    probs = []
    for _name, lst in lists.items():
        for p in lst:
            if isinstance(p, dict) and "cases" in p and \
                    str(p.get("line") or "python").lower() not in ("text", "choice", "theory"):
                probs.append(p)
    return probs


def _load_module(arg: str):
    """模块参数既可以是 app/problems_bank_py_bits.py 这样的路径，也可以是点分名。"""
    p = Path(arg)
    if p.suffix == ".py":
        rel = p.resolve().relative_to(ROOT).with_suffix("")
        dotted = ".".join(rel.parts)
    else:
        dotted = arg
    return importlib.import_module(dotted), dotted


def _file_order(names: list[str], src_path: Path) -> list[str]:
    """按「列表变量在源文件里的定义顺序」排序列名。

    回填靠「None 占位在文件中的出现顺序 = 模块遍历顺序」对齐，
    而 dir() 是字母序 —— 必须用源文件真实顺序，多列表模块才不会错位。
    """
    text = src_path.read_text(encoding="utf-8")
    pos = {}
    for m in re.finditer(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\[", text, re.M):
        pos.setdefault(m.group(1), m.start())
    return sorted(names, key=lambda n: pos.get(n, 1 << 30))


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 1
    cmd, mod_arg = args[0], args[1]
    var = None
    if "--var" in sys.argv:
        i = sys.argv.index("--var")
        var = sys.argv[i + 1]

    mod, dotted = _load_module(mod_arg)
    detected = {var: getattr(mod, var)} if var else _find_problem_lists(mod)
    if not detected:
        print("没探测到题库列表（用 --var 指定）")
        return 1

    # ★ 全局题序 = 源文件里列表定义顺序 × 列表内出现顺序。
    #   回填时 None 占位的文件出现顺序就是这个序 —— 唯一对得上的锚。
    order = _file_order(list(detected), Path(mod.__file__))
    probs: list[dict] = []
    for name in order:
        probs += _prog_problems({name: detected[name]})
    print("模块 %s：列表 %s（按文件顺序），编程题 %d 道"
          % (dotted, "、".join(order), len(probs)))

    # ---- 收集待派生的 (全局题序, case序) 占位 ----
    todo: set[tuple[int, int]] = set()
    if cmd == "derive":
        for pi, p in enumerate(probs):
            for ci, c in enumerate(p["cases"]):
                if c.get("expected_stdout") is None:
                    todo.add((pi, ci))
        if not todo:
            print("没有 expected_stdout=None 的占位，无事可做")
            return 0
        # --var 子集必须覆盖文件里全部占位，否则回填会错位（安全闸）
        text_now = Path(mod.__file__).read_text(encoding="utf-8")
        file_n = len(re.findall(r'("expected_stdout"\s*:\s*)None', text_now))
        if file_n != len(todo):
            print("★ 文件里 None 占位 %d 处，选中范围只覆盖 %d 处 ——\n"
                  "  （其余在未探测到/未选中的列表里）回填会错位，中止"
                  % (file_n, len(todo)))
            return 1

    # ---- 独立性守门：ref 与 alt 源码不许相同（只在 derive 生效；
    #      check 只复核已有 expected，抄没抄懒不归它管） ----
    lazy: list[str] = []
    if cmd == "derive":
        lazy = [probs[pi]["title"] for pi in range(len(probs))
                if (pi, 0) in todo or any((pi, ci) in todo
                                          for ci in range(len(probs[pi]["cases"])))
                and probs[pi].get("alt_solution")
                and probs[pi]["reference_solution"].strip()
                == probs[pi]["alt_solution"].strip()]
    if lazy:
        print("★ 参考解与 alt_solution 源码相同（抄懒了），拒绝："
              + "、".join(lazy))
        return 1

    workdir = Path(tempfile.mkdtemp(prefix="family_kit_"))
    bad = 0
    derived: list[str] = []          # 与文件中 None 占位出现顺序一一对应
    try:
        for pi, p in enumerate(probs):
            for ci, c in enumerate(p["cases"]):
                if cmd == "derive" and (pi, ci) not in todo:
                    continue
                if cmd == "check" and c.get("expected_stdout") is None:
                    continue          # 还没回填的占位不参与复核
                ref_out, ref_err = _run_solution(p["reference_solution"],
                                                 c["stdin"], workdir)
                alt_out, alt_err = (None, None)
                if p.get("alt_solution"):
                    alt_out, alt_err = _run_solution(p["alt_solution"],
                                                     c["stdin"], workdir)
                if ref_err or alt_err:
                    bad += 1
                    print("❌ [%s] 测试点 %d 跑炸\n  参考解: %s\n  alt解: %s"
                          % (p["title"], ci + 1, ref_err, alt_err))
                    continue
                if p.get("alt_solution") and ref_out != alt_out:
                    bad += 1
                    print("❌ [%s] 测试点 %d 两套实现不一致\n  stdin     = %r\n"
                          "  参考解 = %r\n  alt解  = %r"
                          % (p["title"], ci + 1, c["stdin"], ref_out, alt_out))
                    continue
                if cmd == "derive":
                    derived.append(ref_out)
                    print("✅ [%s] 测试点 %d → %r"
                          % (p["title"], ci + 1, ref_out))
                else:
                    exp = c.get("expected_stdout")
                    if ref_out != exp:
                        bad += 1
                        print("❌ [%s] 测试点 %d 与库内 expected 不一致\n"
                              "  库内 = %r\n  重跑 = %r"
                              % (p["title"], ci + 1, exp, ref_out))
                    else:
                        print("✅ [%s] 测试点 %d 一致" % (p["title"], ci + 1))
                sys.stdout.flush()
    finally:
        import shutil
        shutil.rmtree(workdir, ignore_errors=True)

    if bad:
        print("\n%d 处问题，%s 中止（文件未改动）"
              % (bad, "回填" if cmd == "derive" else "复核"))
        return 1

    if cmd == "check":
        print("\n复核全部一致 ✅")
        return 0

    # ---- 回填：按文件中 None 占位出现顺序替换 ----
    src_path = Path(mod.__file__)
    text = src_path.read_text(encoding="utf-8")
    pat = re.compile(r'("expected_stdout"\s*:\s*)None')
    spots = pat.findall(text)
    if len(spots) != len(derived):
        print("★ 文件里 None 占位 %d 处，待回填 %d 处，对不上 —— "
              "模块遍历顺序与文件顺序不一致，中止（文件未改动）"
              % (len(spots), len(derived)))
        return 1
    it = iter(derived)
    new_text = pat.sub(lambda m: m.group(1) + repr(next(it)), text)
    src_path.write_text(new_text, encoding="utf-8", newline="")
    print("\n回填 %d 处 expected_stdout → %s ✅（记得跑 verify_bank --only 复核）"
          % (len(derived), src_path.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
