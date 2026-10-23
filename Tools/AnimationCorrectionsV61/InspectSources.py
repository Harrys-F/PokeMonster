"""Read-only diagnosis of V6 topology, skin envelopes and outer wing roots."""
import bpy,json,math,numpy as np
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2]; O=R/'Saved/AnimationCorrectionsV61'; rows={}
for name,source in [('Player','Art/Characters/YoungTrainer/Source/Player_Meshy_AnimationCorrections_V6.blend'),('Glurak','Art/Characters/Creatures/Glurak/Source/Glurak_AnimationCorrections_V6.blend')]:
 bpy.ops.wm.open_mainfile(filepath=str(R/source)); body=bpy.data.objects['Player_Meshy_Body'if name=='Player'else'Glurak_Body']; rig=bpy.data.objects['Player_Meshy_Rig'if name=='Player'else'Glurak_Rig']; co=np.array([tuple(v.co)for v in body.data.vertices]); groups={g.index:g.name for g in body.vertex_groups}; weights=[{groups[g.group]:g.weight for g in v.groups}for v in body.data.vertices]
 row=dict(source=source,vertices=len(co),polygons=len(body.data.polygons),materials=[m.name for m in body.data.materials],actions=[(a.name,list(a.frame_range))for a in bpy.data.actions]);rows[name]=row
 if name=='Player':
  # Face components after tolerance-controlled virtual seam welding (never mutate topology).
  row['components']=[]
  for tol in [.00001,.0001,.001,.003]:
   _,inv=np.unique(np.rint(co/tol).astype(np.int64),axis=0,return_inverse=True); parent=list(range(int(inv.max())+1))
   def root(i):
    while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
    return i
   for p in body.data.polygons:
    a=root(int(inv[p.vertices[0]]))
    for i in p.vertices[1:]:parent[root(int(inv[i]))]=a
   cc={}
   for i in range(len(co)):cc.setdefault(root(int(inv[i])),[]).append(i)
   largest=sorted(cc.values(),key=len,reverse=True)
   row['components'].append(dict(tolerance=tol,count=len(cc),largest=[dict(vertices=len(ids),bbox=[co[ids].min(0).tolist(),co[ids].max(0).tolist()])for ids in largest[:8]]))
  row['cape_vertices']=[dict(index=v.index,co=list(v.co),weights=weights[v.index])for v in body.data.vertices if any(k.startswith('cape')and value>.1 for k,value in weights[v.index].items())and v.co.z<.65]
 else:
  attr=body.data.color_attributes['PolishV4'];uv=body.data.uv_layers.active;im=next(n for n in body.data.materials[0].node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs['Base Color'].links[0].from_node.image;pix=np.array(im.pixels[:]).reshape(im.size[1],im.size[0],4)
  faces=[]
  for p in body.data.polygons:
   c=sum((body.data.vertices[i].co for i in p.vertices),Vector())/len(p.vertices)
   if .12<abs(c.x)<.65 and .7<c.z<1.55:
    t=sum((uv.data[i].uv for i in p.loop_indices),Vector((0,0)))/len(p.loop_indices);rgb=pix[int((t.y%1)*(im.size[1]-1)),int((t.x%1)*(im.size[0]-1)),:3];w=sum(sum(v for k,v in weights[i].items()if k.startswith('wing'))for i in p.vertices)/len(p.vertices)
    faces.append(dict(index=p.index,center=list(c),normal=list(p.normal),weight=w,rgb=rgb.tolist(),mask=list(attr.data[p.loop_start].color)))
  row['root_faces']=faces
 (O/(name+'Diagnosis.json')).write_text(json.dumps(row,indent=2))
 # Diagnostic renders only; never save the loaded source or change existing cameras/assets.
 s=bpy.context.scene
 for ob in s.objects:ob.hide_render=ob!=body and ob!=rig
 for ob in list(s.objects):
  if ob.type in ['LIGHT','CAMERA']:bpy.data.objects.remove(ob,do_unlink=True)
 s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=8;s.render.resolution_x=900;s.render.resolution_y=900;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.world.color=(.45,.45,.45)
 ld=bpy.data.lights.new('InspectionKey','AREA');lo=bpy.data.objects.new('InspectionKey',ld);s.collection.objects.link(lo);lo.location=(2,-3,4);ld.energy=350;ld.size=4
 cd=bpy.data.cameras.new('InspectionCamera');cam=bpy.data.objects.new('InspectionCamera',cd);s.collection.objects.link(cam);s.camera=cam;cd.type='ORTHO';cd.ortho_scale=1.8 if name=='Player'else 3.7
 poses=[('Idle',1),('Walk',9),('Run',8)]if name=='Player'else[('Idle',1)]
 for role,frame in poses:
  rig.animation_data.action=bpy.data.actions['A_Player_'+role+'_V6'if name=='Player'else'Glurak_'+role+'_V6'];s.frame_set(frame)
  for view,position in ([('Side',(3,0,.8)),('Rear',(0,3,.9))]if name=='Player'else[('Rear',(0,4,2.8)),('Front',(0,-4,2.8))]):
   cam.location=position;cam.rotation_euler=(Vector((0,0,.7 if name=='Player'else.85))-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(O/(name+role+view+'Diagnostic.png'));bpy.ops.render.render(write_still=True)
 print(name,'DIAGNOSED',flush=True)
(O/'SourceDiagnosis.json').write_text(json.dumps(rows,indent=2))
