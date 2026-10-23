/* Mobile navigation and CodeMirror-backed editing keypad. */
(()=>{
  'use strict';
  const narrow=matchMedia('(max-width:1080px)');
  let selecting=false,collapsed=false,expanded=false,currentGrid=null;
  const makeButton=(text,fn)=>{const b=document.createElement('button');b.type='button';b.textContent=text;b.addEventListener('click',fn);return b;};
  const nav=document.querySelector('.nav'),menu=makeButton('菜单',()=>{const open=nav.classList.toggle('mobileMenuOpen');menu.setAttribute('aria-expanded',String(open));});
  menu.className='mobileMenu';menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-controls','mobileNavLinks');nav.querySelector('.navlinks').id='mobileNavLinks';nav.append(menu);
  nav.addEventListener('click',e=>{if(e.target.closest('a'))closeMenu();});
  function closeMenu(){nav.classList.remove('mobileMenuOpen');menu.setAttribute('aria-expanded','false');}
  document.addEventListener('click',e=>{if(!nav.contains(e.target))closeMenu();});
  function focusMode(on){document.body.classList.toggle('mobileFocus',on);document.querySelector('[data-mobile-focus]')?.setAttribute('aria-pressed',String(on));const b=document.querySelector('[data-mobile-focus]');if(b)b.textContent=on?'退出专注':'专注';viewport();}
  function viewport(){const v=window.visualViewport;document.documentElement.style.setProperty('--mobile-height',(v?.height||innerHeight)+'px');document.documentElement.style.setProperty('--mobile-top',(v?.offsetTop||0)+'px');}
  window.visualViewport?.addEventListener('resize',viewport);window.visualViewport?.addEventListener('scroll',viewport);
  function pane(name,scroll=true){const g=document.getElementById('problemGrid');if(!g)return;if(name!=='answer'&&document.body.classList.contains('mobileFocus'))focusMode(false);g.dataset.pane=name;document.querySelectorAll('.mobileTabs button').forEach(b=>b.setAttribute('aria-selected',String(b.dataset.pane===name)));if(name==='result')g.querySelector('.mobileResultEmpty').hidden=!!document.getElementById('resultBox')?.textContent.trim()||!!document.getElementById('histBox')?.textContent.trim();if(scroll)document.querySelector('.mobileTabs')?.scrollIntoView({block:'start'});}
  function edit(action,value){
    if(typeof smartEditor!=='undefined'&&smartEditor?.mobileEdit){smartEditor.mobileEdit(action,value,selecting);status();return;}
    const box=document.getElementById('codeBox');if(!box)return;
    if(action==='insert'||action==='indent'||action==='newline'){
      const s=box.selectionStart,e=box.selectionEnd,pairs={'(':')','[':']','{':'}','"':'"',"'":"'"},text=action==='indent'?'    ':action==='newline'?'\n':value,close=pairs[text]||'';
      box.setRangeText(text+(close?box.value.slice(s,e)+close:''),s,e,'end');if(close)box.setSelectionRange(s+text.length,e+text.length);box.dispatchEvent(new Event('input',{bubbles:true}));
    }else {toast('完整编辑按键需等待代码编辑器加载完成');}
    box.focus();status();
  }
  function status(){const label=document.querySelector('.mobileKeyStatus');if(!label)return;const v=typeof smartEditor!=='undefined'?smartEditor?.view:null;const r=v?.state.selection.main;label.textContent=r?(r.empty?'光标：第 '+v.state.doc.lineAt(r.head).number+' 行':'已选 '+v.state.sliceDoc(r.from,r.to).length+' 个字符'):'符号可直接插入当前光标位置';}
  function keyboard(){
    const box=document.getElementById('codeBox');if(!box||document.querySelector('.mobileKeyboard'))return;
    const panel=document.createElement('section');panel.className='mobileKeyboard compact';panel.setAttribute('aria-label','编程辅助键盘');
    const head=document.createElement('div');head.className='mobileKeyHead';const title=document.createElement('span');title.textContent='编程辅助键盘';head.append(title);
    const more=makeButton('更多',()=>{expanded=!expanded;panel.classList.toggle('compact',!expanded);more.textContent=expanded?'精简':'更多';more.setAttribute('aria-expanded',String(expanded));});more.setAttribute('aria-expanded','false');
    const focus=makeButton('专注',()=>{const on=!document.body.classList.contains('mobileFocus');if(on)pane('answer',false);focusMode(on);});focus.dataset.mobileFocus='';focus.setAttribute('aria-pressed','false');
    const collapse=makeButton(collapsed?'展开':'收起',()=>{collapsed=!collapsed;rows.hidden=collapsed;collapse.textContent=collapsed?'展开':'收起';collapse.setAttribute('aria-expanded',String(!collapsed));});collapse.setAttribute('aria-expanded',String(!collapsed));head.append(more,focus,collapse);panel.append(head);
    const rows=document.createElement('div');rows.className='mobileKeyRows';rows.hidden=collapsed;
    const actions=[['←','left'],['↑','up'],['↓','down'],['→','right'],['Tab','indent'],['退缩进','outdent'],['行首','home'],['行尾','end'],['撤销','undo'],['重做','redo'],['换行','newline'],['退格','backspace']];
    const select=makeButton('选择',()=>{selecting=!selecting;select.setAttribute('aria-pressed',String(selecting));});select.setAttribute('aria-pressed','false');rows.append(select);
    for(const [label,action]of actions){const b=makeButton(label,()=>edit(action));if(['home','end','redo','backspace','newline'].includes(action))b.className='extraKey';rows.append(b);}
    const python=(document.getElementById('langSel')?.value||CUR?.line)==='python';const symbols=python?['(',')','[',']',':','"',"'",'=','+','-','*','/','{','}',';','<','>','\\','_','#','!','&','|','%']:['{','}','(',')','[',']',';','"',"'",'<','>','=','+','-','*','/','\\',':','_','#','!','&','|','%'];
    for(const [i,symbol]of symbols.entries()){const b=makeButton(symbol,()=>edit('insert',symbol));b.setAttribute('aria-label','插入 '+symbol);if(i>=12)b.className='extraKey';rows.append(b);}
    panel.append(rows);const label=document.createElement('output');label.className='mobileKeyStatus';label.setAttribute('aria-live','polite');panel.append(label);
    // Keep the native/editor selection and soft keyboard when pressing a key.
    panel.addEventListener('pointerdown',e=>{if(e.target.closest('button'))e.preventDefault();});
    const help=document.querySelector('.editorHelp');(help||box).after(panel);panel.classList.toggle('compact',!expanded);status();
    document.getElementById('langSel')?.addEventListener('change',()=>{panel.remove();keyboard();});
  }
  function mount(){
    const g=document.getElementById('problemGrid');if(!g){currentGrid=null;focusMode(false);return;}
    if(g!==currentGrid){currentGrid=g;selecting=false;focusMode(false);g.dataset.pane='statement';
      const tabs=document.createElement('div');tabs.className='mobileTabs';tabs.setAttribute('role','tablist');tabs.setAttribute('aria-label','做题视图');
      for(const [name,text]of [['statement','题面'],['answer','作答'],['result','结果'],['split','双栏']]){const b=makeButton(text,()=>pane(name));b.dataset.pane=name;b.setAttribute('role','tab');b.setAttribute('aria-selected',String(name==='statement'));tabs.append(b);}g.before(tabs);tabs.addEventListener('keydown',e=>{const keys=['ArrowLeft','ArrowRight','Home','End'];if(!keys.includes(e.key))return;e.preventDefault();const buttons=[...tabs.querySelectorAll('button')].filter(b=>b.getClientRects().length),i=buttons.indexOf(document.activeElement),next=e.key==='Home'?0:e.key==='End'?buttons.length-1:(i+(e.key==='ArrowRight'?1:buttons.length-1))%buttons.length;buttons[next].focus();pane(buttons[next].dataset.pane,false);});
      const toggle=g.querySelector('.psideToggle');toggle.onclick=e=>{if(!narrow.matches){toggleProblemSidebar();return;}const open=g.classList.toggle('mobileNavOpen');toggle.setAttribute('aria-expanded',String(open));toggle.textContent=open?'收起':'题号';};toggle.setAttribute('aria-expanded','false');if(narrow.matches)toggle.textContent='题号';
      const empty=document.createElement('p');empty.className='mobileResultEmpty hintline';empty.textContent='本题还没有评测结果。切换到作答后提交，即可在这里查看。';g.querySelector('.peditBody').append(empty);
      g.addEventListener('click',e=>{if(e.target.closest('#btnSubmit')&&narrow.matches){pane('result',false);}});
    }
    const empty=g.querySelector('.mobileResultEmpty');if(empty){const hidden=!!document.getElementById('resultBox')?.textContent.trim()||!!document.getElementById('histBox')?.textContent.trim();if(empty.hidden!==hidden)empty.hidden=hidden;}
    keyboard();
  }
  let pending=false;new MutationObserver(()=>{if(!pending){pending=true;requestAnimationFrame(()=>{pending=false;mount();});}}).observe(document.getElementById('app'),{childList:true,subtree:true});
  document.addEventListener('selectionchange',()=>{if(narrow.matches)status();});
  addEventListener('hashchange',()=>{closeMenu();focusMode(false);});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeMenu();focusMode(false);}});
  narrow.addEventListener('change',()=>{focusMode(false);closeMenu();});addEventListener('resize',()=>{if(innerWidth<760&&document.getElementById('problemGrid')?.dataset.pane==='split')pane('statement',false);});mount();viewport();
})();
