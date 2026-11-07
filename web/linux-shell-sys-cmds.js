/* ===========================================================================
   Linux 命令沙箱 · 第 4 层：权限 / 用户 / 归档 / 系统
   ---------------------------------------------------------------------------
   这一层的分工很清楚：

     chmod chown useradd groupadd su id ...        → **真改**虚拟系统状态
     tar gzip zip                                  → **真打包**（存进隐藏的 arc 字段），
                                                     所以 `tar tzf` 立刻能列出你刚打的东西
     ps df systemctl dnf ip ping curl ...           → **模拟**，输出是固定表

   ★ 模拟的那批，输出必须「像真的」：字段齐、单位对、报错句式对。
     学生练的是"看输出正确不正确"，不是"沙箱是不是真内核"。
   =========================================================================== */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.LinuxShellSysCmds = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  function install(core, CMD) {
    var H = CMD.__h;
    var ok = H.ok, bad = H.bad, parseFlags = H.parseFlags;
    var normalize = core.normalize, lookup = core.lookup, locate = core.locate;
    var permitted = core.permitted, modeString = core.modeString;
    var T = core.T;

    function isDir(nd) { return nd && nd.t === T.DIR; }

    /* 解包时把缺的中间目录补上。`tar xzf a.tgz -C dir` 里如果包的路径带
       子目录，真机会自动建，不建的话解出来是空 —— 学生以为包坏了。 */
    function mkParents(fs, abs) {
      var parts = abs.split('/').filter(Boolean);
      var cur = fs.root;
      for (var i = 0; i < parts.length - 1; i++) {
        if (!cur.ch[parts[i]]) cur.ch[parts[i]] = core.dir(0o755, fs.uid, fs.gid);
        cur = cur.ch[parts[i]];
        if (cur.t !== T.DIR) return null;
      }
      return cur;
    }
    function pad(s, n) { s = String(s); while (s.length < n) s = ' ' + s; return s; }
    function lpad(s, n) { s = String(s); while (s.length < n) s += ' '; return s; }

    /* =====================================================================
       内建：echo / printf / export / alias / history / set / unset / clear
       ===================================================================== */

    /* 两个最没存在感、但 `$?` 演示离不开的命令。真机里它们是 shell 内建，
       永远返回 0 / 1 —— 少了它们，学生写 `true; echo $?` 会得到 127。 */
    CMD.true = function () { return ok(''); };
    CMD.false = function () { return bad(''); };
    CMD.echo = function (fs, argv) {
      var noNl = false, esc = false, i = 0;
      while (i < argv.length && /^-[neE]+$/.test(argv[i])) {
        if (argv[i].indexOf('n') >= 0) noNl = true;
        if (argv[i].indexOf('e') >= 0) esc = true;
        if (argv[i].indexOf('E') >= 0) esc = false;
        i++;
      }
      var text = argv.slice(i).join(' ');
      if (esc) text = text.replace(/\\n/g, '\n').replace(/\\t/g, '\t').replace(/\\\\/g, '\\').replace(/\\c/g, '');
      return ok(text + (noNl ? '' : '\n'));
    };

    CMD.printf = function (fs, argv) {
      if (!argv.length) return bad('printf: usage: printf [-v var] format [arguments]');
      var fmt = argv[0].replace(/\\n/g, '\n').replace(/\\t/g, '\t');
      var vals = argv.slice(1), i = 0;
      var out = fmt.replace(/%(?:-?\d*\.?\d*)([sdif%])/g, function (all, k) {
        if (k === '%') return '%';
        var v = vals[i++];
        if (k === 'd' || k === 'i') return String(Math.trunc(parseFloat(v) || 0));
        if (k === 'f') return (parseFloat(v) || 0).toFixed(6);
        return v == null ? '' : v;
      });
      return ok(out);
    };

    CMD.export = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: {} });
      if (!p.rest.length) {
        return ok(Object.keys(fs.env).sort().map(function (k) {
          return 'declare -x ' + k + '="' + fs.env[k] + '"';
        }).join('\n'));
      }
      p.rest.forEach(function (kv) {
        var eq = kv.indexOf('=');
        if (eq > 0) fs.env[kv.slice(0, eq)] = kv.slice(eq + 1);
      });
      return ok('');
    };
    CMD.set = function (fs) { return ok(Object.keys(fs.env).sort().map(function (k) { return k + '=' + fs.env[k]; }).join('\n')); };
    CMD.unset = function (fs, argv) {
      argv.forEach(function (k) { delete fs.env[k]; });
      return ok('');
    };
    CMD.env = function (fs) {
      return ok(Object.keys(fs.env).sort().map(function (k) { return k + '=' + fs.env[k]; }).join('\n'));
    };

    CMD.alias = function (fs, argv) {
      fs.aliases = fs.aliases || { ll: 'ls -l', la: 'ls -a', 'ls' : 'ls --color=auto' };
      if (!argv.length) {
        return ok(Object.keys(fs.aliases).sort().map(function (k) {
          return "alias " + k + "='" + fs.aliases[k] + "'";
        }).join('\n'));
      }
      argv.forEach(function (a) {
        var eq = a.indexOf('=');
        if (eq > 0) fs.aliases[a.slice(0, eq)] = a.slice(eq + 1).replace(/^'|'$/g, '');
      });
      return ok('');
    };
    CMD.unalias = function (fs, argv) {
      argv.forEach(function (k) { if (fs.aliases) delete fs.aliases[k]; });
      return ok('');
    };

    CMD.history = function (fs, argv) {
      var p = parseFlags(argv, { val: 'c', long: {} });
      if (p.o.c) { fs.history = []; return ok(''); }
      var list = fs.history || [];
      var n = argv.length && /^\d+$/.test(argv[argv.length - 1]) ? parseInt(argv[argv.length - 1], 10) : list.length;
      return ok(list.slice(-n).map(function (c, i) {
        return pad(list.length - Math.min(n, list.length) + i + 1, 5) + '  ' + c;
      }).join('\n'));
    };
    CMD.history.toString = function () { return ''; };

    CMD.clear = function () { return { out: '', err: '', code: 0, clear: true }; };

    CMD.exit = function (fs, argv) {
      var code = argv.length ? parseInt(argv[0], 10) : 0;
      return { out: '', err: '', code: isNaN(code) ? 0 : code, exit: true };
    };
    CMD.logout = CMD.exit;

    CMD.source = function (fs, argv) { return ok(''); };
    CMD['.'] = CMD.source;

    /* uname / hostname / date / whoami / id / groups */
    CMD.uname = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { all: 'a', kernel: 's', release: 'r', nodename: 'n', machine: 'm' } });
      if (p.o.a) return ok('Linux fedora 7.1.12-200.fc44.x86_64 #1 SMP PREEMPT_DYNAMIC x86_64 GNU/Linux');
      if (p.o.r) return ok('7.1.12-200.fc44.x86_64');
      if (p.o.n) return ok('fedora');
      if (p.o.m) return ok('x86_64');
      return ok('Linux');
    };
    CMD.hostname = function (fs, argv) {
      if (argv.length && !argv[0].charAt(0) === '-') return ok('');
      return ok(fs.env.HOSTNAME || 'fedora');
    };
    CMD.date = function (fs, argv) {
      var d = new Date((fs.clock || core.BASE_TIME) * 1000);
      var p = parseFlags(argv, { val: '', long: {} });
      if (p.rest.length && /^\+/.test(p.rest[0])) {
        var fmt = p.rest[0].slice(1);
        var W = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        var M = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
        return ok(fmt
          .replace(/%Y/g, d.getUTCFullYear()).replace(/%m/g, String(d.getUTCMonth() + 1).padStart(2, '0'))
          .replace(/%d/g, String(d.getUTCDate()).padStart(2, '0')).replace(/%H/g, String(d.getUTCHours()).padStart(2, '0'))
          .replace(/%M/g, String(d.getUTCMinutes()).padStart(2, '0')).replace(/%S/g, String(d.getUTCSeconds()).padStart(2, '0'))
          .replace(/%A/g, W[d.getUTCDay()]).replace(/%B/g, M[d.getUTCMonth()]).replace(/%F/g, '2025-11-05')
          .replace(/%T/g, '09:20:00').replace(/%Z/g, 'CST'));
      }
      var day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][d.getUTCDay()];
      var mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][d.getUTCMonth()];
      return ok(day + ' Nov  5 09:20:00 CST 2025');
    };

    CMD.whoami = function (fs) { return ok(core.userNameOf(fs, fs.uid) || String(fs.uid)); };

    CMD.id = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { user: 'u', group: 'g', groups: 'G', name: 'n' } });
      var uname2 = core.userNameOf(fs, fs.uid) || String(fs.uid);
      var gname = core.groupNameOf(fs, fs.gid) || String(fs.gid);
      var extra = (fs.groups ? Object.keys(fs.groups) : []).filter(function (g) {
        return fs.groups[g].members.indexOf(uname2) >= 0;
      });
      if (p.o.u) return ok(String(fs.uid));
      if (p.o.g) return ok(String(fs.gid));
      if (p.o.G) return ok([fs.gid].concat(extra.map(function (g) { return fs.groups[g].gid; })).join(' '));
      var gs = [gname].concat(extra).join(',');
      return ok('uid=' + fs.uid + '(' + uname2 + ') gid=' + fs.gid + '(' + gname + ') groups=' + gs);
    };

    CMD.groups = function (fs, argv) {
      var uname2 = argv.length ? argv[0] : (core.userNameOf(fs, fs.uid) || '');
      var gs = (fs.groups ? Object.keys(fs.groups) : []).filter(function (g) {
        return fs.groups[g].members.indexOf(uname2) >= 0 || fs.groups[g].gid === fs.gid;
      });
      return ok(uname2 + ' : ' + gs.join(' '));
    };

    CMD.who = function () {
      return ok('student  tty2         2025-11-05 09:12 (:0)');
    };
    CMD.w = function () {
      return ok([
        ' 09:20:00 up 8 min,  1 user,  load average: 0.21, 0.18, 0.09',
        'USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT',
        'student  tty2     :0               09:12    3.00s  0.12s  0.02s /usr/libexec/gnome-session-binary'
      ].join('\n'));
    };
    CMD.lastlog = function () {
      return ok([
        'Username         Port     From             Latest',
        'root                                       **Never logged in**',
        'student          tty2                      Wed Nov  5 09:12:01 +0800 2025'
      ].join('\n'));
    };

    /* =====================================================================
       chmod / chown / chgrp / umask / ACL
       ===================================================================== */
    CMD.chmod = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { recursive: 'R', verbose: 'v' } });
      var args = p.rest.slice();
      if (args.length < 2) return bad('chmod: missing operand after \'' + (args[0] || '') + '\'');
      var spec = args.shift();
      var msgs = [], code = 0;

      function apply(nd, arg) {
        if (!core.isRoot(fs) && fs.uid !== nd.u) {
          msgs.push("chmod: changing permissions of '" + arg + "': Operation not permitted");
          code = 1; return;
        }
        if (/^[0-7]{3,4}$/.test(spec)) {
          var keep = nd.m & 0o7000;
          nd.m = (parseInt(spec, 8) & 0o7777) | (spec.length === 3 ? keep : 0);
          return;
        }
        /* 符号模式：u+x,g-w,o=r,a+x 以及裸 +x */
        spec.split(',').forEach(function (clause) {
          var m = /^([ugoa]*)([+\-=])([rwxXst]*)$/.exec(clause);
          if (!m) return;
          var who = m[1] || 'a';
          var op = m[2];
          var bits = 0;
          if (m[3].indexOf('r') >= 0) bits |= 4;
          if (m[3].indexOf('w') >= 0) bits |= 2;
          if (m[3].indexOf('x') >= 0) bits |= 1;
          var shifts = [];
          if (who.indexOf('a') >= 0 || who === '') shifts = [6, 3, 0];
          else {
            if (who.indexOf('u') >= 0) shifts.push(6);
            if (who.indexOf('g') >= 0) shifts.push(3);
            if (who.indexOf('o') >= 0) shifts.push(0);
          }
          shifts.forEach(function (sh) {
            var cur = (nd.m >> sh) & 7;
            var nv = op === '+' ? (cur | bits) : op === '-' ? (cur & ~bits) : bits;
            nd.m = (nd.m & ~(7 << sh)) | ((nv & 7) << sh);
          });
          if (m[3].indexOf('s') >= 0 && who.indexOf('u') >= 0) nd.m |= 0o4000;
          if (m[3].indexOf('s') >= 0 && who.indexOf('g') >= 0) nd.m |= 0o2000;
          if (m[3].indexOf('t') >= 0) nd.m |= 0o1000;
        });
      }

      function walk(abs, arg) {
        var nd = lookup(fs, abs, true);
        if (!nd) { msgs.push("chmod: cannot access '" + arg + "': No such file or directory"); code = 1; return; }
        apply(nd, arg);
        if ((p.o.R) && nd.t === T.DIR) {
          Object.keys(nd.ch).sort(H.byName).forEach(function (n) {
            walk(normalize('/', abs + '/' + n), arg.replace(/\/+$/, '') + '/' + n);
          });
        }
      }

      H.expandAll(fs, args).forEach(function (arg) {
        if (/^-[Rrv]+$/.test(arg)) return;
        walk(normalize(fs.cwd, arg), arg);
      });
      return { out: '', err: msgs.join('\n'), code: code };
    };

    function chownLike(fs, argv, field, label) {
      var p = parseFlags(argv, { val: '', long: { recursive: 'R', verbose: 'v' } });
      var args = p.rest.slice();
      if (args.length < 2) return bad(label + ': missing operand after \'' + (args[0] || '') + '\'');
      var spec = args.shift();
      var msgs = [], code = 0;

      function resolveU(name) {
        if (!name) return null;
        if (/^\d+$/.test(name)) return parseInt(name, 10);
        return fs.users[name] ? fs.users[name].uid : null;
      }
      function resolveG(name) {
        if (!name) return null;
        if (/^\d+$/.test(name)) return parseInt(name, 10);
        return fs.groups[name] ? fs.groups[name].gid : null;
      }

      if (!core.isRoot(fs)) {
        return bad(label + ": changing ownership of '" + args[0] + "': Operation not permitted");
      }

      var uWant = null, gWant = null;
      if (field === 'u') {
        var parts = spec.split(':');
        uWant = resolveU(parts[0]);
        if (parts[1]) gWant = resolveG(parts[1]);
        if (uWant === null && parts[0]) return bad(label + ": invalid user: '" + parts[0] + "'");
      } else {
        gWant = resolveG(spec);
        if (gWant === null) return bad(label + ": invalid group: '" + spec + "'");
      }

      function walk(abs, arg) {
        var nd = lookup(fs, abs, true);
        if (!nd) { msgs.push(label + ": cannot access '" + arg + "': No such file or directory"); code = 1; return; }
        if (uWant !== null) nd.u = uWant;
        if (gWant !== null) nd.g = gWant;
        if (p.o.R && nd.t === T.DIR) {
          Object.keys(nd.ch).forEach(function (n) { walk(normalize('/', abs + '/' + n), arg + '/' + n); });
        }
      }
      args.forEach(function (arg) { walk(normalize(fs.cwd, arg), arg); });
      return { out: '', err: msgs.join('\n'), code: code };
    }

    CMD.chown = function (fs, argv) { return chownLike(fs, argv, 'u', 'chown'); };
    CMD.chgrp = function (fs, argv) { return chownLike(fs, argv, 'g', 'chgrp'); };

    CMD.umask = function (fs, argv) {
      var cur = fs.umask == null ? 0o022 : fs.umask;
      if (!argv.length) return ok(('0000' + cur.toString(8)).slice(-4));
      var v = argv[0];
      if (/^[0-7]{3,4}$/.test(v)) fs.umask = parseInt(v, 8);
      return ok('');
    };

    CMD.getfacl = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: {} });
      if (!p.rest.length) return bad('getfacl: missing file operand');
      return ok(p.rest.map(function (arg) {
        var abs = normalize(fs.cwd, arg);
        var nd = lookup(fs, abs, true);
        if (!nd) return 'getfacl: ' + arg + ': No such file or directory';
        var un = core.userNameOf(fs, nd.u) || String(nd.u);
        var gn = core.groupNameOf(fs, nd.g) || String(nd.g);
        var base = [
          '# file: ' + arg,
          '# owner: ' + un,
          '# group: ' + gn,
          'user::' + modeString(nd.m).slice(1, 4),
          'group::' + modeString(nd.m).slice(4, 7),
          'other::' + modeString(nd.m).slice(7, 10)
        ];
        (nd.acl || []).forEach(function (a) {
          base.splice(4, 0, 'user:' + a.user + ':' + a.perm);
        });
        return base.join('\n') + '\n';
      }).join('\n'));
    };

    CMD.setfacl = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { modify: 'm', remove: 'x', recursive: 'R' } });
      var args = p.rest.slice();
      if (args.length < 2) return bad('setfacl: missing operand');
      var spec = args.shift();
      var m = /^u:([^:]+):(.+)$/.exec(spec) || /^user:([^:]+):(.+)$/.exec(spec);
      if (!m) return bad('setfacl: ' + spec + ': Invalid argument');
      var uname2 = m[1], perm = m[2];
      args.forEach(function (arg) {
        var abs = normalize(fs.cwd, arg);
        var nd = lookup(fs, abs, true);
        if (!nd) return;
        nd.acl = nd.acl || [];
        nd.acl = nd.acl.filter(function (a) { return a.user !== uname2; });
        nd.acl.push({ user: uname2, perm: perm.indexOf('r') >= 0 ? 'r--' : perm });
      });
      return ok('');
    };

    /* =====================================================================
       useradd / usermod / userdel / groupadd / passwd / su / sudo
       ===================================================================== */
    function nextUid(fs) {
      var max = 999;
      for (var n in fs.users) max = Math.max(max, fs.users[n].uid);
      return max + 1;
    }
    function nextGid(fs) {
      var max = 999;
      for (var g in fs.groups) max = Math.max(max, fs.groups[g].gid);
      return max + 1;
    }

    CMD.useradd = function (fs, argv) {
      var p = parseFlags(argv, { val: 'u g G d s c e', long: { uid: 'u', gid: 'g', groups: 'G', home: 'd', shell: 's', comment: 'c', 'create-home': 'm', 'no-create-home': 'M' } });
      if (!p.rest.length) return bad('Usage: useradd [options] LOGIN');
      var o = p.o, code = 0, errs = [];
      p.rest.forEach(function (name) {
        if (!/^[a-z_][a-z0-9_-]*$/.test(name)) { errs.push("useradd: invalid user name '" + name + "'"); code = 1; return; }
        if (fs.users[name]) { errs.push("useradd: user '" + name + "' already exists"); code = 1; return; }
        var uid = o.u ? parseInt(o.u, 10) : nextUid(fs);
        for (var k in fs.users) if (fs.users[k].uid === uid && !o.u) uid++;
        var gid = o.g ? (fs.groups[o.g] ? fs.groups[o.g].gid : parseInt(o.g, 10)) : uid;
        if (!o.g) fs.groups[name] = { gid: gid, members: [] };
        var home = o.d || ('/home/' + name);
        var shell = o.s || '/bin/bash';
        fs.users[name] = { uid: uid, gid: gid, home: home, shell: shell, gecos: o.c || name };
        /* -m 建家目录。真机 useradd 默认不建（Fedora 的 /etc/login.defs 里
           CREATE_HOME yes 让 useradd 建，所以这里默认也建，跟 Fedora 一致 */
        var createHome = o.M ? false : true;
        if (createHome) {
          var r = locate(fs, home);
          if (r.parent && !r.node) {
            r.parent.ch[r.name] = core.dir(0o700, uid, gid);
            r.parent.ch[r.name].ch['.bashrc'] = core.file('# .bashrc\n', 0o644, uid, gid);
          }
        }
        if (o.G) {
          o.G.split(',').forEach(function (g) {
            if (fs.groups[g] && fs.groups[g].members.indexOf(name) < 0) fs.groups[g].members.push(name);
          });
        }
        core.rewriteAccounts(fs);
      });
      return { out: '', err: errs.join('\n'), code: code };
    };

    CMD.userdel = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { remove: 'r', force: 'f' } });
      if (!p.rest.length) return bad('Usage: userdel [options] LOGIN');
      var code = 0, errs = [];
      p.rest.forEach(function (name) {
        if (!fs.users[name]) { errs.push("userdel: user '" + name + "' does not exist"); code = 1; return; }
        if (name === 'root') { errs.push('userdel: user root is currently used by process 1'); code = 1; return; }
        var home = fs.users[name].home;
        delete fs.users[name];
        /* 同名私有组一起删（userdel 的默认行为） */
        if (fs.groups[name]) delete fs.groups[name];
        for (var g in fs.groups) {
          fs.groups[g].members = fs.groups[g].members.filter(function (x) { return x !== name; });
        }
        if (p.o.r) {
          var r = locate(fs, home);
          if (r.parent && r.node) delete r.parent.ch[r.name];
        }
        core.rewriteAccounts(fs);
      });
      return { out: '', err: errs.join('\n'), code: code };
    };

    CMD.usermod = function (fs, argv) {
      var p = parseFlags(argv, { val: 'u g G d s c l L', long: { uid: 'u', gid: 'g', groups: 'G', home: 'd', shell: 's', comment: 'c', login: 'l', append: 'a' } });
      if (!p.rest.length) return bad('Usage: usermod [options] LOGIN');
      var o = p.o, code = 0, errs = [];
      p.rest.forEach(function (name) {
        var u = fs.users[name];
        if (!u) { errs.push("usermod: user '" + name + "' does not exist"); code = 1; return; }
        if (o.u) u.uid = parseInt(o.u, 10);
        if (o.g) u.gid = fs.groups[o.g] ? fs.groups[o.g].gid : parseInt(o.g, 10);
        if (o.d) u.home = o.d;
        if (o.s) u.shell = o.s;
        if (o.c) u.gecos = o.c;
        if (o.l) {
          if (fs.users[o.l]) { errs.push("usermod: user '" + o.l + "' already exists"); code = 1; return; }
          fs.users[o.l] = u;
          delete fs.users[name];
          name = o.l;
        }
        if (o.G) {
          var want = o.G.split(',');
          if (!o.a) {
            /* -G 不带 -a 是**替换**所有附加组 —— 这是实验 5 最爱考的坑 */
            for (var g in fs.groups) {
              fs.groups[g].members = fs.groups[g].members.filter(function (x) { return x !== name; });
            }
          }
          want.forEach(function (g) {
            if (!fs.groups[g]) fs.groups[g] = { gid: nextGid(fs), members: [] };
            if (fs.groups[g].members.indexOf(name) < 0) fs.groups[g].members.push(name);
          });
        }
        core.rewriteAccounts(fs);
      });
      return { out: '', err: errs.join('\n'), code: code };
    };

    CMD.groupadd = function (fs, argv) {
      var p = parseFlags(argv, { val: 'g', long: { gid: 'g' } });
      if (!p.rest.length) return bad('Usage: groupadd [options] GROUP');
      var code = 0, errs = [];
      p.rest.forEach(function (name) {
        if (fs.groups[name]) { errs.push("groupadd: group '" + name + "' already exists"); code = 1; return; }
        fs.groups[name] = { gid: p.o.g ? parseInt(p.o.g, 10) : nextGid(fs), members: [] };
        core.rewriteAccounts(fs);
      });
      return { out: '', err: errs.join('\n'), code: code };
    };

    CMD.groupdel = function (fs, argv) {
      var code = 0, errs = [];
      argv.filter(function (a) { return a.charAt(0) !== '-'; }).forEach(function (name) {
        if (!fs.groups[name]) { errs.push("groupdel: group '" + name + "' does not exist"); code = 1; return; }
        delete fs.groups[name];
        core.rewriteAccounts(fs);
      });
      return { out: '', err: errs.join('\n'), code: code };
    };

    CMD.groupmod = function (fs, argv) {
      var p = parseFlags(argv, { val: 'gn', long: { gid: 'g', 'new-name': 'n' } });
      var code = 0, errs = [];
      p.rest.forEach(function (name) {
        if (!fs.groups[name]) { errs.push("groupmod: group '" + name + "' does not exist"); code = 1; return; }
        if (p.o.n) {
          fs.groups[p.o.n] = fs.groups[name];
          delete fs.groups[name];
          name = p.o.n;
        }
        if (p.o.g) fs.groups[name].gid = parseInt(p.o.g, 10);
        core.rewriteAccounts(fs);
      });
      return { out: '', err: errs.join('\n'), code: code };
    };

    CMD.gpasswd = function (fs, argv) {
      return ok('');
    };

    CMD.passwd = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { status: 'S', lock: 'l', unlock: 'u', delete: 'd' } });
      if (!p.rest.length) {
        if (p.o.S) return ok('student PS 2025-11-05 0 99999 7 -1 (Password set, SHA512 crypt.)');
        return ok('（沙箱：密码修改不做持久化，改密流程请在本机 Fedora 上练）');
      }
      var name = p.rest[0];
      if (!fs.users[name]) return bad('passwd: user \'' + name + '\' does not exist');
      if (!core.isRoot(fs) && name !== core.userNameOf(fs, fs.uid)) {
        return bad('passwd: You may not view or modify password information for ' + name + '.');
      }
      if (p.o.S) return ok(name + ' P 2025-11-05 0 99999 7 -1 (Password set, SHA512 crypt.)');
      return ok('passwd: password updated successfully');
    };

    /* su：★ 沙箱里跳过密码，但**环境切换必须真做** ——
       实验 2 第 10 题考的就是 `su -` 之后 pwd 变成 /root。 */
    CMD.su = function (fs, argv) {
      var p = parseFlags(argv, { val: 'c', long: {} });
      /* `su -` 的减号必须单独认：parseFlags 不碰长度 1 的 token，
         所以它留在 rest 里。`su - root` 则是 ['-', 'root']。 */
      var a0 = p.rest[0];
      var login = a0 === '-' || !!p.o.l;
      var target = (!a0 || a0 === '-') ? 'root' : a0;
      if (!fs.users[target]) return bad('su: user ' + target + ' does not exist');
      var back = { uid: fs.uid, gid: fs.gid, cwd: fs.cwd };
      fs.suStack = fs.suStack || [];
      fs.suStack.push(back);
      fs.uid = fs.users[target].uid;
      fs.gid = fs.users[target].gid;
      fs.env.USER = target;
      fs.env.LOGNAME = target;
      if (login) {
        /* 带减号 = 完整登录：$HOME 跟着换，cwd 落到新用户家目录 */
        fs.env.HOME = fs.users[target].home;
        fs.env.SHELL = fs.users[target].shell;
        fs.cwd = fs.users[target].home;
        fs.env.PWD = fs.cwd;
      }
      return { out: '（沙箱：已切到 ' + target + '，密码校验跳过）', err: '', code: 0, suChange: true };
    };

    /* sudo 不能用 parseFlags 解析 —— 它后面的参数是**子命令**，
       一旦被 flag 解析器吃掉（`sudo usermod -aG dev tom` 里的 -aG），
       子命令就残了。只认 sudo 自己的那几个开关。 */
    CMD.sudo = function (fs, argv, ctx) {
      var i = 0, uid = 0;
      while (i < argv.length) {
        var a = argv[i];
        if (a === '-u' || a === '--user') {
          var who = argv[i + 1] || 'root';
          uid = fs.users[who] ? fs.users[who].uid : (parseInt(who, 10) || 0);
          i += 2; continue;
        }
        if (a === '-E' || a === '-H' || a === '-i' || a === '-s' || a === '--preserve-env') { i++; continue; }
        if (a === '--') { i++; break; }
        break;
      }
      var cmd = argv.slice(i);
      if (!cmd.length) return bad('usage: sudo [-u user] command [args]');
      if (!ctx.execAs) return bad('sudo: 沙箱不支持提权执行');
      return ctx.execAs(cmd, uid);
    };

    /* =====================================================================
       tar / gzip / zip  —— 真打包，存在节点的 arc 隐藏字段里
       ===================================================================== */
    function archiveOf(nd) { return nd && nd.arc ? nd.arc : null; }

    CMD.tar = function (fs, argv) {
      /* GNU tar 允许省掉减号：`tar czf a.tgz dir` ≡ `tar -czf ...`。
         实验指导书上两种写法都有，不补这条会直接报 "You must specify..." */
      if (argv.length && /^[a-zA-Z]+$/.test(argv[0]) && /[cxtru]/.test(argv[0])) {
        argv = ['-' + argv[0]].concat(argv.slice(1));
      }
      var p = parseFlags(argv, { val: 'fC', long: { create: 'c', extract: 'x', list: 't', gzip: 'z', xz: 'J', bzip2: 'j', verbose: 'v', file: 'f', directory: 'C' } });
      var o = p.o;
      var mode = o.c ? 'c' : o.x ? 'x' : o.t ? 't' : '';
      if (!mode) return bad('tar: You must specify one of the -Acdtrux options');
      var file = o.f;
      var args = p.rest.slice();
      if (!file && args.length) file = args.shift();
      if (!file) return bad('tar: Refusing to write archive contents to terminal');
      var abs = normalize(fs.cwd, file);
      var out = [], errs = [], code = 0;

      if (mode === 'c') {
        if (!args.length) return bad('tar: Cowardly refusing to create an empty archive');
        var entries = [];
        function addTree(a, arg) {
          var nd = lookup(fs, a, true);
          if (!nd) { errs.push('tar: ' + arg + ': Cannot stat: No such file or directory'); code = 2; return; }
          entries.push({ path: arg.replace(/^\.\//, ''), t: nd.t, m: nd.m, u: nd.u, g: nd.g,
                         c: nd.t === T.FILE ? (nd.c || '') : '' });
          if (nd.t === T.DIR) {
            Object.keys(nd.ch).sort(H.byName).forEach(function (n) {
              addTree(normalize('/', a + '/' + n), arg.replace(/\/+$/, '') + '/' + n);
            });
          }
        }
        args.forEach(function (arg) { addTree(normalize(fs.cwd, arg), arg); });
        var res6 = H.writeFile(fs, abs, '');
        if (res6) return bad('tar: ' + file + ': ' + res6);
        var nd2 = lookup(fs, abs, true);
        nd2.arc = { kind: o.z ? 'gzip' : o.J ? 'xz' : o.j ? 'bzip2' : 'tar', entries: entries };
        nd2.c = (o.z ? '\x1f\x8b' : 'BDC') + ' <binary archive, ' + entries.length + ' entries> ';
        if (o.v) entries.forEach(function (e) { out.push(e.path + (e.t === T.DIR ? '/' : '')); });
        return { out: out.join('\n'), err: errs.join('\n'), code: code };
      }

      var nd3 = lookup(fs, abs, true);
      if (!nd3) return bad('tar: ' + file + ': Cannot open: No such file or directory');
      var arc = archiveOf(nd3);
      if (!arc) return bad('tar: This does not look like a tar archive\ntar: Exiting with failure status due to previous errors');

      if (mode === 't') {
        var names = arc.entries.map(function (e) { return e.path + (e.t === T.DIR ? '/' : ''); });
        if (args.length) {
          names = names.filter(function (n) {
            return args.some(function (a) { return n === a || n.indexOf(a.replace(/\/+$/, '') + '/') === 0 || n === a + '/'; });
          });
        }
        return ok(names.join('\n'));
      }

      /* 解包 */
      var base = o.C ? normalize(fs.cwd, o.C) : fs.cwd;
      var want = args.length ? args : null;
      arc.entries.forEach(function (e) {
        if (want && !want.some(function (a) { var ar = a.replace(/\/+$/, ''); return e.path === a || e.path === ar || e.path.indexOf(ar + '/') === 0; })) return;
        /* 绝对路径条目：真机 tar 会警告 "Removing leading /" 然后按相对路径解 */
        var rel = e.path.replace(/^\/+/, '');
        var target = normalize('/', base + '/' + rel);
        var parent = mkParents(fs, target);
        if (!parent) return;
        var nm = target.replace(/^.*\//, '');
        if (!permitted(fs, parent, 'w')) { errs.push('tar: ' + target + ': Cannot open: Permission denied'); code = 2; return; }
        if (e.t === T.DIR) {
          if (!parent.ch[nm]) parent.ch[nm] = core.dir(e.m, e.u, e.g);
        } else {
          parent.ch[nm] = core.file(e.c, e.m, e.u, e.g);
        }
        if (o.v) out.push(e.path);
      });
      return { out: out.join('\n'), err: errs.join('\n'), code: code };
    };

    CMD.gzip = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { decompress: 'd', keep: 'k', force: 'f', verbose: 'v' } });
      var code = 0, errs = [];
      p.rest.forEach(function (arg) {
        var abs = normalize(fs.cwd, arg);
        var r = locate(fs, abs);
        if (!r.node) { errs.push('gzip: ' + arg + ': No such file or directory'); code = 1; return; }
        if (p.o.d) {
          if (!/\.gz$/.test(arg)) { errs.push('gzip: ' + arg + ': unknown suffix -- ignored'); return; }
          var arc = r.node.arc;
          var plain = arc && arc.entries ? arc.entries[0].c : (arc && arc.text != null ? arc.text : '');
          var outName = r.name.replace(/\.gz$/, '');
          r.parent.ch[outName] = core.file(plain, r.node.m, r.node.u, r.node.g);
          delete r.parent.ch[r.name];
          return;
        }
        var gzName = r.name + '.gz';
        var ndgz = core.file('\x1f\x8b <gzip compressed>', r.node.m, r.node.u, r.node.g);
        ndgz.arc = { kind: 'gzip', text: r.node.c || '', name: r.name };
        r.parent.ch[gzName] = ndgz;
        if (!p.o.k) delete r.parent.ch[r.name];
      });
      return { out: '', err: errs.join('\n'), code: code };
    };
    CMD.gunzip = function (fs, argv) { return CMD.gzip(fs, ['-d'].concat(argv)); };

    CMD.bzip2 = function (fs, argv) { return CMD.gzip(fs, argv.filter(function (a) { return a !== '-z' && a !== '-9'; })); };
    CMD.xz = function (fs, argv) { return CMD.gzip(fs, argv.filter(function (a) { return a !== '-z' && a !== '-9'; })); };

    CMD.zip = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { recursive: 'r', quiet: 'q' } });
      var args = p.rest.slice();
      if (args.length < 2) return bad('zip error: Nothing to do!');
      var file = args.shift();
      var abs = normalize(fs.cwd, file);
      var entries = [];
      function addTree(a, arg) {
        var nd = lookup(fs, a, true);
        if (!nd) return;
        entries.push({ path: arg, t: nd.t, m: nd.m, u: nd.u, g: nd.g, c: nd.t === T.FILE ? (nd.c || '') : '' });
        if (nd.t === T.DIR && p.o.r) {
          Object.keys(nd.ch).sort(H.byName).forEach(function (n) {
            addTree(normalize('/', a + '/' + n), arg.replace(/\/+$/, '') + '/' + n);
          });
        }
      }
      args.forEach(function (arg) { addTree(normalize(fs.cwd, arg), arg); });
      H.writeFile(fs, abs, 'PK <zip archive>');
      var nd = lookup(fs, abs, true);
      nd.arc = { kind: 'zip', entries: entries };
      return ok('  adding: ' + entries.map(function (e) { return e.path; }).join(' (deflated 62%)\n  adding: ') + ' (stored 0%)');
    };

    CMD.unzip = function (fs, argv) {
      var p = parseFlags(argv, { val: 'd', long: { directory: 'd', list: 'l', quiet: 'q' } });
      var args = p.rest.slice();
      if (!args.length) return bad('UnZip 6.00  Usage: unzip [-Z] [-d exdir] file[.zip]');
      var file = args.shift();
      var abs = normalize(fs.cwd, file);
      var nd = lookup(fs, abs, true);
      if (!nd) return bad('unzip:  cannot find or open ' + file + ', ' + file + '.zip or ' + file + '.ZIP.');
      var arc = archiveOf(nd);
      if (!arc) return bad('unzip: cannot find zipfile directory in one of ' + file);
      if (p.o.l) {
        return ok(arc.entries.map(function (e) { return '  ' + String((e.c || '').length).padStart(9) + '  2025-11-05 09:20   ' + e.path; }).join('\n'));
      }
      var base = p.o.d ? normalize(fs.cwd, p.o.d) : fs.cwd;
      var out = [];
      arc.entries.forEach(function (e) {
        var target = normalize('/', base + '/' + e.path.replace(/^\/+/, ''));
        var parent = mkParents(fs, target);
        if (!parent) return;
        var nm = target.replace(/^.*\//, '');
        if (e.t === T.DIR) { if (!parent.ch[nm]) parent.ch[nm] = core.dir(e.m, e.u, e.g); return; }
        parent.ch[nm] = core.file(e.c, e.m, e.u, e.g);
        out.push('  inflating: ' + e.path);
      });
      return ok('Archive:  ' + file + '\n' + out.join('\n'));
    };

    /* =====================================================================
       进程
       ===================================================================== */
    function procTable(fs) {
      if (fs.procs) return fs.procs;
      fs.procs = [
        { pid: 1, ppid: 0, user: 'root', cpu: 0.0, mem: 0.1, vsz: 176000, rss: 13800, tty: '?', stat: 'Ss', time: '00:00:01', cmd: '/usr/lib/systemd/systemd --switched-root --system' },
        { pid: 468, ppid: 1, user: 'root', cpu: 0.0, mem: 0.2, vsz: 44000, rss: 18200, tty: '?', stat: 'Ss', time: '00:00:00', cmd: '/usr/lib/systemd/systemd-journald' },
        { pid: 1201, ppid: 1, user: 'root', cpu: 0.0, mem: 0.3, vsz: 23000, rss: 12400, tty: '?', stat: 'Ss', time: '00:00:00', cmd: 'sshd: /usr/sbin/sshd -D [listener]' },
        { pid: 1402, ppid: 1, user: 'root', cpu: 0.1, mem: 0.4, vsz: 39000, rss: 21400, tty: '?', stat: 'Ss', time: '00:00:02', cmd: '/usr/bin/dbus-broker-launch --scope system' },
        { pid: 2101, ppid: 1980, user: 'student', cpu: 0.2, mem: 1.2, vsz: 512000, rss: 98000, tty: 'tty2', stat: 'Sl', time: '00:00:04', cmd: '/usr/bin/gnome-shell' },
        { pid: 3204, ppid: 2101, user: 'student', cpu: 0.0, mem: 0.3, vsz: 22000, rss: 9600, tty: 'tty2', stat: 'Ss', time: '00:00:00', cmd: '/usr/bin/gnome-terminal-server' },
        { pid: 3310, ppid: 3204, user: 'student', cpu: 0.0, mem: 0.1, vsz: 11000, rss: 5200, tty: 'pts/0', stat: 'Ss', time: '00:00:00', cmd: '-bash' },
        { pid: 3355, ppid: 3310, user: 'student', cpu: 0.0, mem: 0.1, vsz: 8500, rss: 4100, tty: 'pts/0', stat: 'R+', time: '00:00:00', cmd: 'ps' }
      ];
      return fs.procs;
    }

    CMD.ps = function (fs, argv) {
      var p = parseFlags(argv, { val: 'opuU', long: { aux: '', 'a': '', 'u': '', 'x': '', 'e': '', 'f': '' } });
      var raw = argv.join(' ');
      var table = procTable(fs);
      var showAll = /aux|ax|ef|-e|-A/.test(raw);
      var rows = table.filter(function (x) { return showAll || x.ppid === 3310 || x.pid === 3310 || x.tty === 'pts/0'; });

      if (/aux/.test(raw)) {
        var out = ['USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND'];
        rows.forEach(function (r) {
          out.push(lpad(r.user, 8) + pad(r.pid, 6) + ' ' + (r.cpu).toFixed(1) + pad(r.mem.toFixed(1), 5) +
            pad(r.vsz, 7) + pad(r.rss, 6) + ' ' + lpad(r.tty, 8) + ' ' + lpad(r.stat, 4) + ' 09:12 ' + pad(r.time, 7) + ' ' + r.cmd);
        });
        return ok(out.join('\n'));
      }
      if (/ef|-e/.test(raw)) {
        var out2 = ['UID          PID    PPID  C STIME TTY          TIME CMD'];
        rows.forEach(function (r) {
          out2.push(lpad(r.user, 8) + pad(r.pid, 7) + pad(r.ppid, 8) + '  0 09:12 ' + lpad(r.tty, 8) + ' ' + pad(r.time, 8) + ' ' + r.cmd);
        });
        return ok(out2.join('\n'));
      }
      var out3 = ['    PID TTY          TIME CMD'];
      rows.forEach(function (r) {
        out3.push(pad(r.pid, 7) + ' ' + lpad(r.tty, 8) + ' ' + pad(r.time, 8) + ' ' + r.cmd.split(' ')[0].replace(/^.*\//, ''));
      });
      return ok(out3.join('\n'));
    };

    CMD.pgrep = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: {} });
      if (!p.rest.length) return bad('pgrep: no matching criteria specified');
      var hits = procTable(fs).filter(function (r) { return r.cmd.indexOf(p.rest[0]) >= 0; });
      if (!hits.length) return { out: '', err: '', code: 1 };
      return ok(hits.map(function (r) { return String(r.pid); }).join('\n'));
    };
    CMD.pidof = function (fs, argv) {
      var hits = procTable(fs).filter(function (r) { return r.cmd.split(' ')[0].replace(/^.*\//, '') === argv[0]; });
      if (!hits.length) return { out: '', err: '', code: 1 };
      return ok(hits.map(function (r) { return String(r.pid); }).join(' '));
    };

    CMD.kill = function (fs, argv) {
      var p = parseFlags(argv, { val: 's n', long: { signal: 's' } });
      var sig = p.o.s || p.o.n || 'TERM';
      var code = 0, errs = [], out = [];
      var table = procTable(fs);
      p.rest.forEach(function (arg) {
        if (!/^\d+$/.test(arg)) { errs.push('kill: ' + arg + ': arguments must be process or job IDs'); code = 1; return; }
        var pid = parseInt(arg, 10);
        var idx = -1;
        table.forEach(function (r, i) { if (r.pid === pid) idx = i; });
        if (idx < 0) { errs.push('bash: kill: (' + pid + ') - No such process'); code = 1; return; }
        own(pid);
        table.splice(idx, 1);
      });
      function own(pid) {}
      return { out: '', err: errs.join('\n'), code: code };
    };

    CMD.killall = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: {} });
      var name = p.rest[p.rest.length - 1];
      var table = procTable(fs);
      var before = table.length;
      var keep = table.filter(function (r) { return r.cmd.split(' ')[0].replace(/^.*\//, '') !== name; });
      fs.procs = keep;
      if (keep.length === before) return { out: '', err: name + ': no process found', code: 1 };
      return ok('');
    };

    CMD.pkill = function (fs, argv) {
      var p = parseFlags(argv, { val: 'u', long: { user: 'u', signal: 'SIGTERM' } });
      var table = procTable(fs);
      var pat = p.rest[0] || '';
      var keep = table.filter(function (r) { return r.cmd.indexOf(pat) < 0; });
      var killed = table.length - keep.length;
      fs.procs = keep;
      if (!killed) return { out: '', err: '', code: 1 };
      return ok('');
    };

    CMD.jobs = function () { return ok(''); };
    CMD.fg = function () { return bad('fg: current: no such job'); };
    CMD.bg = function () { return bad('bg: current: no such job'); };

    CMD.nohup = function (fs, argv, ctx) {
      if (!ctx.exec) return bad('nohup: 沙箱不支持后台执行');
      var r = ctx.exec(argv);
      return { out: 'nohup: ignoring input and appending output to \'nohup.out\'' + (r.out ? '\n' + r.out : ''), err: r.err, code: r.code };
    };
    CMD.nice = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: 'n', long: {} });
      if (!p.rest.length) return ok('0');
      return ctx.exec ? ctx.exec(p.rest) : bad('nice: 沙箱不支持');
    };
    CMD.renice = function (fs, argv) {
      var p = parseFlags(argv, { val: 'np', long: {} });
      if (!p.rest.length) return bad('renice: invalid number');
      return ok(String(p.rest[0]).replace(/^.*=/, '') ? p.rest[0].replace(/^.*=/, '') + ': old priority 0, new priority ' + (p.o.n || '0') : '');
    };
    CMD.timeout = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: 's', long: {} });
      var args = p.rest.slice(1);
      if (!args.length) return bad('timeout: missing command');
      return ctx.exec ? ctx.exec(args) : bad('timeout: 沙箱不支持');
    };

    CMD.top = function (fs) {
      var table = procTable(fs);
      var rows = table.slice().sort(function (a, b) { return b.cpu - a.cpu; }).slice(0, 8);
      var out = [
        'top - 09:20:00 up 8 min,  1 user,  load average: 0.21, 0.18, 0.09',
        'Tasks: 218 total,   1 running, 217 sleeping,   0 stopped,   0 zombie',
        '%Cpu(s):  1.3 us,  0.7 sy,  0.0 ni, 97.7 id,  0.3 wa,  0.0 hi,  0.0 si,  0.0 st',
        'MiB Mem :   3820.0 total,   1980.4 free,    920.1 used,    919.5 buff/cache',
        'MiB Swap:   3820.0 total,   3820.0 free,      0.0 used.   2700.2 avail Mem',
        '',
        '    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND'
      ];
      rows.forEach(function (r) {
        out.push(pad(r.pid, 7) + lpad(r.user, 8) + '  20   0 ' + pad(r.vsz, 7) + ' ' + pad(r.rss, 6) + '   9800 S   ' +
          (r.cpu).toFixed(1) + '   ' + (r.mem).toFixed(1) + '   0:00.0' + ' ' + r.cmd.split(' ')[0].replace(/^.*\//, ''));
      });
      return ok(out.join('\n'));
    };

    CMD.free = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { human: 'h', total: 't' } });
      if (p.o.h) {
        return ok([
          '               total        used        free      shared  buff/cache   available',
          'Mem:           3.7Gi       920Mi       1.9Gi        18Mi       919Mi       2.6Gi',
          'Swap:          3.7Gi          0B       3.7Gi'
        ].join('\n'));
      }
      return ok([
        '               total        used        free      shared  buff/cache   available',
        'Mem:         3911680      942104     2028844       18432      941732     2704832',
        'Swap:        3911676           0     3911676'
      ].join('\n'));
    };

    CMD.uptime = function (fs) {
      return ok(' 09:20:00 up 8 min,  1 user,  load average: 0.21, 0.18, 0.09');
    };

    CMD.lsof = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: {} });
      var out = [
        'COMMAND    PID    USER   FD      TYPE DEVICE SIZE/OFF NODE NAME',
        'systemd      1    root  cwd       DIR  253,0      224   64 /',
        'systemd      1    root  txt       REG  253,0  1740520 1234 /usr/lib/systemd/systemd',
        'bash      3310 student  cwd       DIR  253,0     4096  256 /home/student',
        'bash      3310 student  txt       REG  253,0  1295840 5678 /usr/bin/bash'
      ];
      if (p.rest.length) {
        var pat = p.rest[0];
        out.push(pad('bash', 10) + ' 3310 student    3r     REG  253,0     2048  999 ' + pat);
      }
      return ok(out.join('\n'));
    };

    /* =====================================================================
       磁盘
       ===================================================================== */
    CMD.df = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { human: 'h', inodes: 'i' } });
      if (p.o.i) {
        return ok(['Filesystem      Inodes  IUsed IFree IUse% Mounted on',
                   '/dev/vda3      1048576 187432 861144   18% /',
                   '/dev/vda2         1024    412    612   41% /boot/efi'].join('\n'));
      }
      if (p.o.h) {
        return ok(['Filesystem      Size  Used Avail Use% Mounted on',
                   '/dev/vda3        20G  6.2G   13G  33% /',
                   'devtmpfs        1.9G     0  1.9G   0% /dev',
                   'tmpfs           1.9G   18M  1.9G   1% /dev/shm',
                   'tmpfs           1.9G  9.1M  1.9G   1% /run',
                   '/dev/vda2       599M  7.4M  592M   2% /boot/efi'].join('\n'));
      }
      return ok(['Filesystem     1K-blocks    Used Available Use% Mounted on',
                 '/dev/vda3       20971520 6445360  13529920  33% /',
                 'devtmpfs         1955840       0   1955840   0% /dev',
                 'tmpfs            1955840   18432   1937408   1% /dev/shm',
                 'tmpfs            1955840    9316   1946524   1% /run',
                 '/dev/vda2         613376    7564    605812   2% /boot/efi'].join('\n'));
    };

    CMD.du = function (fs, argv) {
      var p = parseFlags(argv, { val: 'd', long: { summary: 's', human: 'h', all: 'a', 'max-depth': 'd' } });
      var maxDepth = p.o.d ? parseInt(p.o.d, 10) : (p.o.s ? 0 : Infinity);
      var targets = p.rest.length ? p.rest : ['.'];
      var lines = [];
      var errs = [];

      function sizeOf(nd) {
        if (nd.t === T.FILE) return Math.ceil((nd.c || '').length / 4096) * 4 || 4;
        var sum = 4;
        for (var k in nd.ch) sum += sizeOf(nd.ch[k]);
        return sum;
      }
      function fmt(kb) {
        if (!p.o.h) return String(kb);
        if (kb < 1024) return kb + 'K';
        return (Math.round(kb / 102.4) / 10) + 'M';
      }
      function walk(abs, arg, depth) {
        var nd = lookup(fs, abs, true);
        if (!nd) { errs.push('du: cannot access \'' + arg + '\': No such file or directory'); return; }
        if (nd.t !== T.DIR) { lines.push(fmt(sizeOf(nd)) + '\t' + arg); return; }
        if (depth <= maxDepth) lines.push(fmt(sizeOf(nd)) + '\t' + arg);
        if (depth >= maxDepth) return;
        Object.keys(nd.ch).sort(H.byName).forEach(function (n) {
          if (nd.ch[n].t === T.DIR) walk(normalize('/', abs + '/' + n), arg.replace(/\/+$/, '') + '/' + n, depth + 1);
          else if (p.o.a) lines.push(fmt(sizeOf(nd.ch[n])) + '\t' + arg.replace(/\/+$/, '') + '/' + n);
        });
      }
      targets.forEach(function (t) { walk(normalize(fs.cwd, t), t, 0); });
      return { out: lines.join('\n'), err: errs.join('\n'), code: errs.length ? 1 : 0 };
    };

    CMD.lsblk = function () {
      return ok([
        'NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS',
        'vda    252:0    0    20G  0 disk',
        '├─vda1 252:1    0     1M  0 part',
        '├─vda2 252:2    0   600M  0 part /boot/efi',
        '└─vda3 252:3    0  19.4G  0 part /',
        'sr0     11:0    1  1024M  0 rom'
      ].join('\n'));
    };

    CMD.mount = function (fs, argv) {
      var p = parseFlags(argv, { val: 't o', long: {} });
      if (!p.rest.length) {
        return ok([
          'proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)',
          'sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)',
          'devtmpfs on /dev type devtmpfs (rw,nosuid,size=978920k,nr_inodes=244730,mode=755)',
          'tmpfs on /run type tmpfs (rw,nosuid,nodev,size=782564k,mode=755)',
          '/dev/vda3 on / type xfs (rw,relatime,seclabel,attr2,inode64,logbufs=8,logbsize=32k)',
          '/dev/vda2 on /boot/efi type vfat (rw,relatime,fmask=0077,dmask=0077,codepage=437,iocharset=ascii,shortname=winnt,errors=remount-ro)',
          'tmpfs on /tmp type tmpfs (rw,nosuid,nodev,seclabel,size=782564k,nr_inodes=409600)'
        ].join('\n'));
      }
      return ok('');
    };
    CMD.umount = function (fs, argv) {
      var lines = argv.filter(function (a) { return a.charAt(0) !== '-'; });
      if (!lines.length) return bad('umount: bad usage');
      return ok('');
    };
    CMD.blkid = function () {
      return ok([
        '/dev/vda1: PARTUUID="3f2a9c1e-01"',
        '/dev/vda2: SEC_TYPE="msdos" UUID="A1B2-C3D4" BLOCK_SIZE="512" TYPE="vfat" PARTUUID="3f2a9c1e-02"',
        '/dev/vda3: LABEL="fedora" UUID="8d1f3a2e-6b4c-4a71-9e0d-2c5b8f7a1d34" BLOCK_SIZE="4096" TYPE="xfs" PARTUUID="3f2a9c1e-03"'
      ].join('\n'));
    };
    CMD.iostat = function () {
      return ok([
        'Linux 7.1.12-200.fc44.x86_64 (fedora) \t11/05/2025 \t_x86_64_\t(2 CPU)',
        '',
        'avg-cpu:  %user   %nice %system %iowait  %steal   %idle',
        '           1.32    0.00    0.71    0.28    0.00   97.69',
        '',
        'Device            r/s     rkB/s     w/s     wkB/s   await  %util',
        'vda              1.20     38.40    0.80     12.80   1.42   0.31'
      ].join('\n'));
    };

    /* =====================================================================
       网络（全模拟）
       ===================================================================== */
    CMD.ip = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { brief: 'br', 'show': '' } });
      if (!p.rest.length || p.rest[0] === 'a' || p.rest[0] === 'addr' || p.rest[0] === 'address') {
        return ok([
          '1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000',
          '    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00',
          '    inet 127.0.0.1/8 scope host lo',
          '       valid_lft forever preferred_lft forever',
          '    inet6 ::1/128 scope host noprefixroute',
          '       valid_lft forever preferred_lft forever',
          '2: ens160: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000',
          '    link/ether 00:0c:29:8a:1b:2c brd ff:ff:ff:ff:ff:ff',
          '    inet 192.168.10.128/24 brd 192.168.10.255 scope global dynamic noprefixroute ens160',
          '       valid_lft 1712sec preferred_lft 1712sec',
          '    inet6 fe80::20c:29ff:fe8a:1b2c/64 scope link noprefixroute',
          '       valid_lft forever preferred_lft forever'
        ].join('\n'));
      }
      if (p.rest[0] === 'r' || p.rest[0] === 'route') {
        return ok([
          'default via 192.168.10.2 dev ens160 proto dhcp src 192.168.10.128 metric 100',
          '192.168.10.0/24 dev ens160 proto kernel scope link src 192.168.10.128 metric 100'
        ].join('\n'));
      }
      if (p.rest[0] === 'link') {
        return ok('1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536\n2: ens160: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 state UP');
      }
      return bad('Object "' + p.rest[0] + '" is unknown, try "ip help".');
    };
    CMD.ifconfig = function () {
      return ok([
        'ens160: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500',
        '        inet 192.168.10.128  netmask 255.255.255.0  broadcast 192.168.10.255',
        '        inet6 fe80::20c:29ff:fe8a:1b2c  prefixlen 64  scopeid 0x20<link>',
        '        ether 00:0c:29:8a:1b:2c  txqueuelen 1000  (Ethernet)',
        '        RX packets 4211  bytes 3829104 (3.6 MiB)',
        '        TX packets 2087  bytes 314562 (307.1 KiB)',
        '',
        'lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536',
        '        inet 127.0.0.1  netmask 255.0.0.0',
        '        loop  txqueuelen 1000  (Local Loopback)'
      ].join('\n'));
    };
    CMD.ss = function (fs, argv) {
      return ok([
        'Netid State  Recv-Q Send-Q Local Address:Port Peer Address:Port Process',
        'udp   UNCONN 0      0          127.0.0.1:323        0.0.0.0:*',
        'tcp   LISTEN 0      128          0.0.0.0:22         0.0.0.0:*',
        'tcp   LISTEN 0      128             [::]:22            [::]:*'
      ].join('\n'));
    };
    CMD.netstat = function (fs, argv) {
      return ok([
        'Active Internet connections (only servers)',
        'Proto Recv-Q Send-Q Local Address           Foreign Address         State',
        'tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN',
        'tcp6       0      0 :::22                   :::*                    LISTEN'
      ].join('\n'));
    };
    CMD.ping = function (fs, argv) {
      var p = parseFlags(argv, { val: 'cW', long: {} });
      var host = p.rest[0];
      if (!host) return bad('ping: usage error: Destination address required');
      var n = p.o.c ? Math.min(parseInt(p.o.c, 10), 5) : 4;
      var out = ['PING ' + host + ' (' + (/\d+\.\d+\.\d+\.\d+/.test(host) ? host : '192.168.10.1') + ') 56(84) bytes of data.'];
      for (var i = 1; i <= n; i++) {
        out.push('64 bytes from ' + (/\d+\.\d+\.\d+\.\d+/.test(host) ? host : '192.168.10.1') +
          ': icmp_seq=' + i + ' ttl=64 time=0.0' + (30 + i) + ' ms');
      }
      out.push('');
      out.push('--- ' + host + ' ping statistics ---');
      out.push(n + ' packets transmitted, ' + n + ' received, 0% packet loss, time ' + (n * 1000) + 'ms');
      return ok(out.join('\n'));
    };
    CMD.tracepath = CMD.traceroute = function (fs, argv) {
      var host = argv.filter(function (a) { return a.charAt(0) !== '-'; })[0] || '';
      return ok([
        'traceroute to ' + host + ', 30 hops max, 60 byte packets',
        ' 1  _gateway (192.168.10.2)  0.412 ms  0.388 ms  0.372 ms',
        ' 2  10.0.0.1 (10.0.0.1)  3.210 ms  3.180 ms  3.150 ms',
        ' 3  * * *'
      ].join('\n'));
    };
    CMD.nslookup = function (fs, argv) {
      var host = argv[argv.length - 1] || 'localhost';
      return ok([
        'Server:\t\t192.168.10.2',
        'Address:\t192.168.10.2#53',
        '',
        'Non-authoritative answer:',
        'Name:\t' + host,
        'Address: 93.184.216.34'
      ].join('\n'));
    };
    CMD.dig = function (fs, argv) {
      var host = argv.filter(function (a) { return a.charAt(0) !== '-' && a.charAt(0) !== '+'; })[0] || '.';
      return ok([
        '; <<>> DiG 9.18 <<>> ' + host,
        ';; global options: +cmd',
        ';; Got answer:',
        ';; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 41234',
        '',
        ';; QUESTION SECTION:',
        ';' + host + '.\t\t\tIN\tA',
        '',
        ';; ANSWER SECTION:',
        host + '.\t\t300\tIN\tA\t93.184.216.34',
        '',
        ';; Query time: 12 msec',
        ';; SERVER: 192.168.10.2#53(192.168.10.2)'
      ].join('\n'));
    };
    CMD.curl = function (fs, argv) {
      var p = parseFlags(argv, { val: 'oXHdA', long: { output: 'o', header: 'H', 'data': 'd', 'head': 'I', 'include': 'i' } });
      var url = p.rest.filter(function (a) { return /^(https?:\/\/|www\.)/.test(a); })[0] || p.rest[0] || '';
      if (!url) return bad('curl: try \'curl --help\' or \'curl --manual\' for more information');
      if (p.o.o) {
        var abs = normalize(fs.cwd, p.o.o);
        H.writeFile(fs, abs, 'sandbox fetch result for ' + url + '\n');
        return ok('');
      }
      if (p.o.I) {
        return ok('HTTP/1.1 200 OK\r\nServer: sandbox/1.0\r\nContent-Type: text/html\r\nContent-Length: 1256\r\n\r\n');
      }
      return ok('<html>\n<head><title>Sandbox</title></head>\n<body>fetched ' + url + ' (sandbox)</body>\n</html>');
    };
    CMD.wget = function (fs, argv) {
      var p = parseFlags(argv, { val: 'OP', long: { output: 'O', 'output-document': 'O' } });
      var url = p.rest[0] || '';
      if (!url) return bad('wget: missing URL');
      var name = p.o.O || url.replace(/^https?:\/\/[^/]+\/?/, '').replace(/\/$/, '') || 'index.html';
      var abs = normalize(fs.cwd, name);
      H.writeFile(fs, abs, 'sandbox fetch result for ' + url + '\n');
      return ok([
        '--2025-11-05 09:20:00--  ' + url,
        'Resolving host... 127.0.0.1',
        'Connecting to host|127.0.0.1|:80... connected.',
        'HTTP request sent, awaiting response... 200 OK',
        'Length: 1256 (1.2K) [text/html]',
        'Saving to: \'' + name + '\'',
        '',
        name + '  100%[===================>]   1.23K  --.-KB/s    in 0s',
        '',
        '2025-11-05 09:20:00 (312 MB/s) - \'' + name + '\' saved [1256/1256]'
      ].join('\n'));
    };
    CMD.ssh = function (fs, argv) {
      var p = parseFlags(argv, { val: 'p i', long: { port: 'p', identity: 'i' } });
      var host = p.rest[0] || '';
      if (!host) return bad('usage: ssh [-p port] [user@]hostname [command]');
      var cmd = p.rest.slice(1).join(' ');
      return ok('（沙箱：SSH 直连不可用，下面是模拟握手结果）\n' +
        'Warning: Permanently added \'' + host + '\' (ED25519) to the list of known hosts.\n' +
        (cmd ? 'Last login: Wed Nov  5 09:18:22 2025 from 192.168.10.1\n' : '') +
        (cmd ? '' : 'Last login: Wed Nov  5 09:18:22 2025 from 192.168.10.1'));
    };
    CMD.scp = function (fs, argv) {
      var p = parseFlags(argv, { val: 'P i', long: { port: 'P' } });
      if (p.rest.length < 2) return bad('usage: scp [-P port] source target');
      return ok('（沙箱：scp 传输模拟，文件未真正离开本机）');
    };
    CMD.rsync = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { archive: 'a', verbose: 'v', delete: '' } });
      var args = p.rest.slice();
      if (args.length < 2) return bad('rsync: 缺少源或目标');
      var src = args[0], dst = args[1];
      if (/:\/\//.test(src) || /:\/\//.test(dst)) return ok('（沙箱：远程 rsync 模拟）');
      var sAbs = normalize(fs.cwd, src);
      var sNd = lookup(fs, sAbs, true);
      if (!sNd) return bad('rsync: [sender] link_stat "' + src + '" failed: No such file or directory (2)');
      var dAbs = normalize(fs.cwd, dst);
      var dNd = lookup(fs, dAbs, true);
      var targetAbs = dNd && dNd.t === T.DIR ? normalize('/', dAbs + '/' + sAbs.replace(/^.*\//, '')) : dAbs;
      var r = locate(fs, targetAbs);
      if (!r.parent) return bad('rsync: mkstemp failed: No such file or directory');
      r.parent.ch[r.name] = JSON.parse(JSON.stringify(sNd));
      return ok(p.o.v ? 'sending incremental file list\n' + src.replace(/^.*\//, '') + '\n\nsent 1,204 bytes  received 35 bytes  2,478.00 bytes/sec\ntotal size is 1,024  speedup is 0.83' : '');
    };
    CMD.hostnamectl = function (fs) {
      return ok([
        ' Static hostname: fedora',
        '       Icon name: computer-vm',
        '         Chassis: vm',
        '      Machine ID: 3f2a9c1e6b4c4a719e0d2c5b8f7a1d34',
        '         Boot ID: 9a8b7c6d5e4f4a3b2c1d0e9f8a7b6c5d',
        '    Virtualization: vmware',
        '  Operating System: Fedora Linux 44 (Workstation Edition)',
        '            Kernel: Linux 7.1.12-200.fc44.x86_64',
        '      Architecture: x86-64',
        '   Firmware Version: 6.00'
      ].join('\n'));
    };
    CMD.nmcli = function (fs, argv) {
      if (argv[0] === 'device' || argv[0] === 'd') {
        return ok('DEVICE  TYPE      STATE         CONNECTION\nens160  ethernet  connected     "Wired connection 1"\nlo      loopback  connected (externally)  lo');
      }
      if (argv[0] === 'connection' || argv[0] === 'c') {
        return ok('NAME                UUID                                  TYPE      DEVICE\n"Wired connection 1" 8d1f3a2e-6b4c-4a71-9e0d-2c5b8f7a1d34  ethernet  ens160');
      }
      return ok('Usage: nmcli [OPTIONS] OBJECT { COMMAND | help }');
    };
    CMD.firewall_cmd = function (fs, argv) {
      if (argv.indexOf('--list-all') >= 0) {
        return ok([
          'public (active)',
          '  target: default',
          '  icmp-block-inversion: no',
          '  interfaces: ens160',
          '  sources:',
          '  services: cockpit dhcpv6-client ssh',
          '  ports:',
          '  protocols:',
          '  forward: no',
          '  masquerade: no',
          '  forward-ports:',
          '  source-ports:',
          '  icmp-blocks:',
          '  rich rules:'
        ].join('\n'));
      }
      return ok('success');
    };
    CMD['firewall-cmd'] = CMD.firewall_cmd;

    /* =====================================================================
       软件包与服务（模拟）
       ===================================================================== */
    CMD.dnf = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { 'assumeyes': 'y', 'quiet': 'q' } });
      var sub = p.rest[0] || '';
      var rest = p.rest.slice(1);
      if (sub === 'install' || sub === 'in') {
        if (!rest.length) return bad('Error: Need to pass a list of pkgs to install');
        var out = ['Last metadata expiration check: 0:12:03 ago on Wed 05 Nov 2025 09:08:11 AM CST.', 'Dependencies resolved.'];
        out.push('================================================================================');
        out.push(' Package        Architecture   Version              Repository       Size');
        out.push('================================================================================');
        out.push('Installing:');
        rest.forEach(function (n) {
          out.push(' ' + lpad(n, 14) + ' x86_64         ' + '1.0-1.fc44'.padEnd(21) + ' fedora         ' + (120 + n.length * 7) + ' k');
        });
        out.push('');
        out.push('Transaction Summary');
        out.push('================================================================================');
        out.push('Install  ' + rest.length + ' Package' + (rest.length > 1 ? 's' : ''));
        out.push('');
        out.push('Complete!');
        return ok(out.join('\n'));
      }
      if (sub === 'remove' || sub === 'erase') {
        if (!rest.length) return bad('Error: Need to pass a list of pkgs to remove');
        return ok('Dependencies resolved.\n\nRemoving:\n ' + rest.join('\n ') + '\n\nComplete!');
      }
      if (sub === 'update' || sub === 'upgrade') {
        return ok('Dependencies resolved.\nNothing to do.\nComplete!');
      }
      if (sub === 'list' || sub === 'search' || sub === 'info') {
        var q = rest[0] || '';
        return ok([
          'Last metadata expiration check: 0:12:03 ago on Wed 05 Nov 2025 09:08:11 AM CST.',
          'Available Packages',
          'gcc.x86_64                        14.2.1-6.fc44              fedora',
          'make.x86_64                       1:4.4.1-3.fc44             fedora',
          'vim-enhanced.x86_64               2:9.1.842-1.fc44           fedora',
          q ? 'your-query.x86_64                 1.0-1.fc44                 fedora' : 'tree.x86_64                       2.1.1-3.fc44               fedora'
        ].filter(Boolean).join('\n'));
      }
      if (sub === 'repolist') {
        return ok(['repo id                  repo name', 'fedora                   Fedora 44 - x86_64',
                   'fedora-updates           Fedora 44 - x86_64 - Updates',
                   'updates                  Fedora 44 - x86_64 - Updates'].join('\n'));
      }
      if (sub === 'clean') return ok('0 files removed');
      if (sub === 'history') return ok('ID     | Command line      | Date and time    | Action(s)      | Altered\n-------------------------------------------------------------------------------\n     1 | install gcc       | 2025-11-05 09:09 | Install        |    1  ');
      return bad('No such command: ' + sub + '. Please use /usr/bin/dnf --help');
    };

    CMD.rpm = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { query: 'q', 'all': 'a', info: 'i', list: 'l', verify: 'V', 'files': 'l' } });
      if (p.o.q && p.o.a) {
        return ok([
          'bash-5.2.26-4.fc44.x86_64',
          'coreutils-9.5-5.fc44.x86_64',
          'dnf-4.21.1-1.fc44.noarch',
          'gcc-14.2.1-6.fc44.x86_64',
          'glibc-2.40-3.fc44.x86_64',
          'kernel-7.1.12-200.fc44.x86_64',
          'sudo-1.9.15-4.p5.fc44.x86_64',
          'systemd-256.9-1.fc44.x86_64',
          'vim-enhanced-9.1.842-1.fc44.x86_64'
        ].join('\n'));
      }
      if (p.o.q && p.o.i) {
        return ok([
          'Name        : gcc',
          'Version     : 14.2.1',
          'Release     : 6.fc44',
          'Architecture: x86_64',
          'Install Date: Wed 05 Nov 2025 09:08:41 AM CST',
          'Size        : 112837842',
          'License     : GPL-3.0-or-later',
          'Summary     : Various compilers (C, C++, Objective-C, Java, ...)'
        ].join('\n'));
      }
      if (p.o.q && p.o.l) {
        return ok([
          '/usr/bin/gcc',
          '/usr/bin/gcc-14',
          '/usr/lib/gcc',
          '/usr/libexec/gcc/x86_64-redhat-linux/14/cc1'
        ].join('\n'));
      }
      if (p.o.q) {
        var q = p.rest[p.rest.length - 1] || '';
        return ok(q.replace(/\.rpm$/, '') + ' 未安装（沙箱内无 RPM 数据库）');
      }
      if (/^-i/.test(argv[0] || '')) {
        return ok('Verifying...                          ################################# [100%]\nPreparing...                          ################################# [100%]');
      }
      return ok('');
    };

    CMD.make = function (fs, argv, ctx) {
      var p = parseFlags(argv, { val: 'fC', long: { file: 'f', directory: 'C' } });
      var dir = p.o.C ? normalize(fs.cwd, p.o.C) : fs.cwd;
      var mkf = p.o.f || 'Makefile';
      var abs = normalize('/', dir + '/' + mkf);
      var nd = lookup(fs, abs, true);
      if (!nd) return bad('make: *** No targets specified and no makefile found.  Stop.');
      var text = nd.c || '';
      var targets = text.split('\n').filter(function (l) { return /^[A-Za-z0-9_.-]+\s*:/.test(l); })
        .map(function (l) { return l.split(':')[0].trim(); }).filter(function (t) { return !/^\./.test(t); });
      var want = p.rest[0] || targets[0] || '';
      var cmds = [];
      text.split('\n').forEach(function (l) {
        if (/^\t/.test(l)) cmds.push(l.replace(/^\t+/, ''));
      });
      if (!want) return bad('make: *** No targets.  Stop.');
      var out = [];
      if (cmds.indexOf('gcc') >= 0) {}
      cmds.forEach(function (c) {
        out.push(c);
        if (ctx.exec) {
          var r = ctx.exec(splitCmd(c));
          if (r.out) out.push(r.out.replace(/\n$/, ''));
          if (r.err) out.push(r.err.replace(/\n$/, ''));
        }
      });
      return ok(out.join('\n'));
    };
    function splitCmd(s) { return s.match(/(?:[^\s"']+|"[^"]*"|'[^']*')+/g) || []; }

    function svcTable(fs) {
      if (fs.services) return fs.services;
      fs.services = {
        sshd: { load: 'loaded', active: 'active', sub: 'running', desc: 'OpenSSH server daemon' },
        firewalld: { load: 'loaded', active: 'active', sub: 'running', desc: 'firewalld - dynamic firewall daemon' },
        httpd: { load: 'loaded', active: 'inactive', sub: 'dead', desc: 'The Apache HTTP Server' },
        crond: { load: 'loaded', active: 'active', sub: 'running', desc: 'Command Scheduler' },
        NetworkManager: { load: 'loaded', active: 'active', sub: 'running', desc: 'Network Manager' },
        'sshd.service': null
      };
      delete fs.services['sshd.service'];
      return fs.services;
    }
    function normSvc(n) { return String(n).replace(/\.service$/, ''); }

    CMD.systemctl = function (fs, argv) {
      var p = parseFlags(argv, { val: '', long: { 'no-pager': '', 'now': '' } });
      var sub = p.rest[0] || 'list-units';
      var name = normSvc(p.rest[1] || '');
      var svcs = svcTable(fs);

      if (sub === 'status') {
        if (!name) return bad('Too few arguments.');
        var s = svcs[name];
        if (!s) return { out: 'Unit ' + name + '.service could not be found.', err: '', code: 4 };
        return ok([
          '○ ' + name + '.service - ' + s.desc,
          '     Loaded: loaded (/usr/lib/systemd/system/' + name + '.service; enabled; preset: disabled)',
          '     Active: ' + s.active + ' (' + s.sub + ') since Wed 2025-11-05 09:12:01 CST; 8min ago',
          '   Main PID: 1' + (100 + name.length) + ' (' + name + ')',
          '      Tasks: 1 (limit: 4567)',
          '     Memory: 4.2M',
          '        CPU: 42ms'
        ].join('\n'));
      }
      if (sub === 'start' || sub === 'stop' || sub === 'restart' || sub === 'reload' || sub === 'enable' || sub === 'disable') {
        if (!name) return bad('Too few arguments.');
        if (!svcs[name]) {
          if (sub === 'enable' || sub === 'disable') {
            return bad('Failed to enable unit: Unit file ' + name + '.service does not exist.');
          }
          return bad('Failed to ' + sub + ' ' + name + '.service: Unit ' + name + '.service not found.');
        }
        if (sub === 'start' || sub === 'restart') { svcs[name].active = 'active'; svcs[name].sub = 'running'; }
        if (sub === 'stop') { svcs[name].active = 'inactive'; svcs[name].sub = 'dead'; }
        /* enable/disable 要真的留下痕迹：学生查 is-enabled 时得对得上 */
        svcs[name].enabled = (sub === 'enable') ? true : (sub === 'disable' ? false : svcs[name].enabled);
        return ok('');
      }
      if (sub === 'is-active') {
        var s2 = svcs[name];
        return { out: s2 ? s2.active : 'inactive', err: '', code: s2 && s2.active === 'active' ? 0 : 3 };
      }
      if (sub === 'is-enabled') {
        var s3 = svcs[name];
        return { out: s3 ? (s3.enabled === false ? 'disabled' : 'enabled') : 'not-found', err: '', code: s3 ? 0 : 1 };
      }
      if (sub === 'list-units' || sub === 'list-unit-files' || !sub) {
        var short = sub === 'list-unit-files';
        if (short) {
          var rows2 = ['UNIT FILE                    STATE    PRESET'];
          Object.keys(svcs).forEach(function (k) {
            rows2.push(lpad(k + '.service', 30) + ' ' + lpad((svcs[k].enabled === false ? 'disabled' : 'enabled'), 8) + '   disabled');
          });
          return ok(rows2.join('\n'));
        }
        var rows = ['  UNIT                 LOAD   ACTIVE SUB     DESCRIPTION'];
        Object.keys(svcs).forEach(function (k) {
          var s4 = svcs[k];
          rows.push('  ' + lpad(k + '.service', 21) + lpad(s4.load, 7) + lpad(s4.active, 7) + lpad(s4.sub, 8) + ' ' + s4.desc);
        });
        rows.push('');
        rows.push(Object.keys(svcs).length + ' loaded units listed.');
        return ok(rows.join('\n'));
      }
      if (sub === 'daemon-reload') return ok('');
      return bad('Unknown command verb ' + sub + '.');
    };

    CMD.journalctl = function (fs, argv) {
      var p = parseFlags(argv, { val: 'un', long: { 'unit': 'u', 'lines': 'n', 'no-pager': '', 'follow': 'f', 'since': '' } });
      var out = [
        'Nov 05 09:12:01 fedora systemd[1]: Starting systemd-journald.service...',
        'Nov 05 09:12:01 fedora systemd[1]: Started systemd-journald.service.',
        'Nov 05 09:12:01 fedora systemd[1]: Reached target Local File Systems.',
        'Nov 05 09:12:02 fedora systemd[1]: Starting Network Manager...',
        'Nov 05 09:12:03 fedora NetworkManager[998]: <info>  [1762305122.5] device (ens160): state change: activated',
        'Nov 05 09:12:03 fedora systemd[1]: Reached target Network is Online.',
        'Nov 05 09:12:04 fedora sshd[1201]: Server listening on 0.0.0.0 port 22.',
        'Nov 05 09:12:05 fedora systemd[1]: Reached target graphical.target - Graphical Interface.',
        'Nov 05 09:19:40 fedora systemd[1]: Starting dnf makecache...',
        'Nov 05 09:19:58 fedora systemd[1]: dnf-makecache.service: Deactivated successfully.'
      ];
      if (p.o.n) out = out.slice(-parseInt(p.o.n, 10));
      return ok(out.join('\n'));
    };

    CMD.wall = function (fs, argv) { return ok(''); };
    CMD.man = function (fs, argv) {
      if (!argv.length) return bad('What manual page do you want?\nFor example, try \'man man\'.');
      return ok(argv[0].toUpperCase() + '(1)                    User Commands                    ' + argv[0].toUpperCase() + '(1)\n\nNAME\n    ' +
        argv[0] + ' - （沙箱内不提供 man 手册，请查讲义对应小节）\n\nSEE ALSO\n    ' +
        '讲义《' + argv[0] + '》那一节');
    };
    CMD.help = function (fs, argv) {
      return ok('沙箱支持的命令：\n' + Object.keys(CMD).filter(function (k) { return k.charAt(0) !== '_' && k !== '__h'; }).sort().join(' '));
    };

    return CMD;
  }

  return { install: install };
});
