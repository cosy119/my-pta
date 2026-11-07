/* ===========================================================================
   Linux 命令沙箱 · 第 2 层：文件与目录类命令
   ---------------------------------------------------------------------------
   安装方式：LinuxShellFsCmds.install(core, CMD) 往共享命令表里塞。

   ★ 这一层的原则：**能真改就真改**。
     mkdir/cp/mv/rm/chmod 之后，后续 ls/cat 看到的结果必须跟着变 —— 否则
     学生「先做一步再验证」的学习回路就断了，沙箱也就退化成动画片。
     凡是做不到真实现的（进程、网络、包管理）都放在 sys-cmds 里并明说是模拟。
   =========================================================================== */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.LinuxShellFsCmds = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  function install(core, CMD) {
    var T = core.T;
    var normalize = core.normalize, lookup = core.lookup, locate = core.locate;
    var modeString = core.modeString, permitted = core.permitted;
    var userNameOf = core.userNameOf, groupNameOf = core.groupNameOf;

    /* ---------------------------------------------------------------------
       小工具
       --------------------------------------------------------------------- */

    function ok(out) { return { out: out == null ? '' : out, err: '', code: 0 }; }
    function bad(err, code) { return { out: '', err: err, code: code == null ? 1 : code }; }
    function res(o) { return o; }

    function isDir(nd) { return nd && nd.t === T.DIR; }

    /* 目录项的「大小」：真机是块设备分配量，这里按条目数估一个稳定值，
       免得同一个目录每次刷新 size 都变。 */
    function dirSize(nd) {
      var n = Object.keys(nd.ch || {}).length;
      return 4096 + n * 0;          // 看着像真机：目录恒 4096
    }

    function nlink(nd) {
      if (!isDir(nd)) return 1;
      var d = 2;
      for (var k in nd.ch) if (nd.ch[k].t === T.DIR) d++;
      return d;
    }

    /* `ls -l` 的时间列：固定时钟，两个月份英文缩写拼法跟 ls 一致 */
    var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    function fmtTime(sec) {
      var d = new Date((sec || core.BASE_TIME) * 1000);
      var pad = function (n) { return n < 10 ? '0' + n : '' + n; };
      return MON[d.getUTCMonth()] + ' ' + (d.getUTCDate() < 10 ? ' ' : '') + d.getUTCDate() +
             ' ' + pad(d.getUTCHours()) + ':' + pad(d.getUTCMinutes());
    }

    function sizeText(nd, human) {
      var s = isDir(nd) ? dirSize(nd) : (nd.c || '').length;
      if (!human) return String(s);
      if (s < 1024) return String(s);
      var u = ['K', 'M', 'G', 'T'], i = -1, v = s;
      while (v >= 1024 && i < 3) { v /= 1024; i++; }
      return (v >= 10 ? Math.round(v) : Math.round(v * 10) / 10) + u[i];
    }

    /* 名字排序：C locale 的朴素质序（大写在小写前）。真机默认 locale 排序
       会忽略点和大小写，取朴素质序更好预期。 */
    function byName(a, b) { return a < b ? -1 : a > b ? 1 : 0; }

    /* `-t` 用：时间相同就退回按名，保证输出稳定 */
    function byTime(a, b, ch) {
      var d = (ch[b].mt || 0) - (ch[a].mt || 0);
      return d || byName(a, b);
    }

    /* 只展开最后一段的通配符。像 `/etX/hosts` 这种中间段通配真机支持，
       但题库里没出现过，不做 —— 做了反而容易出意外匹配。 */
    function hasGlob(s) { return /[*?\[]/.test(s); }

    /* 正则元字符逐字符转义。用字符串查表而不用 replace 正则 —— 那个
       字符类里同时要塞 `[` `]` `\` 和 `${}`，写出来极易踩解析坑。 */
    var META = '\\^$.[]|()*+?{}';
    function reEsc(c) { return META.indexOf(c) >= 0 ? '\\' + c : c; }

    function globMatch(name, pat, showHidden) {
      if (name.charAt(0) === '.' && !showHidden && pat.charAt(0) !== '.') return false;
      var re = '^';
      for (var i = 0; i < pat.length; i++) {
        var c = pat[i];
        if (c === '*') re += '[^/]*';
        else if (c === '?') re += '[^/]';
        else re += reEsc(c);
      }
      re += '$';
      try { return new RegExp(re).test(name); } catch (e) { return false; }
    }

    /* 把 argv 里的路径参数展开成真实存在的条目；没匹配上原样保留
       （这样命令自己会报 "No such file or directory"，跟 bash 一样） */
    function expandPath(fs, arg) {
      if (!hasGlob(arg)) return [arg];
      var abs = normalize(fs.cwd, arg);
      var slash = abs.lastIndexOf('/');
      var dirAbs = slash === 0 ? '/' : abs.slice(0, slash);
      var pat = abs.slice(slash + 1);
      var d = lookup(fs, dirAbs, true);
      if (!isDir(d)) return [arg];
      var hits = Object.keys(d.ch).filter(function (n) {
        return globMatch(n, pat, arg.charAt(0) === '.' || arg.indexOf('/.') >= 0);
      }).sort(byName);
      if (!hits.length) return [arg];
      var prefix = arg.slice(0, arg.length - pat.length);
      return hits.map(function (n) { return prefix + n; });
    }

    function expandAll(fs, args) {
      var out = [];
      for (var i = 0; i < args.length; i++) out = out.concat(expandPath(fs, args[i]));
      return out;
    }

    /* 读文件：返回内容或错误串（用 '!' 开头标记是错误） */
    function readFile(fs, abs, nd) {
      if (!nd) return '!No such file or directory';
      if (nd.t === T.DIR) return '!Is a directory';
      if (!permitted(fs, nd, 'r')) return '!Permission denied';
      return nd.c || '';
    }

    function writeFile(fs, abs, text, append) {
      var r = locate(fs, abs);
      /* ★ sink 要在父目录权限之前判：/dev 是 root 拥有的 0755，
         先查父目录写权限的话 `2>/dev/null` 会被判成 Permission denied。 */
      if (r.node && r.node.sink) return null;
      if (!r.parent) return 'No such file or directory';
      if (!permitted(fs, r.parent, 'w')) return 'Permission denied';
      if (r.node && r.node.t === T.DIR) return 'Is a directory';
      if (r.node) {
        if (!permitted(fs, r.node, 'w')) return 'Permission denied';
        r.node.c = append ? (r.node.c || '') + text : text;
        r.node.mt = fs.clock || core.BASE_TIME;
      } else {
        r.parent.ch[r.name] = core.file(text, 0o644, fs.uid, fs.gid);
        r.parent.ch[r.name].mt = fs.clock || core.BASE_TIME;
      }
      return null;
    }

    /* 短选项簇解析：`-la` ≡ `-l -a`；带值的 `-n5` / `-n 5` 都认 */
    function parseFlags(argv, spec) {
      var val = (spec && spec.val) || '', long = (spec && spec.long) || {};
      var o = {}, rest = [], i = 0;
      while (i < argv.length) {
        var a = argv[i];
        if (a === '--') { for (var k = i + 1; k < argv.length; k++) rest.push(argv[k]); break; }
        if (a.length > 1 && a.charAt(0) === '-') {
          if (a.slice(0, 2) === '--') {
            var eq = a.indexOf('=');
            var nm = eq > 0 ? a.slice(2, eq) : a.slice(2);
            var mp = long[nm];
            if (mp) {
              if (val.indexOf(mp) >= 0) o[mp] = eq > 0 ? a.slice(eq + 1) : argv[++i];
              else o[mp] = true;
            }
            i++; continue;
          }
          var j = 1;
          while (j < a.length) {
            var ch = a.charAt(j);
            if (val.indexOf(ch) >= 0) {
              var v = a.slice(j + 1);
              if (!v) v = argv[++i];
              o[ch] = v;
              j = a.length;
            } else { o[ch] = true; j++; }
          }
          i++; continue;
        }
        rest.push(a); i++;
      }
      return { o: o, rest: rest };
    }

    /* -l 的权限串 + SELinux 尾点 */
    function modeFull(nd) {
      var s;
      if (nd.t === T.DIR) s = 'd' + modeString(nd.m).slice(1);
      else if (nd.t === T.LINK) s = 'l' + modeString(0o777).slice(1);
      else s = modeString(nd.m);
      return s + '.';
    }

    function nameOf(nd, entryName, slash) {
      if (nd.t === T.LINK) return entryName + (slash ? '@' : '');
      if (nd.t === T.DIR) return entryName + (slash ? '/' : '');
      if (nd.m & 0o111) return entryName + (slash ? '*' : '');
      return entryName;
    }

    /* 多列排版：像真机 ls 那样按列优先填 */
    function columns(names, width) {
      width = width || 80;
      var maxw = 0;
      for (var i = 0; i < names.length; i++) maxw = Math.max(maxw, names[i].length);
      var perCol = Math.floor(width / (maxw + 2)) || 1;
      var rows = Math.ceil(names.length / perCol);
      var lines = [];
      for (var r = 0; r < rows; r++) {
        var line = '';
        for (var c = 0; c < perCol; c++) {
          var idx = c * rows + r;
          if (idx >= names.length) break;
          var s = names[idx];
          if (c < perCol - 1 && idx + rows < names.length) {
            while (s.length < maxw + 2) s += ' ';
          }
          line += s;
        }
        lines.push(line.replace(/\s+$/, ''));
      }
      return lines.join('\n');
    }

    /* ---------------------------------------------------------------------
       ls
       --------------------------------------------------------------------- */
    CMD.ls = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: '', long: { all: 'a', almost: 'A', long: 'l', directory: 'd', recursive: 'R', reverse: 'r', human: 'h', classify: 'F', inode: 'i', 'one-per-line': '1', size: 'S', time: 't' } });
      var o = p.o, args = expandAll(fs, p.rest);
      var showHidden = !!(o.a || o.A), dotDirs = !!o.a;
      var lines = [];

      /* 无参数 = 当前目录 */
      var targets = args.length ? args : ['.'];
      var multi = targets.length > 1;
      var first = true;

      function listOne(absArg) {
        var abs = normalize(fs.cwd, absArg);
        var nd = lookup(fs, abs, true);
        if (!nd) { ctx.err.push("ls: cannot access '" + absArg + "': No such file or directory"); return; }
        if (nd.t !== T.DIR || o.d) {
          /* 非目录参数按原样打印（真机行为：`ls /etc/hostname` 打全路径） */
          if (o.l) lines.push(longRow(fs, nd, absArg));
          else if (o.i) lines.push(String(inodeOf(fs, nd, absArg)).padStart(7) + ' ' + absArg);
          else lines.push(absArg);
          return;
        }
        var names = Object.keys(nd.ch).filter(function (n) {
          if (n === '.' || n === '..') return false;
          return showHidden || n.charAt(0) !== '.';
        });
        if (dotDirs) names.unshift('.', '..');
        names.sort(o.t ? function (a, b) { return byTime(a, b, nd.ch); } : byName);
        if (o.r) names.reverse();
        if (o.S) names.sort(function (a, b) { return ((nd.ch[b] || {}).c || '').length - ((nd.ch[a] || {}).c || '').length; });

        var head = '';
        if (multi) head = (first ? '' : '\n') + absArg + ':';
        first = false;

        if (o.l) {
          var body = ['total ' + (Math.ceil(names.filter(function (n) { return nd.ch[n]; }).length / 2) * 4)];
          names.forEach(function (n) {
            var ch = n === '.' || n === '..' ? nd : nd.ch[n];
            if (!ch) return;
            body.push(longRow(fs, ch, n));
          });
          lines.push((head ? head + '\n' : '') + body.join('\n'));
          if (o.R) recurse(abs, nd, names);
          return;
        }

        var shown = names.map(function (n) {
          var ch = n === '.' || n === '..' ? nd : nd.ch[n];
          var nm = o.F ? nameOf(ch, n, true) : n;
          return o.i ? String(inodeOf(fs, ch, n)).padStart(7) + ' ' + nm : nm;
        });
        var text = (o['1'] || !ctx.tty || ctx.piped) ? shown.join('\n') : columns(shown, ctx.width || 80);
        lines.push((head ? head + '\n' : '') + text);
        if (o.R) recurse(abs, nd, names);
      }

      function recurse(abs, nd, names) {
        names.forEach(function (n) {
          if (n === '.' || n === '..' || !nd.ch[n]) return;
          if (nd.ch[n].t === T.DIR) {
            lines.push('');
            listOne((abs === '/' ? '' : abs) + '/' + n);
          }
        });
      }

      targets.forEach(function (t) { listOne(t); });
      /* 找不到文件时 ls 的退出码是 2（不是 1）—— `ls x || echo no` 这类
         判断靠的就是它，写成恒 0 会让脚本永远走错分支。 */
      return { out: lines.join('\n'), err: '', code: ctx.err.length ? 2 : 0 };
    };

    function inodeOf(fs, nd, name) {
      /* 稳定的伪 inode：同一路径每次一样。够看「硬链共享 inode」这件事。 */
      var h = 0, s = (nd && nd.key) || name || '';
      for (var i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) & 0x7fffffff;
      return 1000 + (h % 90000);
    }

    function longRow(fs, nd, name) {
      var un = userNameOf(fs, nd.u) || String(nd.u);
      var gn = groupNameOf(fs, nd.g) || String(nd.g);
      var size = sizeText(nd, false);
      var tail = nd.t === T.LINK ? name + ' -> ' + nd.k : (nd.t === T.DIR ? name : name);
      return [
        modeFull(nd).padEnd(11),
        String(nlink(nd)).padStart(2),
        un.padEnd(8),
        gn.padEnd(8),
        size.padStart(6),
        fmtTime(nd.mt),
        tail
      ].join(' ');
    }

    /* ---------------------------------------------------------------------
       pwd / cd（cd 是内建，改 fs.cwd）
       --------------------------------------------------------------------- */
    CMD.pwd = function (fs) { return ok(fs.cwd); };

    CMD.cd = function (fs, argv) {
      var target = argv.length ? argv[0] : (fs.env.HOME || '/');
      if (target === '-') {
        var back = fs.prevCwd || fs.cwd;
        fs.prevCwd = fs.cwd;
        fs.cwd = back;
        fs.env.PWD = fs.cwd;
        return ok(fs.cwd);
      }
      var abs = normalize(fs.cwd, target);
      var nd = lookup(fs, abs, true);
      if (!nd) return bad('cd: ' + target + ': No such file or directory');
      if (nd.t !== T.DIR) return bad('cd: ' + target + ': Not a directory');
      if (!permitted(fs, nd, 'x')) return bad('cd: ' + target + ': Permission denied');
      fs.prevCwd = fs.cwd;
      fs.cwd = abs;
      fs.env.PWD = abs;
      return ok('');
    };

    /* ---------------------------------------------------------------------
       mkdir / rmdir / touch
       --------------------------------------------------------------------- */
    CMD.mkdir = function (fs, argv) {
      var p = parseFlags(argv, { val: 'm', long: { parents: 'p', mode: 'm', verbose: 'v' } });
      var o = p.o, code = 0, msgs = [];
      if (!p.rest.length) return bad('mkdir: missing operand');
      p.rest.forEach(function (arg) {
        var abs = normalize(fs.cwd, arg);
        if (o.p) {
          var parts = abs.split('/').filter(Boolean), cur = fs.root, built = '';
          for (var i = 0; i < parts.length; i++) {
            built += '/' + parts[i];
            if (!cur.ch[parts[i]]) {
              if (o.m && !permitted(fs, cur, 'w')) { msgs.push("mkdir: cannot create directory '" + built + "': Permission denied"); code = 1; break; }
              cur.ch[parts[i]] = core.dir(o.m ? parseInt(o.m, 8) : 0o755, fs.uid, fs.gid);
            } else if (cur.ch[parts[i]].t !== T.DIR) {
              msgs.push("mkdir: cannot create directory '" + arg + "': Not a directory"); code = 1; break;
            }
            cur = cur.ch[parts[i]];
          }
          return;
        }
        var r = locate(fs, abs);
        if (!r.parent) { msgs.push("mkdir: cannot create directory '" + arg + "': No such file or directory"); code = 1; return; }
        if (r.node) { msgs.push("mkdir: cannot create directory '" + arg + "': File exists"); code = 1; return; }
        if (!permitted(fs, r.parent, 'w')) { msgs.push("mkdir: cannot create directory '" + arg + "': Permission denied"); code = 1; return; }
        r.parent.ch[r.name] = core.dir(o.m ? parseInt(o.m, 8) : 0o755, fs.uid, fs.gid);
        if (o.v) msgs.push("mkdir: created directory '" + arg + "'");
      });
      return { out: '', err: msgs.join('\n'), code: code };
    };

    CMD.rmdir = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { parents: 'p', verbose: 'v' } });
      var code = 0, msgs = [];
      if (!p.rest.length) return bad('rmdir: missing operand');
      p.rest.forEach(function (arg) {
        var abs = normalize(fs.cwd, arg);
        var r = locate(fs, abs);
        if (!r.node) { msgs.push("rmdir: failed to remove '" + arg + "': No such file or directory"); code = 1; return; }
        if (r.node.t !== T.DIR) { msgs.push("rmdir: failed to remove '" + arg + "': Not a directory"); code = 1; return; }
        if (Object.keys(r.node.ch).length) { msgs.push("rmdir: failed to remove '" + arg + "': Directory not empty"); code = 1; return; }
        if (!permitted(fs, r.parent, 'w')) { msgs.push("rmdir: failed to remove '" + arg + "': Permission denied"); code = 1; return; }
        delete r.parent.ch[r.name];
      });
      return { out: '', err: msgs.join('\n'), code: code };
    };

    CMD.touch = function (fs, argv) {
      var p = parseFlags(argv, { val: 'dtr', long: { no_create: 'c' } });
      var code = 0, msgs = [];
      if (!p.rest.length) return bad('touch: missing file operand');
      p.rest.forEach(function (arg) {
        var abs = normalize(fs.cwd, arg);
        var r = locate(fs, abs);
        if (!r.parent) { msgs.push("touch: cannot touch '" + arg + "': No such file or directory"); code = 1; return; }
        if (r.node) { r.node.mt = fs.clock || core.BASE_TIME; return; }
        if (p.o.c) return;
        if (!permitted(fs, r.parent, 'w')) { msgs.push("touch: cannot touch '" + arg + "': Permission denied"); code = 1; return; }
        r.parent.ch[r.name] = core.file('', 0o644, fs.uid, fs.gid);
      });
      return { out: '', err: msgs.join('\n'), code: code };
    };

    /* ---------------------------------------------------------------------
       cp / mv / rm / ln
       --------------------------------------------------------------------- */
    function cloneTree(nd) {
      var c = { t: nd.t, m: nd.m, u: nd.u, g: nd.g, mt: nd.mt };
      if (nd.t === T.DIR) { c.ch = {}; for (var k in nd.ch) c.ch[k] = cloneTree(nd.ch[k]); }
      else if (nd.t === T.LINK) c.k = nd.k;
      else c.c = nd.c || '';
      return c;
    }

    CMD.cp = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { recursive: 'r', archive: 'a', force: 'f', verbose: 'v', preserve: 'p' } });
      var o = p.o, args = expandAll(fs, p.rest);
      var rec = !!(o.r || o.R || o.a);
      if (args.length < 2) return bad('cp: missing destination file operand after \'' + (args[0] || '') + '\'');
      var dstArg = args[args.length - 1];
      var srcs = args.slice(0, -1);
      var dstAbs = normalize(fs.cwd, dstArg);
      var dstNd = lookup(fs, dstAbs, true);
      var msgs = [], code = 0, outs = [];

      if (srcs.length > 1 && !isDir(dstNd)) {
        return bad("cp: target '" + dstArg + "' is not a directory");
      }

      srcs.forEach(function (src) {
        var sAbs = normalize(fs.cwd, src);
        var sNd = lookup(fs, sAbs, false);
        if (!sNd) { msgs.push("cp: cannot stat '" + src + "': No such file or directory"); code = 1; return; }
        if (sNd.t === T.DIR && !rec) { msgs.push("cp: -r not specified; omitting directory '" + src + "'"); code = 1; return; }
        var targetAbs = isDir(dstNd) ? normalize('/', dstAbs + '/' + sAbs.replace(/^.*\//, '')) : dstAbs;
        var tr = locate(fs, targetAbs);
        if (!tr.parent) { msgs.push("cp: cannot create regular file '" + dstArg + "': No such file or directory"); code = 1; return; }
        if (!permitted(fs, tr.parent, 'w')) { msgs.push("cp: cannot create regular file '" + targetAbs + "': Permission denied"); code = 1; return; }
        var node2 = cloneTree(sNd);
        if (o.p || o.a) { node2.u = sNd.u; node2.g = sNd.g; }
        else { node2.u = fs.uid; node2.g = fs.gid; }
        tr.parent.ch[tr.name] = node2;
        if (o.v) outs.push("'" + src + "' -> '" + targetAbs + "'");
      });
      return { out: outs.join('\n'), err: msgs.join('\n'), code: code };
    };

    CMD.mv = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { force: 'f', verbose: 'v' } });
      var args = expandAll(fs, p.rest);
      if (args.length < 2) return bad("mv: missing destination file operand after '" + (args[0] || '') + "'");
      var dstArg = args[args.length - 1];
      var srcs = args.slice(0, -1);
      var dstAbs = normalize(fs.cwd, dstArg);
      var dstNd = lookup(fs, dstAbs, true);
      if (srcs.length > 1 && !isDir(dstNd)) return bad("mv: target '" + dstArg + "' is not a directory");
      var msgs = [], code = 0;
      srcs.forEach(function (src) {
        var sAbs = normalize(fs.cwd, src);
        var sr = locate(fs, sAbs);
        if (!sr.node) { msgs.push("mv: cannot stat '" + src + "': No such file or directory"); code = 1; return; }
        if (!permitted(fs, sr.parent, 'w')) { msgs.push("mv: cannot move '" + src + "': Permission denied"); code = 1; return; }
        var targetAbs = isDir(dstNd) ? normalize('/', dstAbs + '/' + sAbs.replace(/^.*\//, '')) : dstAbs;
        if (targetAbs === sAbs) return;
        var tr = locate(fs, targetAbs);
        if (!tr.parent) { msgs.push("mv: cannot move '" + src + "': No such file or directory"); code = 1; return; }
        if (!permitted(fs, tr.parent, 'w')) { msgs.push("mv: cannot move '" + src + "': Permission denied"); code = 1; return; }
        tr.parent.ch[tr.name] = sr.node;
        delete sr.parent.ch[sr.name];
      });
      return { out: '', err: msgs.join('\n'), code: code };
    };

    CMD.rm = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { recursive: 'r', force: 'f', verbose: 'v', directory: 'd' } });
      var o = p.o, args = expandAll(fs, p.rest);
      if (!args.length) return bad(o.f ? '' : 'rm: missing operand');
      var msgs = [], code = 0;
      function drop(abs, arg, allowDir) {
        var r = locate(fs, abs);
        if (!r.node) {
          if (!o.f) { msgs.push("rm: cannot remove '" + arg + "': No such file or directory"); code = 1; }
          return;
        }
        if (r.node.t === T.DIR && !allowDir) {
          msgs.push("rm: cannot remove '" + arg + "': Is a directory"); code = 1; return;
        }
        if (!permitted(fs, r.parent, 'w')) { msgs.push("rm: cannot remove '" + arg + "': Permission denied"); code = 1; return; }
        /* sticky bit：/tmp 下别人建的删不掉 */
        if ((r.parent.m & 0o1000) && fs.uid !== r.node.u && !core.isRoot(fs)) {
          msgs.push("rm: cannot remove '" + arg + "': Operation not permitted"); code = 1; return;
        }
        delete r.parent.ch[r.name];
      }
      args.forEach(function (arg) {
        if (/^-/.test(arg)) return;
        var abs = normalize(fs.cwd, arg);
        if (abs === '/') { msgs.push("rm: it is dangerous to operate recursively on '/'"); code = 1; return; }
        drop(abs, arg, !!(o.r || o.R));
      });
      return { out: '', err: msgs.join('\n'), code: code };
    };

    CMD.ln = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { symbolic: 's', force: 'f', verbose: 'v' } });
      var args = p.rest;
      if (args.length < 2) return bad('ln: missing file operand');
      var target = args[0], lnName = args[1];
      var tAbs = normalize(fs.cwd, target);
      var lAbs = normalize(fs.cwd, lnName);
      var r = locate(fs, lAbs);
      if (!r.parent) return bad("ln: failed to create symbolic link '" + lnName + "': No such file or directory");
      if (r.node && !p.o.f) return bad("ln: failed to create symbolic link '" + lnName + "': File exists");
      if (p.o.s) {
        r.parent.ch[r.name] = core.link(tAbs);
      } else {
        var tNd = lookup(fs, tAbs, false);
        if (!tNd) return bad("ln: failed to access '" + target + "': No such file or directory");
        if (tNd.t === T.DIR) return bad("ln: '" + target + "': hard link not allowed for directory");
        r.parent.ch[r.name] = tNd;       // 硬链 = 同一个节点，inode 天然相同
      }
      return ok('');
    };

    CMD.readlink = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { canonicalize: 'f' } });
      if (!p.rest.length) return bad('readlink: missing operand');
      var abs = normalize(fs.cwd, p.rest[0]);
      var nd = lookup(fs, abs, false);
      if (!nd) return bad('readlink: ' + p.rest[0] + ': No such file or directory');
      if (p.o.f) { var f = lookup(fs, abs, true); return ok(f ? abs : abs); }
      if (nd.t !== T.LINK) return ok('');
      return ok(nd.k);
    };

    CMD.realpath = function (fs, argv) {
      if (!argv.length) return bad('realpath: missing operand');
      return ok(normalize(fs.cwd, argv[0]));
    };

    /* ---------------------------------------------------------------------
       stat / file / tree
       --------------------------------------------------------------------- */
    CMD.stat = function (fs, argv) {
      var p = parseFlags(argv, { val: 'c', long: { format: 'c', 'printf': 'c' } });
      if (!p.rest.length) return bad('stat: missing operand');
      var out = [];
      var code = 0, errs = [];
      p.rest.forEach(function (arg) {
        var abs = normalize(fs.cwd, arg);
        var nd = lookup(fs, abs, true);
        if (!nd) { errs.push("stat: cannot statx '" + arg + "': No such file or directory"); code = 1; return; }
        if (o_fmt(p.o.c, abs, nd, fs)) { out.push(o_fmt(p.o.c, abs, nd, fs)); return; }
        var un = userNameOf(fs, nd.u) || String(nd.u);
        var gn = groupNameOf(fs, nd.g) || String(nd.g);
        var size = isDir(nd) ? 4096 : (nd.c || '').length;
        var kind = isDir(nd) ? 'directory' : nd.t === T.LINK ? 'symbolic link' : 'regular file';
        out.push([
          '  File: ' + abs + (nd.t === T.LINK ? ' -> ' + nd.k : ''),
          '  Size: ' + String(size).padEnd(12) + 'Blocks: ' + Math.ceil(size / 512) + '       IO Block: 4096   ' + kind,
          'Device: 0,27\tInode: ' + inodeOf(fs, nd, abs) + '     Links: ' + nlink(nd),
          'Access: (' + ('0000' + (nd.m & 0o7777).toString(8)).slice(-4) + '/' + modeString(nd.m) + ')  Uid: (' +
            String(nd.u).padStart(5) + '/   ' + un + ')   Gid: (' + String(nd.g).padStart(5) + '/   ' + gn + ')',
          'Access: ' + new Date((nd.mt || core.BASE_TIME) * 1000).toISOString().replace('T', ' ').slice(0, 19) + '.000000000 +0800',
          'Modify: ' + new Date((nd.mt || core.BASE_TIME) * 1000).toISOString().replace('T', ' ').slice(0, 19) + '.000000000 +0800',
          'Change: ' + new Date((nd.mt || core.BASE_TIME) * 1000).toISOString().replace('T', ' ').slice(0, 19) + '.000000000 +0800',
          ' Birth: -'
        ].join('\n'));
      });
      return { out: out.join('\n'), err: errs.join('\n'), code: code };
    };

    /* stat -c 的常用格式符：%n %s %U %G %a %A %u %g %i %h %F %y */
    function o_fmt(fmt, abs, nd, fs) {
      if (!fmt) return '';
      return fmt.replace(/\\n/g, '\n').replace(/\\t/g, '\t').replace(/%./g, function (m) {
        switch (m) {
          case '%n': return abs;
          case '%s': return String(isDir(nd) ? 4096 : (nd.c || '').length);
          case '%U': return userNameOf(fs, nd.u) || String(nd.u);
          case '%G': return groupNameOf(fs, nd.g) || String(nd.g);
          case '%a': return (nd.m & 0o7777).toString(8);
          case '%A': return modeString(nd.m);
          case '%u': return String(nd.u);
          case '%g': return String(nd.g);
          case '%i': return String(inodeOf(fs, nd, abs));
          case '%h': return String(nlink(nd));
          case '%F': return isDir(nd) ? 'directory' : nd.t === T.LINK ? 'symbolic link' : 'regular empty file';
          case '%y': return new Date((nd.mt || core.BASE_TIME) * 1000).toISOString().slice(0, 19).replace('T', ' ');
          default: return m;
        }
      });
    }

    CMD.file = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: {} });
      if (!p.rest.length) return bad('Usage: file [-bcdEhikLNnprsSvzZ0] [--extension] [--mime-type] file...');
      var out = [];
      p.rest.forEach(function (arg) {
        var abs = normalize(fs.cwd, arg);
        var nd = lookup(fs, abs, true);
        if (!nd) { out.push(arg + ': cannot open `' + arg + '\' (No such file or directory)'); return; }
        var c = nd.c || '';
        var desc;
        if (isDir(nd)) desc = 'directory';
        else if (nd.t === T.LINK) desc = 'symbolic link to ' + nd.k;
        else if (/^#!\/bin\/(ba)?sh/.test(c)) desc = 'Bourne-Again shell script, ASCII text executable';
        else if (/^ELF/.test(c)) desc = 'ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked';
        else if (c === '') desc = 'empty';
        else if (/(\bPK\b)/.test(c)) desc = 'Zip archive data';
        else desc = 'ASCII text';
        out.push(arg + ': ' + desc);
      });
      return ok(out.join('\n'));
    };

    CMD.tree = function (fs, argv) {
      var p = parseFlags(argv, { val: 'L', long: { dirsfirst: '', all: 'a' } });
      var roots = p.rest.length ? p.rest : ['.'];
      var lines = [], dirs = 0, files = 0;

      function walk(abs, prefix, depth) {
        var nd = lookup(fs, abs, true);
        if (!nd || nd.t !== T.DIR) return;
        var names = Object.keys(nd.ch).filter(function (n) {
          return p.o.a || n.charAt(0) !== '.';
        }).sort(byName);
        names.forEach(function (n, i) {
          var last = i === names.length - 1;
          var child = nd.ch[n];
          lines.push(prefix + (last ? '└── ' : '├── ') + n);
          if (child.t === T.DIR) {
            dirs++;
            if (!p.o.L || depth + 1 < parseInt(p.o.L, 10)) {
              walk(normalize('/', abs + '/' + n), prefix + (last ? '    ' : '│   '), depth + 1);
            }
          } else files++;
        });
      }

      roots.forEach(function (r) {
        lines.push(r);
        dirs += 0;
        walk(normalize(fs.cwd, r), '', 0);
      });
      lines.push('');
      lines.push(dirs + ' director' + (dirs === 1 ? 'y' : 'ies') + ', ' + files + ' file' + (files === 1 ? '' : 's'));
      return ok(lines.join('\n'));
    };

    CMD.basename = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: {} });
      if (!p.rest.length) return bad('basename: missing operand');
      var b = p.rest[0].replace(/\/+$/, '').replace(/^.*\//, '');
      if (p.rest[1] && b.slice(-p.rest[1].length) === p.rest[1]) b = b.slice(0, -p.rest[1].length);
      return ok(b);
    };

    CMD.dirname = function (fs, argv) {
      if (!argv.length) return bad('dirname: missing operand');
      var s = argv[0].replace(/\/+$/, '');
      var i = s.lastIndexOf('/');
      if (i < 0) return ok('.');
      if (i === 0) return ok('/');
      return ok(s.slice(0, i));
    };

    CMD.namei = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { modes: 'm' } });
      if (!p.rest.length) return bad('namei: missing argument');
      var abs = normalize(fs.cwd, p.rest[0]);
      var parts = abs.split('/').filter(Boolean);
      var out = [], acc = '';
      out.push('f: ' + abs);
      var cur = fs.root;
      for (var i = 0; i < parts.length; i++) {
        acc += '/' + parts[i];
        if (!cur.ch || !cur.ch[parts[i]]) { out.push(' ' + (i === parts.length - 1 ? 'l' : ' ') + ' ' + acc + ' - No such file or directory'); break; }
        cur = cur.ch[parts[i]];
        out.push(' ' + (cur.t === T.DIR ? 'd' : cur.t === T.LINK ? 'l' : '-') + ' ' + acc);
      }
      return ok(out.join('\n'));
    };

    /* ---------------------------------------------------------------------
       cat / head / tail / nl / wc / od
       --------------------------------------------------------------------- */
    CMD.cat = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: '', long: { number: 'n', squeeze: 's', show_ends: 'E' } });
      if (!p.rest.length) return ok(ctx.stdin || '');
      var out = [], errs = [], code = 0;
      expandAll(fs, p.rest).forEach(function (arg) {
        if (arg === '-') { out.push(ctx.stdin || ''); return; }
        var abs = normalize(fs.cwd, arg);
        var nd = lookup(fs, abs, true);
        var c = readFile(fs, abs, nd);
        if (c.charAt(0) === '!') { errs.push("cat: " + arg + ': ' + c.slice(1)); code = 1; return; }
        out.push(c);
      });
      var text = out.join('');
      if (p.o.n) {
        var n = 0;
        text = text.split('\n').map(function (l, i, arr) {
          if (i === arr.length - 1 && l === '') return l;
          n++;
          return String(n).padStart(6) + '\t' + l;
        }).join('\n');
      }
      if (p.o.E) text = text.replace(/\n/g, '$\n');
      return { out: text, err: errs.join('\n'), code: code };
    };

    CMD.tac = function (fs, argv, ctx) {
      var r = CMD.cat(fs, argv, ctx);
      if (r.code) return r;
      var lines = r.out.replace(/\n$/, '').split('\n');
      return ok(lines.reverse().join('\n') + (r.out.endsWith('\n') ? '\n' : ''));
    };

    CMD.head = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: 'nc', long: { lines: 'n', bytes: 'c' } });
      var n = parseInt(p.o.n || 10, 10);
      /* `head -3` 是 `head -n 3` 的简写 —— parseFlags 把它拆成了 o['3'] */
      Object.keys(p.o).forEach(function (k) { if (/^\d+$/.test(k)) n = parseInt(k, 10); });
      var text = gather(fs, p.rest, ctx).text;
      if (p.o.c) return ok(text.slice(0, parseInt(p.o.c, 10)));
      var lines = text.split('\n');
      if (lines[lines.length - 1] === '') lines.pop();
      return ok(lines.slice(0, n).join('\n') + (lines.length ? '\n' : ''));
    };

    CMD.tail = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: 'ncf', long: { lines: 'n', bytes: 'c', follow: 'f' } });
      var text = gather(fs, p.rest, ctx).text;
      if (p.o.c) return ok(text.slice(-parseInt(p.o.c, 10)));
      var n = p.o.n == null ? 10 : (String(p.o.n).charAt(0) === '+' ? -parseInt(p.o.n.slice(1), 10) : parseInt(p.o.n, 10));
      Object.keys(p.o).forEach(function (k) { if (/^\d+$/.test(k)) n = parseInt(k, 10); });
      var lines = text.split('\n');
      if (lines[lines.length - 1] === '') lines.pop();
      var picked = n < 0 ? lines.slice(-n - 1) : lines.slice(-n);
      return ok(picked.join('\n') + (picked.length ? '\n' : ''));
    };

    function gather(fs, args, ctx) {
      var out = [], errs = [], code = 0;
      if (!args.length) return { text: ctx.stdin || '', errs: errs, code: 0 };
      expandAll(fs, args).forEach(function (arg) {
        if (arg === '-') { out.push(ctx.stdin || ''); return; }
        var abs = normalize(fs.cwd, arg);
        var c = readFile(fs, abs, lookup(fs, abs, true));
        if (c.charAt(0) === '!') { errs.push(arg + ': ' + c.slice(1)); code = 1; return; }
        out.push(c);
      });
      return { text: out.join(''), errs: errs, code: code };
    }

    CMD.nl = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: 'bw', long: {} });
      var text = gather(fs, p.rest, ctx).text;
      var n = 0;
      return ok(text.split('\n').map(function (l, i, arr) {
        if (i === arr.length - 1 && l === '') return l;
        n++;
        return String(n).padStart(6) + '\t' + l;
      }).join('\n'));
    };

    CMD.wc = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: '', long: { lines: 'l', words: 'w', chars: 'm', bytes: 'c' } });
      var o = p.o;
      var wantAll = !(o.l || o.w || o.c || o.m);
      var rows = [];
      var errs = [];
      var args = p.rest.length ? p.rest : null;

      function count(text) {
        var lines = (text.match(/\n/g) || []).length;
        var words = (text.match(/\S+/g) || []).length;
        var bytes = new TextEncoder().encode(text).length;
        return { l: lines, w: words, c: bytes };
      }

      var total = { l: 0, w: 0, c: 0 };
      var list = args ? expandAll(fs, args) : ['-'];
      list.forEach(function (arg) {
        var text;
        if (arg === '-') text = ctx.stdin || '';
        else {
          var abs = normalize(fs.cwd, arg);
          var c = readFile(fs, abs, lookup(fs, abs, true));
          if (c.charAt(0) === '!') { errs.push('wc: ' + arg + ': ' + c.slice(1)); return; }
          text = c;
        }
        var k = count(text);
        total.l += k.l; total.w += k.w; total.c += k.c;
        var cols = [];
        if (wantAll || o.l) cols.push(String(k.l).padStart(7 - 0));
        if (wantAll || o.w) cols.push(String(k.w).padStart(7 - 0));
        if (wantAll || o.c) cols.push(String(k.c).padStart(7 - 0));
        if (wantAll || o.m) cols.push(String(text.length).padStart(7 - 0));
        rows.push(cols.join('').replace(/^ +/, '') + (arg === '-' ? '' : ' ' + arg));
      });
      if (args && list.length > 1) {
        var cols2 = [];
        if (wantAll || o.l) cols2.push(String(total.l).padStart(7 - 0));
        if (wantAll || o.w) cols2.push(String(total.w).padStart(7 - 0));
        if (wantAll || o.c) cols2.push(String(total.c).padStart(7 - 0));
        rows.push(cols2.join('').replace(/^ +/, '') + ' total');
      }
      return { out: rows.join('\n'), err: errs.join('\n'), code: errs.length ? 1 : 0 };
    };

    CMD.od = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: 'AjNt', long: {} });
      var text = gather(fs, p.rest, ctx).text;
      var bytes = new TextEncoder().encode(text);
      var out = [];
      for (var i = 0; i < bytes.length; i += 16) {
        var chunk = Array.prototype.slice.call(bytes, i, i + 16);
        var oct = chunk.map(function (b) { return ('000' + b.toString(8)).slice(-3); });
        var addr = i.toString(8);
        out.push(('0000000' + addr).slice(-7) + ' ' + oct.join(' ').padEnd(47) + '  ' +
          chunk.map(function (b) { return b >= 32 && b < 127 ? String.fromCharCode(b) : '.'; }).join(''));
      }
      out.push(('0000000' + bytes.length.toString(8)).slice(-7));
      return ok(out.join('\n'));
    };

    /* less / more：沙箱里不出分页器，直接把内容打出来并附一句提示。
       真机是交互界面，这里的目的是让「内容看得到」这件事成立。 */
    CMD.less = function (fs, argv, ctx) {
      var r = CMD.cat(fs, argv.filter(function (a) { return a.charAt(0) !== '-'; }), ctx);
      return r;
    };
    CMD.more = CMD.less;

    /* 后面几个命令文件（文本 / 权限 / 系统）都要用这些小工具，
       挂在共享表上比自己再抄一份稳 —— 抄一份迟早改漏一处。 */
    CMD.__h = {
      ok: ok, bad: bad, parseFlags: parseFlags, expandPath: expandPath,
      expandAll: expandAll, readFile: readFile, writeFile: writeFile,
      fmtTime: fmtTime, byName: byName, isDir: isDir, sizeText: sizeText,
      dirSize: dirSize, nlink: nlink, columns: columns,
      longRow: longRow, inodeOf: inodeOf, globMatch: globMatch, gather: gather
    };
    return CMD.__h;
  }

  return { install: install };
});
