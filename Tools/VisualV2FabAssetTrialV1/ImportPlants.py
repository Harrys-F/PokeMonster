"""Local-only imports from the user's downloaded Fab cache, no source changes."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2FabAssetTrialV1';V=Path('/Users/Shared/UnrealEngine/Launcher/VaultCache/FabLibrary');ML=unreal.MaterialEditingLibrary;AT=unreal.AssetToolsHelpers.get_asset_tools();W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();ROOT='/Game/Environment/VisualV2FabAssetTrialV1';local='/Game/Fab/VisualV2TrialLocal';rows=[];old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX 0')
try:
 for key,folder in [('Poppy','Field_Poppy-66cb2706'),('Fern','Lady_Fern-3eead001')]:
  paths=list((V/folder).rglob('*'));tex={}
  for suffix in ['BaseColor','Normal','Opacity']:
   src=next(p for p in paths if p.name.endswith('_2K_'+suffix+'.jpg'));t=unreal.AssetImportTask();t.filename=str(src);t.destination_path=local+'/Plants';t.destination_name='T_FAT_'+key+'_'+suffix;t.automated=True;t.save=False;t.replace_existing=False;AT.import_asset_tasks([t]) if not unreal.EditorAssetLibrary.does_asset_exist(t.destination_path+'/'+t.destination_name) else None;a=unreal.load_asset(t.destination_path+'/'+t.destination_name);assert a
   if suffix=='Opacity':a.set_editor_property('srgb',False);a.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS)
   assert unreal.EditorAssetLibrary.save_loaded_asset(a,False);tex[suffix]=a
  name='M_FAT_'+key;m=unreal.load_asset(ROOT+'/Materials/'+name)if unreal.EditorAssetLibrary.does_asset_exist(ROOT+'/Materials/'+name)else AT.create_asset(name,ROOT+'/Materials',unreal.Material,unreal.MaterialFactoryNew());ML.delete_all_material_expressions(m);m.set_editor_property('blend_mode',unreal.BlendMode.BLEND_MASKED);m.set_editor_property('two_sided',True);m.set_editor_property('used_with_instanced_static_meshes',True);m.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_TWO_SIDED_FOLIAGE)
  for suffix,prop in [('BaseColor',unreal.MaterialProperty.MP_BASE_COLOR),('Normal',unreal.MaterialProperty.MP_NORMAL),('Opacity',unreal.MaterialProperty.MP_OPACITY_MASK)]:
   n=ML.create_material_expression(m,unreal.MaterialExpressionTextureSample);n.set_editor_property('texture',tex[suffix]);n.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL if suffix=='Normal'else unreal.MaterialSamplerType.SAMPLERTYPE_MASKS if suffix=='Opacity'else unreal.MaterialSamplerType.SAMPLERTYPE_COLOR);assert ML.connect_material_property(n,'R'if suffix=='Opacity'else'RGB',prop)
   if suffix=='BaseColor':assert ML.connect_material_property(n,'RGB',unreal.MaterialProperty.MP_SUBSURFACE_COLOR)
  rough=ML.create_material_expression(m,unreal.MaterialExpressionConstant);rough.r=.8;ML.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS);ML.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
  for var in ['A','B']:
   src=next(p for p in paths if p.name.endswith('_Var'+var+'_LOD1.fbx'));name='SM_FAT_'+key+var;ui=unreal.FbxImportUI()
   for k,v in dict(import_mesh=True,import_materials=False,import_textures=False,import_as_skeletal=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH).items():ui.set_editor_property(k,v)
   for k,v in dict(combine_meshes=True,auto_generate_collision=False,transform_vertex_to_absolute=True,convert_scene=True,convert_scene_unit=True,import_uniform_scale=1.,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS).items():ui.static_mesh_import_data.set_editor_property(k,v)
   t=unreal.AssetImportTask();t.filename=str(src);t.destination_path=local+'/Plants';t.destination_name=name;t.options=ui;t.automated=True;t.save=False;t.replace_existing=False;assert not unreal.EditorAssetLibrary.does_asset_exist(local+'/Plants/'+name);AT.import_asset_tasks([t]);mesh=unreal.load_asset(local+'/Plants/'+name);assert mesh
   for i in range(len(mesh.static_materials)):mesh.set_material(i,m)
   assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,False);b=mesh.get_bounding_box();rows.append(dict(source=str(src),mesh=mesh.get_path_name(),min=b.min.to_tuple(),max=b.max.to_tuple(),triangles=mesh.get_num_triangles(0),note='Vendor LOD1 imported as selected local mesh; source LOD0 and remaining original LODs untouched'))
finally:unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX '+str(old))
(D/'ImportedPlants.json').write_text(json.dumps(rows,indent=2))
