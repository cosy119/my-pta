/* 真浏览器检查「按难易程度排序」改造是否真的生效。
 *
 * 验证四件事：
 *   1. 分组顺序 = 教学路径序号（不是拼音、不是讲次号）
 *   2. 组内题目难度升序
 *   3. 题号（CP-/PY-/DS-/LX-）随新顺序重编，且严格递增
 *   4. 分组标题带「均难」标签
 *
 * 两种模式都跑：
 *   PTA_API_PORT 设了 → 在线（静态前端 + /api 反代到 uvicorn，= 真实部署形态）
 *   不设             → 离线（纯静态站，读 problems.json 的 section_ranks）
 *
 * PTA_SITE_DIR 可指向临时静态导出；默认检查仓库 docs/。
 */
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { createRequire } from 'node:module';

const repo = process.cwd();
const root = path.resolve(process.env.PTA_SITE_DIR || path.join(repo, 'docs'));
const moduleDir = process.env.NODE_MODULES_DIR || path.join(repo, 'experiments/pyodide-judge/node_modules');
const require = createRequire(path.join(moduleDir, 'noop.js'));
const puppeteer = require('puppeteer-core');
const API_PORT = process.env.PTA_API_PORT ? parseInt(process.env.PTA_API_PORT, 10) : 0;

const bank = JSON.parse(fs.readFileSync(path.join(root, 'problems.json'), 'utf8'));
const items = bank.items || [];
const ranks = bank.section_ranks || {};
if (!items.length) throw Error('静态题库是空的');
if (!Object.keys(ranks).length) throw Error('静态题库缺少 section_ranks（分节教学路径序号）');

const MIME = { '.html':'text/html; charset=utf-8', '.js':'text/javascript; charset=utf-8',
  '.json':'application/json; charset=utf-8', '.css':'text/css; charset=utf-8',
  '.wasm':'application/wasm', '.txt':'text/plain; charset=utf-8', '.mjs':'text/javascript; charset=utf-8' };

/* 静态站；在线模式额外把 /api/ 反代到 uvicorn —— 真实部署就是这套 */
const server = http.createServer((req, res) => {
  const pathname = decodeURIComponent(req.url.split('?')[0]);
  if (API_PORT && pathname.startsWith('/api/')) {
    const up = http.request({
      host: '127.0.0.1', port: API_PORT, path: req.url, method: req.method, headers: req.headers,
    }, ur => { res.writeHead(ur.statusCode || 502, ur.headers); ur.pipe(res); });
    up.on('error', () => { res.writeHead(502); res.end('bad gateway'); });
    req.pipe(up);
    return;
  }
  const file = path.resolve(root, '.' + (pathname === '/' ? '/index.html' : pathname));
  if (!file.startsWith(root + path.sep)) { res.writeHead(403).end(); return; }
  fs.readFile(file, (err, data) => {
    if (err) { res.writeHead(404).end(); return; }
    const ext = path.extname(file);
    res.setHeader('Content-Type', MIME[ext.toLowerCase()] || 'application/octet-stream');
    res.end(data);
  });
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const base = `http://127.0.0.1:${server.address().port}/`;
const browser = await puppeteer.launch({
  executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: true, args: ['--no-sandbox']
});
const page = await browser.newPage();
const errors = [];
page.on('pageerror', e => errors.push(String(e)));
const check = (name, ok, extra) => {
  if (!ok) throw Error(name + (extra ? ' — ' + extra : ''));
  console.log('PASS ' + name);
};
const mode = API_PORT ? ('在线（反代 :' + API_PORT + '）') : '离线（纯静态）';
console.log('模式：' + mode + '\n');

try {
  await page.goto(base + '#/set/cpp');
  await page.waitForSelector('.grpbox');

  /* 序号表来源：在线是 /api/meta，离线是 problems.json ——
     但前端最终都会写进 SECTION_RANKS，直接读它才是真正在验「前端拿到的那份」 */
  const liveRanks = await page.evaluate(() => SECTION_RANKS);
  if (API_PORT) {
    check('在线模式走了 /api/meta 的 section_ranks',
      Object.keys(liveRanks || {}).length === 4,
      JSON.stringify(Object.keys(liveRanks || {})));
  } else {
    check('离线模式走了 problems.json 的 section_ranks',
      Object.keys(liveRanks || {}).length === 4,
      JSON.stringify(Object.keys(liveRanks || {})));
  }

  /* ---- 1. 分组顺序 = 教学路径序号 ---- */
  const groupNames = await page.$$eval('.grpbox', gs => gs.map(g => g.dataset.g));
  const cppRanks = liveRanks.cpp || {};
  const gotRanks = groupNames.map(n => cppRanks[n]);
  const missing = groupNames.filter(n => cppRanks[n] === undefined);
  check('所有 C++ 分组都在序号表里', missing.length === 0, missing.join(','));
  const sorted = gotRanks.slice().sort((a, b) => a - b);
  check('分组按教学路径序号递增',
    JSON.stringify(gotRanks) === JSON.stringify(sorted),
    groupNames.map((n, i) => n + '=' + gotRanks[i]).join(' '));

  /* 关键回归：C++ 编程册的 17 节必须挨在讲次之后、技巧特训之前 */
  const progIdx = groupNames.findIndex(n => n.startsWith('C++ 编程 · '));
  const trickIdx = groupNames.findIndex(n => n.includes('技巧特训'));
  const lastLectureIdx = groupNames.map(n => n.startsWith('第 ')).lastIndexOf(true);
  check('编程册排在 12 个讲次之后', progIdx > lastLectureIdx,
    '讲次最后=' + lastLectureIdx + ' 编程册=' + progIdx);
  check('技巧特训排在编程册之后', trickIdx > progIdx,
    '编程册=' + progIdx + ' 技巧特训=' + trickIdx);

  /* 编程册内部要按编排册序（输入输出 → … → 动态规划 → 综合模拟） */
  const progOrder = groupNames.filter(n => n.startsWith('C++ 编程 · '))
    .map(n => cppRanks[n]);
  check('编程册内部按册序递增',
    JSON.stringify(progOrder) === JSON.stringify(progOrder.slice().sort((a, b) => a - b)),
    progOrder.join(','));

  /* ---- 2. 组内难度升序 ---- */
  const diffSeq = await page.$$eval('.grpbox', gs => gs.map(g => ({
    name: g.dataset.g,
    diffs: [...g.querySelectorAll('tbody tr .c-df')].map(td => {
      const on = td.querySelectorAll('.stars:not(.off)').length;
      return on;
    })
  })));
  const notMono = diffSeq.filter(g => g.diffs.some((d, i) => i > 0 && g.diffs[i - 1] > d));
  check('每组内部难度升序', notMono.length === 0,
    notMono.map(g => g.name + ':' + g.diffs.join(',')).join(' | '));

  /* ---- 3. 题号随新顺序重编且递增 ---- */
  const nos = await page.$$eval('.grpbox', gs => gs.flatMap(g =>
    [...g.querySelectorAll('tbody tr .c-no')].map(td => td.textContent.trim())));
  check('题号全部为 CP- 前缀', nos.length > 0 && nos.every(n => /^CP-\d+$/.test(n)),
    nos.slice(0, 3).join(','));
  const nums = nos.map(n => parseInt(n.split('-')[1], 10));
  check('题号严格递增', nums.every((v, i) => i === 0 || v > nums[i - 1]),
    nums.slice(0, 5).join(',') + '…');

  /* ---- 4. 分组标题带均难标签 ---- */
  const avgs = await page.$$eval('.grpbox .grpHead .pill', ps =>
    ps.map(p => p.textContent.trim()).filter(t => t.startsWith('均难')));
  check('分组标题带「均难」标签', avgs.length === groupNames.length,
    avgs.length + '/' + groupNames.length);

  /* ---- 5. 其它三条线也要正常 ---- */
  for (const [subj, prefix] of [['python', 'PY'], ['ds', 'DS'], ['linux', 'LX']]) {
    await page.goto(base + '#/set/' + subj);
    await page.waitForSelector('.grpbox');
    const names = await page.$$eval('.grpbox', gs => gs.map(g => g.dataset.g));
    const rs = (liveRanks[subj] || {});
    const rr = names.map(n => rs[n]);
    check(subj + ' 线分组按序号递增',
      rr.every(v => v !== undefined) && JSON.stringify(rr) === JSON.stringify(rr.slice().sort((a, b) => a - b)),
      names.map((n, i) => n + '=' + rr[i]).join(' '));
    const n2 = await page.$$eval('.grpbox .c-no', tds => tds.map(t => t.textContent.trim()));
    check(subj + ' 线题号前缀 ' + prefix, n2.every(n => n.startsWith(prefix + '-')),
      n2.slice(0, 2).join(','));
  }

  /* ---- 6. 题型下拉按难度顺序（判断 → 单选 → 多选 → 填空 → 简答 → 实操 → 编程）----
     ★ 必须按 id 精确取：工具栏里现在有两个 .typeSelect（题型 + 排序方式），
       用 class 取会把排序方式的选项也捞进来，断言就假失败。 */
  await page.goto(base + '#/set/cpp');
  await page.waitForSelector('#typeSelect');
  const typeOpts = await page.$$eval('#typeSelect option', os =>
    os.map(o => o.textContent.replace(/（.*$/, '')).filter(t => t && t !== '全部题型'));
  const expectTypes = ['判断题', '单选题', '多选题', '填空题', '简答题', '实操题', '编程题'];
  check('题型下拉按作答难度排序',
    JSON.stringify(typeOpts) === JSON.stringify(expectTypes),
    typeOpts.join(' '));

  check('页面无 JS 报错', errors.length === 0, errors.join(' | '));
  console.log('\n✅ 排序改造全部通过（' + mode + '）');
} finally {
  await browser.close();
  server.close();
}
