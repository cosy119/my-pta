"""分节（知识点分组）的**教学路径顺序表** —— 全站唯一的分节排序来源。

## 为什么需要这张表

题目原本按「讲次」排（`lecOf()` 从 `source_section` 里抠「第 N 讲」），
但**没有讲次号的分组一律返回 0**，于是：

* C++ 线 17 个「C++ 编程 · X」节、Linux 线 12 个「命令特训 · X」节
  全被挤到「第 01 讲」**前面**；
* 它们彼此之间再按拼音排 —— 结果是「动态规划、二维数组与矩阵、分支结构」
  这种完全不成学习路径的顺序。

这张表把每条线的分节按**教学路径**显式列出（路径本身即由易到难）：

==========  ==========================================================
线           轨道
==========  ==========================================================
python      讲次 → 技巧特训 → 编程精练
ds          讲次 → 技巧特训 → 编程精练
cpp         讲次 → C++ 编程册（册序）→ 技巧特训
linux       基础命令 → 实验 → 讲次 → 命令特训（按均难）
==========  ==========================================================

## 轨道内的两种排法

* ``fixed``     —— 按表里写死的次序（讲次、册序、基础命令 A/B/C 组…）。
* ``difficulty``—— 按该节**平均难度**升序；并列时保持表内次序。
  只用于「命令特训」这类**并列专题**（各命令族之间没有知识依赖，
  难度就是唯一可比标尺）。

## 为什么分节不一律纯按平均难度排

分节之间存在知识依赖。纯按均难排会把「函数与参数传递」(1.85) 提到
「循环结构」(2.12) 前面、把「指针与引用」(2.05) 提到「一维数组」前面 ——
而指针得先会数组、函数得先会循环。**组内题目**才按 `difficulty` 升序
（见 `api/problems.py::_order_key`）。

## 维护

新增分节后跑 ``python tools/check_section_order.py``，它会指出
**库里有、表里没有**的分节（漏登记）和 **表里有、库里没有**的（写错了）。
"""
from __future__ import annotations

import re
from typing import Iterable, Mapping

_LECTURE_RE = re.compile(r"第\s*(\d+)\s*讲")


class Track:
    """一条轨道：一组分节 + 轨道内的排法。"""

    __slots__ = ("names", "by_difficulty")

    def __init__(self, names: Iterable[str], by_difficulty: bool = False):
        self.names = list(names)
        self.by_difficulty = by_difficulty


# ---------------------------------------------------------------------------
# 教学路径表
# ---------------------------------------------------------------------------

TRACKS: dict[str, list[Track]] = {
    # --- Python 线：教材 14 讲 → 拔高两组 -----------------------------------
    "python": [
        Track([
            "第 01 讲 · Python 开发入门",
            "第 02 讲 · 编程基础",
            "第 03 讲 · 流程控制语句",
            "第 04 讲 · 字符串",
            "第 05 讲 · 列表与元组",
            "第 06 讲 · 字典与集合",
            "第 07 讲 · 函数（上）",
            "第 07 讲 · 函数",
            "第 08 讲 · 函数（下）",
            "第 08 讲 · 函数",
            "第 09 讲 · 模块与包",
            "第 10 讲 · 面向对象（上）",
            "第 11 讲 · 面向对象（下）",
            "第 12 讲 · 文件",
            "第 13 讲 · 异常",
            "第 14 讲 · 综合案例",
        ]),
        Track(["技巧特训 · Python"]),
        Track(["编程精练 · Python"]),
    ],

    # --- 数据结构线：教材 8 讲 → 拔高两组 ----------------------------------
    "ds": [
        Track([
            "第 01 讲 · 绪论",
            "第 02 讲 · 线性表",
            "第 03 讲 · 栈和队列",
            "第 04 讲 · 串、数组和广义表",
            "第 05 讲 · 树和二叉树",
            "第 06 讲 · 图",
            "第 07 讲 · 查找",
            "第 08 讲 · 排序",
        ]),
        Track(["技巧特训 · C/C++"]),
        Track(["编程精练 · C/C++"]),
    ],

    # --- C++ 线：教材 12 讲 → 编程册 17 节（册序）→ 技巧特训 ----------------
    "cpp": [
        Track([
            "第 01 讲 · 绪论",
            "第 02 讲 · C++ 简单程序设计",
            "第 03 讲 · 函数",
            "第 04 讲 · 类与对象",
            "第 05 讲 · 数据的共享与保护",
            "第 06 讲 · 数组指针与字符串",
            "第 07 讲 · 类的继承",
            "第 08 讲 · 多态性",
            "第 09 讲 · 模板与群体数据",
            "第 10 讲 · 泛型程序设计与STL",
            "第 11 讲 · 流类库与输入输出",
            "第 12 讲 · 异常处理",
        ]),
        Track([
            "C++ 编程 · 输入输出与格式化",
            "C++ 编程 · 运算符与表达式",
            "C++ 编程 · 分支结构",
            "C++ 编程 · 循环结构",
            "C++ 编程 · 嵌套循环与图形",
            "C++ 编程 · 一维数组",
            "C++ 编程 · 二维数组与矩阵",
            "C++ 编程 · 函数与参数传递",
            "C++ 编程 · 递归与递推",
            "C++ 编程 · 指针与引用",
            "C++ 编程 · 字符数组与字符串",
            "C++ 编程 · 结构体与共用体",
            "C++ 编程 · 链表",
            "C++ 编程 · 排序与查找",
            "C++ 编程 · 贪心",
            "C++ 编程 · 动态规划",
            "C++ 编程 · 综合模拟与数学",
        ]),
        Track(["技巧特训 · C++"]),
    ],

    # --- Linux 线：基础命令 → 实验 → 讲次 → 命令特训（并列专题，按均难）-----
    "linux": [
        Track([
            "基础命令 · 先纠正六处",
            "基础命令 · A 组 认命令",
            "基础命令 · B 组 写命令",
            "基础命令 · C 组 找错",
        ]),
        Track([
            "实验 1 · 环境搭建",
            "实验 2 · 基本命令",
            "实验 3 · 常用命令",
            "实验 4 · 综合命令",
            "实验 5 · 用户与权限",
        ]),
        Track([
            "第 01 讲 · Linux 概述",
            "第 03 讲 · X Window 的使用",
            "第 04 讲 · 常用软件",
            "第 05 讲 · 硬件与软件安装",
            "第 06 讲 · 网络的基本配置",
            "第 07 讲 · 常用网络服务",
            "第 08 讲 · 系统管理与监视",
            "第 09 讲 · 系统安全管理",
            "第 10 讲 · Linux 系统的定制",
            "第 11 讲 · Shell 程序设计",
            "第 12 讲 · GCC 的使用与开发",
            "第 13 讲 · GTK 图形界面程序设计",
            "第 14 讲 · Qt 图形界面程序设计",
            "第 15 讲 · Python 程序开发环境",
            "第 16 讲 · 集成开发环境 Eclipse 的使用",
        ]),
        Track([
            "命令特训 · 查看文件内容",
            "命令特训 · 用户与组",
            "命令特训 · 网络与远程",
            "命令特训 · 文件与目录",
            "命令特训 · 软件包与服务",
            "命令特训 · 文本处理",
            "命令特训 · 磁盘与存储",
            "命令特训 · 进程与作业",
            "命令特训 · 压缩与打包",
            "命令特训 · 查找与定位",
            "命令特训 · Shell 与管道",
            "命令特训 · 权限与属性",
        ], by_difficulty=True),
    ],
}

#: 未登记分节的兜底序号起点（排在所有已登记分节之后）
UNKNOWN_BASE = 100000

SUBJECT_ORDER = {"python": 0, "ds": 1, "cpp": 2, "linux": 3}


def lecture_of(section: str) -> int:
    """从分节名里抠讲次号；没有讲次号返回 0。"""
    m = _LECTURE_RE.search(str(section or ""))
    return int(m.group(1)) if m else 0


def known_sections() -> dict[str, list[str]]:
    """已登记的全部分节（按表内次序展开），便于核对。"""
    out: dict[str, list[str]] = {}
    for subject, tracks in TRACKS.items():
        names: list[str] = []
        for t in tracks:
            names.extend(t.names)
        out[subject] = names
    return out


def build_ranks(
    pairs: Iterable[tuple[str, str]],
    stats: Mapping[tuple[str, str], float] | None = None,
) -> dict[tuple[str, str], int]:
    """给 (科目, 分节名) 分配一个**全库唯一且稳定**的排序号。

    :param pairs: 题库里实际出现过的 (subject, source_section) 集合
    :param stats: (subject, section) → 平均难度；给了才会启用
                  ``by_difficulty`` 轨道（并列专题按难度升序）
    """
    ranks: dict[tuple[str, str], int] = {}
    nxt = 0
    for subject in sorted(TRACKS, key=lambda s: SUBJECT_ORDER.get(s, 9)):
        for track in TRACKS[subject]:
            names = list(track.names)
            if track.by_difficulty and stats:
                # 稳定排序：并列时保持表内次序
                names.sort(key=lambda nm, t=track: (float(stats.get((subject, nm), 99.0)),
                                                     t.names.index(nm)))
            for name in names:
                key = (subject, name)
                if key in ranks:          # 表里重复登记 → 后面的一次忽略
                    continue
                ranks[key] = nxt
                nxt += 1

    # 未登记分节：按（讲次号, 名字）排，统一垫底
    unknown = sorted(
        {p for p in pairs if p not in ranks},
        key=lambda p: (SUBJECT_ORDER.get(p[0], 9), lecture_of(p[1]), p[1]),
    )
    for i, key in enumerate(unknown):
        ranks[key] = UNKNOWN_BASE + i
    return ranks


def rank_of(ranks: Mapping[tuple[str, str], int], subject: str, section: str) -> int:
    """查排序号；查不到返回一个很大的兜底值。"""
    return int(ranks.get((str(subject or "python"), str(section or "")), UNKNOWN_BASE + 9999))


def ranks_from_db() -> dict[str, dict[str, int]]:
    """直接从库里算一份分节顺序（后端 API 与静态导出共用）。

    返回 ``{subject: {section: rank}}`` —— 可以直接 JSON 序列化，
    前端拿它来排分组顺序，不用自己再猜一遍。
    """
    from . import db                                   # 延迟导入：避免循环依赖

    rows = db.query("""
        SELECT subject, source_section AS sec, COUNT(*) AS n, AVG(difficulty) AS av
        FROM problems WHERE status='published'
        GROUP BY subject, source_section
    """)
    pairs = {(r["subject"] or "python", r["sec"] or "") for r in rows}
    stats = {(r["subject"] or "python", r["sec"] or ""): float(r["av"] or 0) for r in rows}
    ranks = build_ranks(pairs, stats)

    out: dict[str, dict[str, int]] = {}
    for (subject, section), rank in sorted(ranks.items(), key=lambda kv: kv[1]):
        out.setdefault(subject, {})[section] = int(rank)
    return out

