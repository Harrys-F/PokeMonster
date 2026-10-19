
# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();A=R/'Art/World/TreeShadowProxyV1';O=R/'Saved/TreeShadowProxyV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=e.get_editor_world()
assert not e.get_game_world() and w.get_name()=='Dev_TestMap_TreeShadowProxyV1';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
D='/Game/Environment/TreeShadowProxyV1';T=unreal.AssetToolsHelpers.get_asset_tools();S=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);L=unreal.MaterialEditingLibrary
assert not unreal.EditorAssetLibrary.does_directory_exist(D)
m=T.create_asset('M_TSP_OpaqueShadow',D,unreal.Material,unreal.MaterialFactoryNew());m.set_editor_property('blend_mode',unreal.BlendMode.BLEND_OPAQUE);m.set_editor_property('two_sided',False)
v=L.create_material_expression(m,unreal.MaterialExpressionConstant3Vector);v.set_editor_property('constant',unreal.LinearColor(.2,.22,.16,1));L.connect_material_property(v,'',unreal.MaterialProperty.MP_BASE_COLOR);L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
flag='Interchange.FeatureFlags.Import.FBX';before=unreal.SystemLibrary.get_console_variable_float_value(flag);unreal.SystemLibrary.execute_console_command(w,flag+' 0');meshes={};audit=[]
for name in ['SM_TSP_OakAncient_Bark','SM_TSP_OakAncient_Crown']:
 ui=unreal.FbxImportUI()
 for k,v in {'import_mesh':True,'import_materials':False,'import_textures':False,'import_as_skeletal':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_STATIC_MESH}.items():ui.set_editor_property(k,v)
 for k,v in {'combine_meshes':True,'auto_generate_collision':False,'convert_scene':True,'convert_scene_unit':True,'import_uniform_scale':1,'normal_import_method':unreal.FBXNormalImportMethod.FBXNIM_COMPUTE_NORMALS,'generate_lightmap_u_vs':False}.items():ui.static_mesh_import_data.set_editor_property(k,v)
 t=unreal.AssetImportTask()
 for k,v in {'filename':str(A/'Exports'/(name+'.fbx')),'destination_path':D,'destination_name':name,'automated':True,'save':False,'replace_existing':False,'options':ui}.items():t.set_editor_property(k,v)
 T.import_asset_tasks([t]);sm=unreal.load_asset(D+'/'+name);assert sm;sm.set_material(0,m)
 bs=S.get_lod_build_settings(sm,0);bs.distance_field_resolution_scale=0;bs.recompute_normals=True;bs.recompute_tangents=True;bs.use_mikk_t_space=True;bs.remove_degenerates=True;S.set_lod_build_settings(sm,0,bs);assert unreal.EditorAssetLibrary.save_loaded_asset(sm,False);meshes[name]=sm
 audit.append({'mesh':sm.get_path_name(),'triangles':sm.get_num_triangles(0),'slots':len(sm.static_materials),'collision_count':S.get_simple_collision_count(sm)+S.get_convex_collision_count(sm),'bounds':str(sm.get_bounding_box())})
unreal.SystemLibrary.execute_console_command(w,flag+' '+str(before))
light=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.DirectionalLight) if a.get_actor_label()=='DirectionalLight_Dev');direction=light.get_actor_forward_vector()
actors=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor);chosen=[next(a for a in actors if a.get_actor_label()=='V2_ForestOak_'+str(i)) for i in range(3)];records=[];AS=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for tree in chosen:
 c=tree.static_mesh_component;assert c.cast_shadow;c.set_cast_shadow(False)
 for name,sm in meshes.items():
  position=tree.get_actor_location()
  if name.endswith('Crown'):
   dz=-410*tree.get_actor_scale3d().z;position.x+=dz*direction.x/direction.z;position.y+=dz*direction.y/direction.z
  a=AS.spawn_actor_from_class(unreal.StaticMeshActor,position,tree.get_actor_rotation());a.set_actor_label('TSP_'+tree.get_actor_label()+'_'+name.rsplit('_',1)[1]);a.set_actor_scale3d(tree.get_actor_scale3d());q=a.static_mesh_component;q.set_static_mesh(sm)
  q.set_collision_profile_name('NoCollision');q.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION);q.set_editor_property('generate_overlap_events',False);q.set_editor_property('cast_shadow',True);q.set_editor_property('cast_hidden_shadow',True);q.set_editor_property('hidden_in_game',True);q.set_editor_property('affect_distance_field_lighting',False);q.set_editor_property('visible_in_ray_tracing',False);q.set_editor_property('receives_decals',False)
  a.set_folder_path('TreeShadowProxyV1_ShadowOnly');a.tags=['TreeShadowProxyV1'];records.append({'tree':tree.get_actor_label(),'proxy':a.get_actor_label(),'transform':str(a.get_actor_transform()),'hidden_in_game':True,'cast_hidden_shadow':True,'collision':'None'})
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(O/'ImportPlace.json').write_text(json.dumps({'meshes':audit,'actors':records,'only_original_change':'CastShadow=False on exactly V2_ForestOak_0/1/2 in test map'},indent=2))
