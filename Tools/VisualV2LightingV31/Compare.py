"""Real QHD comparisons and declared image-code-value controls; no scene-pixel retouching."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/LightingV31';O=D/'Comparisons';O.mkdir(exist_ok=True);j=json.loads((D/'FinalComparison/Result.json').read_text());assert j['passed'];rows=[]
for b in [x for x in j['rows']if x['variant']=='Before']:
 a=next(x for x in j['rows']if x['variant']=='After'and x['view']==b['view'])
 for k in ['player','camera','rotation']:assert max(abs(v-u)for v,u in zip(a[k],b[k]))<.03,(b['view'],k)
 assert a['fov']==b['fov']and a['viewport']==b['viewport']==[2560,1440]and a['pp']==b['pp'];assert a['sun_intensity']==b['sun_intensity']and a['sky_source']==b['sky_source']and a['sky_cube']==b['sky_cube']and a['sky_intensity']==b['sky_intensity']
 name=b['view'];paths=[D/'FinalComparison'/v/(name+'.png')for v in ['Before','After']];canvas=Image.new('RGB',(1920,580),(24,24,24));draw=ImageDraw.Draw(canvas)
 for i,p in enumerate(paths):
  im=Image.open(p);assert im.size==(2560,1440);canvas.paste(im.resize((960,540),Image.Resampling.LANCZOS),(960*i,40));draw.text((960*i+16,14),name+(' - Vorher'if i==0 else' - V3.1'),fill='white')
 canvas.save(O/(name+'.jpg'),quality=95);rows.append({'view':name,'before':str(paths[0].relative_to(R)),'after':str(paths[1].relative_to(R)),'sha256':[hashlib.sha256(p.read_bytes()).hexdigest()for p in paths],'camera_match':True})
controls=[('sunny_meadow','SonnigeWiese',[140,80,450,240]),('canopy_edge_ground','Kronenrand',[1630,870,1740,965]),('player_torso','Kronenrand',[1245,700,1315,780]),('interior_floor','Innenraum',[900,750,1100,900])];metrics=[]
for label,view,roi in controls:
 vals=[]
 for v in ['Before','After']:
  im=np.asarray(Image.open(D/'FinalComparison'/v/(view+'.png')).convert('RGB').crop(roi),dtype=float)/255.;lum=im@np.array([.2126,.7152,.0722]);vals.append({'mean_code_luma':float(lum.mean()),'p20_code_luma':float(np.percentile(lum,20)),'p95_code_luma':float(np.percentile(lum,95))})
 metrics.append({'control':label,'view':view,'rectangle_xyxy':roi,'before':vals[0],'after':vals[1],'mean_relative_change_percent':(vals[1]['mean_code_luma']/vals[0]['mean_code_luma']-1)*100,'interpretation':'image code values, not physical light or universal perceptual percentages; animated subjects can vary'})
(D/'Comparisons.json').write_text(json.dumps(rows,indent=2));(D/'ImageControls.json').write_text(json.dumps(metrics,indent=2));print('QHD_PAIRS',len(rows));print(json.dumps(metrics,indent=2))
