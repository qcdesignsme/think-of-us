from PIL import Image, ImageDraw
import numpy as np, base64, io, json
S="/mnt/user-data/uploads/Desktop/2026. Design and AI Experiments/Claude Portfolio"
def circ(im,cx,cy,r,out=256):
    im=im.convert('RGBA').crop((round(cx-r),round(cy-r),round(cx+r),round(cy+r))).resize((out,out),Image.LANCZOS)
    m=Image.new('L',(out*4,out*4),0); ImageDraw.Draw(m).ellipse((2,2,out*4-3,out*4-3),fill=255)
    m=m.resize((out,out),Image.LANCZOS)
    a=np.minimum(np.array(im.split()[3]),np.array(m)); im.putalpha(Image.fromarray(a)); return im
mc=Image.open(S+'/MC Logo circle.jpg'); a=np.array(mc.convert('L'))<200
ys,xs=np.nonzero(a); print('mc',xs.min(),xs.max(),ys.min(),ys.max())
cx=(xs.min()+xs.max())/2; cy=(ys.min()+ys.max())/2; r=max(xs.max()-xs.min(),ys.max()-ys.min())/2+1
bg=Image.new('RGBA',mc.size,'white'); bg.paste(mc); out={}
out['mc']=circ(bg,cx,cy,r)
out['usda']=circ(Image.open(S+'/USDA Logo.png'),420,244,203.5)
va=Image.open(S+'/VA logo.png').convert('RGBA'); al=np.array(va)[...,3]>40
cols=np.nonzero(al[:,45:100].any(0))[0]+45; rows=np.nonzero(al[:,cols.min():cols.max()+1].any(1))[0]
print('va',cols.min(),cols.max(),rows.min(),rows.max())
cx=(cols.min()+cols.max()+1)/2; cy=(rows.min()+rows.max()+1)/2; r=max(cols.max()-cols.min(),rows.max()-rows.min())/2+.5
out['va']=circ(va,cx,cy,r,out=128)
us=Image.open(S+'/US Logo.png').convert('RGBA'); al=np.array(us)[...,3]>40
rows=np.nonzero(al[:,632:].any(1))[0]; cx=(632+871+1)/2; cy=(rows.min()+rows.max()+1)/2; r=(871-632+1)/2
print('us',r,rows.min(),rows.max())
out['us']=circ(us,cx,cy,r)
d={}
sheet=Image.new('RGB',(4*270,270),'#212227')
for i,(k,im) in enumerate(out.items()):
    im.save(k+'.png'); b=io.BytesIO(); im.save(b,'PNG',optimize=True); d[k]='data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
    sheet.paste(im.resize((256,256)),(i*270+7,7),im.resize((256,256)))
sheet.save('crops.png'); json.dump(d,open('logos.json','w')); print({k:len(v) for k,v in d.items()})
