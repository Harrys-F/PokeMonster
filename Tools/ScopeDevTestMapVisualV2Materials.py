"""Scope instancing-capable kit material variants to the new cottage only."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/DevTestMapVisualV2';D='/Game/Environment/DevTestMapVisualV2/Materials';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2' and not E.get_game_world();A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);variants={};uses=[]
for a in A.get_all_level_actors():
 if not a.get_actor_label().startswith('V2_Cottage_'):continue
 for c in a.get_components_by_class(unreal.HierarchicalInstancedStaticMeshComponent):
  for i in range(c.get_num_materials()):
   m=c.get_material(i)
   if not m or not m.get_path_name().startswith('/Game/Environment/Architecture/Westland/Materials/'):continue
   key=m.get_name();path=D+'/M_V2_'+key.removeprefix('M_')+'_Instanced'
   if key not in variants:
    n=unreal.load_asset(path) or unreal.EditorAssetLibrary.duplicate_asset(m.get_path_name().split('.')[0],path);assert n;n.set_editor_property('used_with_instanced_static_meshes',True);unreal.MaterialEditingLibrary.recompile_material(n);assert unreal.EditorAssetLibrary.save_loaded_asset(n,False);variants[key]=n
   c.set_material(i,variants[key]);uses.append([a.get_actor_label(),i,variants[key].get_path_name()])
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2')
packages=[p for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages() if p.get_path_name().startswith('/Game/Environment/Architecture/Westland/Materials/')]
if packages:result,error=unreal.EditorLoadingAndSavingUtils.reload_packages(packages,unreal.ReloadPackagesInteractionMode.ASSUME_POSITIVE);assert result,str(error)
(O/'InstancingMaterialFix.json').write_text(json.dumps({'variants':{k:m.get_path_name() for k,m in variants.items()},'uses':uses,'shared_materials_not_saved':True},indent=2));unreal.SystemLibrary.execute_console_command(w,'MAP CHECK')
