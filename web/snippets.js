/* Personal snippets: local Learning data, escaped previews, explicit insertion. */
const Snippets=(()=>{
  const E=esc,LANGS={python:'Python',cpp:'C++',c:'C',shell:'Shell',text:'其他'},DRAFT='pta.snippetDraft';
  let picker=false,target=null,query='',filter='all';
  const all=()=>Object.entries(Learning.data().snippets||{}).filter(([id,s])=>/^[a-zA-Z0-9_-]{1,80}$/.test(id)&&!['__proto__','prototype','constructor'].includes(id)&&valid(s)).map(([id,s])=>({...s,id})).sort((a,b)=>b.updated-a.updated);
  const button=(text,call)=>'<button type="button" class="btn ghost" onclick="Snippets.'+call+'">'+text+'</button>';
  function valid(s){return s&&typeof s.title==='string'&&typeof s.code==='string'&&Object.hasOwn(LANGS,s.lang);}
  function clean(s){if(!valid(s)||!s.title.trim()||!s.code.trim()||s.code.length>20000)return null;return {title:s.title.slice(0,80),code:s.code,lang:s.lang,description:String(s.description||'').slice(0,500),updated:Number(s.updated)||Date.now(),versions:(Array.isArray(s.versions)?s.versions:[]).filter(valid).slice(0,5).map(v=>({title:v.title.slice(0,80),code:v.code.slice(0,20000),lang:v.lang,description:String(v.description||'').slice(0,500),updated:Number(v.updated)||0}))};}
  function route(){if(location.hash.split('?')[0]!=='#/learn/snippets')return false;picker=false;query='';filter='all';home();return true;}
  function home(){document.getElementById('app').innerHTML='<div class="learn snippets"><a href="#/learn">← 学习中心</a><h1>个人代码片段库</h1><p class="hintline">保存常用代码与用法。资料保存在此浏览器，完整备份包含片段；从题目编辑区可预览并插入。</p><div id="snippetMain"></div></div>';list();}
  function host(){return document.getElementById(picker?'snippetPickerBody':'snippetMain');}
  function list(){
    const root=host();if(!root)return;
    root.innerHTML='<div class="snippetFilters"><label>搜索片段<input id="snippetQuery" type="search" placeholder="名称、代码或用法" value="'+E(query)+'"></label><label>语言<select id="snippetFilter"><option value="all">全部语言</option>'+Object.entries(LANGS).map(([k,v])=>'<option value="'+k+'" '+(filter===k?'selected':'')+'>'+v+'</option>').join('')+'</select></label>'+button('新建片段','form()')+(draft()?button('继续未保存草稿','resumeDraft()'):'')+'</div><p id="snippetCount" class="hintline" role="status"></p><div id="snippetList"></div>';
    root.querySelector('#snippetQuery').addEventListener('input',e=>{query=e.target.value;results();});root.querySelector('#snippetFilter').addEventListener('change',e=>{filter=e.target.value;results();});results();
  }
  function results(){const rows=all().filter(s=>(filter==='all'||s.lang===filter)&&[s.title,s.code,s.description].join('\n').toLowerCase().includes(query.trim().toLowerCase()));const root=host();if(!root)return;root.querySelector('#snippetCount').textContent=rows.length+' / '+all().length+' 个片段';root.querySelector('#snippetList').innerHTML=rows.map(s=>'<article class="snippetCard"><h2>'+E(s.title)+'</h2><p class="hintline">'+LANGS[s.lang]+' · '+new Date(s.updated).toLocaleString()+'</p><p>'+E(s.description||'尚未填写用法说明')+'</p><details><summary>预览代码</summary><pre>'+E(s.code)+'</pre></details><div class="btnrow">'+(picker?button('插入此片段',"insert('"+s.id+"')"):'')+button('复制代码',"copy('"+s.id+"')")+button('编辑',"form('"+s.id+"')")+button('查看版本',"versions('"+s.id+"')")+button('删除',"remove('"+s.id+"')")+'</div></article>').join('')||'<div class="snippetEmpty"><p>'+ (all().length?'没有匹配片段，试试其他关键词或语言。':'还没有片段。新建一份常用代码，或在题目编辑区选择代码后保存。')+'</p></div>';}
  function commit(fn){const before=JSON.parse(JSON.stringify(Learning.data().snippets||{}));const ok=Learning.update(s=>{s.snippets??={};fn(s.snippets);});if(!ok)Learning.data().snippets=before;return ok;}
  function get(id){return all().find(s=>s.id===id);}
  function draft(){try{return JSON.parse(sessionStorage.getItem(DRAFT));}catch{return null;}}
  function persistDraft(){const root=host(),form=root?.querySelector('#snippetForm');if(!form)return;try{sessionStorage.setItem(DRAFT,JSON.stringify({id:form.dataset.id,base:Number(form.dataset.base),title:form.elements.title.value,lang:form.elements.lang.value,description:form.elements.description.value,code:form.elements.code.value}));}catch{toast('片段草稿暂存失败，请先复制代码','err');}}
  function resumeDraft(){const d=draft();if(d)form(d.id,d);}
  function form(id='',prefill){
    if(!prefill&&draft()&&!confirm('已有未保存的片段草稿，开始编辑会替换暂存草稿。继续吗？'))return;
    const s=prefill||get(id)||{title:'',lang:target?.lang||'python',description:'',code:''};
    const root=host();root.innerHTML='<form id="snippetForm" data-id="'+E(id)+'" data-base="'+E(prefill?.base??s.updated??0)+'"><h2>'+(id?'编辑片段':'新建片段')+'</h2><label>名称<input name="title" required maxlength="80" value="'+E(s.title)+'" placeholder="例如：快速输入、二分查找"></label><label>语言<select name="lang">'+Object.entries(LANGS).map(([k,v])=>'<option value="'+k+'" '+(s.lang===k?'selected':'')+'>'+v+'</option>').join('')+'</select></label><label>用法说明<textarea name="description" maxlength="500" rows="2" placeholder="适用场景、参数和注意事项">'+E(s.description||'')+'</textarea></label><label>代码<textarea name="code" required spellcheck="false" autocapitalize="off" autocorrect="off" maxlength="20000" rows="12">'+E(s.code)+'</textarea></label><p class="hintline">最多20,000字符；草稿在此标签页暂存。修改已保存片段时，保留最近5个旧版本。</p><div class="btnrow"><button class="btn" type="submit">保存片段</button>'+button('返回列表，保留草稿','list()')+'</div></form>';
    root.querySelector('form').addEventListener('submit',e=>{e.preventDefault();save();});root.querySelector('form').addEventListener('input',persistDraft);root.querySelector('form').addEventListener('change',persistDraft);persistDraft();root.querySelector('[name=title]').focus();
  }
  function save(){
    const f=host().querySelector('form'),fields=f.elements;let id=f.dataset.id;
    const item=clean({title:fields.title.value.trim(),lang:fields.lang.value,description:fields.description.value.trim(),code:fields.code.value,updated:Date.now()});if(!item){toast('请填写名称和代码，代码最多20,000字符','err');return;}
    Learning.sync();const old=get(id);if(id&&(!old||old.updated!==Number(f.dataset.base))){if(!confirm('原片段已在其他标签页修改或删除。将当前内容保存为新副本？'))return;id='';}
    if(!id&&all().length>=200){toast('最多保存200个片段，请先整理片段库','err');return;}
    item.versions=old&&id?[{title:old.title,code:old.code,lang:old.lang,description:old.description,updated:old.updated},...(old.versions||[])].slice(0,5):[];id||=crypto.randomUUID();item.id=id;
    if(!commit(s=>s[id]=item))return;
    sessionStorage.removeItem(DRAFT);query='';filter=item.lang;toast('片段已保存','ok');if(!picker)home();else list();
  }
  function remove(id){const s=get(id);if(!s||!confirm('删除片段「'+s.title+'」及其版本记录？'))return;if(commit(data=>delete data[id])){toast('片段已删除');list();}}
  async function copy(id){const s=get(id);if(!s)return;try{await navigator.clipboard.writeText(s.code);toast('代码已复制','ok');}catch{toast('复制失败，请展开预览后手动复制','err');}}
  function versions(id){const s=get(id);if(!s)return;host().innerHTML='<h2>'+E(s.title)+' · 旧版本</h2><p class="hintline">恢复时会将当前内容另存为一个旧版本。</p>'+(s.versions||[]).map((v,i)=>'<article class="snippetCard"><h3>'+E(v.title)+' · '+LANGS[v.lang]+'</h3><p>'+E(new Date(v.updated).toLocaleString())+'</p><pre>'+E(v.code)+'</pre>'+button('恢复此版本',"restore('"+id+"',"+i+')')+'</article>').join('')+(!(s.versions||[]).length?'<p>还没有旧版本。</p>':'')+button('返回列表','list()');}
  function restore(id,index){const s=get(id),v=s?.versions?.[index];if(!v||!confirm('将此旧版本恢复为当前片段？'))return;const item={...v,id,updated:Date.now(),versions:[{title:s.title,code:s.code,lang:s.lang,description:s.description,updated:s.updated},...s.versions].slice(0,5)};if(commit(d=>d[id]=item)){toast('版本已恢复','ok');list();}}
  function close(){const wasPicker=picker;picker=false;closeModal();if(wasPicker&&target?.pid===CUR?.id)smartEditor?.view?.focus();}
  function open(fromCode=false){
    if(!CUR||!document.getElementById('codeEditor'))return;if(!Learning.canEdit()){toast('请先接管当前考试再编辑');return;}
    target={pid:CUR.id,lang:document.getElementById('langSel')?.value||CUR.line};picker=true;query='';filter=target.lang in LANGS?target.lang:'all';
    document.getElementById('modalHost').innerHTML='<div class="mask"><div class="modal snippets" role="dialog" aria-modal="true" aria-labelledby="snippetPickerTitle"><div class="modalHead"><span id="snippetPickerTitle">个人代码片段</span><button class="x" type="button" aria-label="关闭片段库" onclick="Snippets.close()">✕</button></div><div class="modalBody"><p class="hintline">插入位置为编辑器光标；有选区时仅替换选中内容。插入后可撤销，不会自动提交代码。</p><div id="snippetPickerBody"></div></div></div></div>';
    if(fromCode){const v=smartEditor?.view,r=v?.state.selection.main,box=document.getElementById('codeBox');const code=v?(r.empty?v.state.doc.toString():v.state.sliceDoc(r.from,r.to)):box.value.slice(box.selectionStart,box.selectionEnd)||box.value;if(!code.trim()){toast('请先输入或选择代码');list();return;}if(draft()&&!confirm('已有片段草稿，使用当前代码创建新草稿？')){list();return;}form('',{title:'',code,description:'',lang:target.lang in LANGS?target.lang:'text'});}else{list();host().querySelector('input')?.focus();}
  }
  function insert(id){const s=get(id);if(!s||target?.pid!==CUR?.id||!document.getElementById('codeBox')){toast('题目已变化，请重新打开片段库');return;}if(!Learning.canEdit()){toast('请先接管当前考试再插入');return;}const lang=document.getElementById('langSel')?.value||CUR.line;if(s.lang!==lang&&s.lang!=='text'&&!confirm('片段语言与当前题目不同，仍要插入吗？'))return;
    if(smartEditor?.insertSnippet)smartEditor.insertSnippet(s.code);else{const box=document.getElementById('codeBox');box.setRangeText(s.code,box.selectionStart,box.selectionEnd,'end');box.dispatchEvent(new Event('input',{bubbles:true}));box.focus();}close();toast('片段已插入','ok');
  }
  let scheduled=false;new MutationObserver(()=>{if(!scheduled){scheduled=true;requestAnimationFrame(()=>{scheduled=false;const head=document.querySelector('.peditHead');if(head&&document.getElementById('codeEditor')&&!head.querySelector('.snippetEntry')){const group=document.createElement('div');group.className='snippetEntry btnrow';group.innerHTML=button('插入片段','open()')+button('存为片段','open(true)');head.append(group);}});}}).observe(document.getElementById('app'),{childList:true,subtree:true});
  addEventListener('hashchange',()=>{if(picker)close();});
  return {route,home,list,form,save,remove,copy,versions,restore,resumeDraft,open,close,insert,clean};
})();window.Snippets=Snippets;
