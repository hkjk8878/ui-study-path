/* New independent UI Study Path Worker (never reuse teuim's Worker/KV). Bind new KV as STUDY_KV. */
const KEY_PATTERN=/^(day:\d{4}-\d{2}-\d{2}|deliverable:[\w-]+:\d+|project:[\w-]+|review:\d+|gate:[\w-]+)$/;
const PREFIX='ui-study-path:entry:';
function cors(req){return {'Access-Control-Allow-Origin':req.headers.get('Origin')||'*','Access-Control-Allow-Methods':'GET,POST,OPTIONS','Access-Control-Allow-Headers':'Content-Type','Vary':'Origin','Cache-Control':'no-store'}}
function result(req,obj,status=200){return new Response(JSON.stringify(obj),{status,headers:{...cors(req),'Content-Type':'application/json; charset=utf-8'}})}
async function body(req,limit){const s=await req.text();if(s.length>limit)throw Error('요청 크기 초과');return JSON.parse(s)}
export default {async fetch(req,env){
if(req.method==='OPTIONS')return new Response(null,{status:204,headers:cors(req)});
if(!env.STUDY_KV)return result(req,{error:'새 STUDY_KV 바인딩이 필요합니다.'},503);
const u=new URL(req.url);
if(req.method==='GET'&&u.pathname==='/health')return result(req,{ok:true,app:'ui-study-path'});
if(req.method==='GET'&&u.pathname==='/api/session')return result(req,{user:{id:'study-path-shared',email:null}});
if(req.method==='POST'&&u.pathname==='/api/entries'){
try{
const j=await body(req,35000);
if(!j||!KEY_PATTERN.test(j.entry_key)||!j.payload||typeof j.payload!=='object'||Array.isArray(j.payload))return result(req,{error:'입력 형식 오류'},400);
const version=Date.now().toString(36)+'-'+crypto.randomUUID().slice(0,8);
await env.STUDY_KV.put(PREFIX+j.entry_key,JSON.stringify(j.payload),{metadata:{version}});
return result(req,{ok:true,version});
}catch(err){return result(req,{error:String(err.message||err)},400)}
}
if(req.method==='POST'&&u.pathname==='/api/pull'){
let known={};try{const j=await body(req,50000);if(j?.known&&typeof j.known==='object'&&!Array.isArray(j.known))known=j.known}catch{return result(req,{error:'요청 형식 오류'},400)}
let cursor;let parts=0;const entries=[];
do{
const page=await env.STUDY_KV.list({prefix:PREFIX,limit:1000,...(cursor?{cursor}:{})});
const updates=page.keys.filter(it=>KEY_PATTERN.test(it.name.slice(PREFIX.length))&&known[it.name.slice(PREFIX.length)]!==it.metadata?.version);
const rows=await Promise.all(updates.map(async it=>{const v=await env.STUDY_KV.get(it.name);if(!v)return null;try{return{entry_key:it.name.slice(PREFIX.length),payload:JSON.parse(v),version:it.metadata?.version||'0'}}catch{return null}}));
entries.push(...rows.filter(Boolean));cursor=page.list_complete?undefined:page.cursor;parts++;
}while(cursor&&parts<3);
return result(req,{entries,partial:!!cursor});
}
return result(req,{error:'요청을 찾을 수 없습니다.'},404);
}};