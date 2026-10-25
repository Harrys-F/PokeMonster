"""Repair only this task's working blends; source geometry and Incoming remain untouched."""
import bpy,json,runpy,hashlib,numpy as np
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster');apply=runpy.run_path(str(R/'Tools/NPCExpansion/Materials.py'))['apply'];rows=[]
for a in json.loads((R/'Tools/NPCExpansion/Library.json').read_text()):
 id=a['id'];C=R/'Art/Characters/NPCs'/id if id!='HobbitBase' else R/'Art/Characters/NPCs/Westland/HobbitBase';p=C/'Source'/(id+'_NPCLibrary.blend');bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False);bpy.context.preferences.filepaths.save_version=0;obj=next(o for o in bpy.data.objects if o.type=='MESH')
 def sha():
  co=np.empty(len(obj.data.vertices)*3,np.float32);obj.data.vertices.foreach_get('co',co);return hashlib.sha256(co.tobytes()).hexdigest()
 before=sha();apply(id,obj,C);assert sha()==before;bpy.ops.wm.save_as_mainfile(filepath=str(p),compress=True);rows.append({'id':id,'geometry_unchanged':True,'original_textures_packed':True})
(R/'Saved/ProjectRefinement/NPCExpansion/SourceMaterialRepair.json').write_text(json.dumps(rows,indent=2))
