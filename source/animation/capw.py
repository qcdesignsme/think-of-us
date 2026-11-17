import asyncio, json
from playwright.async_api import async_playwright
FPS=20
OVR="""(t)=>{
              const hits=__HITS;
              document.querySelectorAll('.logo').forEach((l,i)=>{
                const s=t-hits[i], on=l.classList.contains('on'), col=l.querySelector('.col'), grey=l.querySelector('.grey'), name=l.querySelector('.name');
                const tilt=getComputedStyle(l).getPropertyValue('--tilt').trim()||'0deg';
                const rt=__RESET;
                if(on){ const p=Math.min(Math.max(s/.45,0),1); const e=1+ (p<1? Math.sin(p*Math.PI)*0.18*(1-p) : 0);
                  const sc=.6+(.4)*Math.min(p*2.2,1); col.style.cssText=`opacity:${Math.min(s/.12,1)};transform:scale(${(sc*e).toFixed(3)}) rotate(${tilt})`;
                  grey.style.opacity=Math.max(1-s/.18,0); name.style.animation='none';
                  name.style.transform=`translateX(-50%) scale(${(.8+.2*Math.min(p*2.2,1))*e})`; name.style.color='';
                  l.querySelectorAll('.spark').forEach(sp=>{const q=Math.min(s/.5,1);sp.style.animation='none';sp.style.opacity=s<.5?1-q:0;sp.style.transform=`rotate(${sp.style.getPropertyValue('--a')}) translateY(${-30-26*q}px) scale(${1-.7*q})`;});
                } else if(l.classList.contains('reset')){ const q=Math.min((t-rt)/.5,1);
                  col.style.cssText=`opacity:${1-q};transform:scale(${1-.1*q}) rotate(${tilt})`; grey.style.opacity=q; name.style.transform='translateX(-50%)'; name.style.color=q>.5?'':'inherit';
                  l.querySelectorAll('.spark').forEach(sp=>sp.style.opacity=0);
                } else { col.style.cssText='opacity:0'; grey.style.opacity=1; name.style.transform='translateX(-50%)'; name.style.color='';
                  l.querySelectorAll('.spark').forEach(sp=>sp.style.opacity=0);}
              });
              // limb cycle
              const r=document.getElementById('runner'); const ph=Math.sin(t/.34*Math.PI);
              if(r.classList.contains('running')){
                const set=(sel,deg)=>r.querySelectorAll(sel).forEach(e=>{e.style.animation='none';e.style.transform=`rotate(${deg}deg)`});
                set('.leg.a',34*ph); set('.leg.b',-34*ph); set('.arm.a',-40*ph); set('.arm.b',40*ph); set('.hair-back',8+4*ph);
                r.querySelector('.bob').style.cssText='animation:none;transform:translateY('+(-1-Math.cos(t/.17*Math.PI))+'px)';
              } else { r.querySelectorAll('.leg,.arm,.hair-back,.bob').forEach(e=>{e.style.transform='';e.style.animation='';}); }
            }"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':600,'height':360},device_scale_factor=2)
        await pg.goto('file:///home/claude/anim/logo-loader-wave.html'); await pg.wait_for_timeout(600)
        await pg.add_style_tag(content='html,body{background:transparent!important}.controls{display:none}*{transition:none!important;animation-play-state:paused!important}')
        cdp=await pg.context.new_cdp_session(pg)
        await cdp.send('Animation.enable')
        box=await pg.evaluate("(()=>{const r=document.getElementById('loader').getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height}})()")
        total=await pg.evaluate("__TOTAL")
        n=round(total*FPS); print('frames',n,'box',box)
        for i in range(n):
            t=i/FPS
            await pg.evaluate(f"__seek({t})")
            # drive CSS keyframe/transition-like effects deterministically
            await pg.evaluate(OVR, t)
            await pg.screenshot(path=f'frw/{i:03d}.png',clip=box,omit_background=True)
        await pg.evaluate("__seek(5.55)")
        await pg.evaluate(OVR, 5.55)
        await pg.screenshot(path='still-wave.png',clip=box,omit_background=True)
        await b.close()
asyncio.run(main())
