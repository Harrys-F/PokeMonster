"""Reconfigure only owned Inn actors in the existing kit test map. No imports."""
import unreal,json
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();ART=ROOT/'Art/Architecture/Westland';OUT=ROOT/'Saved/WestlandInnCamera';OUT.mkdir(parents=True,exist_ok=True)
MAP='/Game/Maps/Dev_BuildingKitTestMap';DEST='/Game/Environment/Architecture/Westland'
layout=json.loads((ART/'Buildings/WL_Inn_V1.json').read_text());base=json.loads((ART/'WestlandBuildingKit_V1.json').read_text());ext=json.loads((ART/'WestlandBuildingKit_InnExtensions_V1.json').read_text());defs={d['name']:d for d in base['modules']+ext['modules']}
ed=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not ed.get_game_world();world=ed.get_editor_world();assert world.get_name()=='Dev_BuildingKitTestMap'
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);allactors=actors.get_all_level_actors();by={a.get_actor_label():a for a in allactors}
assert 'WL_Inn_Cutaway' in by
owned=lambda a:a.actor_has_tag('Westland_Inn') or a.actor_has_tag('Westland_Inn_Proxy') or a.get_actor_label() in ('WL_Inn_Cutaway','WL_InnEntrancePath')
def signature(a):
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d();d={'path':a.get_path_name(),'pose':[p.x,p.y,p.z,r.pitch,r.yaw,r.roll,s.x,s.y,s.z],'tags':[str(t) for t in a.get_editor_property('tags')]}
 c=a.get_component_by_class(unreal.StaticMeshComponent)
 if c:d.update(mesh=c.static_mesh.get_path_name() if c.static_mesh else None,materials=[c.get_material(i).get_path_name() if c.get_material(i) else None for i in range(c.get_num_materials())],collision=str(c.get_collision_enabled()))
 if a.get_actor_label()=='WL_Cottage_Cutaway':d.update(distance=a.get_editor_property('interior_camera_distance'),pitch=a.get_editor_property('interior_camera_pitch'),yaw=a.get_editor_property('interior_camera_yaw_offset'),occluders=sorted(x.get_path_name() for x in a.get_editor_property('occluding_actors')))
 return d
before={a.get_actor_label():signature(a) for a in allactors if not owned(a)}
meshes={n:unreal.load_asset(DEST+'/Meshes/'+d['category']+'/'+d['mesh']) for n,d in defs.items()};assert all(meshes.values())
materials={n:unreal.load_asset(DEST+'/Materials/M_WL_'+n) for n in base['materials']};assert all(materials.values())
origin=layout['map_origin_cm'];keep=set();occluders=[]
def get(label,p,yaw=0):
 keep.add(label);a=by.get(label)
 if a is None:a=actors.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*p),unreal.Rotator(yaw=yaw));a.set_actor_label(label)
 else:a.set_actor_location(unreal.Vector(*p),False,False);a.set_actor_rotation(unreal.Rotator(yaw=yaw),False)
 a.set_actor_scale3d(unreal.Vector(1,1,1));a.set_folder_path('Westland/Buildings/Inn');return a
for entry in layout['placements']:
 p=[entry['position_m'][i]*100+origin[i] for i in range(3)];a=get(entry['label'],p,entry['yaw']);c=a.static_mesh_component;c.set_static_mesh(meshes[entry['module']]);c.set_cast_shadow(False)
 # Reset instance material overrides before assigning optional hearth stone.
 c.set_editor_property('override_materials',[])
 if entry['role']=='HearthReserve':
  for i in range(c.get_num_materials()):c.set_material(i,materials['Stone'])
 c.set_collision_profile_name('BlockAll' if defs[entry['module']]['collision_boxes'] else 'NoCollision');c.set_editor_property('generate_overlap_events',False);c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_IGNORE)
 a.set_editor_property('tags',['Westland_Inn','Westland_Module_'+entry['module'],'Westland_Role_'+entry['role']])
 if entry['cutaway']:occluders.append(a)
for item in layout['primitive_proxies']:
 a=get(item['label'],[item['position_m'][i]*100+origin[i] for i in range(3)]);c=a.static_mesh_component;c.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'));c.set_material(0,materials[item['material']]);a.set_actor_scale3d(unreal.Vector(*item['size_m']));c.set_cast_shadow(False);c.set_collision_profile_name('BlockAll');c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_IGNORE);a.set_editor_property('tags',['Westland_Inn_Proxy'])
# Delete only obsolete actors belonging to the previous owned Inn composition.
for a in allactors:
 if (a.actor_has_tag('Westland_Inn') or a.actor_has_tag('Westland_Inn_Proxy')) and a.get_actor_label() not in keep:actors.destroy_actor(a)
cut=by['WL_Inn_Cutaway'];cut.set_actor_location(unreal.Vector(100,-1500,150),False,False);cut.set_editor_property('fade_duration',.4);cut.set_editor_property('threshold_hysteresis',4);cut.set_editor_property('occluding_actors',occluders);cut.set_editor_property('use_interior_camera',True)
cam=layout['interior_camera'];cut.set_editor_property('interior_camera_distance',cam['distance_cm']);cut.set_editor_property('interior_camera_pitch',cam['pitch']);cut.set_editor_property('interior_camera_yaw_offset',cam['yaw_offset']);cut.set_editor_property('interior_camera_target',unreal.Vector(0,0,-70))
cut.get_editor_property('interior_area').set_box_extent(unreal.Vector(410,410,200));door=cut.get_editor_property('door_threshold');door.set_relative_location(unreal.Vector(-400,-100,-42.5),False,False);door.set_box_extent(unreal.Vector(20,80,107.5))
regions=[]
for item in layout['interior_regions_cm']:
 region=unreal.PokeMonsterBuildingInteriorRegion();region.set_editor_property('center',unreal.Vector(*item['center']));region.set_editor_property('extent',unreal.Vector(*item['extent']));regions.append(region)
cut.set_editor_property('interior_regions',regions)
path=by['WL_InnEntrancePath'];path.set_actor_location(unreal.Vector(-775,-1600,-2),False,False);path.set_actor_scale3d(unreal.Vector(9.5,2.6,.03))
after={a.get_actor_label():signature(a) for a in actors.get_all_level_actors() if not owned(a)};assert before==after,'Unrelated actors changed'
assert unreal.EditorLoadingAndSavingUtils.save_map(world,MAP)
(OUT/'MapConfiguration.json').write_text(json.dumps({'map':MAP,'non_inn_actors_unchanged':before,'modules':len(layout['placements']),'occluders':[a.get_actor_label() for a in occluders],'camera':cam,'regions':layout['interior_regions_cm'],'new_assets':[]},indent=2)+'\n')
unreal.log('WESTLAND_INN_CONFIGURED')
