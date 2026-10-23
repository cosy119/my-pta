/* Learning tools: browser-owned state, additive to existing grades and drafts. */
const Learning = (() => {
 const KEY='pta.learning.v1', read=()=>{try{return JSON.parse(localStorage.getItem(KEY))||{}}catch{return {}}};
 let state=read(), busy=false;
 const clone=x=>JSON.parse(JSON.stringify(x));let baseline=clone(state);
 const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 function merge(base,ours,theirs){
  if(equal(base,ours))return theirs;
  if(Array.isArray(ours)&&Array.isArray(theirs)&&ours.every(x=>x&&x.id)&&theirs.every(x=>x&&x.id)){const all=new Map(theirs.map(x=>[x.id,x]));for(const x of ours)all.set(x.id,merge(base?.find(b=>b.id===x.id),x,all.get(x.id)));return [...all.values()].sort((a,b)=>(b.started||0)-(a.started||0)).slice(0,50);}
  if(ours&&theirs&&typeof ours==='object'&&typeof theirs==='object'&&!Array.isArray(ours)&&!Array.isArray(theirs)){
   const out={};for(const k of new Set([...Object.keys(base||{}),...Object.keys(ours),...Object.keys(theirs)])){const value=merge(base?.[k],ours[k],theirs[k]);if(value!==undefined)out[k]=value;}return out;
  }
  return ours;
 }
 const tabId=sessionStorage.getItem('pta.tabId')||crypto.randomUUID();sessionStorage.setItem('pta.tabId',tabId);
 function pull(){state=merge(baseline,state,read());baseline=clone(read());}
 function subjectName(key){return {python:'Python',ds:'数据结构',cpp:'C++',linux:'Linux'}[key]||key;}
 function subjects(){return [...new Set(PROBLEMS.map(subj))];}
 function subjectOptions(){return '<option value="all">全部科目</option>'+subjects().map(k=>'<option value="'+E(k)+'">'+E(subjectName(k))+'</option>').join('');}
 const save=()=>{pull();state.changed=Date.now();try{localStorage.setItem(KEY,JSON.stringify(state));baseline=clone(state);return true}catch{toast('学习记录保存失败，请先导出备份并检查存储空间','err');return false}};
 const E=esc, name=p=>p? p.title:'题目', subj=p=>p.subject||'python';
 const latest=id=>localSubmissions().find(x=>x.problem_id===id);
 const wrong=p=>{const r=state.review?.[p.id],l=latest(p.id);return r?r.wrong:l?l.verdict!=='AC':attemptsOf(p)>0&&!solvedOf(p)};
 const due=p=>{const r=state.review?.[p.id];return r ? (r.due||0)<=Date.now() : wrong(p)||levelOf(p.id)===1;};
 const session=()=>state.session&&!state.session.done?state.session:null;
 const btn=(t,js)=>'<button class="btn ghost" onclick="'+js+'">'+t+'</button>';
 function home(){
  if(window.Snippets?.route())return;
  if(window.LearnTools?.route())return;
  const resultId=location.hash.split('/results/')[1];
  if(resultId){resultPage(resultId);return;}
  const ss=session(), count=PROBLEMS.filter(due).length;
  const forms=state.forms||{}, groups={};
  PROBLEMS.forEach(p=>{const subject=subj(p);(groups[subject]??={});(groups[subject][p.source_section||'未分章']??=[]).push(p);});
  let bytes=0;for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k.startsWith('pta.'))bytes+=(k.length+localStorage.getItem(k).length)*2;}
  const bookmarks=Object.entries(state.notes||{}).flatMap(([slug,n])=>{
   const saved=n.bookmarks|| (n.bookmark?[{anchor:n.anchor||'',title:n.title||slug}]:[]);
   return saved.map(m=>'<li><a href="#/notes/'+encodeURIComponent(slug)+(m.anchor?'#'+encodeURIComponent(m.anchor):'')+'">'+E(n.title||slug)+(m.anchor?' · '+E(m.title):'')+'</a></li>');
  }).join('');
  document.getElementById('app').innerHTML=`<div class="learn">
   <div class="eyebrow">YOUR STUDY ROUTINE</div><h1>学习中心</h1>
   <div class="learnToday"><div><h2>${count?'今日待复习 '+count+' 题':'今日复习已完成'}</h2><p class="hintline">${count?'每轮最多'+(state.plan?.dailyLimit||20)+'题，答对后按下次日期安排回顾。':'可以开始一组新题，或回顾之前的练习。'}</p></div>
   <div class="btnrow">${count?btn('开始今日复习','Learning.start(true)'):btn('练一组新题',"document.getElementById('learnSetup').scrollIntoView({behavior:'smooth'})")}${ss?btn('继续上次练习','Learning.resume()')+btn('结束本轮并查看总结','Learning.finish()'):''}</div></div>
   <nav class="learnLinks"><a href="#/learn/stats">学习周报</a><a href="#/learn/calendar">复习日历</a><a href="#/learn/print">打印复习单</a><a href="#/learn/tasks">评测任务</a><a href="#/learn/snippets">代码片段库</a></nav><section id="learnSetup"><h2>组一份练习</h2><div class="learnFields">
   <label>科目<select id="lSubject">${subjectOptions()}</select></label>
   <label>章节<select id="lChapter"></select></label><label>题数<input id="lCount" type="number" min="1" max="100" value="10"></label>
   <label>模式<select id="lMode"><option value="practice">连续练习</option><option value="exam">模拟考试（逐题提交）</option><option value="batch">考试（统一交卷评测）</option></select></label>
   <label id="lTimeField" hidden>考试分钟<input id="lMinutes" type="number" min="1" max="180" value="30"></label></div>
   <details class="learnAdvanced"><summary>高级选项：题型、范围、错因与顺序</summary><div class="learnFields">
   <label>题型<select id="lType"><option value="all">全部</option><option value="theory">理论题</option><option value="code">编程题</option></select></label>
   <label>范围<select id="lScope"><option value="all">全部</option><option value="new">未做</option><option value="wrong">最近答错</option><option value="star">收藏</option><option value="review">今日到期</option><option value="marked">自评需复习</option></select></label>
   <label>错因<select id="lTag"><option value="">全部错因</option><option>概念不清</option><option>边界遗漏</option><option>审题错误</option><option>语法错误</option></select></label><label class="learnCheck"><input id="lShuffle" type="checkbox" checked>随机顺序</label></div></details>
   <p id="lMatch" role="status" aria-live="polite"></p><p class="hintline" id="lModeHint"></p><div class="btnrow"><button class="btn" id="lStart" onclick="Learning.start(false)">开始练习</button>${btn('恢复默认','Learning.resetForms()')}</div></section>
   <section><h2>最近练习</h2>${(state.history||[]).length?(state.history||[]).map(x=>'<p><a href="#/learn/results/'+x.id+'">'+E(new Date(x.started).toLocaleString())+' · '+(x.exam?'模拟考试':'连续练习')+' · '+Object.keys(x.results||{}).length+'/'+x.ids.length+'题</a></p>').join(''):'<p class="hintline">完成一轮练习后，可以在这里查看成绩和重练错题。</p>'}</section>
   <section><h2>章节学习概览</h2>${Object.entries(groups).map(([subject,chapters])=>'<details class="learnChapter" '+(forms.lSubject===subject?'open':'')+'><summary>'+E(subjectName(subject))+' · '+Object.values(chapters).flat().filter(solvedOf).length+'/'+Object.values(chapters).flat().length+'题已满分</summary><div class="learnTable"><table class="ptable"><thead><tr><th>章节</th><th>未做</th><th>已尝试</th><th>已满分</th><th>今日到期</th></tr></thead><tbody>'+Object.entries(chapters).map(([title,ps])=>'<tr><td><a href="#/set/'+subject+(lecOf(title)?'/lecture/'+lecOf(title):'')+'">'+E(title)+'</a></td><td>'+ps.filter(p=>!attemptsOf(p)).length+'</td><td>'+ps.filter(p=>attemptsOf(p)>0).length+'</td><td>'+ps.filter(solvedOf).length+'</td><td>'+ps.filter(due).length+'</td></tr>').join('')+'</tbody></table></div></details>').join('')}</section>
   <section><h2>笔记书签</h2>${bookmarks?'<ul>'+bookmarks+'</ul>':'<p class="hintline">还没有书签。阅读时可收藏当前小节，稍后从这里继续。</p><a href="#/notes">去读笔记 →</a>'}${Object.entries(state.notes||{}).filter(([,n])=>n.status).map(([slug,n])=>'<p><a href="#/notes/'+encodeURIComponent(slug)+'">'+E(n.title||slug)+'</a> · '+E(n.status)+'</p>').join('')}</section>
   <section><h2>备份与存储</h2><p>提交记录 ${localSubmissions().length} 条 · 约 ${(bytes/1024/1024).toFixed(2)} MB（估算）</p><p id="lBackupStatus">${backupText()}</p>${btn('导出完整备份','exportProgress()')}</section></div>`;
  for(const id of ['lSubject','lCount','lMode','lMinutes','lType','lScope','lTag'])if(forms[id]!=null)document.getElementById(id).value=forms[id];
  if(forms.lShuffle!=null)document.getElementById('lShuffle').checked=forms.lShuffle;
  chapters();if(forms.lChapter&&[...document.getElementById('lChapter').options].some(x=>x.value===forms.lChapter))document.getElementById('lChapter').value=forms.lChapter;
  document.querySelectorAll('.learnFields input,.learnFields select').forEach(el=>{el.addEventListener('change',()=>{if(el.id==='lSubject')chapters();storeForms();updateSetup();});if(el.type==='number')el.addEventListener('input',()=>{storeForms();updateSetup()});});
  updateSetup();
 }
 function selectedProblems(){
  const val=id=>document.getElementById(id).value;
  return PROBLEMS.filter(p=>(!val('lTag')||state.tags?.[p.id]?.includes(val('lTag')))&&(val('lSubject')==='all'||subj(p)===val('lSubject'))&&(val('lChapter')==='all'||p.source_section===val('lChapter'))&&(val('lType')==='all'||(p.line==='text')===(val('lType')==='theory'))&&({all:true,new:!attemptsOf(p),wrong:wrong(p),star:isStarred(p),review:due(p),marked:levelOf(p.id)===1}[val('lScope')]));
 }
 function storeForms(){state.forms={};document.querySelectorAll('.learnFields input,.learnFields select').forEach(el=>state.forms[el.id]=el.type==='checkbox'?el.checked:el.value);save();}
 function resetForms(){state.forms={};save();home();}
 function updateSetup(){
  const exam=document.getElementById('lMode').value!=='practice';document.getElementById('lTimeField').hidden=!exam;
  const n=Math.min(100,Math.max(1,Number(document.getElementById('lCount').value)||10)),matches=selectedProblems().length,take=Math.min(n,matches);
  document.getElementById('lMatch').textContent='匹配 '+matches+' 题 · 本轮抽取 '+take+' 题';const start=document.getElementById('lStart');start.textContent='开始'+take+'题'+(exam?'考试':'练习');start.disabled=!take;
  document.getElementById('lModeHint').textContent=exam?'本场考试内自动保留已填写答案；每题提交后计分，交卷统一展示。离开仍继续计时。':'练习可随时继续；重新进入选择题保持未作答，历史答案可主动查看。';
 }
 function fingerprint(){
  const b=oldBundle(),notes=Object.fromEntries(Object.entries(state.notes||{}).map(([k,n])=>[k,n]));
  const text=JSON.stringify({local:b.local,drafts:b.drafts,mastery:b.mastery,submissions:b.submissions,review:state.review,tags:state.tags,notes,session:state.session,history:state.history,plan:state.plan,cases:state.testCases,jobs:state.jobs,snippets:state.snippets});
  let hash=2166136261;for(let i=0;i<text.length;i++){hash^=text.charCodeAt(i);hash=Math.imul(hash,16777619);}return (hash>>>0).toString(16);
 }
 function backupText(){return '最近导出：'+(state.backup?new Date(state.backup).toLocaleString():'尚未导出')+' · '+(state.backupHash===fingerprint()?'当前学习数据已备份':'有新学习数据待备份（含成绩、草稿和标注）');}
 function archive(s){state.history??=[];const id=String(s.started);const item=JSON.parse(JSON.stringify({...s,id}));state.history=[item,...state.history.filter(x=>x.id!==id)].slice(0,50);return item;}
 function resultPage(id){
  const s=(state.history||[]).find(x=>x.id===id)||(String(state.session?.started)===id?state.session:null);
  if(!s){document.getElementById('app').innerHTML='<div class="learn"><h1>练习记录不存在</h1><a href="#/learn">返回学习中心</a></div>';return;}
  const rs=Object.values(s.results||{}),score=rs.reduce((n,r)=>n+Number(r.score||0),0),max=s.ids.reduce((n,id)=>n+Number(PROBLEMS.find(p=>p.id===id)?.total_score||0),0);
  document.getElementById('app').innerHTML='<div class="learn" id="lSummary"><a href="#/learn">← 学习中心</a><h1 tabindex="-1">本轮总结</h1><p>'+(s.exam?'模拟考试':'连续练习')+' · '+(s.auto?'到时自动交卷 · ':'')+'用时 '+Math.max(1,Math.round(((s.done||Date.now())-s.started)/60000))+' 分钟</p><div class="learnToday"><b>'+score+' / '+max+' 分</b><span>'+rs.length+' / '+s.ids.length+'题已提交 · '+rs.filter(r=>r.verdict==='AC').length+'题答对</span></div><div class="btnrow">'+btn('重练本轮错题',"Learning.retry('"+id+"')")+btn('导出本轮记录',"Learning.exportRound('"+id+"')")+'</div>'+s.ids.map(pid=>{const r=s.results?.[pid],draft=s.answers?.[pid],p=PROBLEMS.find(p=>p.id===pid);return '<details><summary>'+E(name(p))+' · '+E(r?(VERDICT_TXT[r.verdict]||r.verdict):(hasAnswer(draft)?'已填写，未提交':'未作答'))+(s.flags?.[pid]?' · 待检查':'')+'</summary><pre>'+E(r?.answer??draft?.text??'')+'</pre>'+(r?'<p>'+Number(r.score||0)+' / '+Number(r.max_score||0)+' 分</p><p>'+E(r.message||'')+'</p>'+(r.cases||[]).map(c=>'<details><summary>测试点 · '+E(c.verdict)+'</summary>'+diff(c.expected,c.stdout)+'</details>').join(''):'<p>未提交的填写内容仅保留供回顾，不计分。</p>')+'<a href="#/p/'+pid+'">重新练习</a></details>';}).join('')+'<p class="hintline">保留最近50轮练习，完整备份包含这些记录。</p></div>';
  document.querySelector('#lSummary h1').focus({preventScroll:true});
 }
 function exportRound(id){const s=state.history?.find(x=>x.id===id);if(!s)return;const url=URL.createObjectURL(new Blob([JSON.stringify(s,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='practice-'+id+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
 function retry(id){const s=state.history?.find(x=>x.id===id),ids=s?.ids.filter(pid=>s.results?.[pid]?.verdict!=='AC');if(!ids?.length){toast('本轮没有需要重练的错题');return;}if(session()&&!confirm('开始重练会结束当前练习，继续吗？'))return;if(session())archive({...session(),done:Date.now()});state.session={ids,index:0,results:{},answers:{},flags:{},started:Date.now(),exam:false,deadline:0};save();resume();}

 function chapters(){const v=document.getElementById('lSubject').value;const arr=[...new Set(PROBLEMS.filter(p=>v==='all'||subj(p)===v).map(p=>p.source_section).filter(Boolean))];document.getElementById('lChapter').innerHTML='<option value="all">全部章节</option>'+arr.map(x=>'<option>'+E(x)+'</option>').join('')}
 function start(review){
  let ps=review?PROBLEMS.filter(due):selectedProblems();
  if(!ps.length){toast('当前范围没有题目，请调整条件','err');return;}
  if(session()&&!confirm('结束当前练习并开始新一轮？'))return;
  captureAnswer();if(session())archive({...session(),done:Date.now()});
  const val=id=>document.getElementById(id).value;
  if(!review&&document.getElementById('lShuffle').checked)for(let i=ps.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[ps[i],ps[j]]=[ps[j],ps[i]];}
  const n=review?Math.min(100,Math.max(1,Number(state.plan?.dailyLimit)||20)):Math.min(100,Math.max(1,Number(val('lCount'))||10)),exam=!review&&val('lMode')!=='practice';
  if(!review)storeForms();state.session={ids:ps.slice(0,n).map(p=>p.id),index:0,results:{},answers:{},flags:{},started:Date.now(),owner:tabId,mode:review?'practice':val('lMode'),exam,deadline:exam?Date.now()+Math.min(180,Math.max(1,Number(val('lMinutes'))||30))*60000:0};if(save())resume();
 }

 function resume(){pull();const s=session();if(!s)return;if(s.exam&&!s.owner){s.owner=tabId;save();}if(s.exam&&s.owner&&s.owner!==tabId){if(!confirm('本场考试已在另一个标签页打开。在此页接管？'))return;s.owner=tabId;save();}if(s.exam&&Date.now()>=s.deadline){finish(true);return}location.hash='#/p/'+s.ids[s.index];if(SET.view==='p'&&SET.id===s.ids[s.index])banner()}
 function jump(i){captureAnswer();const s=session();if(!s)return;s.index=Math.max(0,Math.min(i,s.ids.length-1));save();resume();}
 function hasAnswer(a){return !!(a&&(a.choices?.length||a.text?.trim()));}
 function captureAnswer(){
  const s=session();if(!s?.exam||(s.owner&&s.owner!==tabId)||SET.view!=='p'||!CUR||!s.ids.includes(CUR.id)||!document.querySelector('.ptitle'))return;
  s.answers??={};const choices=[...document.querySelectorAll('.choice input:checked')].map(x=>Number(x.closest('.choice').dataset.i));
  const text=CUR.is_choice?(questionTypeKey(CUR)==='true_false'?(document.querySelector('.choice input:checked')?.closest('.choice').dataset.v||''):choices.map(i=>String.fromCharCode(65+i)).join('')):codeValue();s.answers[CUR.id]={choices,text};save();
 }
 function restoreAnswer(){
  const s=session(),root=document.querySelector('.ptitle');if(!s?.exam||!root||!s.ids.includes(CUR?.id)||root.dataset.examRestored)return;
  root.dataset.examRestored='1';const a=s.answers?.[CUR.id];if(!a)return;
  if(CUR.is_choice)document.querySelectorAll('.choice').forEach(x=>{const on=a.choices?.includes(Number(x.dataset.i));x.querySelector('input').checked=!!on;x.classList.toggle('on',!!on);});
  else{const input=document.getElementById('codeBox');if(input)input.value=a.text||'';if(smartEditor&&smartEditorProblemId===CUR.id)smartEditor.view.dispatch({changes:{from:0,to:smartEditor.view.state.doc.length,insert:a.text||''}});}
 }
 function finish(force=false){
  captureAnswer();const s=session();if(!s)return;if(s.exam&&s.owner&&s.owner!==tabId){toast('请先在本页接管考试');return;}const missing=s.ids.filter(id=>!s.results?.[id]).length,flagged=s.ids.filter(id=>s.flags?.[id]).length;
  if(!force&&!confirm('确认结束本轮？还有 '+missing+' 题未提交，'+flagged+' 题待检查。已填写但未提交的内容会保留，不计分。'))return;
  if(s.mode==='batch')window.LearnTools?.queueExam(s);const completed={...s,...session(),done:Date.now(),auto:!!force};state.session=completed;const item=archive(completed);save();document.body.classList.remove('examActive');location.hash='#/learn/results/'+item.id;if(SET.view==='learn')home();
 }

 function flag(){const s=session();if(s){s.flags[CUR.id]=!s.flags[CUR.id];save();banner()}}
 function banner(){
  document.getElementById('learnBanner')?.remove();const s=session(),active=s&&SET.view==='p'&&s.ids.includes(CUR?.id);document.body.classList.toggle('examActive',!!(active&&s.exam));if(!active)return;
  s.index=s.ids.indexOf(CUR.id);const b=document.createElement('div');b.id='learnBanner';b.className='learnBanner';
  const elsewhere=s.exam&&s.owner&&s.owner!==tabId;
  const remaining=Math.max(0,Math.ceil((s.deadline-Date.now())/1000)),clock=Math.floor(remaining/60)+':'+String(remaining%60).padStart(2,'0');
  b.innerHTML=(elsewhere?'<p role="status">考试正在其他标签页进行。'+btn('在此页接管','Learning.resume()')+'</p>':'')+'<div class="learnBannerMain"><b>'+(s.exam?'模拟考试':'连续练习')+' '+(s.index+1)+' / '+s.ids.length+'</b>'+(s.exam?'<span id="lClock" aria-label="剩余时间">剩余 '+clock+'</span>':'')+'<span>'+Object.keys(s.results).length+'题已提交</span><a href="#/learn">'+(s.exam?'返回（计时继续）':'暂停 / 返回')+'</a>'+btn('结束本轮','Learning.finish()')+'</div><div class="btnrow"><button class="btn ghost" onclick="Learning.jump('+(s.index-1)+')" '+(!s.index?'disabled':'')+'>上一题</button><button class="btn ghost" onclick="Learning.jump('+(s.index+1)+')" '+(s.index===s.ids.length-1?'disabled':'')+'>下一题</button>'+btn(s.flags[CUR.id]?'取消待检查':'标记待检查','Learning.flag()')+'<details class="learnAnswerCard"><summary>答题卡</summary><div>'+s.ids.map((id,i)=>{const status=s.results[id]?'已提交':hasAnswer(s.answers?.[id])?'已填写':'未作答';return '<button class="btn ghost" aria-label="第'+(i+1)+'题 '+status+(s.flags[id]?' 待检查':'')+'" onclick="Learning.jump('+i+')">'+(i+1)+(s.results[id]?' ✓':hasAnswer(s.answers?.[id])?' ·':'')+(s.flags[id]?' ?':'')+'</button>';}).join('')+'</div></details></div>';
  document.getElementById('app').prepend(b);
 }

 function record(r){if(r._recorded)return;if(!CUR||['pending','judging'].includes(r.verdict))return;captureAnswer();const id=CUR.id;state.review??={};const old=state.review[id]||{},good=r.verdict==='AC',days=good?Math.min(30,(old.days||1)*2):1;state.review[id]={wrong:!good,days,due:Date.now()+days*86400000,at:Date.now()};const s=session();if(s&&s.ids.includes(id)){s.results[id]={verdict:r.verdict,score:r.score,max_score:r.max_score,cases:r.cases||[],message:r.message||'',answer:typeof r.code==='string'?r.code:(latest(id)?.code ?? (CUR.line==='text'?readTheoryAnswer():codeValue()))};}save();banner()}
 function tags(){if(SET.view!=='p'||!CUR||document.getElementById('lTags'))return;const box=document.querySelector('[data-pnotebox]');if(!box)return;const d=document.createElement('div');d.id='lTags';d.innerHTML='<p>错因分类</p>'+['概念不清','边界遗漏','审题错误','语法错误'].map(t=>'<label style="margin-right:14px"><input type="checkbox" '+(state.tags?.[CUR.id]?.includes(t)?'checked':'')+' onchange="Learning.tag(this)"> '+t+'</label>').join('');box.append(d)}
 function tag(el){state.tags??={};state.tags[CUR.id]=[...document.querySelectorAll('#lTags input:checked')].map(x=>x.parentElement.textContent.trim());save()}
 function note(){
  if(SET.view!=='note'||!document.querySelector('.noteTitle')||document.getElementById('lNote'))return;
  const slug=SET.slug,n=state.notes?.[slug]||{},bar=document.createElement('div');bar.id='lNote';bar.className='noteReadTools';
  bar.innerHTML=btn('收藏当前小节','Learning.markNote()')+'<label>阅读状态 <select onchange="Learning.noteStatus(this.value)"><option value="">未标记</option><option>已读</option><option>需要重看</option></select></label><button class="btn ghost" onclick="window.scrollTo({top:0,behavior:\'smooth\'})">回到顶部</button>';
  document.querySelector('.noteTitle').after(bar);bar.querySelector('select').value=n.status||'';
  document.querySelectorAll('#noteBody h1[id],#noteBody h2[id],#noteBody h3[id],#noteBody h4[id]').forEach(h=>{const button=document.createElement('button');button.className='noteSectionBookmark';button.type='button';button.dataset.anchor=h.id;button.dataset.title=h.textContent;button.addEventListener('click',()=>markNote(h.id));h.append(button);});
  updateNoteControls();if(!SET.anchor&&n.y)requestAnimationFrame(()=>{if(SET.view==='note'&&SET.slug===slug)scrollTo(0,n.y);});
 }
 function noteData(){state.notes??={};const n=state.notes[SET.slug]??={title:document.querySelector('.noteTitle')?.textContent||SET.slug};if(!Array.isArray(n.bookmarks))n.bookmarks=n.bookmark?[{anchor:n.anchor||'',title:n.title||SET.slug}]:[];return n;}
 function currentHeading(){return [...document.querySelectorAll('#noteBody h1[id],#noteBody h2[id],#noteBody h3[id],#noteBody h4[id]')].filter(h=>h.getBoundingClientRect().top<=180).at(-1);}
 function updateNoteControls(){
  if(SET.view!=='note'||!document.getElementById('lNote'))return;const n=state.notes?.[SET.slug]||{},marks=n.bookmarks||(n.bookmark?[{anchor:n.anchor||''}]:[]),anchor=currentHeading()?.id||'';
  const top=document.querySelector('#lNote button');const text=marks.some(x=>x.anchor===anchor)?'取消当前小节书签':'收藏当前小节';if(top.textContent!==text)top.textContent=text;
  document.querySelectorAll('.noteSectionBookmark').forEach(b=>{const on=marks.some(x=>x.anchor===b.dataset.anchor),label=(on?'取消书签：':'收藏小节：')+b.dataset.title;b.setAttribute('aria-label',label);b.setAttribute('aria-pressed',String(on));if(b.textContent!==(on?'已收藏':'收藏'))b.textContent=on?'已收藏':'收藏';});
 }
 function markNote(anchor){
  const n=noteData(),h=anchor?document.getElementById(anchor):currentHeading();anchor=anchor??h?.id??'';
  const button=h?.querySelector('.noteSectionBookmark'),title=button?.dataset.title||h?.textContent||n.title;
  const found=n.bookmarks.some(x=>x.anchor===anchor);n.bookmarks=found?n.bookmarks.filter(x=>x.anchor!==anchor):[...n.bookmarks,{anchor,title}];n.bookmark=n.bookmarks.length>0;n.anchor=n.bookmarks[0]?.anchor||'';save();updateNoteControls();
 }
 function noteStatus(v){noteData().status=v;save();}
 function visible(s){return String(s??'').replaceAll(' ','·').replaceAll('\t','→\t').replaceAll('\n','↵\n')}
 function diff(a,b){a=String(a??'');b=String(b??'');let i=0,j=0;while(i<Math.min(a.length,b.length)&&a[i]===b[i])i++;while(j<Math.min(a.length,b.length)-i&&a[a.length-1-j]===b[b.length-1-j])j++;const line=s=>E(visible(s.slice(0,i)))+'<mark>'+E(visible(s.slice(i,s.length-j)))+'</mark>'+E(visible(j?s.slice(-j):''));return '<div class="learnDiff"><div>预期 / 较早版本<pre>'+line(a)+'</pre></div><div>实际 / 较新版本<pre>'+line(b)+'</pre></div></div>'}
 function submissions(){const items=localSubmissions();document.getElementById('app').innerHTML='<div class="learn"><h1>提交记录与对比</h1><p>浏览器历史 '+items.length+' 条。可选择同一道题的两次提交进行对比。</p><div class="learnFields"><label>题目<input id="lsQuery" placeholder="题号或标题" oninput="Learning.filterSubs()"></label><label>结果<select id="lsVerdict" onchange="Learning.filterSubs()"><option value="">全部</option>'+[...new Set(items.map(x=>x.verdict))].map(x=>'<option>'+E(x)+'</option>').join('')+'</select></label><label>日期<input id="lsDate" type="date" onchange="Learning.filterSubs()"></label></div>'+btn('对比选中的两次提交','Learning.compare()')+'<div id="lCompare"></div><div id="lRecords"></div><details><summary>合并查看后端最近记录</summary><div id="lRemote"></div></details></div>';filterSubs();if(!OFFLINE)api('/api/submissions?limit=200').then(r=>{const el=document.getElementById('lRemote');if(el)el.textContent=(r.items||[]).map(x=>name(PROBLEMS.find(p=>p.id===x.problem_id))+' · '+x.verdict+' · '+x.created_at).join('\n')}).catch(()=>{const el=document.getElementById('lRemote');if(el)el.textContent='后端记录加载失败，请稍后重试'})}
 function filterSubs(){const q=document.getElementById('lsQuery').value.toLowerCase(),v=document.getElementById('lsVerdict').value,d=document.getElementById('lsDate').value;document.getElementById('lRecords').innerHTML=localSubmissions().map((x,i)=>({x,i})).filter(({x})=>(!q||(x.problem_id+' '+name(PROBLEMS.find(p=>p.id===x.problem_id))).toLowerCase().includes(q))&&(!v||x.verdict===v)&&(!d||new Date(x.created_at).toLocaleDateString('sv-SE')===d)).map(({x,i})=>'<details><summary><input type="checkbox" aria-label="选择提交 '+(i+1)+'" value="'+i+'"> '+E(name(PROBLEMS.find(p=>p.id===x.problem_id)))+' · '+E(x.verdict)+' · '+E(stamp(x.created_at))+'</summary><pre>'+E(x.code)+'</pre></details>').join('')||'<p>没有匹配记录。</p>'}
 function compare(){const ids=[...document.querySelectorAll('#lRecords input:checked')].map(x=>Number(x.value));const items=localSubmissions();if(ids.length!==2||items[ids[0]].problem_id!==items[ids[1]].problem_id){toast('请选择同一道题的两次提交','err');return}document.getElementById('lCompare').innerHTML=diff(items[ids[1]].code,items[ids[0]].code)}
 if(state.session?.done&&!(state.history||[]).some(x=>x.id===String(state.session.started))){archive(state.session);save();}
 const nav=document.createElement('a');nav.href='#/learn';nav.textContent='学习中心';document.getElementById('navWB').after(nav);
 const oldResult=renderResult;renderResult=function(r){record(r);oldResult(r);if(!session()?.exam){document.getElementById('resultBox')?.insertAdjacentHTML('beforeend','<p class="hintline">本轮已完成，下次回顾：'+new Date(state.review[CUR.id].due).toLocaleDateString()+'</p>');}if(CUR.line!=='text')for(const [i,c] of (r.cases||[]).entries()){if(c.expected!==undefined&&c.stdout!==undefined&&c.expected!==c.stdout)document.querySelectorAll('.caseBody')[i]?.insertAdjacentHTML('beforeend',diff(c.expected,c.stdout))}};
 const oldSequence=problemSequence;problemSequence=function(subject){const ss=session();if(ss&&SET.view==='p'&&ss.ids.includes(SET.id))return ss.ids.map(id=>PROBLEMS.find(p=>p.id===id)).filter(Boolean);return oldSequence(subject)};
 const oldWrong=wrongbookData;wrongbookData=async function(){return (await oldWrong()).map(x=>({...x,is_wrong:x.is_wrong||wrong(x)}))};
 viewSubmissions=submissions;
 const oldBundle=progressBundle;progressBundle=function(){return {...oldBundle(),learning:state}};
 const oldExport=exportProgress;exportProgress=function(){state.backup=Date.now();state.backupHash=fingerprint();try{localStorage.setItem(KEY,JSON.stringify(state));oldExport();const el=document.getElementById('lBackupStatus');if(el)el.textContent=backupText();}catch(e){toast('备份状态保存失败，请检查存储空间','err');}};
 let scrollTimer;addEventListener('scroll',()=>{if(SET.view!=='note'||!document.getElementById('lNote'))return;const slug=SET.slug,y=scrollY;clearTimeout(scrollTimer);scrollTimer=setTimeout(()=>{if(SET.view==='note'&&SET.slug===slug){noteData().y=y;save();updateNoteControls()}},200)},{passive:true});
 document.addEventListener('input',e=>{if(e.target.closest('#app'))captureAnswer();});document.addEventListener('change',e=>{if(e.target.closest('#app'))captureAnswer();});window.addEventListener('hashchange',captureAnswer);window.addEventListener('pagehide',captureAnswer);
 function navState(){const nav=document.querySelector('a[href="#/learn"]');if(nav){const active=SET.view==='learn';nav.classList.toggle('on',active);if(active)nav.setAttribute('aria-current','page');else nav.removeAttribute('aria-current');}}
 addEventListener('storage',event=>{if(event.key!==KEY)return;pull();if(SET.view==='p'){document.querySelectorAll('#lTags input').forEach(el=>{el.checked=!!state.tags?.[CUR?.id]?.includes(el.parentElement.textContent.trim());});banner();}if(SET.view==='learn'&&!document.activeElement?.closest('.learnFields,#snippetForm'))home();});
 const obs=new MutationObserver(()=>{if(busy)return;busy=true;try{navState();restoreAnswer();tags();note();if(SET.view==='p'&&document.querySelector('.ptitle')&&!document.getElementById('learnBanner'))banner();if(SET.view!=='p')document.body.classList.remove('examActive')}finally{busy=false}});obs.observe(document.getElementById('app'),{childList:true,subtree:true});
 setInterval(()=>{const s=session();if(s?.exam&&(!s.owner||s.owner===tabId)){if(Date.now()>=s.deadline)finish(true);else{const el=document.getElementById('lClock');if(el){const n=Math.max(0,Math.ceil((s.deadline-Date.now())/1000));el.textContent='剩余 '+Math.floor(n/60)+':'+String(n%60).padStart(2,'0');}}}},1000);
 const extraStyle=document.createElement('style');extraStyle.textContent=`
.learn [hidden]{display:none!important}#lSummary h1:focus{outline:none}.learnToday{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:20px;background:var(--panel);border:1px solid var(--border);border-radius:10px}.learnToday h2{margin:0 0 8px}.learnToday .hintline{margin:0}.learn .learnAdvanced{padding:12px 0}.learnFields label{min-width:100px}.learnCheck{display:flex!important;align-items:center}.learnChapter>summary{font-weight:600}.learnChapter .learnTable{max-height:none}.learnBanner{padding:12px 20px;position:relative;background:var(--panel)}.learnBannerMain{display:flex;gap:20px;align-items:center;flex-wrap:wrap}.learnBannerMain a{margin-left:auto}.learnBanner .btnrow{margin:8px 0 0}.learnAnswerCard{position:relative}.learnAnswerCard>div{position:absolute;z-index:30;top:30px;left:0;width:300px;max-height:240px;overflow:auto;padding:12px;display:flex;flex-wrap:wrap;gap:6px;background:var(--panel);border:1px solid var(--border);box-shadow:var(--shadow)}body:has(#learnBanner) .crumb+.btnrow{display:none}body:has(#learnBanner) .problemSteps{display:none}.noteReadTools{position:fixed;bottom:22px;right:26px;z-index:40;display:flex;align-items:center;gap:12px;padding:10px;background:var(--panel);border:1px solid var(--border);border-radius:10px;box-shadow:0 4px 22px #0002}.noteReadTools select{padding:7px;color:var(--text);background:var(--panel);border:1px solid var(--border);border-radius:6px}.noteSectionBookmark{font-size:12px;font-weight:400;margin-left:12px;padding:3px 8px;border-radius:5px;border:1px solid var(--border);color:var(--muted);background:var(--panel);cursor:pointer}.noteSectionBookmark[aria-pressed=true]{color:var(--primary);border-color:var(--primary)}.noteMain{padding-bottom:80px}.notesView .hljs-comment,.notesView .hljs-quote{color:#66716b!important}html[data-theme=dark] .notesView .hljs-comment,html[data-theme=dark] .notesView .hljs-quote{color:#a9b9b1!important}@media(prefers-color-scheme:dark){html:not([data-theme=light]) .notesView .hljs-comment,html:not([data-theme=light]) .notesView .hljs-quote{color:#a9b9b1!important}}@media(max-width:800px){.learnToday{align-items:flex-start;flex-direction:column}.noteReadTools{right:12px;left:12px;bottom:12px;flex-wrap:wrap}.learnBannerMain a{margin-left:0}.learnFields select{max-width:100%}}
`;
 const style=document.createElement('style');style.textContent='.learn{max-width:1100px;margin:30px auto}.learn section{padding:24px 0;border-top:1px solid var(--border);margin-top:24px}.learnFields{display:flex;flex-wrap:wrap;gap:16px;margin:18px 0}.learnFields label{display:grid;gap:7px}.learnFields input[type=checkbox]{width:18px;height:18px}.learnFields select{max-width:260px}.learnFields input[type=number]{width:86px}.learn input,.learn select,#lNote select{padding:9px;background:var(--panel);color:var(--text);border:1px solid var(--border);border-radius:6px}.learn details{padding:12px 0;border-bottom:1px solid var(--border)}.learn pre,.learnDiff pre{white-space:pre-wrap;overflow-wrap:anywhere}.learnTable{max-height:450px;overflow:auto}.learnBanner{grid-column:1/-1;background:var(--panel2);padding:16px 24px;border-bottom:1px solid var(--border)}.learnBanner .btnrow{margin:10px 0}.learnDiff{display:grid;grid-template-columns:1fr 1fr;gap:14px;min-width:0}.learnDiff>div{min-width:0}.learnDiff mark{background:#ffe3a0;color:#352600}.examActive #resultBox,.examActive #histBox,.examActive .previousCode,.examActive .resultActions{display:none!important}#lTags{padding:14px 0}#lRemote{white-space:pre-wrap}';document.head.append(style);document.head.append(extraStyle);
 return {data:()=>state,sync:()=>pull(),update:fn=>{pull();fn(state);return save();},refresh:()=>{pull();if(SET.view==='learn')home();},capture:captureAnswer,canEdit:()=>!session()?.exam||!session()?.owner||session().owner===tabId,subjectName,subjects,home,chapters,resetForms,retry,exportRound,start,resume,jump,finish,flag,tag,markNote,noteStatus,filterSubs,compare,diff,wrong,due};
})();
