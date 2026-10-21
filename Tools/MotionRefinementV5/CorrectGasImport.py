"""Correct only our separate V5 gas export binding, never original assets."""
import unreal,json,subprocess
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();assert not subprocess.check_output(['git','ls-files','--','Content/Characters/Creatures/Nebulak/MotionV5'],cwd=R).strip(),'One-time candidate repair must not overwrite released assets';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not E.get_game_world()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
P='/Game/Characters/Creatures/Nebulak/MotionV5';gas=unreal.load_asset(P+'/SM_Nebulak_GasEnvelope');profile=unreal.load_asset(P+'/DA_Nebulak_Presentation');material=unreal.load_asset(P+'/M_Nebulak_GasEnvelope')
old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0')
try:
 ui=unreal.FbxImportUI()
 for k,v in dict(import_mesh=True,import_as_skeletal=False,import_animations=False,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH).items():ui.set_editor_property(k,v)
 for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,combine_meshes=True,auto_generate_collision=False,vertex_color_import_option=unreal.VertexColorImportOption.REPLACE).items():ui.static_mesh_import_data.set_editor_property(k,v)
 task=unreal.AssetImportTask()
 for k,v in dict(filename=str(R/'Art/Characters/Creatures/Nebulak/Exports/MotionV5/Nebulak_GasEnvelope.fbx'),destination_path=P,destination_name='SM_Nebulak_GasEnvelope',automated=True,save=False,replace_existing=True,options=ui).items():task.set_editor_property(k,v)
 unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task]);gas=unreal.load_asset(P+'/SM_Nebulak_GasEnvelope');gas.set_material(0,material)
 ref=unreal.PokeMonsterCreaturePolishLibrary.get_reference_bone_transform(profile.mesh,'head');inverse=ref.inverse();effects=list(profile.effect_anchors)
 for effect in effects:
  if str(effect.id)=='GasEnvelope':effect.set_editor_property('offset',inverse)
 profile.set_editor_property('effect_anchors',effects)
 for a in [gas,profile]:assert unreal.EditorAssetLibrary.save_loaded_asset(a,False)
 (R/'Saved/MotionRefinementV5/GasBinding.json').write_text(json.dumps(dict(reference=str(ref),inverse=str(inverse),mesh=str(gas.get_bounds()),effects=[str(x)for x in effects]),indent=2))
finally:unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX '+str(old))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
