import unreal,json
from pathlib import Path
P=Path(unreal.Paths.project_dir(),'Art/Characters/NPCs/Ranger/Review/V2');e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);unreal.SystemLibrary.execute_console_command(e.get_editor_world(),'pm.Perf.AuditLODs FixV2');m=unreal.load_asset('/Game/Characters/NPCs/RangerV2/Meshes/SK_Ranger_NPC_V2');unreal.EditorAssetLibrary.save_loaded_asset(m,False);(P/'FinalRegistry.json').write_text(json.dumps({str(k):str(v) for k,v in unreal.EditorAssetLibrary.get_tag_values(m.get_path_name()).items()},indent=2))
