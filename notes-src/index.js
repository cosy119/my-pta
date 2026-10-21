/* =========================================================================
   笔记渲染器（自托管，esbuild 打包成 web/notes/notes.js）
   =========================================================================

   为什么要自己打包
   ----------------
   GitHub Pages 那份站点是纯静态、零第三方 CDN 的（README 里对用户承诺过），
   所以 marked / highlight.js 都从 node_modules 打进 bundle，跟 CodeMirror
   编辑器（editor-src/ → web/editor/editor.js）一个套路。

   为什么不用 marked 默认的 renderer 回调
   --------------------------------------
   marked 11 → 12 之间 renderer 的参数从 `(code, infostring, escaped)`
   变成了 `({ text, lang, escaped })`。本文件里两个回调都写成**两种签名都认**
   的样子，免得将来升版本时静默渲染错。

   输入的 markdown 是 tools/export_notes.py 预处理过的
   （Obsidian 的 [[双链]] / callout / ==高亮== 都已转成下面认识的形式）
   ========================================================================= */
import { Marked } from 'marked';
import hljs from 'highlight.js/lib/core';

import bash from 'highlight.js/lib/languages/bash';
import python from 'highlight.js/lib/languages/python';
import c from 'highlight.js/lib/languages/c';
import cpp from 'highlight.js/lib/languages/cpp';
import java from 'highlight.js/lib/languages/java';
import ini from 'highlight.js/lib/languages/ini';
import makefile from 'highlight.js/lib/languages/makefile';
import markdown from 'highlight.js/lib/languages/markdown';
import json from 'highlight.js/lib/languages/json';
import xml from 'highlight.js/lib/languages/xml';
import cmake from 'highlight.js/lib/languages/cmake';
import vim from 'highlight.js/lib/languages/vim';
import asm from 'highlight.js/lib/languages/x86asm';
import plaintext from 'highlight.js/lib/languages/plaintext';

/* 笔记里出现过的 fence 语言（实测统计）→ highlight.js 语言名。
   长尾那些（apache / bind / sshconfig / cron / pro）没有现成 grammar，
   落到 plaintext 即可 —— 总比不显示强，也不会渲染错。 */
const LANGS = {
  bash, sh: bash, shell: bash, zsh: bash, console: bash,
  python, py: python, c, cpp, 'c++': cpp, java, ini, conf: ini, toml: ini,
  makefile, make: makefile, mk: makefile, markdown, md: markdown,
  json, xml, html: xml, yaml: ini, yml: ini, cmake, vim, asm,
  text: plaintext, txt: plaintext,
};
for (const [name, lang] of Object.entries(LANGS)) hljs.registerLanguage(name, lang);

const CALLOUT_KINDS = {
  success: 'ok', check: 'ok', done: 'ok',
  tip: 'tip', hint: 'tip', remember: 'tip',
  warning: 'warn', caution: 'warn', attention: 'warn',
  danger: 'danger', error: 'danger', failure: 'danger', fail: 'danger', bug: 'danger',
  important: 'imp', abstract: 'imp', summary: 'imp', tldr: 'imp',
  note: 'note', info: 'note', todo: 'note',
  question: 'ask', help: 'ask', faq: 'ask', example: 'ask', quote: 'ask', cite: 'ask',
};

/* 标题锚点 id。
   ★ 目标锚点来自 Obsidian 的双链（`#4.2 切片：[start:stop:step]`），
     所以这里只把空格换成连字符，其余（中文、冒号、方括号）原样留着 ——
     一致才能对上号。 */
function slugify(s) {
  return String(s).trim().replace(/\s+/g, '-').replace(/["'<>]/g, '');
}

function escapeHtml(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function highlight(text, lang) {
  const name = (lang || '').toLowerCase().split(/\s+/)[0];
  if (!name || name === 'text' || name === 'txt') return null;   // 4167 个无语言代码块，别浪费
  if (!hljs.getLanguage(name)) return null;
  try {
    return hljs.highlight(text, { language: name, ignoreIllegals: true }).value;
  } catch (e) {
    return null;
  }
}

/* callout：export_notes.py 把 `> [!info] 标题` 转成了
       :::callout <类型> <fold|open> <标题>
       正文（可以含代码块、列表、表格）
       :::
   折叠的（笔记里 1200+ 处「答案收起」）用 <details>，展开的用 <div>。 */
const calloutExt = {
  name: 'callout',
  level: 'block',
  start(src) { return src.indexOf(':::callout'); },
  tokenizer(src) {
    const m = /^:::callout[ \t]+(\S+)[ \t]+(\S+)[ \t]*([^\n]*)\n([\s\S]*?)\n:::[ \t]*(?:\n|$)/.exec(src);
    if (!m) return undefined;
    /* ★ 标题的 inline token 必须在**这里**算好：marked 18 的 renderer 上下文里
       只有 `this.parser`，没有 `this.lexer`，在 renderer 里调 inlineTokens 会
       抛 "Cannot read properties of undefined (reading 'inlineTokens')"。 */
    const titleRaw = m[3].trim();
    const token = {
      type: 'callout', raw: m[0],
      kind: CALLOUT_KINDS[m[1].toLowerCase()] || 'note',
      folded: m[2].toLowerCase() === 'fold',
      titleTokens: titleRaw ? this.lexer.inlineTokens(titleRaw) : [],
      tokens: [],
    };
    this.lexer.blockTokens(m[4], token.tokens);
    return token;
  },
  renderer(token) {
    const title = token.titleTokens.length
      ? this.parser.parseInline(token.titleTokens)
      : '提示';
    const body = this.parser.parse(token.tokens);
    const cls = 'callout callout-' + token.kind;
    if (token.folded) {
      return `<details class="${cls}" data-callout="${token.kind}">`
        + `<summary class="callout-title">${title}</summary>`
        + `<div class="callout-body">${body}</div></details>\n`;
    }
    return `<div class="${cls}" data-callout="${token.kind}">`
      + `<div class="callout-title">${title}</div>`
      + `<div class="callout-body">${body}</div></div>\n`;
  },
};

const marked = new Marked();
marked.use({ gfm: true, breaks: false }, { extensions: [calloutExt] });

marked.use({
  renderer: {
    /* 两种签名都认（见文件头说明） */
    code(codeOrToken, infostring) {
      const isTok = codeOrToken && typeof codeOrToken === 'object';
      const raw = isTok ? codeOrToken.text : codeOrToken;
      const info = (isTok ? codeOrToken.lang : infostring) || '';
      const name = info.toLowerCase().split(/\s+/)[0];
      const hl = highlight(raw, name);
      const cls = 'hljs' + (name ? ' language-' + name : '');
      return `<pre class="code-block"><code class="${cls}">`
        + (hl != null ? hl : escapeHtml(raw)) + '</code></pre>\n';
    },
  },
});

/* 给标题补 id：用后处理而不是 renderer 回调 ——
   marked 各版本 heading 回调的参数形状差异最大，后处理只认最终 HTML，稳。 */
function addHeadingIds(html) {
  const used = new Map();
  return html.replace(/<h([1-6])>([\s\S]*?)<\/h\1>/g, (all, lv, inner) => {
    const text = inner.replace(/<[^>]+>/g, '');
    let id = slugify(text);
    if (!id) return all;
    const n = used.get(id) || 0;
    used.set(id, n + 1);
    if (n) id += '-' + n;                      // 同名标题去重
    return `<h${lv} id="${id}">${inner}</h${lv}>`;
  });
}

/** markdown → HTML（笔记正文） */
export function renderNotes(md) {
  // Older exports may place custom blocks directly after a paragraph or
  // before a setext separator. Keep block boundaries explicit outside fences.
  const lines = String(md || '').split('\n'), normalized = [];
  let fence = null;
  for (const line of lines) {
    const marker = /^\s*(`{3,}|~{3,})/.exec(line);
    if (marker) {
      if (!fence) fence = marker[1];
      else if (marker[1][0] === fence[0] && marker[1].length >= fence.length) fence = null;
      normalized.push(line);
      continue;
    }
    if (!fence && /^:::callout\s/.test(line)) normalized.push('');
    normalized.push(line);
    if (!fence && /^:::\s*$/.test(line)) normalized.push('');
  }
  return addHeadingIds(marked.parse(normalized.join('\n')));
}

/** 目录树里显示的一行纯文本（去掉标记，给搜索/悬浮用） */
export function plain(md) {
  return String(md || '')
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/:::callout[^\n]*/g, ' ')
    .replace(/[#>*`|\-]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

export { slugify };
