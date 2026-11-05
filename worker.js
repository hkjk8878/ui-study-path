/* UI Study Path only. New, independent Worker + KV.
   Required binding: STUDY_KV -> a NEW namespace (not the teuim KV).
   No login. Anyone with this Worker URL can read/write study progress.
   Endpoint: GET /api/session; POST /api/pull; POST /api/entries.
*/
const KEY_PATTERN = /^(day:\d{4}-\d{2}-\d{2}|deliverable:[\w-]+:\d+|project:[\w-]+|review:\d+|gate:[\w-]+)$/;
const PREFIX = 'ui-study-path:entry:';
const IMAGE_PREFIX = 'ui-study-path:image:';
const HTML_PREFIX = 'ui-study-path:html:';
const IMAGE_ID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
const MAX_IMAGE_SIZE = 1024 * 1024;
function cors(request){
  const origin=request.headers.get('Origin')||'*';
  return {
    'Access-Control-Allow-Origin':origin,
    'Access-Control-Allow-Methods':'GET,POST,DELETE,OPTIONS',
    'Access-Control-Allow-Headers':'Content-Type',
    'Vary':'Origin',
    'Cache-Control':'no-store',
  };
}
function result(request,data,status=200){return new Response(JSON.stringify(data),{status,headers:{...cors(request),'Content-Type':'application/json; charset=utf-8'}})}
async function readBody(request,limit){
  const length=Number(request.headers.get('Content-Length')||0);
  if(length>limit)throw new Error('요청 용량이 너무 큽니다.');
  const text=await request.text();
  if(text.length>limit)throw new Error('요청 용량이 너무 큽니다.');
  return JSON.parse(text);
}
export default {
  async fetch(request,env){
    if(request.method==='OPTIONS')return new Response(null,{status:204,headers:cors(request)});
    if(!env.STUDY_KV)return result(request,{error:'UI Study Path 전용 KV 바인딩(STUDY_KV)이 없습니다.'},503);
    const url=new URL(request.url);
    if(request.method==='GET'&&url.pathname==='/api/session')return result(request,{user:{id:'study-path-shared',email:null},backend:'cloudflare-kv-independent'});
    if(request.method==='GET'&&url.pathname==='/health')return result(request,{ok:true,app:'ui-study-path',storage:'independent-kv'});

    if(request.method==='POST'&&url.pathname==='/api/html-files'){
      if(request.headers.get('Content-Type')!=='application/octet-stream')
        return result(request,{error:'HTML 파일을 선택해 주세요.'},415);
      if(Number(request.headers.get('Content-Length'))>MAX_IMAGE_SIZE)
        return result(request,{error:'HTML 파일은 1MB 이하여야 해요.'},413);
      const bytes=await request.arrayBuffer();
      if(!bytes.byteLength||bytes.byteLength>MAX_IMAGE_SIZE)
        return result(request,{error:'HTML 파일은 1MB 이하여야 해요.'},413);
      const id=crypto.randomUUID();
      await env.STUDY_KV.put(HTML_PREFIX+id,bytes);
      return result(request,{ok:true,id},201);
    }
    const htmlFile=url.pathname.match(/^\/api\/html-files\/([0-9a-f-]{36})$/);
    if(request.method==='GET'&&htmlFile&&IMAGE_ID.test(htmlFile[1])){
      const bytes=await env.STUDY_KV.get(HTML_PREFIX+htmlFile[1],'arrayBuffer');
      if(bytes===null)return result(request,{error:'HTML 파일이 없어요.'},404);
      return new Response(bytes,{headers:{
        'Content-Type':'application/octet-stream',
        'Content-Disposition':'attachment; filename="study-exercise.html"',
        'Content-Security-Policy':"sandbox; default-src 'none'",
        'X-Content-Type-Options':'nosniff',
        'Cache-Control':'no-store',
      }});
    }

    // Compressed study images, stored as separate binary KV values (not large base64 notes).
    if(request.method==='POST'&&url.pathname==='/api/images'){
      const mime=(request.headers.get('Content-Type')||'').split(';')[0].trim().toLowerCase();
      if(!['image/webp','image/jpeg','image/png'].includes(mime))return result(request,{error:'WebP/JPEG/PNG 이미지만 업로드할 수 있어요.'},415);
      const length=Number(request.headers.get('Content-Length')||0);
      if(length>MAX_IMAGE_SIZE)return result(request,{error:'이미지는 1MB 이하여야 해요.'},413);
      try{
        const bytes=await request.arrayBuffer();
        if(!bytes.byteLength||bytes.byteLength>MAX_IMAGE_SIZE)return result(request,{error:'이미지는 1MB 이하여야 해요.'},413);
        const head=new Uint8Array(bytes,0,Math.min(bytes.byteLength,16));
        const ascii=(a,b)=>String.fromCharCode(...head.slice(a,b));
        const valid=mime==='image/webp' ? ascii(0,4)==='RIFF'&&ascii(8,12)==='WEBP' : mime==='image/png' ? head[0]===137&&ascii(1,4)==='PNG' : head[0]===255&&head[1]===216&&head[2]===255;
        if(!valid)return result(request,{error:'이미지 파일 형식이 올바르지 않아요.'},415);
        const id=crypto.randomUUID();
        await env.STUDY_KV.put(IMAGE_PREFIX+id,bytes,{metadata:{mime,size:bytes.byteLength}});
        return result(request,{ok:true,id,mime,size:bytes.byteLength},201);
      }catch(e){return result(request,{error:String(e.message||e)},500)}
    }
    const match=url.pathname.match(/^\/api\/images\/([0-9a-f-]{36})$/);
    if(match&&IMAGE_ID.test(match[1])){
      const key=IMAGE_PREFIX+match[1];
      if(request.method==='GET'){
        const {value,metadata}=await env.STUDY_KV.getWithMetadata(key,'arrayBuffer');
        if(value===null)return result(request,{error:'이미지가 없거나 삭제됐어요.'},404);
        const mime=['image/webp','image/jpeg','image/png'].includes(metadata?.mime)?metadata.mime:'application/octet-stream';
        return new Response(value,{status:200,headers:{'Content-Type':mime,'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
      }
      if(request.method==='DELETE'){
        await env.STUDY_KV.delete(key);
        return result(request,{ok:true});
      }
    }
    if(request.method==='POST'&&url.pathname==='/api/entries'){
      try{
        const body=await readBody(request,35000);
        if(!body||!KEY_PATTERN.test(body.entry_key)||!body.payload||typeof body.payload!=='object'||Array.isArray(body.payload))return result(request,{error:'저장 항목 형식이 잘못됐어요.'},400);
        const version=Date.now().toString(36)+'-'+crypto.randomUUID().slice(0,8);
        await env.STUDY_KV.put(PREFIX+body.entry_key,JSON.stringify(body.payload),{metadata:{version}});
        return result(request,{ok:true,version});
      }catch(error){return result(request,{error:String(error.message||error)},400)}
    }
    if(request.method==='POST'&&url.pathname==='/api/pull'){
      let known={};
      try{const body=await readBody(request,50000);if(body?.known&&typeof body.known==='object'&&!Array.isArray(body.known))known=body.known;}
      catch{return result(request,{error:'불러오기 요청 형식이 잘못됐어요.'},400)}
      const entries=[];let cursor;let pageCount=0;
      do{
        const page=await env.STUDY_KV.list({prefix:PREFIX,limit:1000,...(cursor?{cursor}:{})});
        const changed=page.keys.filter(record=>{const k=record.name.slice(PREFIX.length);return KEY_PATTERN.test(k) && known[k]!==record.metadata?.version});
        const rows=await Promise.all(changed.map(async record=>{
          const value=await env.STUDY_KV.get(record.name);
          if(value===null)return null;
          try{return {entry_key:record.name.slice(PREFIX.length),payload:JSON.parse(value),version:record.metadata?.version||'0'}}catch{return null}
        }));
        entries.push(...rows.filter(Boolean));
        cursor=page.list_complete?undefined:page.cursor;pageCount++;
        if(pageCount>=3)break;
      }while(cursor);
      return result(request,{entries,partial:Boolean(cursor)});
    }
    return result(request,{error:'요청을 찾을 수 없습니다.'},404);
  }
};
