"""One-time V3 reference polish in the existing Healing House testmap.
Retained furniture collision stays on original actors; new visuals are separate.
"""
import unreal,json,math,random,re
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();H='/Game/Environment/HealingHouse/QualityV3'
OUT=ROOT/'Saved/HealingQualityV3';OUT.mkdir(parents=True,exist_ok=True)
ed=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);world=ed.get_editor_world()
assert world.get_name()=='Dev_HealingHouseTestMap' and not ed.get_game_world()
actorlib=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors=actorlib.get_all_level_actors();by={a.get_actor_label():a for a in actors}
assert not any(n.startswith('HH_Q3_') for n in by), 'Already dressed; do not rebuild'
cut=by['HouseCutaway'];occ=list(cut.get_editor_property('occluding_actors'));original_occ=[a.get_actor_label() for a in occ]
healer=by['HouseHealer'].get_actor_transform();changes=[];new=[];colliders=[]
catalog=json.loads((ROOT/'Art/HealingHouse/QualityV3/Props.json').read_text())
assert all(unreal.load_asset(H+'/Meshes/SM_HH_Q3_'+name) for name in catalog)
def spawn(label,name,pos,yaw=0,scale=(1,1,1),front=False):
    mesh=unreal.load_asset(H+'/Meshes/SM_HH_Q3_'+name);assert mesh,name
    a=actorlib.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*pos),unreal.Rotator(yaw=yaw))
    a.set_actor_label('HH_Q3_'+label);a.set_folder_path('HealingHouse/QualityV3')
    a.tags=['HealingHouse_QualityV3'];a.set_actor_scale3d(unreal.Vector(*scale))
    c=a.static_mesh_component;c.set_static_mesh(mesh);c.set_collision_profile_name('NoCollision')
    c.set_editor_property('cast_shadow',not name.startswith(('Broad','Narrow','Leaf','Flower','Trailing','Hanging','HerbBundle')))
    if front:occ.append(a)
    new.append({'actor':a.get_actor_label(),'mesh':name,'position_cm':pos,'scale':scale,'front_occluder':front})
    return a
def replace(a,name):
    c=a.static_mesh_component;original=c.static_mesh
    if c.get_collision_enabled()!=unreal.CollisionEnabled.NO_COLLISION:
        # Keep the original blocking geometry byte-identical. Visibility is visual
        # state only and does not disable its gameplay collision.
        p=a.get_actor_location();r=a.get_actor_rotation();scale=a.get_actor_scale3d()
        visual=spawn('Visual_'+a.get_actor_label(),name,[p.x,p.y,p.z],r.yaw,[scale.x,scale.y,scale.z])
        c.set_visibility(False);a.set_actor_hidden_in_game(True)
        colliders.append({'actor':a.get_actor_label(),'original_mesh':original.get_path_name(),'visual':visual.get_actor_label()})
    else:
        c.set_static_mesh(unreal.load_asset(H+'/Meshes/SM_HH_Q3_'+name))
        for i in range(c.get_num_materials()):c.set_material(i,None)
    changes.append({'actor':a.get_actor_label(),'old_mesh':original.get_path_name(),'new_visual':name})

mapping={'HH_Art_Reception':'CounterStepped','HH_Art_BenchWaiting':'Bench','HH_Art_BenchCompanion':'Bench',
         'HH_Art_TableWaiting':'Table','HH_V3_HerbTable':'HerbTable',
         'HH_V3_Bookcase':'Bookcase','HH_V3_HerbShelf':'HerbShelf',
         'HH_Art_RearApothecary_0':'Bookcase','HH_Art_RearApothecary_1':'Bookcase',
         'HH_V3_TreatmentBedSmall':'TreatmentBedSmall','HH_V3_TreatmentBedLarge':'TreatmentBedLarge',
         'HH_V3_GuardianSign':'GuardianSign'}
for label,name in mapping.items():replace(by[label],name)
for name in ['Roof_Main','Roof_Porch','Roof_Entry','Roof_Trim','Timber_Front','Timber_CameraSide','Timber_Far','Timber_Entry','Stone_Front','Stone_CameraSide','Stone_Far','Chimney','Windows_Front','Windows_CameraSide','Windows_Far','DoorFrame']:
    replace(by['HH_V2_'+name],name)
# Retained plaster/glass/loft/back fields gain only scoped fade material overrides.
for a in actors:
    n=a.get_actor_label()
    if n.startswith('HH_V2_') and isinstance(a,unreal.StaticMeshActor) and a.static_mesh_component.is_visible():
        c=a.static_mesh_component
        for i,m in enumerate(c.get_materials()):
            if not m:continue
            key=m.get_name().split('_')[-1]
            replacement=unreal.load_asset(H+'/Materials/M_HH_Q3_Fade_'+key)
            if replacement:c.set_material(i,replacement)

# Replace existing pot silhouettes while preserving their mounting positions.
families=['BroadHerb','LeafPlant','FlowerPlant','NarrowHerb','TrailingHerb']
plants=[]
for a in actors:
    if not isinstance(a,unreal.StaticMeshActor) or not a.static_mesh_component.static_mesh:continue
    mesh=a.static_mesh_component.static_mesh.get_name();label=a.get_actor_label()
    if mesh=='SM_HH_Art_HerbPot':
        name=families[len(plants)%len(families)];replace(a,name);plants.append(label)
    elif mesh=='SM_HH_Art_DriedHerbs':replace(a,'HerbBundle')

# Real-camera corner review: keep two larger floor plants out of the side path.
for label,pos in {'HH_Art_FloorHerb_1':(19620,480,1),'HH_Art_FloorHerb_2':(20380,410,1)}.items():
    by[label].set_actor_location(unreal.Vector(*pos),False,False)
by['HH_Art_FloorHerb_1'].set_actor_scale3d(unreal.Vector(.85,.85,.85))

# Windowboxes are small independent reusable modules, with empty path/door reserve.
for index,(x,y,yaw,z) in enumerate([(-493,-275,0,68),(-493,275,0,68),(-260,-480,90,72),(260,-480,90,72),(-260,480,-90,72),(260,480,-90,72)]):
    # Box local long X is along the window sill; orient perpendicular to its wall.
    angle=yaw+90
    spawn('WindowBox_'+str(index),'WindowPlanter',(x,y,z),angle,front=index<2)
    for j,offset in enumerate([-.38,0,.38]):
        if index<2:pos=(x,y+offset*100,z+23)
        else:pos=(x+offset*100,y,z+23)
        spawn('WindowHerb_'+str(index)+'_'+str(j),['FlowerPlant','BroadHerb','TrailingHerb'][j],pos,
              (index*39+j*71)%360,(.50,.50,.65),front=index<2)
# Floor pots flank the entry rather than its free 150 cm aperture.
for index,(x,y) in enumerate([(-540,-175),(-550,275),(-680,-410),(320,-530)]):
    spawn('EntranceHerb_'+str(index),['FlowerPlant','NarrowHerb','BroadHerb','LeafPlant'][index],(x,y,0),index*63,(1.25,1.25,1.15),front=index<2)
# Hanging pots meet beams; botanical shape replaces identical static bundles.
for index,(hook,pot,yaw) in enumerate([((19735,-590,228),(19735,-570,214),0),((20315,590,228),(20315,570,214),180),((20490,-425,228),(20470,-425,214),90)]):
    spawn('HangingHook_'+str(index),'LanternHook',hook,yaw,(1,.85,1))
    spawn('HangingHerb_'+str(index),'HangingHerb',pot,index*59,(.55,.55,.55))
for index,(x,y,z) in enumerate([(20485,-454,137),(20485,-420,148),(20485,-390,158)]):
    spawn('HerbBundle_'+str(index),'HerbBundle',(x,y,z),index*37,(.75,.75,.75))
for n,a in by.items():
    if n.startswith('HH_V3_DriedHerbBundle_'):
        a.static_mesh_component.set_visibility(False);a.set_actor_hidden_in_game(True)
    if n.startswith('ForecourtPlant_'):
        for c in a.get_components_by_class(unreal.StaticMeshComponent):c.set_visibility(False)
        a.set_actor_hidden_in_game(True)
        p=a.get_actor_location();spawn('ForecourtHerb_'+n.rsplit('_',1)[-1],families[int(n.rsplit('_',1)[-1])],[p.x,p.y,0],int(n.rsplit('_',1)[-1])*71,(1.6,1.6,1.4))

# Spatial light islands, controlled source size/range, one shadowed fire light.
lights=[]
def tune(a,intensity,radius,source,temperature,shadow=False,position=None):
    c=a.get_component_by_class(unreal.PointLightComponent)
    if position:a.set_actor_location(unreal.Vector(*position),False,False)
    c.set_use_inverse_squared_falloff(True);c.set_intensity_units(unreal.LightUnits.CANDELAS)
    c.set_intensity(intensity);c.set_attenuation_radius(radius)
    c.set_editor_property('source_radius',source);c.set_editor_property('soft_source_radius',source*1.4)
    c.set_use_temperature(True);c.set_temperature(temperature)
    c.set_light_color(unreal.LinearColor(1,1,1,1));c.set_editor_property('cast_shadows',shadow)
    lights.append({'actor':a.get_actor_label(),'candela':intensity,'range_cm':radius,'source_cm':source,'temperature':temperature,'shadows':shadow})
tune(by['HH_Art_Light_Fire'],20,270,18,2450,True,(20065,-505,67))
tune(by['HH_Art_Light_Waiting'],3.8,245,12,2850,False,(19780,-365,135))
tune(by['HH_Art_Light_Reception'],5.5,260,15,3100,False,(20235,-80,180))
tune(by['HH_Art_Light_Treatment'],3.5,260,16,3400,False,(20130,440,178))
tune(by['HH_V3_CounterGlow'],1.8,210,16,3050)
tune(by['HH_V3_RestAreaGlow'],1.5,210,16,3200)
for i,(pos,target) in enumerate([((19730,-552,167),(19920,-230,50)),((20310,-552,167),(20160,-220,60)),((19730,552,167),(19920,250,45)),((20310,552,167),(20150,250,55)),((20472,-350,178),(20100,-250,65)),((20472,350,178),(20100,260,65))]):
    a=actorlib.spawn_actor_from_class(unreal.SpotLight,unreal.Vector(*pos));a.set_actor_label('HH_Q3_WindowLight_'+str(i));a.set_folder_path('HealingHouse/QualityV3/Lighting')
    c=a.spot_light_component;c.set_mobility(unreal.ComponentMobility.MOVABLE)
    direction=unreal.Vector(target[0]-pos[0],target[1]-pos[1],target[2]-pos[2])
    a.set_actor_rotation(unreal.MathLibrary.make_rot_from_x(direction),False)
    c.set_editor_property('inner_cone_angle',12);c.set_editor_property('outer_cone_angle',48)
    c.set_editor_property('source_radius',24);c.set_editor_property('cast_shadows',False)
    c.set_intensity_units(unreal.LightUnits.CANDELAS);c.set_intensity(5);c.set_attenuation_radius(440)
    c.set_use_temperature(True);c.set_temperature(5800)
    lights.append({'actor':a.get_actor_label(),'candela':5,'range_cm':440,'source_cm':24,'temperature':5800,'shadows':False})
# Lower uniform fill while keeping floor/Player readable; bounded volume only.
pp=by['HH_Art_InteriorLighting'];settings=pp.get_editor_property('settings')
settings.set_editor_property('auto_exposure_bias',-.63)
settings.set_editor_property('ambient_occlusion_intensity',.95)
settings.set_editor_property('ambient_occlusion_radius',65)
pp.set_editor_property('settings',settings)

# New front dressing follows the existing Cutaway; no extra side/rear wall fades.
cut.set_editor_property('occluding_actors',occ)
assert [a.get_actor_label() for a in occ[:len(original_occ)]]==original_occ
assert by['HouseHealer'].get_actor_transform()==healer
assert cut.get_editor_property('interior_camera_distance')==2600 and cut.get_editor_property('fade_duration')>.399
unreal.EditorLoadingAndSavingUtils.save_map(world,'/Game/Maps/Dev_HealingHouseTestMap')
record={'changes':changes,'retained_collision_actors':colliders,'plants_replaced':plants,'new_actors':new,
        'lights':lights,'original_occluders':original_occ,'new_front_occluders':[a.get_actor_label() for a in occ[len(original_occ):]],
        'decorative_plant_moves_cm':{'HH_Art_FloorHerb_1':[19620,480,1],'HH_Art_FloorHerb_2':[20380,410,1]},'layout_and_gameplay_preserved':True}
(OUT/'Placement.json').write_text(json.dumps(record,indent=2)+'\n')
(ROOT/'Art/HealingHouse/QualityV3/Placement.json').write_text(json.dumps(record,indent=2)+'\n')
unreal.log('QUALITY_V3_DRESSED')
