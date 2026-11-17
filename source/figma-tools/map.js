const fs=require('fs'),kiwi=require('kiwi-schema'),pako=require('pako'),fzstd=require('fzstd');
const b=fs.readFileSync('tou/canvas.fig');let o=12;const ch=[];while(o<b.length){const n=b.readUInt32LE(o);o+=4;ch.push(b.subarray(o,o+n));o+=n;}
const dec=c=>{ if(c[0]==0x28&&c[1]==0xb5) return fzstd.decompress(c); try{return pako.inflateRaw(c)}catch(e){return fzstd.decompress(c)} };
const m=kiwi.compileSchema(kiwi.decodeBinarySchema(dec(ch[0]))).decodeMessage(dec(ch[1]));
const id=g=>g?g.sessionID+':'+g.localID:null;const by={};for(const n of m.nodeChanges)by[id(n.guid)]=n;
const chain=n=>{const a=[];while(n){a.unshift(n.name);n=n.parentIndex&&by[id(n.parentIndex.guid)];}return a.join(' > ')};
for(const n of m.nodeChanges){for(const p of n.fillPaints||[]) if(p.type==='IMAGE'&&p.image&&p.image.hash) console.log(Buffer.from(p.image.hash).toString('hex').slice(0,8),p.visible===false?'HIDDEN':'',id(n.guid),chain(n))}
for(const n of m.nodeChanges) if(n.type==='CANVAS') console.log('CANVAS',n.name,id(n.guid));
