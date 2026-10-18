"""Labeled comparisons of unmodified genuine screenshots. Run after timed phases."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2VegetationPerfV1';O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/ImageReview');O.mkdir(exist_ok=True);photos=json.loads((S/'Photos.json').read_text())
for mode in ['PIE','Standalone']:
 for w,h,q,sp in [(1280,720,1,75),(2560,1440,2,100)]:
  selected=[p for p in photos if p['config']==[w,h,q,sp] and ('_'+mode+'_') in p['label'] and 'Scout' not in p['label']]
  if not selected:continue
  assert len(selected)==8;im=Image.new('RGB',(1920,2260),(24,24,24));draw=ImageDraw.Draw(im)
  for ri,site in enumerate(['Dorf','Wald','Weg','NPCWald']):
   for ci,variant in enumerate(['Control','FullyRough']):
    p=next(p for p in selected if p['site']==site and p['factor']=='VegPerf:'+variant);source=Image.open(p['file']);assert source.size==(w,h);im.paste(source.resize((960,540),Image.Resampling.LANCZOS),(ci*960,ri*565+25));draw.text((ci*960+4,ri*565+4),f'{mode} {site} | {variant} | {w}x{h} Q{q} SP{sp}',fill='white')
  stem=f'{mode}_{w}_Q{q}_SP{sp}_AB';im.save(O/(stem+'.png'));im.crop((0,565,1920,1130)).save(O/(stem+'_Wald.png'))
print('Genuine photo comparisons complete')
