"""Native V6/V1 and unaltered barefoot-sheet comparisons; Saved outputs only."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parents[1];O=R.parents[2]/'Saved/YoungTrainerClothingFeetV1/Review'
P=(235,226,209,255);INK=(45,40,35);FONT=ImageFont.load_default(size=18)
reg=json.loads((O/'Registration.json').read_text());align=json.loads((R/'Reference/BarefootFinal/Alignment.json').read_text())
views=['Front','FrontRight','Right','BackRight','Back','BackLeft','Left','FrontLeft']
def native(prefix,view):return Image.open(O/(prefix+'_'+view+'.png')).convert('RGBA')
def paste(out,im,xy,size=None):
 if size:im=im.resize(size,Image.Resampling.LANCZOS)
 out.paste(im,xy,im if im.mode=='RGBA' else None)
def label(out,xy,text):ImageDraw.Draw(out).text(xy,text,font=FONT,fill=INK)
def reference(view):
 a=next(row for row in align['views'] if row['name']==view);v=reg[view];factor=(v['sole_y_px']-v['crown_y_px'])/390
 im=Image.open(R/'Reference/BarefootFinal'/a['file']).convert('RGB');im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.LANCZOS)
 out=Image.new('RGB',(600,900),P[:3]);axis=(a['axis_global']-a['crop'][0])*factor;ground=(477-a['crop'][1])*factor
 paste(out,im,(round(v['axis_x_px']-axis),round(v['sole_y_px']-ground)));return out
# Full-height / ground / axis registration, no independent body/head scaling.
out=Image.new('RGB',(1800,960),P[:3]);paste(out,reference('Front'),(0,0));paste(out,native('V6','Front'),(600,0));paste(out,native('CF1','Front'),(1200,0))
for i,t in enumerate(['Referenz / barfuessiges Sheet','V6 / vor dem Kleidungspass','ClothingFeet V1 / Kopf unveraendert']):label(out,(i*600+12,923),t)
out.save(O/'FrontBeforeAfter.jpg',quality=95)
out=Image.new('RGB',(1800,2870),P[:3])
for row,view in enumerate(['Front','Right','Back']):
 paste(out,reference(view),(0,row*950));label(out,(12,row*950+920),'Referenz / '+view)
 for col,prefix in enumerate(['V6','CF1'],1):
  paste(out,native(prefix,view),(col*600,row*950));label(out,(col*600+12,row*950+920),prefix+' / '+view)
label(out,(12,2850),'Orthographic: gleiche Bodenlinie, Achse und 1,40-m-Hoehe. Rechte Sheet-Seite ist Kamera -X.')
out.save(O/'ReferenceFrontSideBack.jpg',quality=95)
# Eight requested comparisons, with both quarter views as additional silhouette control.
out=Image.new('RGB',(1600,2520),P[:3])
for i,view in enumerate(views):
 for j,prefix in enumerate(['V6','CF1']):
  x=(i%2)*800+j*400;y=(i//2)*630
  paste(out,native(prefix,view),(x,y),(400,600));label(out,(x+12,y+606),prefix+' / '+view)
out.save(O/'EightViewsBeforeAfter.jpg',quality=95)
# Same crop factor across all elevated model views; sheet perspective approximate.
images=[native(p,'Game_'+v) for p in ['V6','CF1'] for v in views];boxes=[im.getchannel('A').getbbox() for im in images]
factor=min(180/max(b[2]-b[0] for b in boxes),300/max(b[3]-b[1] for b in boxes))
out=Image.new('RGB',(1600,1040),P[:3]);im=Image.open(R/'Reference/BarefootFinal/GameDirections.png').convert('RGB')
im=im.resize((1600,round(im.height*1600/im.width)),Image.Resampling.LANCZOS);paste(out,im,(0,0))
label(out,(12,315),'Verbindliches Sheet / gezeichnete Perspektive nicht exakt kalibriert')
for row,prefix in enumerate(['V6','CF1']):
 for i,view in enumerate(views):
  im=native(prefix,'Game_'+view);im=im.crop(im.getchannel('A').getbbox());im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.LANCZOS)
  y=355+row*320;paste(out,im,(i*200+(200-im.width)//2,y+300-im.height));label(out,(i*200+8,y+302),prefix+' / '+view)
label(out,(12,1010),'Blender-Formkamera / feste Distanz, FOV, Winkel, Beleuchtung in V6 und V1 / kein Unreal-PIE-Test')
out.save(O/'GameBeforeAfter.jpg',quality=95)
for view in ['BareFeet','FeetTop','ClothingClose']:
 im=native('CF1',view);w,h=im.size;out=Image.new('RGB',(w*2,h+50),P[:3])
 for i,prefix in enumerate(['V6','CF1']):paste(out,native(prefix,view),(i*w,0));label(out,(i*w+12,h+15),prefix+' / '+view+' / identische Kamera')
 out.save(O/(view+'BeforeAfter.jpg'),quality=95)
out=Image.new('RGB',(1600,640),P[:3])
for i,view in enumerate(['Front','Right','Back','FrontRight']):
 im=native('CF1',view);black=Image.new('RGBA',im.size,(25,22,19,255));black.putalpha(im.getchannel('A'))
 paste(out,black,(i*400,0),(400,600));label(out,(i*400+12,613),'V1 / '+view)
out.save(O/'Silhouettes.jpg',quality=95)
print('ClothingFeet V1 native comparison images ready:',O)
