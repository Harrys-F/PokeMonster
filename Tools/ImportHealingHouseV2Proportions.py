"""Update only proportion-changed V2 meshes and necessary map dimensions.

Materials/gameplay are preserved; existing collision profiles remain active.
"""
import unreal
import json
from pathlib import Path

ROOT = Path(unreal.Paths.project_dir()).resolve()
ART = ROOT/'Art/HealingHouse'
REVIEW = ART/'Review/V2/Proportions'
MAP = '/Game/Maps/Dev_HealingHouseTestMap'
DEST = '/Game/Environment/HealingHouse/Meshes'
world = unreal.EditorLoadingAndSavingUtils.load_map(MAP)
assert world
subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = subsystem.get_all_level_actors()
cutaway = next(a for a in actors if a.get_class().get_name()=='PokeMonsterBuildingCutaway')
threshold = cutaway.get_editor_property('door_threshold')
assert threshold.get_unscaled_box_extent().y == 120, 'Already adjusted; inspect before repeating.'
audit = json.loads((ART/'Review/V2/GeometryAudit.json').read_text())
asset_before = set(map(str,unreal.EditorAssetLibrary.list_assets(DEST,True,False)))

def signature(a):
    p,s,r = a.get_actor_location(),a.get_actor_scale3d(),a.get_actor_rotation()
    return {'label':a.get_actor_label(),'position':[p.x,p.y,p.z],'scale':[s.x,s.y,s.z],
        'rotation':[r.pitch,r.yaw,r.roll],
        'collision':[(c.get_name(),str(c.get_collision_enabled()),
            str(c.get_collision_response_to_channel(unreal.CollisionChannel.ECC_PAWN)),
            str(c.get_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY)))
            for c in a.get_components_by_class(unreal.PrimitiveComponent)]}
before = {a.get_path_name():signature(a) for a in actors}
materials = {}
for name in audit['proportion_changed_modules']:
    mesh = unreal.load_asset(DEST+'/SM_'+name)
    assert mesh
    materials[name] = [(str(slot.get_editor_property('imported_material_slot_name')),
                        slot.get_editor_property('material_interface'))
                       for slot in mesh.get_editor_property('static_materials')]
tasks = []
for name in audit['proportion_changed_modules']:
    ui = unreal.FbxImportUI()
    for prop,value in {'import_mesh':True,'import_materials':False,'import_textures':False,
        'import_as_skeletal':False,'automated_import_should_detect_type':False,
        'mesh_type_to_import':unreal.FBXImportType.FBXIT_STATIC_MESH}.items():
        ui.set_editor_property(prop,value)
    for prop,value in {'combine_meshes':True,'auto_generate_collision':False,
        'transform_vertex_to_absolute':True,'bake_pivot_in_vertex':False,
        'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':False,
        'import_uniform_scale':1}.items(): ui.static_mesh_import_data.set_editor_property(prop,value)
    task = unreal.AssetImportTask()
    for prop,value in {'filename':str(ART/'Exports/V2Modules'/('SM_'+name+'.fbx')),
        'destination_path':DEST,'destination_name':'SM_'+name,'automated':True,
        'save':False,'replace_existing':True,'replace_existing_settings':True,'options':ui}.items():
        task.set_editor_property(prop,value)
    tasks.append(task)
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
bounds_report = {}
for name in audit['proportion_changed_modules']:
    mesh = unreal.load_asset(DEST+'/SM_'+name)
    assert mesh
    for i,slot in enumerate(mesh.get_editor_property('static_materials')):
        imported_name = str(slot.get_editor_property('imported_material_slot_name'))
        material = next((mat for slot_name,mat in materials[name] if slot_name==imported_name),None)
        assert material, (name,imported_name)
        mesh.set_material(i,material)
    entry = next(m for m in audit['modules'] if m['name']==name)
    bounds = mesh.get_bounding_box()
    mins,maxs = [bounds.min.x,bounds.min.y,bounds.min.z],[bounds.max.x,bounds.max.y,bounds.max.z]
    for i in range(3):
        assert abs(mins[i]-100*entry['unreal_bounds_min_m'][i])<.3, (name,mins)
        assert abs(maxs[i]-100*entry['unreal_bounds_max_m'][i])<.3, (name,maxs)
    bounds_report[name] = {'min_cm':mins,'max_cm':maxs}
    assert unreal.EditorAssetLibrary.save_loaded_asset(mesh)
assert asset_before == set(map(str,unreal.EditorAssetLibrary.list_assets(DEST,True,False))), 'Unexpected new asset hierarchy'

changed_actors = []
for a in actors:
    name = a.get_actor_label()
    p,s = a.get_actor_location(),a.get_actor_scale3d()
    change = False
    if a.actor_has_tag('HealingHouse_EntranceWall'):
        p.y = 260 if p.y>0 else -260; s.y=3.5;change=True
    elif name=='DoorLintel':
        p.z=237.5;s.y=1.7;s.z=.45;change=True
    elif name=='RearWall': s.y=8.7;change=True
    elif name in ('FarSideWall','CameraSideWall'):
        p.y=435 if p.y>0 else -435;change=True
    elif name=='InteriorFloor': s.y=8.4;change=True
    elif name=='SupplyShelf' or name.startswith('HerbPot_'):
        p.y += 50;change=True
    if change:
        a.set_actor_location(p,False,False)
        a.set_actor_scale3d(s)
        changed_actors.append(name)
threshold.set_relative_location(unreal.Vector(-410,0,-42.5),False,True)
threshold.set_box_extent(unreal.Vector(20,85,107.5),False)
cutaway.get_editor_property('interior_area').set_box_extent(unreal.Vector(490,435,250),False)
assert abs(cutaway.get_editor_property('fade_duration')-.4)<1e-6
assert cutaway.get_editor_property('threshold_hysteresis')==4
for a in actors:
    after = signature(a)
    old = before[a.get_path_name()]
    assert old['collision']==after['collision'], 'Collision profile changed: '+a.get_actor_label()
    if a.get_actor_label() not in changed_actors:
        assert old==after, 'Unexpected actor change: '+a.get_actor_label()
assert unreal.EditorLoadingAndSavingUtils.save_map(world,MAP)
report = {'changed_meshes':audit['proportion_changed_modules'],'bounds':bounds_report,
    'changed_map_actors':changed_actors,'all_collision_profiles_preserved':True,
    'all_other_actor_transforms_preserved':True,'threshold_cm':[40,170,215],
    'threshold_centre_cm':[-450,0,107.5],'fade_seconds':.4,
    'counter_moved':False,'healer_moved':False,'no_additional_assets':True}
(REVIEW/'UnrealChanges.json').write_text(json.dumps(report,indent=2)+'\n')
unreal.SystemLibrary.execute_console_command(world,'MAP CHECK')
unreal.log('HEALING_HOUSE_PROPORTIONS_IMPORTED '+str(len(tasks)))
