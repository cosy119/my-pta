/* 真浏览器检查「按章节 / 按难度」排序切换是否真的生效。
 *
 * 验证：
 *   1. 默认是「按章节」，分组显示，分组数 > 1
 *   2. 切「难度 易→难」：只剩一个分组、组内难度不减、组名标了方向
 *   3. 切「难度 难→易」：组内难度不增
 *   4. 难度模式下分组名是「全部题目 · 难度 …」而不是某个章节名
 *   5. ★ 题号（CP-01 等）在三种模式下**完全不变** —— 它是稳定标识，
 *      换了排序就跳号的话，收藏/记录/分享链接全对不上
 *   6. 切回「按章节」：恢复多分组，且顺序与初始状态一致
 *   7. 刷新页面后排序方式被记住（localStorage）
 *   8. 页面无 JS 报错
 *
 * 两种模式都跑：
 *   PTA_API_PORT 设了 → 在线（静态前端 + /api 反代到 uvicorn）
 *   不设             → 离线（纯静态站）
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

const MIME = { '.html':'text/html; charset=utf-8', '.js':'text/javascript; charset=utf-8',
  '.json':'application/json; charset=utf-8', '.css':'text/css; charset=utf-8',
  '.wasm':'application/wasm', '.txt':'text/plain; charset=utf-8', '.mjs':'text/javascript; charset=utf-8' };

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
    res.setHeader('Content-Type', MIME[path.extname(file).toLowerCase()] || 'application/octet-stream');
    res.end(data);
  });
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const base = `http://127.0.0.1:${server.address().port}/`;

const browser = await puppeteer.launch({
  executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: true, args: ['--no-sandbox'],
});
const page = await browser.newPage();
const errors = [];
page.on('pageerror', e => errors.push(String(e)));

let passed = 0;
const check = (name, ok, extra) => {
  if (!ok) throw Error(name + (extra ? ' — ' + extra : ''));
  passed++;
  console.log('PASS ' + name);
};

/* 读当前列表状态：分组名、每组题号、每组难度（★ 是实心星的数量） */
async function snapshot() {
  return page.evaluate(() => [...document.querySelectorAll('.grpbox')].map(b => ({
    name: b.dataset.g,
    codes: [...b.querySelectorAll('tbody tr td.c-no')].map(t => t.textContent.trim()),
    diffs: [...b.querySelectorAll('tbody tr td.c-df')].map(td =>
      [...td.querySelectorAll('.stars > *')].filter(e => !e.classList.contains('off')).length),
  })));
}
const isSorted = (a, dir) => a.every((v, i) => i === 0 || (dir === 'asc' ? v >= a[i - 1] : v <= a[i - 1]));

async function selectSort(value) {
  await page.select('#sortSelect', value);
  await new Promise(r => setTimeout(r, 350));
}

const mode = API_PORT ? ('在线（反代 :' + API_PORT + '）') : '离线（纯静态）';
console.log('模式：' + mode + '\n');

try {
  await page.goto(base + '#/set/cpp');
  await page.waitForSelector('.grpbox');
  /* 从干净状态开始：本地可能存着上次选的排序方式 */
  await page.evaluate(() => { try { localStorage.removeItem('pta.sortMode'); } catch (e) {} });
  await page.reload();
  await page.waitForSelector('.grpbox');

  /* ---- 1. 默认按章节 ---- */
  const sel0 = await page.$eval('#sortSelect', s => s.value);
  check('默认排序方式是 chapter', sel0 === 'chapter', sel0);
  const optLabels = await page.$$eval('#sortSelect option', os => os.map(o => o.textContent.trim()));
  check('排序下拉有三个选项', optLabels.length === 3, optLabels.join(' | '));
  check('排序选项文案：按章节 / 难度 易→难 / 难度 难→易',
    JSON.stringify(optLabels) === JSON.stringify(['按章节', '难度 易→难', '难度 难→易']),
    optLabels.join(' | '));

  const chapter = await snapshot();
  check('按章节时分多个组', chapter.length > 1, chapter.length + ' 组');
  check('按章节时组内难度升序',
    chapter.every(g => isSorted(g.diffs, 'asc')),
    chapter.filter(g => !isSorted(g.diffs, 'asc')).map(g => g.name).slice(0, 3).join(','));
  const chapterOrder = chapter.map(g => g.name).join(' | ');
  const chapterCodes = chapter.flatMap(g => g.codes);

  /* ---- 2. 难度 易→难 ---- */
  await selectSort('difficulty');
  const up = await snapshot();
  check('难度 易→难：只剩一个分组', up.length === 1, up.length + ' 组');
  check('难度 易→难：组名标了方向', /难度\s*易→难/.test(up[0].name), up[0].name);
  check('难度 易→难：组内难度不减', isSorted(up[0].diffs, 'asc'),
    '前 10 个：' + up[0].diffs.slice(0, 10).join(','));
  check('难度 易→难：题数不变', up[0].codes.length === chapterCodes.length,
    up[0].codes.length + ' vs ' + chapterCodes.length);
  check('难度 易→难：题号集合与按章节完全一致（不丢不重）',
    JSON.stringify(up[0].codes.slice().sort()) === JSON.stringify(chapterCodes.slice().sort()));

  /* ---- 3. 难度 难→易 ---- */
  await selectSort('difficulty_desc');
  const dn = await snapshot();
  check('难度 难→易：只剩一个分组', dn.length === 1, dn.length + ' 组');
  check('难度 难→易：组名标了方向', /难度\s*难→易/.test(dn[0].name), dn[0].name);
  check('难度 难→易：组内难度不增', isSorted(dn[0].diffs, 'desc'),
    '前 10 个：' + dn[0].diffs.slice(0, 10).join(','));
  check('难度 难→易：题号集合与按章节完全一致',
    JSON.stringify(dn[0].codes.slice().sort()) === JSON.stringify(chapterCodes.slice().sort()));
  /* ★ 别断言「整表互为倒序」：同难度段内两种模式都按章节序**升序**兜底
     （这样同一难度的题在两种视图里次序一致），所以整表不是严格镜像，
     镜像的只是**难度序列**。 */
  check('易→难 与 难→易 的难度序列互为镜像',
    JSON.stringify(up[0].diffs.slice().reverse()) === JSON.stringify(dn[0].diffs),
    up[0].diffs.slice(0, 8).join(',') + ' ↔ ' + dn[0].diffs.slice(0, 8).join(','));

  /* ---- 4. ★ 题号是稳定标识：同一道题在任何排序下题号都一样 ---- */
  const codeById = await page.evaluate(() => {
    const map = {};
    document.querySelectorAll('.grpbox tbody tr').forEach(tr => {
      const a = tr.querySelector('td.c-tt a');
      const no = tr.querySelector('td.c-no');
      if (a && no) map[a.getAttribute('href')] = no.textContent.trim();
    });
    return map;
  });
  await selectSort('chapter');
  const codeById2 = await page.evaluate(() => {
    const map = {};
    document.querySelectorAll('.grpbox tbody tr').forEach(tr => {
      const a = tr.querySelector('td.c-tt a');
      const no = tr.querySelector('td.c-no');
      if (a && no) map[a.getAttribute('href')] = no.textContent.trim();
    });
    return map;
  });
  const drift = Object.keys(codeById).filter(k => codeById[k] !== codeById2[k]);
  check('题号不随排序方式变化（同一题题号恒定）', drift.length === 0,
    drift.slice(0, 3).map(k => k + ' ' + codeById[k] + '→' + codeById2[k]).join(','));

  /* ---- 5. 切回按章节：恢复多组、顺序不变 ---- */
  const back = await snapshot();
  check('切回按章节：分组数恢复', back.length === chapter.length, back.length + ' vs ' + chapter.length);
  check('切回按章节：分组顺序与初始一致', back.map(g => g.name).join(' | ') === chapterOrder);

  /* ---- 6. 刷新后记住选择 ---- */
  await selectSort('difficulty');
  await page.reload();
  await page.waitForSelector('.grpbox');
  const selAfter = await page.$eval('#sortSelect', s => s.value);
  const afterReload = await snapshot();
  check('刷新后仍是难度 易→难', selAfter === 'difficulty', selAfter);
  check('刷新后仍是单分组', afterReload.length === 1, afterReload.length + ' 组');

  /* ---- 7. 难度模式 + 题型筛选能叠加 ---- */
  const typed = await page.evaluate(async () => {
    const sel = document.getElementById('typeSelect');
    const opt = [...sel.options].find(o => !o.disabled && o.value !== 'all');
    if (!opt) return null;
    sel.value = opt.value;
    sel.dispatchEvent(new Event('change'));
    await new Promise(r => setTimeout(r, 300));
    const codes = [...document.querySelectorAll('.grpbox tbody tr td.c-no')].map(t => t.textContent.trim());
    const diffs = [...document.querySelectorAll('.grpbox tbody tr td.c-df')].map(td =>
      [...td.querySelectorAll('.stars > *')].filter(e => !e.classList.contains('off')).length);
    return { value: opt.value, n: codes.length, diffs };
  });
  if (typed) {
    check('难度模式 + 题型筛选：结果非空', typed.n > 0, typed.n + ' 题');
    check('难度模式 + 题型筛选：仍保持难度升序', isSorted(typed.diffs, 'asc'));
  }

  check('页面无 JS 报错', errors.length === 0, errors.join(' | '));
  console.log('\n✅ 排序方式切换全部通过（' + passed + ' 项，' + mode + '）');
} finally {
  await browser.close();
  server.close();
}
