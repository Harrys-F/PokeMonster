from pathlib import Path
import json,re,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2WorldArtV7';O=Path('/Users/harry/Documents/Codex/PokeMonster_WorldArt_V7_2026-10-19');rows=[]
for phase,value in [('ShadowHalf',.5),('ShadowZero',0)]:
 aroot=S/'Photos/PIE_Q1_BeforeFinal_2560_1440';broot=S/('Photos/PIE_Q1_'+phase+'_2560_1440');ar={r['name']:r for r in json.loads((aroot/'Result.json').read_text())};br={r['name']:r for r in json.loads((broot/'Result.json').read_text())}
 for name in ar:
  assert br[name]['shadow_amount']==value
  for k in ['camera','camera_rotation_rpy','player']:assert max(abs(a-b) for a,b in zip(ar[name][k],br[name][k]))<.02
  a=np.asarray(Image.open(next(aroot.glob(name+'*.png'))).convert('RGB'),dtype=float)/255;b=np.asarray(Image.open(next(broot.glob(name+'*.png'))).convert('RGB'),dtype=float)/255;weights=np.array([.2126,.7152,.0722]);la=a@weights;lb=b@weights;mask=(la>.015)&(la<.15)
  rows.append({'phase':phase,'value':value,'view':name,'same_dark_pixels_mean_before':float(la[mask].mean()),'same_dark_pixels_mean_after':float(lb[mask].mean()),'median_dark_pixel_delta':float(np.median(lb[mask]-la[mask])),'global_luma_absolute_mean_difference':float(abs(lb-la).mean()),'is_shadow_factor_or_perceptual_50_percent_measurement':False})
(S/'ShadowProbeAnalysis.json').write_text(json.dumps({'conclusion':'No useful shadow lift in the active VSM renderer; no shadow change saved. Dark-pixel masks are diagnostics, not isolated physical shadow measurements.','rows':rows},indent=2));(O/'ShadowProbeAnalysis.json').write_bytes((S/'ShadowProbeAnalysis.json').read_bytes());print('Shadow probes:',len(rows),'paired views; max median dark pixel delta:',max(abs(r['median_dark_pixel_delta']) for r in rows))
