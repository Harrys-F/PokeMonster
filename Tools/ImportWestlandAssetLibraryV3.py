"""Three new sibling meshes + one shared Masked foliage family. Never reimports V2."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir());A=R/'Art/World/WestlandAssetLibrary';O=R/'Saved/WestlandAssetLibraryV3';D='/Game/Environment/WestlandAssetLibrary/QualityV3';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world() and E.get_editor_world().get_name()=='Dev_WestlandAssetLibrary'
data=json.loads((A/'ArtQualityV3.json').read_text());assert len(data['assets'])==3 and (O/'ArtReviewAccepted.json').exists()
T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;S=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
tn='T_WLA_FoliageGroups_V3';task=unreal.AssetImportTask();task.filename=str(R/data['foliage_texture']);task.destination_path=D+'/Textures';task.destination_name=tn;task.automated=True;task.save=False;task.replace_existing=True;T.import_asset_tasks([task]);tex=unreal.load_asset(D+'/Textures/'+tn);assert tex
tex.set_editor_property('srgb',True);tex.set_editor_property('max_texture_size',2048);tex.set_editor_property('never_stream',False)
# Native texture build normalization preserves the RGBA source and atlas UV layout.
tex.set_editor_property('power_of_two_mode',unreal.TexturePowerOfTwoSetting.STRETCH_TO_POWER_OF_TWO);tex.set_editor_property('mip_gen_settings',unreal.TextureMipGenSettings.TMGS_FROM_TEXTURE_GROUP)
tex.set_editor_property('do_scale_mips_for_alpha_coverage',True);tex.set_editor_property('alpha_coverage_thresholds',unreal.Vector4(0,0,0,.45));unreal.EditorAssetLibrary.save_loaded_asset(tex,False)
mn='M_WLA_FoliageGroups_V3';m=unreal.load_asset(D+'/Materials/'+mn)
if not m:
 m=T.create_asset(mn,D+'/Materials',unreal.Material,unreal.MaterialFactoryNew())
if unreal.EditorAssetLibrary.get_metadata_tag(m,'WLA_V3_GraphReady')!='true':
 m.set_editor_property('blend_mode',unreal.BlendMode.BLEND_MASKED);m.set_editor_property('two_sided',True);m.set_editor_property('opacity_mask_clip_value',.45)
 paint=L.create_material_expression(m,unreal.MaterialExpressionTextureSampleParameter2D,-600,0);paint.set_editor_property('parameter_name','Paint');paint.set_editor_property('texture',tex)
 tint=L.create_material_expression(m,unreal.MaterialExpressionVectorParameter,-600,220);tint.set_editor_property('parameter_name','Tint');tint.set_editor_property('default_value',unreal.LinearColor(.94,.98,.91,1))
 vc=L.create_material_expression(m,unreal.MaterialExpressionVertexColor,-600,380);a=L.create_material_expression(m,unreal.MaterialExpressionMultiply,-340,0);b=L.create_material_expression(m,unreal.MaterialExpressionMultiply,-120,0)
 L.connect_material_expressions(paint,'RGB',a,'A');L.connect_material_expressions(tint,'RGB',a,'B');L.connect_material_expressions(a,'',b,'A');L.connect_material_expressions(vc,'RGB',b,'B');L.connect_material_property(b,'',unreal.MaterialProperty.MP_BASE_COLOR);L.connect_material_property(paint,'A',unreal.MaterialProperty.MP_OPACITY_MASK)
 for value,prop,y in [(.95,unreal.MaterialProperty.MP_ROUGHNESS,540),(.05,unreal.MaterialProperty.MP_SPECULAR,620)]:
  n=L.create_material_expression(m,unreal.MaterialExpressionConstant,-120,y);n.set_editor_property('r',value);L.connect_material_property(n,'',prop)
 L.recompile_material(m);unreal.EditorAssetLibrary.set_metadata_tag(m,'WLA_V3_GraphReady','true');assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
mi=T.create_asset('MI_WLA_FoliageGroups_V3',D+'/Materials',unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew()) if not unreal.EditorAssetLibrary.does_asset_exist(D+'/Materials/MI_WLA_FoliageGroups_V3') else unreal.load_asset(D+'/Materials/MI_WLA_FoliageGroups_V3')
L.set_material_instance_parent(mi,m);L.set_material_instance_texture_parameter_value(mi,'Paint',tex);L.update_material_instance(mi);unreal.EditorAssetLibrary.save_loaded_asset(mi,False)
materials={'WLA_V3_Bark':unreal.load_asset('/Game/Environment/WestlandAssetLibrary/Materials/MI_WLA_Bark'),'WLA_V3_FoliageGroups':mi};assert all(materials.values())
unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0');tasks=[]
for a in data['assets']:
 ui=unreal.FbxImportUI()
 for k,v in {'import_mesh':True,'import_materials':False,'import_textures':False,'import_as_skeletal':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_STATIC_MESH}.items():ui.set_editor_property(k,v)
 for k,v in {'combine_meshes':True,'auto_generate_collision':False,'one_convex_hull_per_ucx':True,'transform_vertex_to_absolute':True,'convert_scene':True,'convert_scene_unit':True,'import_uniform_scale':1,'vertex_color_import_option':unreal.VertexColorImportOption.REPLACE,'generate_lightmap_u_vs':True,'normal_import_method':unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS,'normal_generation_method':unreal.FBXNormalGenerationMethod.MIKK_T_SPACE}.items():ui.static_mesh_import_data.set_editor_property(k,v)
 t=unreal.AssetImportTask()
 for k,v in {'filename':str(A/'Exports/V3'/(a['object']+'.fbx')),'destination_path':D+'/Meshes/'+a['family'],'destination_name':a['object'],'automated':True,'save':False,'replace_existing':True,'replace_existing_settings':True,'options':ui}.items():t.set_editor_property(k,v)
 tasks.append(t)
T.import_asset_tasks(tasks);audit=[]
for a in data['assets']:
 sm=unreal.load_asset(D+'/Meshes/'+a['family']+'/'+a['object']);assert sm;slots=list(sm.get_editor_property('static_materials'));assert len(slots)==2
 for slot in slots:slot.set_editor_property('material_interface',materials[str(slot.get_editor_property('imported_material_slot_name')).split('.')[0]])
 sm.set_editor_property('static_materials',slots);opts=unreal.StaticMeshReductionOptions();rs=[]
 for fraction,screen in [(1,1),(.60,.34),(.30,.13)]:
  x=unreal.StaticMeshReductionSettings();x.percent_triangles=fraction;x.screen_size=screen;rs.append(x)
 opts.reduction_settings=rs;opts.auto_compute_lod_screen_size=False;S.set_lods(sm,opts)
 for i in range(S.get_lod_count(sm)):
  bs=S.get_lod_build_settings(sm,i);bs.recompute_normals=i>0;bs.recompute_tangents=i>0;bs.use_mikk_t_space=True;bs.remove_degenerates=True;bs.distance_field_resolution_scale=0;S.set_lod_build_settings(sm,i,bs)
 box=sm.get_bounding_box();size=box.max-box.min;assert all(abs(v/100-t)<max(.02,t*.01) for v,t in zip(size.to_tuple(),a['dimensions_m']))
 count=S.get_simple_collision_count(sm)+S.get_convex_collision_count(sm);assert count==len(a['collision_objects']);assert sm.get_num_triangles(0)==a['triangles'];assert box.min.z>=-.1
 unreal.EditorAssetLibrary.set_metadata_tag(sm,'WLA_ArtStatus','V3: technical and agent visual review; human approval pending');assert unreal.EditorAssetLibrary.save_loaded_asset(sm,False)
 audit.append({'object':a['object'],'asset':sm.get_path_name(),'triangles':[sm.get_num_triangles(i) for i in range(S.get_lod_count(sm))],'slots':2,'sections_lod0':sm.get_num_sections(0),'collision_count':count,'bounds_cm':list(size.to_tuple()),'uv_channels':S.get_num_uv_channels(sm,0)})
(O/'ImportAudit.json').write_text(json.dumps(audit,indent=2));unreal.log('WLA_V3_IMPORT_PASS')
