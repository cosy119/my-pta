/* ===========================================================================
   Linux 命令沙箱（第 1 部分）—— 虚拟文件系统 + shell 解析
   命令实现见 linux-shell-cmds.js
   =========================================================================== */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.LinuxShellCore = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var T = { DIR: 'd', FILE: 'f', LINK: 'l' };

  /* ★ 时间必须固定。用 Date.now() 的话同一道题每次刷新 `ls -l` 显示的月份都不同，
     学生截图对不上，自动化测试也没法断言。 */
  var BASE_TIME = 1762300800;  // 2025-11-05 09:20 左右的某个整数秒

  function node(t, mode, uid, gid, extra) {
    var n = { t: t, m: mode, u: uid, g: gid, mt: BASE_TIME };
    if (extra) for (var k in extra) n[k] = extra[k];
    return n;
  }
  function dir(mode, uid, gid) { return node(T.DIR, mode == null ? 0o755 : mode, uid || 0, gid || 0, { ch: {} }); }
  function file(content, mode, uid, gid) {
    return node(T.FILE, mode == null ? 0o644 : mode, uid, gid, { c: content == null ? '' : content });
  }
  function link(target) { return node(T.LINK, 0o777, 0, 0, { k: target }); }
  function put(parent, name, child) { parent.ch[name] = child; return child; }
  function putPath(rootDir, path, child) {
    var parts = path.split('/').filter(Boolean);
    var cur = rootDir;
    for (var i = 0; i < parts.length - 1; i++) {
      var nm = parts[i];
      if (!cur.ch[nm]) cur.ch[nm] = dir(0o755, 0, 0);
      cur = cur.ch[nm];
    }
    return put(cur, parts[parts.length - 1], child);
  }

  /* -------------------------------------------------------------------------
     初始镜像：一台刚装好的 Fedora 44 Workstation
     ★ 这里放什么直接决定学生能做什么题。改动前先对一遍题库。
     ------------------------------------------------------------------------- */
  function buildImage(opts) {
    opts = opts || {};
    var user = opts.user || 'student';
    var uid = opts.uid || 1000;

    var root = dir(0o755, 0, 0);

    ['dev', 'proc', 'run', 'srv', 'mnt', 'media', 'opt', 'sys'].forEach(function (n) {
      put(root, n, dir(0o755, 0, 0));
    });
    /* /dev 下的几个设备文件必须存在且可写：`cmd 2>/dev/null` 是题库里
       出现频率最高的写法之一，没有 /dev/null 这条命令会直接报权限错。 */
    ['null', 'zero', 'tty', 'random', 'urandom'].forEach(function (n) {
      var f = file('', 0o666, 0, 0);
      f.sink = true;                 // 写进去就丢，不留内容
      put(root.ch.dev, n, f);
    });
    put(root, 'tmp', dir(0o1777, 0, 0));       // sticky bit —— /tmp 的标志
    put(root, 'root', dir(0o550, 0, 0));
    put(root, 'home', dir(0o755, 0, 0));
    put(root, 'boot', dir(0o755, 0, 0));
    put(root, 'etc', dir(0o755, 0, 0));
    put(root, 'var', dir(0o755, 0, 0));
    put(root, 'usr', dir(0o755, 0, 0));

    /* usrMerge：Fedora 的 /bin /sbin /lib /lib64 都是指向 /usr 的软链 */
    put(root, 'bin', link('/usr/bin'));
    put(root, 'sbin', link('/usr/sbin'));
    put(root, 'lib', link('/usr/lib'));
    put(root, 'lib64', link('/usr/lib64'));

    /* ---- /usr ---- */
    var usr = root.ch.usr;
    ['bin', 'sbin', 'lib', 'lib64', 'share', 'include', 'src', 'local'].forEach(function (n) {
      put(usr, n, dir(0o755, 0, 0));
    });
    var local = usr.ch.local;
    ['bin', 'games', 'lib', 'src'].forEach(function (n) { put(local, n, dir(0o755, 0, 0)); });
    putPath(local, 'share/applications', dir(0o755, 0, 0));

    /* 【实验 2 第 1 题】/usr/local/bin 里要真有东西，否则 ls 一片空白，学生以为环境坏了 */
    put(usr.ch.bin, 'bash', file('ELF', 0o755, 0, 0));
    put(usr.ch.bin, 'ls', file('ELF', 0o755, 0, 0));
    put(usr.ch.bin, 'cat', file('ELF', 0o755, 0, 0));
    put(usr.ch.bin, 'gcc', file('ELF', 0o755, 0, 0));
    put(local.ch.bin, 'custom-tool', file('#!/bin/sh\necho hi\n', 0o755, 0, 0));
    put(local.ch.bin, 'backup.sh', file('#!/bin/bash\ntar czf /tmp/bak.tgz /etc\n', 0o755, 0, 0));
    put(local.ch.games, 'sol', file('ELF', 0o755, 0, 0));

    /* ---- /etc ---- */
    var etc = root.ch.etc;

    /* 【实验 2 第 7 题】 */
    put(etc, 'shells', file('/bin/sh\n/bin/bash\n/usr/bin/sh\n/usr/bin/bash\n/usr/bin/tmux\n', 0o644, 0, 0));
    /* 【实验 1】沙箱里也照真机写，方便对照 */
    put(etc, 'os-release', file(
      'NAME="Fedora Linux"\nVERSION="44 (Workstation Edition)"\nID=fedora\nVERSION_ID=44\n' +
      'PLATFORM_ID="platform:f44"\nPRETTY_NAME="Fedora Linux 44 (Workstation Edition)"\n' +
      'ANSI_COLOR="0;38;2;60;110;180"\nLOGO=fedora-logo-icon\n' +
      'HOME_URL="https://fedoraproject.org/"\nVARIANT="Workstation Edition"\nVARIANT_ID=workstation\n',
      0o644, 0, 0));
    put(etc, 'hostname', file('fedora\n', 0o644, 0, 0));
    put(etc, 'hosts', file('127.0.0.1   localhost localhost.localdomain\n::1         localhost\n', 0o644, 0, 0));
    put(etc, 'redhat-release', file('Fedora release 44 (Workstation Edition)\n', 0o644, 0, 0));
    put(etc, 'fstab', file(
      'UUID=8d1f3a2e-6b4c-4a71-9e0d-2c5b8f7a1d34 /         xfs  defaults        0 0\n' +
      'UUID=A1B2-C3D4                            /boot/efi vfat umask=0077 0 2\n', 0o644, 0, 0));

    /* 【实验 2 第 9 题】 */
    var ssh = put(etc, 'ssh', dir(0o700, 0, 0));
    put(ssh, 'ssh_config', file(
      '# $OpenBSD: ssh_config,v 1.35 $\n' +
      '# This is the ssh client system-wide configuration file.\n' +
      'Include /etc/ssh/ssh_config.d/*.conf\n\n' +
      'Host *\n' +
      '#   ForwardAgent no\n' +
      '#   ForwardX11 no\n' +
      '#   PasswordAuthentication yes\n' +
      '#   StrictHostKeyChecking ask\n' +
      '   Ciphers aes128-ctr,aes192-ctr,aes256-ctr\n' +
      '#   SendEnv LANG LC_*\n' +
      '#   HashKnownHosts yes\n', 0o600, 0, 0));
    put(ssh, 'ssh_config.d', dir(0o700, 0, 0));

    /* 用户库的真相就在这三个文件里 —— 所有用户/组命令最后都要回写它们 */
    put(etc, 'passwd', file('', 0o644, 0, 0));
    put(etc, 'group', file('', 0o644, 0, 0));
    put(etc, 'shadow', file('', 0o000, 0, 0));   // ★ 000：普通用户读不了，这是真机行为
    put(etc, 'gshadow', file('', 0o000, 0, 0));
    put(etc, 'login.defs', file(
      'MAIL_DIR        /var/spool/mail\nCREATE_HOME     yes\nUID_MIN         1000\nUID_MAX         60000\n' +
      'GID_MIN         1000\nGID_MAX         60000\nUMASK           022\nHOME_MODE       0700\n', 0o644, 0, 0));

    /* ---- /boot（实验 3 第 6 题要 cp /boot/vmlinuz*）---- */
    var boot = root.ch.boot;
    put(boot, 'vmlinuz-7.1.12-200.fc44.x86_64', file('ELF kernel image', 0o755, 0, 0));
    put(boot, 'initramfs-7.1.12-200.fc44.x86_64.img', file('initramfs', 0o600, 0, 0));
    /* config 在真机是 644（普通用户读得到），initramfs 才是 600 */
    put(boot, 'config-7.1.12-200.fc44.x86_64', file('CONFIG_X86_64=y\n', 0o644, 0, 0));
    put(boot, 'grub2', dir(0o700, 0, 0));
    putPath(root, 'boot/efi/EFI/fedora', dir(0o700, 0, 0));

    /* ---- /var ---- */
    var varr = root.ch.var;
    ['cache', 'db', 'spool', 'tmp', 'lib', 'opt'].forEach(function (n) { put(varr, n, dir(0o755, 0, 0)); });
    var log = put(varr, 'log', dir(0o755, 0, 0));
    put(log, 'messages', file(
      'Nov  5 09:12:01 fedora systemd[1]: Started dbus.service.\n' +
      'Nov  5 09:12:03 fedora systemd[1]: Reached target graphical.target.\n', 0o644, 0, 0));
    put(log, 'dnf.log', file(
      '2025-11-05T09:10:22+0800 INFO --- logging initialized ---\n' +
      '2025-11-05T09:10:22+0800 DEBUG timer: config: 12 ms\n', 0o644, 0, 0));
    put(log, 'secure', file('Nov  5 09:12:01 fedora sshd[1201]: Server listening on 0.0.0.0 port 22.\n', 0o600, 0, 0));
    put(log, 'boot.log', file('', 0o644, 0, 0));

    /* ---- /home/<user> ---- */
    var home = root.ch.home;
    var me = put(home, user, dir(0o700, uid, uid));
    put(me, '.bashrc', file(
      '# .bashrc\nif [ -f /etc/bashrc ]; then\n\t. /etc/bashrc\nfi\n\nalias ll=\'ls -l\'\n',
      0o644, uid, uid));
    put(me, '.bash_profile', file(
      '# .bash_profile\nif [ -f ~/.bashrc ]; then\n\t. ~/.bashrc\nfi\n\nPATH=$PATH:$HOME/.local/bin:$HOME/bin\nexport PATH\n',
      0o644, uid, uid));
    put(me, '.bash_logout', file('# ~/.bash_logout\n', 0o644, uid, uid));
    put(me, '.config', dir(0o700, uid, uid));
    put(me, '.cache', dir(0o700, uid, uid));
    var md = put(me, '.local', dir(0o700, uid, uid));
    put(md, 'share', dir(0o755, uid, uid));
    /* 中文桌面环境会建这几个目录，实验 4 的 Eclipse 那题要用「下载」 */
    put(me, '下载', dir(0o755, uid, uid));
    put(me, '文档', dir(0o755, uid, uid));
    put(me, '桌面', dir(0o755, uid, uid));
    put(me, '图片', dir(0o755, uid, uid));

    var fs = {
      root: root,
      user: user,          // 这台机器的普通用户（登录名）
      uid: uid,
      gid: uid,
      cwd: '/home/' + user,
      prevCwd: '/home/' + user,
      users: {},
      groups: {},
      env: {
        HOME: '/home/' + user, USER: user, LOGNAME: user, SHELL: '/bin/bash',
        PWD: '/home/' + user, PATH: '/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin',
        HOSTNAME: 'fedora', LANG: 'zh_CN.UTF-8', TERM: 'xterm-256color'
      },
      history: [],
      lastCode: 0,
      clock: BASE_TIME
    };

    [{ n: 'root', uid: 0, gid: 0, h: '/root', s: '/bin/bash', g: 'root' },
     { n: 'bin', uid: 1, gid: 1, h: '/bin', s: '/sbin/nologin', g: 'bin' },
     { n: 'daemon', uid: 2, gid: 2, h: '/sbin', s: '/sbin/nologin', g: 'daemon' },
     { n: 'adm', uid: 3, gid: 4, h: '/var/adm', s: '/sbin/nologin', g: 'adm' },
     { n: 'nobody', uid: 65534, gid: 65534, h: '/', s: '/sbin/nologin', g: 'nobody' }
    ].forEach(function (x) {
      fs.users[x.n] = { uid: x.uid, gid: x.gid, home: x.h, shell: x.s, gecos: x.n };
    });
    fs.users[user] = { uid: uid, gid: uid, home: '/home/' + user, shell: '/bin/bash', gecos: user };

    [{ n: 'root', gid: 0, m: [] }, { n: 'bin', gid: 1, m: [] }, { n: 'daemon', gid: 2, m: [] },
     { n: 'sys', gid: 3, m: [] }, { n: 'adm', gid: 4, m: [] },
     { n: 'wheel', gid: 10, m: [user] }, { n: 'nobody', gid: 65534, m: [] }
    ].forEach(function (x) { fs.groups[x.n] = { gid: x.gid, members: x.m.slice() }; });
    fs.groups[user] = { gid: uid, members: [] };

    return fs;
  }

  /* 把 fs.users / fs.groups 回写到 /etc/passwd 与 /etc/group。
     所有改用户/组的命令收尾都要调 —— 这样「tail /etc/passwd 能看到」才成立。 */
  function rewriteAccounts(fs) {
    var names = Object.keys(fs.users).sort(function (a, b) { return fs.users[a].uid - fs.users[b].uid; });
    fs.root.ch.etc.ch.passwd.c = names.map(function (n) {
      var u = fs.users[n];
      return [n, 'x', u.uid, u.gid, u.gecos || n, u.home, u.shell].join(':');
    }).join('\n') + '\n';

    var gn = Object.keys(fs.groups).sort(function (a, b) { return fs.groups[a].gid - fs.groups[b].gid; });
    fs.root.ch.etc.ch.group.c = gn.map(function (n) {
      var g = fs.groups[n];
      return [n, 'x', g.gid, g.members.join(',')].join(':');
    }).join('\n') + '\n';
  }

  /* =========================================================================
     路径与权限
     ========================================================================= */

  function normalize(cwd, p) {
    if (p == null || p === '') p = '.';
    var abs = p.charAt(0) === '/' ? p : cwd.replace(/\/+$/, '') + '/' + p;
    var parts = abs.split('/'), out = [];
    for (var i = 0; i < parts.length; i++) {
      var s = parts[i];
      if (s === '' || s === '.') continue;
      if (s === '..') { out.pop(); continue; }
      out.push(s);
    }
    return '/' + out.join('/');
  }

  /* 按绝对路径找节点；follow=true 时沿软链走（最多 8 跳防环） */
  function lookup(fs, absPath, follow) {
    if (follow === undefined) follow = true;
    var parts = absPath.split('/').filter(Boolean);
    var cur = fs.root, hops = 0;
    for (var i = 0; i < parts.length; i++) {
      if (cur.t === T.LINK && follow) {
        if (++hops > 8) return null;
        cur = lookup(fs, normalize('/', cur.k), true);
        if (!cur) return null;
      }
      if (cur.t !== T.DIR) return null;
      var nm = parts[i];
      if (!Object.prototype.hasOwnProperty.call(cur.ch, nm)) return null;
      cur = cur.ch[nm];
    }
    return cur;
  }

  /* 找节点 + 它的父目录（rm / mv / chmod 都要） */
  function locate(fs, absPath) {
    var parts = absPath.split('/').filter(Boolean);
    if (!parts.length) return { parent: null, name: '', node: fs.root };
    var name = parts[parts.length - 1];
    var parent = lookup(fs, '/' + parts.slice(0, -1).join('/'), true);
    if (!parent || parent.t !== T.DIR) return { parent: null, name: name, node: null };
    var nd = Object.prototype.hasOwnProperty.call(parent.ch, name) ? parent.ch[name] : null;
    return { parent: parent, name: name, node: nd };
  }

  /* 权限位 → rwx 串。setuid/setgid/sticky 的显示规则跟 ls 一致：
     带 x 显示小写 s/t，不带 x 显示大写 S/T */
  function modeString(mode) {
    var rwx = function (b) {
      return ((b & 4) ? 'r' : '-') + ((b & 2) ? 'w' : '-') + ((b & 1) ? 'x' : '-');
    };
    var u = rwx((mode >> 6) & 7), g = rwx((mode >> 3) & 7), o = rwx(mode & 7);
    if (mode & 0o4000) u = u.slice(0, 2) + ((mode & 0o100) ? 's' : 'S');
    if (mode & 0o2000) g = g.slice(0, 2) + ((mode & 0o010) ? 's' : 'S');
    if (mode & 0o1000) o = o.slice(0, 2) + ((mode & 0o001) ? 't' : 'T');
    return '-' + u + g + o;
  }

  function isRoot(fs) { return fs.uid === 0; }

  function userNameOf(fs, uid) {
    for (var n in fs.users) if (fs.users[n].uid === uid) return n;
    return null;
  }
  function groupNameOf(fs, gid) {
    for (var n in fs.groups) if (fs.groups[n].gid === gid) return n;
    return null;
  }
  function inGroup(fs, uid, gid) {
    var name = userNameOf(fs, uid);
    if (!name) return false;
    for (var g in fs.groups) {
      if (fs.groups[g].gid === gid && fs.groups[g].members.indexOf(name) >= 0) return true;
    }
    return false;
  }

  /* 有没有某权限。root 绕过读写检查，但执行位仍然要至少一个 x（真机如此） */
  function permitted(fs, nd, want) {
    if (!nd) return false;
    if (isRoot(fs)) {
      if (want === 'x') return nd.t === T.DIR || !!(nd.m & 0o111);
      return true;
    }
    var bits;
    if (fs.uid === nd.u) bits = (nd.m >> 6) & 7;
    else if (fs.gid === nd.g || inGroup(fs, fs.uid, nd.g)) bits = (nd.m >> 3) & 7;
    else bits = nd.m & 7;
    return !!(bits & (want === 'r' ? 4 : want === 'w' ? 2 : 1));
  }

  /* =========================================================================
     分词：返回 {v, q} —— q 记录这个 token 的引号性质
     -------------------------------------------------------------------------
     ★ q 的用途只有一个：决定要不要做变量展开。
       单引号里一律不展开（echo '$HOME' 打印字面量），双引号和裸词都展开。
     ========================================================================= */
  function tokenize(line) {
    var toks = [], cur = '', has = false;
    var sawSingle = false, sawExpandable = false;
    var i = 0, quote = null;

    function flush() {
      if (!has) return;
      var q = (sawSingle && !sawExpandable) ? "'" : (sawSingle ? 'm' : '');
      toks.push({ v: cur, q: q });
      cur = ''; has = false; sawSingle = false; sawExpandable = false;
    }

    while (i < line.length) {
      var ch = line[i];
      if (quote) {
        if (ch === quote) { quote = null; i++; continue; }
        if (quote === '"' && ch === '\\' && i + 1 < line.length) {
          var nx = line[i + 1];
          if (nx === '"' || nx === '\\' || nx === '$' || nx === '`') { cur += nx; i += 2; sawExpandable = true; continue; }
          cur += ch; i++; continue;
        }
        cur += ch; i++; continue;
      }
      if (ch === "'") { quote = "'"; has = true; sawSingle = true; sawExpandable = sawExpandable; i++; continue; }
      if (ch === '"') { quote = '"'; has = true; sawExpandable = true; i++; continue; }
      if (ch === '\\' && i + 1 < line.length) { cur += line[i + 1]; has = true; sawExpandable = true; i += 2; continue; }
      if (ch === ' ' || ch === '\t') { flush(); i++; continue; }

      /* ★ 三个字符的要先判：`2>>` 一旦被 `2>` 抢走，剩下的 `>` 会变成
         一个独立的重定向操作符，整条命令就歪了。 */
      var three = line.substr(i, 3);
      if (three === '2>>') { flush(); toks.push({ v: '2>>', q: '@' }); i += 3; continue; }
      var two = line.substr(i, 2);
      if (two === '&&' || two === '||' || two === '>>' || two === '<<' || two === '2>' || two === '&>') {
        flush(); toks.push({ v: two, q: '@' }); i += 2; continue;
      }
      if (ch === '>' || ch === '<' || ch === '|' || ch === ';') {
        flush(); toks.push({ v: ch, q: '@' }); i++; continue;
      }
      cur += ch; has = true; sawExpandable = true; i++;
    }
    flush();
    return toks;
  }

  var isOp = function (t) { return t.q === '@'; };

  /* 把 token 流切成「简单命令段 + 段间连接符」 */
  function parsePipelines(toks) {
    var segs = [], seps = [];
    var cur = { argv: [], redir: {} };
    var i = 0;
    while (i < toks.length) {
      var t = toks[i];
      if (isOp(t) && (t.v === '|' || t.v === ';' || t.v === '&&' || t.v === '||')) {
        segs.push(cur); seps.push(t.v);
        cur = { argv: [], redir: {} };
        i++; continue;
      }
      if (isOp(t) && (t.v === '>' || t.v === '>>' || t.v === '2>' || t.v === '2>>' || t.v === '<')) {
        var target = toks[i + 1];
        var tv = target ? target.v : '';
        if (t.v === '<') cur.redir.in = tv;
        else if (t.v === '2>' || t.v === '2>>') { cur.redir.err = tv; cur.redir.errAppend = (t.v === '2>>'); }
        else { cur.redir.out = tv; cur.redir.outAppend = (t.v === '>>'); }
        i += 2; continue;
      }
      cur.argv.push(t.v);
      i++;
    }
    if (cur.argv.length || cur.redir.out != null || cur.redir.in != null) segs.push(cur);
    return { segs: segs, seps: seps };
  }

  /* =========================================================================
     变量展开与算术求值
     ========================================================================= */

  /* ★ 动态变量：值会随执行过程变化（`$?` 是上一条的退出码，`$PWD` 跟着 cd 走）。
     展开发生在**解析阶段**（整行 tokenize 完就展开），而命令是**之后**才逐条执行的
     —— 如果直接取当前值，`cd /tmp && echo $PWD` 打印的还是旧目录，
     `ls /nope; echo $?` 永远是 0。所以解析阶段先落一个占位符，
     每段命令执行前再用 resolveDynamic() 换成此刻的真值。
     `\u0001` 是不可打印字符，正常命令里不会出现，拿它当分隔最省事。 */
  var DYN = '\u0001';
  function dynMark(name) { return DYN + name + DYN; }

  function resolveDynamic(fs, s) {
    if (typeof s !== 'string' || s.indexOf(DYN) < 0) return s;
    return s.replace(/\u0001([?A-Za-z_][A-Za-z0-9_]*)\u0001/g, function (m, k) {
      if (k === '?') return String(fs.lastCode);
      if (k === 'PWD') return fs.cwd;
      if (k === 'OLDPWD') return fs.prevCwd || fs.env.HOME || '';
      return fs.env[k] == null ? '' : String(fs.env[k]);
    });
  }

  /* $VAR ${VAR} $? $$ $((算术)) $(命令) —— $(命令) 只支持最简单的 `$(cmd)` 形式 */
  function expandVars(fs, s, depth) {
    depth = depth || 0;
    if (depth > 4) return s;
    var out = '', i = 0;
    while (i < s.length) {
      var ch = s[i];
      if (ch !== '$') { out += ch; i++; continue; }
      var nx = s[i + 1];
      if (nx === '(' && s[i + 2] === '(') {
        var end = s.indexOf('))', i + 3);
        if (end < 0) { out += ch; i++; continue; }
        out += String(arith(s.slice(i + 3, end), fs));
        i = end + 2; continue;
      }
      if (nx === '(') {
        var e2 = matchParen(s, i + 1);
        if (e2 < 0) { out += ch; i++; continue; }
        out += String(fs.lastCode);   // 简化：$(...) 求值不了就退化成退出码
        i = e2 + 1; continue;
      }
      if (nx === '{') {
        var e3 = s.indexOf('}', i + 2);
        if (e3 < 0) { out += ch; i++; continue; }
        var name = s.slice(i + 2, e3);
        out += dynMark(name);
        i = e3 + 1; continue;
      }
      if (nx === '?') { out += dynMark('?'); i += 2; continue; }
      if (nx === '$') { out += '1'; i += 2; continue; }
      if (nx === '#') { out += '1'; i += 2; continue; }
      if (nx === '@' || nx === '*' || nx === '0' || nx === '1') { out += ''; i += 2; continue; }
      var m = /^[A-Za-z_][A-Za-z0-9_]*/.exec(s.slice(i + 1));
      if (m) { out += dynMark(m[0]); i += 1 + m[0].length; continue; }
      out += ch; i++;
    }
    return out;
  }

  function envGet(fs, name) {
    if (Object.prototype.hasOwnProperty.call(fs.env, name)) return String(fs.env[name]);
    return '';
  }

  function matchParen(s, open) {
    var d = 0;
    for (var i = open; i < s.length; i++) {
      if (s[i] === '(') d++;
      else if (s[i] === ')') { d--; if (d === 0) return i; }
    }
    return -1;
  }

  /* bash 算术：支持 + - * / % ** 括号 变量，整数除法向零截断 */
  function arith(expr, fs) {
    var src = String(expr).replace(/\$?\{?([A-Za-z_][A-Za-z0-9_]*)\}?/g, function (all, name) {
      if (['x', 'e'].indexOf(name) >= 0) return name;
      var v = envGet(fs, name);
      if (v !== '' && /^-?\d+$/.test(v)) return v;
      return Object.prototype.hasOwnProperty.call(fs.shellVars || {}, name) ? String(fs.shellVars[name]) : '0';
    });
    var tokens = src.match(/\d+|[-+*/%()]|\*\*|[A-Za-z_][A-Za-z0-9_]*/g);
    if (!tokens) return 0;
    var pos = 0;
    function peek() { return tokens[pos]; }
    function next() { return tokens[pos++]; }

    function primary() {
      var t = next();
      if (t === '(') { var v = addsub(); next(); return v; }
      if (t === '-') return -primary();
      if (t === '+') return primary();
      if (t && /^\d+$/.test(t)) return parseInt(t, 10);
      return 0;
    }
    function power() {
      var b = primary();
      if (peek() === '**') { next(); return Math.pow(b, power()); }
      return b;
    }
    function muldiv() {
      var v = power();
      while (peek() === '*' || peek() === '/' || peek() === '%') {
        var op = next(), r = power();
        if (op === '*') v = v * r;
        else if (op === '/') v = r === 0 ? 0 : Math.trunc(v / r);
        else v = r === 0 ? 0 : v % r;
      }
      return v;
    }
    function addsub() {
      var v = muldiv();
      while (peek() === '+' || peek() === '-') {
        var op = next(), r = muldiv();
        v = op === '+' ? v + r : v - r;
      }
      return v;
    }
    return addsub();
  }

  return {
    T: T, BASE_TIME: BASE_TIME,
    node: node, dir: dir, file: file, link: link, put: put, putPath: putPath,
    buildImage: buildImage, rewriteAccounts: rewriteAccounts,
    normalize: normalize, lookup: lookup, locate: locate,
    modeString: modeString, permitted: permitted, isRoot: isRoot,
    userNameOf: userNameOf, groupNameOf: groupNameOf, inGroup: inGroup,
    tokenize: tokenize, parsePipelines: parsePipelines,
    expandVars: expandVars, arith: arith, envGet: envGet, isOp: isOp,
    resolveDynamic: resolveDynamic
  };
});
