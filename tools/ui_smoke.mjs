/* 前端冒烟测试：用 jsdom 真把 web/index.html 跑起来，看它能不能渲染、会不会抛错。
 *
 * 为什么需要
 * ----------
 * `node --check` 只能证明「语法没错」。49KB 的前端逻辑里真正的风险是
 * **运行期** 的问题：某道题的字段是空的、某个分组名带引号、离线分支没走到……
 * 这些只有真的执行一遍渲染函数才会暴露。
 *
 * 跑两遍：
 *   1. 离线模式（后端 404）→ 走 problems.json + localStorage 那条路
 *   2. 假后端模式（把 docs/problems.json 伪装成 /api/* 的返回）→ 走在线那条路
 *
 * 用法（在仓库根目录下）：
 *   NODE_PATH=<node workspace>/node_modules node tools/ui_smoke.mjs
 */
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

/* jsdom 不是本仓库的依赖（只有这个冒烟测试用）—— 优先按常规解析，
   找不到就去环境变量 NODE_MODULES_DIR 指的 node_modules 里找。
   ESM 的 import 不认 NODE_PATH，所以必须走 createRequire。 */
function loadJsdom() {
  const tries = [createRequire(import.meta.url)];
  if (process.env.NODE_MODULES_DIR) {
    tries.push(createRequire(path.join(process.env.NODE_MODULES_DIR, 'noop.js')));
  }
  for (const req of tries) {
    try { return req('jsdom'); } catch (e) { /* 试下一个 */ }
  }
  console.error('找不到 jsdom。先装一个，并告诉我在哪：\n'
    + '  npm install jsdom\n'
    + '  NODE_MODULES_DIR=<含 node_modules 的目录> node tools/ui_smoke.mjs');
  process.exit(3);
}
const { JSDOM, VirtualConsole } = loadJsdom();

const CWD = process.cwd();
const HTML = fs.readFileSync(path.join(CWD, 'web', 'index.html'), 'utf8');
const BANK = JSON.parse(fs.readFileSync(path.join(CWD, 'docs', 'problems.json'), 'utf8'));
const BANK_SCORE = BANK.items.reduce((sum, p) => sum + Number(p.total_score || 0), 0);
const subjectItems = key => BANK.items.filter(p => p.subject === key);
const subjectGroups = key => new Set(subjectItems(key).map(p => p.source_section || '未分组')).size;

let PASS = 0;
const FAIL = [];
const jsErrors = [];

function check(name, cond, extra) {
  if (cond) { PASS++; console.log('  [PASS] ' + name + (extra ? '  ' + extra : '')); }
  else { FAIL.push(name); console.log('  [FAIL] ' + name + (extra ? '  ' + extra : '')); }
}

/* ---------------- 把 problems.json 伪装成后端接口的返回 ---------------- */
const LABELS = { python: 'Python 快乐编程基础入门', ds: '数据结构（C 语言版）', linux: 'Linux 系统应用与开发' };

function langsFor(line) {
  if (line === 'python') return [{ lang: 'python', label: 'Python', hint: '解释执行',
    interpreters: [{ key: 'py313', label: 'Python 3.13.14' }, { key: 'py314', label: 'Python 3.14.4' }] }];
  if (line === 'cpp') return [
    { lang: 'cpp', label: 'C++ (g++)', hint: '-std=c++17', interpreters: [] },
    { lang: 'c', label: 'C (gcc)', hint: '-std=gnu11', interpreters: [] }];
  if (line === 'c') return [{ lang: 'c', label: 'C (gcc)', hint: '-std=gnu11', interpreters: [] }];
  return [];
}
function row(it) {
  return Object.assign({}, it, {
    best_score: 0, attempts: 0, ac_count: 0, level: 0, is_starred: 0, last_verdict: '',
    solved_at: '', solved: false, score_label: '0/' + it.total_score,
    is_choice: !!(it.choices && it.choices.length),
    langs: langsFor(it.line),
  });
}
function detail(it) {
  return Object.assign(row(it), {
    subject_label: LABELS[it.subject] || it.subject,
    case_points: it.case_points || [], points_sum: it.points_sum || 0,
    hidden_count: it.hidden_count || 0,
    mastery: {}, best_score: 0, solved: false, last_submission: null,
    history: [], history_count: 0,
  });
}
function buildCatalog() {
  const subs = {};
  BANK.items.forEach(it => {
    const k = it.subject || 'python';
    const s = subs[k] || (subs[k] = { key: k, label: LABELS[k] || k, total: 0, solved: 0,
      attempted: 0, score: 0, max_score: 0, difficulty: {}, lines: {}, sections: {} });
    s.total++; s.max_score += it.total_score;
    const sec = it.source_section || '未分组';
    const g = s.sections[sec] || (s.sections[sec] = { name: sec, total: 0, solved: 0, score: 0, max_score: 0 });
    g.total++; g.max_score += it.total_score;
  });
  const ORDER = { python: 0, ds: 1, linux: 2 };
  const list = Object.keys(subs).map(k => {
    const s = subs[k];
    s.sections = Object.values(s.sections).sort((a, b) => {
      const la = (a.name.match(/第\s*(\d+)\s*讲/) || [0, 0])[1];
      const lb = (b.name.match(/第\s*(\d+)\s*讲/) || [0, 0])[1];
      return (+la - +lb) || a.name.localeCompare(b.name, 'zh');
    });
    return s;
  }).sort((a, b) => ORDER[a.key] - ORDER[b.key]);
  return { subjects: list, user_score: 0, max_score: 0, user_max_score: BANK_SCORE };
}

const NO_BACKEND = { ok: false, status: 404, json: async () => ({ detail: 'not found' }) };
const jsonOk = obj => ({ ok: true, status: 200, json: async () => obj });

function stubFetch(mode) {
  return async (url) => {
    const u = String(url);
    if (u.endsWith('problems.json')) return jsonOk(BANK);
    const p = new URL(u, 'http://localhost/').pathname;
    if (mode === 'offline') return NO_BACKEND;
    if (p === '/api/meta') return jsonOk({ langs: [], subjects: [], limits: {} });
    if (p === '/api/catalog') return jsonOk(buildCatalog());
    if (p === '/api/problems') return jsonOk({ items: BANK.items.map(row), total: BANK.items.length });
    if (p.startsWith('/api/problems/')) {
      const id = +p.split('/').pop();
      const it = BANK.items.find(x => x.id === id);
      return it ? jsonOk(detail(it)) : NO_BACKEND;
    }
    if (p === '/api/submissions') return jsonOk({ items: [] });
    if (p === '/api/me') return jsonOk({ id: 1, nickname: '', score: 0, max_score: BANK_SCORE });
    return NO_BACKEND;
  };
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

/* jsdom 自己没实现的东西（不是页面的问题）—— 从错误里滤掉，别让噪声淹没真问题 */
const JSDOM_NOISE = [
  "Not implemented: Window's scrollTo() method",
  "Not implemented: window.scrollTo",
];
const realErrors = list => list.filter(e => !JSDOM_NOISE.some(n => String(e).includes(n)));

async function newDom(mode) {
  const errors = [];
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => errors.push(String(e && e.message || e)));
  const dom = new JSDOM(HTML, {
    url: 'http://localhost:8799/',
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    virtualConsole: vc,
    beforeParse(win) {
      win.fetch = stubFetch(mode);
      if (!win.crypto || !win.crypto.getRandomValues) {
        win.crypto = { getRandomValues(a) { for (let i = 0; i < a.length; i++) a[i] = (i * 37 + 11) & 255; return a; } };
      }
      win.addEventListener('error', e => errors.push('uncaught: ' + (e.message || e.error)));
    },
  });
  // 等启动完成（#app 里不再是「正在加载」）
  for (let i = 0; i < 60; i++) {
    await sleep(50);
    const app = dom.window.document.getElementById('app');
    if (app && !app.innerHTML.includes('正在加载')) break;
  }
  return { dom, errors };
}

async function goto(dom, hash) {
  dom.window.location.hash = hash;
  await sleep(120);
}

/* ================================================================= */
async function run() {
  console.log('== 前端冒烟测试（jsdom 真渲染）==');
  console.log('题库快照：' + BANK.count + ' 题 / ' + BANK.total_score + ' 分\n');

  /* ---------------- 第一遍：离线模式 ---------------- */
  console.log('[1] 离线模式（后端不可用）');
  {
    const { dom, errors } = await newDom('offline');
    const doc = dom.window.document;
    const app = doc.getElementById('app');
    check('离线时显示「离线浏览」提示条', !!doc.querySelector('.banner.warn'));
    check('离线时右上角有「离线浏览」角标',
      doc.getElementById('offlineTag').style.display !== 'none');
    check('题集广场渲染出 3 张科目卡片', doc.querySelectorAll('.card').length === 3,
      String(doc.querySelectorAll('.card').length));
    check('卡片里有进度条', doc.querySelectorAll('.card .bar').length >= 3);
    check('hero 里显示了总分', app.textContent.includes(String(BANK_SCORE)));

    await goto(dom, '#/set/ds');
    const grps = app.querySelectorAll('.grpbox');
    check('数据结构题集分组齐全', grps.length === subjectGroups('ds'), String(grps.length));
    const rows = app.querySelectorAll('table.ptable tbody tr');
    check('题集内表格题数正确', rows.length === subjectItems('ds').length, String(rows.length));
    check('状态列渲染了圆点', app.querySelectorAll('td.c-st .st').length === rows.length);
    check('难度列渲染了星星', app.querySelectorAll('td.c-df .stars').length === rows.length);
    check('类型列渲染了标签', app.querySelectorAll('td.c-ty .tyTag').length === rows.length);

    // 折叠
    dom.window.toggleGroup(0);
    await sleep(60);
    check('点分组标题能折叠', app.querySelectorAll('.grpbox.closed').length === 1,
      String(app.querySelectorAll('.grpbox.closed').length));
    // 「展开 / 折叠」是**整体翻转**：只要还有开着的就全关，全关了再点就全开
    dom.window.toggleAllGroups();
    await sleep(60);
    check('「展开 / 折叠」：还有开着的 → 全部收起',
      app.querySelectorAll('.grpbox.closed').length === 4,
      String(app.querySelectorAll('.grpbox.closed').length));
    dom.window.toggleAllGroups();
    await sleep(60);
    check('再点一次 → 全部展开（第一次点不是空操作）',
      app.querySelectorAll('.grpbox.closed').length === 0,
      String(app.querySelectorAll('.grpbox.closed').length));

    // 筛选
    dom.window.setFilter('solved');
    await sleep(60);
    check('筛选「已解决」在离线且未标记时是空列表',
      app.querySelectorAll('.empty').length === 1);

    // 数据结构编程题
    await goto(dom, '#/p/57');
    check('题目页渲染出标题', !!app.querySelector('.ptitle'), (app.querySelector('.ptitle') || {}).textContent);
    check('编程题给了 C / C++ 语言下拉',
      !!doc.getElementById('langSel') && doc.querySelectorAll('#langSel option').length === 2,
      String(doc.querySelectorAll('#langSel option').length));
    check('代码编辑器在', !!doc.getElementById('codeBox'));
    check('样例渲染出来了', app.querySelectorAll('.sample').length === 2,
      String(app.querySelectorAll('.sample').length));
    check('离线时提交按钮换成「标记为已掌握」', !!app.textContent.match(/标记为已掌握/));
    check('题目页显示所属科目', app.textContent.includes('数据结构'));
    dom.window.markSolved(15);
    await sleep(80);
    check('手动标记后进度条不再是 0', dom.window.document.getElementById('navScore').textContent.includes('15'),
      doc.getElementById('navScore').textContent.trim());

    // 理论题：单选题
    const mc = BANK.items.find(x => x.line === 'text' && x.choices && x.choices.length > 2);
    await goto(dom, '#/p/' + mc.id);
    check('单选题渲染成可点选项', app.querySelectorAll('.choice').length === mc.choices.length,
      String(app.querySelectorAll('.choice').length));
    check('单选题没有代码编辑器', !doc.getElementById('codeBox'));
    dom.window.pickChoice(app.querySelectorAll('.choice')[1]);
    await sleep(40);
    check('点一下能选中选项', app.querySelectorAll('.choice.on').length === 1);
    dom.window.doSubmit();
    await sleep(120);
    check('离线时提交被拦住并给了提示', app.textContent.includes('离线模式') || app.textContent.includes('手动标记'));

    // 理论题：判断题
    const tf = BANK.items.find(x => x.line === 'text' && x.choices && x.choices.length === 2
      && x.choices.includes('对'));
    await goto(dom, '#/p/' + tf.id);
    check('判断题渲染两个选项', app.querySelectorAll('.choice').length === 2,
      String(app.querySelectorAll('.choice').length));

    // 理论题：填空题（无选项）
    const fill = BANK.items.find(x => x.line === 'text' && (!x.choices || !x.choices.length));
    await goto(dom, '#/p/' + fill.id);
    check('填空题给出输入框（且没有语言下拉）',
      !!doc.getElementById('codeBox') && !doc.getElementById('langSel'));

    // markdown 折叠提示
    dom.window.location.hash = '#/p/' + BANK.items[0].id;
    await sleep(120);
    const hasCal = BANK.items.some(x => (x.statement_md || '').includes('[!warning]'));
    if (hasCal) {
      const w = BANK.items.find(x => (x.statement_md || '').includes('[!warning]'));
      await goto(dom, '#/p/' + w.id);
      check('题面里的 [!warning] 渲染成提示块', !!app.querySelector('blockquote.cal-warning'));
    }

    // 我的提交
    await goto(dom, '#/subs');
    check('离线时「我的提交」不崩且给了说明', !!app.querySelector('.empty') || !!app.querySelector('.ptable'));

    const errs = realErrors(errors);
    check('离线模式全程没有 JS 异常', errs.length === 0, errs.slice(0, 3).join(' | '));
    if (errs.length) jsErrors.push(...errs);
    dom.window.close();
  }

  /* ---------------- 第二遍：假后端模式 ---------------- */
  console.log('\n[2] 在线模式（后端返回正常数据）');
  {
    const { dom, errors } = await newDom('online');
    const doc = dom.window.document;
    const app = doc.getElementById('app');
    check('在线时没有「离线浏览」提示条', !doc.querySelector('.banner.warn'));
    check('在线时角标隐藏', doc.getElementById('offlineTag').style.display === 'none');
    check('导航栏显示了总分 / 满分', doc.getElementById('navScore').textContent.includes(String(BANK_SCORE)),
      doc.getElementById('navScore').textContent.trim());
    check('在线时题集广场也是 3 张卡片', doc.querySelectorAll('.card').length === 3,
      String(doc.querySelectorAll('.card').length));
    check('三种科目的卡片名都对得上',
      ['Python', '数据结构', 'Linux'].every(k => app.textContent.includes(k)));

    await goto(dom, '#/set/linux');
    const rows = app.querySelectorAll('table.ptable tbody tr');
    check('Linux 题集题数正确', rows.length === subjectItems('linux').length, String(rows.length));
    check('Linux 题集分组齐全', app.querySelectorAll('.grpbox').length === subjectGroups('linux'),
      String(app.querySelectorAll('.grpbox').length));

    // 搜索
    dom.window.onQuery('tar');
    await sleep(320);
    const n = app.querySelectorAll('table.ptable tbody tr').length;
    check('搜索能把题目筛出来', n > 0 && n < subjectItems('linux').length, n + ' 行');
    dom.window.onQuery('');
    await sleep(320);

    // 单选提交：交给后端
    const mc = BANK.items.find(x => x.line === 'text' && x.choices && x.choices.length > 2);
    await goto(dom, '#/p/' + mc.id);
    dom.window.pickChoice(app.querySelectorAll('.choice')[2]);
    await sleep(40);
    dom.window.doSubmit();
    await sleep(200);
    check('在线时提交走的是真实接口（界面有反应）',
      app.textContent.includes('提交') || app.textContent.includes('评测'));

    await goto(dom, '#/subs');
    check('「我的提交」页面渲染出表格或空态',
      !!app.querySelector('.ptable') || !!app.querySelector('.empty'));

    const errs = realErrors(errors);
    check('在线模式全程没有 JS 异常', errs.length === 0, errs.slice(0, 3).join(' | '));
    if (errs.length) jsErrors.push(...errs);
    dom.window.close();
  }

  console.log('\n' + '='.repeat(66));
  console.log('通过 ' + PASS + ' 项，失败 ' + FAIL.length + ' 项');
  if (FAIL.length) console.log('失败项：' + FAIL.join('、'));
  else console.log('全部通过 ✅');
  console.log('='.repeat(66));
  return FAIL.length ? 1 : 0;
}

run().then(c => process.exit(c)).catch(e => { console.error(e); process.exit(2); });
