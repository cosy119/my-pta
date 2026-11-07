/* 命令沙箱的 node 侧自检。
   跑法：node tools/test_linux_shell.mjs
   ★ 这里断言的都是「学生在题里会敲的那几十条命令」，
     不是实现细节 —— 沙箱改实现可以，但这批行为不能变。 */
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);

const S = require('../web/linux-shell.js');

let pass = 0, fail = 0;
const fails = [];

function eq(name, got, want) {
  var g = String(got == null ? '' : got).replace(/\s+$/, '');
  var w = String(want == null ? '' : want).replace(/\s+$/, '');
  if (g === w) { pass++; return; }
  fail++;
  fails.push({ name, got: g, want: w });
}
function has(name, got, needle) {
  if (String(got).indexOf(needle) >= 0) { pass++; return; }
  fail++;
  fails.push({ name, got: String(got), want: '（应包含）' + needle });
}
function code(name, got, want) {
  if (got === want) { pass++; return; }
  fail++;
  fails.push({ name, got: 'exit=' + got, want: 'exit=' + want });
}

function fresh() { S.reset(); return S; }

/* ---------------- 基本命令 ---------------- */
fresh();
eq('pwd 初始', S.exec('pwd').out, '/home/student');
eq('whoami', S.exec('whoami').out, 'student');
eq('ls 家目录有 .bashrc', S.exec('ls -a | grep .bashrc').out, '.bashrc');
eq('ls -l 长格式首列', S.exec('ls -l .bashrc').out.split('\n')[0].slice(0, 1), '-');
has('ls -l 显示属主', S.exec('ls -l .bashrc').out, 'student');
eq('cd /usr 后 pwd', (S.exec('cd /usr'), S.exec('pwd').out), '/usr');
eq('cd ../.. 相对路径', (S.exec('cd /usr/local/bin'), S.exec('cd ../..'), S.exec('pwd').out), '/usr');
eq('cd ~ 回家', (S.exec('cd /'), S.exec('cd ~'), S.exec('pwd').out), '/home/student');
code('cd 不存在目录', S.exec('cd /nope').code, 1);
has('cd 报错文案', S.exec('cd /nope').err, 'No such file or directory');

/* ---------------- 文件操作真改状态 ---------------- */
fresh();
S.exec('mkdir -p ~/work/sub');
eq('mkdir -p 建两层', S.exec('test 2>/dev/null; ls -d ~/work/sub').out, '/home/student/work/sub');
eq('touch 建文件', (S.exec('touch ~/work/a.txt'), S.exec('ls ~/work').out), 'a.txt\nsub');
eq('echo 重定向写文件', (S.exec('echo hello > ~/work/b.txt'), S.exec('cat ~/work/b.txt').out), 'hello');
eq('>> 追加', (S.exec('echo world >> ~/work/b.txt'), S.exec('cat ~/work/b.txt').out), 'hello\nworld');
eq('cp 复制', (S.exec('cp ~/work/b.txt ~/work/c.txt'), S.exec('cat ~/work/c.txt').out), 'hello\nworld');
eq('mv 改名', (S.exec('mv ~/work/c.txt ~/work/d.txt'), S.exec('ls ~/work | sort').out), 'a.txt\nb.txt\nd.txt\nsub');
eq('rm 删文件', (S.exec('rm ~/work/d.txt'), S.exec('ls ~/work | grep -c d.txt').code), 1);
code('rm 非空目录报错', S.exec('rm ~/work').code, 1);
eq('rmdir 非空报错', (S.exec('rmdir ~/work').err.indexOf('Directory not empty') >= 0 ? 1 : 0), 1);
eq('rm -rf 递归删', (S.exec('rm -rf ~/work'), S.exec('ls ~/work').err.indexOf('No such file') >= 0 ? 1 : 0), 1);
eq('ln -s 建软链', (S.exec('ln -s /etc/hostname ~/hn'), S.exec('ls -l ~/hn').out.indexOf('-> /etc/hostname') >= 0 ? 1 : 0), 1);
eq('readlink 读软链', S.exec('readlink ~/hn').out, '/etc/hostname');

/* ---------------- 查看内容 ---------------- */
fresh();
eq('cat -n 行号', S.exec('cat -n /boot/config-7.1.12-200.fc44.x86_64').out, '     1\tCONFIG_X86_64=y');
eq('head -3 取前 3 行', S.exec('cat /etc/os-release | head -3').out.trim().split('\n').length, 3);
eq('tail -1', S.exec('tail -1 /etc/shells').out, '/usr/bin/tmux');
eq('wc -l', S.exec('wc -l /etc/shells').out.split(/\s+/)[0], '5');
eq('wc -w', S.exec('echo one two three | wc -w').out.split(/\s+/)[0], '3');
eq('nl 编号', S.exec('nl /etc/hostname').out, '     1\tfedora');
eq('sort 排序', S.exec('printf "b\\na\\nc\\n" | sort').out, 'a\nb\nc');
eq('sort -r', S.exec('printf "b\\na\\nc\\n" | sort -r').out, 'c\nb\na');
eq('sort -n 数值', S.exec('printf "10\\n9\\n100\\n" | sort -n').out, '9\n10\n100');
eq('uniq -c 计数', S.exec('printf "a\\na\\nb\\n" | sort | uniq -c').out.trim().split('\n').map(function(l){return l.trim();}).join('|'), '2 a|1 b');
eq('cut -d: -f1', S.exec('cut -d: -f1 /etc/passwd | head -1').out, 'root');
eq('cut -c1-4', S.exec('echo abcdef | cut -c1-4').out, 'abcd');
eq('tr 大小写', S.exec('echo Hello | tr a-z A-Z').out, 'HELLO');
eq('tr -d 删除', S.exec('echo "a1b2c3" | tr -d 0-9').out, 'abc');

/* ---------------- grep ---------------- */
fresh();
eq('grep 基本', S.exec('grep VERSION_ID /etc/os-release').out, 'VERSION_ID=44');
eq('grep -c 计数', S.exec('grep -c bash /etc/shells').out, '2');
eq('grep -i 忽略大小写', S.exec('grep -i FEDORA /etc/os-release | grep -c .').out, '5');
eq('grep -v 反向', S.exec('grep -v bash /etc/shells').out, '/bin/sh\n/usr/bin/sh\n/usr/bin/tmux');
eq('grep -n 行号', S.exec('grep -n tmux /etc/shells').out, '5:/usr/bin/tmux');
eq('grep "^NAME"', S.exec('grep ^NAME /etc/os-release').out, 'NAME="Fedora Linux"');
eq('grep -r 递归', S.exec('grep -rl VERSION_ID /etc | head -1').out, '/etc/os-release');
eq('grep -w 整词', S.exec('echo "abc ab a" | grep -w ab').out, 'abc ab a');
eq('grep -o 只输出匹配', S.exec('echo "abc123" | grep -o "[0-9]*"').out, '123');
code('grep 无匹配退出码', S.exec('grep zzz /etc/hostname').code, 1);

/* ---------------- sed ---------------- */
fresh();
eq('sed s/// 首个替换', S.exec('echo aaa | sed s/a/b/').out, 'baa');
eq('sed s///g 全部替换', S.exec('echo aaa | sed s/a/b/g').out, 'bbb');
eq('sed -n 只打匹配行', S.exec('sed -n /bash/p /etc/shells').out, '/bin/bash\n/usr/bin/bash');
eq('sed 删除行', S.exec('printf "a\\nb\\nc\\n" | sed 2d').out, 'a\nc');
eq('sed 行尾锚点', S.exec('printf "a\\nb\\n" | sed s/a$/X/').out, 'X\nb');
eq('sed -i 改文件', (S.exec('echo old > ~/s.txt'), S.exec('sed -i s/old/new/ ~/s.txt'), S.exec('cat ~/s.txt').out), 'new');

/* ---------------- awk ---------------- */
fresh();
eq('awk print $1', S.exec('printf "a 1\\nb 2\\n" | awk \'{print $1}\'').out, 'a\nb');
eq('awk -F 指定分隔符', S.exec('echo a:b:c | awk -F: \'{print $2}\'').out, 'b');
eq('awk 求和', S.exec('printf "1\\n2\\n3\\n" | awk \'{s+=$1} END{print s}\'').out, '6');
eq('awk NR', S.exec('printf "x\\ny\\n" | awk \'{print NR}\'').out, '1\n2');
eq('awk NF', S.exec('echo a b c | awk \'{print NF}\'').out, '3');
eq('awk 模式过滤', S.exec('printf "foo\\nbar\\n" | awk /foo/').out, 'foo');
eq('awk $NF 最后一列', S.exec('echo a b c | awk \'{print $NF}\'').out, 'c');

/* ---------------- find ---------------- */
fresh();
eq('find -name', S.exec('find /etc -name hosts').out, '/etc/hosts');
eq('find -type f | wc -l', S.exec('find /usr -type f | wc -l').out.replace(/\s+/g, ''), '7');
eq('find -maxdepth 1 -type d', S.exec('find /usr/local -maxdepth 1 -type d | sort | head -2').out, '/usr/local\n/usr/local/bin');
eq('find -size', S.exec('find /etc -name os-release -size +100c').out, '/etc/os-release');
has('find -exec', S.exec('find /usr/local/bin -name "*.sh" -exec cat {} \\;').out, 'tar czf');
eq('find -delete', (S.exec('touch ~/zz'), S.exec('find ~ -maxdepth 1 -name zz -delete'), S.exec('ls ~/zz').code), 2);

/* ---------------- 权限 ---------------- */
fresh();
eq('chmod 数字', (S.exec('touch ~/p'), S.exec('chmod 644 ~/p'), S.exec('stat -c %a ~/p').out), '644');
eq('chmod u+x', (S.exec('chmod u+x ~/p'), S.exec('stat -c %a ~/p').out), '744');
eq('chmod g-w 去掉写', (S.exec('chmod 664 ~/p'), S.exec('chmod g-w ~/p'), S.exec('stat -c %a ~/p').out), '644');
eq('chmod o=r', (S.exec('chmod o=r ~/p'), S.exec('stat -c %a ~/p').out), '644');
has('ls -l 权限串', (S.exec('chmod 755 ~/p'), S.exec('ls -l ~/p').out), '-rwxr-xr-x');
code('chmod 别人的文件被拒', (S.exec('chmod 777 /etc/hosts').code), 1);
has('chmod 无权提示', S.exec('chmod 777 /etc/hosts').err, 'Operation not permitted');
eq('umask 默认', S.exec('umask').out, '0022');

/* ---------------- 用户 ---------------- */
fresh();
eq('id 普通用户', S.exec('id -u').out, '1000');
eq('useradd 后 passwd 有它', (S.exec('sudo useradd -m tom'), S.exec('grep -c "^tom:" /etc/passwd').out), '1');
eq('useradd 建家目录', S.exec('ls -d /home/tom').out, '/home/tom');
eq('useradd 重名报错', S.exec('sudo useradd tom').err.indexOf('already exists') >= 0 ? 1 : 0, 1);
eq('usermod -aG 加组', (S.exec('sudo groupadd dev'), S.exec('sudo usermod -aG dev tom'), S.exec('groups tom').out.indexOf('dev') >= 0 ? 1 : 0), 1);
eq('userdel 删除', (S.exec('sudo userdel -r tom'), S.exec('grep -c "^tom:" /etc/passwd').code), 1);
eq('root 读 shadow', S.exec('sudo cat /etc/shadow').code, 0);
code('普通用户读 shadow 被拒', S.exec('cat /etc/shadow').code, 1);
has('shadow 权限拒绝', S.exec('cat /etc/shadow').err, 'Permission denied');
eq('su - 切 root 的 pwd', (S.exec('su -'), S.exec('pwd').out), '/root');
eq('su - 后 whoami', (S.exec('su -'), S.exec('whoami').out), 'root');
eq('root 能读 /root', S.exec('su -').code, 0);

/* ---------------- 归档 ---------------- */
fresh();
eq('tar czf 建包', (S.exec('tar czf ~/etc.tgz /etc/hostname'), S.exec('ls ~/etc.tgz').out), '/home/student/etc.tgz');
eq('tar tzf 列内容', S.exec('tar tzf ~/etc.tgz').out, '/etc/hostname');
eq('tar xzf 解包', (S.exec('mkdir ~/x'), S.exec('tar xzf ~/etc.tgz -C ~/x'), S.exec('cat ~/x/etc/hostname').out), 'fedora');
eq('gzip 生成 .gz', (S.exec('echo hi > ~/g.txt'), S.exec('gzip ~/g.txt'), S.exec('ls ~ | grep -c "g.txt.gz"').out), '1');
eq('gunzip 还原', (S.exec('gunzip ~/g.txt.gz'), S.exec('cat ~/g.txt').out), 'hi');
eq('zip/unzip 往返', (S.exec('zip ~/a.zip ~/g.txt'), S.exec('mkdir ~/u'), S.exec('unzip -d ~/u ~/a.zip'), S.exec('cat ~/u/home/student/g.txt').out), 'hi');

/* ---------------- 管道与逻辑 ---------------- */
fresh();
eq('管道三级', S.exec('ls /etc | grep bash | wc -l').out.replace(/\s+/g, ''), '0');
eq('管道 grep|wc', S.exec('grep bash /etc/shells | wc -l').out.replace(/\s+/g, ''), '2');
eq('&& 成功链', S.exec('true 2>/dev/null; echo a && echo b').out, 'a\nb');
eq('|| 失败链', S.exec('ls /nope 2>/dev/null || echo fallback').out, 'fallback');
eq('; 顺序执行', S.exec('echo 1; echo 2').out, '1\n2');
eq('2> 丢弃 stderr', (S.exec('ls /nope 2>/dev/null').err), '');
eq('2>> 追加 err', (S.exec('ls /nope 2>>~/e.log'), S.exec('grep -c No ~/e.log').out), '1');

/* ---------------- 变量与引号 ---------------- */
fresh();
eq('$HOME', S.exec('echo $HOME').out, '/home/student');
eq('单引号不展开', S.exec('echo \'$HOME\'').out, '$HOME');
eq('双引号展开', S.exec('echo "$HOME"').out, '/home/student');
eq('$? 取退出码', (S.exec('ls /nope 2>/dev/null'), S.exec('echo $?').out), '2');
eq('math $(( ))', S.exec('echo $((3+4*2))').out, '11');
eq('$() 命令替换', S.exec('echo $(whoami)').out, 'student');
eq('export 变量', (S.exec('export FOO=bar'), S.exec('echo $FOO').out), 'bar');
eq('alias ll', (S.exec('alias ll=\'ls -l\''), S.exec('ll /etc/hostname').out.split('\n')[0].slice(0, 1)), '-');

/* ★ 同一行里的变量必须按**执行到那一刻**的值展开（2026-11-07 修）。
   以前整行 tokenize 完就展开，于是 `cd /tmp && echo $PWD` 打印旧目录、
   `ls /nope; echo $?` 永远是 0 —— 学生最常用来「验收」的两招全是错的。 */
fresh();
eq('同一行：cd 之后 $PWD 立刻生效', S.exec('cd /tmp && echo $PWD').out, '/tmp');
eq('同一行：$? 取到前一条的退出码', S.exec('ls /nope 2>/dev/null; echo $?').out, '2');
eq('同一行：成功的命令 $? 是 0', S.exec('ls /tmp >/dev/null; echo $?').out, '0');
eq('同一行：export 之后立刻能读到', S.exec('export A=1; echo $A').out, '1');
eq('同一行：连写两个变量', S.exec('export A=1; export B=2; echo $A$B').out, '12');
eq('true / false 的退出码', S.exec('true; echo $?; false; echo $?').out, '0\n1');
eq('$OLDPWD 跟着 cd 走', S.exec('cd /tmp; cd /etc; echo $OLDPWD').out, '/tmp');
eq('单引号里的 $? 不展开', S.exec("echo '$?'").out, '$?');

/* ---------------- 系统命令 ---------------- */
fresh();
has('df -h 表头', S.exec('df -h').out, 'Filesystem');
has('du -sh', S.exec('du -sh /etc').out, '/etc');
has('ps aux 有表头', S.exec('ps aux').out, 'PID');
has('systemctl status sshd', S.exec('systemctl status sshd').out, 'active');
eq('systemctl stop 改状态', (S.exec('systemctl stop sshd'), S.exec('systemctl is-active sshd').out), 'inactive');
eq('systemctl start 恢复', (S.exec('systemctl start sshd'), S.exec('systemctl is-active sshd').out), 'active');
has('dnf install 假装', S.exec('dnf install tree').out, 'Complete!');
has('ip addr 有 inet', S.exec('ip addr').out, 'inet 192.168.10.128');
has('ping -c2', S.exec('ping -c 2 127.0.0.1').out, '2 packets transmitted, 2 received');
has('uname -r', S.exec('uname -r').out, 'fc44');
eq('which ls', S.exec('which ls').out, '/usr/bin/ls');
eq('type cd', S.exec('type cd').out, 'cd is a shell builtin');
code('不存在的命令', S.exec('nosuchcmd').code, 127);
has('命令不存在的报错', S.exec('nosuchcmd').err, 'command not found');

/* ---------------- 汇总 ---------------- */
console.log('');
if (fails.length) {
  console.log('✗ 失败 ' + fail + ' 项（通过 ' + pass + '）');
  fails.forEach(function (f) {
    console.log('\n【' + f.name + '】');
    console.log('  实际: ' + JSON.stringify(f.got));
    console.log('  期望: ' + JSON.stringify(f.want));
  });
  process.exit(1);
} else {
  console.log('✓ 全部通过：' + pass + ' 项');
}
