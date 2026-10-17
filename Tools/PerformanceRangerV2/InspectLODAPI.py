import unreal,json
from pathlib import Path
S=unreal.get_editor_subsystem(unreal.SkeletalMeshEditorSubsystem);m=unreal.load_asset('/Game/Characters/NPCs/RangerV2/Meshes/SK_Ranger_NPC_V2');out={'mesh_lod_members':{n:str(getattr(m,n).__doc__) for n in dir(m) if 'lod' in n},'subsystem_lod_members':{n:str(getattr(S,n).__doc__) for n in dir(S) if 'lod' in n},'lod_count':S.get_lod_count(m)};Path(unreal.Paths.project_dir(),'Art/Characters/NPCs/Ranger/Review/V2/LODAPI.json').write_text(json.dumps(out,indent=2))
