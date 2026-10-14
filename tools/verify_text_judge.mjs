#!/usr/bin/env node
/* 对拍：理论题判题口径（JS 侧）。

   前置：先跑 python tools/verify_text_judge.py 生成夹具
   用法：node tools/verify_text_judge.mjs

   它把夹具里每条答案在 web/judge_text.js 上重判一遍，
   与 Python 侧（真实的 TextRunner + compare + scoring）的结果逐字段比对。
   任何一条不一致都会让退出码非 0。
*/
import { createRequire } from 'module';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const require = createRequire(import.meta.url);

const TJ = require(join(ROOT, 'web', 'judge_text.js'));
const FIX = join(ROOT, 'data', '_text_judge_fixtures.json');

const FIELDS = ['verdict', 'score', 'max_score', 'passed', 'total', 'normalized', 'message'];

function j(x) { return JSON.stringify(x); }

function diffOne(py, js) {
  const diffs = [];
  for (const k of FIELDS) {
    if (py[k] !== js[k]) diffs.push(`  ${k}:  python=${j(py[k])}  js=${j(js[k])}`);
  }
  const pc = py.cases || [];
  const jc = (js.cases || []).map(c => c.verdict);
  if (pc.length !== jc.length) {
    diffs.push(`  case 数: python=${pc.length}  js=${jc.length}`);
  } else {
    for (let i = 0; i < pc.length; i++) {
      if (pc[i] !== jc[i]) diffs.push(`  case[${i}]: python=${pc[i]}  js=${jc[i]}`);
    }
  }
  return diffs;
}

function main() {
  let payload;
  try {
    payload = JSON.parse(readFileSync(FIX, 'utf8'));
  } catch (e) {
    console.error('读不到夹具：' + FIX);
    console.error('先跑：python tools/verify_text_judge.py');
    process.exit(2);
  }

  const probs = payload.probs || [];
  let nAns = 0, nBad = 0, nAC = 0, nWrong = 0;
  const badCases = [];

  for (const p of probs) {
    for (const a of (p.answers || [])) {
      nAns++;
      const js = TJ.judgeTextProblem(p, a.text);
      if (js.error) {
        nBad++;
        badCases.push({ id: p.id, title: p.title, answer: a.text, diffs: ['  js 报错：' + js.error] });
        continue;
      }
      if (a.py.verdict === 'AC') nAC++; else nWrong++;
      const diffs = diffOne(a.py, js);
      if (diffs.length) {
        nBad++;
        if (badCases.length < 25) {
          badCases.push({ id: p.id, title: p.title, answer: a.text, diffs });
        }
      }
    }
  }

  /* ---- 正反两面都要有，否则对拍本身可能是假的 ---- */
  console.log('='.repeat(64));
  console.log('理论题判题对拍：JS(web/judge_text.js)  vs  Python(真实实现)');
  console.log('='.repeat(64));
  console.log(`题目 ${probs.length} 道 / 答案 ${nAns} 条`);
  console.log(`  python 侧判 AC 的：${nAC} 条`);
  console.log(`  python 侧判错的：  ${nWrong} 条`);
  console.log('');

  const sane = nAC > 0 && nWrong > 0;
  console.log(`[合理性] python 侧同时存在 AC 与非 AC：${sane ? '是' : '★ 否 —— 对拍可能恒真，无意义'}`);

  if (nBad) {
    console.log('');
    console.log(`[差异] ${nBad} / ${nAns} 条不一致，前几例：`);
    for (const b of badCases) {
      console.log(`  · 题 #${b.id} ${b.title.slice(0, 26)}  答案=${j(b.answer)}`);
      b.diffs.forEach(d => console.log(d));
    }
  }

  console.log('');
  const ok = nBad === 0 && sane;
  console.log(ok ? `全部通过：${nAns} 条答案两端结果逐字段一致`
                 : `★ 失败：${nBad} 条不一致`);
  process.exit(ok ? 0 : 1);
}

main();
