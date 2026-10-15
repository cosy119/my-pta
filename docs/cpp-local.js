/* Browser-only C/C++ judging. One compile, then isolated runs for all test cases. */
(function (root) {
  'use strict';
  let worker = null, nextId = 1, busy = false;
  function reset() { if (worker) worker.terminate(); worker = null; }
  function ensure() { return worker || (worker = new Worker('cpp-worker.js')); }
  function request(payload, timeoutMs, onLoad) {
    return new Promise((resolve, reject) => {
      const w = ensure(), id = nextId++;
      const timer = setTimeout(() => {
        w.removeEventListener('message', onMessage);
        w.removeEventListener('error', onError); reset();
        resolve({ verdict: payload.type === 'compile' ? 'IE' : 'TLE',
          stdout: '', stderr: '', ms: timeoutMs,
          detail: payload.type === 'compile' ? '编译器加载或编译超时' : '超过 ' + timeoutMs + ' ms，已中断程序' });
      }, timeoutMs);
      function onMessage(e) {
        if (e.data.type === 'load') { if (onLoad) onLoad(e.data.value); return; }
        if (e.data.type !== 'result' || e.data.id !== id) return;
        clearTimeout(timer); w.removeEventListener('message', onMessage);
        w.removeEventListener('error', onError);
        resolve(e.data.payload);
      }
      function onError(e) {
        clearTimeout(timer); w.removeEventListener('message', onMessage);
        w.removeEventListener('error', onError);
        reset(); reject(Error(e.message || 'C/C++ 编译器加载失败'));
      }
      w.addEventListener('message', onMessage);
      w.addEventListener('error', onError, { once: true });
      w.postMessage(Object.assign({ id }, payload));
    });
  }
  async function compile(code, lang, progress) {
    return request({ type: 'compile', code, lang }, 90000,
      value => { if (progress) progress('load', Math.round(100 * value)); });
  }
  function emptyResult(problem, lang, verdict, message, compileOutput) {
    return { verdict, score: 0, max_score: Number(problem.total_score) || 0,
      passed: 0, total: (problem.cases || []).length, time_ms: 0,
      lang, message, compile_output: compileOutput || '', cases: [] };
  }
  async function submit(problem, code, lang, progress) {
    if (busy) throw Error('已有 C/C++ 任务正在运行');
    const cases = problem.cases || [];
    if (!cases.length) throw Error('静态题库缺少测试点');
    busy = true;
    try {
      const compiled = await compile(code, lang, progress);
      if (compiled.verdict !== 'OK') return emptyResult(problem, lang,
        compiled.verdict, compiled.verdict === 'CE' ? '编译未通过' : compiled.detail,
        compiled.verdict === 'CE' ? compiled.detail : '');
      const verdicts = [], details = [], outputs = [], errors = [], times = [];
      for (let i = 0; i < cases.length; i++) {
        const c = cases[i];
        const limit = Math.max(3000, (Number(problem.time_limit_ms) || 1000) * 3);
        const run = await request({ type: 'run', stdin: c.stdin || '' }, limit);
        let verdict = run.verdict, detail = run.detail || '';
        if (verdict === 'OK') {
          const cmp = root.TextJudge.compare(c.expected_stdout || '', run.stdout || '',
            problem.checker || 'standard', Number(problem.float_eps) || 1e-6);
          verdict = cmp.ok ? 'AC' : cmp.kind === 'pe' ? 'PE' : 'WA';
          detail = cmp.detail || '';
        }
        verdicts.push(verdict); details.push(detail); outputs.push(run.stdout || '');
        errors.push(run.stderr || ''); times.push(run.ms || 0);
        if (progress) progress('case', i + 1, cases.length);
        if (verdict === 'TLE' || verdict === 'IE') break;
      }
      const grade = root.TextJudge.grade(cases.map(c => c.points), verdicts,
        Number(problem.total_score) || 0);
      const firstFailure = verdicts.findIndex(v => v !== 'AC');
      return { verdict: firstFailure < 0 ? 'AC' : verdicts[firstFailure],
        score: grade.score, max_score: grade.max_score,
        passed: verdicts.filter(v => v === 'AC').length, total: cases.length,
        time_ms: times.reduce((a, b) => a + b, 0), lang,
        message: firstFailure < 0 ? '' : details[firstFailure],
        cases: verdicts.map((v, i) => ({ verdict: v, points: grade.points[i],
          earned: grade.earned[i], time_ms: times[i], stdin: cases[i].stdin || '',
          expected: cases[i].expected_stdout || '', stdout: outputs[i], stderr: errors[i],
          detail: details[i], is_sample: !!cases[i].is_sample, ord: cases[i].ord })) };
    } finally { busy = false; }
  }
  async function run(code, lang, stdin, progress) {
    if (busy) throw Error('已有 C/C++ 任务正在运行');
    busy = true;
    try {
      const compiled = await compile(code, lang, progress);
      if (compiled.verdict !== 'OK') return { ...compiled, compile_output: compiled.detail || '' };
      return await request({ type: 'run', stdin }, 6000);
    } finally { busy = false; }
  }
  root.CppLocal = { submit, run };
})(typeof window !== 'undefined' ? window : self);
