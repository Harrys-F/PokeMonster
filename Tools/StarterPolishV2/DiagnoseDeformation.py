import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[2];rows=[]
for species,file,bodyname,rigname,ids in [('Zunderlauf','Glumanda_Meshy_V11.blend','Glumanda_Meshy','Glumanda_Meshy_Rig',[7444,11754]),('Bisasam','Bisasam_Meshy_V1.blend','Bisasam_Body','Bisasam_Rig',[2433,10716])]:
 bpy.ops.wm.open_mainfile(filepath=str(R/'Art/Characters/Creatures'/species/'Source'/file));b=bpy.data.objects[bodyname];rig=bpy.data.objects[rigname];rows.append({'species':species,'bones':[{'name':x.name,'parent':x.parent.name if x.parent else None,'head':list(x.head_local)}for x in rig.data.bones],'vertices':[{'id':i,'rest':list(b.data.vertices[i].co),'groups':[(b.vertex_groups[g.group].name,g.weight)for g in b.data.vertices[i].groups]}for i in ids]})
(R/'Saved/StarterPolishV2/DeformationDiagnosis.json').write_text(json.dumps(rows,indent=2))
