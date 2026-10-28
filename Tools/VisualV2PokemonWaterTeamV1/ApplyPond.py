"""Explicit, one-time VisualV2-only authoring. Preserve all original source assets.
Requires a clean owned editor. Imports only this task's new FBXs and saves only
those meshes plus the already existing VisualV2 map. No other map is loaded/saved.
"""
import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PokemonWaterTeamV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world()
assert W.get_name()=='Dev_TestMap_VisualV2'and not E.get_game_world()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert not(D/'PondApplied.json').exists()
folder='/Game/Environment/VisualV2PokemonWaterTeamV1/Meshes';names=['SM_VisualV2PondGround','SM_VisualV2PondWater']
assert all(not unreal.EditorAssetLibrary.does_asset_exist(folder+'/'+n)for n in names)
unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX 0');tasks=[]
for name in names:
 ui=unreal.FbxImportUI()
 for k,v in dict(import_mesh=True,import_materials=False,import_textures=False,import_as_skeletal=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH).items():ui.set_editor_property(k,v)
 for k,v in dict(combine_meshes=True,auto_generate_collision=False,transform_vertex_to_absolute=True,convert_scene=True,convert_scene_unit=True,import_uniform_scale=1.,generate_lightmap_u_vs=True,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS).items():ui.static_mesh_import_data.set_editor_property(k,v)
 t=unreal.AssetImportTask()
 for k,v in dict(filename=str(R/'Art/World/VisualV2PokemonWaterTeamV1/Exports'/(name+'.fbx')),destination_path=folder,destination_name=name,automated=True,save=False,replace_existing=False,options=ui).items():t.set_editor_property(k,v)
 tasks.append(t)
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors();by={a.get_actor_label():a for a in actors};ground=by['V2_Ground'];g=ground.static_mesh_component;original_mat=g.get_material(0)
watermat=unreal.load_asset('/Game/Environment/VisualV2EnvironmentV3/Materials/M_EQ3_Stream');assert watermat
for name,material in zip(names,[original_mat,watermat]):
 m=unreal.load_asset(folder+'/'+name);assert m;m.set_material(0,material)
 if name==names[0]:m.get_editor_property('body_setup').set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
 assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
changes=[]
def remember(a,purpose):changes.append({'actor':a.get_actor_label(),'before':a.get_actor_transform().export_text(),'purpose':purpose})
remember(ground,'same floor outline, real basin');g.set_static_mesh(unreal.load_asset(folder+'/'+names[0]));ground.set_actor_transform(unreal.Transform(),False,False)
water=by['P2D_Surface_Pond_Water'];remember(water,'expanded continuous existing water material');water.static_mesh_component.set_static_mesh(unreal.load_asset(folder+'/'+names[1]));water.static_mesh_component.set_material(0,watermat);water.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION);water.set_actor_transform(unreal.Transform(),False,False)
# Keep the existing blocker and interaction infrastructure. Water creatures ignore
# only these tagged player barriers; the player still cannot walk into the basin.
barrier=by['VS_WaterBlockPond'];remember(barrier,'player-only pond boundary');barrier.set_actor_location(unreal.Vector(720,-1000,100),False,False);barrier.set_actor_scale3d(unreal.Vector(17.6,12.6,2));barrier.tags=list(barrier.tags)+[unreal.Name('BiomePlayerWaterBarrier')]
for name in ['VS_WaterBlockOutlet','VS_WaterBlockEast','VS_WaterBlockWest']:
 if name in by:
  a=by[name];a.tags=list(set(list(a.tags)+[unreal.Name('BiomePlayerWaterBarrier')]))
# Original decorative pond surface stays as an inert historical actor, not a
# second active surface over the new basin.
a=by['Pond_Water'];remember(a,'inactive legacy surface');a.set_actor_hidden_in_game(True);a.set_actor_enable_collision(False)
def radial(x,y):return math.hypot((x-720)/900,(y+1000)/650)
def bank(x,y,extra):
 dx=(x-720)/900;dy=(y+1000)/650;r=math.hypot(dx,dy)
 if r<.001:dx,dy,r=1,0,1
 target=1.13+extra;return 720+900*dx/r*target,-1000+650*dy/r*target
instances=[]
for a in actors:
 if a in [ground,water,barrier]or a.get_actor_label().startswith('VS_WaterBlock'):continue
 for c in a.get_components_by_class(unreal.InstancedStaticMeshComponent):
  for i in range(c.get_instance_count()):
   t=c.get_instance_transform(i,True);x,y,z=t.translation.to_tuple()
   if radial(x,y)<1.08:
    nx,ny=bank(x,y,(i%7)*.019);t.translation=unreal.Vector(nx,ny,z);assert c.update_instance_transform(i,t,True,True,True);instances.append({'actor':a.get_actor_label(),'component':c.get_name(),'index':i,'before':[x,y,z],'after':[nx,ny,z]})
 if a.get_components_by_class(unreal.InstancedStaticMeshComponent):continue
 x,y,z=a.get_actor_location().to_tuple();name=a.get_actor_label()
 if name.startswith(('V2_Tree_','V2_Bush_','V2_Stone_'))and radial(x,y)<1.16:
  remember(a,'preserved decoration relocated onto bank');nx,ny=bank(x,y,.20 if 'Tree'in name else(len(changes)%5)*.025);a.set_actor_location(unreal.Vector(nx,ny,z),False,False)
# Save only the explicit target; fail rather than silently saving unrelated work.
assert all(p.get_path_name()=='/Game/Maps/Dev_TestMap_VisualV2'for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages())
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2')
for row in changes:row['after']=by[row['actor']].get_actor_transform().export_text()
(D/'PondApplied.json').write_text(json.dumps({'changes':changes,'relocated_instances':instances,'size_cm':[1800,1300],'maximum_depth_cm':424.2,'water_z':4.2,'original_assets_unchanged':True},indent=2))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
