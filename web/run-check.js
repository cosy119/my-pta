/* Self-test output comparison. It never submits answers or updates grades. */
const RunCheck=(()=>{
  const E=esc,LIMIT=30000;let busy=false,last=null,visible=true;
  const exactInput=s=>String(s??'').replace(/\r\n/g,'\n');
  function reference(problem,input){
    const mode=document.getElementById('runRefMode')?.value||'auto';
    if(mode==='custom')return {text:document.getElementById('runExpected')?.value||'',title:'预期输出（自定义）'};
    const i=(problem.samples||[]).findIndex(s=>exactInput(s.stdin)===exactInput(input));
    return i<0?{text:null,title:'示例输出',note:'当前输入未匹配题目样例。可载入样例输入，或填写自定义预期输出。'}:{text:String(problem.samples[i].expected_stdout??''),title:'示例输出（样例 '+(i+1)+'）'};
  }
  function sourceHint(){const custom=document.getElementById('runRefMode')?.value==='custom';const field=document.getElementById('runExpectedField');if(field)field.hidden=!custom;const p=CUR;if(!p)return;const r=reference(p,document.getElementById('stdinBox')?.value||'');const hint=document.getElementById('runRefHint');if(hint)hint.textContent=r.text===null?r.note:custom?'按你填写的预期输出比较；留空表示预期没有输出。':'运行后与'+r.title+'逐字符对照。';}
  function decorate(){
    const input=document.getElementById('stdinBox');if(!input||!document.getElementById('codeEditor')||document.getElementById('runReference'))return;
    const box=document.createElement('details');box.id='runReference';box.innerHTML='<summary>自测输出对照设置</summary><div class="runRefFields"><label>对照来源<select id="runRefMode"><option value="auto">自动匹配题目样例</option><option value="custom">自定义预期输出</option></select></label>'+((CUR.samples||[]).length?'<label>载入样例输入<select id="runSample">'+CUR.samples.map((_,i)=>'<option value="'+i+'">样例 '+(i+1)+'</option>').join('')+'</select></label><button type="button" class="btn ghost" onclick="RunCheck.loadSample()">载入此样例</button>':'')+'</div><label id="runExpectedField" hidden>预期输出<textarea id="runExpected" rows="3" spellcheck="false"></textarea></label><p id="runRefHint" class="hintline"></p>';
    input.closest('details').after(box);document.getElementById('runExpected').value=practiceDraft('expected',CUR.id)||'';document.getElementById('runRefMode').value=practiceDraft('expectedMode',CUR.id)==='custom'?'custom':'auto';
    input.addEventListener('input',sourceHint);document.getElementById('runRefMode').addEventListener('change',e=>{savePracticeDraft('expectedMode',CUR.id,e.target.value);sourceHint();});document.getElementById('runExpected').addEventListener('input',e=>savePracticeDraft('expected',CUR.id,e.target.value));sourceHint();
  }
  function loadSample(){const s=CUR?.samples?.[Number(document.getElementById('runSample')?.value)];if(!s)return;const input=document.getElementById('stdinBox');input.value=s.stdin||'';savePracticeDraft('stdin',CUR.id,input.value);document.getElementById('runRefMode').value='auto';savePracticeDraft('expectedMode',CUR.id,'auto');input.dispatchEvent(new Event('input',{bubbles:true}));input.closest('details').open=true;sourceHint();}
  function bounds(a,b){const x=Array.from(a),y=Array.from(b);let from=0,tail=0;while(from<Math.min(x.length,y.length)&&x[from]===y[from])from++;while(tail<Math.min(x.length,y.length)-from&&x[x.length-tail-1]===y[y.length-tail-1])tail++;return {from,aEnd:x.length-tail,bEnd:y.length-tail,x,y};}
  function description(c){return c===undefined?'输出结束':c===' '?'空格':c==='\n'?'换行 LF':c==='\r'?'回车 CR':c==='\t'?'制表符 Tab':'“'+c+'”';}
  function firstDiff(a,b){if(a===b)return '字符完全一致，包括空格和换行。';const d=bounds(a,b),prefix=d.x.slice(0,d.from),line=prefix.filter(c=>c==='\n').length+1,col=prefix.length-prefix.lastIndexOf('\n');return '首处差异：第 '+line+' 行，第 '+col+' 列；我的输出为'+description(d.x[d.from])+'，对照输出为'+description(d.y[d.from])+'。';}
  function output(text,from,end,show){
    if(!text)return '<div class="runEmpty">（空输出，0 个字符）</div>';
    const chars=Array.from(text),count=Math.min(chars.length,LIMIT);let html='<div class="runOutputLine"><span class="runLineNo" aria-hidden="true">1</span><span class="runLineText">',line=1;
    for(let i=0;i<count;i++){
      const c=chars[i];let token=c===' '?show?'<span class="runWs" title="空格 U+0020">·</span>':' ':c==='\t'?show?'<span class="runWs" title="制表符 Tab U+0009">⇥</span>':'\t':c==='\r'?'<span class="runWs" title="回车 CR U+000D">'+(show?'␍':'')+'</span>':c==='\n'?show?'<span class="runWs" title="换行 LF U+000A">↵</span>':'':E(c);
      if(i>=from&&i<end)token='<mark class="runMismatch">'+token+'</mark>';html+=token;
      if(c==='\n')html+='</span></div><div class="runOutputLine"><span class="runLineNo" aria-hidden="true">'+(++line)+'</span><span class="runLineText">';
    }
    html+='<span class="runEof'+(from===chars.length&&end===chars.length?' runMismatch':'')+'" title="输出结束标记，不属于实际输出">'+(count<chars.length?'已截断':'EOF')+'</span></span></div>';return html;
  }
  function stats(text){const xs=Array.from(text);return xs.length+' 字符 · '+xs.filter(c=>c===' ').length+' 空格 · '+xs.filter(c=>c==='\n').length+' 换行 · '+xs.filter(c=>c==='\t').length+' Tab';}
  function pair(actual,expected,expectedTitle='示例输出',show=true,note=''){
    actual=String(actual??'');const has=expected!==null&&expected!==undefined;expected=has?String(expected):'';const d=has&&actual!==expected?bounds(actual,expected):{from:Infinity,aEnd:0,bEnd:0};
    return '<div class="runOutputPair"><section><h4>我的输出</h4><p class="hintline">'+stats(actual)+'</p><div class="runOutput" role="region" aria-label="我的输出" tabindex="0">'+output(actual,d.from,d.aEnd,show)+'</div></section><section><h4>'+E(expectedTitle)+'</h4>'+(has?'<p class="hintline">'+stats(expected)+'</p><div class="runOutput" role="region" aria-label="'+E(expectedTitle)+'" tabindex="0">'+output(expected,d.from,d.bEnd,show)+'</div>':'<p class="hintline">'+E(note||'没有与当前输入对应的示例输出。')+'</p>')+'</section></div>';
  }
  function render(scroll=false){if(!last)return;const r=last.result,ref=last.ref,success=(r.verdict==='OK'||(!r.verdict&&r.ok===true))&&r.ok!==false,verdict=r.verdict||(r.ok?'OK':'IE');let html=verdictHtml(verdict,success?'自测运行完成':({CE:'编译错误',RE:'运行错误',TLE:'运行超时',IE:'运行环境失败'}[verdict]||'运行未成功'),r.detail||r.message||'');
    const ms=r.time_ms??r.ms;if(ms!==undefined&&ms!==null)html+='<div class="resMeta"><span>耗时 <b>'+E(ms)+' ms</b></span>'+(r.mem_kb!==undefined?'<span>内存 <b>'+((Number(r.mem_kb)||0)/1024).toFixed(1)+' MB</b></span>':'')+'</div>';
    html+='<p class="hintline">本次输入与输出均为点击运行时的快照。自测不计成绩，下面按原始字符比较，正式判题规则可能允许部分格式差异。</p><label class="runVisible"><input type="checkbox" '+(visible?'checked':'')+' onchange="RunCheck.toggle(this.checked)">显示空白字符：· 空格　↵ 换行　⇥ Tab　␍ 回车</label>';
    if(success&&ref.text!==null)html+='<p class="runCompareStatus" role="status">'+E(firstDiff(String(r.stdout??''),ref.text))+'</p>';else if(!success)html+='<p class="runCompareStatus">运行未成功，不判定输出是否匹配。</p>';
    html+=pair(r.stdout,ref.text,ref.title,visible,ref.note)+'<div class="btnrow"><button type="button" class="btn ghost" onclick="RunCheck.copyOutput(\'actual\')">复制我的原始输出</button>'+(ref.text!==null?'<button type="button" class="btn ghost" onclick="RunCheck.copyOutput(\'expected\')">复制对照原始输出</button>':'')+'</div>';
    if(r.compile_output)html+=ioRow('编译器信息',r.compile_output,'err');if(r.stderr)html+=ioRow('标准错误',r.stderr,'err');html+='<details><summary>查看本次自测输入</summary><pre>'+E(last.input)+'</pre></details>';const rb=document.getElementById('resultBox');rb.innerHTML=html;if(scroll&&innerWidth>1080){const body=rb.closest('.peditBody');if(body)body.scrollTop+=rb.getBoundingClientRect().top-body.getBoundingClientRect().top-8;}
  }
  function toggle(value){visible=value;render();}
  async function copyOutput(which){try{await navigator.clipboard.writeText(which==='actual'?String(last.result.stdout??''):last.ref.text);toast('已复制原始文本，不含可视标记','ok');}catch{toast('复制失败，请检查剪贴板权限','err');}}
  async function run(){
    if(busy){toast('自测正在运行，请稍候');return;}if(!Learning.canEdit()){toast('请先接管当前考试');return;}if(Object.values(Learning.data().jobs||{}).some(j=>['queued','running','polling'].includes(j.status))){toast('请等待当前评测完成后再运行自测');return;}
    const p=CUR,code=codeValue();if(!p||!code.trim()){toast('代码不能为空','err');return;}const version=routeVersion,input=document.getElementById('stdinBox')?.value||'',ref=reference(p,input),lang=document.getElementById('langSel')?.value||p.line,interp=document.getElementById('interpSel')?.value||(lang==='c'?'gcc':lang==='cpp'?'gpp':'py313');const current=()=>version===routeVersion&&SET.view==='p'&&CUR?.id===p.id;busy=true;
    for(const b of document.querySelectorAll('#btnRow button'))b.disabled=true;
    if(innerWidth<=1080)document.querySelector('.mobileTabs [data-pane=result]')?.click();document.getElementById('resultBox').innerHTML=verdictHtml('pending','正在运行自测…','首次可能需要加载运行引擎。');
    try{let r;if(!OFFLINE)r=await api('/api/run',{method:'POST',body:{code,lang,interpreter:interp,stdin:input,time_limit_ms:5000,memory_limit_mb:256}});else if(p.line==='python')r=await PythonLocal.run(code,input);else r=await CppLocal.run(code,lang,input,(phase,percent,_total,detail)=>{if(current())document.getElementById('resultBox').innerHTML=verdictHtml('judging',phase==='compile'?'正在编译 C/C++…':(detail||'正在加载 C/C++ · '+percent+'%'),'');});if(current()){last={result:r||{verdict:'IE',detail:'未返回运行结果'},ref,input};render(true);}}
    catch(e){if(current()){last={result:{verdict:'IE',detail:String(e.message||e),stdout:''},ref,input};render(true);}}
    finally{busy=false;if(current())renderButtons();}
  }
  for(const name of ['doRun','doRunPythonLocal','doRunCppLocal'])window[name]=run;
  let scheduled=false;new MutationObserver(()=>{if(!scheduled){scheduled=true;requestAnimationFrame(()=>{scheduled=false;decorate();});}}).observe(document.getElementById('app'),{childList:true,subtree:true});
  return {run,loadSample,toggle,copyOutput,pair,firstDiff};
})();window.RunCheck=RunCheck;
