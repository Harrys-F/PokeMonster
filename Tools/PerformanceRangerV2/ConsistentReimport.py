import unreal,json
from pathlib import Path
P=Path(unreal.Paths.project_dir(),'Art/Characters/NPCs/Ranger/Review/V2');e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();m=unreal.load_asset('/Game/Characters/NPCs/RangerV2/Meshes/SK_Ranger_NPC_V2_Clean');old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(w,'Interchange.FeatureFlags.Import.FBX 0')
try:
 assert unreal.get_editor_subsystem(unreal.SkeletalMeshEditorSubsystem).reimport_all_custom_lods(m);unreal.EditorAssetLibrary.save_loaded_asset(m,False)
finally:unreal.SystemLibrary.execute_console_command(w,'Interchange.FeatureFlags.Import.FBX '+str(old))
(P/'ConsistentReimport.json').write_text(json.dumps({'reimport_all_custom_lods':True,'importer':'Legacy FBX (same as first import)','restored_interchange_flag':old},indent=2))
