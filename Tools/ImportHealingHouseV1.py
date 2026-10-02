"""Unreal Python commandlet: import V1, validate next to the retained blockout,
then replace visibility only. Existing collision/functions/actors are preserved.
Refuses to overwrite assets or run twice. No Dev_TestMap access.
"""
import unreal
import json
from pathlib import Path

ROOT = Path(unreal.Paths.project_dir()).resolve()
ART = ROOT / 'Art/HealingHouse'
MAP = '/Game/Maps/Dev_HealingHouseTestMap'
DEST = '/Game/Environment/HealingHouse'
audit = json.loads((ART/'Review/GeometryAudit.json').read_text())
# Reject a completed integration before creating or changing any assets.
world=unreal.EditorLoadingAndSavingUtils.load_map(MAP)
if not world: raise RuntimeError('Existing house map missing')
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
original=actors.get_all_level_actors()
if any(a.actor_has_tag('HealingHouse_BlenderV1') for a in original):
    raise RuntimeError('V1 already placed; preserve the completed integration')
if unreal.EditorAssetLibrary.list_assets(DEST+'/Materials',True,False):
    raise RuntimeError('Existing materials; preserve user work')
existing_paths=unreal.EditorAssetLibrary.list_assets(DEST+'/Meshes',True,False)
expected_paths=[DEST+'/Meshes/SM_'+m['name'] for m in audit['modules']]
if existing_paths and set(p.split('.')[0] for p in existing_paths)!=set(expected_paths):
    raise RuntimeError('Unexpected existing assets; preserve user work.')
ui = unreal.FbxImportUI()
ui.set_editor_property('import_mesh', True)
ui.set_editor_property('import_materials', False)
ui.set_editor_property('import_textures', False)
ui.set_editor_property('import_as_skeletal', False)
ui.set_editor_property('automated_import_should_detect_type', False)
ui.set_editor_property('mesh_type_to_import', unreal.FBXImportType.FBXIT_STATIC_MESH)
data = ui.static_mesh_import_data
for prop, val in {'combine_meshes':False,'auto_generate_collision':False,
                  'transform_vertex_to_absolute':True,'bake_pivot_in_vertex':False,
                  'convert_scene':True,'convert_scene_unit':True,
                  'force_front_x_axis':False,'import_uniform_scale':1.0}.items():
    data.set_editor_property(prop,val)
task = unreal.AssetImportTask()
task.set_editor_property('filename',str(ART/'Exports/HealingHouse_V1.fbx'))
task.set_editor_property('destination_path',DEST+'/Meshes')
task.set_editor_property('automated',True)
task.set_editor_property('save',True)
task.set_editor_property('replace_existing',False)
task.set_editor_property('options',ui)
if not existing_paths:
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
meshes = {}
report = {'fbx':audit['export'],'map':MAP,'import_scale':1.0,'bounds':{},'assets':[]}
for path in (existing_paths or task.get_editor_property('imported_object_paths')):
    obj = unreal.load_asset(path)
    if not isinstance(obj,unreal.StaticMesh): continue
    # FBX import may prefix the filename; resolve the authored object suffix.
    match = next((m for m in audit['modules'] if obj.get_name().endswith(m['name'])),None)
    if not match: raise RuntimeError('Unexpected FBX mesh: '+obj.get_name())
    name = match['name']
    new_path = DEST+'/Meshes/SM_'+name
    if obj.get_path_name().split('.')[0] != new_path:
        if not unreal.EditorAssetLibrary.rename_asset(obj.get_path_name(),new_path):
            raise RuntimeError('Mesh rename failed: '+name)
    meshes[name] = obj
    bounds = obj.get_bounding_box()
    mins=[bounds.min.x,bounds.min.y,bounds.min.z]
    maxs=[bounds.max.x,bounds.max.y,bounds.max.z]
    for i in range(3):
        if abs(mins[i]-100*match['unreal_bounds_min_m'][i])>0.3 or abs(maxs[i]-100*match['unreal_bounds_max_m'][i])>0.3:
            raise RuntimeError('Scale/axis mismatch '+name+' '+str((mins,maxs)))
    report['bounds'][name]={'min_cm':mins,'max_cm':maxs}
    report['assets'].append(new_path)
if len(meshes)!=len(audit['modules']): raise RuntimeError('Incomplete modular import')

colors={'Plaster':(0.73,0.61,0.43),'Wood':(0.31,0.17,0.075),
        'Timber':(0.13,0.075,0.035),'Stone':(0.39,0.40,0.35),
        'Roof':(0.48,0.13,0.065),'Metal':(0.15,0.16,0.14),'Glass':(0.95,0.60,0.19)}
materials={}
for name,color in colors.items():
    mat=unreal.AssetToolsHelpers.get_asset_tools().create_asset('M_HH_'+name,DEST+'/Materials',unreal.Material,unreal.MaterialFactoryNew())
    node=unreal.MaterialEditingLibrary.create_material_expression(mat,unreal.MaterialExpressionConstant3Vector,0,0)
    node.set_editor_property('constant',unreal.LinearColor(*color,1))
    unreal.MaterialEditingLibrary.connect_material_property(node,'',unreal.MaterialProperty.MP_BASE_COLOR)
    rough=unreal.MaterialEditingLibrary.create_material_expression(mat,unreal.MaterialExpressionConstant,0,140)
    rough.set_editor_property('r',0.8)
    unreal.MaterialEditingLibrary.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS)
    if name=='Glass':
        unreal.MaterialEditingLibrary.connect_material_property(node,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    unreal.MaterialEditingLibrary.recompile_material(mat)
    materials[name]=mat
    report['assets'].append(DEST+'/Materials/M_HH_'+name)
for name,obj in meshes.items():
    for index,slot in enumerate(obj.get_editor_property('static_materials')):
        slotname=str(slot.get_editor_property('imported_material_slot_name'))
        if slotname not in materials: raise RuntimeError('Unknown material slot '+slotname)
        obj.set_material(index,materials[slotname])

cutaway=next(a for a in original if a.get_class().get_name()=='PokeMonsterBuildingCutaway')
healer=next(a for a in original if a.actor_has_tag('HealingHouse_Healer'))
report['healer_before']=[healer.get_actor_location().x,healer.get_actor_location().y,healer.get_actor_location().z]
placed={}
# Controlled comparison placement on the existing ground, with old shell still visible.
for name,obj in meshes.items():
    actor=actors.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(1200,0,0))
    actor.set_actor_label(name)
    actor.set_folder_path('HealingHouse/BlenderV1')
    actor.set_editor_property('tags',['HealingHouse_BlenderV1'])
    comp=actor.static_mesh_component
    comp.set_static_mesh(obj)
    comp.set_collision_profile_name('NoCollision')
    comp.set_cast_shadow(False)
    placed[name]=actor
report['comparison_offset_cm']=[1200,0,0]
# The imported floor, facade lines and counter must exactly match the original functional envelope.
assert report['bounds']['HH_Walls_Front']['min_cm'][0] < -450 < report['bounds']['HH_Walls_Front']['max_cm'][0]
assert report['bounds']['HH_Floor']['max_cm'][2] == 0
assert abs(report['bounds']['HH_Counter']['min_cm'][0]-173)<0.3
assert str(healer.get_editor_property('checkpoint_id'))=='Dev_HealingHouse'

# Preserve original blockers and furnishings; hide only superseded visual pieces.
for actor in original:
    if not isinstance(actor,unreal.StaticMeshActor): continue
    label=actor.get_actor_label()
    folder=str(actor.get_folder_path())
    superseded=any(folder.startswith('HealingHouse/'+p) for p in ('Body','Roof','Door','Windows'))
    superseded=superseded or label in ('InteriorFloor','HealingCounter','CounterTop')
    if superseded:
        actor.static_mesh_component.set_visibility(False,False)
        actor.set_editor_property('tags',list(actor.get_editor_property('tags'))+['HealingHouse_RetainedBlockout'])
for actor in placed.values(): actor.set_actor_location(unreal.Vector(0,0,0),False,False)
hidden_modules=['HH_Walls_Front','HH_Walls_CameraSide','HH_Gable_Front','HH_Roof_Main',
                'HH_Roof_Porch','HH_Timber_Front','HH_Timber_CameraSide',
                'HH_DoorFrame','HH_WindowFrames_Front','HH_WindowFrames_CameraSide',
                'HH_Glass_Front','HH_Glass_CameraSide','HH_Chimney','HH_ChimneyCap']
cutaway.set_editor_property('occluding_actors',list(cutaway.get_editor_property('occluding_actors'))+[placed[n] for n in hidden_modules])
report['cutaway_modules']=hidden_modules
# Read the actual player visual/collision size rather than rescaling the player to the model.
player=unreal.get_default_object(unreal.load_class(None,'/Script/PokeMonster.PokeMonsterPlayerCharacter'))
sprite=player.get_editor_property('sprite')
flipbook=unreal.load_asset('/Game/Characters/Prototype2D/Flipbooks/HobbitPlayer/FB_PlayerIdleDown')
if flipbook:
    frame=flipbook.get_sprite_at_frame(0)
    dim=frame.get_editor_property('source_dimension')
    ppu=frame.get_editor_property('pixels_per_unreal_unit')
    report['player_source_size_cm']=[dim.x/ppu,dim.y/ppu]
    # Existing BeginPlay uses 0.36; this is a read-only comparison, not a rescale.
    report['player_sprite_plane_height_cm']=dim.y/ppu*0.36
    report['player_visual_scale']=[0.36,0.36,0.36]
report['player_speed_cm_s']=player.get_editor_property('character_movement').max_walk_speed
report['healer_after']=[healer.get_actor_location().x,healer.get_actor_location().y,healer.get_actor_location().z]
assert report['healer_before']==report['healer_after']
assert report['player_speed_cm_s']==210
unreal.EditorAssetLibrary.save_directory(DEST,False,True)
if not unreal.EditorLoadingAndSavingUtils.save_map(world,MAP): raise RuntimeError('Map save failed')
(ART/'Review/UnrealImportAudit.json').write_text(json.dumps(report,indent=2)+'\n')
unreal.log('HH_IMPORT_SUCCESS meshes='+str(len(meshes)))
