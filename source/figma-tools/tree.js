const fs=require('fs');const name=process.argv[2];const maxd=+process.argv[3]||2;
const m=JSON.parse(fs.readFileSync(name+'.json'));const id=g=>g?g.sessionID+':'+g.localID:null;
const by={},kids={};for(const n of m.nodeChanges){by[id(n.guid)]=n;const p=n.parentIndex&&id(n.parentIndex.guid);if(p)(kids[p]=kids[p]||[]).push(n);}
for(const k in kids)kids[k].sort((a,b)=>a.parentIndex.position<b.parentIndex.position?-1:1);
const root=m.nodeChanges.find(n=>n.type==='DOCUMENT');
function walk(n,d){const s=n.size?` ${Math.round(n.size.x)}x${Math.round(n.size.y)}`:'';const t=n.transform?` @${Math.round(n.transform.m02)},${Math.round(n.transform.m12)}`:'';
 console.log('  '.repeat(d)+`${n.type} "${n.name}" [${id(n.guid)}]${s}${t} kids=${(kids[id(n.guid)]||[]).length}`);
 if(d<maxd)for(const c of kids[id(n.guid)]||[])walk(c,d+1);}
walk(root,0);
