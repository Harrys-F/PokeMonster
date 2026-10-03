"""Import only new Westland assets and assemble a separate test map.
Run in a full Unreal Editor (legacy FBX requires Slate). Never modify HealingHouse or existing maps.
"""
import unreal,json,math
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();ART=ROOT/'Art/Architecture/Westland';OUT=ROOT/'Saved/WestlandKitV1'
DEST='/Game/Environment/Architecture/Westland';MAP='/Game/Maps/Dev_BuildingKitTestMap'
kit=json.loads((ART/'WestlandBuildingKit_V1.json').read_text());layout=json.loads((ART/'Buildings/WL_Cottage_V1.json').read_text())
assert not unreal.EditorAssetLibrary.does_asset_exist(MAP)
assert not unreal.EditorAssetLibrary.list_assets(DEST,True,False)
# Legacy FBX honors named UCX box bodies deterministically; do not rely on the
# Interchange auto-collision flag that failed in the earlier V3 import.
unreal.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
assettools=unreal.AssetToolsHelpers.get_asset_tools();materials={};assets=[]
for name in kit['materials']:
 old='/Game/Environment/HealingHouse/Materials/M_HH_V2_'+name
 new=DEST+'/Materials/M_WL_'+name
 material=unreal.EditorAssetLibrary.duplicate_asset(old,new);assert material,(old,new)
 assert material.get_path_name().split('.')[0]==new
 assert material.get_editor_property('blend_mode')==unreal.BlendMode.BLEND_MASKED
 materials['WL_'+name]=material;assets.append(new)
tasks=[]
for entry in kit['modules']:
 ui=unreal.FbxImportUI()
 for p,v in {'import_mesh':True,'import_materials':False,'import_textures':False,'import_as_skeletal':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_STATIC_MESH}.items():ui.set_editor_property(p,v)
 for p,v in {'combine_meshes':True,'auto_generate_collision':False,'one_convex_hull_per_ucx':True,'transform_vertex_to_absolute':True,'bake_pivot_in_vertex':False,'convert_scene':True,'convert_scene_unit':True,'import_uniform_scale':1}.items():ui.static_mesh_import_data.set_editor_property(p,v)
 task=unreal.AssetImportTask()
 for p,v in {'filename':str(ART/'Exports/Modules'/(entry['mesh']+'.fbx')),'destination_path':DEST+'/Meshes/'+entry['category'],'destination_name':entry['mesh'],'automated':True,'save':False,'replace_existing':False,'options':ui}.items():task.set_editor_property(p,v)
 tasks.append(task)
assettools.import_asset_tasks(tasks);meshes={};bounds={}
for entry in kit['modules']:
 path=DEST+'/Meshes/'+entry['category']+'/'+entry['mesh'];mesh=unreal.load_asset(path);assert mesh,path
 for i,slot in enumerate(mesh.get_editor_property('static_materials')):
  name=str(slot.get_editor_property('imported_material_slot_name'));assert name in materials,(path,name)
  mesh.set_material(i,materials[name])
 b=mesh.get_bounding_box();lo=[b.min.x,b.min.y,b.min.z];hi=[b.max.x,b.max.y,b.max.z]
 for i in range(3):assert abs(lo[i]-entry['min_m'][i]*100)<.3 and abs(hi[i]-entry['max_m'][i]*100)<.3,(path,lo,hi,entry)
 mesh.get_editor_property('asset_import_data').scripted_add_filename(str(ART/'Exports/Modules'/(entry['mesh']+'.fbx')),0,'')
 meshes[entry['name']]=mesh;bounds[entry['name']]={'min_cm':lo,'max_cm':hi};assets.append(path)
assert unreal.EditorLevelLibrary.new_level(MAP)
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
gm=unreal.load_class(None,'/Script/PokeMonster.PokeMonsterGameMode');assert gm
world.get_world_settings().set_editor_property('default_game_mode',gm)
def spawn(cls,label,p,yaw=0,folder='Westland/Buildings/Cottage'):
 a=actors.spawn_actor_from_class(cls,unreal.Vector(*p),unreal.Rotator(yaw=yaw));a.set_actor_label(label);a.set_folder_path(folder);return a
occluding=[];placed=[]
for entry in layout['placements']:
 a=spawn(unreal.StaticMeshActor,entry['label'],[x*100 for x in entry['position_m']],entry['yaw']);c=a.static_mesh_component;c.set_static_mesh(meshes[entry['module']]);c.set_cast_shadow(False)
 desc=next(m for m in kit['modules'] if m['name']==entry['module'])
 block=bool(desc['collision_boxes']);c.set_collision_profile_name('BlockAll' if block else 'NoCollision');c.set_editor_property('generate_overlap_events',False)
 if block:c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_IGNORE)
 a.set_editor_property('tags',['Westland_Cottage','Westland_Module_'+entry['module']]);placed.append(a)
 if entry['cutaway']:occluding.append(a)
cutclass=unreal.load_class(None,'/Script/PokeMonster.PokeMonsterBuildingCutaway');assert cutclass
cut=spawn(cutclass,'WL_Cottage_Cutaway',(0,0,150))
cut.set_editor_property('use_interior_camera',True);cut.set_editor_property('interior_camera_distance',2000);cut.set_editor_property('interior_camera_pitch',-50);cut.set_editor_property('interior_camera_yaw_offset',0);cut.set_editor_property('interior_camera_target',unreal.Vector(0,0,-70))
cut.set_editor_property('fade_duration',.4);cut.set_editor_property('threshold_hysteresis',4);cut.set_editor_property('occluding_actors',occluding)
cut.get_editor_property('interior_area').set_box_extent(unreal.Vector(310,310,200))
threshold=cut.get_editor_property('door_threshold');threshold.set_relative_location(unreal.Vector(-300,0,-50),False,False);threshold.set_box_extent(unreal.Vector(20,65,100))
# Display gallery is deliberately offset from the house and the walking route.
for i,entry in enumerate(kit['modules']):
 x=(i%5)*240-480;y=1300+(i//5)*400
 a=spawn(unreal.StaticMeshActor,'Library_'+entry['name'],(x,y,-entry['min_m'][2]*100-3.6),folder='Westland/ModuleGallery');a.static_mesh_component.set_static_mesh(meshes[entry['name']]);a.static_mesh_component.set_collision_profile_name('NoCollision');a.static_mesh_component.set_cast_shadow(False)
cube=unreal.load_asset('/Engine/BasicShapes/Cube')
def surface(label,p,size,material,block=True):
 a=spawn(unreal.StaticMeshActor,label,p,folder='Westland/TestGround');c=a.static_mesh_component;c.set_static_mesh(cube);c.set_material(0,material);a.set_actor_scale3d(unreal.Vector(*(v/100 for v in size)));c.set_collision_profile_name('BlockAll' if block else 'NoCollision');c.set_cast_shadow(False);return a
surface('WL_TestGround',(0,700,-12),(3600,4600,16),unreal.load_asset('/Game/Environment/Prototype2D/Materials/M_PaintedGround'))
surface('WL_EntrancePath',(-725,0,-2),(850,220,3),unreal.load_asset('/Game/Environment/Prototype2D/Materials/M_SoftPath'),False)
spawn(unreal.PlayerStart,'WL_PlayerStart',(-950,0,50),folder='Westland/Test')
sun=spawn(unreal.DirectionalLight,'WL_SoftDaylight',(0,0,900),folder='Westland/Test');sun.set_actor_rotation(unreal.Rotator(pitch=-55,yaw=-30),False);sun.light_component.set_editor_property('intensity',2.2);sun.light_component.set_editor_property('cast_shadows',False)
sky=spawn(unreal.SkyLight,'WL_SoftAmbient',(0,0,700),folder='Westland/Test');sky.light_component.set_editor_property('source_type',unreal.SkyLightSourceType.SLS_SPECIFIED_CUBEMAP);sky.light_component.set_editor_property('cubemap',unreal.load_asset('/Engine/EngineResources/DefaultTextureCube'));sky.light_component.set_editor_property('intensity',.7)
assert unreal.EditorAssetLibrary.save_directory(DEST,True,True)
assert unreal.EditorLoadingAndSavingUtils.save_map(world,MAP)
unreal.SystemLibrary.execute_console_command(world,'MAP CHECK')
(OUT/'UnrealImport.json').write_text(json.dumps({'map':MAP,'assets':assets,'meshes':len(meshes),'materials':len(materials),'bounds':bounds,'placed_modules':len(placed),'cutaway_class':'PokeMonsterBuildingCutaway','threshold_cm':[40,130,200],'fade_s':.4,'module_counts':layout['module_counts'],'no_cpp_changes':True},indent=2)+'\n')
unreal.log('WESTLAND_IMPORT_COMPLETE')
