"""Import the versioned art pass without altering any functional house actors.

Run in UnrealEditor-Cmd. V1 assets stay intact and V1 actors are only hidden.
All original placements/collision and cutaway parameters are checked unchanged.
New meshes use the existing blockout collision rather than whole-house hulls.
"""
import json
from pathlib import Path
import unreal

ROOT=Path(unreal.Paths.project_dir()).resolve()
ART=ROOT/'Art/HealingHouse'
REVIEW=ART/'Review/V2'
MAP='/Game/Maps/Dev_HealingHouseTestMap'
DEST='/Game/Environment/HealingHouse'
audit=json.loads((REVIEW/'GeometryAudit.json').read_text())
world=unreal.EditorLoadingAndSavingUtils.load_map(MAP)
if not world: raise RuntimeError('Existing test house map missing')
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
original=actors.get_all_level_actors()
if any(a.actor_has_tag('HealingHouse_BlenderV2') for a in original):
    raise RuntimeError('V2 already integrated; preserve completed work')
cutaway=next(a for a in original if a.get_class().get_name()=='PokeMonsterBuildingCutaway')
healer=next(a for a in original if a.actor_has_tag('HealingHouse_Healer'))

def signature():
    def xyz(v): return [v.x,v.y,v.z]
    return {a.get_path_name():{'location':xyz(a.get_actor_location()),
        'scale':xyz(a.get_actor_scale3d()),'rotation':[a.get_actor_rotation().pitch,a.get_actor_rotation().yaw,a.get_actor_rotation().roll],
        'collision':[(c.get_name(),str(c.get_collision_enabled()),
                      str(c.get_collision_response_to_channel(unreal.CollisionChannel.ECC_PAWN)),
                      str(c.get_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY)))
                     for c in a.get_components_by_class(unreal.PrimitiveComponent)]}
        for a in original}

before=signature()
threshold=cutaway.get_editor_property('door_threshold')
cut_before={'threshold':[threshold.get_world_location().x,threshold.get_world_location().y,threshold.get_world_location().z],
            'extent':[threshold.get_unscaled_box_extent().x,threshold.get_unscaled_box_extent().y,threshold.get_unscaled_box_extent().z],
            'fade':cutaway.get_editor_property('fade_duration'),
            'hysteresis':cutaway.get_editor_property('threshold_hysteresis')}
assert abs(cut_before['fade']-.4)<1e-6
names=('Plaster','Wood','Timber','Stone','Roof','Metal','Glass')
assettools=unreal.AssetToolsHelpers.get_asset_tools()
for name in names:
    if unreal.EditorAssetLibrary.does_asset_exist(DEST+'/Materials/M_HH_V2_'+name):
        raise RuntimeError('Preserve already imported V2 materials')

tasks=[]
for name in names:
    if unreal.EditorAssetLibrary.does_asset_exist(DEST+'/Textures/T_HH_V2_'+name): continue
    task=unreal.AssetImportTask()
    task.set_editor_property('filename',str(ART/'Textures/V2'/('T_HH_V2_'+name+'.png')))
    task.set_editor_property('destination_path',DEST+'/Textures')
    task.set_editor_property('automated',True)
    task.set_editor_property('save',True)
    task.set_editor_property('replace_existing',False)
    tasks.append(task)
assettools.import_asset_tasks(tasks)
library=unreal.MaterialEditingLibrary
function=unreal.load_asset('/Engine/Functions/Engine_MaterialFunctions02/Utility/DitherTemporalAA')
materials={}
asset_paths=[]
for name in names:
    tex=unreal.load_asset(DEST+'/Textures/T_HH_V2_'+name)
    if not tex: raise RuntimeError('Texture import failed: '+name)
    tex.set_editor_property('srgb',True)
    mat=assettools.create_asset('M_HH_V2_'+name,DEST+'/Materials',unreal.Material,unreal.MaterialFactoryNew())
    sample=library.create_material_expression(mat,unreal.MaterialExpressionTextureSample,-620,-100)
    sample.set_editor_property('texture',tex)
    library.connect_material_property(sample,'RGB',unreal.MaterialProperty.MP_BASE_COLOR)
    rough=library.create_material_expression(mat,unreal.MaterialExpressionConstant,-360,80)
    rough.set_editor_property('r',.82)
    library.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS)
    spec=library.create_material_expression(mat,unreal.MaterialExpressionConstant,-360,170)
    spec.set_editor_property('r',.12)
    library.connect_material_property(spec,'',unreal.MaterialProperty.MP_SPECULAR)
    if name=='Glass':
        glow=library.create_material_expression(mat,unreal.MaterialExpressionMultiply,-330,-160)
        glow.set_editor_property('const_b',.25)
        library.connect_material_expressions(sample,'RGB',glow,'A')
        library.connect_material_property(glow,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    fade=library.create_material_expression(mat,unreal.MaterialExpressionScalarParameter,-600,420)
    fade.set_editor_property('parameter_name','HouseCutaway')
    fade.set_editor_property('default_value',0)
    fade.set_editor_property('use_custom_primitive_data',True)
    fade.set_editor_property('primitive_data_index',0)
    visible=library.create_material_expression(mat,unreal.MaterialExpressionOneMinus,-360,420)
    dither=library.create_material_expression(mat,unreal.MaterialExpressionMaterialFunctionCall,-140,420)
    dither.set_editor_property('material_function',function)
    alpha=next(str(n) for n in library.get_material_expression_input_names(dither) if 'alpha' in str(n).lower())
    library.connect_material_expressions(fade,'',visible,str(library.get_material_expression_input_names(visible)[0]))
    library.connect_material_expressions(visible,'',dither,alpha)
    library.connect_material_property(dither,'',unreal.MaterialProperty.MP_OPACITY_MASK)
    mat.set_editor_property('blend_mode',unreal.BlendMode.BLEND_MASKED)
    library.recompile_material(mat)
    materials['HH_V2_'+name]=mat
    asset_paths += [tex.get_path_name(),mat.get_path_name()]

ui=unreal.FbxImportUI()
for prop,value in {'import_mesh':True,'import_materials':False,'import_textures':False,
                   'import_as_skeletal':False,'automated_import_should_detect_type':False,
                   'mesh_type_to_import':unreal.FBXImportType.FBXIT_STATIC_MESH}.items():
    ui.set_editor_property(prop,value)
for prop,value in {'combine_meshes':False,'auto_generate_collision':False,
                  'transform_vertex_to_absolute':True,'bake_pivot_in_vertex':False,
                  'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':False,
                  'import_uniform_scale':1}.items():
    ui.static_mesh_import_data.set_editor_property(prop,value)
task=unreal.AssetImportTask()
for prop,value in {'filename':str(ART/'Exports/HealingHouse_V2.fbx'),
                  'destination_path':DEST+'/Meshes','automated':True,'save':True,
                  'replace_existing':False,'options':ui}.items(): task.set_editor_property(prop,value)
existing=[DEST+'/Meshes/SM_'+m['name'] for m in audit['modules']]
if not all(unreal.EditorAssetLibrary.does_asset_exist(p) for p in existing):
    if any(unreal.EditorAssetLibrary.does_asset_exist(p) for p in existing): raise RuntimeError('Partial mesh import requires inspection')
    assettools.import_asset_tasks([task])
    existing=list(task.get_editor_property('imported_object_paths'))
meshes={}
report={'source_head':'8705b16','map':MAP,'assets':asset_paths,'bounds':{},
        'cutaway_before':cut_before,'triangles':audit['total_triangles']}
for path in existing:
    obj=unreal.load_asset(path)
    if not isinstance(obj,unreal.StaticMesh): continue
    entry=next((m for m in audit['modules'] if obj.get_name().endswith(m['name'])),None)
    if not entry: raise RuntimeError('Unexpected mesh '+obj.get_name())
    name=entry['name']
    dest=DEST+'/Meshes/SM_'+name
    if obj.get_path_name().split('.')[0]!=dest:
        if not unreal.EditorAssetLibrary.rename_asset(obj.get_path_name(),dest): raise RuntimeError('Rename failed '+name)
    bounds=obj.get_bounding_box()
    mins=[bounds.min.x,bounds.min.y,bounds.min.z];maxs=[bounds.max.x,bounds.max.y,bounds.max.z]
    for i in range(3):
        if abs(mins[i]-100*entry['unreal_bounds_min_m'][i])>.3 or abs(maxs[i]-100*entry['unreal_bounds_max_m'][i])>.3:
            raise RuntimeError('Scale or handedness mismatch '+name)
    for index,slot in enumerate(obj.get_editor_property('static_materials')):
        slotname=str(slot.get_editor_property('imported_material_slot_name'))
        if slotname not in materials: raise RuntimeError('Unexpected material '+slotname)
        obj.set_material(index,materials[slotname])
    meshes[name]=obj
    report['assets'].append(dest)
    report['bounds'][name]={'min_cm':mins,'max_cm':maxs}
if len(meshes)!=len(audit['modules']): raise RuntimeError('Incomplete modular import')
assert abs(report['bounds']['HH_V2_Counter']['min_cm'][0]-173)<.3
assert abs(report['bounds']['HH_V2_Counter']['max_cm'][2]-92)<.3
assert report['bounds']['HH_V2_Floor']['max_cm'][2]==0

placed={}
for name,obj in meshes.items():
    actor=actors.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(0,0,0))
    actor.set_actor_label(name)
    actor.set_folder_path('HealingHouse/BlenderV2')
    actor.set_editor_property('tags',['HealingHouse_BlenderV2'])
    comp=actor.static_mesh_component
    comp.set_static_mesh(obj)
    comp.set_collision_profile_name('NoCollision')
    comp.set_cast_shadow(False)
    placed[name]=actor
hidden=('Walls_Front','Walls_CameraSide','Gable_Front','Glass_Front','Glass_CameraSide',
        'Glass_Loft','Windows_Front','Windows_CameraSide','Windows_Loft','Roof_Main',
        'Roof_Trim','Roof_Porch','Roof_Entry','Timber_Front','Timber_CameraSide',
        'Timber_Entry','DoorFrame','DoorLeaf','Stone_Front','Stone_CameraSide',
        'Chimney','ChimneyCap','InteriorBeams_CameraSide')
occluders=[placed['HH_V2_'+n] for n in hidden]
cutaway.set_editor_property('occluding_actors',list(cutaway.get_editor_property('occluding_actors'))+occluders)
for a in original:
    if a.actor_has_tag('HealingHouse_BlenderV1'):
        a.static_mesh_component.set_visibility(False,False)
        a.set_editor_property('tags',list(a.get_editor_property('tags'))+['HealingHouse_RetainedV1'])
report['cutaway_modules']=[a.get_actor_label() for a in occluders]
if before!=signature():
    (REVIEW/'UnexpectedChanges.json').write_text(json.dumps({'before':before,'after':signature()},indent=2))
    raise RuntimeError('Original actor placements/collision changed')
cut_after={'threshold':[threshold.get_world_location().x,threshold.get_world_location().y,threshold.get_world_location().z],
           'extent':[threshold.get_unscaled_box_extent().x,threshold.get_unscaled_box_extent().y,threshold.get_unscaled_box_extent().z],
           'fade':cutaway.get_editor_property('fade_duration'),
           'hysteresis':cutaway.get_editor_property('threshold_hysteresis')}
if cut_before!=cut_after: raise RuntimeError('Cutaway timing or threshold changed')
report['original_actor_placements_and_collision_unchanged']=True
report['cutaway_after']=cut_after
unreal.EditorAssetLibrary.save_directory(DEST,True,True)
if not unreal.EditorLoadingAndSavingUtils.save_map(world,MAP): raise RuntimeError('Map save failed')
(REVIEW/'UnrealImportAudit.json').write_text(json.dumps(report,indent=2)+'\n')
unreal.SystemLibrary.execute_console_command(world,'MAP CHECK')
unreal.log('HH_V2_IMPORT_SUCCESS modules='+str(len(meshes))+' tris='+str(audit['total_triangles']))
