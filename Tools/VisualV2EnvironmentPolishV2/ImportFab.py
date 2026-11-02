"""Import only existing owned cache inputs to the already ignored local Fab root."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2EnvironmentPolishV2';V=Path('/Users/Shared/UnrealEngine/Launcher/VaultCache/FabLibrary');L='/Game/Fab/VisualV2TrialLocal/PolishV2';ROOT='/Game/Environment/VisualV2EnvironmentPolishV2';AT=unreal.AssetToolsHelpers.get_asset_tools();ML=unreal.MaterialEditingLibrary;W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2';rows=[];old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX 0')
def imp(src,path,name,options=None):
 q=path+'/'+name
 if unreal.EditorAssetLibrary.does_asset_exist(q):return unreal.load_asset(q)
 t=unreal.AssetImportTask();t.filename=str(src);t.destination_path=path;t.destination_name=name;t.automated=True;t.save=False;t.replace_existing=False
 if options:t.options=options
 AT.import_asset_tasks([t]);a=unreal.load_asset(q);assert a,(q,list(t.imported_object_paths));return a
try:
 for key,folder,vars in [('Hydrangea','Bigleaf_Hydrangea-b8220edc',['A','B']),('Pratia','Matted_Pratia-146202e2',['A','B']),('Embankment','Mossy_Embankment-65c47533',[None])]:
  fs=list((V/folder).rglob('*'));tex={}
  for suf in ['BaseColor','Normal','Roughness']+([]if key=='Embankment'else['Opacity']):
   src=next(p for p in fs if p.name.endswith('_2K_'+suf+'.jpg'));a=imp(src,L+'/'+key,'T_EP2_'+key+'_'+suf)
   if suf in ['Roughness','Opacity']:a.set_editor_property('srgb',False);a.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS)
   assert unreal.EditorAssetLibrary.save_loaded_asset(a,False);tex[suf]=a
  name='M_EP2_'+key;m=unreal.load_asset(ROOT+'/Materials/'+name)if unreal.EditorAssetLibrary.does_asset_exist(ROOT+'/Materials/'+name)else AT.create_asset(name,ROOT+'/Materials',unreal.Material,unreal.MaterialFactoryNew());assert m;ML.delete_all_material_expressions(m);m.set_editor_property('used_with_instanced_static_meshes',True)
  if key!='Embankment':m.set_editor_property('blend_mode',unreal.BlendMode.BLEND_MASKED);m.set_editor_property('two_sided',True);m.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_TWO_SIDED_FOLIAGE)
  for suf,prop in [('BaseColor',unreal.MaterialProperty.MP_BASE_COLOR),('Normal',unreal.MaterialProperty.MP_NORMAL),('Roughness',unreal.MaterialProperty.MP_ROUGHNESS),('Opacity',unreal.MaterialProperty.MP_OPACITY_MASK)]:
   if suf not in tex:continue
   n=ML.create_material_expression(m,unreal.MaterialExpressionTextureSample);n.texture=tex[suf];n.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL if suf=='Normal'else unreal.MaterialSamplerType.SAMPLERTYPE_MASKS if suf in ['Roughness','Opacity']else unreal.MaterialSamplerType.SAMPLERTYPE_COLOR);assert ML.connect_material_property(n,'R'if suf in ['Roughness','Opacity']else'RGB',prop)
   if suf=='BaseColor'and key!='Embankment':assert ML.connect_material_property(n,'RGB',unreal.MaterialProperty.MP_SUBSURFACE_COLOR)
  ML.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
  for var in vars:
   src=next(p for p in fs if p.name.endswith(('_Var'+var+'_LOD1.fbx')if var else'_Mid.fbx'));name='SM_EP2_'+key+(var or'');ui=unreal.FbxImportUI()
   for k,v in dict(import_mesh=True,import_materials=False,import_textures=False,import_as_skeletal=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH).items():ui.set_editor_property(k,v)
   for k,v in dict(combine_meshes=True,auto_generate_collision=False,transform_vertex_to_absolute=True,convert_scene=True,convert_scene_unit=True,import_uniform_scale=1.,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS).items():ui.static_mesh_import_data.set_editor_property(k,v)
   mesh=imp(src,L+'/'+key,name,ui)
   for i in range(len(mesh.static_materials)):mesh.set_material(i,m)
   assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,False);b=mesh.get_bounding_box();rows.append(dict(key=key,var=var,source=str(src),mesh=mesh.get_path_name(),triangles=mesh.get_num_triangles(0),min=b.min.to_tuple(),max=b.max.to_tuple()))
 # Native glTF meshes retain all vendor textures/material graphs in local ignored storage.
 for key,folder in [('MushroomA','Bolete_Mushrooms-6c750219'),('MushroomB','Bolete_Mushrooms-83c5683b'),('Wall','Mossy_Stone_Wall-c6fe222d')]:
  src=next((V/folder).rglob('*.gltf'));reg=unreal.AssetRegistryHelpers.get_asset_registry();assets=reg.get_assets_by_path(L+'/'+key,recursive=True);meshes=[d.get_asset()for d in assets if str(d.asset_class_path.asset_name)=='StaticMesh']
  if not meshes:
   t=unreal.AssetImportTask();t.filename=str(src);t.destination_path=L+'/'+key;t.automated=True;t.save=True;t.replace_existing=False;AT.import_asset_tasks([t]);assets=reg.get_assets_by_path(L+'/'+key,recursive=True);meshes=[d.get_asset()for d in assets if str(d.asset_class_path.asset_name)=='StaticMesh']
  assert meshes,key;meshes=sorted(meshes,key=lambda m:m.get_path_name());m=meshes[0];b=m.get_bounding_box();rows.append(dict(key=key,source=str(src),mesh=m.get_path_name(),available_meshes=[x.get_path_name()for x in meshes],triangles=m.get_num_triangles(0),min=b.min.to_tuple(),max=b.max.to_tuple()))
finally:unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX '+str(old))
(D/'ImportedFab.json').write_text(json.dumps(rows,indent=2));assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
