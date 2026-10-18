"""Labeled genuine native captures. No generated concepts or image content changes."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2TAAIntegrationV1';O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/ImageReview');O.mkdir(exist_ok=True);photos=json.loads((S/'Photos.json').read_text())
for ci,res in [('1','720p_Medium75'),('6','QHD_High100')]:
 rows=[p for p in photos if p['mode']=='Standalone' and p['label'].endswith('_C'+ci)];assert len(rows)==8
 im=Image.new('RGB',(1920,4*565),(24,24,24));draw=ImageDraw.Draw(im)
 for i,site in enumerate(['Dorf','Wald','Weg','NPCWald']):
  for j,factor in enumerate(['MapTAA:TSR','MapTAA:Native']):
   p=next(p for p in rows if p['site']==site and p['factor']==factor);source=Image.open(p['file']);assert source.size==tuple(p['viewport']);source=source.resize((960,540),Image.Resampling.LANCZOS);im.paste(source,(j*960,i*565+25));draw.text((j*960+6,i*565+5),f"{site} | {'TSR control' if j==0 else 'TAA saved map'} | {res}",fill='white')
 im.save(O/('Standalone_'+res+'_AB.png'))
print('Two genuine native A/B overviews complete')
