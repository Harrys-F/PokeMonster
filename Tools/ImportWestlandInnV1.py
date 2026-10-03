"""Import only additive Westland variants and append an inn to the existing kit map.
Run in a full Unreal Editor (legacy FBX requires Slate). Never modify HealingHouse or existing maps.
"""
import unreal,json,math
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();ART=ROOT/'Art/Architecture/Westland';OUT=ROOT/'Saved/WestlandInnV1'
DEST='/Game/Environment/Architecture/Westland';MAP='/Game/Maps/Dev_BuildingKitTestMap'
base=json.loads((ART/'WestlandBuildingKit_V1.json').read_text());kit=json.loads((ART/'WestlandBuildingKit_InnExtensions_V1.json').read_text());layout=json.loads((ART/'Buildings/WL_Inn_V1.json').read_text())
assert unreal.EditorAssetLibrary.does_asset_exist(MAP)
assert 'Dev_BuildingKitTestMap' in unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world().get_name()
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert all(not unreal.EditorAssetLibrary.does_asset_exist(DEST+'/Meshes/'+m['category']+'/'+m['mesh']) for m in kit['modules'])
unreal.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
assettools=unreal.AssetToolsHelpers.get_asset_tools();assets=[]
materials={'WL_'+n:unreal.load_asset(DEST+'/Materials/M_WL_'+n) for n in base['materials']}
assert all(materials.values())
tasks=[]
for entry in kit['modules']:
 ui=unreal.FbxImportUI()
 for p,v in {'import_mesh':True,'import_materials':False,'import_textures':False,'import_as_skeletal':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_STATIC_MESH}.items():ui.set_editor_property(p,v)
 for p,v in {'combine_meshes':True,'auto_generate_collision':False,'one_convex_hull_per_ucx':True,'transform_vertex_to_absolute':True,'bake_pivot_in_vertex':False,'convert_scene':True,'convert_scene_unit':True,'import_uniform_scale':1}.items():ui.static_mesh_import_data.set_editor_property(p,v)
 task=unreal.AssetImportTask()
 for p,v in {'filename':str(ART/'Exports/InnExtensions'/(entry['mesh']+'.fbx')),'destination_path':DEST+'/Meshes/'+entry['category'],'destination_name':entry['mesh'],'automated':True,'save':False,'replace_existing':False,'options':ui}.items():task.set_editor_property(p,v)
 tasks.append(task)
assettools.import_asset_tasks(tasks);meshes={};bounds={}
for entry in kit['modules']:
 path=DEST+'/Meshes/'+entry['category']+'/'+entry['mesh'];mesh=unreal.load_asset(path);assert mesh,path
 for i,slot in enumerate(mesh.get_editor_property('static_materials')):
  name=str(slot.get_editor_property('imported_material_slot_name'));assert name in materials,(path,name)
  mesh.set_material(i,materials[name])
 b=mesh.get_bounding_box();lo=[b.min.x,b.min.y,b.min.z];hi=[b.max.x,b.max.y,b.max.z]
 for i in range(3):assert abs(lo[i]-entry['min_m'][i]*100)<.3 and abs(hi[i]-entry['max_m'][i]*100)<.3,(path,lo,hi,entry)
 mesh.get_editor_property('asset_import_data').scripted_add_filename(str(ART/'Exports/InnExtensions'/(entry['mesh']+'.fbx')),0,'')
 meshes[entry['name']]=mesh;bounds[entry['name']]={'min_cm':lo,'max_cm':hi};assets.append(path)

for m in base['modules']:
 meshes[m['name']]=unreal.load_asset(DEST+'/Meshes/'+m['category']+'/'+m['mesh']);assert meshes[m['name']]
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
assert not any(a.actor_has_tag('Westland_Inn') for a in actors.get_all_level_actors())
# Preserve the cottage and its separate cutaway; only append actors and enlarge test ground.
cottage=[a for a in actors.get_all_level_actors() if a.actor_has_tag('Westland_Cottage')];assert len(cottage)==148
def pose(a):
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d()
 return [p.x,p.y,p.z,r.pitch,r.yaw,r.roll,s.x,s.y,s.z]
before={a.get_path_name():pose(a) for a in cottage}
def spawn(cls,label,p,yaw=0,folder='Westland/Buildings/Inn'):
 a=actors.spawn_actor_from_class(cls,unreal.Vector(*p),unreal.Rotator(yaw=yaw));a.set_actor_label(label);a.set_folder_path(folder);return a
origin=layout['map_origin_cm'];occluding=[];placed=[]
allmods=base['modules']+kit['modules']
for entry in layout['placements']:
 p=[entry['position_m'][i]*100+origin[i] for i in range(3)]
 a=spawn(unreal.StaticMeshActor,entry['label'],p,entry['yaw']);c=a.static_mesh_component;c.set_static_mesh(meshes[entry['module']]);c.set_cast_shadow(False)
 desc=next(m for m in allmods if m['name']==entry['module'])
 block=bool(desc['collision_boxes']);c.set_collision_profile_name('BlockAll' if block else 'NoCollision');c.set_editor_property('generate_overlap_events',False)
 if block:c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_IGNORE)
 if entry['role']=='HearthReserve':
  for i in range(c.get_num_materials()):c.set_material(i,materials['WL_Stone'])
 a.set_editor_property('tags',['Westland_Inn','Westland_Module_'+entry['module'],'Westland_Role_'+entry['role']]);placed.append(a)
 if entry['cutaway']:occluding.append(a)
cutclass=unreal.load_class(None,'/Script/PokeMonster.PokeMonsterBuildingCutaway');assert cutclass
cut=spawn(cutclass,'WL_Inn_Cutaway',(origin[0],origin[1],150))
cut.set_editor_property('fade_duration',.4);cut.set_editor_property('threshold_hysteresis',4);cut.set_editor_property('occluding_actors',occluding)
cut.get_editor_property('interior_area').set_box_extent(unreal.Vector(410,410,200))
threshold=cut.get_editor_property('door_threshold');threshold.set_relative_location(unreal.Vector(-400,-100,-42.5),False,False);threshold.set_box_extent(unreal.Vector(20,80,107.5))
cube=unreal.load_asset('/Engine/BasicShapes/Cube')
for item in layout['primitive_proxies']:
 p=[item['position_m'][i]*100+origin[i] for i in range(3)];a=spawn(unreal.StaticMeshActor,item['label'],p,folder='Westland/Buildings/Inn/InteriorReserve');c=a.static_mesh_component;c.set_static_mesh(cube);c.set_material(0,materials['WL_'+item['material']]);a.set_actor_scale3d(unreal.Vector(*item['size_m']));c.set_cast_shadow(False);c.set_collision_profile_name('BlockAll');c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_IGNORE);a.set_editor_property('tags',['Westland_Inn_Proxy'])
for i,m in enumerate(kit['modules']):
 a=spawn(unreal.StaticMeshActor,'Library_'+m['name'],((i%5)*240-480,3300+(i//5)*400,-m['min_m'][2]*100-3.6),folder='Westland/ModuleGallery/Extensions');c=a.static_mesh_component;c.set_static_mesh(meshes[m['name']]);c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False)
ground=next(a for a in actors.get_all_level_actors() if a.get_actor_label()=='WL_TestGround');ground.set_actor_location(unreal.Vector(0,500,-12),False,False);ground.set_actor_scale3d(unreal.Vector(36,72, .16))
# Simple readable approach, no village dressing or new ground assets.
a=spawn(unreal.StaticMeshActor,'WL_InnEntrancePath',(-825,-1600,-2),folder='Westland/TestGround');c=a.static_mesh_component;c.set_static_mesh(cube);a.set_actor_scale3d(unreal.Vector(8.5,2.6,.03));c.set_material(0,unreal.load_asset('/Game/Environment/Prototype2D/Materials/M_SoftPath'));c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False)
a=spawn(unreal.StaticMeshActor,'WL_ConnectionPath',(-1020,-800,-2),folder='Westland/TestGround');c=a.static_mesh_component;c.set_static_mesh(cube);a.set_actor_scale3d(unreal.Vector(2.4,16,.03));c.set_material(0,unreal.load_asset('/Game/Environment/Prototype2D/Materials/M_SoftPath'));c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False)
assert before=={a.get_path_name():pose(a) for a in cottage}
for asset in assets:assert unreal.EditorAssetLibrary.save_asset(asset,False)
assert unreal.EditorLoadingAndSavingUtils.save_map(world,MAP)
unreal.SystemLibrary.execute_console_command(world,'MAP CHECK')
(OUT/'UnrealImport.json').write_text(json.dumps({'map':MAP,'new_assets':assets,'new_meshes':len(kit['modules']),'placed_modules':len(placed),'existing_reused_instances':sum(p['existing'] for p in layout['placements']),'bounds':bounds,'cottage_transforms_preserved':True,'threshold_cm':[40,160,215],'fade_s':.4,'module_counts':layout['module_counts'],'no_cpp_changes':True},indent=2)+'\n')
unreal.log('WESTLAND_INN_IMPORT_COMPLETE')
