/* Extended study tools. Data stays in Learning's versioned browser store. */
const LearnTools = (() => {
  const E=esc, data=()=>Learning.data(), update=fn=>Learning.update(fn);
  const title=id=>PROBLEMS.find(p=>p.id===Number(id))?.title||('#'+id);
  const label=v=>VERDICT_TXT[v]||v;
  const link=(text,path)=>'<a class="btn ghost" href="'+path+'">'+text+'</a>';
  const action=(text,call)=>'<button class="btn ghost" onclick="LearnTools.'+call+'">'+text+'</button>';
  const dateKey=d=>new Date(d).toLocaleDateString('sv-SE');
  const jobBusy=j=>['queued','running','polling'].includes(j.status);
  let serial=Promise.resolve(),importFile=null,importData=null;
  const inflight=new Set(),selected=new Map();let page=1,filtered=[];const tabId=sessionStorage.getItem('pta.tabId'),heartbeatKey='pta.jobHeartbeat.'+tabId;
  function shell(name,html){document.getElementById('app').innerHTML='<div class="learn"><a href="#/learn">← 学习中心</a><h1 tabindex="-1">'+name+'</h1>'+html+'</div>';}
  function route(){
    const section=(location.hash.split('/')[2]||'').split('?')[0];
    if(section==='stats'){stats();return true;}if(section==='calendar'){calendar();return true;}
    if(section==='print'){printSetup();return true;}if(section==='tasks'){tasks();return true;}return false;
  }
  function refreshJobs(){
    if(SET.view==='learn'&&/\/(tasks|results)\//.test(location.hash))Learning.home();
    else if(location.hash==='#/learn/tasks')tasks();
    if(SET.view==='p'&&CUR)decorate();
  }
  function upsertResult(j,r){
    if(!r||['pending','judging'].includes(r.verdict))return;
    update(s=>{
      const job=s.jobs[j.id];if(!job||job.status==='done')return;
      if(r.verdict==='IE'){job.status='failed';job.error=r.message||'评测环境失败，可重试';return;}
      job.status='done';job.verdict=r.verdict;job.finished=Date.now();
      s.review??={};const days=r.verdict==='AC'?Math.min(30,(s.review[j.pid]?.days||1)*2):1;
      s.review[j.pid]={wrong:r.verdict!=='AC',days,due:Date.now()+days*86400000,at:Date.now()};
      const result={verdict:r.verdict,score:r.score,max_score:r.max_score,cases:r.cases||[],message:r.message||'',answer:j.code,jobId:j.id};
      if(String(s.session?.started)===String(j.round))s.session.results[j.pid]=result;
      const archived=s.history?.find(x=>String(x.id)===String(j.round));if(archived)archived.results[j.pid]=result;
    });
    refreshJobs();
  }
  function createJob(p,code,lang,round,mode){
    const id=crypto.randomUUID();const j={id,pid:p.id,code:String(code),lang:lang||'text',round:round?String(round):'',mode:mode||'local',status:'queued',owner:tabId,created:Date.now()};
    update(s=>{s.jobs??={};s.jobs[id]=j;});return j;
  }
  async function problem(id){return OFFLINE?localProblem(Number(id)):await api('/api/problems/'+Number(id));}
  async function perform(j){
    if(inflight.has(j.id)||data().jobs?.[j.id]?.status==='done')return;
    inflight.add(j.id);const beat=()=>{try{localStorage.setItem(heartbeatKey,String(Date.now()));}catch{}};beat();const pulse=setInterval(beat,5000);update(s=>{s.jobs[j.id].owner=tabId;s.jobs[j.id].status='running';delete s.jobs[j.id].error;});refreshJobs();
    try{
      const p=await problem(j.pid);if(!p)throw Error('题目已不存在');let r;
      if(j.mode==='backend'){
        let sid=j.submissionId;
        if(!sid){const initial=await api('/api/submissions',{method:'POST',body:{problem_id:j.pid,code:j.code,lang:j.lang,interpreter:j.interpreter||(j.lang==='text'?'text':j.lang==='python'?'py313':j.lang==='c'?'gcc':'gpp')}});sid=initial.id;update(s=>{s.jobs[j.id].submissionId=sid;s.jobs[j.id].status='polling';});}
        for(let n=0;n<120;n++){r=await api('/api/submissions/'+sid+'?with_cases=1');if(!['pending','judging'].includes(r.verdict))break;await new Promise(resolve=>setTimeout(resolve,1000));}
        if(r?.problem_id&&Number(r.problem_id)!==j.pid)throw Error('回执题目与任务不一致，请检查后端连接');if(!r||['pending','judging'].includes(r.verdict))throw Error('等待评测结果超时，可重试查询');
      }else if(p.line==='text')r=TextJudge.judgeTextProblem(p,j.code);
      else if(p.line==='python')r=await PythonLocal.submit(p,j.code);
      else r=await CppLocal.submit(p,j.code,j.lang||'cpp');
      if(!r?.verdict)throw Error(r?.error||'未返回有效评测结果');if(r.verdict==='IE')throw Error(r.message||'评测环境失败');
      r.lang=j.lang;r._recorded=true;
      saveLocalSubmission(p,r,j.code,j.lang);
      if(j.mode==='backend'){
        const items=localSubmissions();if(items[0]){items[0].source='backend';items[0].id=data().jobs[j.id].submissionId;}localStorage.setItem(LOCAL_SUBMISSIONS,JSON.stringify(items));
      }
      setLocalProgress(p.id,r.score,r.max_score);upsertResult(j,r);
      if(SET.view==='p'&&CUR?.id===j.pid){RESULT=r;renderResult(r);renderButtons();}
      await afterJudgeRefresh();
    }catch(e){update(s=>{s.jobs[j.id].status='failed';s.jobs[j.id].error=String(e.message||e);});refreshJobs();if(SET.view==='p'&&CUR?.id===j.pid){document.getElementById('resultBox').innerHTML=verdictHtml('IE','评测未完成，可从任务列表重试',String(e.message||e));renderButtons();}}
    finally{inflight.delete(j.id);clearInterval(pulse);try{localStorage.removeItem(heartbeatKey);}catch{}}
  }
  function enqueue(j){serial=serial.catch(()=>{}).then(()=>perform(j));return serial;}
  async function submitCurrent(){
    if(!Learning.canEdit()){toast('本场考试在其他标签页，请先接管');return;}
    const s=data().session;if(s?.exam&&!s.done&&Date.now()>=s.deadline){Learning.finish(true);return;}
    const p=CUR;if(!p)return;const code=p.line==='text'?readTheoryAnswer():codeValue();if(!code?.trim())return;
    Learning.capture();const lang=p.line==='text'?'text':document.getElementById('langSel')?.value||(p.line==='python'?'python':'cpp');
    const round=s&&!s.done&&s.ids.includes(p.id)?s.started:'';
    if(Object.values(data().jobs||{}).some(j=>j.pid===p.id&&jobBusy(j))){toast('这道题已有评测任务，请等待结果');return;}
    const j=createJob(p,code,lang,round,OFFLINE?'local':'backend');
    j.interpreter=document.getElementById('interpSel')?.value;update(st=>st.jobs[j.id].interpreter=j.interpreter);
    const button=document.getElementById('btnSubmit');if(button)button.disabled=true;
    document.getElementById('resultBox').innerHTML=verdictHtml('pending','已加入评测队列，离开后结果仍会保存','');return enqueue(j);
  }
  function retryJob(id){const j=data().jobs?.[id];if(!j||inflight.has(id))return;update(s=>s.jobs[id].status='queued');enqueue(j);tasks();}
  function queueExam(s){
    const jobs=[];for(const id of s.ids){const a=s.answers?.[id];if(!a?.text?.trim())continue;const existing=s.results?.[id];if(existing?.answer===a.text)continue;
      if(Object.values(data().jobs||{}).some(j=>String(j.round)===String(s.started)&&j.pid===id&&jobBusy(j)))continue;
      const p=localProblem(id)||PROBLEMS.find(x=>x.id===id);if(!p)continue;
      const lang=p.line==='text'?'text':a.lang||(p.line==='python'?'python':'cpp');jobs.push(createJob(p,a.text,lang,s.started,OFFLINE?'local':'backend'));
    }
    setTimeout(()=>jobs.forEach(enqueue),0);
  }
  function tasks(){
    const jobs=Object.values(data().jobs||{}).sort((a,b)=>b.created-a.created);
    shell('评测任务', '<p class="hintline">评测与练习轮次绑定，交卷后仍会补回成绩。页面关闭会中断本地任务，再次打开可手动重试。</p>'+(jobs.length?jobs.map(j=>'<article class="toolCard"><a href="#/p/'+j.pid+'">'+E(title(j.pid))+'</a><p>'+E({queued:'排队中',running:'评测中',polling:'等待后端结果',done:label(j.verdict),failed:'未完成',interrupted:'已中断'}[j.status]||j.status)+' · '+E(new Date(j.created).toLocaleString())+'</p>'+(j.error?'<p>'+E(j.error)+'</p>':'')+(['failed','interrupted'].includes(j.status)?action('重试',"retryJob('"+j.id+"')"):'')+(j.round?link('查看本轮结果','#/learn/results/'+j.round):'')+'</article>').join(''):'<p>还没有评测任务。</p>'));
  }
  function decorate(){
    if(SET.view!=='p'||!CUR||!document.querySelector('.ptitle'))return;
    const s=data().session;
    let status=document.getElementById('toolJobStatus');
    if(!status){status=document.createElement('div');status.id='toolJobStatus';status.setAttribute('role','status');document.getElementById('btnRow')?.after(status);}
    const active=Object.values(data().jobs||{}).filter(j=>j.pid===CUR.id&&jobBusy(j));const text=active.length?'已有评测任务，正在等待结果。交卷后成绩仍会补回。':'';if(status.textContent!==text)status.textContent=text;
    if(active.length){const b=document.getElementById('btnSubmit');if(b)b.disabled=true;}
    if(s?.exam&&!s.done&&s.mode==='batch'){
      const b=document.getElementById('btnSubmit');if(b){b.disabled=true;if(b.textContent!=='已暂存，交卷时统一评测')b.textContent='已暂存，交卷时统一评测';}
    }
    if(CUR.line!=='text'&&!document.getElementById('customCases')){
      const box=document.createElement('details');box.id='customCases';box.innerHTML='<summary>自定义测试用例组（仅自测，不计成绩）</summary><div id="caseRows"></div><div class="btnrow">'+action('添加用例','addCase()')+action('从题目样例建立','sampleCases()')+action('运行全部','runCases()')+'</div><div id="caseResults" role="status" aria-live="polite"></div>';
      document.getElementById('btnRow')?.before(box);renderCases();
    }
  }
  function caseList(){return data().testCases?.[CUR.id]||[];}
  function renderCases(){const host=document.getElementById('caseRows');if(!host)return;host.innerHTML=caseList().map((c,i)=>'<div class="caseEditor"><b>用例 '+(i+1)+'</b><label>输入<textarea data-case="'+i+'" data-field="input">'+E(c.input)+'</textarea></label><label>预期输出<textarea data-case="'+i+'" data-field="expected">'+E(c.expected)+'</textarea></label>'+action('删除','deleteCase('+i+')')+'</div>').join('')||'<p class="hintline">添加输入和预期输出，方便检查空输入、边界值等情况。</p>';host.querySelectorAll('textarea').forEach(el=>el.addEventListener('input',()=>{update(s=>{s.testCases[CUR.id][Number(el.dataset.case)][el.dataset.field]=el.value;});}));}
  function addCase(){if(caseList().length>=30){toast('每题最多30组用例');return;}update(s=>{s.testCases??={};s.testCases[CUR.id]??=[];s.testCases[CUR.id].push({input:'',expected:''});});renderCases();}
  function deleteCase(i){update(s=>s.testCases[CUR.id].splice(i,1));renderCases();}
  function sampleCases(){update(s=>{s.testCases??={};s.testCases[CUR.id]=(CUR.samples||[]).slice(0,30).map(x=>({input:x.stdin||'',expected:x.expected_stdout??x.expected??x.stdout??''}));});renderCases();}
  async function runCases(){
    if(!caseList().length){toast('请先添加测试用例');return;}if(Object.values(data().jobs||{}).some(jobBusy)){toast('请先等待评测任务完成');return;}
    const p=CUR,code=codeValue(),lang=document.getElementById('langSel')?.value||(p.line==='python'?'python':'cpp'),cases=JSON.parse(JSON.stringify(caseList()));if(!code.trim()){toast('请先填写代码');return;}
    const host=document.getElementById('caseResults');host.textContent='正在运行 '+cases.length+' 组用例…';let html='';
    for(let i=0;i<cases.length;i++){
      try{let r;if(!OFFLINE)r=await api('/api/run',{method:'POST',body:{code,lang,stdin:cases[i].input,interpreter:lang==='python'?'py313':lang==='c'?'gcc':'gpp'}});else r=p.line==='python'?await PythonLocal.run(code,cases[i].input):await CppLocal.run(code,lang,cases[i].input);
        const actual=String(r.stdout??''),ok=!r.stderr&&actual.replace(/\r\n/g,'\n').trimEnd()===cases[i].expected.replace(/\r\n/g,'\n').trimEnd();html+='<details open><summary>用例 '+(i+1)+' · '+(ok?'通过':'输出不同或运行失败')+'</summary>'+Learning.diff(cases[i].expected,actual)+(r.stderr?'<pre>'+E(r.stderr)+'</pre>':'')+'</details>';
      }catch(e){html+='<p>用例 '+(i+1)+' · '+E(e.message||e)+'</p>';}
      if(SET.view==='p'&&CUR?.id===p.id&&host.isConnected)host.innerHTML=html;
    }
  }
  function stats(){
    const days=Number(new URLSearchParams(location.hash.split('?')[1]||'').get('days'))===30?30:7,cutoff=Date.now()-days*86400000;
    const rows=localSubmissions().filter(x=>Date.parse(x.created_at)>=cutoff&&!['IE','pending','judging'].includes(x.verdict)),unique=new Set(rows.map(x=>x.problem_id)),correct=rows.filter(x=>x.verdict==='AC').length;
    const groups={};for(const r of rows){const p=PROBLEMS.find(p=>p.id===r.problem_id),k=p?.subject||'其他';const g=groups[k]??={attempts:0,ac:0};g.attempts++;if(r.verdict==='AC')g.ac++;}
    const types={};for(const r of rows){const problem=PROBLEMS.find(p=>p.id===r.problem_id);const key=problem?problemType(problem):'未知题型';const group=types[key]??={attempts:0,ac:0};group.attempts++;if(r.verdict==='AC')group.ac++;}
    const repeated=Object.entries(rows.filter(x=>x.verdict!=='AC').reduce((m,r)=>(m[r.problem_id]=(m[r.problem_id]||0)+1,m),{})).filter(([,n])=>n>=2).sort((a,b)=>b[1]-a[1]);
    const daily=Array.from({length:days},(_,i)=>{const key=dateKey(Date.now()-(days-1-i)*86400000),a=rows.filter(r=>dateKey(r.created_at)===key);return '<tr><td>'+key+'</td><td>'+a.length+'</td><td>'+a.filter(r=>r.verdict==='AC').length+'</td><td>'+new Set(a.map(r=>r.problem_id)).size+'</td></tr>';}).join('');
    shell('学习周报与薄弱分析','<div class="btnrow">'+link('近7天','#/learn/stats?days=7')+link('近30天','#/learn/stats?days=30')+'</div><div class="toolMetrics"><p><b>'+rows.length+'</b> 次有效提交</p><p><b>'+unique.size+'</b> 道练习题</p><p><b>'+(rows.length?Math.round(correct/rows.length*100)+'%':'—')+'</b> 作答正确率</p></div><p class="hintline">仅统计当前浏览器保留的提交记录，每次提交计一次；环境失败不计入正确率，不以历史最高分代替最近表现。</p><h2>科目分布</h2>'+(Object.keys(groups).length?Object.entries(groups).map(([k,g])=>'<p>'+E(Learning.subjectName(k))+' · '+g.attempts+'次 · '+Math.round(g.ac/g.attempts*100)+'%正确</p>').join(''):'<p class="hintline">还没有有效提交，<a href="#/learn">开始一组练习</a>后查看科目分布。</p>')+'<h2>题型分布</h2>'+(Object.keys(types).length?Object.entries(types).map(([key,g])=>'<p>'+E(key)+' · '+g.attempts+'次 · '+Math.round(g.ac/g.attempts*100)+'%正确</p>').join(''):'<p class="hintline">完成练习后，这里会展示各题型的作答表现。</p>')+'<h2>反复出错的题</h2>'+(repeated.map(([id,n])=>'<p><a href="#/p/'+id+'">'+E(title(id))+'</a> · '+n+'次未通过</p>').join('')||'<p>当前时间范围内没有重复错题。</p>')+'<h2>每日练习</h2><table class="ptable"><thead><tr><th>日期</th><th>提交</th><th>答对</th><th>题数</th></tr></thead><tbody>'+daily+'</tbody></table>');
  }
  function calendar(){
    const limit=data().plan?.dailyLimit||20,today=dateKey(Date.now()),groups={};for(let i=0;i<7;i++)groups[dateKey(Date.now()+i*86400000)]=[];
    for(const p of PROBLEMS){const r=data().review?.[p.id];const k=r?dateKey(r.due):Learning.due(p)?today:'';if(k&&k<=today)groups[today].push(p);else if(groups[k])groups[k].push(p);}
    const completed=Object.values(data().review||{}).filter(r=>r.at&&dateKey(r.at)===today).length;
    shell('复习日历','<p>今天已复习 '+completed+' 题 / 每日目标 '+limit+' 题，可继续加练。</p><label>每日目标（也是单轮上限） <input id="dailyLimit" type="number" min="1" max="100" value="'+limit+'"></label>'+action('保存安排','savePlan()')+'<p class="hintline">今天含已逾期题；每轮按设定数量分批练习，不改变最高成绩。</p>'+Object.entries(groups).map(([day,ps])=>'<section><h2>'+day+' · '+ps.length+'题</h2>'+ps.slice(0,100).map(p=>'<div class="calendarRow"><a href="#/p/'+p.id+'">'+E(p.title)+'</a>'+action((data().review?.[p.id]?.due||0)>Date.now()?'延后一天':'明天再看','snooze('+p.id+')')+action('已掌握，30天后','mastered('+p.id+')')+'</div>').join('')+(ps.length>100?'<p>前100题已展示，可通过今日复习分批完成。</p>':'')+'</section>').join(''));
  }
  function savePlan(){const value=Math.min(100,Math.max(1,Number(document.getElementById('dailyLimit').value)||20));update(s=>s.plan={...s.plan,dailyLimit:value});toast('每轮复习题量已保存','ok');}
  function snooze(id){update(s=>{s.review??={};s.review[id]={...s.review[id],due:Math.max(Date.now(),s.review[id]?.due||0)+86400000};});calendar();}
  function mastered(id){saveMastery(id,{level:2});update(s=>{s.review??={};s.review[id]={...s.review[id],wrong:false,days:30,due:Date.now()+30*86400000};});calendar();}
  function submissionKey(x){return JSON.stringify([x.problem_id,x.created_at,x.code,x.verdict]);}
  function submissions(){
    page=1;selected.clear();shell('提交记录与对比','<div class="learnFields"><label>题目<input id="lsQuery" placeholder="题号或标题"></label><label>结果<select id="lsVerdict"><option value="">全部</option>'+[...new Set(localSubmissions().map(x=>x.verdict))].map(v=>'<option value="'+E(v)+'">'+E(label(v))+'</option>').join('')+'</select></label><label>日期<input id="lsDate" type="date"></label></div><div class="btnrow">'+action('对比选中的两次提交','compare()')+action('清空选择','clearSelection()')+'<span id="selectedCount" role="status"></span></div><div id="lCompare"></div><div id="historyCount" role="status"></div><div id="lRecords"></div><div id="historyPager" class="btnrow"></div><details><summary>后端最近记录</summary><div id="remoteHistory"></div></details>');
    for(const id of ['lsQuery','lsVerdict','lsDate'])document.getElementById(id).addEventListener('input',()=>{page=1;filterSubs();});filterSubs();
    if(!OFFLINE)api('/api/submissions?limit=200').then(r=>{const el=document.getElementById('remoteHistory');if(el)el.innerHTML=(r.items||[]).map(x=>'<p><a href="#/p/'+Number(x.problem_id)+'">'+E(title(x.problem_id))+'</a> · '+E(label(x.verdict))+' · '+E(stamp(x.created_at))+'</p>').join('')||'暂无记录';}).catch(()=>{const el=document.getElementById('remoteHistory');if(el)el.textContent='加载失败，请稍后重试';});
  }
  function filterSubs(){
    if(!document.getElementById('lsQuery'))return;const q=document.getElementById('lsQuery').value.toLowerCase(),v=document.getElementById('lsVerdict').value,d=document.getElementById('lsDate').value,lookup=new Map(PROBLEMS.map(p=>[p.id,p.title]));
    filtered=localSubmissions().filter(x=>(!q||(x.problem_id+' '+(lookup.get(x.problem_id)||'')).toLowerCase().includes(q))&&(!v||x.verdict===v)&&(!d||dateKey(x.created_at)===d));renderHistoryPage();
  }
  function renderHistoryPage(){
    page=Math.min(Math.max(1,page),Math.max(1,Math.ceil(filtered.length/50)));const first=(page-1)*50,rows=filtered.slice(first,first+50);
    document.getElementById('historyCount').textContent='匹配 '+filtered.length+' 条 · 第 '+page+' / '+Math.max(1,Math.ceil(filtered.length/50))+' 页（每页50条）';
    document.getElementById('lRecords').innerHTML=rows.map((x,i)=>'<article class="submissionRow"><label><input type="checkbox" data-record="'+(first+i)+'" aria-label="选择提交 '+(first+i+1)+'" '+(selected.has(submissionKey(x))?'checked':'')+'></label><div><a href="#/p/'+x.problem_id+'">'+E(title(x.problem_id))+'</a> · <b>'+E(label(x.verdict))+'</b> · '+E(stamp(x.created_at))+'<small> · '+(x.source==='backend'?'后端回执':'此浏览器')+'</small><details><summary>查看作答</summary><pre>'+E(x.code)+'</pre></details></div></article>').join('')||'<p>没有匹配记录。</p>';
    document.querySelectorAll('[data-record]').forEach(el=>el.addEventListener('change',()=>{const x=filtered[Number(el.dataset.record)],key=submissionKey(x);if(el.checked)selected.set(key,x);else selected.delete(key);selectionStatus();}));
    document.getElementById('historyPager').innerHTML='<button class="btn ghost" onclick="LearnTools.historyPage(-1)" '+(page===1?'disabled':'')+'>上一页</button><button class="btn ghost" onclick="LearnTools.historyPage(1)" '+(first+50>=filtered.length?'disabled':'')+'>下一页</button>';selectionStatus();
  }
  function selectionStatus(){document.getElementById('selectedCount').textContent='已选择 '+selected.size+' 条（跨页保留）';}
  function historyPage(delta){page+=delta;renderHistoryPage();document.getElementById('historyCount').scrollIntoView({block:'start'});}
  function clearSelection(){selected.clear();renderHistoryPage();}
  function compare(){const items=[...selected.values()].sort((a,b)=>Date.parse(a.created_at)-Date.parse(b.created_at));if(items.length!==2||items[0].problem_id!==items[1].problem_id){toast('请选择同一道题的两次提交','err');return;}document.getElementById('lCompare').innerHTML=Learning.diff(items[0].code,items[1].code);}
  function printSetup(){
    shell('打印复习单','<p>可打印为A4，或在浏览器打印窗口另存为PDF。每份最多100题。</p><div class="learnFields"><label>范围<select id="printScope"><option value="wrong">最近答错</option><option value="star">收藏题</option><option value="chapter">按章节</option><option value="round">最近一轮错题</option></select></label><label>科目<select id="printSubject"><option value="all">全部</option>'+Learning.subjects().map(k=>'<option value="'+E(k)+'">'+E(Learning.subjectName(k))+'</option>').join('')+'</select></label><label>章节<select id="printChapter"><option value="all">全部章节</option>'+[...new Set(PROBLEMS.map(p=>p.source_section).filter(Boolean))].map(x=>'<option>'+E(x)+'</option>').join('')+'</select></label><label><input type="checkbox" id="printAnswers">附答案与自己的错因（另起一页）</label></div>'+action('打开打印预览','printSheet()')+'<p class="hintline">理论题有参考答案时展示参考答案；编程题展示上次提交并明确标注，不将个人代码当作标准解。</p>');
  }
  function printSheet(){
    const val=id=>document.getElementById(id).value,scope=val('printScope'),round=data().history?.[0];
    const ps=PROBLEMS.filter(p=>(val('printSubject')==='all'||p.subject===val('printSubject'))&&(val('printChapter')==='all'||p.source_section===val('printChapter'))&&({wrong:Learning.wrong(p),star:isStarred(p),chapter:true,round:round?.ids.includes(p.id)&&round.results?.[p.id]?.verdict!=='AC'}[scope]));
    if(!ps.length){toast('没有符合条件的题目');return;}const list=ps.slice(0,100),w=window.open('about:blank','_blank');if(!w){toast('请允许打开打印预览窗口');return;}
    let html='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>学习复习单</title><style>body{font:15px/1.8 "Microsoft YaHei",sans-serif;margin:24px;color:#222}article{break-inside:avoid;border-bottom:1px solid #ccc;padding:14px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f5f5f5;padding:10px}h1{font-size:24px}button{padding:10px}small{color:#666}.answers{break-before:page}@page{size:A4;margin:18mm}@media print{button{display:none}body{margin:0}}</style><body><button onclick="window.print()">打印 / 另存为PDF</button><h1>学习复习单</h1><p>'+list.length+'题'+(ps.length>100?'（范围共'+ps.length+'题，本次取前100题）':'')+'</p>';
    html+=list.map((p,i)=>{const full=localProblem(p.id)||p;return '<article><h2>'+(i+1)+'. '+E(p.title)+'</h2>'+mdRender(full.statement_md||'')+[['输入格式',full.input_format],['输出格式',full.output_format],['数据范围',full.constraints_md]].filter(([,v])=>v).map(([k,v])=>'<h3>'+k+'</h3>'+mdRender(v)).join('')+(full.samples||[]).map((c,n)=>'<h3>样例'+(n+1)+'</h3><p>输入</p><pre>'+E(c.stdin||'')+'</pre><p>输出</p><pre>'+E(c.expected_stdout??c.stdout??c.expected??'')+'</pre>').join('')+(full.choices||[]).map((c,k)=>'<p>'+String.fromCharCode(65+k)+'. '+E(c)+'</p>').join('')+'<p>我的答案：________________________________________________</p></article>';}).join('');
    if(document.getElementById('printAnswers').checked)html+='<section class="answers"><h1>答案与错因</h1>'+list.map((p,i)=>{const full=localProblem(p.id)||p,last=localSubmissions().find(x=>x.problem_id===p.id);const expected=full.line==='text'?(full.testcases||full.cases||[]).map(c=>c.expected_stdout??c.expected).filter(x=>x!=null).join(' / '):'';return '<article><h2>'+(i+1)+'. '+E(p.title)+'</h2>'+(expected?'<p>参考答案：'+E(expected)+'</p>':'')+(last?'<p>上次作答（不代表标准答案）：</p><pre>'+E(last.code)+'</pre>':'<p>暂无可展示答案，请回网站查看评测。</p>')+'<p>我的错因：'+E(noteOf(p.id)||'未填写')+'</p></article>';}).join('')+'</section>';
    w.document.open();w.document.write(html+'</body></html>');w.document.close();
  }
  function closePreview(){importFile=null;importData=null;closeModal();}
  const originalImport=importProgress;
  async function previewImport(ev){
    const file=ev?.target?.files?.[0];if(!file)return;
    try{
      const incoming=JSON.parse(await file.text());if(incoming.kind!=='my-pta-progress'||!incoming.local||typeof incoming.local!=='object'||Array.isArray(incoming.local))throw Error('这不是有效的进度备份');
      importFile=file;importData=incoming;const current=progressBundle(),count=x=>x&&typeof x==='object'?Object.keys(x).length:0;
      const noteConflicts=Object.keys(incoming.mastery||{}).filter(id=>current.mastery[id]?.note&&incoming.mastery[id]?.note&&current.mastery[id].note!==incoming.mastery[id].note).length;
      const unseen=(a,b)=>Object.keys(a||{}).filter(k=>!Object.hasOwn(b||{},k)).length;
      const knownSubmissions=new Set((current.submissions||[]).map(submissionKey)),knownRounds=new Set((current.learning?.history||[]).map(x=>String(x.id||x.started)));
      const fields=[['代码片段',count(incoming.learning?.snippets),unseen(incoming.learning?.snippets,current.learning?.snippets)],['题目成绩',count(incoming.local),unseen(incoming.local,current.local)],['提交记录',incoming.submissions?.length||0,(incoming.submissions||[]).filter(x=>!knownSubmissions.has(submissionKey(x))).length],['草稿',count(incoming.drafts),unseen(incoming.drafts,current.drafts)],['收藏/备注/自评',count(incoming.mastery),unseen(incoming.mastery,current.mastery)],['笔记',count(incoming.learning?.notes),unseen(incoming.learning?.notes,current.learning?.notes)],['练习轮次',incoming.learning?.history?.length||0,(incoming.learning?.history||[]).filter(x=>!knownRounds.has(String(x.id||x.started))).length],['测试用例组',count(incoming.learning?.testCases),unseen(incoming.learning?.testCases,current.learning?.testCases)],['评测任务',count(incoming.learning?.jobs),unseen(incoming.learning?.jobs,current.learning?.jobs)]];
      const host=document.getElementById('modalHost');host.innerHTML='<div class="mask"><div class="modal" role="dialog" aria-modal="true" aria-labelledby="importTitle"><div class="modalBody"><h2 id="importTitle">导入前预览</h2><p>备份时间：'+E(incoming.exported_at||'未知')+'</p><table class="ptable"><thead><tr><th>内容</th><th>备份数量</th><th>新增 / 已有</th></tr></thead><tbody>'+fields.map(([k,n,added])=>'<tr><td>'+k+'</td><td>'+n+'</td><td>'+added+' / '+(n-added)+'</td></tr>').join('')+'</tbody></table><p>'+noteConflicts+'处备注冲突。成绩保留最高，提交去重；已有草稿和标注优先保留本机，新内容补入；同ID代码片段保留本机版本。</p><label><input id="importToken" type="checkbox" checked>采用备份通行证（连接后端时用于恢复原身份）</label><div class="btnrow">'+action('先导出当前快照','backupBeforeImport()')+action('确认合并','applyImport()')+action('取消','closePreview()')+'</div></div></div></div>';host.querySelector('button').focus();
    }catch(e){toast(String(e.message||e),'err');}finally{if(ev.target)ev.target.value='';}
  }
  function backupBeforeImport(){exportProgress();}
  function mergeExtension(incoming){
    if(!incoming||typeof incoming!=='object')return;
    update(s=>{
      for(const key of ['notes','tags','review','testCases']){
        const input=incoming[key];if(!input||typeof input!=='object'||Array.isArray(input))continue;s[key]??={};
        for(const [id,value] of Object.entries(input)){
          if(!s[key][id])s[key][id]=value;
          else if(key==='tags'&&Array.isArray(value))s[key][id]=[...new Set([...value,...s[key][id]])];
          else if(key==='testCases'&&Array.isArray(value))s[key][id]=[...new Map([...value,...s[key][id]].filter(x=>x&&typeof x.input==='string'&&typeof x.expected==='string').map(x=>[JSON.stringify(x),x])).values()].slice(0,30);
          else if(key==='notes'&&value&&typeof value==='object'){
            const local=s[key][id];const incomingMarks=Array.isArray(value.bookmarks)?value.bookmarks:value.bookmark?[{anchor:value.anchor||'',title:value.title||id}]:[];
            const localMarks=Array.isArray(local.bookmarks)?local.bookmarks:local.bookmark?[{anchor:local.anchor||'',title:local.title||id}]:[];
            s[key][id]={...value,...local,bookmarks:[...new Map([...incomingMarks,...localMarks].map(x=>[x.anchor,x])).values()]};
          }
        }
      }
      if(incoming.jobs&&typeof incoming.jobs==='object'&&!Array.isArray(incoming.jobs)){s.jobs??={};for(const [id,j] of Object.entries(incoming.jobs))if(j&&typeof j.code==='string'&&Number.isFinite(j.pid)&&!s.jobs[id])s.jobs[id]={...j,id,owner:'imported',status:j.status==='done'?'done':'interrupted',error:j.status==='done'?'':'从备份恢复的任务，请确认连接后手动重试'};}
      if(incoming.snippets&&typeof incoming.snippets==='object'&&!Array.isArray(incoming.snippets)){s.snippets??={};for(const [id,value]of Object.entries(incoming.snippets)){if(!/^[a-zA-Z0-9_-]{1,80}$/.test(id)||['__proto__','prototype','constructor'].includes(id)||Object.hasOwn(s.snippets,id)||Object.keys(s.snippets).length>=200)continue;const item=window.Snippets?.clean(value);if(item)s.snippets[id]={...item,id};}}
      if(!s.plan&&incoming.plan)s.plan=incoming.plan;
      if(Array.isArray(incoming.history)){const rounds=new Map([...(incoming.history||[]),...(s.history||[])].filter(x=>x&&Array.isArray(x.ids)&&Number.isFinite(Number(x.started))).map(x=>[String(x.id||x.started),{...x,id:String(x.id||x.started)}]));s.history=[...rounds.values()].sort((a,b)=>b.started-a.started).slice(0,50);}
      if(!s.session&&incoming.session&&Array.isArray(incoming.session.ids))s.session=incoming.session;
    });
  }
  function applyImport(){
    if(!importFile||!importData)return;const incoming=JSON.parse(JSON.stringify(importData));if(!document.getElementById('importToken').checked)delete incoming.token;
    mergeExtension(incoming.learning);const file=new File([JSON.stringify(incoming)],'progress.json',{type:'application/json'});importFile=null;importData=null;originalImport({target:{files:[file],value:''}});
  }
  importProgress=previewImport;viewSubmissions=submissions;
  for(const key of ['doSubmit','doSubmitLocal','doSubmitPythonLocal','doSubmitCppLocal'])window[key]=submitCurrent;
  // Completed results and pending jobs are visible even after navigating away.
  new MutationObserver(()=>{
    if(SET.view==='p')decorate();
    const summary=document.getElementById('lSummary');if(summary&&!document.getElementById('roundPending')){
      const id=location.hash.split('/results/')[1],jobs=Object.values(data().jobs||{}).filter(j=>String(j.round)===String(id));
      const pending=jobs.filter(jobBusy).length,failed=jobs.filter(j=>['failed','interrupted'].includes(j.status)).length;
      if(pending||failed){const el=document.createElement('p');el.id='roundPending';el.setAttribute('role','status');el.innerHTML=pending+'题等待评测，'+failed+'题未完成。'+link('查看评测任务','#/learn/tasks');summary.querySelector('h1').after(el);}
    }
  }).observe(document.getElementById('app'),{childList:true,subtree:true});
  document.addEventListener('input',()=>{const s=data().session;if(s?.exam&&!s.done&&CUR&&s.answers?.[CUR.id]){const lang=document.getElementById('langSel')?.value;if(lang&&s.answers[CUR.id].lang!==lang)update(st=>st.session.answers[CUR.id].lang=lang);}});
  // Never silently replay a task after a browser restart.
  update(s=>{for(const j of Object.values(s.jobs||{}))if(jobBusy(j)&&(j.owner===tabId||Date.now()-Number(localStorage.getItem('pta.jobHeartbeat.'+j.owner)||0)>20000)){j.status='interrupted';j.error='原页面已关闭或刷新，可手动重试';}});
  addEventListener('pagehide',()=>{update(s=>{for(const j of Object.values(s.jobs||{}))if(j.owner===tabId&&jobBusy(j)){j.status='interrupted';j.error='原页面已关闭或刷新，可手动重试';}});try{localStorage.removeItem(heartbeatKey);}catch{}});
  const css=document.createElement('style');css.textContent='.learnLinks{display:flex;flex-wrap:wrap;gap:20px;margin:22px 0}.toolCard{padding:16px;border:1px solid var(--border);border-radius:8px;margin:12px 0}.toolMetrics{display:flex;gap:28px;flex-wrap:wrap;padding:18px;background:var(--panel);border:1px solid var(--border);border-radius:10px}.toolMetrics b{font-size:26px;display:block}.calendarRow{display:flex;gap:12px;align-items:center;padding:10px 0;border-bottom:1px solid var(--border)}.calendarRow>a{flex:1}.submissionRow{display:flex;align-items:flex-start;gap:12px;padding:14px 0;border-bottom:1px solid var(--border)}.submissionRow>div{min-width:0;flex:1}.submissionRow pre{white-space:pre-wrap;overflow-wrap:anywhere}.caseEditor{display:grid;gap:8px;margin:12px 0;padding:12px;border:1px solid var(--border);border-radius:8px}.caseEditor label{display:grid;gap:5px}.caseEditor textarea{font-family:var(--mono);min-height:70px;padding:8px;color:var(--text);background:var(--panel);border:1px solid var(--border);border-radius:5px}#customCases{margin:16px 0}#toolJobStatus{font-size:13px;color:var(--muted);padding:6px 0}#dailyLimit{width:80px;padding:8px;background:var(--panel);color:var(--text);border:1px solid var(--border)}@media(max-width:800px){.calendarRow{flex-wrap:wrap}}';document.head.append(css);
  return {route,queueExam,retryJob,submitCurrent,tasks,addCase,deleteCase,sampleCases,runCases,savePlan,snooze,mastered,filterSubs,historyPage,clearSelection,compare,printSheet,closePreview,backupBeforeImport,applyImport};
})();

window.LearnTools=LearnTools;
