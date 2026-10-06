"""Read-only Blender character audit with temporary FK deformation probes."""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer');OUT=ROOT.parents[2]/'Saved/YoungTrainerV1';OUT.mkdir(parents=True,exist_ok=True)
scene=bpy.data.scenes['YoungTrainer_Reference_V1']
if bpy.context.window:bpy.context.window.scene=scene
arm=bpy.data.objects['YT_Rig'];obs=[o for o in bpy.data.collections['YT_Character'].objects if o.type=='MESH'];deform={b.name for b in arm.data.bones if b.use_deform}
rows=[];errors=[]
for o in obs:
 bm=bmesh.new();bm.from_mesh(o.data)
 loose=sum(not v.link_faces for v in bm.verts);badarea=sum(f.calc_area()<1e-12 for f in bm.faces);bound=sum(e.is_boundary for e in bm.edges);nonman=sum(not e.is_manifold and not e.is_boundary for e in bm.edges)
 uv=o.data.uv_layers.active;invalid_uv=sum(not all(math.isfinite(x) and 0<=x<=1 for x in d.uv) for d in uv.data) if uv else len(o.data.loops)
 badweights=[];maxweights=0
 for v in o.data.vertices:
  w=[g.weight for g in v.groups if o.vertex_groups[g.group].name in deform];maxweights=max(maxweights,len(w))
  if abs(sum(w)-1)>1e-5 or len(w)>4:badweights.append(v.index)
 row={'object':o.name,'vertices':len(o.data.vertices),'triangles':sum(len(p.vertices)-2 for p in o.data.polygons),'quads':sum(len(p.vertices)==4 for p in o.data.polygons),'loose_vertices':loose,'zero_area_faces':badarea,'boundary_edges':bound,'nonmanifold_edges':nonman,'invalid_uv_loops':invalid_uv,'bad_weight_vertices':len(badweights),'max_weights':maxweights,'materials':len(o.data.materials),'scale':list(o.scale),'rotation':list(o.rotation_euler)};rows.append(row);bm.free()
 if loose or badarea or invalid_uv or badweights or nonman or bound:errors.append(row)
 assert all(abs(v-1)<1e-6 for v in o.scale) and sum(abs(x) for x in o.rotation_euler)<1e-6
coords=[o.matrix_world@v.co for o in obs for v in o.data.vertices];bounds={'min':[min(v[i] for v in coords) for i in range(3)],'max':[max(v[i] for v in coords) for i in range(3)]}
assert abs(bounds['min'][2])<1e-6 and abs(bounds['max'][2]-1.4)<1e-6
assert len(obs)==20 and len(arm.data.bones)==32
for o in [bpy.data.objects['YT_CharacterRoot'],arm]:
 assert sum(abs(x) for x in o.location)+sum(abs(x) for x in o.rotation_euler)<1e-6 and all(abs(x-1)<1e-6 for x in o.scale)
assert all(b.matrix_basis==b.matrix_basis.__class__.Identity(4) for b in arm.pose.bones)
def tree(o):
 dg=bpy.context.evaluated_depsgraph_get();e=o.evaluated_get(dg);m=e.to_mesh();vs=[e.matrix_world@v.co for v in m.vertices];faces=[tuple(p.vertices) for p in m.polygons];t=BVHTree.FromPolygons(vs,faces);e.to_mesh_clear();return t
probes=[];saved=[(b,b.rotation_mode,b.matrix_basis.copy()) for b in arm.pose.bones]
try:
 for name,rotations in [('Rest',{}),('Stride',{'upperarm.L':(20,0,0),'upperarm.R':(-20,0,0),'thigh.L':(14,0,0),'thigh.R':(-14,0,0),'shin.R':(-16,0,0)}),('Interact',{'upperarm.L':(-18,0,0),'forearm.L':(-35,0,0),'head':(0,20,0)}),('RunProbe',{'upperarm.L':(35,0,0),'upperarm.R':(-35,0,0),'forearm.L':(-40,0,0),'forearm.R':(-40,0,0),'thigh.L':(25,0,0),'thigh.R':(-25,0,0),'shin.R':(-45,0,0)})]:
  for b in arm.pose.bones:b.rotation_mode='XYZ';b.rotation_euler=(0,0,0)
  for n,r in rotations.items():arm.pose.bones[n].rotation_euler=[math.radians(v) for v in r]
  bpy.context.view_layer.update()
  backpack=tree(bpy.data.objects['YT_Backpack']);hands=tree(bpy.data.objects['YT_Hands']);body=tree(bpy.data.objects['YT_Body'])
  overlap={'hands_backpack':len(hands.overlap(backpack)),'skin_backpack':len(body.overlap(backpack))}
  probes.append({'pose':name,'bone_rotations_degrees':rotations,'overlap_face_pairs':overlap})
finally:
 for b,mode,basis in saved:b.rotation_mode=mode;b.matrix_basis=basis
 bpy.context.view_layer.update()
originals={n:{'location':list(bpy.data.objects[n].location),'scale':list(bpy.data.objects[n].scale),'rotation':list(bpy.data.objects[n].rotation_euler)} for n in ['Cube','Camera','Light']}
record={'file':bpy.data.filepath,'height_m':1.4,'bounds_m':bounds,'mesh_count':len(obs),'bone_count':len(arm.data.bones),'triangles':sum(r['triangles'] for r in rows),'objects':rows,'errors':errors,'fk_probes':probes,'original_scene_objects':originals,'textures':[{'name':i.name,'size':list(i.size),'packed':bool(i.packed_file)} for i in bpy.data.images if i.name.startswith('YT_')],'limitations':['Temporary FK poses do not replace a full animation suite.','Palette tile UVs are intentionally shared; no unique painted body bake.','No facial blendshapes/IK/Unreal import test in this Blender-only task.']}
record['vertices']=sum(r['vertices'] for r in rows);record['quads']=sum(r['quads'] for r in rows)
record['linear_skinning']=all(not m.use_deform_preserve_volume for o in obs for m in o.modifiers if m.type=='ARMATURE')
record['passed']=not errors and all(not any(p['overlap_face_pairs'].values()) for p in probes) and record['linear_skinning']
(OUT/'Audit.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({k:v for k,v in record.items() if k not in ['objects','original_scene_objects']},indent=2))
assert record['passed'], 'Inspect audit; final mesh/probe checks failed.'
