/* UI Study Path — offline-first app shell; data synchronizes online via separate Worker. */
const CACHE='ui-study-path-v20';
const SHELL=['./','./index.html','./payload.txt','./config.js','./manifest.webmanifest','./icon.svg'];
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).catch(()=>{}))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
const u=new URL(e.request.url);
if(e.request.method!=='GET'||u.origin!==location.origin)return;
e.respondWith(fetch(e.request,{cache:'no-store'}).then(res=>{if(res.ok){const copy=res.clone();caches.open(CACHE).then(c=>c.put(e.request,copy)).catch(()=>{})}return res}).catch(()=>caches.match(e.request).then(r=>r||caches.match('./index.html'))));
});