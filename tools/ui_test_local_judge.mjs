/* ===================================================================
   离线本地判题 —— 专项测试（真 jsdom + 真加载 judge_text.js）

   为什么单独一个文件
   ----------------
   `ui_smoke.mjs` 用 jsdom 但不加载外链脚本（没有 resources:'usable'），
   所以它测不到 `judge_text.js`。而「离线也能判理论题」这件事的全部价值，
   恰恰在于**那个文件真的被加载、且判出来的结果与后端一致**。
   所以这里起一个真的静态服务器，让 `<script src="judge_text.js">` 真去取。

   它验的是「接线」，不是「口径」
   -----------------------------
   判题口径本身由 `tools/verify_text_judge.mjs` 负责（题库全部理论题 × 多种答案
   = 3463 条，与 Python 侧逐字段比对）。这里只管：
     · 脚本挂上了没有、按钮出不出来、答案取不取得到
     · 判完结果渲染对不对、进度写没写进 localStorage
     · ★ 答对之后再答错，最高分会不会被冲掉（这条是回归）
     · 导出 / 导入进度（含「导入低分备份不能冲掉高分」）
     · 在线时仍然走后端，不许被本地判题抢走

   用法（在仓库根目录下）：
     NODE_MODULES_DIR=C:/Users/Lijh node tools/ui_test_local_judge.mjs

   前置：docs/problems.json 必须是 `export_static.py --with-cases` 的产物。
   =================================================================== */
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { createRequire } from 'node:module';

function loadDep(name) {
  const tries = [createRequire(import.meta.url)];
  if (process.env.NODE_MODULES_DIR) {
    tries.push(createRequire(path.join(process.env.NODE_MODULES_DIR, 'noop.js')));
  }
  for (const req of tries) {
    try { return req(name); } catch (e) { /* 试下一个 */ }
  }
  console.error('找不到 ' + name + '。先装一个，并告诉我在哪：\n'
    + '  npm install ' + name + '\n'
    + '  NODE_MODULES_DIR=<含 node_modules 的目录> node tools/ui_test_local_judge.mjs');
  process.exit(3);
}
const { JSDOM, VirtualConsole } = loadDep('jsdom');

const CWD = process.cwd();
const HTML = fs.readFileSync(path.join(CWD, 'web', 'index.html'), 'utf8');
const BANK_PATH = path.join(CWD, 'docs', 'problems.json');
const BANK = JSON.parse(fs.readFileSync(BANK_PATH, 'utf8'));

if (!BANK.items || !BANK.items.length || !BANK.items[0].cases) {
  console.error('docs/problems.json 里没有 cases —— 本地判题需要完整测试点，先跑：\n'
    + '  python tools/export_static.py --with-cases');
  process.exit(4);
}
/* 反面对照：把 cases 剥掉，验证「题库没带测试点时不给本地判题按钮」 */
const BANK_NOCASES = Object.assign({}, BANK, {
  items: BANK.items.map(p => { const q = Object.assign({}, p); delete q.cases; return q; }),
});

let PASS = 0;
const FAIL = [];
const jsErrors = [];
function check(name, cond, extra) {
  if (cond) { PASS++; console.log('  [PASS] ' + name + (extra ? '  ' + extra : '')); }
  else { FAIL.push(name); console.log('  [FAIL] ' + name + (extra !== undefined ? '  ' + extra : '')); }
}
const sleep = ms => new Promise(r => setTimeout(r, ms));

/* ------------------------------------------------------------------ *
 * 一个只服务 web/ 的静态服务器 —— 目的就是让外链脚本真的被取到
 * ------------------------------------------------------------------ */
function serveWeb() {
  const ROOT = path.join(CWD, 'web');
  const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json',
                 '.css': 'text/css', '.svg': 'image/svg+xml' };
  const srv = http.createServer((req, res) => {
    const p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    const f = path.normalize(path.join(ROOT, p === '/' ? 'index.html' : p));
    if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) {
      res.statusCode = 404; return res.end('404');
    }
    res.setHeader('Content-Type', (MIME[path.extname(f)] || 'application/octet-stream') + '; charset=utf-8');
    res.end(fs.readFileSync(f));
  });
  return new Promise(r => srv.listen(0, '127.0.0.1', () => r(srv)));
}

/* ------------------------------------------------------------------ *
 * 假后端
 * ------------------------------------------------------------------ */
const NO_BACKEND = { ok: false, status: 404, json: async () => ({ detail: 'not found' }) };
const jsonOk = obj => ({ ok: true, status: 200, json: async () => obj });

function stubFetch(mode, bank) {
  return async (url) => {
    const u = String(url);
    if (u.endsWith('problems.json')) return jsonOk(bank);
    const p = new URL(u, 'http://localhost/').pathname;
    if (mode === 'offline') return NO_BACKEND;
    if (p === '/api/meta') return jsonOk({ langs: [], subjects: [], limits: {} });
    if (p === '/api/catalog') return jsonOk({ subjects: [], user_score: 0, user_max_score: 0 });
    if (p === '/api/problems') return jsonOk({ items: bank.items, total: bank.items.length });
    if (p.startsWith('/api/problems/')) {
      const it = bank.items.find(x => x.id === +p.split('/').pop());
      return it ? jsonOk(Object.assign({}, it, {
        mastery: {}, best_score: 0, solved: false, last_submission: null,
        history: [], history_count: 0, langs: [],
      })) : NO_BACKEND;
    }
    return NO_BACKEND;
  };
}

const JSDOM_NOISE = [
  "Not implemented: Window's scrollTo() method",
  "Not implemented: window.scrollTo",
];
const realErrors = list => list.filter(e => !JSDOM_NOISE.some(n => String(e).includes(n)));

async function newDom(mode, bank, port) {
  const errors = [];
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => errors.push(String((e && e.message) || e)));
  const dom = new JSDOM(HTML, {
    url: 'http://127.0.0.1:' + port + '/',
    runScripts: 'dangerously',
    resources: 'usable',          /* ★ 关键：这一行才让 judge_text.js 真的被加载 */
    pretendToBeVisual: true,
    virtualConsole: vc,
    beforeParse(win) {
      win.fetch = stubFetch(mode, bank);
      if (!win.crypto || !win.crypto.getRandomValues) {
        win.crypto = { getRandomValues(a) { for (let i = 0; i < a.length; i++) a[i] = (i * 37 + 11) & 255; return a; } };
      }
      /* 下载相关的 jsdom 没实现 —— 不是页面的问题，替身掉 */
      win.URL.createObjectURL = () => 'blob:stub';
      win.URL.revokeObjectURL = () => {};
      win.HTMLAnchorElement.prototype.click = function () {};
      win.addEventListener('error', e => errors.push('uncaught: ' + (e.message || e.error)));
    },
  });
  /* 等外链脚本就位 + boot 跑完（#app 不再是「正在加载」） */
  for (let i = 0; i < 80 && !dom.window.TextJudge; i++) await sleep(50);
  for (let i = 0; i < 80; i++) {
    await sleep(50);
    const app = dom.window.document.getElementById('app');
    if (app && !app.innerHTML.includes('正在加载')) break;
  }
  return { dom, errors };
}

async function goto(dom, hash) {
  dom.window.location.hash = hash;
  dom.window.dispatchEvent(new dom.window.Event('hashchange'));
  await sleep(140);
}

const txt = (doc, id) => { const e = doc.getElementById(id); return e ? e.textContent : ''; };
const readProg = win => { try { return JSON.parse(win.localStorage.getItem('pta.localProgress') || '{}'); } catch (e) { return {}; } };
const resetProg = win => { try { win.localStorage.removeItem('pta.localProgress'); } catch (e) {} };

/* 从题目的期望输出里取出一个「一定能判对」的答案 */
function goodAnswer(win, p) {
  const exp = (p.cases[0] || {}).expected_stdout || '';
  const alts = win.TextJudge.oneofAlternatives(exp);
  return alts.length ? alts[0] : exp.replace(/\s+$/, '');
}

/* ================================================================= */
async function run() {
  console.log('== 离线本地判题测试（真 jsdom + 真加载 judge_text.js）==');
  console.log('题库快照：' + BANK.count + ' 题 / ' + BANK.total_score + ' 分，'
    + '带测试点的理论题 '
    + BANK.items.filter(x => x.line === 'text' && x.cases).length + ' 道\n');

  const srv = await serveWeb();
  const PORT = srv.address().port;

  const fill = BANK.items.find(x => x.line === 'text' && (!x.choices || !x.choices.length));
  const mc = BANK.items.find(x => x.line === 'text' && x.choices && x.choices.length > 2);
  const tf = BANK.items.find(x => x.line === 'text' && x.choices && x.choices.length === 2 && x.choices.includes('对'));
  if (!fill || !mc || !tf) { console.error('题库里找不到三类理论题，测试无法进行'); process.exit(5); }

  /* ---------------- [1] 题库没带测试点 → 不给本地判题 ---------------- */
  console.log('[1] 题库未带测试点（对照）');
  {
    const { dom, errors } = await newDom('offline', BANK_NOCASES, PORT);
    const doc = dom.window.document;
    check('判题脚本已加载（外链真的取到了）', !!dom.window.TextJudge);
    check('canJudgeLocally 对没有 cases 的题返回 false',
      dom.window.TextJudge.canJudgeLocally(BANK_NOCASES.items.find(x => x.id === fill.id)) === false);
    await goto(dom, '#/p/' + fill.id);
    check('没有「提交并判题」按钮', !txt(doc, 'btnRow').includes('提交并判题'), txt(doc, 'btnRow').trim());
    check('退回手动标记', txt(doc, 'btnRow').includes('标记为已掌握'));
    const errs = realErrors(errors);
    check('[1] 全程没有 JS 异常', errs.length === 0, errs.slice(0, 2).join(' | '));
    if (errs.length) jsErrors.push(...errs);
    dom.window.close();
  }

  /* ---------------- [2] 填空题：判题 + 计分 + 进度 ---------------- */
  console.log('\n[2] 填空题（离线本地判题）');
  let dom, errors;
  {
    const r = await newDom('offline', BANK, PORT);
    dom = r.dom; errors = r.errors;
    const doc = dom.window.document;
    check('判题脚本已加载', !!dom.window.TextJudge);
    check('canJudgeLocally 对带 cases 的题返回 true',
      dom.window.TextJudge.canJudgeLocally(BANK.items.find(x => x.id === fill.id)) === true);

    await goto(dom, '#/p/' + fill.id);
    check('离线理论题出现「提交并判题」', txt(doc, 'btnRow').includes('提交并判题'), txt(doc, 'btnRow').trim());
    check('提示说明这是本地判题', txt(doc, 'btnRow').includes('本地判题'));

    const box = doc.getElementById('codeBox');
    check('填空题有输入框', !!box);

    /* --- 先交一个错的 --- */
    box.value = '这肯定不是正确答案_ZZZ';
    box.dispatchEvent(new dom.window.Event('input'));
    dom.window.doSubmitLocal();
    await sleep(80);
    check('错答案判 WA', txt(doc, 'resultBox').includes('答案错误'), txt(doc, 'resultBox').slice(0, 60));
    check('错答案得 0 分', txt(doc, 'resultBox').includes('0 / ' + fill.total_score),
      txt(doc, 'resultBox').slice(0, 80));
    check('进度里记了这次作答', (readProg(dom.window)[fill.id] || {}).attempts === 1,
      JSON.stringify(readProg(dom.window)[fill.id]));

    /* --- 再交正确的 --- */
    const good = goodAnswer(dom.window, fill);
    box.value = good;
    box.dispatchEvent(new dom.window.Event('input'));
    dom.window.doSubmitLocal();
    await sleep(80);
    check('正确答案判 AC', txt(doc, 'resultBox').includes('答案正确'), txt(doc, 'resultBox').slice(0, 60));
    check('AC 拿满分', txt(doc, 'resultBox').includes(fill.total_score + ' / ' + fill.total_score),
      txt(doc, 'resultBox').slice(0, 80));
    check('通过测试点 1 / 1', txt(doc, 'resultBox').includes('1 / 1'));
    check('展示每个测试点的详情', doc.querySelectorAll('.caseRow').length === fill.cases.length,
      String(doc.querySelectorAll('.caseRow').length));

    const lp = readProg(dom.window);
    check('进度写进 localStorage', (lp[fill.id] || {}).best_score === fill.total_score,
      JSON.stringify(lp[fill.id]));
    check('进度标了满分', (lp[fill.id] || {}).total_score === fill.total_score);
    check('顶栏总分跟着涨', txt(doc, 'navScore').includes(String(fill.total_score)),
      txt(doc, 'navScore').trim());
    check('题集广场不再显示离线横幅的「只能手动标记」（已可判题）',
      txt(doc, 'btnRow').includes('本地判题'));

    /* --- ★ 关键回归：答对之后再答错，最高分不能被冲掉 --- */
    box.value = '又是错的_QQQ';
    box.dispatchEvent(new dom.window.Event('input'));
    dom.window.doSubmitLocal();
    await sleep(120);
    const lp2 = readProg(dom.window);
    check('★ 答对后再答错，最高分没有被冲掉',
      (lp2[fill.id] || {}).best_score === fill.total_score, JSON.stringify(lp2[fill.id]));
    check('作答次数累加到 3', (lp2[fill.id] || {}).attempts === 3, String((lp2[fill.id] || {}).attempts));
    check('★ 顶栏总分也没掉', txt(doc, 'navScore').includes(String(fill.total_score)),
      txt(doc, 'navScore').trim());
  }

  /* ---------------- [3] 选择题 / 判断题 ---------------- */
  console.log('\n[3] 选择题与判断题');
  {
    const doc = dom.window.document;

    await goto(dom, '#/p/' + mc.id);
    const letter = dom.window.TextJudge.normalizeAnswer(goodAnswer(dom.window, mc));
    const idx = letter.charCodeAt(0) - 65;
    check('单选题参考答案确实是一个选项字母', /^[A-Z]$/.test(letter) && idx >= 0 && idx < mc.choices.length, letter);
    check('离线单选题也是「提交并判题」', txt(doc, 'btnRow').includes('提交并判题'));

    dom.window.pickChoice(doc.querySelectorAll('.choice')[(idx + 1) % mc.choices.length]);   /* 先点错的 */
    dom.window.doSubmitLocal();
    await sleep(80);
    check('单选题点错选项判 WA', txt(doc, 'resultBox').includes('答案错误'), txt(doc, 'resultBox').slice(0, 60));

    dom.window.pickChoice(doc.querySelectorAll('.choice')[idx]);
    dom.window.doSubmitLocal();
    await sleep(80);
    check('单选题点对选项判 AC', txt(doc, 'resultBox').includes('答案正确'), txt(doc, 'resultBox').slice(0, 60));
    check('单选题 AC 拿满分', txt(doc, 'resultBox').includes(mc.total_score + ' / ' + mc.total_score));

    await goto(dom, '#/p/' + tf.id);
    const tfAns = dom.window.TextJudge.normalizeAnswer(goodAnswer(dom.window, tf));
    check('判断题参考答案归一化后是「对」或「错」', tfAns === '对' || tfAns === '错', tfAns);
    const target = Array.prototype.find.call(doc.querySelectorAll('.choice'),
      c => c.getAttribute('data-v') === tfAns);
    check('判断题里能找到对应选项', !!target);
    if (target) {
      dom.window.pickChoice(target);
      dom.window.doSubmitLocal();
      await sleep(80);
      check('判断题选对判 AC', txt(doc, 'resultBox').includes('答案正确'), txt(doc, 'resultBox').slice(0, 60));
    }
  }

  /* ---------------- [4] 进度导出 / 导入 ---------------- */
  console.log('\n[4] 进度导出 / 导入');
  {
    const doc = dom.window.document;
    const b = dom.window.progressBundle();
    check('导出的包有 kind / version', b.kind === 'my-pta-progress' && b.version === 1);
    check('导出的包里有本地进度', Object.keys(b.local).length >= 1, Object.keys(b.local).length + ' 道题');
    check('导出的包里有合法通行证', /^[0-9a-f]{16,64}$/.test(b.token));

    let threw = null;
    try { dom.window.exportProgress(); } catch (e) { threw = String(e && e.message || e); }
    check('导出进度不抛异常（真的会下载一个 JSON）', threw === null, threw || '');

    /* 清空 → 导入 → 应该回来 */
    resetProg(dom.window);
    check('清空后本地进度为空', Object.keys(dom.window.localProgress()).length === 0);
    const f1 = new dom.window.File([JSON.stringify(b)], 'p.json', { type: 'application/json' });
    dom.window.importProgress({ target: { files: [f1], value: '' } });
    await sleep(250);
    check('导入后进度恢复（含满分）',
      (dom.window.localProgress()[fill.id] || {}).best_score === fill.total_score,
      JSON.stringify(dom.window.localProgress()[fill.id]));

    /* 导入一份更低的备份 → 不许冲掉高分 */
    const low = JSON.parse(JSON.stringify(b));
    low.local[fill.id].best_score = 0;
    const f2 = new dom.window.File([JSON.stringify(low)], 'p2.json', { type: 'application/json' });
    dom.window.importProgress({ target: { files: [f2], value: '' } });
    await sleep(250);
    check('★ 导入低分备份不会冲掉已有的高分',
      dom.window.localProgress()[fill.id].best_score === fill.total_score,
      JSON.stringify(dom.window.localProgress()[fill.id]));

    /* 垃圾文件 → 拒绝 */
    const f3 = new dom.window.File(['{"hello":1}'], 'x.json', { type: 'application/json' });
    dom.window.importProgress({ target: { files: [f3], value: '' } });
    await sleep(200);
    check('导入不相干的 JSON 被拒绝，进度不变',
      dom.window.localProgress()[fill.id].best_score === fill.total_score);
    check('拒绝时给了提示', txt(doc, 'toast').includes('不是本平台'), txt(doc, 'toast').slice(0, 40));

    const errs = realErrors(errors);
    check('[2][3][4] 全程没有 JS 异常', errs.length === 0, errs.slice(0, 3).join(' | '));
    if (errs.length) jsErrors.push(...errs);
    dom.window.close();
  }

  /* ---------------- [5] 在线时仍然走后端 ---------------- */
  console.log('\n[5] 在线时不被本地判题抢走');
  {
    const { dom: d2, errors: e2 } = await newDom('online', BANK, PORT);
    const doc = d2.window.document;
    await goto(d2, '#/p/' + fill.id);
    const row = txt(doc, 'btnRow');
    check('在线时按钮是「提交评测」', row.includes('提交评测'), row.trim());
    check('在线时不出现「提交并判题」', !row.includes('提交并判题'), row.trim());
    const errs = realErrors(e2);
    check('[5] 全程没有 JS 异常', errs.length === 0, errs.slice(0, 2).join(' | '));
    if (errs.length) jsErrors.push(...errs);
    d2.window.close();
  }

  srv.close();

  console.log('\n' + '='.repeat(66));
  console.log('通过 ' + PASS + ' 项，失败 ' + FAIL.length + ' 项');
  if (FAIL.length) console.log('失败项：' + FAIL.join('、'));
  else console.log('全部通过 ✅');
  console.log('='.repeat(66));
  return FAIL.length ? 1 : 0;
}

run().then(c => process.exit(c)).catch(e => { console.error(e); process.exit(2); });
