#!/usr/bin/env node
/* 本地理论题判题器的「行为说明书」——用真实行为回答「是不是拿固定答案糊弄」。

   做三件事：
     A. 逐题演示：同一道题喂多种写法，看判题器接受哪些、拒绝哪些
     B. 变异测试：把标准答案故意改坏（删/增/换字符），证明它真的在判别
     C. 反向统计：非标准答案里被拒的比例

   用法：node tools/show_text_judge.mjs
   （数据来自 docs/problems.json，即线上站点实际下发的那份） */

import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..');

const TextJudge = require(join(ROOT, 'web', 'judge_text.js'));
const bank = JSON.parse(readFileSync(join(ROOT, 'docs', 'problems.json'), 'utf8'));
const items = (bank.items || []).filter((p) => p.line === 'text');

let fail = 0;
function check(name, cond, extra) {
  const ok = !!cond;
  if (!ok) fail++;
  console.log(`   ${ok ? '✓' : '✗'} ${name}${extra ? '   ' + extra : ''}`);
}

/* 判一次，返回 'AC' / 'WA' / 'PE' */
function judge(p, answer) {
  const r = TextJudge.judgeTextProblem(p, answer);
  if (r.error) throw new Error(r.error);
  return r.verdict;
}

const byId = (id) => items.find((p) => String(p.id) === String(id));
const altsOf = (p) => TextJudge.oneofAlternatives((p.cases[0] || {}).expected_stdout || '');

/* 打印一题：声明接受什么 + 我喂的每种写法结果如何 */
function showcase(p, variants) {
  console.log(`\n── [${p.id}] ${p.title}`);
  console.log(`   类型 ${p.is_choice ? '选择题' : '填空题'} · checker=${p.checker} · 分值 ${p.total_score}`);
  const alts = altsOf(p);
  console.log(`   题库声明接受 ${alts.length} 种写法：`);
  alts.forEach((a) => console.log(`     · ${JSON.stringify(a)}`));
  console.log('   实际判定：');
  variants.forEach((v) => {
    const declared = alts.indexOf(v.text) >= 0;
    const got = judge(p, v.text);
    const good = got === v.want;
    if (!good) fail++;
    const mark = got === 'AC' ? 'AC' : got;
    console.log(`     ${good ? ' ' : '!'} ${mark.padEnd(2)}  ${JSON.stringify(v.text).padEnd(46)}` +
      `  ${v.note}${declared ? '（题库里有）' : '（题库里没有，靠判题逻辑判）'}${good ? '' : '  ← 与预期 ' + v.want + ' 不符'}`);
  });
}

console.log('================================================================');
console.log(' 本地理论题判题器 · 真实行为演示');
console.log(` 题库：${items.length} 道理论题（全部 oneof）`);
console.log('================================================================');

/* ---------------- A. 逐题演示 ---------------- */

console.log('\n【A】同一道题，多种写法');

const q111 = byId(111);   // 填空：ls -la /etc
if (q111) {
  showcase(q111, [
    { text: 'ls -la /etc', want: 'AC', note: '标准写法' },
    { text: '  ls -la /etc  ', want: 'AC', note: '前后多余空格' },
    { text: 'ls -la /etc。', want: 'AC', note: '手滑加了全角句号' },
    { text: 'ls -a -l /etc', want: 'AC', note: '短选项拆开写' },
    { text: 'ls -lha /etc', want: 'AC', note: '短选项顺序打乱 -lah→-lha' },
    { text: 'ls    -la   /etc', want: 'AC', note: '中间多个空格' },
    { text: 'ls -la /var', want: 'WA', note: '路径写错' },
    { text: 'ls -1 /etc', want: 'WA', note: '选项写错（漏了 a）' },
    { text: 'ls /etc', want: 'WA', note: '选项全漏' },
  ]);
}

const q117 = byId(117);   // 填空：tar -czf
if (q117) {
  showcase(q117, [
    { text: 'tar -czf project.tar.gz ~/project', want: 'AC', note: '标准写法' },
    { text: 'tar czf project.tar.gz ~/project', want: 'AC', note: '不带横杠' },
    { text: 'tar -c -z -f project.tar.gz ~/project', want: 'AC', note: '短选项拆开' },
    { text: 'tar -fz -c project.tar.gz ~/project', want: 'AC', note: '短选项乱序' },
    { text: 'tar -xzf project.tar.gz ~/project', want: 'WA', note: '把 c 写成 x（方向反了）' },
    { text: 'tar --create --gzip --file project.tar.gz ~/project', want: 'WA',
      note: '★长选项写法：题库没声明，判题器不认（下面会专门说这条）' },
  ]);
}

/* 找一道真·选择题和一道判断题 */
const qChoice = items.find((p) => p.is_choice && altsOf(p).length >= 2 && !/判断题/.test(p.title));
const qJudge = items.find((p) => p.is_choice && altsOf(p).some((a) => a.indexOf('错') === 0));

if (qChoice) {
  const alts = altsOf(qChoice);
  const letter = alts.find((a) => /^[A-D]$/.test(a)) || alts[0];
  const wrongLetter = 'ABCD'.split('').find((c) => alts.indexOf(c) < 0) || 'D';
  showcase(qChoice, [
    { text: letter, want: 'AC', note: '选项字母' },
    { text: alts[alts.length - 1], want: 'AC', note: '选项原文全文' },
    { text: ' ' + letter + ' ', want: 'AC', note: '字母两边带空格' },
    { text: wrongLetter, want: 'WA', note: '选错' },
    { text: 'E', want: 'WA', note: '不存在的选项' },
  ]);
}

if (qJudge) {
  showcase(qJudge, [
    { text: '错', want: 'AC', note: '标准写法' },
    { text: '错误', want: 'AC', note: '同义' },
    { text: 'F', want: 'AC', note: '英文缩写' },
    { text: ' 错 ', want: 'AC', note: '带空格' },
    { text: '对', want: 'WA', note: '选反了' },
    { text: 'false', want: 'AC', note: '英文全称也被认（词表归一化：false→错）' },
    { text: 'yes', want: 'WA', note: 'yes=对，判成非 AC 才对' },
  ]);
}

/* ---------------- B. 变异测试 ---------------- */

console.log('\n\n【B】变异测试：把标准答案故意改坏，看能不能被揪出来');
console.log('   （拿 24 道填空题的命令答案做底，每题生成 3 类「近似错」）');

const fill = items.filter((p) => !p.is_choice && altsOf(p).length >= 1);
let mutTotal = 0, mutCaught = 0;
const escaped = [];

function mutate(s, kind) {
  const arr = Array.from(s);
  if (!arr.length) return null;
  if (kind === 'drop') {
    const i = Math.max(0, arr.length - 1);
    return arr.slice(0, i).join('');
  }
  if (kind === 'corrupt') {
    /* 把命令名最后一个字母换掉（ls→lz、head→heax）：语义必变，必须被抓 */
    const parts = s.split(' ');
    const cmd = Array.from(parts[0]);
    if (cmd.length < 2) return null;
    cmd[cmd.length - 1] = cmd[cmd.length - 1] === 'z' ? 'q' : 'z';
    return [cmd.join(''), ...parts.slice(1)].join(' ');
  }
  if (kind === 'swap') {
    const parts = s.split(' ');
    if (parts.length < 2) return null;
    if (parts.length === 2) return parts[1] + ' ' + parts[0];
    const out = parts.slice();
    const t = out[1]; out[1] = out[2]; out[2] = t;
    return out.join(' ');
  }
  return null;
}

fill.forEach((p) => {
  const base = altsOf(p)[0];
  if (!/^[\x20-\x7e]+$/.test(base)) return;   // 只变异纯 ASCII 命令
  ['drop', 'corrupt', 'swap'].forEach((kind) => {
    const m = mutate(base, kind);
    if (m === null || m === base) return;
    mutTotal++;
    const v = judge(p, m);
    if (v === 'AC') {
      /* 变异后仍然 AC —— 要么它恰好等于题库里另一个合法备选，要么是判题太松 */
      const declared = altsOf(p).indexOf(m) >= 0;
      if (!declared) escaped.push({ id: p.id, base, mut: m, kind });
    } else {
      mutCaught++;
    }
  });
});

console.log(`   生成错答案 ${mutTotal} 条，被判定为非 AC 的 ${mutCaught} 条 ` +
  `（${(mutCaught / mutTotal * 100).toFixed(1)}%）`);
check(`${mutTotal} 条变异答案中，至少 95% 被判错`, mutCaught / mutTotal >= 0.95,
  `${mutCaught}/${mutTotal}`);
check('没有「变异后仍然意外判对」的漏网（即判题不是恒真）', escaped.length === 0,
  escaped.length ? JSON.stringify(escaped.slice(0, 5)) : '0 条漏网');

/* ---------------- C. 反向统计：正例 vs 反例 ---------------- */

console.log('\n\n【C】全库抽样：标准答案 vs 人为错答案');

let accAll = 0, accOk = 0, rejAll = 0, rejOk = 0;
items.forEach((p) => {
  const alts = altsOf(p);
  if (!alts.length) return;
  /* 正例：每个声明备选都该 AC */
  alts.forEach((a) => { accAll++; if (judge(p, a) === 'AC') accOk++; });
  /* 反例：明显不沾边的字符串都该被拒 */
  ['zzz_不存在_zzz', '42', '???'].forEach((bad) => {
    rejAll++; if (judge(p, bad) !== 'AC') rejOk++;
  });
});

check(`题库声明的 ${accAll} 个标准答案全部判 AC`, accOk === accAll, `${accOk}/${accAll}`);
check(`人为胡写的 ${rejAll} 个答案全部被判错`, rejOk === rejAll, `${rejOk}/${rejAll}`);

console.log('\n================================================================');
console.log(fail === 0 ? ' 全部证据通过' : ` 有 ${fail} 项不符`);
console.log('================================================================');
process.exit(fail === 0 ? 0 : 1);
