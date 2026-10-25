"""Read-only reopen of the prepared runtime library; no source saving."""
import bpy,json,numpy as np
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster');rows=[]
for a in json.loads((R/'Tools/NPCExpansion/Library.json').read_text()):
 C=R/'Art/Characters/NPCs'/a['id'] if a['id']!='HobbitBase' else R/'Art/Characters/NPCs/Westland/HobbitBase';p=C/'Source'/(a['id']+'_NPCLibrary.blend');bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False);meshes=[o for o in bpy.data.objects if o.type=='MESH'];rigs=[o for o in bpy.data.objects if o.type=='ARMATURE'];assert len(meshes)==len(rigs)==1;mesh=meshes[0];rig=rigs[0];expected=['Idle','Talk','Greet','TurnLeft','TurnRight']+(['Walk'] if a['walk']>0 else [])+(['Run'] if a['run']>0 else [])
 assert all(bpy.data.actions.get('A_'+a['id']+'_'+k+'_Library') for k in expected)
 deforming={b.name for b in rig.data.bones if b.use_deform};sums=[sum(g.weight for g in v.groups if mesh.vertex_groups[g.group].name in deforming) for v in mesh.data.vertices];assert min(sums)>.999 and max(sums)<1.001,(a['id'],min(sums),max(sums));used=set()
 for m in mesh.data.materials:
  if m and m.use_nodes:
   for n in m.node_tree.nodes:
    if n.type=='TEX_IMAGE' and n.image:used.add(n.image)
 assert len(used)>=3 and all(i.packed_file for i in used)
 rows.append({'id':a['id'],'reopened':True,'mesh_count':len(meshes),'bones':len(rig.data.bones),'active_clip_roles':expected,'vertices':len(mesh.data.vertices),'weight_sum_min':min(sums),'weight_sum_max':max(sums),'packed_material_textures':len(used)})
(R/'Saved/ProjectRefinement/NPCExpansion/SourceReopen.json').write_text(json.dumps(rows,indent=2));print('ALL_NPC_LIBRARY_SOURCES_REOPENED',len(rows),flush=True)
