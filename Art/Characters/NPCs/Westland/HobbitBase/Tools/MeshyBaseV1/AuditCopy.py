import bpy,bmesh,json,math,hashlib,struct
from pathlib import Path
from collections import Counter
from mathutils import Vector
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_MeshyBase_V1'];bpy.context.window.scene=s;mesh=s.objects['HNM1_Body'];rig=s.objects['HNM1_Rig'];me=mesh.data
with bpy.data.libraries.load(str(B.parents[2]/'YoungTrainer/Source/Player_Meshy_Sprint_V1.blend'),link=False) as (a,b):
 b.objects=['Player_Meshy_Body','Player_Meshy_Rig']
oldmesh,oldrig=b.objects
# The comparison objects stay unlinked and this process never saves the source.
def hash_mesh(o):
 h=hashlib.sha256()
 for v in o.data.vertices:h.update(struct.pack('3f',*v.co));h.update(repr([(g.group,g.weight) for g in v.groups]).encode())
 for p in o.data.polygons:h.update(repr(tuple(p.vertices)).encode())
 for uv in o.data.uv_layers:
  for c in uv.data:h.update(struct.pack('2f',*c.uv))
 return h.hexdigest()
geom_equal=hash_mesh(mesh)==hash_mesh(oldmesh)
def bone_signature(o):return [(b.name,b.parent.name if b.parent else None,list(b.head_local),list(b.tail_local),b.use_deform) for b in o.data.bones]
bones_equal=bone_signature(rig)==bone_signature(oldrig)
me.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(me);bm.verts.ensure_lookup_table();parts=[];visited=set()
for v in bm.verts:
 if v.index in visited:continue
 todo=[v];visited.add(v.index);count=0
 while todo:
  q=todo.pop();count+=1
  for e in q.link_edges:
   other=e.other_vert(q)
   if other.index not in visited:visited.add(other.index);todo.append(other)
 parts.append(count)
weights=[sum(g.weight for g in v.groups) for v in me.vertices];influences=[sum(g.weight>1e-6 for g in v.groups) for v in me.vertices]
# Evaluate actual deformed geometry at every saved clip frame; no Unreal springs are present here.
pose_enum=next(i.identifier for i in bpy.types.Armature.bl_rna.properties['pose_position'].enum_items if i.identifier=='POSE');rig.data.pose_position=pose_enum
ids={side:[v.index for v in me.vertices if v.co.z<.085 and ((v.co.x>0)==(side=='left'))] for side in ['left','right']};clips=[]
for aname in ['HNM1_Idle_V2','HNM1_Walk_V2','HNM1_Run_V1']:
 act=bpy.data.actions[aname];rig.animation_data.action=act
 if len(act.slots):rig.animation_data.action_slot=act.slots[0]
 curves=[c for layer in act.layers for strip in layer.strips for bag in strip.channelbags for c in bag.fcurves]
 badpaths=[c.data_path for c in curves if c.data_path.startswith('pose.bones[') and c.data_path.split('"')[1] not in rig.pose.bones]
 rows=[]
 for frame in range(int(act.frame_range[0]),int(act.frame_range[1])+1):
  s.frame_set(frame);bpy.context.view_layer.update();evaluated=mesh.evaluated_get(bpy.context.evaluated_depsgraph_get());dm=evaluated.to_mesh()
  rows.append({'frame':frame,'sole_min_m':{side:min((evaluated.matrix_world@dm.vertices[i].co).z for i in ix) for side,ix in ids.items()},'root_translation_m':list(rig.pose.bones['root'].matrix.translation),'finite_vertices':all(all(math.isfinite(x) for x in v.co) for v in dm.vertices)})
  evaluated.to_mesh_clear()
 clips.append({'name':aname,'frame_range':list(act.frame_range),'seconds_at_60fps':(act.frame_range[1]-act.frame_range[0])/60,'curves':len(curves),'invalid_bone_paths':badpaths,'samples':rows,'min_sole_m':min(v for row in rows for v in row['sole_min_m'].values()),'root_max_translation_m':max(Vector(row['root_translation_m']).length for row in rows)})
images=[n.image for n in me.materials[0].node_tree.nodes if n.type=='TEX_IMAGE' and n.image]
result={'source':bpy.data.filepath,'mesh_geometry_weights_uv_equal_to_source':geom_equal,'rig_equal_to_source':bones_equal,'height_m':max(v.co.z for v in me.vertices)-min(v.co.z for v in me.vertices),'minimum_z':min(v.co.z for v in me.vertices),'mesh_objects':1,'vertices':len(me.vertices),'faces':len(me.polygons),'triangles':len(me.loop_triangles),'face_types':dict(Counter(len(p.vertices) for p in me.polygons)),'material_slots':len(me.materials),'uv_layers':[u.name for u in me.uv_layers],'connected_components':len(parts),'largest_components':sorted(parts,reverse=True)[:12],'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'boundary_edges':sum(e.is_boundary for e in bm.edges),'loose_vertices':sum(not v.link_faces for v in bm.verts),'degenerate_faces':sum(f.calc_area()<1e-12 for f in bm.faces),'unweighted_vertices':sum(w<1e-6 for w in weights),'weight_sum_max_error':max(abs(w-1) for w in weights),'max_weight_influences':max(influences),'bones':bone_signature(rig),'bone_count':len(rig.data.bones),'clips':clips,'textures':[{'name':i.name,'size':list(i.size),'packed':bool(i.packed_file),'filepath':i.filepath,'colorspace':i.colorspace_settings.name} for i in images],'externally_linked_model_data':[d.name for d in [mesh,mesh.data,rig,rig.data,*me.materials,*images] if d.library],'armature_modifier_targets_copy':all(m.object==rig for m in mesh.modifiers if m.type=='ARMATURE'),'deformation_limit':'Full clip-frame sole and finite-coordinate tests, selected rendered pose reviews. No complete self-intersection or terrain/contact/retarget tests.'}
bm.free();(B/'Review/MeshyBaseV1/ReopenAudit.json').write_text(json.dumps(result,indent=2));print({k:v for k,v in result.items() if k not in ['clips','bones','textures']});print('Clip summaries',[(a['name'],a['seconds_at_60fps'],a['min_sole_m']) for a in clips]);assert geom_equal and bones_equal;assert not result['externally_linked_model_data'];assert result['armature_modifier_targets_copy'];assert all(i.packed_file for i in images)
