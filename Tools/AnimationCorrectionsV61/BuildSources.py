"""Two guarded V6.1 skin/material-mask repairs. Original geometry, UVs and actions remain exact."""
import bpy,json,hashlib,numpy as np,sys,subprocess
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
for name in (['Player']if '--refine-player'in sys.argv else['Glurak']if '--refine-glurak'in sys.argv else['Player','Glurak']):
 A=R/('Art/Characters/YoungTrainer'if name=='Player'else'Art/Characters/Creatures/Glurak');source=A/'Source'/(('Player_Meshy'if name=='Player'else name)+'_AnimationCorrections_V6.blend');dest=source.with_name(source.stem+'1.blend');assert not dest.exists()or(any(f in sys.argv for f in ['--refine-player','--refine-glurak'])and not subprocess.check_output(['git','ls-files','--',str(dest.relative_to(R))],cwd=R).strip()),dest;before=sha(source)
 bpy.ops.wm.open_mainfile(filepath=str(source));bpy.context.preferences.filepaths.save_version=0;b=bpy.data.objects['Player_Meshy_Body'if name=='Player'else'Glurak_Body'];rig=bpy.data.objects['Player_Meshy_Rig'if name=='Player'else'Glurak_Rig'];coords=[tuple(v.co)for v in b.data.vertices];uvs=[tuple(v.uv)for v in b.data.uv_layers.active.data];topology=[tuple(p.vertices)for p in b.data.polygons];rest={x.name:[list(row)for row in x.matrix_local]for x in rig.data.bones};changed=[]
 im=next(n for n in b.data.materials[0].node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs['Base Color'].links[0].from_node.image;pix=np.array(im.pixels[:]).reshape(im.size[1],im.size[0],4);uvv=np.zeros((len(coords),2))
 for l in b.data.loops:uvv[l.vertex_index]=b.data.uv_layers.active.data[l.index].uv
 rgb=pix[(uvv[:,1]*(im.size[1]-1)).astype(int),(uvv[:,0]*(im.size[0]-1)).astype(int),:3]
 if name=='Player':
  # The old rear-plane assignment (y > .075) cut through the BROWN trousers.
  # Texture + anatomical bounds distinguish them from the GREEN cape, not a global plane cut.
  _,inv=np.unique(np.rint(np.array(coords)/.0001).astype(np.int64),axis=0,return_inverse=True);parent=list(range(int(inv.max())+1))
  def root(i):
   while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
   return i
  for poly in topology:
   first=root(int(inv[poly[0]]))
   for i in poly[1:]:parent[root(int(inv[i]))]=first
  components={}
  for i in range(len(coords)):components.setdefault(root(int(inv[i])),[]).append(i)
  # The median of an entire connected surface tolerates atlas-edge bleed at a vertex.
  # V6 cloak patches have median R/G around 1.06; the main trouser patch is 1.475.
  brown=set()
  for ids in components.values():
   if np.median(rgb[ids,0]/np.maximum(rgb[ids,1],.001))>1.23:brown.update(ids)
  for v in b.data.vertices:
   x,y,z=v.co;old={b.vertex_groups[q.group].name:q.weight for q in v.groups};cape=sum(q for k,q in old.items()if k.startswith('cape'))
   if not(cape>.01 and .17<z<.76 and abs(x)<.34 and v.index in brown):continue
   side='l'if x>=0 else'r'
   if z<.56:
    t=smooth(.26,.40,z);new={'shin_'+side:1-t,'thigh_'+side:t}
   else:
    t=smooth(.66,.79,z);new={'pelvis':1-t,'spine':t}
   for grp in b.vertex_groups:grp.remove([v.index])
   for k,q in new.items():
    if q>1e-5:b.vertex_groups[k].add([v.index],q,'REPLACE')
   changed.append(dict(vertex=v.index,rest=list(v.co),texture_rgb=rgb[v.index].tolist(),before=old,after=new))
  # Smooth the genuine shared trouser crotch instead of assigning adjacent vertices to opposite thighs.
  for v in b.data.vertices:
   x,y,z=v.co;old={b.vertex_groups[q.group].name:q.weight for q in v.groups}
   if not(abs(x)<.04 and .45<z<.60 and v.index in brown and sum(q for k,q in old.items()if k.startswith('thigh'))>.1):continue
   center=1-smooth(.02,.04,abs(x));pelvis=smooth(.47,.60,z)*center;left=smooth(-.04,.04,x);new={'pelvis':pelvis,'thigh_l':(1-pelvis)*left,'thigh_r':(1-pelvis)*(1-left)}
   for grp in b.vertex_groups:grp.remove([v.index])
   for k,q in new.items():
    if q>1e-5:b.vertex_groups[k].add([v.index],q,'REPLACE')
   changed.append(dict(vertex=v.index,rest=list(v.co),before=old,after=new,reason='continuous crotch blend'))
  assert 100<len(changed)<2500,len(changed)
 else:
  bv=BVHTree.FromPolygons([v.co for v in b.data.vertices],topology,all_triangles=True);attr=b.data.color_attributes['PolishV4']
  for p in b.data.polygons:
   c=sum((b.data.vertices[i].co for i in p.vertices),Vector())/len(p.vertices);r,g,blue=rgb[list(p.vertices)].mean(0)
   # Confirmed blue root membrane has zero wing weight; the V6 anatomical-weight filter omitted it.
   if not(p.material_index==0 and .10<abs(c.x)<.67 and .65<c.z<1.52 and -.02<c.y<.5 and g>r*1.5 and blue>r*1.5):continue
   rear=bv.ray_cast(Vector((c.x,2,c.z)),Vector((0,-1,0)),4)[2]==p.index;front=bv.ray_cast(Vector((c.x,-2,c.z)),Vector((0,1,0)),4)[2]==p.index
   if rear and not front and attr.data[p.loop_start].color[0]<.5:
    for i in p.loop_indices:attr.data[i].color=(1,0,1 if p.normal.y>0 else 0,1)
    changed.append(dict(face=p.index,center=list(c),rgb=[float(r),float(g),float(blue)]))
  # Final residual audit: 312 genuine exterior root faces remain near the body and
  # under the atlas-edge threshold. Keep actual front surfaces dark; no view-dependent shader.
  for p in b.data.polygons:
   c=sum((b.data.vertices[i].co for i in p.vertices),Vector())/len(p.vertices)
   if not(p.material_index==0 and .035<abs(c.x)<.67 and .65<c.z<1.52 and .02<c.y<.5 and p.normal.y>.05 and attr.data[p.loop_start].color[0]<.5):continue
   t=sum((b.data.uv_layers.active.data[i].uv for i in p.loop_indices),Vector((0,0)))/len(p.vertices);r,g,blue=pix[int(t.y*(im.size[1]-1)),int(t.x*(im.size[0]-1)),:3]
   if not(g>r*1.3 and blue>r*1.3):continue
   direction=Vector((0,-1,-.8)).normalized();top=bv.ray_cast(c-direction*3,direction,4)[2]==p.index;front=bv.ray_cast(Vector((c.x,-2,c.z)),Vector((0,1,0)),4)[2]==p.index
   if top and not front:
    for i in p.loop_indices:attr.data[i].color=(1,0,1,1)
    changed.append(dict(face=p.index,center=list(c),rgb=[float(r),float(g),float(blue)],reason='confirmed exterior root residual, front occluded, rear-top visible'))
  assert 500<len(changed)<8000,len(changed)
 assert coords==[tuple(v.co)for v in b.data.vertices]and uvs==[tuple(v.uv)for v in b.data.uv_layers.active.data]and topology==[tuple(p.vertices)for p in b.data.polygons]
 rig.animation_data.action=bpy.data.actions['A_Player_Idle_V6'if name=='Player'else'Glurak_Idle_V6'];s=bpy.context.scene;s.frame_set(1);s.frame_start=1;s.frame_end=int(rig.animation_data.action.frame_range[1]);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));assert sha(source)==before
 E=A/'Exports/AnimationV61';assert not E.exists()or(any(f in sys.argv for f in ['--refine-player','--refine-glurak'])and not subprocess.check_output(['git','ls-files','--',str(E.relative_to(R))],cwd=R).strip());E.mkdir(exist_ok=any(f in sys.argv for f in ['--refine-player','--refine-glurak']));p=E/(name+'_Idle.fbx');bpy.ops.object.select_all(action='DESELECT');b.hide_set(False);rig.hide_set(False);b.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig;kw=dict(use_selection=True,object_types={'ARMATURE','MESH'},global_scale=1,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE',path_mode='AUTO',colors_type='LINEAR')
 if name=='Player':kw.update(use_armature_deform_only=True,apply_scale_options='FBX_SCALE_UNITS')
 bpy.ops.export_scene.fbx(filepath=str(p),**kw)
 (A/'AnimationCorrectionsV61_Audit.json').write_text(json.dumps(dict(source=str(dest.relative_to(R)),source_sha256=sha(dest),previous=str(source.relative_to(R)),previous_sha256=before,export=str(p.relative_to(R)),export_sha256=sha(p),changes=changed,vertices=len(coords),triangles=sum(len(p)-2 for p in topology),geometry_uv_rest_and_animations_unchanged=True,rest=rest),indent=2));print(name,'REPAIRED',len(changed),flush=True)
