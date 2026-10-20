"""Create clearly labelled crops/GIF from real QHD Unreal screenshots, never generated artwork.
Requires Pillow (available in the bundled Codex workspace Python). Originals stay unchanged.
"""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];S=R/'Saved/ZunderlaufV1';D=S/'RuntimeReviewGrounded';O=S/'Evidence';O.mkdir(exist_ok=True);j=json.loads((D/'Result.json').read_text());assert j['passed'];rows=[];rejected=[]
samples=[json.loads(x)for x in (D/'Frames.jsonl').read_text().splitlines()]
for r in j['rows']:
 paths=list(D.glob(Path(r['file']).stem+'*.png'))
 if not paths:continue
 assert len(paths)==1;im=Image.open(paths[0])
 if im.size!=(2560,1440):rejected.append({'file':paths[0].name,'actual_size':list(im.size),'reason':'Resize warm-up, excluded from QHD evidence'});continue
 r={**r,'actual':paths[0].name};r['game_time']=min((a for a in samples if a['phase']==r['phase']),key=lambda a:abs(a['phase_time']-r['time']))['game_time'];rows.append(r)
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',19);small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',15)
def crop(r):
 im=Image.open(D/r['actual']).convert('RGB').crop((1010,620,1400,930)).resize((780,620),Image.Resampling.LANCZOS);draw=ImageDraw.Draw(im);draw.rectangle((0,0,780,55),fill=(23,27,29));draw.text((12,5),r['phase']+' · '+format(r['time'],'.2f')+' s',font=font,fill='white');draw.text((12,29),'Echter QHD-Spielkameraausschnitt · 2× vergrößert',font=small,fill='#dddddd');return im
frames=[crop(r)for r in rows];dur=[max(50,min(1200,round((rows[i+1]['game_time']-r['game_time'])*1000)))if i+1<len(rows)else 500 for i,r in enumerate(rows)];frames[0].save(O/'Zunderlauf_Unreal_Bildsequenz.gif',save_all=True,append_images=frames[1:],duration=dur,loop=0,optimize=False)
phases=['Idle','Walk','Run','Attack','Hit','Faint','Happy'];contact=Image.new('RGB',(1560,4*620),(23,27,29))
for i,name in enumerate(phases):
 options=[r for r in rows if r['phase']==name];r=min(options,key=lambda r:abs(r['time']-(.9 if name=='Faint'else .55)));contact.paste(crop(r),((i%2)*780,(i//2)*620))
contact.save(O/'Sieben_Clips_Unreal.png');crop(next(r for r in rows if r['phase']=='Idle')).save(O/'Zunderlauf_Spielkamera_Detail.png');(O/'EvidenceAudit.json').write_text(json.dumps({'source':'Real Unreal PIE shots','source_dimensions':[2560,1440],'crop_box':[1010,620,1400,930],'crop_display_scale':2,'verified_images':len(rows),'requested_images':len(j['rows']),'rejected_non_qhd':rejected,'max_tail_socket_error_cm':max(a['tail_socket_error_cm']for a in samples),'phases':sorted(set(r['phase']for r in rows)),'gif':'assembled from timed real screenshots, not a realtime video recording','no_art_generated':True},indent=2));print('REAL_QHD_EVIDENCE',len(rows))
