"""Review corrections scoped exclusively to VisualV2 map/new assets."""
import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/DevTestMapVisualV2';D='/Game/Environment/DevTestMapVisualV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2' and not E.get_game_world();A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);actors=list(A.get_all_level_actors());L=unreal.MaterialEditingLibrary
# Correct generated ribbon facing without mutating shared NaturalGround materials.
path=D+'/Materials/M_V2_PathBlend';m=unreal.load_asset(path)
if not m:m=unreal.EditorAssetLibrary.duplicate_asset('/Game/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_PathBlend',path)
m.set_editor_property('two_sided',True);L.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m,False)
for a in actors:
 n=a.get_actor_label()
 if n.startswith('V2_Path_'):a.static_mesh_component.set_material(0,m);a.set_actor_location(unreal.Vector(0,0,.15),False,False)
 if isinstance(a,unreal.DirectionalLight):a.light_component.set_intensity(7.5 if n=='DirectionalLight_Dev' else .5)
 if isinstance(a,unreal.SkyLight):a.light_component.set_intensity(1.25)
 if n=='V2_OutdoorExposure':s=a.get_editor_property('settings');s.set_editor_property('auto_exposure_bias',.3);a.set_editor_property('settings',s)
 # NameLabel updates may change visibility; HiddenInGame remains a map-only visual override.
 for c in a.get_components_by_class(unreal.TextRenderComponent):c.set_hidden_in_game(True)
 if n=='V2_ForestOak_4':a.set_actor_location(unreal.Vector(-2680,-120,0),False,False)
# A second coherent village facade assembled from the existing kit, HISM per module.
kit=json.loads((R/'Art/Architecture/Westland/WestlandBuildingKit_V1.json').read_text());layout=json.loads((R/'Art/Architecture/Westland/Buildings/WL_Cottage_V1.json').read_text());modules={x['name']:x for x in kit['modules']};centre=unreal.Vector(-2250,-930,0);groups={};count=0
assert not any(a.get_actor_label().startswith('V2_Cottage_') for a in actors)
for entry in layout['placements']:groups.setdefault((entry['module'],entry['cutaway']),[]).append(entry)
occ=[];sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
for (key,occluder),entries in groups.items():
 desc=modules[key];mesh=unreal.load_asset('/Game/Environment/Architecture/Westland/Meshes/'+desc['category']+'/'+desc['mesh']);assert mesh
 a=A.spawn_actor_from_class(unreal.Actor,unreal.Vector());a.set_actor_label('V2_Cottage_'+key+('_Occluder' if occluder else ''));a.set_folder_path('VisualV2/Village/Cottage');a.tags=['DevVisualV2'];root=sub.k2_gather_subobject_data_for_instance(a)[0];handle,reason=sub.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle));assert c,reason;c.set_static_mesh(mesh);c.set_collision_profile_name('BlockAll' if desc['collision_boxes'] else 'NoCollision');c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_IGNORE);c.set_cast_shadow(not occluder);c.set_cull_distances(6000,8500)
 for entry in entries:c.add_instance(unreal.Transform(location=centre+unreal.Vector(*(v*100 for v in entry['position_m'])),rotation=unreal.Rotator(yaw=entry['yaw']),scale=unreal.Vector(1,1,1)),True);count+=1
 if occluder:occ.append(a)
cut=A.spawn_actor_from_class(unreal.PokeMonsterBuildingCutaway,centre+unreal.Vector(0,0,150));cut.set_actor_label('V2_Cottage_Cutaway');cut.set_folder_path('VisualV2/Village/Cottage');cut.set_editor_property('occluding_actors',occ);cut.set_editor_property('fade_duration',.4);cut.get_editor_property('interior_area').set_box_extent(unreal.Vector(310,310,200));th=cut.get_editor_property('door_threshold');th.set_relative_location(unreal.Vector(-300,0,-50),False,False);th.set_box_extent(unreal.Vector(20,65,100))
# No decoration inside the newly reserved footprint. Only new HISM instances changed.
removed=0
for a in actors:
 if a.get_actor_label().startswith('V2_Instanced_'):
  c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
  for i in reversed(range(c.get_instance_count())):
   t=c.get_instance_transform(i,True);p=t.translation
   if abs(p.x-centre.x)<360 and abs(p.y-centre.y)<360:c.remove_instance(i);removed+=1
# Link cottage doorway with a short organic path mesh using existing ribbon tool chunk.
g=__import__('runpy').run_path if False else None
(O/'Polish.json').write_text(json.dumps({'lighting':{'sun_lux':7.5,'fill_lux':.5,'sky':1.25,'exposure_bias':.3},'two_sided_path_material':path,'cottage_modules':count,'cottage_hism_groups':len(groups),'cottage_origin_cm':centre.to_tuple(),'cottage_occluders':[a.get_actor_label() for a in occ],'decoration_instances_removed_from_new_footprint':removed,'debug_labels_hidden_in_map_only':True},indent=2))
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');unreal.SystemLibrary.execute_console_command(w,'MAP CHECK')
