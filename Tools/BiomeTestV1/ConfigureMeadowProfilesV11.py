"""Only new V1.1 profiles: existing float layer for insects, exact-skeleton hover roles for Habitak."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
# An explicitly recognized own new draft failed the Floating-family validator; restore only that option.
dirty=list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages())
if dirty:
 assert [p.get_path_name()for p in dirty]==['/Game/Characters/Creatures/Smettbo/MeshyV1/DA_Smettbo_Presentation']
 draft=unreal.load_asset('/Game/Characters/Creatures/Smettbo/MeshyV1/DA_Smettbo_Presentation');assert list(draft.get_validation_errors())==['Overworld float requires a floating rig and a finite amplitude of 0..10 cm'];assert draft.get_editor_property('overworld_float_amplitude_cm')==2.
 draft.set_editor_property('overworld_float_amplitude_cm',0.);assert not draft.get_validation_errors();assert unreal.EditorAssetLibrary.save_loaded_asset(draft,False)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
O=R/'Saved/BiomeTestV11/MeadowProfiles.json';assert not O.exists();baseline=json.loads((R/'Saved/BiomeTestV11/Before.json').read_text())['hashes'];rows=[]
for name in ['Smettbo','Bibor','Habitak']:
 P='/Game/Characters/Creatures/'+name+'/MeshyV1';p=unreal.load_asset(P+'/DA_'+name+'_Presentation');assert p and not p.get_validation_errors();assert 'Content/Characters/Creatures/'+name+'/MeshyV1/DA_'+name+'_Presentation.uasset'not in baseline
 if name!='Habitak':p.set_editor_property('overworld_float_amplitude_cm',0.);rows.append({'species':name,'float_option':False,'motion':'Own animated wing/body clips; no Floating-only profile override'})
 else:
  unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0');clips={};sk=p.mesh.skeleton
  for role in ['Takeoff','Hover','Land']:
   dest=P+'/Animations/A_Habitak_'+role;assert not unreal.EditorAssetLibrary.does_asset_exist(dest);ui=unreal.FbxImportUI()
   for k,v in dict(import_mesh=False,import_as_skeletal=True,import_animations=True,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_ANIMATION,skeleton=sk,override_full_name=True).items():ui.set_editor_property(k,v)
   for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,import_uniform_scale=1.,use_default_sample_rate=False,custom_sample_rate=30,animation_length=unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME).items():ui.anim_sequence_import_data.set_editor_property(k,v)
   t=unreal.AssetImportTask()
   for k,v in dict(filename=str(R/'Art/Characters/Creatures/Habitak/Exports/MeshyV1'/('Habitak_'+role+'.fbx')),destination_path=P+'/Animations',destination_name='A_Habitak_'+role,automated=True,save=False,replace_existing=False,options=ui).items():t.set_editor_property(k,v)
   unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t]);clip=next(x for x in t.get_objects()if isinstance(x,unreal.AnimSequence))
   if clip.get_path_name().split('.')[0]!=dest:assert not unreal.EditorAssetLibrary.does_asset_exist(dest);assert unreal.EditorAssetLibrary.rename_asset(clip.get_path_name().split('.')[0],dest);clip=unreal.load_asset(dest)
   clip.set_editor_property('enable_root_motion',False);assert clip.get_editor_property('skeleton')==sk;assert unreal.EditorAssetLibrary.save_loaded_asset(clip,False);clips[role]=clip
  for k,v in dict(takeoff_clip=clips['Takeoff'],hover_clip=clips['Hover'],land_clip=clips['Land'],hover_height_cm=135.,bAllowGroundHover=True).items():p.set_editor_property(k,v)
  rows.append({'species':name,'hover_height_cm':135,'clips':{n:c.get_path_name()for n,c in clips.items()}})
 assert not p.get_validation_errors();assert unreal.EditorAssetLibrary.save_loaded_asset(p,False)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();O.write_text(json.dumps(rows,indent=2))
