# V5 optional evidence gate: no gameplay/build validation is skipped here.
import sys as _evidence_sys
from pathlib import Path as _EvidencePath
_evidence_root = next(p for p in _EvidencePath(__file__).resolve().parents if (p/'PokeMonster.uproject').is_file())
_evidence_sys.path.insert(0, str(_evidence_root/'Tools/DevelopmentEvidence'))
from evidence import review_preflight as _review_preflight
_review_preflight(__file__)
"""Tracked enlarged crops from genuine Unreal recording, no retouching/interpolation."""
import json,csv,math,bisect,statistics
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];O=R/'Art/Characters/NPCs/Ranger/Review/AnimationV3';F=O/'Unreal/RecordingOpenPath'
a=json.loads((O/'Data/RecordedMotionOpenPath.json').read_text());samples=a['frames'];times=[x['t'] for x in samples]
rows=list(csv.DictReader((F/'Frames.csv').open()));offset=next(x['end_t'] for x in a['stages'] if x['name']=='Warmup')
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',19)
def project(p,r):
 pitch,yaw=map(math.radians,[r['pitch'],r['camera_yaw']]);d=[p[i]-r['camera'][i] for i in range(3)]
 fw=[math.cos(pitch)*math.cos(yaw),math.cos(pitch)*math.sin(yaw),math.sin(pitch)];right=[-math.sin(yaw),math.cos(yaw),0];up=[-math.sin(pitch)*math.cos(yaw),-math.sin(pitch)*math.sin(yaw),math.cos(pitch)]
 depth=sum(x*y for x,y in zip(d,fw));f=1280/(2*math.tan(math.radians(r['fov']/2)))
 return 640+sum(x*y for x,y in zip(d,right))*f/depth,370-sum(x*y for x,y in zip(d,up))*f/depth
manifest=[]
for tag,height in [('Feet',24),('Cape',110)]:
 dest=O/('Unreal/RecordingOpenPath'+tag);assert not dest.exists();dest.mkdir()
 table=[]
 for row in rows:
  t=float(row['game_seconds'])+offset;i=min(bisect.bisect_left(times,t),len(samples)-1);r=samples[i]
  pos=list(r['position']) if r['stage'] not in ['Talk','ReturnIdle'] else [-920,-1080,3]
  pos[2]+=height;x,y=project(pos,r);width,high=(150,110) if tag=='Feet' else (170,200)
  box=(round(x-width/2),round(y-high/2),round(x+width/2),round(y+high/2))
  im=Image.open(F/row['file']).convert('RGB').crop(box).resize((width*4,high*4),Image.Resampling.LANCZOS)
  frame=Image.new('RGB',(im.width,im.height+60),(24,27,30));frame.paste(im,(0,60));d=ImageDraw.Draw(frame);d.text((10,8),f"Unreal | {float(row['game_seconds']):.2f} s | {r['stage']}",font=font,fill='white');d.text((10,33),tag+' | echter Bildausschnitt, 4x vergroessert',font=font,fill='white')
  name=Path(row['file']).stem+'.jpg';frame.save(dest/name,quality=94)
  table.append([row['frame'],row['game_seconds'],row['wall_seconds'],frame.width,frame.height,name]);manifest.append({'kind':tag,'source':row['file'],'t':row['game_seconds'],'stage':r['stage'],'crop':box})
 with (dest/'Frames.csv').open('w') as f:
  w=csv.writer(f);w.writerow(['frame','game_seconds','wall_seconds','width','height','file']);w.writerows(table)
gaps=[float(b['game_seconds'])-float(a['game_seconds']) for a,b in zip(rows,rows[1:])]
(O/'Data/RecordingOpenPathAudit.json').write_text(json.dumps({'frame_count':len(rows),'seconds':float(rows[-1]['game_seconds']),'median_interval_s':statistics.median(gaps),'maximum_interval_s':max(gaps),'average_capture_fps':(len(rows)-1)/float(rows[-1]['game_seconds']),'all_output_sizes':sorted(set((r['width'],r['height']) for r in rows)),'timestamp_alignment_offset_s':offset,'limitations':['Framebuffer capture introduces readback/encoding overhead. Not a performance sample.','Crops enlarge original pixels; no additional anatomical detail is invented.','Variable actual capture timestamps preserved; no interpolated frames.'],'crop_manifest':manifest},indent=2))
print('CROPPED',len(rows),'frames each')
