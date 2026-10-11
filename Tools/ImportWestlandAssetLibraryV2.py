"""Targeted in-place reimport: twenty V2 meshes only, unchanged existing asset paths."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir());ART=R/'Art/World/WestlandAssetLibrary';O=R/'Saved/WestlandAssetLibraryV2';DEST='/Game/Environment/WestlandAssetLibrary';MAP='/Game/Maps/Dev_WestlandAssetLibrary'
e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();assert e.get_editor_world().get_name()=='Dev_WestlandAssetLibrary'
data=json.loads((ART/'Assets.json').read_text());assets=[a for a in data['assets'] if a.get('art_status')=='V2_review_pending'];assert len(assets)==20 and (O/'ArtReviewAccepted.json').exists()
T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;SM=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
materials={}
for key in ('LeafOak','LeafBirch','LeafOrchard','LeafFern'):
 spec=data['materials'][key];name=Path(spec['texture']).stem;p=DEST+'/Textures/'+name
 if not unreal.EditorAssetLibrary.does_asset_exist(p):
  t=unreal.AssetImportTask();t.filename=str(R/spec['texture']);t.destination_path=DEST+'/Textures';t.destination_name=name;t.automated=True;t.save=False;T.import_asset_tasks([t])
 tex=unreal.load_asset(p);tex.set_editor_property('max_texture_size',1024);tex.set_editor_property('never_stream',False);tex.set_editor_property('srgb',True);unreal.EditorAssetLibrary.save_loaded_asset(tex,False)
 p=DEST+'/Materials/MI_WLA_'+key
 if unreal.EditorAssetLibrary.does_asset_exist(p):mi=unreal.load_asset(p)
 else:mi=T.create_asset('MI_WLA_'+key,DEST+'/Materials',unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew())
 L.set_material_instance_parent(mi,unreal.load_asset(DEST+'/Materials/M_WLA_PaintedLeaf'));L.set_material_instance_texture_parameter_value(mi,'Paint',tex);L.set_material_instance_vector_parameter_value(mi,'Tint',unreal.LinearColor(*spec['color'],1));L.update_material_instance(mi);unreal.EditorAssetLibrary.save_loaded_asset(mi,False);materials['WLA_'+key]=mi
unreal.SystemLibrary.execute_console_command(e.get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0')
tasks=[]
for a in assets:
 ui=unreal.FbxImportUI()
 for k,v in {'import_mesh':True,'import_materials':False,'import_textures':False,'import_as_skeletal':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_STATIC_MESH}.items():ui.set_editor_property(k,v)
 for k,v in {'combine_meshes':True,'auto_generate_collision':False,'one_convex_hull_per_ucx':True,'transform_vertex_to_absolute':True,'convert_scene':True,'convert_scene_unit':True,'import_uniform_scale':1,'vertex_color_import_option':unreal.VertexColorImportOption.REPLACE,'generate_lightmap_u_vs':True,'normal_import_method':unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS,'normal_generation_method':unreal.FBXNormalGenerationMethod.MIKK_T_SPACE}.items():ui.static_mesh_import_data.set_editor_property(k,v)
 task=unreal.AssetImportTask()
 for k,v in {'filename':str(ART/'Exports'/(a['object']+'.fbx')),'destination_path':DEST+'/Meshes/'+a['family'],'destination_name':a['object'],'automated':True,'save':False,'replace_existing':True,'replace_existing_settings':True,'options':ui}.items():task.set_editor_property(k,v)
 tasks.append(task)
T.import_asset_tasks(tasks);audit=[]
for a in assets:
 sm=unreal.load_asset(DEST+'/Meshes/'+a['family']+'/'+a['object']);slots=list(sm.get_editor_property('static_materials'))
 for slot in slots:
  key=str(slot.get_editor_property('imported_material_slot_name')).split('.')[0];mat=materials.get(key) or unreal.load_asset(DEST+'/Materials/MI_'+key);assert mat,key;slot.set_editor_property('material_interface',mat)
 sm.set_editor_property('static_materials',slots)
 # LOD reduction preserves surface normals; reduced LODs recompute a valid Mikk tangent frame.
 opts=unreal.StaticMeshReductionOptions();reduction=[]
 for fraction,screen in [(1.,1.),(.60,.40),(.30,.15)] if a['triangles']>1000 else [(1.,1.)]:
  x=unreal.StaticMeshReductionSettings();x.percent_triangles=fraction;x.screen_size=screen;reduction.append(x)
 opts.reduction_settings=reduction;opts.auto_compute_lod_screen_size=False;SM.set_lods(sm,opts)
 for lod in range(SM.get_lod_count(sm)):
  bs=SM.get_lod_build_settings(sm,lod);bs.distance_field_resolution_scale=0;bs.recompute_normals=lod>0;bs.recompute_tangents=lod>0;bs.use_mikk_t_space=True;bs.remove_degenerates=True;SM.set_lod_build_settings(sm,lod,bs)
 bounds=sm.get_bounding_box();size=bounds.max-bounds.min;assert all(abs(v/100-t)<max(.02,t*.01) for v,t in zip(size.to_tuple(),a['dimensions_m'])),a['id'];count=SM.get_simple_collision_count(sm)+SM.get_convex_collision_count(sm);assert count==len(a['collision_objects'])
 assert all(sm.get_material(i) for i in range(SM.get_number_materials(sm)));unreal.EditorAssetLibrary.set_metadata_tag(sm,'WLA_ArtStatus','V2: source/import reviewed; human approval pending');assert unreal.EditorAssetLibrary.save_loaded_asset(sm,False)
 audit.append({'id':a['id'],'triangles':[sm.get_num_triangles(i) for i in range(SM.get_lod_count(sm))],'bounds_cm':size.to_tuple(),'slots':SM.get_number_materials(sm),'collisions':count,'asset_path':sm.get_path_name()})
# Refresh art tags; orient only the two runestones toward the unchanged game camera.
for actor in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
 if actor.get_actor_label().startswith('Library_') and any(actor.get_actor_label()=='Library_'+a['id'] for a in assets):actor.tags=['WLA_V1','WLA_ArtV2']
 if actor.get_actor_label().startswith('Library_WLA_Runestone_'):actor.set_actor_rotation(unreal.Rotator(pitch=0,yaw=45,roll=0),False)
assert unreal.EditorLoadingAndSavingUtils.save_map(e.get_editor_world(),MAP)
(O/'ImportAudit.json').write_text(json.dumps(audit,indent=2));unreal.log('WLA_V2_IMPORT_COMPLETE')
