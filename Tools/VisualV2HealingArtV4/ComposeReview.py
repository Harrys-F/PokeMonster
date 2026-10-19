"""Labelled true screenshot comparisons. Only crop/resize for presentation; no retouch."""
from pathlib import Path
import json,sys
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2HealingArtV4';O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V4_2026-10-19')/'Comparisons';O.mkdir(exist_ok=True);quality=int(sys.argv[1]);mode=sys.argv[2];afterphase=sys.argv[3] if len(sys.argv)>3 else 'After';font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',24);manifest=[]
for pose in ['Heilhaus','Vorplatz','Wegsaum','Kraeutertoepfe','Grasflaeche']:
 files=[S/'Photos'/f'{mode}_Q{quality}_{phase}_2560_1440'/(pose+'00000.png') for phase in ['Before',afterphase]];metadata=[json.loads((p.parent/'Result.json').read_text()) for p in files];rows=[next(r for r in a if r['name']==pose) for a in metadata]
 for prop in ['camera','camera_rotation_rpy','player']:
  assert max(abs(a-b) for a,b in zip(rows[0][prop],rows[1][prop]))<.02,(pose,prop,rows)
 assert rows[0]['fov']==rows[1]['fov']==35 and rows[0]['viewport']==rows[1]['viewport']==[2560,1440]
 images=[Image.open(p).convert('RGB') for p in files];assert all(i.size==(2560,1440) for i in images)
 out=Image.new('RGB',(2560,780),(25,28,28));draw=ImageDraw.Draw(out)
 for i,(im,label) in enumerate(zip(images,['VORHER','NACHHER'])):
  out.paste(im.resize((1280,720),Image.Resampling.LANCZOS),(i*1280,60));draw.text((i*1280+22,16),f'{label} | {pose} | {mode} | {"Medium" if quality==1 else "High"} | QHD / 100 %',font=font,fill='white')
 file=O/f'{mode}_Q{quality}_{pose}_BeforeAfter.png';out.save(file);manifest.append({'comparison':str(file),'originals':[str(p) for p in files],'presentation':'Both full frames scaled equally; no retouch; identical measured camera.'})
 if pose=='Vorplatz':
  rect=(690,210,1220,700);detail=Image.new('RGB',(1060,545),(25,28,28));d=ImageDraw.Draw(detail)
  for i,(im,label) in enumerate(zip(images,['VORHER','NACHHER'])):detail.paste(im.crop(rect),(i*530,55));d.text((i*530+18,14),label+' | Originalpixel-Ausschnitt',font=font,fill='white')
  detailfile=O/f'{mode}_Q{quality}_PotDetail_BeforeAfter.png';detail.save(detailfile);manifest.append({'comparison':str(detailfile),'originals':[str(p) for p in files],'source_crop_px':list(rect),'presentation':'Unscaled crop from true QHD frames, no retouch.'})
(O/f'{mode}_Q{quality}_Manifest.json').write_text(json.dumps(manifest,indent=2));print('COMPARISONS',len(manifest),flush=True)
