/* 真浏览器检查题型标签、筛选与多选交互。
   PTA_SITE_DIR 可指向临时静态导出；默认检查仓库 docs/。 */
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { createRequire } from 'node:module';

const repo = process.cwd();
const root = path.resolve(process.env.PTA_SITE_DIR || path.join(repo, 'docs'));
const moduleDir = process.env.NODE_MODULES_DIR || path.join(repo, 'experiments/pyodide-judge/node_modules');
const require = createRequire(path.join(moduleDir, 'noop.js'));
const puppeteer = require('puppeteer-core');
const bank = JSON.parse(fs.readFileSync(path.join(root, 'problems.json'), 'utf8'));
const items = bank.items || [];
if (!items.length || items.some(p => !p.question_type)) throw Error('静态题库缺少 question_type');

const server = http.createServer((req, res) => {
  const pathname = decodeURIComponent(req.url.split('?')[0]);
  const file = path.resolve(root, '.' + (pathname === '/' ? '/index.html' : pathname));
  if (!file.startsWith(root + path.sep)) { res.writeHead(403).end(); return; }
  fs.readFile(file, (err, data) => {
    if (err) { res.writeHead(404).end(); return; }
    const ext = path.extname(file);
    res.setHeader('Content-Type', ext === '.js' ? 'text/javascript' : ext === '.json' ? 'application/json' : 'text/html');
    res.end(data);
  });
});
await new Promise(resolve => server.listen(0, resolve));
const base = `http://127.0.0.1:${server.address().port}/`;
const browser = await puppeteer.launch({
  executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: true, args: ['--no-sandbox']
});
const page = await browser.newPage();
const errors = [];
page.on('pageerror', e => errors.push(String(e)));
const check = (name, ok) => { if (!ok) throw Error(name); console.log('PASS ' + name); };
try {
  await page.goto(base + '#/set/linux');
  await page.waitForSelector('.typeSelect');
  const expectedFill = items.filter(p => p.subject === 'linux' && p.question_type === 'fill_blank').length;
  await page.select('.typeSelect', 'fill_blank');
  const shown = await page.$$('.ptable tbody tr');
  check('题型筛选计数', shown.length === expectedFill && expectedFill > 0);
  check('列表题型标签', await page.$$eval('.ptable tbody .tyTag', tags => tags.every(t => t.textContent === '填空题')));
  await page.click('.ptable tbody tr a');
  await page.waitForSelector('.chips .tyTag');
  check('题面题型标签', await page.$eval('.chips .tyTag', e => e.textContent === '填空题'));

  await page.evaluate(() => {
    const source = PROBLEMS.find(p => p.line === 'text' && p.choices && p.choices.length >= 3);
    const synthetic = Object.assign({}, source, { id: 999999, title: '多选交互校验', question_type: 'multiple_choice' });
    PROBLEMS.push(synthetic);
    CUR = synthetic;
    renderProblem();
  });
  await page.click('.choice[data-i="2"]');
  await page.click('.choice[data-i="0"]');
  check('多选按字母顺序提交', await page.evaluate(() => readTheoryAnswer() === 'AC'));
  await page.click('.choice[data-i="2"]');
  check('多选可取消', await page.evaluate(() => readTheoryAnswer() === 'A'));
  check('页面无脚本错误', errors.length === 0);
} finally {
  await browser.close();
  server.close();
}
