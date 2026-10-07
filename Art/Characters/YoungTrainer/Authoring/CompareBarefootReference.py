"""Native renders beside verbatim reference crops, registered by sole/crown."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer');O=R.parents[2]/'Saved/YoungTrainerReferenceRework/Review';P=(235,226,209,255)
reg=json.loads((O/'Registration.json').read_text());align=json.loads((R/'Reference/BarefootFinal/Alignment.json').read_text())
def rendered(name):
 im=Image.open(O/name).convert('RGBA');bg=Image.new('RGBA',im.size,P);bg.alpha_composite(im);return bg.convert('RGB')
for view,sheet in [('Front','Front'),('RightOrtho','Left'),('Back','Back')]:
 a=next(row for row in align['views'] if row['name']==sheet);im=Image.open(R/'Reference/BarefootFinal'/a['file']).convert('RGB');v=reg[view]
 factor=(v['sole_y_px']-v['crown_y_px'])/390;im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.LANCZOS)
 left=Image.new('RGB',(600,900),P[:3]);axis=(a['axis_global']-a['crop'][0])*factor;ground=(477-a['crop'][1])*factor
 left.paste(im,(round(v['axis_x_px']-axis),round(v['sole_y_px']-ground)))
 pair=Image.new('RGB',(1200,950),P[:3]);pair.paste(left,(0,0));pair.paste(rendered('V4_'+view+'.png'),(600,0));d=ImageDraw.Draw(pair);d.text((20,925),'REFERENCE '+sheet+' / same height and ground',fill=(45,40,35));d.text((620,925),'V4 '+view,fill=(45,40,35));pair.save(O/('Compare_'+view+'.jpg'),quality=95)
 # Geometric silhouette with the same native camera, no illustration substituted.
 silhouette=Image.open(O/('V4_'+view+'.png')).convert('RGBA');black=Image.new('RGBA',silhouette.size,(0,0,0,255));black.putalpha(silhouette.getchannel('A'));bg=Image.new('RGBA',black.size,P);bg.alpha_composite(black);bg.convert('RGB').save(O/('Silhouette_'+view+'.jpg'),quality=95)
views=['Front','FrontRight','Right','BackRight','Back','BackLeft','Left','FrontLeft'];eight=Image.new('RGB',(1600,1240),P[:3]);d=ImageDraw.Draw(eight)
for i,v in enumerate(views):
 im=rendered('V4_'+v+'.png').resize((400,600));x=i%4*400;y=i//4*620;eight.paste(im,(x,y));d.text((x+12,y+600),v,fill=(45,40,35))
eight.save(O/'EightDirections.jpg',quality=95)
game=Image.new('RGB',(1600,620),P[:3]);d=ImageDraw.Draw(game)
sheet=Image.open(R/'Reference/BarefootFinal/GameDirections.png').convert('RGB')
sheet=sheet.resize((1600,round(sheet.height*1600/sheet.width)),Image.Resampling.LANCZOS)
game.paste(sheet,(0,0));game_images=[Image.open(O/('V4_Game_'+v+'.png')).convert('RGBA') for v in views]
boxes=[im.getchannel('A').getbbox() for im in game_images]
factor=min(178/max(b[2]-b[0] for b in boxes),242/max(b[3]-b[1] for b in boxes))
for i,(v,im,box) in enumerate(zip(views,game_images,boxes)):
 im=im.crop(box);im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.LANCZOS)
 game.paste(im,(i*200+(200-im.width)//2,580-im.height),im)
 d.text((i*200+12,587),v,fill=(45,40,35))
d.text((12,610),'Elevated form review / same native camera for all directions; illustration perspective is not calibrated.',fill=(45,40,35))
game.save(O/'GameDirectionsComparison.jpg',quality=95)
four=Image.new('RGB',(1600,630),P[:3]);d=ImageDraw.Draw(four)
for i,v in enumerate(['Front','RightOrtho','Back','GamePerspective']):
 four.paste(rendered('V4_'+v+'.png').resize((400,600)),(i*400,0));d.text((i*400+12,610),v,fill=(45,40,35))
four.save(O/'FourViews.jpg',quality=95)
comparison=Image.new('RGB',(1200,1000),P[:3]);d=ImageDraw.Draw(comparison)
for v,xy in [('Front',(0,0)),('RightOrtho',(600,0)),('Back',(0,475))]:
 comparison.paste(Image.open(O/('Compare_'+v+'.jpg')).resize((600,475),Image.Resampling.LANCZOS),xy)
reference_game=Image.open(R/'Reference/BarefootFinal/GameDirections.png').crop((111,0,223,171)).convert('RGB')
reference_game=reference_game.resize((235,359),Image.Resampling.LANCZOS);comparison.paste(reference_game,(627,527))
native=Image.open(O/'V4_GamePerspective.png').convert('RGBA');native=native.crop(native.getchannel('A').getbbox())
native=native.resize((round(native.width*285/native.height),285),Image.Resampling.LANCZOS)
comparison.paste(native,(1010-native.width//2,592),native)
d.text((620,930),'Reference game view / native elevated form review',fill=(45,40,35))
d.text((620,948),'Approximate perspective, no camera calibration.',fill=(45,40,35))
d.text((18,978),'Front / Blender Right Orthographic / Back: common 1.40 m scale and sole baseline.',fill=(45,40,35))
comparison.save(O/'ComparisonFourViews.jpg',quality=95)
face=Image.new('RGB',(1400,750),P[:3]);portrait=Image.open(R/'Reference/BarefootFinal/Portrait.png').crop((0,0,295,310));portrait=portrait.resize((round(295*700/310),700),Image.Resampling.LANCZOS);face.paste(portrait,(0,0));face.paste(rendered('V4_HeadQuarter.png'),(700,0));d=ImageDraw.Draw(face);d.text((20,720),'NEW REFERENCE PORTRAIT',fill=(45,40,35));d.text((720,720),'V4 / native geometry / close review',fill=(45,40,35));face.save(O/'PortraitComparison.jpg',quality=95)
print('V4 orthographic, silhouette, four-view and eight-direction comparisons ready:',O)
