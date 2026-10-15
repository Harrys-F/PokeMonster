import bpy,bmesh,json
from pathlib import Path
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_MeshyBase_V1'];bpy.context.window.scene=s;ob=s.objects['HNM1_Body'];rig=s.objects['HNM1_Rig']
# Analysis only: weld a disposable BMesh to distinguish split seams from disconnected shape.
bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bm.verts.ensure_lookup_table();visited=set();parts=[]
for v in bm.verts:
 if v.index in visited:continue
 todo=[v];visited.add(v.index);n=0
 while todo:
  q=todo.pop();n+=1
  for e in q.link_edges:
   w=e.other_vert(q)
   if w.index not in visited:visited.add(w.index);todo.append(w)
 parts.append(n)
welded={'tolerance_m':1e-6,'vertices':len(bm.verts),'components':len(parts),'largest_components':sorted(parts,reverse=True)[:10],'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'saved_to_mesh':False};bm.free()
rows=[]
for height in [1.20,1.32,1.45]:
 factor=height/1.4;rig.scale=(factor,)*3
 rig.data.pose_position=next(i.identifier for i in bpy.types.Armature.bl_rna.properties['pose_position'].enum_items if i.identifier=='REST');bpy.context.view_layer.update()
 dg=bpy.context.evaluated_depsgraph_get();e=ob.evaluated_get(dg);m=e.to_mesh();points=[e.matrix_world@v.co for v in m.vertices];row={'target_m':height,'temporary_scale':factor,'reference_height_m':max(v.z for v in points)-min(v.z for v in points),'reference_sole_z':min(v.z for v in points)};e.to_mesh_clear()
 rows.append(row)
with bpy.data.libraries.load(str(B.parents[2]/'YoungTrainer/Source/Player_Meshy_AnimationQuality_V2.blend'),link=False) as (a,b):b.objects=['Player_Meshy_Body','Player_Meshy_Rig']
a=ob.data;c=b.objects[0].data
same=len(a.vertices)==len(c.vertices) and all(v.co==w.co and [(g.group,g.weight) for g in v.groups]==[(g.group,g.weight) for g in w.groups] for v,w in zip(a.vertices,c.vertices))
result={'analysis_did_not_save_source':True,'welded_analysis':welded,'temporary_uniform_scale_checks':rows,'V2_mesh_positions_and_weights_equal_to_NPC_copy':same,'skeletal_hierarchy_V2_matches':[(b.name,b.parent.name if b.parent else None) for b in rig.data.bones]==[(b.name,b.parent.name if b.parent else None) for b in b.objects[1].data.bones],'nonuniform_proportion_retarget_tested':False}
(B/'Review/MeshyBaseV1/VariantAudit.json').write_text(json.dumps(result,indent=2));print(result)
