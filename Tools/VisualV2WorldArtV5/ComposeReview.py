"""Compose labelled genuine QHD frames, no retouch or generated review imagery."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2WorldArtV5';O=Path('/Users/harry/Documents/Codex/PokeMonster_WorldArt_V5_2026-10-19')/'Comparisons';O.mkdir(exist_ok=True)
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',25);manifest=[]
rects={'Wald':(470,440,1170,980),'Wiese':(1130,500,1830,1040),'Flussufer':(1050,30,1750,570)}
for mode in ['PIE','Standalone']:
 for quality in [1,2]:
  for pose in ['Wald','Wiese','Flussufer','HeilhausKontrolle']:
   files=[S/'Photos'/f'{mode}_Q{quality}_{phase}_2560_1440'/(pose+'00000.png') for phase in ['BeforeFinal','AfterFinal']]
   rows=[next(x for x in json.loads((p.parent/'Result.json').read_text()) if x['name']==pose) for p in files]
   for key in ['player','camera','camera_rotation_rpy']:
    assert max(abs(a-b) for a,b in zip(rows[0][key],rows[1][key]))<.02,(mode,quality,pose,key)
   for row in rows:
    assert row['viewport']==[2560,1440] and row['fov']==35 and row['screen_percentage_cvar']==100 and row['secondary_percentage_cvar']==100 and row['dynamic_resolution_mode']==0
   ims=[Image.open(p).convert('RGB') for p in files];assert all(im.size==(2560,1440) for im in ims)
   out=Image.new('RGB',(2560,780),(25,28,28));draw=ImageDraw.Draw(out)
   for i,(im,label) in enumerate(zip(ims,['VORHER V4','NACHHER V5'])):
    out.paste(im.resize((1280,720),Image.Resampling.LANCZOS),(i*1280,60));draw.text((i*1280+18,16),f'{label} | {pose} | {mode} | {"Medium" if quality==1 else "High"} | QHD / 100 %',font=font,fill='white')
   file=O/f'{mode}_Q{quality}_{pose}_BeforeAfter.png';out.save(file);manifest.append({'path':str(file),'originals':[str(p) for p in files],'identical_measured_camera':True,'presentation':'Complete frames equally reduced; no retouch.'})
   if pose in rects:
    rect=rects[pose];out=Image.new('RGB',(1400,600),(25,28,28));draw=ImageDraw.Draw(out)
    for i,(im,label) in enumerate(zip(ims,['VORHER V4','NACHHER V5'])):
     out.paste(im.crop(rect),(i*700,60));draw.text((i*700+16,16),label+' | Originalpixel-Detail',font=font,fill='white')
    file=O/f'{mode}_Q{quality}_{pose}_GroundDetail.png';out.save(file);manifest.append({'path':str(file),'originals':[str(p) for p in files],'source_crop_px':list(rect),'presentation':'Unscaled original QHD pixels, no retouch.'})
(O/'Manifest.json').write_text(json.dumps(manifest,indent=2));print('Verified comparisons:',len(manifest))
