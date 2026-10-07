"""V5 / V6 comparison with fixed native cameras and unaltered reference crops.

Only review images under ignored Saved are written. All full orthographic
reference views share one sole/crown registration; game sheet is approximate.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
R=Path(__file__).resolve().parents[1]
O=R.parents[2]/'Saved/YoungTrainerHeadFormV6/Review'
B=R.parents[2]/'Saved/YoungTrainerHeadFormV5/Review'
P=(235,226,209,255);INK=(45,40,35)
font=ImageFont.load_default(size=18)
reg=json.loads((O/'Registration.json').read_text())
align=json.loads((R/'Reference/BarefootFinal/Alignment.json').read_text())
views=['Front','FrontRight','Right','BackRight','Back','BackLeft','Left','FrontLeft']

def native(version,view):
    root=B if version==5 else O
    return Image.open(root/f'V{version}_{view}.png').convert('RGBA')

def paste(out,im,xy,size=None):
    if size:im=im.resize(size,Image.Resampling.LANCZOS)
    out.paste(im,xy,im if im.mode=='RGBA' else None)

def label(out,xy,text):
    ImageDraw.Draw(out).text(xy,text,font=font,fill=INK)

def reference(view):
    a=next(row for row in align['views'] if row['name']==view)
    im=Image.open(R/'Reference/BarefootFinal'/a['file']).convert('RGB')
    v=reg[view];factor=(v['sole_y_px']-v['crown_y_px'])/390
    im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.LANCZOS)
    axis=(a['axis_global']-a['crop'][0])*factor
    ground=(477-a['crop'][1])*factor
    out=Image.new('RGB',(600,900),P[:3])
    paste(out,im,(round(v['axis_x_px']-axis),round(v['sole_y_px']-ground)))
    return out

# Full requested comparisons, including back quarters and both side conventions.
out=Image.new('RGB',(1600,2520),P[:3])
for i,view in enumerate(views):
    cell=Image.new('RGB',(800,630),P[:3])
    for j,v in enumerate([5,6]):
        paste(cell,native(v,view),(j*400,0),(400,600))
        label(cell,(j*400+12,607),f'V{v} / {view}')
    paste(out,cell,((i%2)*800,(i//2)*630))
out.save(O/'V5_V6_EightViews.jpg',quality=95)

# Front, side and back: identical whole-body scale beside reference.
out=Image.new('RGB',(1800,2850),P[:3])
for row,view in enumerate(['Front','Right','Back']):
    paste(out,reference(view),(0,row*950))
    label(out,(12,row*950+918),'Referenz / '+view)
    for col,v in enumerate([5,6],1):
        paste(out,native(v,view),(col*600,row*950))
        label(out,(col*600+12,row*950+918),f'V{v} / gleiche Kamera, Bodenlinie, Hoehe')
out.save(O/'ReferenceFrontSideBack.jpg',quality=95)

# Near head view is illustrative; do not manufacture an exact perspective overlay.
for view in ['HeadFront','HeadQuarter','HeadRight','HeadBack']:
    out=Image.new('RGB',(1400,740),P[:3])
    for j,v in enumerate([5,6]):
        paste(out,native(v,view),(j*700,0))
        label(out,(j*700+12,710),f'V{v} / {view} / identische Kamera und Beleuchtung')
    out.save(O/(view+'BeforeAfter.jpg'),quality=95)
out=Image.new('RGB',(1800,660),P[:3])
p=Image.open(R/'Reference/BarefootFinal/Portrait.png').convert('RGB').crop((0,0,295,310))
p.thumbnail((570,600),Image.Resampling.LANCZOS)
factor=600/p.height;p=p.resize((round(p.width*factor),600),Image.Resampling.LANCZOS)
paste(out,p,((600-p.width)//2,0));label(out,(12,620),'Referenzportrait / unveraenderter Ausschnitt')
for j,v in enumerate([5,6],1):
    paste(out,native(v,'HeadQuarter'),(j*600,0),(600,600))
    label(out,(j*600+12,620),f'V{v} / gleiche native Kopfkamera')
out.save(O/'HeadBeforeAfter.jpg',quality=95)

# One common crop factor for every game view and both model versions.
images=[native(v,'Game_'+view) for v in [5,6] for view in views]
boxes=[im.getchannel('A').getbbox() for im in images]
factor=min(180/max(b[2]-b[0] for b in boxes),300/max(b[3]-b[1] for b in boxes))
out=Image.new('RGB',(1600,1040),P[:3])
sheet=Image.open(R/'Reference/BarefootFinal/GameDirections.png').convert('RGB')
sheet=sheet.resize((1600,round(sheet.height*1600/sheet.width)),Image.Resampling.LANCZOS)
paste(out,sheet,(0,0));label(out,(12,315),'Referenz: illustrative Spielansichten / Perspektive nicht kalibriert')
for row,v in enumerate([5,6]):
    for i,view in enumerate(views):
        im=native(v,'Game_'+view);im=im.crop(im.getchannel('A').getbbox())
        im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.LANCZOS)
        y=355+row*320
        paste(out,im,(i*200+(200-im.width)//2,y+300-im.height))
        label(out,(i*200+8,y+302),f'V{v} / {view}')
label(out,(12,1010),'Blender-Formpruefung, keine Unreal-PIE-Kamera / gleiche Distanz, FOV, Winkel und Beleuchtung in V5 und V6')
out.save(O/'GameBeforeAfter.jpg',quality=95)
# Silhouette test uses only alpha from native geometry, no reference painted in.
out=Image.new('RGB',(1600,640),P[:3])
for i,view in enumerate(['Front','Right','Back','BackRight']):
    im=native(6,view);black=Image.new('RGBA',im.size,(30,26,22,255));black.putalpha(im.getchannel('A'))
    paste(out,black,(i*400,0),(400,600));label(out,(i*400+12,615),'V6 / '+view)
out.save(O/'Silhouettes.jpg',quality=95)
print('V5/V6 reference, eight-view, silhouette, head and game comparisons complete:',O)
