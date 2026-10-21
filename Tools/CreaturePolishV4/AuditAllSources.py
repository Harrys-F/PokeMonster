"""Read-only frame audit of all ten actual current source variants; not a visual acceptance claim."""
import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/CreaturePolishV4';files={'Zunderlauf':'Zunderlauf/Source/Glumanda_Meshy_V11.blend','Schiggy':'Schiggy/Source/Schiggy_Surface_V2.blend','Bisasam':'Bisasam/Source/Bisasam_Meshy_PolishV2.blend'}
for n in ['Pikachu','Myrapla','Machomei','Gengar']:files[n]=n+'/Source/'+n+'_Meshy_V1.blend'
for n in ['Enton','Nebulak','Glurak']:files[n]=n+'/Source/'+n+'_PolishV4.blend'
rows={}
for name,relative in files.items():
 p=R/'Art/Characters/Creatures'/relative;digest=hashlib.sha256(p.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(p));rig=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE'and o.animation_data);body=next(o for o in bpy.context.scene.objects if o.type=='MESH'and any(m.type=='ARMATURE'and m.object==rig for m in o.modifiers));
 if name=='Zunderlauf':
  with bpy.data.libraries.load(str(R/'Art/Characters/Creatures/Zunderlauf/Source/Glumanda_Faint_PolishV2.blend'),link=False)as(fr,to):to.actions=['Glumanda_Faint_PolishV2']
 s=bpy.context.scene;row=dict(source=str(p.relative_to(R)),sha256=digest,bones=len(rig.data.bones),vertices=len(body.data.vertices),actions={})
 for a in bpy.data.actions:
  if name=='Zunderlauf' and a.name=='Glumanda_Faint':continue
  rig.animation_data.action=a;lo,hi=map(int,a.frame_range);zs=[];minimum=None
  for f in range(lo,hi+1):
   s.frame_set(f);ob=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ob.to_mesh();v=min(m.vertices,key=lambda v:v.co.z);zs.append(v.co.z)
   if minimum is None or v.co.z<minimum['z_cm']/100:
    orig=body.data.vertices[v.index];minimum=dict(frame=f,index=v.index,z_cm=v.co.z*100,rest=list(orig.co),weights={body.vertex_groups[g.group].name:g.weight for g in orig.groups})
   ob.to_mesh_clear()
  row['actions'][a.name]=dict(frames=hi-lo+1,minimum=minimum,max_min_z_cm=max(zs)*100)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==digest;rows[name]=row;print('SOURCE_FRAME_AUDIT',name,len(row['actions']),flush=True)
(O/'AllSourceFrames.json').write_text(json.dumps(rows,indent=2))
