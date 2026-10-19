/* ===========================================================================
   浏览器端判题（理论题 / 选择题 / 填空题）—— 零后端、零下载。

   它是什么
   --------
   `app/judge/compare.py` + `app/judge/runner_text.py` + `app/scoring.py`
   的 **JS 移植**。理论题没有「可执行的东西」：用户交的就是答案本身，
   判题 = 一堆字符串归一化 + 比对。所以这件事浏览器完全干得了。

   ★★ 口径必须与后端逐字节一致 ★★
   --------------------------------
   判题口径一旦分叉，同一份答案在「本地判」和「后端判」下会得到不同结果，
   而这个 bug 极其隐蔽（大多数答案仍然判得对，只在边角处悄悄分叉）。
   所以本文件的规矩是：**任何改动都必须先跑**

       node tools/verify_text_judge.mjs

   它会把题库里全部理论题 × 多种答案在 JS 侧跑一遍、在 Python 侧跑一遍，
   逐条比对 verdict / score。不一致就是回归。

   几个必须小心的地方（都踩过）
   ----------------------------
   1. **Unicode 空白**：Python 的 `str.split()` / `str.strip()` 认的空白是
      CPython 的 `Py_UNICODE_ISSPACE` 表，**不等于** JS 的 `\s`。
      差异举例：Python 认 `\x1c`~`\x1f`、`\x85`；JS 的 `\s` 认 `\ufeff`
      而 Python 不认。这里用显式字符类把 Python 的表抄下来。
   2. **`strip(chars)` 是按码点剥字符集合**，不是按子串。所以用 `[...s]`
      展开码点，别用下标（UTF-16 码元在非 BMP 上会错位）。
   3. **位置**：`_EDGE`（识别选项字母用）含 ASCII 的 `. ' "`，
      `_EDGE_PUNCT`（宽容剥标点用）**刻意不含**它们 ——
      ASCII 的 `. ' "` 在命令行里有意义（`cd ../..`、`echo -n "hi"`）。
      两个集合用途不同，绝不能合并。
   =========================================================================== */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.TextJudge = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /* ---------------------------------------------------------------
     Python 语义的小工具
     --------------------------------------------------------------- */

  /* CPython `Py_UNICODE_ISSPACE` 覆盖的空白集合（BMP）。
     `str.split()`（无参）、`str.strip()`（无参）用的就是它。 */
  const PY_WS_CLASS =
    '[\\t\\n\\v\\f\\r\\x1c-\\x1f \\x85\\u00a0\\u1680\\u2000-\\u200a' +
    '\\u2028\\u2029\\u202f\\u205f\\u3000]';
  const PY_WS_RE = new RegExp(PY_WS_CLASS, 'g');
  const PY_WS_RUN_RE = new RegExp(PY_WS_CLASS + '+', 'g');
  /* 只看单个字符是不是 Python 空白。★ 专用一个**不带 g** 的正则：
     带 g 的 `.test()` 会记住 lastIndex，连续调用会时对时错。 */
  const PY_WS_ONE_RE = new RegExp('^' + PY_WS_CLASS + '$');
  const PY_WS_TAIL_RE = new RegExp(PY_WS_CLASS + '+$');

  /* Python `text.rstrip()` */
  function pyRStrip(s) { return String(s).replace(PY_WS_TAIL_RE, ''); }

  /* Python `" ".join(text.split())`：按 Unicode 空白切、折成单空格 */
  function squeezeWs(text) {
    const s = String(text == null ? '' : text);
    if (!s) return '';
    const parts = s.split(PY_WS_RUN_RE).filter(function (x) { return x !== ''; });
    return parts.join(' ');
  }

  /* Python `text.strip()`：剥首尾的 Python 空白 */
  function pyStrip(s) {
    return pyStripChars(s, null);
  }

  /* Python `text.strip(chars)`：剥首尾的**字符集合**（按码点，不是子串） */
  function pyStripChars(s, chars) {
    const arr = Array.from(String(s == null ? '' : s));
    const drop = (chars == null)
      ? function (c) { return PY_WS_ONE_RE.test(c); }
      : function (c) { return chars.indexOf(c) >= 0; };
    let i = 0, j = arr.length;
    while (i < j && drop(arr[i])) i++;
    while (j > i && drop(arr[j - 1])) j--;
    return arr.slice(i, j).join('');
  }

  /* Python `text.startswith(pre)` */
  function startsWith(s, pre) { return String(s).indexOf(pre) === 0; }

  /* Python `str.isascii()` */
  function isAscii(s) {
    const arr = Array.from(String(s));
    for (let i = 0; i < arr.length; i++) if (arr[i].codePointAt(0) > 127) return false;
    return true;
  }

  /* Python `len(s)` —— 码点数，不是 UTF-16 码元数 */
  function pyLen(s) { return Array.from(String(s)).length; }

  /* Python f"{x:g}" —— 6 位有效数字、去掉尾零；指数 < -4 或 >= 6 时用科学计数法
     （指数至少两位，如 1e-06）。只用于生成给人看的提示文本，判定不依赖它。 */
  function fmtG(x) {
    const v = Number(x);
    if (!isFinite(v)) return String(v);
    if (v === 0) return '0';
    const exp = Math.floor(Math.log10(Math.abs(v)));
    if (exp < -4 || exp >= 6) {
      const parts = v.toExponential(5).split('e');
      let mant = parts[0];
      if (mant.indexOf('.') >= 0) mant = mant.replace(/0+$/, '').replace(/\.$/, '');
      const ei = parseInt(parts[1], 10);
      const ea = String(Math.abs(ei));
      return mant + 'e' + (ei < 0 ? '-' : '+') + (ea.length < 2 ? '0' + ea : ea);
    }
    let s = v.toPrecision(6);
    if (s.indexOf('.') >= 0 && s.indexOf('e') < 0) s = s.replace(/0+$/, '').replace(/\.$/, '');
    return s;
  }

  /* ---------------------------------------------------------------
     1. runner_text.py —— 答案归一化
     --------------------------------------------------------------- */

  /* 「对」的各种写法（判断题用） */
  const TRUE_WORDS = new Set(['对', '正确', '是', '√', '✓', 't', 'true', 'y', 'yes', 'right']);
  const FALSE_WORDS = new Set(['错', '错误', '否', '×', 'x', '✗', 'f', 'false', 'n', 'no', 'wrong']);

  /* ★ 只用于「识别单个选项字母」时顺手剥掉的首尾标点。
       识别完只返回那个字母本身，**绝不拿它去裁剪长答案**。 */
  const EDGE = ' \t\r\n.。、,，:：;；\'"“”‘’()（）[]【】<>';

  /* 把上交的答案整理成可比较的形式（对应 runner_text.normalize_answer） */
  function normalizeAnswer(text) {
    let s = pyStrip(String(text == null ? '' : text));
    if (!s) return '';

    const low = s.toLowerCase();
    const core0 = pyStrip(pyStripChars(s, EDGE));
    /* 只有「剥掉首尾标点」确实改变了内容时才认这个剥过的串 ——
       免得把 `true` / `false` 这类**命令**也当成判断题词 */
    const cand = core0 !== s ? core0 : s;

    if (TRUE_WORDS.has(low) || TRUE_WORDS.has(cand.toLowerCase())) return '对';
    if (FALSE_WORDS.has(low) || FALSE_WORDS.has(cand.toLowerCase())) return '错';

    /* 选择题：单字母/单数字 → 大写（`B.` / `（B）` / `“B”` 都归到 `B`） */
    if (pyLen(core0) === 1 && isAscii(core0)) return core0.toUpperCase();

    /* 形如「选 B」「答案：B」这种带前缀的，把前缀剥掉 */
    const pres = ['答案', '选', '答', 'answer', 'Answer', 'ANSWER'];
    for (let i = 0; i < pres.length; i++) {
      const pre = pres[i];
      if (startsWith(s, pre)) {
        const rest = pyStrip(pyStripChars(s.slice(pre.length), EDGE));
        if (pyLen(rest) === 1 && isAscii(rest)) return rest.toUpperCase();
      }
    }

    return s;
  }

  /* ---------------------------------------------------------------
     2. compare.py —— 输出比对
     --------------------------------------------------------------- */

  const CHECKERS = ['standard', 'ignore_trailing', 'token', 'float', 'oneof'];
  const ALT_PREFIX = '|';

  function toText(x) { return x == null ? '' : String(x); }

  function normalizeNewlines(t) {
    return String(t).replace(/\r\n/g, '\n').replace(/\r/g, '\n');
  }

  function linesDropTrailingBlank(text) {
    const lines = String(text).split('\n');
    while (lines.length && pyStrip(lines[lines.length - 1]) === '') lines.pop();
    return lines;
  }

  /* 人手打答案时最容易顺手带上的「排版类」标点。
     ★★ 刻意**不含** ASCII 的 `. ' " ( ) [ ]` —— 见文件头注释。 */
  const EDGE_PUNCT = ' \t\r\n。，、；：（）【】《》〈〉「」『』“”‘’…！？';

  /* 同一个答案的「宽容形式」集合（从严格到宽松），对应 compare.answer_forms */
  function answerForms(text) {
    const t = pyStrip(normalizeNewlines(toText(text)));
    const forms = new Set([squeezeWs(t)]);
    const core = pyStrip(pyStripChars(t, EDGE_PUNCT));
    if (core && core !== t) forms.add(squeezeWs(core));
    /* 在已有个形式的基础上，再叠一层命令归一化 */
    Array.from(forms).forEach(function (f) { forms.add(squeezeWs(normCmd(f))); });
    /* 再叠一层「家目录」归一化：/home/<谁> → ~，任意登录名都通吃 */
    Array.from(forms).forEach(function (f) { forms.add(squeezeWs(normHome(f))); });
    return forms;
  }

  /* `/home/<某个名字>` 这一整段（不含其后的路径分隔符） */
  const HOME_RE = /(?<![\w/])\/home\/[^/\s]+(?=\/|\s|$)/g;

  /* 把 `/home/<谁>` 折成 `~`：`cp -a /home/zhangsan/docs /tmp/` → `cp -a ~/docs /tmp/`。
     题库里别人的家目录写成占位符 `{user}`（显示时才替换成人名），答案只认 `~/...`，
     所以两边都折一遍，写 `/home/任意登录名/...` 也判得过。 */
  function normHome(text) { return String(text).replace(HOME_RE, '~'); }

  /* 纯字母的短选项，如 -l / -a / -lah（两个横杠的长选项、带数字的 -9、单独的 - 都不匹配） */
  const SHORT_OPT_RE = /^-[A-Za-z]+$/;

  /* 命令行的宽容归一化：空白折叠 + 相邻短选项合并 + 簇内字母排序去重。
     `ls -la /etc`、`ls -al /etc`、`ls -l -a /etc` 视为同一件事。 */
  function normCmd(text) {
    const toks = String(text).split(PY_WS_RUN_RE).filter(function (x) { return x !== ''; });
    const out = [];
    let i = 0;
    while (i < toks.length) {
      if (SHORT_OPT_RE.test(toks[i])) {
        let buf = '';
        while (i < toks.length && SHORT_OPT_RE.test(toks[i])) {
          buf += toks[i].slice(1);
          i++;
        }
        out.push('-' + Array.from(new Set(Array.from(buf))).sort().join(''));
        continue;
      }
      out.push(toks[i]);
      i++;
    }
    return out.join(' ');
  }

  /* 从期望值里取出「多个可接受答案」清单（每行以 `|` 开头） */
  function oneofAlternatives(expected) {
    const alts = [];
    normalizeNewlines(toText(expected)).split('\n').forEach(function (ln) {
      if (ln.indexOf(ALT_PREFIX) === 0) {
        const a = pyStrip(ln.slice(1));
        if (a !== '') alts.push(a);
      }
    });
    return alts;
  }

  /* Python `text.lstrip()` */
  function pyStripLeft(s) {
    const arr = Array.from(String(s == null ? '' : s));
    let i = 0;
    while (i < arr.length && PY_WS_ONE_RE.test(arr[i])) i++;
    return arr.slice(i).join('');
  }

  /* 这道题该不该按 oneof 口径判（对应 compare._uses_oneof）
     ★ 必须**同时**要求有 `|` 行：写错了 checker 却没写 `|` 时按 oneof 走会得到
       一份空的备选清单 —— 那等于把所有答案都判错，比按 standard 比还糟。 */
  function usesOneof(checker, expected) {
    if (!oneofAlternatives(expected).length) return false;
    return checker === 'oneof' || pyStripLeft(String(expected)).indexOf(ALT_PREFIX) === 0;
  }

  function diffHint(expected, actual, maxLines) {
    maxLines = maxLines || 6;
    const eLines = linesDropTrailingBlank(expected);
    const aLines = linesDropTrailingBlank(actual);
    const n = Math.max(eLines.length, aLines.length);
    for (let i = 0; i < n; i++) {
      const e = i < eLines.length ? eLines[i] : '<缺行>';
      const a = i < aLines.length ? aLines[i] : '<缺行>';
      if (pyRStrip(e) !== pyRStrip(a)) {
        return '第 ' + (i + 1) + ' 行起不同：期望 ' + repr(e) + ' / 实际 ' + repr(a);
      }
    }
    if (eLines.length !== aLines.length) {
      return '行数不同：期望 ' + eLines.length + ' 行 / 实际 ' + aLines.length + ' 行';
    }
    return '';
  }

  /* Python `repr()` 的近似 —— 只用于生成给人看的提示文本。
     ★ 引号选择是 Python 的规则：默认单引号；字符串里**有单引号且没有双引号**时
       改用双引号（否则答案里成对的单引号会被转义成一堆反斜杠，人看不下去）。 */
  function repr(s) {
    const str = String(s);
    const hasS = str.indexOf("'") >= 0, hasD = str.indexOf('"') >= 0;
    const q = (hasS && !hasD) ? '"' : "'";
    let out = q;
    Array.from(str).forEach(function (ch) {
      const cp = ch.codePointAt(0);
      if (ch === '\\') out += '\\\\';
      else if (ch === q) out += '\\' + ch;
      else if (ch === '\t') out += '\\t';
      else if (ch === '\n') out += '\\n';
      else if (ch === '\r') out += '\\r';
      else if (cp < 0x20 || cp === 0x7f) out += '\\x' + cp.toString(16).padStart(2, '0');
      else out += ch;
    });
    return out + q;
  }

  function closeEnough(a, b, eps) {
    if (a === b) return true;
    if (a !== a || b !== b) return false;            /* NaN */
    const diff = Math.abs(a - b);
    if (diff <= eps) return true;
    const scale = Math.max(Math.abs(a), Math.abs(b));
    return scale > 0 && diff / scale <= eps;
  }

  function compareFloat(e, a, eps) {
    const eT = e.split(PY_WS_RUN_RE).filter(function (x) { return x !== ''; });
    const aT = a.split(PY_WS_RUN_RE).filter(function (x) { return x !== ''; });
    if (eT.length !== aT.length) {
      return { ok: false, kind: 'wa',
               detail: '输出项数不同：期望 ' + eT.length + ' 项 / 实际 ' + aT.length + ' 项' };
    }
    for (let i = 0; i < eT.length; i++) {
      if (eT[i] === aT[i]) continue;
      const ev = Number(eT[i]), av = Number(aT[i]);
      const eOk = eT[i].trim() !== '' && isFinite(ev);
      const aOk = aT[i].trim() !== '' && isFinite(av);
      if (!eOk || !aOk) {
        return { ok: false, kind: 'wa',
                 detail: '第 ' + (i + 1) + ' 项不是数字：期望 ' + repr(eT[i]) + ' / 实际 ' + repr(aT[i]) };
      }
      if (!closeEnough(ev, av, eps)) {
        return { ok: false, kind: 'wa',
                 detail: '第 ' + (i + 1) + ' 项超出容差：期望 ' + repr(eT[i]) +
                         ' / 实际 ' + repr(aT[i]) + '（eps=' + fmtG(eps) + '）' };
      }
    }
    return { ok: true, kind: 'ok', detail: '' };
  }

  /* 比对实际输出与期望输出，对应 compare.compare */
  function compare(expected, actual, checker, eps) {
    const e = normalizeNewlines(toText(expected));
    const a = normalizeNewlines(toText(actual));
    const ck = CHECKERS.indexOf(checker) >= 0 ? checker : 'standard';
    const tol = (eps === undefined || eps === null) ? 1e-6 : Number(eps);

    /* ---- 完全一致（归一化后）---- */
    if (e === a) return { ok: true, kind: 'ok', detail: '' };

    /* ---- oneof 口径：命中任意一个可接受答案即通过 ----
       ★ 必须放在最前面 —— 这种题的期望值形如 "|B"，跟实际输出 "B" 永远不相等 */
    if (usesOneof(ck, e)) {
      const alts = oneofAlternatives(e);
      const aForms = answerForms(a);
      for (let i = 0; i < alts.length; i++) {
        const af = answerForms(alts[i]);
        let hit = false;
        af.forEach(function (x) { if (aForms.has(x)) hit = true; });
        if (hit) return { ok: true, kind: 'ok', detail: '' };
      }
      let shown = alts.slice(0, 4).map(repr).join(' / ');
      if (alts.length > 4) shown += ' 等 ' + alts.length + ' 个';
      return { ok: false, kind: 'wa', detail: '都不匹配，可接受答案：' + shown };
    }

    if (ck === 'float') return compareFloat(e, a, tol);

    if (ck === 'token') {
      if (squeezeWs(e) === squeezeWs(a)) return { ok: true, kind: 'ok', detail: '' };
      return { ok: false, kind: 'wa', detail: diffHint(e, a) };
    }

    let eLines, aLines;
    if (ck === 'ignore_trailing') {
      eLines = e.split('\n');
      aLines = a.split('\n');
    } else {
      eLines = linesDropTrailingBlank(e);
      aLines = linesDropTrailingBlank(a);
    }
    const eNorm = eLines.map(function (x) { return pyRStrip(x); });
    const aNorm = aLines.map(function (x) { return pyRStrip(x); });

    /* 逐元素比较（对应 Python 的列表 ==） */
    let same = eNorm.length === aNorm.length;
    if (same) {
      for (let i = 0; i < eNorm.length; i++) {
        if (eNorm[i] !== aNorm[i]) { same = false; break; }
      }
    }
    if (same) {
      return { ok: true, kind: 'ok', detail: '输出了多余的行尾空白，已按该题口径忽略' };
    }
    if (squeezeWs(e) === squeezeWs(a)) {
      return { ok: false, kind: 'pe', detail: '内容正确但空白/换行与期望不符' };
    }
    return { ok: false, kind: 'wa', detail: diffHint(e, a) };
  }

  /* ---------------------------------------------------------------
     3. scoring.py —— 分值分配
     --------------------------------------------------------------- */

  /* 把 total_score 尽量平均分给 n 个点，余数分给前面的 */
  function distributePoints(totalScore, n) {
    totalScore = parseInt(totalScore || 0, 10) || 0;
    n = parseInt(n || 0, 10) || 0;
    if (n <= 0) return [];
    if (totalScore <= 0) return new Array(n).fill(0);
    const base = Math.floor(totalScore / n);
    const rem = totalScore % n;
    const out = [];
    for (let i = 0; i < n; i++) out.push(base + (i < rem ? 1 : 0));
    return out;
  }

  /* 把库里存的 points 规范化（全 0 时按满分均分兜底） */
  function normalizePoints(rawPoints, totalScore) {
    const vals = (rawPoints || []).map(function (p) { return Math.max(0, parseInt(p || 0, 10) || 0); });
    if (!vals.length) return [];
    let sum = 0;
    vals.forEach(function (v) { sum += v; });
    if (sum === 0) return distributePoints(totalScore, vals.length);
    return vals;
  }

  /* 算一次提交的得分：只有 AC 拿分，得分 = 通过点分值之和 */
  function grade(rawPoints, verdicts, totalScore) {
    const pts = normalizePoints(rawPoints, totalScore);
    const n = Math.min(pts.length, (verdicts || []).length);
    const earned = [];
    for (let i = 0; i < n; i++) earned.push(verdicts[i] === 'AC' ? pts[i] : 0);
    while (earned.length < pts.length) earned.push(0);
    let score = 0;
    earned.forEach(function (x) { score += x; });
    let maxScore = 0;
    pts.forEach(function (x) { maxScore += x; });
    return { points: pts, earned: earned, score: score, max_score: maxScore };
  }

  /* ---------------------------------------------------------------
     4. 组装：理论题整题判定（对应 worker.py 的主循环）
     --------------------------------------------------------------- */

  /* 这道题能不能在浏览器里判（需要导出时带了完整测试点） */
  function canJudgeLocally(p) {
    return !!(p && p.cases && p.cases.length);
  }

  function judgeTextProblem(p, answer) {
    const cases = p.cases || [];
    if (!cases.length) return { error: '题库里没有这道题的测试点（导出时需加 --with-cases）' };

    const checker = p.checker || 'standard';
    const eps = (p.float_eps === undefined || p.float_eps === null) ? 1e-6 : Number(p.float_eps);
    const totalScore = parseInt(p.total_score || 0, 10) || 0;

    const norm = normalizeAnswer(answer);
    const actual = norm + '\n';

    const verdicts = [];
    const details = [];
    const outputs = [];
    let passed = 0, overall = 'AC', firstFail = '';

    cases.forEach(function (c) {
      const cmp = compare(c.expected_stdout || '', actual, checker, eps);
      let v, detail;
      if (cmp.ok) { v = 'AC'; detail = cmp.detail; }
      else { v = cmp.kind === 'pe' ? 'PE' : 'WA'; detail = cmp.detail; }
      verdicts.push(v); details.push(detail || ''); outputs.push(actual);
      if (v === 'AC') passed++;
      else if (overall === 'AC') { overall = v; firstFail = detail; }
    });

    const g = grade(cases.map(function (c) { return c.points; }), verdicts, totalScore);

    return {
      verdict: overall,
      score: g.score,
      max_score: g.max_score,
      passed: passed,
      total: cases.length,
      message: firstFail,
      normalized: norm,
      cases: cases.map(function (c, i) {
        return {
          verdict: verdicts[i], points: g.points[i], earned: g.earned[i],
          stdin: c.stdin || '', expected: c.expected_stdout || '',
          stdout: outputs[i], detail: details[i],
          is_sample: !!c.is_sample, ord: c.ord, time_ms: 0,
        };
      }),
    };
  }

  return {
    /* 归一化 */
    normalizeAnswer: normalizeAnswer,
    /* 比对 */
    compare: compare,
    answerForms: answerForms,
    oneofAlternatives: oneofAlternatives,
    normCmd: normCmd,
    /* 计分 */
    grade: grade,
    normalizePoints: normalizePoints,
    distributePoints: distributePoints,
    /* 组装 */
    judgeTextProblem: judgeTextProblem,
    canJudgeLocally: canJudgeLocally,
    /* 常量（对拍脚本要用） */
    CHECKERS: CHECKERS,
    EDGE: EDGE,
    EDGE_PUNCT: EDGE_PUNCT,
    squeezeWs: squeezeWs,
  };
});
