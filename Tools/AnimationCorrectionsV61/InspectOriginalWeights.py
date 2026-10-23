import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[2];out={}
for p in sorted((R/'Art/Characters/YoungTrainer/Source').glob('*.blend')):
 bpy.ops.wm.open_mainfile(filepath=str(p));o=bpy.data.objects.get('Player_Meshy_Body')
 if not o:continue
 ids=[3501,3272,6149];out[p.name]=dict(vertices=len(o.data.vertices),groups=[g.name for g in o.vertex_groups],examples=[dict(index=i,co=list(o.data.vertices[i].co),weights={o.vertex_groups[g.group].name:g.weight for g in o.data.vertices[i].groups})for i in ids if i<len(o.data.vertices)])
(R/'Saved/AnimationCorrectionsV61/OriginalWeights.json').write_text(json.dumps(out,indent=2))
