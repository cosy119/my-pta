"""理论题 runner：选择题 / 判断题 / 填空题。

这类题**没有可执行的东西** —— 用户提交的内容本身就是答案。
所以这个 runner 不启任何子进程，直接把提交文本当作「程序输出」回传，
后面的 compare / scoring / 历史记录 / 进度统计**全部复用同一套管道**，
一行判题逻辑都不用另写。

这么做的理由
------------
PTA 上选择题和编程题是同一套「测试点 + 分值」模型：交上去 → 判对错 → 给分。
既然模型一致，就没必要给理论题另开一条判题链路（那会同时多出两套
提交记录、两套进度、两套历史回填）。让理论题的「运行结果」= 答案本身，
一切自动统一。

★ 答案归一化
------------
人手输入总会带点噪声：`b`、`B`、`B.`、`B、`、`  B  `。
这里先做一层轻量归一化（去空白、去首尾标点、单个字母转大写、
把「正确/√/T」这类等价的判断词收成规范写法），
剩下的等价写法（比如 `ls -a /` 与 `ls -la /`）交给 `oneof` checker 处理 ——
它允许一道题挂多个可接受答案。
"""
from __future__ import annotations

from pathlib import Path

from .runner_base import CaseResult, Limits

# 「对」的各种写法（判断题用）
_TRUE_WORDS = {"对", "正确", "是", "√", "✓", "t", "true", "y", "yes", "right"}
_FALSE_WORDS = {"错", "错误", "否", "×", "x", "✗", "f", "false", "n", "no", "wrong"}

# 用来「识别」单个字母时，允许被顺手带上的首尾标点。
#
# ★★ 这套标点**只用于判断「这是不是一个选项字母」**，判断完只返回那个字母本身，
#    绝不拿它去裁剪长答案。原因见 compare._EDGE_PUNCT 的注释：
#    ASCII 的 `. ' "` 在命令行里是有意义的（`cd ../..`、`echo -n "hi"`），
#    早期版本统一剥掉，把命令答案的最后一个字符吃掉了，题目永远判不过。
_EDGE = " \t\r\n.。、,，:：;；'\"“”‘’()（）[]【】<>"


def normalize_answer(text: str) -> str:
    """把用户交上来的答案整理成可比较的形式。

    只做「明显等价」的归一化，绝不猜意图：
    - 去首尾空白
    - 单个 ASCII 字母 → 大写（`b`、`B.`、`（B）` 都收成 `B`）
    - 判断题的各种写法 → 统一成 `对` / `错`
    - **其余情况原样保留**（含中间的、以及末尾的标点）——
      命令里的引号与点号是答案的一部分，交给 `oneof` 去宽容
    """
    s = str(text or "").strip()
    if not s:
        return ""

    # 判断题：先把整串收成规范词
    low = s.lower()
    core0 = s.strip(_EDGE).strip()
    # 只有「剥掉首尾标点」确实改变了内容时才认这个剥过的串 ——
    # 免得把 `true` / `false` 这类**命令**也当成判断题词
    cand = core0 if core0 != s else s
    if low in _TRUE_WORDS or cand.lower() in _TRUE_WORDS:
        return "对"
    if low in _FALSE_WORDS or cand.lower() in _FALSE_WORDS:
        return "错"

    # 选择题：单字母/单数字 → 大写（`B.` / `（B）` / `“B”` 都归到 `B`）
    if len(core0) == 1 and core0.isascii():
        return core0.upper()

    # 形如「选 B」「答案：B」这种带前缀的，把前缀剥掉
    for pre in ("答案", "选", "答", "answer", "Answer", "ANSWER"):
        if s.startswith(pre):
            rest = s[len(pre):].strip(_EDGE).strip()
            if len(rest) == 1 and rest.isascii():
                return rest.upper()

    return s


class TextRunner:
    """理论题：提交内容即输出。"""

    lang = "text"

    def __init__(self, label: str = "text"):
        self.label = label
        self._answer = ""

    def prepare(self, code: str, workdir: Path) -> tuple[bool, str]:
        # 空答案**不报 CE** —— 理论题没有「编译」这回事，
        # 交空白就是没答对，让它走正常的比对流程判 WA 更诚实
        self._answer = normalize_answer(code)
        return True, ""

    def run_case(self, workdir: Path, stdin_bytes: bytes, limits: Limits) -> CaseResult:
        # 不启动子进程：直接把答案当 stdout 交回去走比对
        out = (self._answer + "\n").encode("utf-8")
        return CaseResult(verdict="OK", time_ms=0, mem_kb=0, stdout=out, stderr=b"",
                          exit_code=0)

    def cleanup(self, workdir: Path) -> None:
        self._answer = ""
