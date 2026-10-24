"""Small walkable viewing jetty from an existing bridge mesh; no new map or original asset changes."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);ES=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);SUB=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);w=E.get_editor_world();assert not E.get_game_world()and w.get_name()=='Dev_BiomeTestMap_V1';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();O=R/'Saved/BiomeTestV11/WaterJetty.json';assert not O.exists();actors=ES.get_all_level_actors();assert not any(a.get_actor_label().startswith('Biome_V11_Jetty')for a in actors)
a=ES.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*L.world(2200,2800,15)),unreal.Rotator(yaw=45));a.set_actor_label('Biome_V11_Jetty');a.tags=['BiomeTestV1'];a.set_folder_path('BiomeV1/Structures');a.static_mesh_component.set_static_mesh(unreal.load_asset('/Game/Environment/WestlandRegion/Meshes/WR_WoodBridge'));a.set_actor_scale3d(unreal.Vector(.42,1.16,.9));a.static_mesh_component.set_collision_profile_name('NoCollision')
def box(label,u,v,z,half):
 a=ES.spawn_actor_from_class(unreal.Actor,unreal.Vector(*L.world(u,v,z)),unreal.Rotator(yaw=45));a.set_actor_label(label);a.tags=['BiomeTestV1','CreatureNoWalk'];a.set_folder_path('BiomeV1/Collision');root=SUB.k2_gather_subobject_data_for_instance(a)[0];h,why=SUB.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.BoxComponent,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h));assert c,why;c.set_box_extent(unreal.Vector(*half));c.set_collision_profile_name('BlockAll');c.set_hidden_in_game(True)
box('Biome_V11_JettyDeck',2200,2800,7,(340,140,10))
for side in [-1,1]:box('Biome_V11_JettyRail_'+str(side),2200,2800+side*151,63,(340,6,43))
opened=[]
for a in actors:
 if a.actor_has_tag('BiomePlayerWaterBarrier'):
  p=a.get_actor_location();u,v=L.local(p.x,p.y)
  if abs(u-2200)<405 and abs(v-2800)<145:a.set_actor_enable_collision(False);opened.append(a.get_actor_label())
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert all(p.get_path_name()=='/Game/Maps/Dev_BiomeTestMap_V1'for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages());assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_BiomeTestMap_V1');O.write_text(json.dumps({'existing_mesh':'/Game/Environment/WestlandRegion/Meshes/WR_WoodBridge','purpose':'True fixed-camera observation of large swimmer without resizing creature or changing camera','deck_uv_centre_cm':[2200,2800],'deck_surface_z_cm':17,'half_size_cm':[340,140],'opened_only_under_deck_barriers':opened},indent=2))
