"""把 Obsidian 笔记导出成 PTA 静态站的「笔记」模块数据。

为什么单独一个脚本
------------------
笔记是 **480 篇 markdown**、2.5 MB 文本，跟题库（SQLite）完全是两回事，
所以导出逻辑不塞进 export_static.py，而是产出一份「前端能直接吃」的数据集，
由 export_static.py 负责拷到 docs/ 里去。

产出（默认 docs/notes/）
------------------------
- `index.json`    目录树（三条学习线 → 讲 → 分节）+ 统计
- `p/<slug>.json` 单篇：预处理后的 markdown + 上下节 + 面包屑
- `search.json`   全文索引（纯文本，供前端即时搜索）

slug 规则（纯 ASCII，无斜杠与中文，方便直接塞进 hash 路由）
----------------------------------------------------------
    讲内分节   `<线>-<讲号>-<节号>`    例 py-05-05 / ds-02-04 / linux-16-03
    讲内索引   `<线>-<讲号>-00`        例 linux-16-00
    顶层文档   `<线>-<别名>`           例 py-overview / linux-bank / ds-codeindex

预处理都做了什么（这些是 Obsidian 语法 → 前端能渲染的 markdown）
--------------------------------------------------------------
1. frontmatter 剥离（title / 教材 / 状态等留下做元信息）
2. `[[目标|别名]]` → `[别名](#/notes/<slug>)`；解析不出来就退化成纯文本
3. callout（`> [!info] 标题`）→ `:::callout <类型> <折叠> <标题> ... :::`
   —— 2210 个，其中 574 个内部还嵌着代码块，所以必须**先识别 callout、
      再去前缀、再按普通 markdown 处理内部**，不能拿正则整段扫。
4. `==高亮==` → `<mark>`，`%%注释%%` 删除
5. 篇首那种「← 返回本讲 · ← 上一节 · 下一节 →」整行删掉（前端会按
   目录结构生成统一导航条，留着就重复了）

★ 代码块里的一切**必须原样保留** —— 笔记里有大量 bash，`[[ -f $f ]]`
  这种条件表达式跟 wikilink 长得一模一样，误替换就把命令毁了。
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_OUT = Path(__file__).resolve().parent.parent / "docs" / "notes"


def default_vault() -> Path:
    """笔记源目录。这台机器之外（比如 CI）没有它，调用方要能容忍。"""
    return Path(os.environ.get("PTA_NOTES_VAULT") or r"D:\work\Obsidian")

# 三条学习线：目录名 → (线 key, 展示名)
LINES = [
    ("Linux学习", "linux", "Linux 学习"),
    ("Python学习", "py", "Python 学习"),
    ("数据结构学习", "ds", "数据结构学习"),
]

# 顶层文档（不在任何「NN讲_XXX」目录里的那些）→ (线 key, slug 别名, 展示名)
TOP_DOCS = {
    "Linux学习总览": ("linux", "overview", "总览"),
    "Linux基础命令": ("linux", "cmd", "基础命令手册"),
    "Linux实验题库": ("linux", "bank", "实验题库"),
    "Python学习总览": ("py", "overview", "总览"),
    "习题工具箱": ("py", "toolbox", "习题工具箱"),
    "数据结构学习总览": ("ds", "overview", "总览"),
    "代码解释": ("ds", "codeindex", "代码解释"),
}

CALLOUT_RE = re.compile(r"^>\s*\[!(\w+)\]\s*([+-]?)\s*(.*)$")
# ★ 允许内部出现一层方括号：`py-overview` 里有个链接的锚点长这样 ——
#   [[04-04 …#4.2 切片：[start:stop:step]]]
#   用 `[^\[\]]+` 会整个漏掉（那行就会原样显示成 [[…]]）。
#   末尾可选多吃的那个 `]` 是源文件里多打的（`]]]`），一并收掉免得页面上冒出孤零零一个 `]`。
WIKILINK_RE = re.compile(r"\[\[((?:[^\[\]]|\[[^\[\]]*\])+?)\]\]\]?")
FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})\s*([^\s`]*)")
LECTURE_DIR_RE = re.compile(r"^(\d{1,2})讲[_\s]*(.*)$")
SECTION_RE = re.compile(r"^(\d{1,2})-(\d{1,2})")

# 前端折叠 callout 用的标记
FOLD_MARKS = {"-": "fold", "+": "open", "": "open"}


# --------------------------------------------------------------------------
# 1. 扫描
# --------------------------------------------------------------------------
def split_front(text: str):
    """拆出 frontmatter（只要标量，够用就行，不引 YAML 依赖）。"""
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n?", text, re.S)
    if not m:
        return {}, text
    fm: dict[str, str] = {}
    for line in m.group(1).split("\n"):
        mm = re.match(r"^([^:\s#][^:]*):\s*(.*)$", line)
        if mm:
            fm[mm.group(1).strip()] = mm.group(2).strip().strip("\"'")
    return fm, text[m.end():]


def display_title(stem: str) -> str:
    """文件名 → 目录里的显示名（去掉 `05-05 ` 这类前缀）。"""
    m = SECTION_RE.match(stem)
    if m:
        return stem[m.end():].strip() or stem
    return stem.strip()


def scan(vault: Path):
    """扫出所有笔记，顺便算出 slug。返回 (notes, warnings)。"""
    notes: list[dict] = []
    warnings: list[str] = []
    for dirname, key, label in LINES:
        base = vault / dirname
        if not base.is_dir():
            warnings.append(f"缺少目录：{base}")
            continue
        for path in sorted(base.rglob("*.md")):
            rel = path.relative_to(base).as_posix()
            parts = rel.split("/")
            stem = path.stem
            note = {
                "line": key, "lineName": label, "dir": dirname,
                "rel": rel, "stem": stem, "path": path,
                "lecture": None, "group": None, "sec": None,
            }
            if len(parts) == 1:                       # 顶层文档
                if stem in TOP_DOCS:
                    _, alias, name = TOP_DOCS[stem]
                    note["slug"] = f"{key}-{alias}"
                else:                                 # 用户新加的 → 兜底，别撞车
                    note["slug"] = f"{key}-top{len(notes)}"
                note["kind"] = "top"
                note["title"] = stem
            else:
                group = parts[0]
                gm = LECTURE_DIR_RE.match(group)
                lec = gm.group(1).zfill(2) if gm else "00"
                sm = SECTION_RE.match(stem)
                if sm:
                    sec = sm.group(2).zfill(2)
                elif "分节索引" in stem:
                    sec = "00"
                else:
                    sec = "99"          # 命名不规范的文件，排到本讲最后
                note.update({
                    "lecture": lec, "group": group, "sec": sec, "kind": "page",
                    "slug": f"{key}-{lec}-{sec}",
                    "title": display_title(stem),
                    "lectureTitle": (gm.group(2) if gm else group),
                })
            if "title" not in note:
                note["title"] = stem
            notes.append(note)

    # slug 撞车必须炸掉：静默覆盖会让链接指到别的笔记上
    seen: dict[str, str] = {}
    for n in notes:
        if n["slug"] in seen:
            raise SystemExit(f"slug 重复：{n['slug']}\n  {seen[n['slug']]}\n  {n['rel']}")
        seen[n["slug"]] = n["rel"]
    return notes, warnings


# --------------------------------------------------------------------------
# 2. 双链解析
# --------------------------------------------------------------------------
def build_resolver(notes: list[dict]):
    by_stem: dict[str, list[dict]] = {}
    by_relstem: dict[str, list[dict]] = {}
    by_line_stem: dict[tuple, list[dict]] = {}
    for n in notes:
        by_stem.setdefault(n["stem"], []).append(n)
        by_relstem.setdefault(n["rel"][:-3], []).append(n)      # 去掉 .md，含「讲/文件」
        by_line_stem.setdefault((n["line"], n["stem"]), []).append(n)

    def pick(cands: list[dict], src: dict) -> dict | None:
        if not cands:
            return None
        if len(cands) == 1:
            return cands[0]
        # 重名（`NN-01 一页速览` 在 Python 和 DS 里都有）→ 同线优先，再同讲优先
        same = [c for c in cands if c["line"] == src["line"]]
        if same:
            cands = same
        if len(cands) == 1:
            return cands[0]
        if src.get("lecture"):
            samel = [c for c in cands if c.get("lecture") == src["lecture"]]
            if samel:
                return samel[0]
        if src.get("group"):
            sameg = [c for c in cands if c.get("group") == src["group"]]
            if sameg:
                return sameg[0]
        return cands[0]

    def resolve(target: str, src: dict):
        """`目标` 或 `讲_目录/文件` → note（找不到返回 None）。"""
        t = target.strip()
        if not t:
            return None
        # 路径式：DS 线的索引链接是 [[02讲_线性表/00 本讲分节索引|...]]
        cands = by_relstem.get(t) or by_relstem.get(t[:-3] if t.endswith(".md") else t)
        if cands:
            return pick(cands, src)
        # 后一段（有的链接会带线名前缀）
        if "/" in t:
            t = t.split("/")[-1]
        return pick(by_stem.get(t) or by_stem.get(t[:-3] if t.endswith(".md") else t) or [], src) \
            or pick(by_line_stem.get((src["line"], t), []), src)

    return resolve, by_stem


# --------------------------------------------------------------------------
# 3. 预处理
# --------------------------------------------------------------------------
def is_nav_line(line: str) -> bool:
    """「← 返回本讲 · ← 上一节 · 下一节 →」这类纯导航行。"""
    s = line.strip()
    if s.count("[[") < 2:
        return False
    rest = WIKILINK_RE.sub("", s)
    for ch in "·•|→← \t\u3000":
        rest = rest.replace(ch, "")
    return rest == ""


class Preprocessor:
    def __init__(self, resolve, src: dict, unknown: set):
        self.resolve = resolve
        self.src = src
        self.unknown = unknown

    # ---- 行内替换（不含 callout / fence，那两样由 process 按行状态机处理）
    def inline(self, line: str) -> str:
        # ★ 反引号里的行内代码必须先挖出来护住：笔记里满是
        #   `` `[[ -f $f ]]` ``、`` `[[ 10 > 9 ]]` `` 这种 bash 条件式，
        #   跟 wikilink 长得一模一样，不护住就把命令改坏了。
        parts = re.split(r"(`+[^`\n]*`+)", line)
        return "".join(p if i % 2 else self._inline_text(p)
                       for i, p in enumerate(parts))

    def _inline_text(self, line: str) -> str:
        line = re.sub(r"%%.*?%%", "", line)
        line = re.sub(r"==([^=\n]+)==", r"<mark>\1</mark>", line)

        def sub(m):
            body = m.group(1)
            target, _, alias = body.partition("|")
            anchor = ""
            if "#" in target:
                target, _, anchor = target.partition("#")
            target_s, anchor_s = target.strip(), anchor.strip()

            # ① 空目标 + 无锚点：不是双链。笔记里有一句「三兄弟：test / [ / [[ ]] 的差异」，
            #    那个 `[[ ]]` 是**没加反引号护住**的 bash 条件式，会被当成"目标为空的双链"。
            #    原样留着当文本，别记进 unknown —— 否则导出一场就多一条无从下手的告警。
            if not target_s and not anchor_s:
                return m.group(0)

            # ② 空目标 + 有锚点：**同页锚点链接** `[[#小标题]]`（Python「习题工具箱」整表在用）。
            #    目标就是当前这篇笔记自己，label 退回用锚点名。旧版没这条分支，
            #    于是 resolve("") 必然失败、unknown 里多一个空字符串目标。
            if not target_s:
                label = (alias or anchor_s).strip()
                return f"[{label}](#/notes/{self.src['slug']}#{anchor_s})"

            note = self.resolve(target, self.src)
            label = (alias or target).strip()
            if note is None:
                self.unknown.add(target_s)
                return label
            url = "#/notes/" + note["slug"]
            if anchor:
                url += "#" + anchor.strip()
            return f"[{label}]({url})"

        return WIKILINK_RE.sub(sub, line)

    def process(self, lines: list[str], depth: int = 0) -> list[str]:
        """逐行状态机：fence 原样、callout 递归、其余走行内替换。

        ★ 顺序很要紧：callout 里的代码块在源文件里每行都带 `> ` 前缀，
          必须**先摘掉前缀**再送进递归，否则 fence 检测根本认不出来。
        """
        out: list[str] = []
        i, n = 0, len(lines)
        while i < n:
            line = lines[i]

            m = CALLOUT_RE.match(line)
            if m and depth < 4:
                typ = m.group(1).lower()
                fold = FOLD_MARKS.get(m.group(2), "open")
                # ★ 标题里经常直接就是个双链：`> [!abstract] [[Linux实验题库]]`
                #   所以标题也得过一遍行内替换，不然页面上会原样显示 `[[…]]`。
                title = self.inline(m.group(3).strip())
                i += 1
                body: list[str] = []
                while i < n:
                    cur = lines[i]
                    if cur.startswith(">"):
                        body.append(re.sub(r"^>\s?", "", cur))
                        i += 1
                    elif cur.strip() == "" and i + 1 < n and lines[i + 1].startswith(">"):
                        body.append("")          # callout 内部的空行
                        i += 1
                    else:
                        break
                inner = self.process(body, depth + 1)
                # 去掉尾部空行，免得 ::: 前面一堆空白
                while inner and not inner[-1].strip():
                    inner.pop()
                out.append(f":::callout {typ} {fold} {title}".rstrip())
                out.extend(inner)
                out.append(":::")
                continue

            fm = FENCE_RE.match(line)
            if fm:
                marker = fm.group(2)[0]
                out.append(line)
                i += 1
                while i < n:
                    out.append(lines[i])
                    if re.match(rf"^\s*{marker}{{3,}}\s*$", lines[i]):
                        i += 1
                        break
                    i += 1
                continue

            if is_nav_line(line):
                i += 1                            # 纯导航行，整行丢弃
                continue

            out.append(self.inline(line))
            i += 1
        return out


def to_plain(md: str) -> str:
    """给搜索用的纯文本（保留代码内容 —— 搜命令很有用）。"""
    s = re.sub(r"```[^\n]*\n", "", md)
    s = s.replace("```", "")
    s = re.sub(r":::callout[^\n]*", "", s).replace(":::", "")
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"^\s{0,3}[#>\-\*\+\|]\s?", "", s, flags=re.M)
    s = s.replace("|", " ")
    return re.sub(r"\s+", " ", s).strip()


# --------------------------------------------------------------------------
# 4. 组装
# --------------------------------------------------------------------------
def build(vault: Path, out_dir: Path) -> dict:
    notes, warnings = scan(vault)
    if not notes:
        raise SystemExit(f"没扫到任何笔记，检查 vault 路径：{vault}")

    resolve, _ = build_resolver(notes)
    unknown: set[str] = set()

    pages_dir = out_dir / "p"
    pages_dir.mkdir(parents=True, exist_ok=True)

    search_items = []
    total_chars = 0
    for n in notes:
        text = io.open(n["path"], encoding="utf-8", errors="replace").read()
        fm, body = split_front(text)
        pre = Preprocessor(resolve, n, unknown)
        md = "\n".join(pre.process(body.split("\n"))).strip()
        total_chars += len(md)

        # 上下节：按同讲内的 sec 排序推，不依赖 frontmatter（那样更脆）
        prev = next_ = None
        if n["kind"] == "page":
            sibs = sorted([x for x in notes
                           if x["line"] == n["line"] and x.get("group") == n["group"]],
                          key=lambda x: x["sec"])
            idx = sibs.index(n)
            if idx > 0:
                prev = {"slug": sibs[idx - 1]["slug"], "title": sibs[idx - 1]["title"]}
            if idx < len(sibs) - 1:
                next_ = {"slug": sibs[idx + 1]["slug"], "title": sibs[idx + 1]["title"]}

        crumb = [n["lineName"]]
        if n.get("group"):
            crumb.append(n["group"])

        page = {
            "slug": n["slug"], "title": n["title"], "line": n["line"],
            "lineName": n["lineName"], "crumb": crumb,
            "kind": n["kind"], "md": md,
            "prev": prev, "next": next_,
            "fm": {k: v for k, v in fm.items()
                   if k in ("教材", "状态", "type", "tags", "说明", "创建日期")},
        }
        if n.get("lecture"):
            page["lecture"] = n["lecture"]
            page["lectureTitle"] = n.get("lectureTitle", "")
            page["lectureIndex"] = f"{n['line']}-{n['lecture']}-00"
        (pages_dir / f"{n['slug']}.json").write_text(
            json.dumps(page, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

        search_items.append({
            "s": n["slug"], "t": n["title"],
            "b": " / ".join(crumb), "x": to_plain(md),
        })

    # ---- 目录树
    lines_out = []
    for key, label in [(k, l) for _, k, l in LINES]:
        ln = [n for n in notes if n["line"] == key]
        if not ln:
            continue
        lectures = []
        for group in sorted({n["group"] for n in ln if n.get("group")}):
            pages = sorted([n for n in ln if n.get("group") == group], key=lambda x: x["sec"])
            head = next((p for p in pages if p["sec"] == "00"), None)
            lectures.append({
                "group": group,
                "title": (head or pages[0]).get("lectureTitle") or group,
                "index": (head or pages[0])["slug"],
                "pages": [{"slug": p["slug"], "title": p["title"], "sec": p["sec"]}
                          for p in pages],
            })
        extras = [{"slug": n["slug"], "title": n["title"]}
                  for n in ln if not n.get("group")]
        lines_out.append({
            "key": key, "name": label, "count": len(ln),
            "lectures": lectures, "extras": extras,
            "pages": sum(len(x["pages"]) for x in lectures),
        })

    index = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(notes), "total_chars": total_chars,
        "lines": lines_out,
    }
    (out_dir / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    (out_dir / "search.json").write_text(
        json.dumps({"generated_at": index["generated_at"], "items": search_items},
                   ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    return {"index": index, "unknown": sorted(unknown), "warnings": warnings}


def main() -> int:
    ap = argparse.ArgumentParser(description="把 Obsidian 笔记导出成静态站数据")
    ap.add_argument("--vault", default=str(default_vault()),
                    help="Obsidian vault 根目录（默认 D:\\work\\Obsidian，可用环境变量 PTA_NOTES_VAULT 覆盖）")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="输出目录（默认 docs/notes）")
    args = ap.parse_args()

    vault = Path(args.vault)
    if not vault.is_dir():
        print(f"⚠ vault 不存在，跳过笔记导出：{vault}")
        return 0

    res = build(vault, Path(args.out))
    idx = res["index"]
    size = sum(f.stat().st_size for f in Path(args.out).rglob("*") if f.is_file())
    print("笔记 %d 篇 / %.1f 万字 / %.1f MB → %s"
          % (idx["count"], idx["total_chars"] / 10000, size / 1024 / 1024, args.out))
    for ln in idx["lines"]:
        print("  %-16s %3d 篇（%d 讲 + %d 篇顶层）"
              % (ln["name"], ln["count"], len(ln["lectures"]), len(ln["extras"])))
    for w in res["warnings"]:
        print("  ⚠ " + w)
    if res["unknown"]:
        print("  ⚠ 有 %d 个双链目标没解析出来（会退化成纯文本）：" % len(res["unknown"]))
        for u in res["unknown"][:15]:
            print("      " + u)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
