"""V3 scene dressing after the saved/reopened Blender source and front PIE gate.

Only the healing-house map/new V3 assets are saved. All gameplay actor settings
and the already approved doorway/camera remain unchanged. Small props stay
independently editable; none of the decorations are interaction actors.
"""
import unreal, json, math
from pathlib import Path

ROOT=Path(unreal.Paths.project_dir()).resolve()
ART=ROOT/'Art/HealingHouse'; REVIEW=ART/'Review/V3/Dressing'
DEST='/Game/Environment/HealingHouse/V3'
MAP='/Game/Maps/Dev_HealingHouseTestMap'
assert json.loads((ART/'Review/V3/Front/PIEGate.json').read_text())['phase1_passed']
world=unreal.EditorLoadingAndSavingUtils.load_map(MAP)
assert world
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
original=actors.get_all_level_actors()
assert not any(a.actor_has_tag('HealingHouse_V3') for a in original)
cutaway=next(a for a in original if a.get_class().get_name()=='PokeMonsterBuildingCutaway')
healer=next(a for a in original if a.actor_has_tag('HealingHouse_Healer'))
healer_before=healer.get_actor_transform()
threshold=cutaway.get_editor_property('door_threshold')
assert threshold.get_unscaled_box_extent()==unreal.Vector(20,75,107.5)
assert abs(cutaway.get_editor_property('fade_duration')-.4)<1e-6
assettools=unreal.AssetToolsHelpers.get_asset_tools()
lib=unreal.MaterialEditingLibrary
function=unreal.load_asset('/Engine/Functions/Engine_MaterialFunctions02/Utility/DitherTemporalAA')
materials={n:unreal.load_asset('/Game/Environment/HealingHouse/Materials/M_HH_V2_'+n)
           for n in ('Wood','Timber','Metal','Glass','Stone')}
colors={'Linen':(.64,.60,.45),'Sage':(.23,.36,.25),'Ochre':(.49,.32,.16),
        'Cream':(.88,.77,.49),'Lamp':(.95,.54,.18),'Herb':(.14,.28,.14),
        'Flower':(.55,.32,.38),'Bottle':(.16,.32,.30),'Book':(.24,.29,.40)}
assets=[]
for name,color in colors.items():
    path=DEST+'/Materials/M_HH_V3_'+name
    assert not unreal.EditorAssetLibrary.does_asset_exist(path)
    mat=assettools.create_asset('M_HH_V3_'+name,DEST+'/Materials',unreal.Material,unreal.MaterialFactoryNew())
    tint=lib.create_material_expression(mat,unreal.MaterialExpressionConstant3Vector,-600,0)
    tint.set_editor_property('constant',unreal.LinearColor(*color,1))
    lib.connect_material_property(tint,'',unreal.MaterialProperty.MP_BASE_COLOR)
    rough=lib.create_material_expression(mat,unreal.MaterialExpressionConstant,-300,100)
    rough.set_editor_property('r',.88)
    lib.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS)
    spec=lib.create_material_expression(mat,unreal.MaterialExpressionConstant,-300,170)
    spec.set_editor_property('r',.08)
    lib.connect_material_property(spec,'',unreal.MaterialProperty.MP_SPECULAR)
    if name=='Lamp':
        glow=lib.create_material_expression(mat,unreal.MaterialExpressionMultiply,-300,-130)
        glow.set_editor_property('const_b',.65)
        lib.connect_material_expressions(tint,'',glow,'A')
        lib.connect_material_property(glow,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    fade=lib.create_material_expression(mat,unreal.MaterialExpressionScalarParameter,-600,420)
    fade.set_editor_property('parameter_name','HouseCutaway')
    fade.set_editor_property('default_value',0)
    fade.set_editor_property('use_custom_primitive_data',True)
    fade.set_editor_property('primitive_data_index',0)
    visible=lib.create_material_expression(mat,unreal.MaterialExpressionOneMinus,-360,420)
    dither=lib.create_material_expression(mat,unreal.MaterialExpressionMaterialFunctionCall,-140,420)
    dither.set_editor_property('material_function',function)
    alpha=next(str(n) for n in lib.get_material_expression_input_names(dither) if 'alpha' in str(n).lower())
    lib.connect_material_expressions(fade,'',visible,str(lib.get_material_expression_input_names(visible)[0]))
    lib.connect_material_expressions(visible,'',dither,alpha)
    lib.connect_material_property(dither,'',unreal.MaterialProperty.MP_OPACITY_MASK)
    mat.set_editor_property('blend_mode',unreal.BlendMode.BLEND_MASKED)
    lib.recompile_material(mat)
    materials[name]=mat; assets.append(path)

audit=json.loads((REVIEW/'PropAudit.json').read_text())
tasks=[]
fixed={'TreatmentBedSmall','TreatmentBedLarge','HerbShelf','Bookcase','HerbTable'}
for name,entry in audit.items():
    ui=unreal.FbxImportUI()
    for p,v in {'import_mesh':True,'import_materials':False,'import_textures':False,
                'import_as_skeletal':False,'automated_import_should_detect_type':False,
                'mesh_type_to_import':unreal.FBXImportType.FBXIT_STATIC_MESH}.items():ui.set_editor_property(p,v)
    for p,v in {'combine_meshes':True,'auto_generate_collision':name in fixed,
                'transform_vertex_to_absolute':True,'bake_pivot_in_vertex':False,
                'convert_scene':True,'convert_scene_unit':True,'import_uniform_scale':1}.items():
        ui.static_mesh_import_data.set_editor_property(p,v)
    task=unreal.AssetImportTask()
    for p,v in {'filename':str(ART/'Exports/V3Modules'/('SM_'+entry['name']+'.fbx')),
                'destination_path':DEST+'/Meshes','destination_name':'SM_'+entry['name'],
                'automated':True,'save':False,'replace_existing':False,'options':ui}.items():task.set_editor_property(p,v)
    tasks.append(task)
assettools.import_asset_tasks(tasks)
meshes={}
for name,entry in audit.items():
    path=DEST+'/Meshes/SM_'+entry['name'];mesh=unreal.load_asset(path);assert mesh
    for i,slot in enumerate(mesh.get_editor_property('static_materials')):
        slotname=str(slot.get_editor_property('imported_material_slot_name'))
        matname=slotname.removeprefix('HH_V2_').removeprefix('HH_V3_')
        assert matname in materials,(name,slotname)
        mesh.set_material(i,materials[matname])
    bounds=mesh.get_bounding_box();size=bounds.max-bounds.min
    for actual,expected in zip((size.x,size.y,size.z),entry['size_cm']):assert abs(actual-expected)<.3,(name,size)
    mesh.get_editor_property('asset_import_data').scripted_add_filename(str(ART/'Exports/V3Modules'/('SM_'+entry['name']+'.fbx')),0,'')
    meshes[name]=mesh;assets.append(path)

new=[];occluders=[]
def spawn(cls,name,p,folder='Interior',rotation=(0,0,0)):
    a=actors.spawn_actor_from_class(cls,unreal.Vector(*p),unreal.Rotator(pitch=rotation[0],yaw=rotation[1],roll=rotation[2]))
    a.set_actor_label('HH_V3_'+name);a.set_folder_path('HealingHouse/V3/'+folder)
    a.set_editor_property('tags',['HealingHouse_V3']);new.append(a);return a
def meshactor(name,p,mesh,material=None,size=None,block=False,hide=False,folder='Interior',rotation=(0,0,0)):
    a=spawn(unreal.StaticMeshActor,name,p,folder,rotation);c=a.static_mesh_component
    c.set_static_mesh(mesh)
    if material:c.set_material(0,materials[material])
    if size:a.set_actor_scale3d(unreal.Vector(*(v/100 for v in size)))
    c.set_cast_shadow(False);c.set_collision_profile_name('BlockAll' if block else 'NoCollision')
    c.set_editor_property('generate_overlap_events',False)
    if block:c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_IGNORE)
    if block:a.set_editor_property('tags',list(a.get_editor_property('tags'))+['HealingHouse_V3_Furniture'])
    else:a.set_editor_property('tags',list(a.get_editor_property('tags'))+['HealingHouse_V3_Decoration'])
    if hide:occluders.append(a)
    return a
basic={n:unreal.load_asset('/Engine/BasicShapes/'+n) for n in ('Cube','Cylinder','Sphere')}
def cube(name,p,size,mat='Wood',**kw):return meshactor(name,p,basic['Cube'],mat,size,**kw)
def cyl(name,p,size,mat='Wood',**kw):return meshactor(name,p,basic['Cylinder'],mat,size,**kw)
def orb(name,p,size,mat='Herb',**kw):return meshactor(name,p,basic['Sphere'],mat,size,**kw)
for name,entry in audit.items():
    exterior=name in ('SignBracket','GuardianSign','Lantern')
    meshactor(name,entry['unreal_location_cm'],meshes[name],block=name in fixed,
              hide=exterior,folder='Exterior' if exterior else 'Interior')

# Existing blockout furniture is retained but its visual and collision are
# replaced by the visible V3 furniture, avoiding duplicate invisible blockers.
replaced=[]
for a in original:
    label=a.get_actor_label()
    if label in ('RestBed_-50','RestBed_170','RestBedCover_-50','RestBedCover_170',
                 'SupplyShelf','SpareCreatureBed') or label.startswith('HerbPot_'):
        c=a.static_mesh_component;c.set_visibility(False,False);c.set_collision_profile_name('NoCollision')
        a.set_editor_property('tags',list(a.get_editor_property('tags'))+['HealingHouse_V3_ReplacedBlockout'])
        replaced.append(label)

def sprite(name,p,asset,scale,folder='Exterior'):
    a=spawn(unreal.PaperSpriteActor,name,p,folder,(0,45,-55));c=a.get_editor_property('render_component')
    c.set_mobility(unreal.ComponentMobility.MOVABLE)
    sprite_asset=unreal.load_asset('/Game/Environment/Prototype2D/Details/'+asset)
    assert sprite_asset and c.set_sprite(sprite_asset)
    c.set_mobility(unreal.ComponentMobility.STATIC)
    c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False)
    a.set_actor_scale3d(unreal.Vector(scale,scale,scale))
    a.set_editor_property('tags',list(a.get_editor_property('tags'))+['HealingHouse_V3_Decoration'])
    return a
def bottle(name,p,height=22):
    x,y,z=p
    cyl(name+'_Body',(x,y,z+height*.32),(height*.42,height*.42,height*.64),'Bottle')
    cyl(name+'_Neck',(x,y,z+height*.78),(height*.18,height*.18,height*.30),'Bottle')
    cyl(name+'_Cork',(x,y,z+height*.96),(height*.20,height*.20,height*.10),'Ochre')
def pot(name,p,scale=1,hide=False,folder='Interior',flowers=False):
    x,y,z=p
    cyl(name+'_Pot',(x,y,z+9*scale),(21*scale,21*scale,18*scale),'Ochre',hide=hide,folder=folder)
    for j,(dx,dy,dz) in enumerate(((-6,0,25),(5,3,28),(0,-4,30))):
        orb(name+'_Leaf'+str(j),(x+dx*scale,y+dy*scale,z+dz*scale),(15*scale,13*scale,23*scale),hide=hide,folder=folder)
    if flowers:
        orb(name+'_Flower',(x,y,z+39*scale),(12*scale,12*scale,9*scale),'Flower',hide=hide,folder=folder)

# Paired window boxes retain the established calm frontal balance.
for side in (-1,1):
    y=side*275
    cube('WindowBox_'+str(side),(-481,y,92),(25,116,19),'Wood',hide=True,folder='Exterior')
    cube('WindowBoxSoil_'+str(side),(-481,y,103),(20,105,3),'Ochre',hide=True,folder='Exterior')
    for j in range(4):pot('WindowHerb_'+str(side)+'_'+str(j),(-488,y-40+j*27,105),.72,True,'Exterior',j%2==0)
    # Sparse climbing leaves follow outer corner posts, never the central door.
    for j in range(7):
        orb('Ivy_'+str(side)+'_'+str(j),(-473,side*(390+math.sin(j*1.5)*15),85+j*21),
            (7,25,18),hide=True,folder='Exterior')

# Small porch supplies, deliberately outside the door and central approach.
for i,(x,y) in enumerate(((-375,-520),(-333,-552))):
    cyl('Barrel_'+str(i),(x,y,26),(39,39,52),'Wood',folder='Exterior')
    for z in (11,41):cyl('BarrelHoop_'+str(i)+'_'+str(z),(x,y,z),(41,41,3),'Metal',folder='Exterior')
cube('SupplyCrate',(-470,-562,18),(42,42,36),'Wood',folder='Exterior')
for j in range(5):
    cyl('PorchLog_'+str(j),(-270,-565+(j%3)*17,13+(j//3)*17),(15,15,80),
        'Wood',folder='Exterior',rotation=(0,0,90))
for i,(x,y,s) in enumerate(((-635,-325,.35),(-722,-375,.42),(-930,335,.43),
                           (-1100,-280,.32),(-470,535,.46),(-305,510,.38),
                           (-120,515,.37),(230,510,.40),(-560,-645,.40))):
    sprite('FlowerPatch_'+str(i),(x,y,2),'S_Wildflowers',s)
for i,(x,y,s) in enumerate(((-795,-360,.38),(-1030,360,.45),(-1160,-240,.32),
                           (-620,395,.30),(-350,540,.40),(60,535,.40),(-545,-610,.37))):
    sprite('GrassPatch_'+str(i),(x,y,2),'S_GrassCluster',s)
for i,(x,y) in enumerate(((-880,-300),(-690,325),(-120,535),(-500,-610))):
    sprite('MossStones_'+str(i),(x,y,2),'S_MossStones',.30)
for i,(x,y,z,sz) in enumerate(((-980,-210,1,(42,30,3)),(-905,-235,1,(32,24,3)),
                             (-745,235,1,(38,28,3)),(-610,270,1,(34,26,3)))):
    orb('PathStone_'+str(i),(x,y,z),sz,'Stone',folder='Exterior')

# Independently editable shelf contents, work materials and seating.
for i,x in enumerate((-208,-194,-179,-159,-145)):
    for level,z in enumerate((16,62,110)):
        cube('ShelfBook_'+str(i)+'_'+str(level),(x,-383,z+13),(8,24,26),
             ('Book','Ochre','Sage')[(i+level)%3],rotation=(0,(i%3-1)*5,0))
for i,(x,z) in enumerate(((90,16),(125,16),(170,62),(195,62),(110,110),(205,110))):
    bottle('ShelfVial_'+str(i),(x,-380,z),18+(i%3)*3)
for i,x in enumerate((110,165,205)):pot('ShelfHerb_'+str(i),(x,-383,174),.70)
for i,x in enumerate((-285,-245)):
    pot('TableHerb_'+str(i),(x,315,84),.60)
bottle('WorkVial',(-228,301,84),18)
cube('TreatmentCloth',(-266,300,86),(27,24,3),'Linen')
for i in range(3):cube('CounterBook_'+str(i),(222,-225,94+i*5),(27-i*3,19,4),'Book' if i==1 else 'Ochre')
bottle('CounterVial',(220,38,94),18)
cube('CounterBandage',(217,2,96),(24,16,5),'Linen')
cyl('CounterBowl',(221,-182,100),(25,25,10),'Cream')

# A compact rear-side sitting nook, away from the healer approach.
cube('NookTableTop',(355,239,66),(80,70,8),'Wood',block=True)
for x in (326,384):
    for y in (215,262):cube('NookTableLeg_'+str(x)+'_'+str(y),(x,y,31),(8,8,62),'Timber')
cube('NookBenchSeat',(348,305,38),(94,30,8),'Wood',block=True)
for x in (313,383):cube('NookBenchLeg_'+str(x),(x,305,17),(8,23,34),'Timber')
cube('NookBenchBack',(348,321,66),(94,7,44),'Timber')
cube('ReadingBook',(351,237,72),(28,22,4),'Cream')
cube('AisleRug',(-62,15,1.2),(250,205,1.2),'Sage')
for y in (-81,111):cube('RugBorder_'+str(y),(-62,y,2),(240,3,1),'Cream')
for x in (-177,53):cube('RugBorder_'+str(x),(x,15,2),(3,188,1),'Cream')
for j in range(3):orb('DriedHerbBundle_'+str(j),(370,-409,148+j*18),(17,5,26),'Herb')

# Soft, shadow-free pools of warm light; restrained enough to preserve colors.
light_report=[]
for name,p,intensity,radius in [('EntranceGlow',[-550,-130,192],140,280),
                              ('CounterGlow',[160,-120,205],220,430),
                              ('RestAreaGlow',[-30,300,180],140,330)]:
    a=spawn(unreal.PointLight,name,p,'Lighting');c=a.point_light_component
    c.set_editor_property('intensity',intensity);c.set_editor_property('attenuation_radius',radius)
    c.set_editor_property('light_color',unreal.Color(255,211,159,255))
    c.set_editor_property('use_inverse_squared_falloff',False)
    c.set_editor_property('source_radius',45);c.set_cast_shadows(False)
    light_report.append({'name':name,'intensity':intensity,'radius_cm':radius,'shadows':False})
for i,p in enumerate(((164,-120,195),(-27,335,177))):
    meshactor('InteriorLantern_'+str(i),p,meshes['Lantern'])

cutaway.set_editor_property('occluding_actors',list(cutaway.get_editor_property('occluding_actors'))+occluders)
assert healer.get_actor_transform()==healer_before
assert threshold.get_unscaled_box_extent()==unreal.Vector(20,75,107.5)
assert abs(cutaway.get_editor_property('fade_duration')-.4)<1e-6
assert cutaway.get_editor_property('threshold_hysteresis')==4
assert unreal.EditorAssetLibrary.save_directory(DEST,True,True)
assert unreal.EditorLoadingAndSavingUtils.save_map(world,MAP)
report={'new_assets':assets,'new_actors':[a.get_actor_label() for a in new],
        'replaced_blockout':replaced,'new_cutaway_actors':[a.get_actor_label() for a in occluders],
        'fixed_furniture_collision':sorted(fixed),'all_small_decorations_no_collision':True,
        'healer_transform_preserved':True,'counter_preserved':True,'threshold_preserved':True,
        'lighting':light_report,'no_gameplay_changes':True}
(REVIEW/'UnrealDressingAudit.json').write_text(json.dumps(report,indent=2)+'\n')
unreal.SystemLibrary.execute_console_command(world,'MAP CHECK')
unreal.log('HEALING_HOUSE_V3_DRESSING_OK actors='+str(len(new)))
