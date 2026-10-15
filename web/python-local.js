/* Browser-only Python judge. The worker owns Pyodide and can be terminated on timeout. */
(function (root) {
  'use strict';
  let worker = null, ready = null, nextId = 1, busy = false;

  function reset() {
    if (worker) worker.terminate();
    worker = null; ready = null;
  }

  function ensure() {
    if (ready) return ready;
    const w = new Worker('python-worker.js', { type: 'module' });
    worker = w;
    ready = new Promise((resolve, reject) => {
      const timer = setTimeout(() => fail(Error('Python 引擎加载超时')), 90000);
      function fail(error) { clearTimeout(timer); reset(); reject(error); }
      w.addEventListener('error', e => fail(Error(e.message || 'Python Worker 加载失败')), { once: true });
      w.addEventListener('messageerror', () => fail(Error('Python Worker 消息错误')), { once: true });
      w.addEventListener('message', e => {
        if (e.data.type === 'ready') { clearTimeout(timer); resolve(e.data.python); }
        if (e.data.type === 'fatal') fail(Error(e.data.detail));
      });
    });
    return ready;
  }

  async function runCase(payload, timeoutMs) {
    await ensure();
    return new Promise(resolve => {
      const w = worker, id = nextId++;
      const timer = setTimeout(() => {
        w.removeEventListener('message', onMessage);
        reset();
        resolve({ verdict: 'TLE', ms: timeoutMs, stdout: '', stderr: '',
          detail: '超过 ' + timeoutMs + ' ms，已中断运行' });
      }, timeoutMs);
      function onMessage(e) {
        if (e.data.type !== 'result' || e.data.id !== id) return;
        clearTimeout(timer);
        w.removeEventListener('message', onMessage);
        resolve(e.data.payload);
      }
      w.addEventListener('message', onMessage);
      w.postMessage(Object.assign({ type: 'case', id }, payload));
    });
  }

  async function submit(problem, code, progress) {
    if (busy) throw Error('已有 Python 任务正在运行');
    const cases = problem.cases || [];
    if (!cases.length) throw Error('静态题库缺少测试点，无法在浏览器判题');
    busy = true;
    try {
      const rawPoints = cases.map(c => Math.max(0, Number(c.points) || 0));
      let points = rawPoints;
      if (!points.some(Boolean)) {
        const total = Number(problem.total_score) || 0;
        const base = Math.floor(total / cases.length), rem = total % cases.length;
        points = cases.map((_, i) => base + (i < rem ? 1 : 0));
      }
      let score = 0, passed = 0, totalMs = 0, verdict = 'AC', message = '';
      const details = [];
      for (let i = 0; i < cases.length; i++) {
        const c = cases[i];
        const limit = Math.max(2000, (Number(problem.time_limit_ms) || 1000) * 3 + 1000);
        const r = await runCase({ mode: 'judge', code, stdin: c.stdin || '',
          expected: c.expected_stdout || '', checker: problem.checker || 'standard',
          eps: Number(problem.float_eps) || 1e-6 }, limit);
        const earned = r.verdict === 'AC' ? points[i] : 0;
        score += earned;
        if (earned || r.verdict === 'AC') passed++;
        if (r.verdict !== 'AC' && verdict === 'AC') { verdict = r.verdict; message = r.detail || ''; }
        totalMs += Number(r.ms) || 0;
        details.push({ verdict: r.verdict, points: points[i], earned,
          time_ms: Math.round(Number(r.ms) || 0), stdin: c.stdin || '',
          expected: c.expected_stdout || '', stdout: r.stdout || '', stderr: r.stderr || '',
          detail: r.detail || '' });
        if (progress) progress(i + 1, cases.length);
        if (r.verdict === 'CE' || r.verdict === 'IE') break;
      }
      return { verdict, score, max_score: points.reduce((a, b) => a + b, 0),
        passed, total: cases.length, time_ms: Math.round(totalMs), lang: 'python',
        message, cases: details };
    } finally { busy = false; }
  }

  async function run(code, stdin) {
    if (busy) throw Error('已有 Python 任务正在运行');
    busy = true;
    try { return await runCase({ mode: 'run', code, stdin }, 6000); }
    finally { busy = false; }
  }

  root.PythonLocal = { submit, run };
})(typeof window !== 'undefined' ? window : self);
