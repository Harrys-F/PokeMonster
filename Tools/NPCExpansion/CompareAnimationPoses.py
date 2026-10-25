"""Confirm the new animation-only FBX reproduces the previously played native animation poses."""
from pathlib import Path
import json,math
R=Path(__file__).resolve().parents[2];O=R/'Saved/ProjectRefinement/NPCExpansion';a=json.loads((O/'AnimationPoses_before.json').read_text());b=json.loads((O/'AnimationPoses_after.json').read_text());assert a.keys()==b.keys();maximum={'translation_cm':0.,'scale':0.,'quaternion_component':0.};samples=0
for path,x in a.items():
 y=b[path];assert x['seconds']==y['seconds'];assert len(x['poses'])==len(y['poses'])
 for f,g in zip(x['poses'],y['poses']):
  id=path.split('/Library/')[1].split('/')[0]
  if id in ['WhiteHairedWarrior','DwarfWarrior','ElvenArcher']:
   f={('__armature__' if k==id+'_LibraryRig' else k):v for k,v in f.items()};g={('__armature__' if k==id+'_Rig' else k):v for k,v in g.items()}
  assert f.keys()==g.keys(),(path,f.keys(),g.keys())
  for bone,p in f.items():
   q=g[bone];samples+=1;maximum['translation_cm']=max(maximum['translation_cm'],math.dist(p['p'],q['p']));maximum['scale']=max(maximum['scale'],max(abs(u-v) for u,v in zip(p['s'],q['s'])));sign=1 if sum(u*v for u,v in zip(p['q'],q['q']))>=0 else -1;maximum['quaternion_component']=max(maximum['quaternion_component'],max(abs(u-sign*v) for u,v in zip(p['q'],q['q'])))
assert maximum['translation_cm']<.001 and maximum['scale']<.00001 and maximum['quaternion_component']<.00001,maximum
result={'passed':True,'clips':len(a),'sampled_bone_transforms':samples,'maximum_differences':maximum,'method':'17 actual Unreal raw pose samples per clip, all imported bones; before/after only this task\'s animation-only FBX reimport'};(O/'AnimationPoseComparison.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
