"""Author only the optional same-map expanded Healing House interior.
Run in Dev_HealingHouseTestMap with PIE stopped. Reuses existing V3 props and
Westland modules; saves only this map. Refuses to repeat the operation.
"""
import json
from pathlib import Path
import unreal
ROOT=Path(unreal.Paths.project_dir()).resolve()
OUT=ROOT/'Saved/HealingExpanded';OUT.mkdir(parents=True,exist_ok=True)
editor=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not editor.get_game_world(), 'Stop PIE before authoring'
world=editor.get_editor_world()
assert world.get_name()=='Dev_HealingHouseTestMap'
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
original=list(sub.get_all_level_actors());by={a.get_actor_label():a for a in original}
cut=next(a for a in original if a.get_class().get_name()=='PokeMonsterBuildingCutaway')
assert not cut.get_editor_property('use_relocated_interior'), 'Already authored'
assert not any(a.actor_has_tag('HealingHouse_Expanded') for a in original)
outer_occluders=list(cut.get_editor_property('occluding_actors'))
outer_door=cut.get_editor_property('door_threshold')
assert outer_door.get_world_location()==unreal.Vector(-450,0,107.5)
assert outer_door.get_unscaled_box_extent()==unreal.Vector(20,75,107.5)
assert abs(cut.get_editor_property('fade_duration')-.4)<1e-6
new=[];moved=[];front=[]
# Unit transforms, parallel inward +X door axes. Ground level is identical.
origin=unreal.Vector(20000,0,150)
area=cut.get_editor_property('relocated_interior_area')
area.set_world_location(origin,False,False)
area.set_box_extent(unreal.Vector(520,610,250),False)
door=cut.get_editor_property('relocated_door_threshold')
door.set_relative_location(unreal.Vector(-500,0,-42.5),False,False)
door.set_box_extent(unreal.Vector(20,75,107.5),False)
cut.set_editor_property('use_interior_camera',True)
cut.set_editor_property('use_relocated_interior',True)
cut.set_editor_property('interior_camera_distance',2600.)
cut.set_editor_property('interior_camera_pitch',-50.)
cut.set_editor_property('interior_camera_yaw_offset',0.)
cut.set_editor_property('relocated_camera_target',unreal.Vector(-60,0,-70))
cut.set_editor_property('relocation_mask_half_width',.2)
# Move whole furniture groups without scaling them or rebuilding their contents.
def shift(a,dx,dy):
    p=a.get_actor_location();q=unreal.Vector(p.x+20000+dx,p.y+dy,p.z)
    a.set_actor_location(q,False,True);a.set_folder_path('HealingHouse/ExpandedInterior/'+str(a.get_folder_path()).split('/')[-1])
    moved.append({'name':a.get_actor_label(),'before':[p.x,p.y,p.z],'after':[q.x,q.y,q.z]})
for a in original:
    label=a.get_actor_label().removeprefix('HH_V3_');folder=str(a.get_folder_path())
    if label in ('HealingCounter','CounterTop','HouseHealer'):
        shift(a,0,0)
    elif 'HealingHouse/V3/Interior' in folder:
        dx=dy=0
        if label.startswith(('ShelfBook','ShelfVial','ShelfHerb')) or label in ('Bookcase','HerbShelf'):dy=-65
        elif label.startswith(('TableHerb','WorkVial','TreatmentCloth')) or label=='HerbTable':dx=-80;dy=80
        elif label.startswith(('Nook','ReadingBook')):dx=60;dy=40
        elif label.startswith('TreatmentBed'):dy=70
        elif label.startswith('DriedHerb'):dx=100;dy=-45
        shift(a,dx,dy)
    elif folder=='HealingHouse/V3/Lighting' and label!='EntranceGlow':
        shift(a,0,50 if label=='RestAreaGlow' else 0)
# Upright healer billboard facing the new frontal camera; its sprite/scale is retained.
healer=by['HouseHealer'];healer.get_editor_property('sprite').set_world_rotation(unreal.Rotator(pitch=0,yaw=90,roll=0),False,False)
# Keep outer architectural actors and their imported asset pivots byte-for-byte configured.
materials={n:unreal.load_asset('/Game/Environment/HealingHouse/Materials/M_HH_V2_'+n) for n in ('Wood','Timber','Stone')}
assert all(materials.values())
base='/Game/Environment/Architecture/Westland/Meshes/'
cache={}
def mesh_actor(label,p,path,yaw=0,scale=(1,1,1),material=None,block=True,hide=False):
    mesh=cache.setdefault(path,unreal.load_asset(path));assert mesh,path
    a=sub.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*p),unreal.Rotator(pitch=0,yaw=yaw,roll=0))
    a.set_actor_label('HH_Expanded_'+label);a.set_folder_path('HealingHouse/ExpandedInterior/Architecture')
    a.set_editor_property('tags',['HealingHouse_Expanded'])
    a.set_actor_scale3d(unreal.Vector(*scale))
    c=a.static_mesh_component;c.set_static_mesh(mesh)
    if material:c.set_material(0,materials[material])
    c.set_cast_shadow(False);c.set_collision_profile_name('BlockAll' if block else 'NoCollision')
    c.set_editor_property('generate_overlap_events',False)
    c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_IGNORE)
    new.append(a)
    if hide:front.append(a)
    return a
def cube(label,p,size,mat,block=True,hide=False):
    return mesh_actor(label,p,'/Engine/BasicShapes/Cube',scale=tuple(v/100 for v in size),material=mat,block=block,hide=hide)
# 12 x 10m footprint; flush collision floor and short safe approach apron.
cube('Floor',(20000,0,-10),(1040,1240,20),'Wood')
cube('DoorApron',(19455,0,-10),(110,180,20),'Wood')
# Reusable Westland wall bays. No extra invisible outer-world blockers.
for i,y in enumerate(range(-600,600,200)):
    mesh_actor('RearWall_'+str(i),(20500,y,0),base+'Walls/SM_WL_WallSolid2m')
for side in (-1,1):
    for i,x in enumerate(range(19500,20500,200)):
        mesh_actor('SideWall_'+str(side)+'_'+str(i),(x,side*600,0),base+'Walls/SM_WL_WallSolid2m',yaw=-90)
# Camera-facing wall uses precisely the same clear 150 x 215cm doorway.
for side in (-1,1):
    cube('FrontWall_'+str(side),(19500,side*337.5,150),(30,525,300),'Stone',hide=True)
    cube('DoorPost_'+str(side),(19487,side*84,107.5),(18,18,215),'Timber',block=False,hide=True)
cube('DoorLintel',(19500,0,257.5),(30,150,85),'Stone',hide=True)
cube('DoorBeam',(19487,0,225),(18,190,20),'Timber',block=False,hide=True)
# Structural beams repeat the same Kit modules, not a new detail/decor pass.
for i,y in enumerate(range(-600,600,200)):
    mesh_actor('RearBeam_'+str(i),(20485,y,270),base+'Timber/SM_WL_HorizontalBeam2m',block=False)
for side in (-1,1):
    for i,x in enumerate(range(19500,20500,200)):
        mesh_actor('SideBeam_'+str(side)+'_'+str(i),(x,side*585,270),base+'Timber/SM_WL_HorizontalBeam2m',yaw=-90,block=False)
mesh_actor('CounterVisual',(20000,0,0),'/Game/Environment/HealingHouse/Meshes/SM_HH_V2_Counter',block=False)
# One existing chimney module establishes the fireplace zone without new VFX/light mood.
mesh_actor('Fireplace',(20420,-470,0),base+'Structural/SM_WL_Chimney60cm',scale=(1.4,1.4,.65))
cut.set_editor_property('occluding_actors',outer_occluders+front)
assert list(cut.get_editor_property('occluding_actors'))[:len(outer_occluders)]==outer_occluders
assert outer_door.get_world_location()==unreal.Vector(-450,0,107.5)
assert unreal.EditorLoadingAndSavingUtils.save_map(world,'/Game/Maps/Dev_HealingHouseTestMap')
(OUT/'Authoring.json').write_text(json.dumps({'footprint_cm':[1000,1200],'room_center_cm':[20000,0,150],'exterior_door_cm':[-450,0,107.5],'interior_door_cm':[19500,0,107.5],'moved':moved,'new_actors':[a.get_actor_label() for a in new],'new_assets':[]},indent=2))
unreal.log('HEALING_EXPANDED_AUTHORED')
