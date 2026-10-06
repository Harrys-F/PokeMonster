"""Review composites of native Blender renders and the unedited portrait crop."""
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];OUT=R.parents[2]/'Saved/YoungTrainerHeadPass/Review'
PAPER=(233,225,209,255)
def render(name):
 im=Image.open(OUT/name).convert('RGBA');bg=Image.new('RGBA',im.size,PAPER);bg.alpha_composite(im);return bg.convert('RGB')
portrait=Image.open(R/'Reference/HeadPass/Portrait.png').crop((0,0,287,328)).convert('RGB')
portrait=portrait.resize((round(portrait.width*500/portrait.height),500),Image.Resampling.LANCZOS)
left=Image.new('RGB',(500,500),PAPER[:3]);left.paste(portrait,((500-portrait.width)//2,0))
sheet=Image.new('RGB',(1500,570),PAPER[:3]);d=ImageDraw.Draw(sheet)
for i,(im,label) in enumerate([(left,'REFERENCE PORTRAIT'),(render('V2_Head_FrontRight.png').resize((500,500)),'BEFORE / V2'),(render('V3_Head_FrontRight.png').resize((500,500)),'AFTER / V3')]):
 sheet.paste(im,(i*500,0));d.text((i*500+15,520),label,fill=(45,40,35))
d.text((15,550),'Portrait is illustrative; V2 and V3 use the same camera and review light.',fill=(45,40,35))
sheet.save(OUT/'Portrait_Before_After.jpg',quality=95)
views=['Front','FrontRight','Right','BackRight','Back','BackLeft','Left','FrontLeft']
sheet=Image.new('RGB',(1600,860),PAPER[:3]);d=ImageDraw.Draw(sheet)
sil=Image.new('RGB',(1600,860),PAPER[:3]);sd=ImageDraw.Draw(sil)
game=Image.new('RGB',(800,420),PAPER[:3]);gd=ImageDraw.Draw(game)
for i,name in enumerate(views):
 x=(i%4)*400;y=(i//4)*430;sheet.paste(render('V3_Head_'+name+'.png').resize((400,400)),(x,y));d.text((x+12,y+410),name,fill=(45,40,35))
 original=Image.open(OUT/('V3_Head_'+name+'.png')).convert('RGBA');im=Image.new('RGBA',original.size,(0,0,0,0));im.putalpha(original.getchannel('A'))
 bg=Image.new('RGBA',im.size,PAPER);bg.alpha_composite(im);sil.paste(bg.convert('RGB').resize((400,400)),(x,y));sd.text((x+12,y+410),name,fill=(45,40,35))
 # Centre crop at native pixel size, not a zoomed replacement for the real camera.
 g=render('V3_Game25m_'+name+'.png').crop((540,275,740,455));gx=(i%4)*200;gy=(i//4)*205
 game.paste(g,(gx,gy));gd.text((gx+10,gy+184),name,fill=(45,40,35))
sheet.save(OUT/'Head_8Directions.jpg',quality=95);sil.save(OUT/'Head_Silhouette_8Directions.jpg',quality=95);game.save(OUT/'Game25m_8Directions_ActualPixels.jpg',quality=95)
full=Image.new('RGB',(1920,720),PAPER[:3]);d=ImageDraw.Draw(full)
for i,name in enumerate(['Front','ThreeQuarter','GameQuarter','GameBack']):
 full.paste(render('V3_Full_'+name+'.png').resize((480,600)),(i*480,60));d.text((i*480+12,680),name+' / close review',fill=(45,40,35))
full.save(OUT/'FullCharacter_Views.jpg',quality=95)
print('Head, portrait, silhouette and native game-distance comparison sheets complete:',OUT)
