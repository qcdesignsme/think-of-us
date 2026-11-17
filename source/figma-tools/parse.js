const fs=require('fs'),kiwi=require('kiwi-schema'),pako=require('pako'),fzstd=require('fzstd');
function parse(p){const b=fs.readFileSync(p);let o=8;const ver=b.readUInt32LE(o);o+=4;const chunks=[];while(o<b.length){const n=b.readUInt32LE(o);o+=4;chunks.push(b.subarray(o,o+n));o+=n;}
const dec=c=>{ if(c[0]==0x28&&c[1]==0xb5&&c[2]==0x2f&&c[3]==0xfd) return fzstd.decompress(c); try{return pako.inflateRaw(c)}catch(e){return fzstd.decompress(c)} };
const schema=kiwi.decodeBinarySchema(dec(chunks[0]));const compiled=kiwi.compileSchema(schema);return compiled.decodeMessage(dec(chunks[1]));}
const name=process.argv[2];const m=parse(name+'/canvas.fig');
fs.writeFileSync(name+'.json',JSON.stringify(m,(k,v)=>typeof v==='bigint'?v.toString():(v instanceof Uint8Array?{__bytes:v.length}:v)));
const nodes=m.nodeChanges;console.log(name,'nodes',nodes.length);
const tc={};for(const n of nodes)tc[n.type]=(tc[n.type]||0)+1;console.log(tc);
