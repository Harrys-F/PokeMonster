"""Preserve the original armature wrapper names for direct animation import into existing skeletons."""
import bpy,json
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster');rows=[]
for a in json.loads((R/'Tools/NPCExpansion/Library.json').read_text()):
 if not a.get('reuse_mesh'):continue
 C=R/'Art/Characters/NPCs'/a['id'];p=C/'Source'/(a['id']+'_NPCLibrary.blend');bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False);bpy.context.preferences.filepaths.save_version=0;rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');old=rig.name;rig.name=a['rig'];bpy.ops.wm.save_as_mainfile(filepath=str(p),compress=True);rows.append({'id':a['id'],'old_wrapper':old,'original_wrapper':rig.name,'reason':'Reuse the pre-existing matching mesh/skeleton; deforming bones, topology, UVs, weights and curves unchanged.'})
(R/'Saved/ProjectRefinement/NPCExpansion/ReusedRigs.json').write_text(json.dumps(rows,indent=2))
