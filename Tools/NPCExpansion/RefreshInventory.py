import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/NPCExpansion';rows=[]
for a in json.loads((R/'Tools/NPCExpansion/Library.json').read_text()):
 id=a['id'];p=unreal.load_asset('/Game/Characters/NPCs/Library/Profiles/DA_NPC_'+id);assert not list(p.get_validation_errors());rows.append({'id':id,'profile':p.get_path_name(),'mesh':p.mesh.get_path_name(),'skeleton':p.mesh.skeleton.get_path_name(),'materials':[m.get_path_name()for m in p.materials],'clips':{role:getattr(p,prop).get_path_name() if getattr(p,prop)else None for role,prop in [('Idle','idle'),('Walk','walk'),('Run','run'),('Talk','talk'),('Greet','greeting'),('TurnLeft','turn_left'),('TurnRight','turn_right')]},'height_cm':p.reference_height_cm,'limits':str(p.limitations)})
(O/'FinalProfiles.json').write_text(json.dumps(rows,indent=2))
