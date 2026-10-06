"""Pixel-scale comparison sheets from unchanged reference crops and native renders."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT.parents[2]/'Saved/YoungTrainerProportions/Review'
data=json.loads((ROOT/'Reference/Orthographic/Alignment.json').read_text());factor=500*data['scale_m_per_pixel']
def reference(name):
 row=next(r for r in data['views'] if r['name']==name);l,t,r,b=row['crop'];im=Image.open(ROOT/'Reference/Orthographic'/row['file']).convert('RGBA')
 im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.LANCZOS)
 canvas=Image.new('RGBA',(640,800),(233,225,209,255));x=round(320-(row['axis_pixel_global']-l)*factor);y=round(750-(row['ground_pixel_global']-t)*factor)
 canvas.alpha_composite(im,(x,y));return canvas
def model(prefix,name):
 canvas=Image.new('RGBA',(640,800),(233,225,209,255));canvas.alpha_composite(Image.open(OUT/(prefix+'_'+name+'.png')).convert('RGBA'));return canvas
for group,names in [('FrontSide',['Front','Right']),('BackLeft',['Back','Left'])]:
 sheet=Image.new('RGB',(1200,1060),(233,225,209));d=ImageDraw.Draw(sheet)
 for row,n in enumerate(names):
  for col,(label,im) in enumerate([('REFERENCE',reference(n)),('V1',model('V1_Gray',n)),('V2',model('V2_Gray',n))]):
   im=im.resize((400,500));sheet.paste(im,(col*400,row*530));d.text((col*400+15,row*530+505),label+' / '+n,fill=(50,48,43))
 sheet.save(OUT/(group+'_Comparison.jpg'),quality=95)
 # All images share one camera/pixel scale; no eye/boot-based re-registration.
 for n in names:
  overlay=Image.blend(reference(n),model('V2_Gray',n),.5);overlay.save(OUT/('Overlay_'+n+'.png'))
names=['Front','FrontRight','Right','BackRight','Back','BackLeft','Left','FrontLeft']
sheet=Image.new('RGB',(1600,1050),(233,225,209));d=ImageDraw.Draw(sheet)
for i,n in enumerate(names):
 im=model('V2_Silhouette',n).resize((400,500));sheet.paste(im,((i%4)*400,(i//4)*525));d.text(((i%4)*400+12,(i//4)*525+505),n,fill=(50,48,43))
sheet.save(OUT/'V2_Silhouette_8Directions.jpg',quality=95)
names=['FrontRight','BackRight','BackLeft','FrontLeft','GameFront','GameBack']
sheet=Image.new('RGB',(1440,1250),(233,225,209));d=ImageDraw.Draw(sheet)
for i,n in enumerate(names):
 im=model('V2_Gray',n).resize((480,600));sheet.paste(im,((i%3)*480,(i//3)*625));d.text(((i%3)*480+12,(i//3)*625+605),n,fill=(50,48,43))
sheet.save(OUT/'V2_ThreeQuarter_Game.jpg',quality=95)
names=['Front','FrontRight','Right','BackRight','Back','BackLeft','Left','FrontLeft']
sheet=Image.new('RGB',(2400,810),(233,225,209));d=ImageDraw.Draw(sheet)
for i,n in enumerate(names):
 x=(i%4)*600;y=(i//4)*405
 sheet.paste(reference(n).resize((300,375)),(x,y))
 sheet.paste(model('V2_Gray',n).resize((300,375)),(x+300,y))
 d.text((x+12,y+380),'Reference / V2: '+n,fill=(50,48,43))
sheet.save(OUT/'V2_Reference_8Directions.jpg',quality=95)
original=Image.open(ROOT/'Reference/Character_Turnaround.png')
game_row=original.crop((19,589,922,752));game_row.save(OUT/'Reference_GameRow.png')
sheet=Image.new('RGB',(1400,820),(233,225,209));d=ImageDraw.Draw(sheet)
sheet.paste(game_row.resize((1400,253)),(0,0))
for i,(prefix,n) in enumerate([('V1_Gray','GameReferenceFront'),('V2_Gray','GameReferenceFront'),('V1_Gray','GameReferenceBack'),('V2_Gray','GameReferenceBack')]):
 sheet.paste(model(prefix,n).resize((350,438)),(i*350,280))
 d.text((i*350+12,730),prefix.split('_')[0]+' / '+n,fill=(50,48,43))
d.text((12,780),'30-degree elevated orthographic review; reference camera is illustrative, not calibrated.',fill=(50,48,43))
sheet.save(OUT/'GamePerspective_Comparison.jpg',quality=95)
print('Reference, gray, overlay and silhouette comparison sheets:',OUT)
