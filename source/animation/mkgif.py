from PIL import Image
import numpy as np, glob, os
MATTE=np.array([0x21,0x22,0x27],float)
files=sorted(glob.glob('fr/*.png'))
def prep(f,scale):
    im=Image.open(f).convert('RGBA')
    if scale!=1: im=im.resize((im.width//scale,im.height//scale),Image.LANCZOS)
    a=np.array(im).astype(float); al=a[...,3:4]/255
    rgb=a[...,:3]*al+MATTE*(1-al)          # soft edges blended onto the hero colour
    mask=a[...,3]>=10
    return rgb.astype(np.uint8),mask
for scale,name in [(1,'logo-loader@2x.gif'),(2,'logo-loader.gif')]:
    fr=[prep(f,scale) for f in files]
    # one shared palette from sample frames so colours don't flicker
    sample=np.concatenate([fr[i][0][fr[i][1]] for i in range(0,len(fr),8)])[None]
    pal_img=Image.fromarray(sample).quantize(255,method=Image.Quantize.MEDIANCUT)
    out=[]
    for rgb,mask in fr:
        p=Image.fromarray(rgb).quantize(palette=pal_img,dither=Image.Dither.NONE)
        arr=np.array(p); arr[~mask]=255; q=Image.fromarray(arr,'P')
        pal=pal_img.getpalette()[:765]+[0,0,0]; q.putpalette(pal); out.append(q)
    out[0].save('/mnt/user-data/outputs/'+name,save_all=True,append_images=out[1:],duration=50,loop=0,transparency=255,disposal=2,optimize=False)
    print(name,out[0].size,os.path.getsize('/mnt/user-data/outputs/'+name)//1024,'KB')
s=Image.open('still.png'); s.save('/mnt/user-data/outputs/logo-loader@2x.png',optimize=True)
s.resize((s.width//2,s.height//2),Image.LANCZOS).save('/mnt/user-data/outputs/logo-loader.png',optimize=True)
print(s.size, s.getpixel((2,2)))
# previews on hero bg and on white
g=Image.open('/mnt/user-data/outputs/logo-loader@2x.gif'); sheet=Image.new('RGB',(1040*2,552*2))
for k,(idx,bg) in enumerate([(22,'#212227'),(60,'#212227'),(22,'#ffffff'),(None,'#ffffff')]):
    if idx is None: im=s
    else: g.seek(idx); im=g.convert('RGBA')
    c=Image.new('RGBA',im.size,bg); c.alpha_composite(im); sheet.paste(c.convert('RGB'),((k%2)*1040,(k//2)*552))
sheet.save('gifcheck.png')
