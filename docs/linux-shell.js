/* ===========================================================================
   Linux 命令沙箱 · 主控（第 5 层）
   ---------------------------------------------------------------------------
   职责三件：
     1. 把一行命令真正跑起来（引号 / 变量 / 管道 / 重定向 / && || ;）
     2. 提供一个 xterm 味的终端界面，嵌在每道 Linux 题旁边
     3. 全局只维护**一台**虚拟机 —— 学生在这里 ls、cd、chmod 的效果会累积，
        跟真机一致。搞乱了按「重置」重开。

   ★ 为什么判题不用它：判题在浏览器里比对**命令文本**（见 app/judge/compare.py），
     不执行学生提交的内容。沙箱只负责「让你试」，不负责「给你打分」。
     这样即使沙箱有 bug，也不会有人靠它在判题上作弊。
   =========================================================================== */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.LinuxShell = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var core = null, CMD = null;

  function ensureLoaded() {
    if (CMD) return true;
    if (typeof require === 'function' && typeof module === 'object' && module.exports) {
      core = require('./linux-shell-core.js');
      CMD = {};
      require('./linux-shell-fs-cmds.js').install(core, CMD);
      require('./linux-shell-text-cmds.js').install(core, CMD);
      require('./linux-shell-sys-cmds.js').install(core, CMD);
      return true;
    }
    var g = typeof self !== 'undefined' ? self : this;
    if (!g.LinuxShellCore || !g.LinuxShellFsCmds || !g.LinuxShellTextCmds || !g.LinuxShellSysCmds) return false;
    core = g.LinuxShellCore;
    CMD = {};
    g.LinuxShellFsCmds.install(core, CMD);
    g.LinuxShellTextCmds.install(core, CMD);
    g.LinuxShellSysCmds.install(core, CMD);
    return true;
  }

  /* =========================================================================
     执行引擎
     ========================================================================= */

  var fs = null;

  function reset(opts) {
    ensureLoaded();
    fs = core.buildImage(opts || {});
    fs.aliases = { ll: 'ls -l', la: 'ls -a' };
    fs.umask = 0o022;
    core.rewriteAccounts(fs);
    return fs;
  }

  function getFs() { if (!fs) reset(); return fs; }

  function userName() { return core.userNameOf(fs, fs.uid) || String(fs.uid); }

  /* 补全 `~`：`~/x` → HOME。单引号里的不动。 */
  function tilde(s) {
    if (s === '~') return fs.env.HOME;
    if (s.slice(0, 2) === '~/') return fs.env.HOME.replace(/\/$/, '') + s.slice(1);
    if (s.slice(0, 2) === '~+') return fs.cwd;
    return s;
  }

  /* $(命令) 真的执行并把输出接进来；其余交给 core.expandVars */
  function expand(s, q) {
    if (q === "'") return s;
    var out = '', i = 0;
    while (i < s.length) {
      if (s[i] === '$' && s[i + 1] === '(' && s[i + 2] !== '(') {
        var depth = 0, j = i + 1;
        while (j < s.length) {
          if (s[j] === '(') depth++;
          else if (s[j] === ')') { depth--; if (depth === 0) break; }
          j++;
        }
        if (j < s.length) {
          var inner = s.slice(i + 2, j);
          var r = runLine(inner);
          out += String(r.out).replace(/\n+$/, '');
          i = j + 1;
          continue;
        }
      }
      out += s[i]; i++;
    }
    return core.expandVars(fs, out);
  }

  /* 执行一条简单命令（argv 已展开）；返回 {out, err, code}
     meta.piped —— 输出接去了管道或重定向。ls 靠它决定「多列还是单列」：
     真机 ls 到管道时自动单列，学生 `ls | grep x` 才不会一行匹配出三个名字。 */
  function runSimple(argv, stdin, meta) {
    if (!argv.length) return { out: '', err: '', code: fs.lastCode };

    /* 前导赋值：FOO=bar cmd */
    var i = 0, assigns = [];
    while (i < argv.length && /^[A-Za-z_][A-Za-z0-9_]*=/.test(argv[i])) {
      assigns.push(argv[i]); i++;
    }
    if (assigns.length) {
      assigns.forEach(function (a) {
        var eq = a.indexOf('=');
        var val = a.slice(eq + 1);
        fs.env[a.slice(0, eq)] = val;
      });
      if (i >= argv.length) return { out: '', err: '', code: 0 };
      argv = argv.slice(i);
    }

    /* 别名展开（只展开第一个词，且不递归） */
    var name = argv[0];
    if (fs.aliases && fs.aliases[name]) {
      var aliasVal = fs.aliases[name];
      var parts = aliasVal.match(/(?:[^\s"']+|"[^"]*"|'[^']*')+/g) || [];
      argv = parts.concat(argv.slice(1));
      name = argv[0];
    }

    var fn = CMD[name];
    if (!fn) {
      /* 沙箱里没有的命令：报 bash 那句原话，别让人以为自己打错了 */
      return { out: '', err: name + ': command not found', code: 127 };
    }

    var ctx = {
      stdin: stdin == null ? '' : stdin,
      err: [],
      width: 80,
      piped: !!(meta && meta.piped),
      tty: !(meta && meta.piped) && !!(meta && meta.tty),
      exec: function (a) { return runSimple(a, '', { piped: true }); },
      execAs: function (a, uid) {
        var bu = fs.uid, bg = fs.gid, be = { USER: fs.env.USER, HOME: fs.env.HOME, LOGNAME: fs.env.LOGNAME };
        fs.uid = uid; fs.gid = uid;
        fs.env.USER = core.userNameOf(fs, uid) || 'root';
        fs.env.LOGNAME = fs.env.USER;
        var r = runSimple(a, '', { piped: true });
        fs.uid = bu; fs.gid = bg;
        fs.env.USER = be.USER; fs.env.HOME = be.HOME; fs.env.LOGNAME = be.LOGNAME;
        return r;
      }
    };

    var r;
    try {
      r = fn(fs, argv.slice(1), ctx);
    } catch (e) {
      return { out: '', err: name + ': ' + (e && e.message ? e.message : '内部错误'), code: 2 };
    }
    if (r == null) r = { out: '', err: '', code: 0 };
    if (typeof r === 'string') r = { out: r, err: '', code: 0 };
    if (ctx.err.length) r.err = [r.err || ''].concat(ctx.err).filter(Boolean).join('\n');
    if (r.code == null) r.code = 0;
    return r;
  }

  /* 一整个管道段（含重定向） */
  function runSegment(seg, stdin, meta) {
    var argv = seg.argv.map(function (t) { return t; });
    var r = runSimple(argv, stdin, meta);
    var out = r.out, err = r.err || '', code = r.code;

    /* 命令输出统一以换行收尾（真机就是这样）。少了这一个 \n，
       `grep x f | wc -l` 会永远少数一行 —— 这是最隐蔽的一类偏差。 */
    var cname = argv[0];
    var keepNoNl = cname === 'printf' || (cname === 'echo' && argv.indexOf('-n') >= 0);
    if (!keepNoNl && out && out.slice(-1) !== '\n') out += '\n';

    if (seg.redir) {
      if (seg.redir.out != null) {
        var abs = core.normalize(fs.cwd, seg.redir.out);
        var e = CMD.__h.writeFile(fs, abs, out, !!seg.redir.outAppend);
        if (e) err = (err ? err + '\n' : '') + 'bash: ' + seg.redir.out + ': ' + e;
        else out = '';
      }
      if (seg.redir.err != null) {
        var abs2 = core.normalize(fs.cwd, seg.redir.err);
        var e2 = CMD.__h.writeFile(fs, abs2, err + (err ? '\n' : ''), !!seg.redir.errAppend);
        if (!e2) err = '';
      }
    }
    return { out: out, err: err, code: code };
  }

  /* 执行一整行（可能含 ; && ||） */
  function runLine(line, o) {
    ensureLoaded();
    getFs();
    var tty = !!(o && o.tty);
    if (line == null) return { out: '', err: '', code: 0 };
    var toks = core.tokenize(String(line));
    if (!toks.length) return { out: '', err: '', code: fs.lastCode };

    /* 先把 token 里的变量与 ~ 展开；操作符 token（q==='@'）跳过 */
    toks = toks.map(function (t) {
      if (t.q === '@') return t;
      var v = expand(t.v, t.q);
      if (t.q !== "'") v = tilde(v);
      return { v: v, q: t.q };
    });

    var parsed = core.parsePipelines(toks);
    var outs = [], errs = [], code = 0;
    var lastOut = '';

    parsed.segs.forEach(function (seg, idx) {
      var prevSep = idx > 0 ? parsed.seps[idx - 1] : null;
      var nextSep = parsed.seps[idx];
      if (prevSep === '&&' && code !== 0) return;
      if (prevSep === '||' && code === 0) return;
      if (!seg.argv.length && seg.redir.out == null && seg.redir.err == null) return;

      /* ★ 这一段要执行的字符串，到这里才把 `$?` / `$PWD` 换成此刻的真值。
         解析阶段只能落占位符 —— 那时候上一段还没跑，取到的都是旧值。 */
      seg.argv = seg.argv.map(function (v) { return core.resolveDynamic(fs, v); });
      ['out', 'err', 'in', 'append'].forEach(function (k) {
        if (seg.redir && seg.redir[k] != null) seg.redir[k] = core.resolveDynamic(fs, seg.redir[k]);
      });

      var piped = prevSep === '|' || nextSep === '|' || seg.redir.out != null;
      var stdin = prevSep === '|' ? lastOut : '';
      var r = runSegment(seg, stdin, { piped: piped, tty: tty && !piped });
      /* ★ 退出码要**当场**写回去：下一段的 `$?` 在它执行前才解析，
         等到循环结束再写就永远是上一行的旧值。 */
      fs.lastCode = r.code;
      lastOut = r.out;
      if (nextSep !== '|') outs.push(r.out);
      if (r.err) errs.push(r.err);
      code = r.code;
    });

    fs.lastCode = code;
    return { out: outs.filter(Boolean).join(''), err: errs.filter(Boolean).join('\n'), code: code };
  }

  /* 供外部（测试）用 */
  function exec(line, o) {
    var r = runLine(line, o);
    fs.lastCode = r.code;
    return r;
  }
  function execScript(text) {
    var out = [], errs = [], code = 0;
    String(text).split('\n').forEach(function (l) {
      if (!l.trim() || /^\s*#/.test(l)) return;
      var r = runLine(l);
      if (r.out) out.push(r.out.replace(/\n$/, ''));
      if (r.err) errs.push(r.err);
      code = r.code;
    });
    return { out: out.join('\n'), err: errs.join('\n'), code: code };
  }

  /* =========================================================================
     终端界面
     ========================================================================= */

  function promptText() {
    var u = userName();
    var home = fs.env.HOME || '';
    var cwd = fs.cwd;
    if (home && cwd.indexOf(home) === 0) cwd = '~' + cwd.slice(home.length);
    if (!cwd) cwd = '/';
    return { user: u, host: fs.env.HOSTNAME || 'fedora', cwd: cwd, root: fs.uid === 0 };
  }

  var HISTORY = [];
  var histIdx = -1;

  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function mount(el, opts) {
    ensureLoaded();
    getFs();
    opts = opts || {};
    if (el.__shellMounted) return el.__shellApi;
    el.__shellMounted = true;

    el.classList.add('shellTerm');
    el.innerHTML =
      '<div class="shellBar">' +
        '<span class="shellDots"><i></i><i></i><i></i></span>' +
        '<span class="shellTitle">fedora : bash</span>' +
        '<span class="grow"></span>' +
        '<button type="button" class="shellBtn" data-act="clear" title="清屏（Ctrl+L）">清屏</button>' +
        '<button type="button" class="shellBtn" data-act="reset" title="重开一台干净的虚拟机">重置</button>' +
      '</div>' +
      '<div class="shellBody" tabindex="0">' +
        '<div class="shellOut"></div>' +
        '<div class="shellLine">' +
          '<span class="shellPs1"></span>' +
          '<input class="shellIn" type="text" spellcheck="false" autocomplete="off" ' +
            'autocapitalize="off" autocorrect="off" aria-label="命令行输入">' +
        '</div>' +
      '</div>';

    var out = el.querySelector('.shellOut');
    var body = el.querySelector('.shellBody');
    var input = el.querySelector('.shellIn');
    var ps1 = el.querySelector('.shellPs1');

    function drawPrompt() {
      var p = promptText();
      ps1.innerHTML = '<b class="' + (p.root ? 'uRoot' : 'uUser') + '">' + esc(p.user) + '</b>' +
        '<span class="at">@</span><b class="uHost">' + esc(p.host) + '</b> ' +
        '<span class="uPath">' + esc(p.cwd) + '</span>' +
        '<span class="uMark">' + (p.root ? '#' : '$') + '</span>';
    }

    function print(text, cls) {
      if (!text) return;
      var d = document.createElement('div');
      d.className = 'shellRow' + (cls ? ' ' + cls : '');
      d.textContent = text;
      out.appendChild(d);
    }

    function run(text) {
      var p = promptText();
      print('[' + p.user + '@' + p.host + ' ' + p.cwd + ']' + (p.root ? '#' : '$') + ' ' + text, 'shellEcho');
      var r = exec(text);
      if (r.out) print(r.out.replace(/\n$/, ''));
      if (r.err) print(r.err.replace(/\n$/, ''), 'shellErr');
      if (r.code) print('（退出码 ' + r.code + '）', 'shellCode');
      body.scrollTop = body.scrollHeight;
      drawPrompt();
    }

    input.addEventListener('keydown', function (ev) {
      if (ev.isComposing) return;
      if (ev.key === 'Enter') {
        ev.preventDefault();
        var v = input.value;
        input.value = '';
        if (v.trim()) { HISTORY.push(v); histIdx = HISTORY.length; }
        if (/^\s*clear\s*$/.test(v)) { out.innerHTML = ''; return; }
        run(v);
        if (opts.onRun) opts.onRun(v, el);
        return;
      }
      if (ev.key === 'ArrowUp') {
        ev.preventDefault();
        if (histIdx > 0) { histIdx--; input.value = HISTORY[histIdx] || ''; }
        return;
      }
      if (ev.key === 'ArrowDown') {
        ev.preventDefault();
        if (histIdx < HISTORY.length - 1) { histIdx++; input.value = HISTORY[histIdx] || ''; }
        else { histIdx = HISTORY.length; input.value = ''; }
        return;
      }
      if (ev.key === 'Tab') {
        ev.preventDefault();
        complete(input);
        return;
      }
      if (ev.key === 'l' && (ev.ctrlKey || ev.metaKey)) {
        ev.preventDefault();
        out.innerHTML = '';
        return;
      }
      if (ev.key === 'c' && ev.ctrlKey) {
        ev.preventDefault();
        print('^C', 'shellErr');
        input.value = '';
        drawPrompt();
      }
    });

    /* Tab 补全：先补命令名（第一个词），否则补路径 */
    function complete(inp) {
      var v = inp.value;
      var parts = v.split(/\s+/);
      if (parts.length <= 1) {
        var names = Object.keys(CMD).filter(function (k) {
          return k.indexOf('__') !== 0 && k !== 'help' && k.charAt(0) !== '_' && k.indexOf(v) === 0;
        }).sort();
        if (names.length === 1) inp.value = names[0] + ' ';
        else if (names.length > 1) print(names.join('  '));
        return;
      }
      var last = parts[parts.length - 1];
      var abs = core.normalize(fs.cwd, last === '' ? '.' : last);
      var slash = abs.lastIndexOf('/');
      var dirAbs = slash === 0 ? '/' : abs.slice(0, slash);
      var stem = abs.slice(slash + 1);
      var d = core.lookup(fs, dirAbs, true);
      if (!d || d.t !== 'T') {}
      if (!d || d.t !== core.T.DIR) return;
      var hits = Object.keys(d.ch).filter(function (n) { return n.indexOf(stem) === 0; }).sort();
      if (!hits.length) return;
      if (hits.length === 1) {
        var pref = last.slice(0, last.length - stem.length);
        var isDirEntry = d.ch[hits[0]].t === core.T.DIR;
        parts[parts.length - 1] = pref + hits[0] + (isDirEntry ? '/' : ' ');
        inp.value = parts.join(' ');
      } else {
        print(hits.join('  '));
      }
    }

    el.querySelector('.shellBar').addEventListener('click', function (ev) {
      var act = ev.target && ev.target.getAttribute('data-act');
      if (act === 'clear') { out.innerHTML = ''; input.focus(); }
      if (act === 'reset') {
        reset();
        out.innerHTML = '';
        print('已重置：回到刚装好系统的状态。', 'shellNote');
        drawPrompt();
        input.focus();
      }
    });

    body.addEventListener('click', function (ev) {
      if (ev.target === out || ev.target === body) input.focus();
    });

    drawPrompt();
    print('Fedora Linux 44 (Workstation Edition)  ·  命令沙箱', 'shellNote');
    print('这是一台虚拟机器：ls / cd / cp / chmod / useradd 都会真的改这里的文件。' +
          '写命令前先在这儿试，试明白了再提交。', 'shellNote');

    var api = {
      el: el,
      exec: exec,
      fs: function () { return fs; },
      reset: function () { reset(); out.innerHTML = ''; drawPrompt(); },
      print: print,
      focus: function () { input.focus(); }
    };
    el.__shellApi = api;
    return api;
  }

  return {
    reset: reset, fs: getFs, exec: exec, execScript: execScript,
    mount: mount, commands: function () { ensureLoaded(); return Object.keys(CMD); }
  };
});
