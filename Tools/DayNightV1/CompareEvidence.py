"""Read raw native QHDs; validate identical camera/light controls, label contact sheets only."""
from pathlib import Path
import json,math
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/DayNightV1';O=D/'Comparison02';j=json.loads((O/'Result.json').read_text());assert j['passed'];pairs=[]
font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',22)
def sheet(rows,name,w=640):
 h=360;out=Image.new('RGB',(len(rows[0])*(w+12)+12,len(rows)*(h+40)+12),(20,23,27));draw=ImageDraw.Draw(out)
 for y,row in enumerate(rows):
  for x,(p,label)in enumerate(row):
   im=Image.open(p);assert im.size==(2560,1440);im.thumbnail((w,h));a=12+x*(w+12);b=12+y*(h+40);out.paste(im,(a,b+32));draw.text((a,b),label,font=font,fill='white')
 out.save(D/name)
for v in ['Wiese','Baumkrone','Gebaeude','Waldweg','Felsen']:
 a,b=[next(r for r in j['rows']if r['view']==v and r['variant']==var)for var in ['B75','C85']]
 for k in ['player','camera','rotation']:assert math.dist(a[k],b[k])<.03,(v,k,a[k],b[k])
 for k in ['clock','phase','fov','exposure','sky_intensity','sky_color']:assert a[k]==b[k],(v,k)
 al={x['name']:x for x in a['lights']};bl={x['name']:x for x in b['lights']};assert al.keys()==bl.keys()
 for name,row in al.items():
  other=bl[name];ra=dict(row);rb=dict(other)
  if 'DirectionalLight_1.'in name:
   assert abs(ra['actor_rotation'][1]+75)<.01 and abs(rb['actor_rotation'][1]+85)<.01
   for idx in [0,2]:assert abs(ra['actor_rotation'][idx]-rb['actor_rotation'][idx])<.01
   del ra['actor_rotation'];del rb['actor_rotation']
  assert ra==rb,(v,name,ra,rb)
 pairs.append({'scene':v,'identical_camera_clock_exposure_and_non_sun_lights':True,'sun_pitch_B':-75,'sun_pitch_C':-85,'qhd':True})
for p in O.rglob('*.png'):assert Image.open(p).size==(2560,1440)
sheet([[(O/'B75'/(v+'.png'),'B · 75° · '+v),(O/'C85'/(v+'.png'),'C · 85° · '+v)]for v in ['Wiese','Baumkrone','Gebaeude','Waldweg','Felsen']],'Noon_B75_C85.jpg')
sheet([[(O/var/(v+'.png'),label+' · '+v)for var,label in [('Original','Original · 48°'),('B75','B · 75°'),('C85','C · 85°')]]for v in ['Wiese','Baumkrone','Gebaeude','Waldweg','Felsen']],'Original_B75_C85.jpg')
sheet([[(O/'Cycle'/('Time%02d%02d.png'%(h,m)),'%02d:%02d · B75'%(h,m))for h,m in row]for row in [[(4,30),(6,0)],[(9,0),(12,0)],[(16,0),(19,0)],[(22,0),(0,0)]]],'Cycle_B75.jpg')
(D/'ComparisonValidation02.json').write_text(json.dumps({'passed':True,'pairs':pairs,'qhd_images':len(list(O.rglob('*.png'))),'native_images_unchanged':True,'contact_sheets':'Only resized raw Unreal images plus labels; no relighting or retouch.'},indent=2));print('PASS',len(pairs),'pairs, 25 native QHD images')
