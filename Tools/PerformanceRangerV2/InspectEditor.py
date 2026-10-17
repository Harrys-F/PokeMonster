import unreal,json
from pathlib import Path
P=Path(unreal.Paths.project_dir()).resolve()/'Art/Characters/NPCs/Ranger/Review/V2';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);out={'map':e.get_editor_world().get_path_name(),'dirty_maps':[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'skeletal_lod_api':{},'console':{}}
for cls in ['SkeletalMeshEditorSubsystem','EditorSkeletalMeshLibrary']:
 if hasattr(unreal,cls):
  c=getattr(unreal,cls);out['skeletal_lod_api'][cls]={n:getattr(c,n).__doc__ for n in dir(c) if any(t in n for t in ['import_lod','lod_count','lod_info','lod_build','lod_screen','triangles','vertices','lod_settings'])}
(P/'EditorAPI.json').write_text(json.dumps(out,indent=2))
