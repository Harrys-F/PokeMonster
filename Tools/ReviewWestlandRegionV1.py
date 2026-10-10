"""Create an annotated overview from authored metre coordinates (not a game render)."""
from pathlib import Path
import sys,math,json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];sys.dont_write_bytecode=True;sys.path.insert(0,str(ROOT/'Tools'));import WestlandRegionLayout as L
OUT=ROOT/'Art/World/WestlandRegion';W=1600;H=1240;ox=100;oy=130;s=1.6
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',20);small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',17);title=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',32)
def xy(e,n):return (ox+(e+400)*s,oy+(300-n)*s)
im=Image.new('RGB',(W,H),(240,234,217));pix=im.load()
for x in range(ox,ox+1281):
 for y in range(oy,oy+961):
  e=(x-ox)/s-400;n=300-(y-oy)/s;h=L.height(e,n);val=min(1,max(0,h/20));r=95+int(val*47);g=123+int(val*25);b=65+int(val*40);pix[x,y]=(r,g,b)
d=ImageDraw.Draw(im);d.text((100,34),'Westland – Region V1',font=title,fill='#292e24');d.text((100,79),'Gespeicherte Layout-Koordinaten · 800 × 600 m · Übersicht, kein Spielkamera-Render',font=font,fill='#44483c')
# River and organic route sampling are identical to the authoring layout.
rv=[xy(L.river(n),n) for n in range(-300,301)];d.line(rv,fill='#7ba7a6',width=17);d.line(rv,fill='#c6dcdc',width=4)
colors=['#edcb8c','#e5dbb2','#d7c9a0','#dfb078','#afc89b','#a6c7bb']
for i,(name,p,width) in enumerate(L.PATHS):d.line([xy(*v) for v in L.sample(p)],fill=colors[i],width=7 if i==0 else 4)
for b in L.buildings():
 ce,cn=b['place'];depth,width=b['size'];angle=math.radians(b['yaw']+45);points=[]
 for e,n in [(-width/2,-depth/2),(width/2,-depth/2),(width/2,depth/2),(-width/2,depth/2)]:points.append(xy(ce+e*math.cos(angle)-n*math.sin(angle),cn+e*math.sin(angle)+n*math.cos(angle)))
 d.polygon(points,fill='#9e7151',outline='#ead4a2')
for e,n in [(-310,205)]:d.rectangle([xy(e-4.5,n+4.65),xy(e+4.5,n-4.65)],fill='#a56540')
labels={'Hof':('Spielerhof',(-20,40)),'Dorf':('Dorf / Brunnen',(10,55)),'Heilhaus':('Heilhaus · +10 m',(-55,-66)),'Steinkreis':('Steinkreis · +18 m',(-20,-50)),'Wildwiesen':('Wildwiesen',(15,35)),'Waldruinen':('Waldruinen · +12 m',(-45,-55)),'Muehle':('Mühle / Felder',(10,40)),'Ausgang':('Regionsausgang',(-180,-45)),'Lichtung':('Verborgene Lichtung',(12,10)),'Aussicht':('Aussicht',(-50,-38)),'Uferfund':('Uferfund',(12,14))}
for k,(label,delta) in labels.items():
 e,n=L.PLACES[k];x,y=xy(e,n);d.ellipse((x-5,y-5,x+5,y+5),fill='#fff6d5',outline='#3b3b25');tx=x+delta[0];ty=y+delta[1];ft=small if k in ['Lichtung','Aussicht','Uferfund'] else font;box=d.textbbox((tx,ty),label,font=ft);d.rounded_rectangle((box[0]-5,box[1]-4,box[2]+5,box[3]+4),radius=4,fill='#f0e5c8');d.text((tx,ty),label,font=ft,fill='#242d22');d.line([(x,y),(tx,ty)],fill='#ece3c5',width=1)
for name,n in [('Steinbrücke',-50),('Holzbrücke',-235)]:
 e=L.river(n);x,y=xy(e,n);d.line([(x-18,y),(x+18,y)],fill='#ece1c9',width=8);d.text((x+23,y-15),name,font=small,fill='#fff3d6')
d.rectangle((ox,oy,ox+1280,oy+960),outline='#505342',width=2)
for e in range(-400,401,100):x,y=xy(e,-300);d.text((x-18,y+14),str(e)+' m',font=small,fill='#474c3d')
for n in range(-300,301,100):x,y=xy(-400,n);d.text((15,y-10),str(n)+' m',font=small,fill='#474c3d')
d.text((1410,150),'Bild-Norden ↑',font=small,fill='#38422d');d.text((1410,185),'Bild-Osten →',font=small,fill='#38422d')
for i,(name,_,_) in enumerate(L.PATHS):y=280+i*46;d.line((1415,y,1450,y),fill=colors[i],width=7);d.text((1415,y+12),name,font=small,fill='#394331')
d.text((100,1150),'Hauptroute: 1.026 m geplant · 1.041 m tatsächlich gelaufen · 210 cm/s · ca. 9:02 min mit Prüfpausen',font=font,fill='#394331');d.text((100,1185),'100 m zusätzliche Außenkulisse pro Seite. Gebäude und Figuren bleiben in ihrem bestehenden Maßstab.',font=small,fill='#394331')
im.save(OUT/'WestlandRegion_V1_Uebersicht.png')
