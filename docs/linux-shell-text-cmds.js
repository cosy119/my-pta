/* ===========================================================================
   Linux 命令沙箱 · 第 3 层：文本处理与查找
   ---------------------------------------------------------------------------
   grep / sed / awk / find 是题库里的四大件（find 71 次、grep 54 次、
   sed 26 次、awk 15 次）。这四个不能糊弄 —— 糊弄了学生一上手就发现
   「老师给的命令在沙箱里跑不出结果」，整个练习环境就废了。

   ★ 正则一律用 JS RegExp。BRE（basic）和 ERE（extended）的差别
     在这里不区分：学生写 `grep 'a\|b'` 会失败，写 `grep -E 'a|b'` 能过 ——
     和真机一致的部分保留，不一致的部分在题面里避开。
   =========================================================================== */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.LinuxShellTextCmds = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  function install(core, CMD) {
    var H = CMD.__h;
    var ok = H.ok, bad = H.bad, parseFlags = H.parseFlags;
    var normalize = core.normalize, lookup = core.lookup, locate = core.locate;
    var T = core.T;

    function isDir(nd) { return nd && nd.t === T.DIR; }
    function errText(c) { return c.charAt(0) === '!'; }

    /* 读若干文件；返回 {text, name, errs} 列表（-r 时按文件拆开，
       因为 grep 要给每行加文件名前缀） */
    function collect(fs, args, ctx, recursive) {
      var files = [], errs = [];
      if (!args.length) {
        files.push({ name: '(standard input)', text: ctx.stdin || '' });
        return { files: files, errs: errs };
      }
      function walk(abs, arg) {
        var nd = lookup(fs, abs, true);
        if (!nd) { errs.push(arg + ': No such file or directory'); return; }
        if (nd.t === T.DIR) {
          if (!recursive) { errs.push(arg + ': Is a directory'); return; }
          Object.keys(nd.ch).sort(H.byName).forEach(function (n) {
            walk(normalize('/', abs + '/' + n), arg.replace(/\/+$/, '') + '/' + n);
          });
          return;
        }
        var c = H.readFile(fs, abs, nd);
        if (errText(c)) { errs.push(arg + ': ' + c.slice(1)); return; }
        files.push({ name: arg, text: c });
      }
      args.forEach(function (arg) {
        if (arg === '-') { files.push({ name: '(standard input)', text: ctx.stdin || '' }); return; }
        walk(normalize(fs.cwd, arg), arg);
      });
      return { files: files, errs: errs };
    }

    /* ---------------------------------------------------------------------
       grep
       --------------------------------------------------------------------- */
    CMD.grep = function (fs, argv, ctx) {
      var p = parseFlags(argv, {
        val: 'eABCm',
        long: { ignore_case: 'i', invert: 'v', line_number: 'n', count: 'c',
                files_with_matches: 'l', files_without: 'L', recursive: 'r',
                extended: 'E', fixed: 'F', word: 'w', only: 'o', quiet: 'q',
                no_filename: 'h', with_filename: 'H', after: 'A', before: 'B',
                context: 'C', max_count: 'm', 'color': '' }
      });
      var o = p.o;
      var pat = o.e;
      var args = p.rest.slice();
      if (pat == null) {
        if (!args.length) return bad('Usage: grep [OPTION]... PATTERNS [FILE]...');
        pat = args.shift();
      }
      var flags = 'g' + (o.i ? 'i' : '');
      var re;
      try {
        var src = o.F ? pat.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') : pat;
        if (o.w) src = '\\b(?:' + src + ')\\b';
        re = new RegExp(src, flags);
      } catch (e) {
        return bad('grep: ' + pat + ': invalid regular expression');
      }
      var recursive = !!(o.r || o.R);
      var got = collect(fs, H.expandAll(fs, args), ctx, recursive);
      var showName = o.H || (o.h ? false : got.files.length > 1 || recursive);
      var out = [], hitCount = 0, code = 1;
      var maxN = o.m ? parseInt(o.m, 10) : Infinity;

      got.files.forEach(function (f) {
        var lines = f.text.split('\n');
        if (lines[lines.length - 1] === '') lines.pop();
        var matched = 0;
        var printed = [];
        lines.forEach(function (line, i) {
          re.lastIndex = 0;
          var m = re.test(line);
          var hit = o.v ? !m : m;
          if (!hit) return;
          matched++;
          if (matched > maxN) return;
          hitCount++;
          if (o.l || o.L) return;
          if (o.c) return;
          var prefix = (showName ? f.name + ':' : '') + (o.n ? (i + 1) + ':' : '');
          if (o.o && !o.v && !o.F) {
            var mm, re2 = new RegExp(re.source, flags);
            while ((mm = re2.exec(line)) !== null) {
              if (mm[0] === '') { re2.lastIndex++; continue; }
              printed.push(prefix + mm[0]);
            }
          } else {
            printed.push(prefix + line);
          }
        });
        if (o.l && matched) out.push(f.name);
        else if (o.L && !matched) out.push(f.name);
        else if (o.c) out.push((showName ? f.name + ':' : '') + matched);
        else out = out.concat(printed);
        if (matched) code = 0;
      });

      if (o.q) return { out: '', err: got.errs.join('\n'), code: code };
      return { out: out.join('\n'), err: got.errs.join('\n'), code: code };
    };
    CMD.egrep = CMD.grep;
    CMD.fgrep = CMD.grep;

    /* ---------------------------------------------------------------------
       sed —— 只做「题库里真的会出现」的那个子集：
         s/re/repl/flags（含 s|a|b| 换分隔符）、d、p、行号与 /re/ 地址、-n、-i
       ★ 不做 a/i/c、不做 hold space、不做标签跳转。真机支持但教学里
         头两节课用不到，写了没人验证反而是负担。
       --------------------------------------------------------------------- */
    CMD.sed = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: 'e', long: { 'expression': 'e', in_place: 'i', quiet: 'n', 'regexp-extended': 'E', 'separate': 's' } });
      var o = p.o;
      var scripts = [];
      if (o.e) scripts.push(o.e);
      var args = p.rest.slice();
      if (!scripts.length) {
        if (!args.length) return bad('sed: no script specified');
        scripts.push(args.shift());
      }
      var prog = [];
      scripts.forEach(function (sc) {
        sc.split(';').forEach(function (part) {
          var t = part.trim();
          if (t) prog.push(t);
        });
      });
      var got = collect(fs, H.expandAll(fs, args), ctx, false);
      if (got.errs.length && !got.files.length) return bad('sed: ' + got.errs[0]);
      var inPlace = !!o.i;
      var outputs = [];

      got.files.forEach(function (f) {
        var lines = f.text.split('\n');
        var trailing = lines[lines.length - 1] === '';
        if (trailing) lines.pop();
        var res = [];
        lines.forEach(function (line, idx) {
          var ln = idx + 1, deleted = false, forcedPrint = false, cur = line, quit = false;
          prog.forEach(function (cmd) {
            if (deleted || quit) return;
            var addrRe = /^\/(.+?)\//.exec(cmd);
            var addrNum = /^(\d+|\$)/.exec(cmd);
            var applies = true;
            var body = cmd;
            if (addrRe) {
              applies = new RegExp(addrRe[1]).test(line);
              body = cmd.slice(addrRe[0].length).trim();
            } else if (addrNum) {
              var want = addrNum[1] === '$' ? lines.length : parseInt(addrNum[1], 10);
              applies = want === ln;
              body = cmd.slice(addrNum[0].length).trim();
            }
            if (!applies) return;
            if (body === 'd') { deleted = true; return; }
            if (body === 'p') { forcedPrint = true; return; }
            if (body === 'q') { quit = true; return; }
            if (body.charAt(0) === 's') {
              var sep = body.charAt(1);
              /* 跳过 `s` 和分隔符本身：s/a/b/ 要从索引 2 开始切，否则首段是空串 */
              var parts = splitSed(body.slice(2), sep);
              if (parts.length < 2) return;
              var g = parts[2] || '';
              var rx;
              try { rx = new RegExp(parts[0], g.indexOf('g') >= 0 ? 'g' : ''); } catch (e) { return; }
              cur = cur.replace(rx, parts[1].replace(/\\1/g, '$1').replace(/&/g, '$&'));
            }
          });
          if (deleted) return;
          if (forcedPrint) res.push(cur);
          if (!o.n) res.push(cur);
          if (quit) res.push('');
        });
        var text = res.join('\n') + (res.length ? '\n' : '');
        if (inPlace) outputs.push({ name: f.name, text: text });
        else outputs.push({ out: text });
      });

      if (inPlace) {
        /* -i：改回文件本身。题库里 `sed -i 's/a/b/' f` 出现得不少，
           所以这一步必须真的落盘，不然「改完再看」验不出来。 */
        got.files.forEach(function (f, i) {
          if (f.name === '(standard input)') return;
          var abs = normalize(fs.cwd, f.name);
          var e = H.writeFile(fs, abs, outputs[i].text, false);
          if (e) return bad('sed: cannot write ' + f.name + ': ' + e);
        });
        return ok('');
      }
      return { out: outputs.map(function (x) { return x.out; }).join(''), err: '', code: 0 };
    };

    /* s/a/b/flags 按分隔符切三段，第三段是 flag（可为空） */
    function splitSed(s, sep) {
      var out = [], cur = '', i = 0;
      while (i < s.length) {
        var ch = s[i];
        if (ch === '\\' && i + 1 < s.length) { cur += ch + s[i + 1]; i += 2; continue; }
        if (ch === sep) { out.push(cur); cur = ''; i++; continue; }
        cur += ch; i++;
      }
      out.push(cur);
      return out;
    }

    /* ---------------------------------------------------------------------
       awk —— 子集实现
       ---------------------------------------------------------------------
       支持：`-F`、`-v`、模式（/re/、表达式、BEGIN、END）、动作里的
       print / printf / 赋值（= += -= *= /= / ++ / --）/ 算术比较 /
       $n、$0、NF、NR、FNR、length()、substr()、index()、split()
       ★ 不支持 if/for/while/数组。题库里 awk 的答案清一色是
         `{print $2}` 和 `{sum+=$1} END{print sum}` 这两种形状。
       --------------------------------------------------------------------- */
    CMD.awk = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: 'Fv', long: { field_separator: 'F', assign: 'v' } });
      var o = p.o;
      var args = p.rest.slice();
      if (!args.length) return bad('usage: awk [-F fs][-v var=value][prog | -f progfile][file ...]');
      var progText = args.shift();

      var got = collect(fs, H.expandAll(fs, args), ctx, false);
      var FS = o.F != null ? String(o.F) : ' ';
      var vars = { FS: FS, OFS: ' ', ORS: '\n', NR: 0, NF: 0, FNR: 0 };
      if (o.v) {
        var eq = o.v.indexOf('=');
        if (eq > 0) vars[o.v.slice(0, eq)] = o.v.slice(eq + 1);
      }
      var out = [];

      var rules = parseAwk(progText);
      var g = { vars: vars, out: out, fields: [], line: '' };

      runBlock(rules.begin, g);

      got.files.forEach(function (f) {
        var lines = f.text.split('\n');
        if (lines[lines.length - 1] === '') lines.pop();
        vars.FNR = 0;
        lines.forEach(function (line) {
          vars.NR++;
          vars.FNR++;
          g.line = line;
          g.fields = line.split(vars.FS === ' ' ? /[ \t]+/ : new RegExp(escRe(vars.FS)));
          if (g.fields.length === 1 && g.fields[0] === '') g.fields = [];
          vars.NF = g.fields.length;
          rules.main.forEach(function (rule) {
            if (rule.pat && !evalCond(rule.pat, g)) return;
            runBlock(rule.acts, g);
          });
        });
      });

      runBlock(rules.end, g);
      return { out: out.join(''), err: got.errs.join('\n'), code: 0 };
    };

    function escRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

    /* 把 awk 程序切成 BEGIN / END / 模式+动作 三段列表 */
    function parseAwk(src) {
      var rules = { begin: [], main: [], end: [] };
      var i = 0;
      src = src.replace(/\n/g, ' ');
      while (i < src.length) {
        while (i < src.length && /\s|;/.test(src[i])) i++;
        if (i >= src.length) break;
        var pat = null, kind = 'main';
        var mBeg = /^BEGIN\s*/.exec(src.slice(i));
        var mEnd = /^END\s*/.exec(src.slice(i));
        if (mBeg) { kind = 'begin'; i += mBeg[0].length; }
        else if (mEnd) { kind = 'end'; i += mEnd[0].length; }
        else if (src[i] === '{') { /* 无模式 */ }
        else {
          /* 读模式：到 `{` 或 `;` 为止 */
          var start = i, depth = 0;
          while (i < src.length) {
            var c = src[i];
            if (c === '"') { i++; while (i < src.length && src[i] !== '"') i++; i++; continue; }
            if (c === '(') depth++;
            if (c === ')') depth--;
            if (c === '{' && depth === 0) break;
            if (c === ';' && depth === 0) break;
            i++;
          }
          pat = src.slice(start, i).trim() || null;
        }
        var acts = [];
        if (src[i] === '{') {
          var d = 0, s2 = i;
          while (i < src.length) {
            if (src[i] === '"') { i++; while (i < src.length && src[i] !== '"') i++; i++; continue; }
            if (src[i] === '{') d++;
            else if (src[i] === '}') { d--; if (d === 0) { i++; break; } }
            i++;
          }
          acts = splitStmts(src.slice(s2 + 1, i - 1));
        } else if (pat === null) {
          i++;
          continue;
        } else {
          /* 只有模式没有动作 = print $0 */
          acts = [{ t: 'print', args: ['$0'] }];
        }
        if (kind === 'begin') rules.begin = rules.begin.concat(acts);
        else if (kind === 'end') rules.end = rules.end.concat(acts);
        else rules.main.push({ pat: pat, acts: acts });
      }
      return rules;
    }

    /* 动作块里的语句切分（分号分隔，括号和引号内不切） */
    function splitStmts(body) {
      var stmts = [], cur = '', depth = 0, i = 0;
      while (i < body.length) {
        var c = body[i];
        if (c === '"') {
          cur += c; i++;
          while (i < body.length && body[i] !== '"') { cur += body[i]; i++; }
          cur += '"'; i++; continue;
        }
        if (c === '(' || c === '{') depth++;
        if (c === ')' || c === '}') depth--;
        if ((c === ';' || c === '\n') && depth === 0) { stmts.push(cur.trim()); cur = ''; i++; continue; }
        cur += c; i++;
      }
      if (cur.trim()) stmts.push(cur.trim());
      return stmts.map(function (s) { return parseStmt(s); }).filter(Boolean);
    }

    function parseStmt(s) {
      if (!s) return null;
      var mp = /^print\b\s*(.*)$/.exec(s);
      if (mp) {
        var body2 = mp[1];
        if (!body2.trim()) return { t: 'print', args: ['$0'] };
        return { t: 'print', args: splitArgs(body2) };
      }
      var mf = /^printf\b\s*(.*)$/.exec(s);
      if (mf) return { t: 'printf', args: splitArgs(mf[1]) };
      var ma = /^([A-Za-z_][A-Za-z0-9_]*|\$[0-9A-Za-z_]+)\s*([+\-*/]?=)\s*(.*)$/.exec(s);
      if (ma) {
        /* `+=` 里的 + 前面可能有空格，正则已经兜住 */
        return { t: 'assign', target: ma[1], op: ma[2], expr: ma[3] };
      }
      return { t: 'expr', expr: s };
    }

    /* 逗号分隔的参数（引号内不切） */
    function splitArgs(s) {
      var out = [], cur = '', i = 0, depth = 0;
      while (i < s.length) {
        var c = s[i];
        if (c === '"') {
          cur += c; i++;
          while (i < s.length && s[i] !== '"') { cur += s[i]; i++; }
          cur += '"'; i++; continue;
        }
        if (c === '(') depth++;
        if (c === ')') depth--;
        if (c === ',' && depth === 0) { out.push(cur.trim()); cur = ''; i++; continue; }
        cur += c; i++;
      }
      if (cur.trim()) out.push(cur.trim());
      return out;
    }

    function runBlock(stmts, g) {
      if (!stmts || !stmts.length) return;
      stmts.forEach(function (st) {
        if (!st) return;
        if (st.t === 'print') {
          var vals = st.args.map(function (a) { return toStr(evalAwk(a, g), g); });
          g.out.push(vals.join(String(g.vars.OFS)) + String(g.vars.ORS));
        } else if (st.t === 'printf') {
          var fmt = toStr(evalAwk(st.args[0], g), g);
          var rest = st.args.slice(1).map(function (a) { return evalAwk(a, g); });
          g.out.push(printf(fmt, rest));
        } else if (st.t === 'assign') {
          var v = evalAwk(st.expr, g);
          var cur = st.target.charAt(0) === '$' ? evalAwk(st.target, g) : (g.vars[st.target] || 0);
          if (st.op === '=') cur = 0;
          var nv;
          if (st.op === '=') nv = v;
          else if (st.op === '+=') nv = num(cur) + num(v);
          else if (st.op === '-=') nv = num(cur) - num(v);
          else if (st.op === '*=') nv = num(cur) * num(v);
          else nv = num(v) === 0 ? 0 : num(cur) / num(v);
          g.vars[st.target] = nv;
        }
      });
    }

    function num(v) { return typeof v === 'number' ? v : (parseFloat(v) || 0); }
    function toStr(v, g) {
      if (typeof v === 'number') {
        return Number.isInteger(v) ? String(v) : String(v);
      }
      return v == null ? '' : String(v);
    }

    function printf(fmt, vals) {
      var i = 0;
      return fmt.replace(/%(-?\d*\.?\d*)([sdifc%])/g, function (all, spec, kind) {
        if (kind === '%') return '%';
        var v = vals[i++];
        if (kind === 'd' || kind === 'i') return String(Math.trunc(num(v)));
        if (kind === 'f') {
          var dec = /\.(\d+)/.exec(spec);
          return num(v).toFixed(dec ? parseInt(dec[1], 10) : 6);
        }
        return String(v == null ? '' : v);
      });
    }

    /* 模式条件：/re/ 或任意表达式 */
    function evalCond(pat, g) {
      var m = /^\/(.+)\/$/.exec(pat.trim());
      if (m) { try { return new RegExp(m[1]).test(g.line); } catch (e) { return false; } }
      var v = evalAwk(pat, g);
      if (typeof v === 'string') return v !== '' && v !== '0';
      return !!v;
    }

    /* 表达式求值：支持 ? : 与逻辑、比较、算术、拼接、$n、变量、函数调用 */
    function evalAwk(expr, g) {
      var tokens = tokenizeAwk(String(expr));
      var pos = 0;
      function peek() { return tokens[pos]; }
      function next() { return tokens[pos++]; }

      function primary() {
        var t = next();
        if (t == null) return '';
        if (t.v === '(') { var v = ternary(); next(); return v; }
        if (t.v === '-') return -num(primary());
        if (t.v === '+') return num(primary());
        if (t.v === '!') return !truthy(primary());
        if (t.k === 'num') return parseFloat(t.v);
        if (t.k === 'str') return t.v;
        if (t.k === 'field') {
          var idx = t.v === '$0' ? 0 : parseInt(t.v.slice(1), 10);
          if (t.v === '$NF') idx = g.vars.NF;
          return idx === 0 ? g.line : (g.fields[idx - 1] == null ? '' : g.fields[idx - 1]);
        }
        if (t.k === 'func') {
          var args = [];
          next(); // (
          if (peek() && peek().v !== ')') {
            for (;;) {
              args.push(ternary());
              if (peek() && peek().v === ',') { next(); continue; }
              break;
            }
          }
          if (peek() && peek().v === ')') next();
          return callAwk(t.v, args, g);
        }
        if (t.v === 'NF' || t.v === 'NR' || t.v === 'FNR' || t.v === 'OFS' || t.v === 'ORS' || t.v === 'FS') {
          return g.vars[t.v];
        }
        return g.vars[t.v] != null ? g.vars[t.v] : '';
      }
      function muldiv() {
        var v = primary();
        while (peek() && (peek().v === '*' || peek().v === '/' || peek().v === '%')) {
          var op = next().v, r = primary();
          if (op === '*') v = num(v) * num(r);
          else if (op === '/') v = num(r) === 0 ? 0 : num(v) / num(r);
          else v = num(r) === 0 ? 0 : num(v) % num(r);
        }
        return v;
      }
      function addsub() {
        var v = muldiv();
        while (peek() && (peek().v === '+' || peek().v === '-')) {
          var op = next().v, r = muldiv();
          v = op === '+' ? num(v) + num(r) : num(v) - num(r);
        }
        return v;
      }
      function compare() {
        var v = addsub();
        while (peek() && ['<', '<=', '>', '>=', '==', '!='].indexOf(peek().v) >= 0) {
          var op = next().v, r = addsub();
          var a = num(v), b = num(r);
          var sa = String(v), sb = String(r);
          var bothNum = /^-?\d+(\.\d+)?$/.test(sa) && /^-?\d+(\.\d+)?$/.test(sb);
          var res;
          if (bothNum) {
            res = op === '<' ? a < b : op === '<=' ? a <= b : op === '>' ? a > b :
                  op === '>=' ? a >= b : op === '==' ? a === b : a !== b;
          } else {
            res = op === '<' ? sa < sb : op === '<=' ? sa <= sb : op === '>' ? sa > sb :
                  op === '>=' ? sa >= sb : op === '==' ? sa === sb : sa !== sb;
          }
          v = res ? 1 : 0;
        }
        return v;
      }
      function logic() {
        var v = compare();
        while (peek() && (peek().v === '&&' || peek().v === '||')) {
          var op = next().v, r = compare();
          v = op === '&&' ? (truthy(v) && truthy(r) ? 1 : 0) : (truthy(v) || truthy(r) ? 1 : 0);
        }
        return v;
      }
      function ternary() {
        var v = logic();
        if (peek() && peek().v === '?') {
          next();
          var a = ternary();
          if (peek() && peek().v === ':') next();
          var b = ternary();
          return truthy(v) ? a : b;
        }
        /* 相邻字符串/表达式 = 拼接（awk 的隐式 concatenation） */
        while (peek() && !['+', '-', '*', '/', '%', ')', ',', '?', ':', '&&', '||', '<', '>', '<=', '>=', '==', '!=', ']'].includes(peek().v)) {
          var nxt = peek();
          if (nxt.k === 'word' || nxt.k === 'str' || nxt.k === 'field' || nxt.k === 'func' || nxt.v === '(') {
            v = String(v) + String(primary());
          } else break;
        }
        return v;
      }
      return ternary();
    }

    function truthy(v) {
      if (typeof v === 'number') return v !== 0;
      if (v === '' || v == null) return false;
      if (/^-?\d+(\.\d+)?$/.test(v)) return parseFloat(v) !== 0;
      return true;
    }

    function callAwk(name, args, g) {
      if (name === 'length') {
        var a = args.length ? args[0] : g.line;
        return String(a).length;
      }
      if (name === 'substr') {
        var s = String(args[0]), st = num(args[1]) | 0, len = args.length > 2 ? num(args[2]) | 0 : undefined;
        var begin = st > 0 ? st - 1 : 0;
        return len == null ? s.slice(begin) : s.substr(begin, len);
      }
      if (name === 'index') {
        return String(args[0]).indexOf(String(args[1])) + 1;
      }
      if (name === 'toupper') return String(args[0]).toUpperCase();
      if (name === 'tolower') return String(args[0]).toLowerCase();
      if (name === 'int') return Math.trunc(num(args[0]));
      if (name === 'split') {
        var str = String(args[0]), fs = args.length > 1 ? String(args[1]) : g.vars.FS;
        var parts = str.split(fs === ' ' ? /[ \t]+/ : new RegExp(escRe(fs)));
        return parts.length;
      }
      return '';
    }

    function tokenizeAwk(s) {
      var out = [], i = 0;
      while (i < s.length) {
        var c = s[i];
        if (/\s/.test(c)) { i++; continue; }
        if (c === '"') {
          var j = i + 1, buf = '';
          while (j < s.length && s[j] !== '"') {
            if (s[j] === '\\' && j + 1 < s.length) {
              var nx = s[j + 1];
              buf += nx === 'n' ? '\n' : nx === 't' ? '\t' : nx;
              j += 2; continue;
            }
            buf += s[j]; j++;
          }
          out.push({ k: 'str', v: buf }); i = j + 1; continue;
        }
        var m3 = /^(\$[A-Za-z_][A-Za-z0-9_]*|\$\d+)/.exec(s.slice(i));
        if (m3) { out.push({ k: 'field', v: m3[1] }); i += m3[1].length; continue; }
        var m2 = /^(-?\d+(?:\.\d+)?)/.exec(s.slice(i));
        if (m2) { out.push({ k: 'num', v: m2[1] }); i += m2[1].length; continue; }
        var mf = /^([A-Za-z_][A-Za-z0-9_]*)\s*\(/.exec(s.slice(i));
        if (mf) { out.push({ k: 'func', v: mf[1] }); i += mf[1].length; continue; }
        var mw = /^[A-Za-z_][A-Za-z0-9_]*/.exec(s.slice(i));
        if (mw) { out.push({ k: 'word', v: mw[0] }); i += mw[0].length; continue; }
        var two = s.substr(i, 2);
        if (['<=', '>=', '==', '!=', '&&', '||', '++', '--'].indexOf(two) >= 0) {
          out.push({ k: 'op', v: two }); i += 2; continue;
        }
        out.push({ k: 'op', v: c }); i++;
      }
      return out;
    }

    /* ---------------------------------------------------------------------
       sort / uniq / cut / tr / paste / comm / diff / expand / tee
       --------------------------------------------------------------------- */
    function readLines(fs, args, ctx) {
      var got = collect(fs, H.expandAll(fs, args), ctx, false);
      var text = got.files.map(function (f) { return f.text; }).join('');
      var lines = text.split('\n');
      if (lines[lines.length - 1] === '') lines.pop();
      return { lines: lines, errs: got.errs };
    }

    CMD.sort = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: 'kto', long: { numeric: 'n', reverse: 'r', unique: 'u', 'field-separator': 't', key: 'k', human: 'h', month: 'M', version: 'V' } });
      var o = p.o;
      var r = readLines(fs, p.rest, ctx);
      var lines = r.lines.slice();
      var sep = o.t || null;
      var keyIdx = 0;
      if (o.k) keyIdx = parseInt(o.k, 10) - 1;
      function key(l) {
        var parts = sep ? l.split(sep) : l.trim().split(/\s+/);
        return parts[keyIdx] == null ? '' : parts[keyIdx];
      }
      lines.sort(function (a, b) {
        var ka = o.k ? key(a) : a, kb = o.k ? key(b) : b;
        if (o.n) {
          var na = parseFloat(ka.replace(/[^\d.\-]/g, '')), nb = parseFloat(kb.replace(/[^\d.\-]/g, ''));
          if (isNaN(na)) na = 0;
          if (isNaN(nb)) nb = 0;
          if (na !== nb) return na - nb;
          return a < b ? -1 : a > b ? 1 : 0;
        }
        return ka < kb ? -1 : ka > kb ? 1 : 0;
      });
      if (o.r) lines.reverse();
      if (o.u) {
        var seen = {};
        lines = lines.filter(function (l) { if (seen[l]) return false; seen[l] = 1; return true; });
      }
      return ok(lines.join('\n') + (lines.length ? '\n' : ''));
    };

    CMD.uniq = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: '', long: { count: 'c', repeated: 'd', unique: 'u', ignore_case: 'i' } });
      var o = p.o;
      var r = readLines(fs, p.rest, ctx);
      var out = [], prev = null, n = 0;
      var src = r.lines.concat([' ']);
      src.forEach(function (l) {
        var cmp = o.i ? l.toLowerCase() : l;
        var pv = prev === null ? null : (o.i ? prev.toLowerCase() : prev);
        if (pv !== null && cmp === pv) { n++; return; }
        if (prev !== null) push(prev, n);
        prev = l; n = 1;
      });
      function push(l, c) {
        if (l === ' ') return;
        if (o.d && c < 2) return;
        if (o.u && c > 1) return;
        out.push(o.c ? String(c).padStart(7) + ' ' + l : l);
      }
      return ok(out.join('\n') + (out.length ? '\n' : ''));
    };

    CMD.cut = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: 'dfc', long: { delimiter: 'd', fields: 'f', characters: 'c', only_delimited: 's' } });
      var o = p.o;
      if (!o.f && !o.c) return bad('cut: you must specify a list of bytes, characters, or fields');
      var r = readLines(fs, p.rest, ctx);
      var fields = [];
      var spec = o.f || o.c;
      spec.split(',').forEach(function (seg) {
        var m = /^(\d+)-(\d*)$/.exec(seg);
        if (m) {
          var b = parseInt(m[1], 10), e = m[2] ? parseInt(m[2], 10) : b;
          for (var i = b; i <= e; i++) fields.push(i);
        } else if (/^\d+$/.test(seg)) fields.push(parseInt(seg, 10));
      });
      var out = r.lines.map(function (l) {
        if (o.c) {
          return fields.map(function (i) { return l.charAt(i - 1); }).join('');
        }
        if (!o.d && l.indexOf('\t') < 0) {
          if (o.s) return null;
          return l;
        }
        var parts = o.d ? l.split(o.d) : l.split('\t');
        if (o.s && parts.length === 1) return null;
        return fields.map(function (i) { return parts[i - 1] == null ? '' : parts[i - 1]; }).join(o.d || '\t');
      }).filter(function (x) { return x !== null; });
      return ok(out.join('\n') + (out.length ? '\n' : ''));
    };

    CMD.tr = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: '', long: { delete: 'd', squeeze: 's', complement: 'c' } });
      var o = p.o;
      var args = p.rest;
      var set1 = expandSet(args[0] || ''), set2 = expandSet(args[1] || '');
      var text = ctx.stdin || '';
      if (!p.rest.length) return bad('tr: missing operand');
      if (o.d) {
        var del = {};
        set1.forEach(function (c) { del[c] = 1; });
        text = text.split('').filter(function (c) {
          return o.c ? !del[c] : !del[c];
        }).join('');
      } else if (set2.length) {
        text = text.split('').map(function (c) {
          var i = set1.indexOf(c);
          if (i < 0) return c;
          return set2[Math.min(i, set2.length - 1)];
        }).join('');
      }
      if (o.s) {
        var sq = set2.length ? set2 : set1;
        if (sq.length === 1) text = text.split(sq[0] + sq[0]).join(sq[0]);
      }
      return ok(text);
    };

    /* tr 的 a-z / [:upper:] / 转义 */
    function expandSet(s) {
      var out = [], i = 0;
      var named = { '[:upper:]': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', '[:lower:]': 'abcdefghijklmnopqrstuvwxyz',
                    '[:digit:]': '0123456789', '[:space:]': ' \t\n', '[:alpha:]': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' };
      for (var k in named) s = s.split(k).join(named[k]);
      while (i < s.length) {
        if (s[i] === '\\' && i + 1 < s.length) {
          var nx = s[i + 1];
          out.push(nx === 'n' ? '\n' : nx === 't' ? '\t' : nx);
          i += 2; continue;
        }
        if (s[i + 1] === '-' && s[i + 2] != null) {
          var a = s.charCodeAt(i), b = s.charCodeAt(i + 2);
          for (var c = a; c <= b; c++) out.push(String.fromCharCode(c));
          i += 3; continue;
        }
        out.push(s[i]); i++;
      }
      return out;
    }

    CMD.paste = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: 'd', long: { delimiters: 'd', serial: 's' } });
      var d = p.o.d == null ? '\t' : p.o.d;
      var cols = p.rest.map(function (name) {
        var abs = normalize(fs.cwd, name);
        var c = H.readFile(fs, abs, lookup(fs, abs, true));
        var lines = c.split('\n');
        if (lines[lines.length - 1] === '') lines.pop();
        return lines;
      });
      if (p.o.s) {
        return ok(cols.map(function (l) { return l.join(d); }).join('\n') + '\n');
      }
      var max = Math.max.apply(null, cols.map(function (c) { return c.length; }).concat([0]));
      var out = [];
      for (var i = 0; i < max; i++) {
        out.push(cols.map(function (c) { return c[i] == null ? '' : c[i]; }).join(d));
      }
      return ok(out.join('\n') + (out.length ? '\n' : ''));
    };

    CMD.comm = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: '', long: {} });
      if (p.rest.length < 2) return bad('comm: missing operand');
      var a = readOne(fs, p.rest[0]).split('\n').filter(Boolean);
      var b = readOne(fs, p.rest[1]).split('\n').filter(Boolean);
      var out = [], i = 0, j = 0;
      var sup1 = p.o['1'], sup2 = p.o['2'], sup3 = p.o['3'];
      while (i < a.length || j < b.length) {
        if (i >= a.length) { if (!sup3) out.push((!sup1 ? '\t' : '') + (!sup2 ? '\t' : '') + b[j]); j++; continue; }
        if (j >= b.length) { if (!sup2) out.push((!sup1 ? '' : '\t') + a[i]); i++; continue; }
        if (a[i] === b[j]) { if (!sup1 && !sup2) out.push((!sup3 ? '\t\t' : '') + a[i]); i++; j++; }
        else if (a[i] < b[j]) { if (!sup2) out.push(a[i]); i++; }
        else { if (!sup1) out.push((!sup2 ? '' : '\t') + b[j]); j++; }
      }
      function readOne(name) {
        var abs = normalize(fs.cwd, name);
        var c = H.readFile(fs, abs, lookup(fs, abs, true));
        return errText(c) ? '' : c;
      }
      return ok(out.join('\n') + (out.length ? '\n' : ''));
    };

    CMD.diff = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: 'UC', long: { unified: 'u', context: 'C' } });
      if (p.rest.length < 2) return bad('diff: missing operand after \'' + (p.rest[0] || '') + '\'');
      var A = readOne(p.rest[0]).split('\n').filter(function (l, i, arr) { return !(i === arr.length - 1 && l === ''); });
      var B = readOne(p.rest[1]).split('\n').filter(function (l, i, arr) { return !(i === arr.length - 1 && l === ''); });
      function readOne(name) {
        if (name === '-') return '';
        var abs = normalize(fs.cwd, name);
        var c = H.readFile(fs, abs, lookup(fs, abs, true));
        return errText(c) ? '' : c;
      }
      if (A.join('\n') === B.join('\n')) return ok('');
      var out = [];
      out.push('--- ' + p.rest[0]);
      out.push('+++ ' + p.rest[1]);
      /* 极简 LCS：够看「差在哪一行」，不追求 GNU diff 的最小编辑脚本 */
      var n = A.length, m = B.length;
      var dp = [];
      for (var i = 0; i <= n; i++) { dp.push(new Array(m + 1).fill(0)); }
      for (var i2 = n - 1; i2 >= 0; i2--) {
        for (var j2 = m - 1; j2 >= 0; j2--) {
          dp[i2][j2] = A[i2] === B[j2] ? dp[i2 + 1][j2 + 1] + 1 : Math.max(dp[i2 + 1][j2], dp[i2][j2 + 1]);
        }
      }
      var ii = 0, jj = 0;
      while (ii < n && jj < m) {
        if (A[ii] === B[jj]) { out.push(' ' + A[ii]); ii++; jj++; }
        else if (dp[ii + 1][jj] >= dp[ii][jj + 1]) { out.push('-' + A[ii]); ii++; }
        else { out.push('+' + B[jj]); jj++; }
      }
      while (ii < n) { out.push('-' + A[ii]); ii++; }
      while (jj < m) { out.push('+' + B[jj]); jj++; }
      return ok(out.join('\n') + '\n');
    };

    CMD.expand = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: 't', long: { tabs: 't' } });
      var w = parseInt(p.o.t || 8, 10);
      var text = p.rest.length ? readOne2(fs, p.rest[0]) : (ctx.stdin || '');
      function readOne2(fs2, name) {
        var abs = normalize(fs2.cwd, name);
        var c = H.readFile(fs2, abs, lookup(fs2, abs, true));
        return errText(c) ? '' : c;
      }
      return ok(text.split('\n').map(function (l) {
        var col = 0, o2 = '';
        for (var i = 0; i < l.length; i++) {
          if (l[i] === '\t') { var add = w - (col % w); o2 += ' '.repeat(add); col += add; }
          else { o2 += l[i]; col++; }
        }
        return o2;
      }).join('\n'));
    };

    CMD.tee = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: '', long: { append: 'a' } });
      var text = ctx.stdin || '';
      var errs = [];
      var outs = [];
      p.rest.forEach(function (arg) {
        var abs = normalize(fs.cwd, arg);
        var e = H.writeFile(fs, abs, text, !!p.o.a);
        if (e) errs.push('tee: ' + arg + ': ' + e);
        else outs.push(text);
      });
      return { out: text, err: errs.join('\n'), code: errs.length ? 1 : 0 };
    };

    /* ---------------------------------------------------------------------
       find
       --------------------------------------------------------------------- */
    CMD.find = function (fs, argv, ctx) {
      var start = [], i = 0;
      /* 前导路径：不是以 - 或 ( 或 ! 开头的都算起点 */
      while (i < argv.length && argv[i].charAt(0) !== '-' && argv[i] !== '(' && argv[i] !== '!') {
        start.push(argv[i]); i++;
      }
      if (!start.length) start = ['.'];
      var expr = argv.slice(i);

      var out = [], errs = [];
      var maxDepth = null, minDepth = 0;

      /* 先把表达式拆成「测试项」链表，方便 -o / ! 组合。这里只做
         「项 → 谓词函数」的线性组合，用 -o 时按「或」处理。 */
      var ors = [[]];
      var neg = false;
      var execIdx = -1;

      for (var k = 0; k < expr.length; k++) {
        var a = expr[k];
        if (a === '-o' || a === '-or') { ors.push([]); continue; }
        if (a === '-a' || a === '-and') continue;
        if (a === '!' || a === '-not') { neg = !neg; continue; }
        var item = { op: a, val: expr[k + 1], neg: neg };
        neg = false;
        /* ★ -exec 不在这里：它的「参数」是子命令本身，通用的「吃掉一个
           参数」会把子命令名一起吃掉，于是 `-exec cat {} \;` 变成只剩 `{}`。 */
        if (['-name', '-iname', '-type', '-size', '-mtime', '-mmin', '-perm', '-user', '-group',
             '-newer', '-path', '-maxdepth', '-mindepth', '-printf'].indexOf(a) >= 0) k++;
        if (a === '-exec') {
          /* 收集到 \; 或 + 为止 */
          var sub = [];
          k++;
          while (k < expr.length && expr[k] !== ';' && expr[k] !== '+') { sub.push(expr[k]); k++; }
          item.sub = sub;
        }
        if (a === '-maxdepth') maxDepth = parseInt(item.val, 10);
        if (a === '-mindepth') minDepth = parseInt(item.val, 10);
        ors[ors.length - 1].push(item);
      }

      function matchType(nd, want) {
        if (want === 'f') return nd.t === T.FILE;
        if (want === 'd') return nd.t === T.DIR;
        if (want === 'l') return nd.t === T.LINK;
        return true;
      }

      function sizeOk(nd, spec) {
        var m = /^([+-]?)(\d+)([ckMG]?)$/.exec(spec);
        if (!m) return false;
        var unit = { c: 1, k: 1024, M: 1024 * 1024, G: 1024 * 1024 * 1024, '': 512 }[m[3]];
        var want = parseInt(m[2], 10) * unit;
        var size = nd.t === T.DIR ? 4096 : (nd.c || '').length;
        if (unit === 512) { want = parseInt(m[2], 10) * 512; size = Math.ceil(size / 512) * 512; }
        if (m[1] === '+') return size > want;
        if (m[1] === '-') return size < want;
        return Math.floor(size / unit) === parseInt(m[2], 10);
      }

      function permOk(nd, spec) {
        if (/^[0-7]{3,4}$/.test(spec)) return (nd.m & 0o7777) === parseInt(spec, 8);
        var m = /^([ugoa]*)([+\-=])([rwx]+)$/.exec(spec);
        if (!m) return false;
        var bits = 0;
        (m[3].indexOf('r') >= 0) && (bits |= 4);
        (m[3].indexOf('w') >= 0) && (bits |= 2);
        (m[3].indexOf('x') >= 0) && (bits |= 1);
        var shifts = m[1].indexOf('u') >= 0 ? [6] : m[1].indexOf('g') >= 0 ? [3] : m[1].indexOf('o') >= 0 ? [0] : [6, 3, 0];
        return shifts.every(function (s) { return ((nd.m >> s) & 7) === bits; });
      }

      function testItem(item, nd, abs, name, depth) {
        var v;
        switch (item.op) {
          case '-name': v = H.globMatch(name, item.val, true); break;
          case '-iname': v = H.globMatch(name.toLowerCase(), String(item.val).toLowerCase(), true); break;
          case '-path': v = H.globMatch(abs, item.val, true); break;
          case '-type': v = matchType(nd, item.val); break;
          case '-size': v = sizeOk(nd, item.val); break;
          case '-mtime':
          case '-mmin': v = true; break;     // 时间全固定，按「都算匹配」处理
          case '-perm': v = permOk(nd, item.val); break;
          case '-user': v = (core.userNameOf(fs, nd.u) || '') === item.val; break;
          case '-group': v = (core.groupNameOf(fs, nd.g) || '') === item.val; break;
          case '-empty': v = nd.t === T.DIR ? !Object.keys(nd.ch).length : !(nd.c || '').length; break;
          case '-print': v = true; break;
          case '-print0': v = true; break;
          case '-delete': v = true; break;
          case '-exec':
          case '-printf': v = true; break;
          case '-maxdepth':
          case '-mindepth': v = true; break;
          default: v = true;
        }
        return item.neg ? !v : v;
      }

      /* 找到 -exec / -delete / -print0 就走特殊出口 */
      var hasExec = ors.some(function (g) { return g.some(function (it) { return it.op === '-exec'; }); });
      var hasDelete = ors.some(function (g) { return g.some(function (it) { return it.op === '-delete'; }); });
      var hasPrint0 = ors.some(function (g) { return g.some(function (it) { return it.op === '-print0'; }); });

      function walk(abs, name, depth) {
        var nd = lookup(fs, abs, true);
        if (!nd) return;
        var hit = depth >= minDepth && ors.some(function (grp) {
          return grp.every(function (it) { return testItem(it, nd, abs, name, depth); });
        });

        if (hit) {
          var execItem = null;
          ors.forEach(function (grp) {
            grp.forEach(function (it) { if (it.op === '-exec') execItem = it; });
          });
          if (hasDelete) {
            var r = locate(fs, abs);
            if (r.parent && r.node) delete r.parent.ch[r.name];
            return;
          }
          if (execItem && execItem.sub) {
            var subArgs = execItem.sub.map(function (a) { return a === '{}' ? abs : a; });
            /* `-exec ls -l {} \;` 里的 {} 被替换成真实路径，
               子命令交给主控去执行（这样 `-exec rm {} \;` 才真的会删） */
            var r2 = ctx.exec ? ctx.exec(subArgs) : null;
            if (r2) {
              if (r2.out) out.push(r2.out.replace(/\n$/, ''));
              if (r2.err) errs.push(r2.err.replace(/\n$/, ''));
            }
          } else if (hasPrint0) {
            out.push(abs);
          } else {
            out.push(abs);
          }
        }

        if (isDir(nd) && (maxDepth == null || depth < maxDepth)) {
          Object.keys(nd.ch).sort(H.byName).forEach(function (n) {
            walk(normalize('/', abs + '/' + n), n, depth + 1);
          });
        }
      }

      start.forEach(function (s) {
        var abs = normalize(fs.cwd, s);
        var nd = lookup(fs, abs, true);
        if (!nd) { errs.push("find: '" + s + "': No such file or directory"); return; }
        walk(abs, s === '.' ? '.' : abs.replace(/^.*\//, ''), 0);
      });

      return { out: out.join(hasPrint0 ? '\0' : '\n'), err: errs.join('\n'), code: errs.length ? 1 : 0 };
    };

    /* ---------------------------------------------------------------------
       which / whereis / type / locate / xargs
       --------------------------------------------------------------------- */
    var BUILTIN_PATHS = ['/usr/bin/', '/usr/local/bin/', '/bin/'];

    CMD.which = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { all: 'a' } });
      var out = [], code = 1;
      p.rest.forEach(function (name) {
        var dirs = (fs.env.PATH || '').split(':');
        var found = null;
        for (var i = 0; i < dirs.length && !found; i++) {
          var abs = normalize('/', dirs[i] + '/' + name);
          var nd = lookup(fs, abs, true);
          if (nd && nd.t === T.FILE && (nd.m & 0o111)) found = abs;
        }
        /* 沙箱里没为每条命令都建 ELF 文件，但「命令存在」这件事必须成立，
           否则 which ls 报 not found 就太假了。 */
        if (!found && CMD[name]) found = '/usr/bin/' + name;
        if (found) { out.push(found); code = 0; }
      });
      return { out: out.join('\n'), err: '', code: code };
    };

    CMD.type = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: {} });
      var out = [];
      p.rest.forEach(function (name) {
        if (fs.aliases && fs.aliases[name]) { out.push(name + " is aliased to `" + fs.aliases[name] + "'"); return; }
        if (['cd', 'exit', 'export', 'alias', 'unset', 'source', 'history', 'jobs', 'fg', 'bg'].indexOf(name) >= 0) {
          out.push(name + ' is a shell builtin'); return;
        }
        var r = CMD.which(fs, [name]);
        if (r.code === 0) out.push(name + ' is ' + r.out.trim());
        else out.push('bash: type: ' + name + ': not found');
      });
      return ok(out.join('\n'));
    };

    CMD.whereis = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { binary: 'b', manual: 'm', source: 's' } });
      var out = [];
      p.rest.forEach(function (name) {
        var r = CMD.which(fs, [name]);
        if (r.code === 0) out.push(name + ': ' + r.out.trim());
        else out.push(name + ':');
      });
      return ok(out.join('\n'));
    };

    CMD.locate = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { ignore_case: 'i' } });
      if (!p.rest.length) return bad('locate: no pattern to search for specified');
      var pat = p.rest[0];
      var out = [];
      (function walk(abs) {
        var nd = lookup(fs, abs, true);
        if (!nd || nd.t !== T.DIR) return;
        Object.keys(nd.ch).forEach(function (n) {
          var child = abs === '/' ? '/' + n : abs + '/' + n;
          var cmp = p.o.i ? child.toLowerCase() : child;
          var needle = p.o.i ? pat.toLowerCase() : pat;
          if (cmp.indexOf(needle) >= 0) out.push(child);
          if (nd.ch[n].t === T.DIR) walk(child);
        });
      })('/');
      if (!out.length) return { out: '', err: 'locate: can not stat () `/var/lib/mlocate/mlocate.db\': No such file or directory', code: 1 };
      return ok(out.sort().join('\n'));
    };

    CMD.xargs = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: 'nId', long: { max_args: 'n', 'replace': 'I' } });
      var cmdv = p.rest.length ? p.rest : ['echo'];
      var items = (ctx.stdin || '').split(/\s+/).filter(Boolean);
      if (!items.length) return ok('');
      var out = [], err = '', code = 0;
      var n = p.o.n ? parseInt(p.o.n, 10) : items.length;
      for (var i = 0; i < items.length; i += n) {
        var chunk = items.slice(i, i + n);
        var call = cmdv.concat(chunk);
        if (p.o.I) call = cmdv.map(function (a) { return a.split(p.o.I).join(chunk.join(' ')); });
        var r = ctx.exec ? ctx.exec(call) : ok('');
        if (r.out) out.push(r.out.replace(/\n$/, ''));
        if (r.err) err += r.err;
        if (r.code) code = r.code;
      }
      return { out: out.join('\n'), err: err, code: code };
    };

    return CMD;
  }

  return { install: install };
});
