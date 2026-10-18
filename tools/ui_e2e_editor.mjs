/* ===================================================================
   智能编辑器（CodeMirror）—— 真 Chrome 端到端测试

   为什么必须真浏览器
   ------------------
   编辑器这东西全是**交互**：缩进、括号配对、补全面板、Tab 键往哪儿走。
   jsdom 里既没有真实键盘事件流（beforeinput / keydown 的默认行为、
   焦点的转移），也没有布局（补全面板要真的量位置才会出现）。
   拿 jsdom 测这些等于测了个寂寞 —— 只有真 Chrome 说了算。

   它验的是**发布产物**：直接服务 `docs/`（GitHub Pages 上那一份），
   所以顺带证明了「公开静态网页无需额外服务即可使用」。
   ★ 不连后端：全程离线，正好也是绝大多数人的使用方式。

   用法（在仓库根目录下）：
     NODE_MODULES_DIR=<含 puppeteer-core 的目录> node tools/ui_e2e_editor.mjs

   默认用系统 Chrome，不下载浏览器。
   =================================================================== */
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { createRequire } from 'node:module';

function loadDep(name, extra) {
  const tries = [createRequire(import.meta.url)];
  const dirs = [process.env.NODE_MODULES_DIR, ...(extra || [])].filter(Boolean);
  for (const d of dirs) tries.push(createRequire(path.join(d, 'noop.js')));
  for (const req of tries) {
    try { return req(name); } catch (e) { /* 试下一个 */ }
  }
  console.error('找不到 ' + name + '。\n'
    + '  装：npm install ' + name + '\n'
    + '  然后：NODE_MODULES_DIR=<含它的目录> node tools/ui_e2e_editor.mjs');
  process.exit(3);
}
const puppeteer = loadDep('puppeteer-core', [path.join(process.cwd(), 'experiments', 'pyodide-judge', 'node_modules')]);

const CHROME_PATHS = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
];
const CHROME = CHROME_PATHS.find(p => fs.existsSync(p));
if (!CHROME) { console.error('找不到系统 Chrome/Edge'); process.exit(3); }

const CWD = process.cwd();
const DOCS = path.join(CWD, 'docs');
const BANK = JSON.parse(fs.readFileSync(path.join(DOCS, 'problems.json'), 'utf8'));

let PASS = 0;
const FAIL = [];
function check(name, cond, extra) {
  if (cond) { PASS++; console.log('  [PASS] ' + name + (extra ? '  ' + extra : '')); }
  else { FAIL.push(name); console.log('  [FAIL] ' + name + (extra !== undefined ? '  ' + extra : '')); }
}
const sleep = ms => new Promise(r => setTimeout(r, ms));

function serveDir(root) {
  const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json' };
  const srv = http.createServer((req, res) => {
    const p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    const f = path.normalize(path.join(root, p === '/' ? 'index.html' : p));
    if (!f.startsWith(root) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) {
      res.statusCode = 404; return res.end('404');
    }
    res.setHeader('Content-Type', (MIME[path.extname(f)] || 'application/octet-stream') + '; charset=utf-8');
    res.end(fs.readFileSync(f));
  });
  return new Promise(r => srv.listen(0, '127.0.0.1', () => r(srv)));
}

/* ---------------- 页面侧的小动作 ---------------- */

/* 编辑器「挂载完成」的唯一可靠信号：宿主 div 不再是 hidden 且里面真有 CM 的 DOM。
   ★ 别只看 #codeEditor 在不在 —— 它一开始就在（hidden），那是给回退留的位置。 */
async function waitEditor(page) {
  await page.waitForFunction(() => {
    const h = document.getElementById('codeEditor');
    return !!(h && !h.hidden && h.querySelector('.cm-content'));
  }, { timeout: 25000 });
}
/* ★★ 切题时必须连**题号**一起等。
   只等「#codeEditor 非空」是假信号 —— hashchange 的处理器是异步派的，
   页面里那一瞬间还挂着**上一道题的**编辑器和 DOM。
   于是紧接着的「点进编辑器打字」会打在旧实例上：
   回调里 `CUR.id === problemId` 一比对（新题号 vs 旧实例）就不写草稿了，
   表现出来就是「明明打了字，localStorage 却是 null」。
   拿题号角标（`.pill.p-pri` 里的 #id）当「这一题真的渲染好了」的凭据。 */
async function waitProblem(page, id) {
  await page.waitForFunction(expected => {
    const badge = document.querySelector('.pill.p-pri');
    // 2026-10-18 起角标显示科内独立编号（DS-07），全局 id 挪到 data-pid
    if (!badge || String(badge.dataset.pid) !== String(expected)) return false;
    const h = document.getElementById('codeEditor');
    return !!(h && !h.hidden && h.querySelector('.cm-content'));
  }, { timeout: 25000 }, id);
}
async function openProblem(page, id) {
  const cur = await page.evaluate(() => location.hash);
  if (cur !== '#/p/' + id) await page.evaluate(id => { location.hash = '#/p/' + id; }, id);
  await waitProblem(page, id);
}
/* 理论题：等题号角标对上（它没有编辑器，等不了 #codeEditor），
   而后**故意再等一会儿** —— 要证明的是「编辑器没被挂上」，
   不是「还没来得及挂上」。 */
async function waitTheory(page, id) {
  const cur = await page.evaluate(() => location.hash);
  if (cur !== '#/p/' + id) await page.evaluate(id => { location.hash = '#/p/' + id; }, id);
  await page.waitForFunction(expected => {
    const b = document.querySelector('.pill.p-pri');
    return !!(b && String(b.dataset.pid) === String(expected));
  }, { timeout: 20000 }, id);
  await sleep(500);
}
/* ★ 内容从**被隐藏的 textarea** 里读 —— 那不是替身，是 onChange 实时写回的真镜像。
   比去啃 contenteditable 的 DOM 稳得多（CM 只渲染视口内的行）。 */
const value = page => page.$eval('#codeBox', el => el.value);
const visible = page => page.$eval('#codeBox', el => getComputedStyle(el).display !== 'none');
async function focusEditor(page) { await page.click('.cm-content'); }
async function clearEditor(page) {
  await focusEditor(page);
  await page.keyboard.down('Control');
  await page.keyboard.press('KeyA');
  await page.keyboard.up('Control');
  await page.keyboard.press('Backspace');
  await sleep(60);
}
async function type(page, text) {
  await page.keyboard.type(text);
  await sleep(150);
}
/* 等补全面板真的开好。
   ★★ 这里有个必须等的坑：`acceptCompletion` 里有一道 interactionDelay（默认 75ms），
   面板刚弹出就按 Tab 会被它拒掉 —— 于是命令返回 false、Tab 掉进「缩进」分支。
   真人从看见面板到抬手按 Tab 怎么都超过 75ms，只有测试会快到踩雷。
   所以「面板在不在」和「能不能接受」是两件事，后者要额外等。 */
async function waitCompletion(page) {
  await page.waitForSelector('.cm-tooltip-autocomplete', { timeout: 4000 });
  await sleep(150);
}
const tooltipOpen = async page => !!(await page.$('.cm-tooltip-autocomplete'));
const labels = page => page.$$eval('.cm-tooltip-autocomplete .cm-completionLabel',
  els => els.map(e => e.textContent));
/* 某个词在当前语言的高亮下**拿到的样式类名**（没被包进 span 就是空串）。
   ★ 别用「有没有 span」来判断高亮换没换：defaultHighlightStyle 里
     `definition(variableName)` 也是有样式的，于是 C 里 `int namespace;` 的
     `namespace` 照样是个带样式的变量名 —— 两边都有 span，判据不成立。
     比**类名**才真的说明「同一个词被两门语言判成了不同的语法成分」。 */
const tokenClass = (page, word) => page.evaluate(w => {
  for (const line of document.querySelectorAll('.cm-content .cm-line')) {
    for (const sp of line.querySelectorAll('span')) if (sp.textContent === w) return sp.className;
  }
  return '';
}, word);

/* ---------------- 夹具 ---------------- */

const py = BANK.items.filter(x => x.line === 'python');
const ds = BANK.items.filter(x => x.subject === 'ds');
/* ★ 理论题要分两种挑：填空题才有 textarea，选择题是点圆标、**根本没有 #codeBox**。
   第一版只挑了「第一道理论题」，结果撞上选择题 → 断言 #codeBox 时元素不存在直接抛错。 */
const theoryFill = BANK.items.find(x => x.line === 'text' && !x.is_choice && !(x.choices || []).length);
const theoryMc = BANK.items.find(x => x.line === 'text' && x.is_choice && (x.choices || []).length > 2);
if (py.length < 2 || !ds.length || !theoryFill || !theoryMc) {
  console.error('题库里找不到合适的 Python×2 / 数据结构 / 理论题（填空+选择），测试无法进行'); process.exit(5);
}
const PY1 = py[0], PY2 = py[1], DS = ds[0];
const T_FILL = theoryFill, T_MC = theoryMc;

async function run() {
  console.log('== 智能编辑器 · 真 Chrome 端到端 ==');
  console.log('服务目录：docs/（发布产物）  ' + BANK.count + ' 题');
  console.log('夹具：Python #' + PY1.id + ' / #' + PY2.id + '、数据结构 #' + DS.id
    + '、理论题 #' + T_FILL.id + '（填空）/ #' + T_MC.id + '（选择）\n');

  const srv = await serveDir(DOCS);
  const BASE = 'http://127.0.0.1:' + srv.address().port + '/';

  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: 'new',
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });
  const page = await browser.newPage();
  page.__base = BASE;
  await page.setViewport({ width: 1400, height: 900 });
  const pageErrors = [];
  page.on('pageerror', e => pageErrors.push(String(e && e.message || e)));
  page.on('console', m => { if (m.type() === 'error') pageErrors.push('console: ' + m.text()); });

  try {
    /* ---------- [1] 编辑器真的挂上去了 ---------- */
    console.log('[1] 打开 Python 题 → 编辑器应替换 textarea');
    await page.goto(BASE, { waitUntil: 'load' });
    await page.waitForFunction(() => {
      const app = document.getElementById('app');
      return app && app.innerHTML && !app.innerHTML.includes('正在加载');
    }, { timeout: 30000 });

    await page.goto(BASE + '#/p/' + PY1.id, { waitUntil: 'load' });
    await waitProblem(page, PY1.id);
    check('编辑器挂载成功（.cm-editor 有内容）',
      await page.$eval('.cm-editor', el => el.clientHeight > 100),
      await page.$eval('.cm-editor', el => '高 ' + Math.round(el.clientHeight) + 'px'));
    check('原 textarea 让位（display:none）', (await visible(page)) === false);
    check('行号槽在（lineNumbers）', !!(await page.$('.cm-gutters .cm-lineNumbers')));
    check('分栏拖拽条还在', !!(await page.$('#problemDivider')));
    check('键盘操作说明可见并提到 Esc / Tab',
      await page.$eval('.editorKeys', el => /Esc/.test(el.textContent) && /Tab/.test(el.textContent)),
      (await page.$eval('.editorKeys', el => el.textContent)).slice(0, 46) + '…');

    /* ---------- [2] 缩进：回车按语言规则 ---------- */
    console.log('\n[2] 缩进（回车按语言规则）');
    await clearEditor(page);
    await type(page, 'def f():');
    await page.keyboard.press('Enter');
    await sleep(80);
    let v = await value(page);
    check('Python：`def f():` 回车后缩进 4 空格', v === 'def f():\n    ', JSON.stringify(v));
    await type(page, 'pass');
    check('Python：正文接着写还在缩进里', (await value(page)) === 'def f():\n    pass',
      JSON.stringify(await value(page)));

    await openProblem(page, DS.id);
    await clearEditor(page);
    await type(page, 'int main(void) {');
    await page.keyboard.press('Enter');
    await sleep(80);
    await type(page, 'return 0;');
    v = await value(page);
    /* ★ 期望值里带着 `}` —— 输入 `{` 时它是被自动补出来的，不是我们打的。
       （第一版这里写成不带 `}`，于是把「是对的」判成了「错的」。） */
    check('C/C++：`{` 回车后缩进 4 空格', v === 'int main(void) {\n    return 0;\n}', JSON.stringify(v));

    /* ---------- [3] 括号与引号配对 ---------- */
    console.log('\n[3] 括号 / 引号配对与包裹');
    await clearEditor(page);
    await type(page, '(');
    check('输入 `(` 自动补出 `)`', (await value(page)) === '()', JSON.stringify(await value(page)));
    await type(page, 'x');
    check('光标在括号中间（继续打字落在里面）', (await value(page)) === '(x)',
      JSON.stringify(await value(page)));
    await clearEditor(page);
    await type(page, '[]');
    check('输入 `[` 自动补出 `]`', (await value(page)) === '[]', JSON.stringify(await value(page)));
    await clearEditor(page);
    await type(page, '{}');
    check('输入 `{` 自动补出 `}`', (await value(page)) === '{}', JSON.stringify(await value(page)));

    await clearEditor(page);
    await type(page, 'abc');
    await page.keyboard.down('Control'); await page.keyboard.press('KeyA'); await page.keyboard.up('Control');
    await type(page, '(');
    check('选中文字后用 `(` 包裹', (await value(page)) === '(abc)', JSON.stringify(await value(page)));
    await page.keyboard.down('Control'); await page.keyboard.press('KeyA'); await page.keyboard.up('Control');
    await type(page, '"');
    check('选中文字后用 `"` 包裹', (await value(page)) === '"(abc)"', JSON.stringify(await value(page)));

    /* ---------- [4] 补全 ---------- */
    console.log('\n[4] 本地补全（不联网、不走后端）');
    await clearEditor(page);
    await type(page, 'retu');
    await waitCompletion(page);
    check('输入 `retu` 弹出补全面板', await tooltipOpen(page));
    check('面板里有 `return` 关键字', (await labels(page)).includes('return'),
      (await labels(page)).slice(0, 6).join(','));
    await page.keyboard.press('Escape');
    await sleep(120);
    check('Esc 关掉补全面板', !(await tooltipOpen(page)));
    await page.keyboard.down('Control');
    await page.keyboard.press('Space');
    await page.keyboard.up('Control');
    await sleep(250);
    check('Ctrl+空格 把提示重新叫出来', await tooltipOpen(page), (await labels(page)).length + ' 项');

    await clearEditor(page);
    await type(page, 'for');
    await waitCompletion(page);
    const ls = await labels(page);
    /* ★ 同一个词条出现两次是对的：一条是代码片段、一条是关键字。
       第一版这里断言「含 for 且含 return」——`return` 跟 `for` 根本不匹配，
       那条断言测的是我自己的想当然。 */
    check('`for` 同时给出代码片段和关键字（两项）',
      ls.filter(x => x === 'for').length === 2, ls.join(','));
    await page.keyboard.press('Escape');
    await sleep(120);

    /* ---------- [5] Tab 行为 ---------- */
    console.log('\n[5] Tab / Shift+Tab / Enter');
    await clearEditor(page);
    await type(page, 'retu');
    await waitCompletion(page);
    check('（前提）补全面板已打开', await tooltipOpen(page));
    await page.keyboard.press('Tab');
    await sleep(150);
    check('有候选时 Tab = 接受补全', (await value(page)) === 'return', JSON.stringify(await value(page)));
    check('接受后补全面板关掉', !(await tooltipOpen(page)));

    await clearEditor(page);
    await type(page, 'zzz');           /* 不匹配任何候选 → 面板不弹 */
    check('（前提）没有候选词', !(await tooltipOpen(page)));
    await page.keyboard.press('Tab');
    await sleep(120);
    check('没有候选时 Tab = 缩进一级', (await value(page)) === '    zzz', JSON.stringify(await value(page)));
    /* ★ puppeteer 25 的键名表不吃 `'Shift+Tab'` / `'Control+Space'` 这种合并写法
       （它拿整串去查表 → Unknown key）。组合键一律拆成 down / press / up。 */
    await page.keyboard.down('Shift');
    await page.keyboard.press('Tab');
    await page.keyboard.up('Shift');
    await sleep(120);
    check('Shift+Tab = 减少缩进', (await value(page)) === 'zzz', JSON.stringify(await value(page)));

    await clearEditor(page);
    await type(page, 'zzz');
    await page.keyboard.press('Tab');
    await sleep(120);
    check('（前提）Tab 已把内容缩进', (await value(page)) === '    zzz');
    await page.keyboard.press('Escape');
    await sleep(80);
    await page.keyboard.press('Tab');
    await sleep(200);
    const stillIn = await page.evaluate(() => {
      const host = document.querySelector('.codeEditor');
      return !!(host && host.contains(document.activeElement));
    });
    check('Esc 后按 Tab 能离开编辑器（焦点不在编辑器里）', stillIn === false);
    check('而且这一下 Tab 没有顺手改代码', (await value(page)) === '    zzz',
      JSON.stringify(await value(page)));
    check('焦点确实落到页面里别的东西上',
      await page.evaluate(() => document.activeElement !== document.body
        && !document.querySelector('.codeEditor').contains(document.activeElement)),
      await page.evaluate(() => document.activeElement.tagName + (document.activeElement.id ? '#' + document.activeElement.id : '')));

    await focusEditor(page);
    await clearEditor(page);
    await type(page, 'for');
    await waitCompletion(page);
    check('（前提）补全面板已打开', await tooltipOpen(page));
    await page.keyboard.press('Enter');
    await sleep(150);
    v = await value(page);
    check('Enter 保持换行（不会被拿去接受补全）', v.indexOf('for\n') === 0 && v.indexOf('{') < 0,
      JSON.stringify(v));

    /* ---------- [6] 切题草稿 ---------- */
    console.log('\n[6] 切题 / 刷新后草稿仍在');
    await openProblem(page, PY1.id);
    await clearEditor(page);
    await type(page, 'DRAFT_ONE_42');
    await sleep(150);
    /* 黑盒一点：只问「有值等于这段草稿的条目吗」，不去猜 key 长什么样。
       （顺带守住刚修的那个坑：key 必须以 `pta.draft.` 开头，
        否则「导出进度」按前缀捞草稿会一份都捞不到。） */
    const saved = await page.evaluate(() => {
      const hit = [];
      for (let i = 0; i < localStorage.length; i++) {
        const k = localStorage.key(i);
        if (localStorage.getItem(k) === 'DRAFT_ONE_42') hit.push(k);
      }
      return hit;
    });
    check('草稿已落盘', saved.length === 1, JSON.stringify(saved));
    check('草稿的 key 是规范的 `pta.draft.<id>`（否则导出进度捞不到它）',
      saved[0] === 'pta.draft.' + PY1.id, String(saved[0]));

    await openProblem(page, PY2.id);
    check('切到另一题：编辑器是新的、内容不串', (await value(page)) === '',
      JSON.stringify(await value(page)));

    /* 旧格式草稿的迁移。老版本把 `LS.draft + id` 当 key 用了，可 LS.draft 是个函数，
       拼出来的字面量就是下面这串 —— 老用户浏览器里存的草稿全长这样。
       升级不能让人把草稿弄丢，所以写一份进去看读不读得回来。 */
    const legacyKey = "p => 'pta.draft.' + p" + PY2.id;
    await page.evaluate((k, v) => localStorage.setItem(k, v), legacyKey, 'LEGACY_DRAFT_9');
    await page.reload({ waitUntil: 'load' });
    await waitProblem(page, PY2.id);
    check('旧格式的草稿读得回来（升级不丢草稿）', (await value(page)) === 'LEGACY_DRAFT_9',
      JSON.stringify(await value(page)));
    check('而且顺手搬到了规范的 key 上',
      await page.evaluate((oldK, id) => localStorage.getItem(oldK) === null
        && localStorage.getItem('pta.draft.' + id) === 'LEGACY_DRAFT_9', legacyKey, PY2.id));

    await openProblem(page, PY1.id);
    check('切回来：草稿回来了', (await value(page)) === 'DRAFT_ONE_42', JSON.stringify(await value(page)));

    await page.reload({ waitUntil: 'load' });
    await waitProblem(page, PY1.id);
    check('整页刷新后草稿也还在', (await value(page)) === 'DRAFT_ONE_42', JSON.stringify(await value(page)));
    check('草稿就是提交/自测要取的那份内容（codeValue 一致）',
      await page.evaluate(() => typeof codeValue === 'function' && codeValue() === document.getElementById('codeBox').value
        && codeValue() === 'DRAFT_ONE_42'));

    /* ---------- [7] C / C++ 语言切换 ---------- */
    console.log('\n[7] C / C++ 切换：换高亮和提示，不清空代码');
    await openProblem(page, DS.id);
    const selOpts = await page.$$eval('#langSel option', els => els.map(e => e.value));
    check('数据结构题有 C/C++ 语言下拉', selOpts.length === 2 && selOpts.indexOf('c') >= 0 && selOpts.indexOf('cpp') >= 0,
      selOpts.join('/'));
    check('默认语言是 C++（下拉第一项）',
      (await page.$eval('#langSel', el => el.value)) === 'cpp');

    await clearEditor(page);
    await type(page, 'MARK_CX_7');
    check('记号已写上（后面拿它证明切换不清空）', (await value(page)) === 'MARK_CX_7');

    await page.select('#langSel', 'c');
    await sleep(300);
    check('切到 C 之后代码没被清空', (await value(page)) === 'MARK_CX_7', JSON.stringify(await value(page)));
    check('切到 C 之后编辑器仍在（textarea 仍隐藏）', (await visible(page)) === false);
    check('切到 C 之后提示文案变了',
      (await page.$eval('#langHint', el => el.textContent)).includes('gcc'),
      (await page.$eval('#langHint', el => el.textContent)).slice(0, 40));

    await clearEditor(page);
    await type(page, 'main');
    await waitCompletion(page);
    const cLabels = await labels(page);
    check('C 的补全里有 `main` 片段', cLabels.includes('main'), cLabels.slice(0, 6).join(','));
    await page.keyboard.press('Tab');
    await sleep(200);
    v = await value(page);
    check('C 的 main 片段展开成 `int main(void)`', v.includes('int main(void)'), JSON.stringify(v.slice(0, 40)));

    await page.select('#langSel', 'cpp');
    await sleep(250);
    check('再从 C 切回 C++：代码还是没清空', (await value(page)).includes('int main(void)'),
      JSON.stringify((await value(page)).slice(0, 40)));
    check('切回 C++ 后提示文案也回来了',
      (await page.$eval('#langHint', el => el.textContent)).includes('g++'));
    await clearEditor(page);
    await type(page, 'main');
    await waitCompletion(page);
    await page.keyboard.press('Tab');
    await sleep(200);
    v = await value(page);
    check('C++ 的 main 片段展开成 `int main()`（补全源真跟着语言变了）', v.includes('int main()'), JSON.stringify(v.slice(0, 40)));
    check('切换语言后写下的代码能提交（codeValue 取到的是编辑器内容）',
      await page.evaluate(() => codeValue() === document.getElementById('codeBox').value && codeValue().length > 0));

    /* 高亮：跨语言（Python ↔ C++）才是真差异。
       ★★ 先把一个事实钉在这里：C 与 C++ 在 CodeMirror 里用的是**同一套 Lezer 语法**
       （`@codemirror/lang-cpp` 并没有单独的 C 语法），所以那两个选项之间
       高亮本来就一模一样 —— 跟着换的是提示与补全片段（上面已经逐条验过）。
       钉住它，免得以后有人看见「切 C/C++ 高亮没变」当成 bug 去修。 */
    await clearEditor(page);
    await type(page, 'int namespace;');
    await sleep(400);
    const cppCls = await tokenClass(page, 'namespace');
    await page.select('#langSel', 'c');
    await sleep(400);
    const cCls = await tokenClass(page, 'namespace');
    check('C 与 C++ 共用一套语法 → 高亮一致（这是事实，不是缺陷）',
      cppCls !== '' && cppCls === cCls, 'C++=' + cppCls + ' / C=' + cCls);

    await openProblem(page, PY1.id);
    await clearEditor(page);
    await type(page, 'int namespace;');
    await sleep(400);
    const pyCls = await tokenClass(page, 'namespace');
    check('换一种语言（C++ ↔ Python）高亮就完全是另一回事了',
      pyCls !== cppCls, 'Python=' + (pyCls || '(无样式)') + ' / C++=' + cppCls);

    /* ---------- [8] 理论题保持原样 ---------- */
    console.log('\n[8] 理论题保持原有输入方式');
    await waitTheory(page, T_FILL.id);
    check('填空题没挂编辑器', !(await page.$('.cm-editor')));
    check('填空题还是原来的输入框', await visible(page));
    await waitTheory(page, T_MC.id);
    check('选择题也没挂编辑器', !(await page.$('.cm-editor')));
    check('选择题还是点圆标作答', !!(await page.$('.choiceList')) && !(await page.$('#codeBox')));

    /* ---------- [9] 加载失败 → 回退，且不是「一次失败终身降级」 ---------- */
    console.log('\n[9] 编辑器加载失败 → 回退到原输入框');
    const page2 = await browser.newPage();
    await page2.setViewport({ width: 1400, height: 900 });
    let blockEditor = true;
    await page2.setRequestInterception(true);
    page2.on('request', req => {
      if (blockEditor && /\/editor\/editor\.js/.test(req.url())) req.abort();
      else req.continue();
    });
    const errs2 = [];
    page2.on('pageerror', e => errs2.push(String(e && e.message || e)));

    await page2.goto(BASE + '#/p/' + PY1.id, { waitUntil: 'load' });
    await sleep(1200);
    check('拿不到编辑器脚本时：textarea 正常显示', await visible(page2));
    check('回退时把编辑器宿主藏起来了',
      await page2.$eval('#codeEditor', el => el.hidden === true));
    check('回退时给了人话提示',
      (await page2.$$eval('.toast', els => els.map(e => e.textContent).join('|'))).includes('回退'),
      await page2.$$eval('.toast', els => els.map(e => e.textContent).join('|')));
    await focusEditorFallback(page2);
    await page2.keyboard.type('FALLBACK_OK');
    await sleep(80);
    /* ★ 别断言「等于 FALLBACK_OK」：localStorage 是这个 origin 共享的，
       page1 在 [6] 里留下的 DRAFT_ONE_42 会被正常回填到 textarea 里（这是对的行为）。
       这里要证明的是「回退之后照样能打字、照样进草稿」。 */
    check('回退后照样能输入，且内容照样进草稿',
      (await value(page2)).endsWith('FALLBACK_OK')
      && await page2.evaluate(() => {
        for (let i = 0; i < localStorage.length; i++) {
          const k = localStorage.key(i);
          if (k.indexOf('pta.draft.') === 0 && localStorage.getItem(k).endsWith('FALLBACK_OK')) return true;
        }
        return false;
      }), JSON.stringify(await value(page2)));

    blockEditor = false;
    await page2.evaluate(id => { location.hash = '#/p/' + id; }, PY2.id);
    let recovered = false;
    try {
      await page2.waitForFunction(() => {
        const h = document.getElementById('codeEditor');
        return !!(h && !h.hidden && h.querySelector('.cm-content'));
      }, { timeout: 10000 });
      recovered = true;
    } catch (e) { /* 超时就是没恢复 */ }
    check('网络恢复后切一道题就能用上编辑器（失败不该被永久缓存）', recovered);
    await page2.close();

    /* ---------- [10] 没报错 ---------- */
    const errs = pageErrors.filter(e => !/favicon|404 \(Not Found\)|Failed to load resource/.test(e));
    check('全程没有 JS 异常', errs.length === 0, errs.slice(0, 3).join(' | '));
  } finally {
    await browser.close();
    srv.close();
  }

  console.log('\n' + '='.repeat(66));
  console.log('通过 ' + PASS + ' 项，失败 ' + FAIL.length + ' 项');
  if (FAIL.length) console.log('失败项：' + FAIL.join('、'));
  else console.log('全部通过 ✅');
  console.log('='.repeat(66));
  return FAIL.length ? 1 : 0;
}

async function focusEditorFallback(page) {
  await page.click('#codeBox');
}

run().then(c => process.exit(c)).catch(e => { console.error(e); process.exit(2); });
