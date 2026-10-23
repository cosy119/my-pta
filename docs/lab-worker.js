/* Dedicated experiment runtime; no grading APIs or question state. */
importScripts('python-local.js','cpp-local.js');
self.onmessage=async({data:m})=>{
  try{
    const result=m.lang==='python'?await PythonLocal.run(m.code,m.stdin):await CppLocal.run(m.code,m.lang,m.stdin,(phase,value)=>self.postMessage({type:'progress',phase,value}));
    self.postMessage({type:'result',result});
  }catch(e){self.postMessage({type:'result',result:{verdict:'IE',stdout:'',stderr:'',detail:String(e.message||e)}});}
};
