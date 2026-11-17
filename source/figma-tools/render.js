const fs=require('fs'),kiwi=require('kiwi-schema'),pako=require('pako'),fzstd=require('fzstd');
function parse(p){const b=fs.readFileSync(p);let o=12;const chunks=[];while(o<b.length){const n=b.readUInt32LE(o);o+=4;chunks.push(b.subarray(o,o+n));o+=n;}
const dec=c=>{ if(c[0]==0x28&&c[1]==0xb5) return fzstd.decompress(c); try{return pako.inflateRaw(c)}catch(e){return fzstd.decompress(c)} };
return kiwi.compileSchema(kiwi.decodeBinarySchema(dec(chunks[0]))).decodeMessage(dec(chunks[1]));}
const name=process.argv[2];const m=parse(name+'/canvas.fig');
const id=g=>g?g.sessionID+':'+g.localID:null;
const by={},kids={};for(const n of m.nodeChanges){by[id(n.guid)]=n;const p=n.parentIndex&&id(n.parentIndex.guid);if(p)(kids[p]=kids[p]||[]).push(n);}
for(const k in kids)kids[k].sort((a,b)=>a.parentIndex.position<b.parentIndex.position?-1:(a.parentIndex.position>b.parentIndex.position?1:0));
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
const col=(p)=>{const c=p.color,a=(c.a??1)*(p.opacity??1);return `rgba(${Math.round(c.r*255)},${Math.round(c.g*255)},${Math.round(c.b*255)},${+a.toFixed(3)})`};
const solid=ps=>{if(!ps)return null;const v=ps.filter(p=>p.visible!==false&&p.type==='SOLID');return v.length?col(v[v.length-1]):null};
function blobPath(i){const b=m.blobs[i]&&m.blobs[i].bytes;if(!b)return '';const dv=new DataView(b.buffer,b.byteOffset,b.byteLength);let o=0,d='';const f=()=>{const v=dv.getFloat32(o,true);o+=4;return +v.toFixed(2)};
 while(o<b.length){const c=b[o++];if(c===0)d+='Z';else if(c===1)d+=`M${f()} ${f()}`;else if(c===2)d+=`L${f()} ${f()}`;else if(c===3)d+=`Q${f()} ${f()} ${f()} ${f()}`;else if(c===4)d+=`C${f()} ${f()} ${f()} ${f()} ${f()} ${f()}`;else break;}return d;}
const texts=[];
function ovKey(path){return path.map(id).join('/')}
function render(n,ctx,depth){ // ctx: {path:[], ov:Map, derived:Map}
  const kid_=id(n.overrideKey||n.guid);const key=ctx.path.concat([kid_]).join('/');
  let N=n; const o=ctx.ov.get(key), dd=ctx.derived.get(key);
  if(o||dd) N=Object.assign({},n,dd||{},o||{});
  if(N.componentPropRefs&&ctx.props){ for(const r of N.componentPropRefs){ const v=ctx.props.get(id(r.defID)); if(!v)continue; if(N===n)N=Object.assign({},n);
      if(r.componentPropNodeField==='TEXT_DATA'&&v.textValue)N.textData=Object.assign({},N.textData,{characters:v.textValue.characters});
      else if(r.componentPropNodeField==='VISIBLE'&&v.boolValue!=null)N.visible=v.boolValue;
      else if(r.componentPropNodeField==='OVERRIDDEN_SYMBOL_ID'&&v.guidValue)N.overriddenSymbolID=v.guidValue; } }
  if(N.visible===false) return '';
  const w=N.size?N.size.x:0,h=N.size?N.size.y:0,t=N.transform||{m00:1,m01:0,m02:0,m10:0,m11:1,m12:0};
  let st=`position:absolute;left:0;top:0;width:${w.toFixed(1)}px;height:${h.toFixed(1)}px;transform:matrix(${t.m00},${t.m10},${t.m01},${t.m11},${t.m02},${t.m12});transform-origin:0 0;box-sizing:border-box;`;
  if(N.opacity!=null&&N.opacity<1)st+=`opacity:${N.opacity};`;
  const fill=solid(N.fillPaints),stroke=solid(N.strokePaints);
  const r=N.cornerRadius||0; const rr=N.rectangleCornerRadiiIndependent?`${N.rectangleTopLeftCornerRadius||0}px ${N.rectangleTopRightCornerRadius||0}px ${N.rectangleBottomRightCornerRadius||0}px ${N.rectangleBottomLeftCornerRadius||0}px`:(r?r+'px':'');
  let inner='';
  const type=N.type;
  if(type==='TEXT'){
    const td=N.textData||{};const chars=td.characters||'';texts.push(chars);
    const fs_=N.fontSize||14,lh=N.lineHeight?(N.lineHeight.units==='PIXELS'?N.lineHeight.value+'px':N.lineHeight.units==='PERCENT'?(N.lineHeight.value/100):'normal'):'normal';
    const fam=N.fontName?N.fontName.family:'sans-serif',sty=N.fontName?N.fontName.style:'';
    const wt=/black/i.test(sty)?900:/extra ?bold/i.test(sty)?800:/semi ?bold/i.test(sty)?600:/bold/i.test(sty)?700:/medium/i.test(sty)?500:/light/i.test(sty)?300:400;
    st+=`color:${fill||'#000'};font:${/italic/i.test(sty)?'italic ':''}${wt} ${fs_}px/${lh} '${fam}',sans-serif;white-space:pre-wrap;text-align:${(N.textAlignHorizontal||'LEFT').toLowerCase()};`;
    if(N.letterSpacing&&N.letterSpacing.value)st+=`letter-spacing:${N.letterSpacing.units==='PERCENT'?N.letterSpacing.value/100+'em':N.letterSpacing.value+'px'};`;
    if(N.textDecoration==='UNDERLINE')st+='text-decoration:underline;';
    if(N.textAlignVertical==='CENTER')st+='display:flex;align-items:center;'+(N.textAlignHorizontal==='CENTER'?'justify-content:center;':'');
    return `<div style="${st}" data-n="${esc(N.name)}"><span>${esc(chars)}</span></div>`;
  }
  if(['VECTOR','BOOLEAN_OPERATION','ELLIPSE','LINE','STAR','REGULAR_POLYGON'].includes(type)){
    if(type==='ELLIPSE'){st+=`border-radius:50%;`+(fill?`background:${fill};`:'')+(stroke?`border:${N.strokeWeight||1}px solid ${stroke};`:'');return `<div style="${st}"></div>`;}
    if(type==='LINE'){return `<div style="${st}border-top:${N.strokeWeight||1}px solid ${stroke||'#000'};height:0"></div>`;}
    let paths='';for(const g of N.fillGeometry||[]){ if(g.commandsBlob!=null&&fill)paths+=`<path d="${blobPath(g.commandsBlob)}" fill="${fill}" fill-rule="${g.windingRule==='ODD'?'evenodd':'nonzero'}"/>`;}
    for(const g of N.strokeGeometry||[]){ if(g.commandsBlob!=null&&stroke)paths+=`<path d="${blobPath(g.commandsBlob)}" fill="${stroke}"/>`;}
    if(type==='BOOLEAN_OPERATION'&&!paths){ for(const c of kids[id(n.guid)]||[]) inner+=render(c,ctx,depth+1); return `<div style="${st}">${inner}</div>`;}
    return `<svg style="${st}overflow:visible" viewBox="0 0 ${w||1} ${h||1}">${paths}</svg>`;
  }
  // containers
  if(fill)st+=`background:${fill};`;
  const img=(N.fillPaints||[]).find(p=>p.type==='IMAGE'&&p.visible!==false);
  if(img&&img.image&&img.image.hash){const hx=Buffer.from(img.image.hash).toString('hex');st+=`background:#ddd url(images/${hx}) center/cover;`;}
  if(stroke){const sw=N.strokeWeight||1; if(N.borderStrokeWeightsIndependent){st+=`border-style:solid;border-color:${stroke};border-width:${N.borderTopWeight||0}px ${N.borderRightWeight||0}px ${N.borderBottomWeight||0}px ${N.borderLeftWeight||0}px;`}else st+=`box-shadow:inset 0 0 0 ${sw}px ${stroke};`;}
  if(rr)st+=`border-radius:${rr};`;
  for(const e of N.effects||[]){ if(e.visible!==false&&e.type==='DROP_SHADOW'){st+=`filter:drop-shadow(${e.offset.x}px ${e.offset.y}px ${e.radius/2}px ${col({color:e.color})});`;break;} }
  if((type==='FRAME'||type==='SYMBOL'||type==='INSTANCE')&&N.frameMaskDisabled===false)st+='overflow:hidden;';
  if(type==='INSTANCE'&&N.symbolData&&N.symbolData.symbolID){
    const sym=by[id(N.overriddenSymbolID||N.symbolData.symbolID)];
    if(sym){
      const path=ctx.path.concat([kid_]);
      const ov=new Map(ctx.ov),derived=new Map(ctx.derived);
      // overrides defined on this instance: guidPath relative to this instance
      for(const so of (N.symbolData.symbolOverrides||[])){ if(!so.guidPath)continue; const k=path.concat(so.guidPath.guids.map(id)).join('/'); const {guidPath,...rest}=so; ov.set(k,Object.assign({},ov.get(k)||{},rest)); }
      for(const ds of (N.derivedSymbolData||[])){ if(!ds.guidPath)continue; const k=path.concat(ds.guidPath.guids.map(id)).join('/'); const {guidPath,...rest}=ds; derived.set(k,Object.assign({},derived.get(k)||{},rest)); }
      // overrides from outer on nested instance's own symbol swap
      const props=new Map();for(const a of N.componentPropAssignments||[])props.set(id(a.defID),a.value||{});const c2={path,ov,derived,props};
      // scale if no derived data and size differs
      let sc=''; if(!(N.derivedSymbolData||[]).length&&sym.size&&(Math.abs(sym.size.x-w)>0.5||Math.abs(sym.size.y-h)>0.5)) sc=`transform:scale(${w/sym.size.x},${h/sym.size.y});transform-origin:0 0;position:absolute;left:0;top:0;width:${sym.size.x}px;height:${sym.size.y}px`;
      for(const c of kids[id(sym.guid)]||[]) inner+=render(c,c2,depth+1);
      if(sc)inner=`<div style="${sc}">${inner}</div>`;
      if(!fill&&!N.fillPaints){const sf=solid(sym.fillPaints);if(sf)st+=`background:${sf};`;}
    }
  } else for(const c of kids[id(n.guid)]||[]) inner+=render(c,ctx,depth+1);
  return `<div style="${st}" data-n="${esc(N.name)}">${inner}</div>`;
}
const targets=process.argv.slice(3);
fs.mkdirSync('out',{recursive:true});
for(const tid of targets){const n=by[tid];texts.length=0;
  const base=Object.assign({},n,{transform:{m00:1,m01:0,m02:0,m10:0,m11:1,m12:0}});
  const body=render(base,{path:[],ov:new Map(),derived:new Map()},0);
  const f=`out/${name}-${tid.replace(':','_')}.html`;
  fs.writeFileSync(f,`<html><head><link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@400;500;600;700&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet"></head><body style="margin:0;background:#888;position:relative;width:${n.size.x}px;height:${n.size.y}px">${body}</body></html>`);
  fs.writeFileSync(f.replace('.html','.txt'),texts.join('\n'));
  console.log(f,n.name,Math.round(n.size.x),Math.round(n.size.y),'texts',texts.length);}
