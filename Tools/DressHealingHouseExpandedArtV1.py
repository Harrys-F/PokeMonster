"""Art-only pass on the existing expanded room. Never changes gameplay settings.
Retained blocker geometry remains authoritative. New detail has no collision;
new furniture has saved simple collision and ignores interaction traces.
"""
import unreal,json,math
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();DEST='/Game/Environment/HealingHouse/ExpandedArtV1';OUT=ROOT/'Saved/HealingArt';OUT.mkdir(parents=True,exist_ok=True)
editor=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not editor.get_game_world();world=editor.get_editor_world();assert world.get_name()=='Dev_HealingHouseTestMap'
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);before=list(actors.get_all_level_actors());by={a.get_actor_label():a for a in before};assert not any(a.actor_has_tag('HealingHouse_ExpandedArt') for a in before)
cut=by['HouseCutaway'];original_occluders=list(cut.get_editor_property('occluding_actors'));healer=by['HouseHealer'];healer_transform=healer.get_actor_transform();door=cut.get_editor_property('door_threshold').get_unscaled_box_extent()
materials={n:unreal.load_asset(DEST+'/Materials/M_HH_Art_'+n) for n in ('Wood','Timber','Plaster','Stone','Mortar','Sage','Linen','Gold','Metal','Leaf','LeafLight','Flower','Ceramic','Glass','Book','Paper','Fire','Window')};assert all(materials.values())
meshes={n:unreal.load_asset(DEST+'/Meshes/SM_HH_Art_'+n) for n in json.loads((ROOT/'Art/HealingHouse/ExpandedArtV1/Props.json').read_text())};assert all(meshes.values())
placed=[]
def spawn(name,prop,x,y,z=0,yaw=0,scale=(1,1,1),blocking=False):
 a=actors.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(20000+x,y,z),unreal.Rotator(roll=0,pitch=0,yaw=yaw));a.set_actor_label('HH_Art_'+name);a.set_folder_path('HealingHouse/ExpandedInterior/ArtV1');a.tags=['HealingHouse_ExpandedArt'];a.set_actor_scale3d(unreal.Vector(*scale));c=a.static_mesh_component;c.set_static_mesh(meshes[prop]);c.set_collision_profile_name('BlockAll' if blocking else 'NoCollision');c.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS if blocking else unreal.CollisionEnabled.NO_COLLISION);c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_IGNORE);c.set_editor_property('cast_shadow',False)
 placed.append({'name':a.get_actor_label(),'prop':prop,'position_cm':[x,y,z],'yaw':yaw,'scale':list(scale),'blocking':blocking});return a
def tint_old(a):
 c=a.static_mesh_component
 for i,m in enumerate(c.get_materials()):
  name=m.get_name() if m else ''
  key=next((n for n in materials if name.endswith('_'+n)),None)
  if key:c.set_material(i,materials[key])
# Warm materials are actor overrides ONLY within the expanded room.
for a in before:
 if 19400<a.get_actor_location().x<20700 and isinstance(a,unreal.StaticMeshActor) and a not in original_occluders:tint_old(a)
# Existing authoritative floor, no new ground collision.
by['HH_Expanded_Floor'].static_mesh_component.set_material(0,materials['Mortar'])
for ix in range(5):
 for iy in range(6):spawn('Floor_%d_%d'%(ix,iy),'FloorTile2m',-400+ix*200,-500+iy*200,1)
# Window geometry replaces selected solid bays, exact overall wall height/width.
# Whole original wall blockers are retained separately and invisible: they keep
# movement collisions exactly as before while actual render mesh has an aperture.
for label in ['HH_Expanded_SideWall_-1_1','HH_Expanded_SideWall_-1_4','HH_Expanded_SideWall_1_1','HH_Expanded_SideWall_1_3','HH_Expanded_RearWall_0','HH_Expanded_RearWall_4']:
 a=by[label];pos=a.get_actor_location();rot=a.get_actor_rotation()
 blocker=actors.spawn_actor_from_class(unreal.StaticMeshActor,pos,rot);blocker.set_actor_label('HH_Art_RetainedBlocker_'+label);blocker.set_folder_path('HealingHouse/ExpandedInterior/ArtV1/RetainedBlockers');blocker.tags=['HealingHouse_ExpandedArt'];bc=blocker.static_mesh_component;bc.set_static_mesh(a.static_mesh_component.static_mesh);bc.set_collision_profile_name(a.static_mesh_component.get_collision_profile_name());bc.set_collision_enabled(a.static_mesh_component.get_collision_enabled());bc.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_IGNORE);bc.set_visibility(False);blocker.set_actor_hidden_in_game(True)
 center=pos+unreal.Vector(100,0,0) if 'Side' in label else pos+unreal.Vector(0,100,0)
 a.set_actor_location(center,False,False);a.static_mesh_component.set_static_mesh(meshes['WindowWall2m']);a.static_mesh_component.set_collision_profile_name('NoCollision');a.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
 # The far side uses the same frame facing the room; yaw180 flips its near face.
 if 'SideWall_1_' in label:a.set_actor_rotation(unreal.Rotator(roll=0,pitch=0,yaw=90),False)
 if 'Rear' in label:a.set_actor_rotation(unreal.Rotator(roll=0,pitch=0,yaw=0),False)
# Framing/stone on retained walls only, with no overhead central beams.
for side in (-1,1):
 for i in range(5):spawn('StoneSide_%s_%s'%(side,i),'StoneWainscot2m',-400+i*200,side*584,0,-90 if side<0 else 90)
 for i in range(6):spawn('PostSide_%s_%s'%(side,i),'WallPost',-495+i*198,side*578,0,-90 if side<0 else 90)
for i in range(6):spawn('StoneRear_%d'%i,'StoneWainscot2m',484,-500+i*200,0)
for i in range(7):spawn('PostRear_%d'%i,'WallPost',478,-585+i*195,0,0)
# Counter visuals replaced, collision / healer transform unchanged.
by['HH_Expanded_CounterVisual'].static_mesh_component.set_visibility(False);by['HH_Expanded_CounterVisual'].set_actor_hidden_in_game(True)
spawn('Reception','CounterStepped',220,-80)
# Former chimney is superseded visually and no longer contributes furniture collision.
old=by['HH_Expanded_Fireplace'];old.static_mesh_component.set_visibility(False);old.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION);old.set_actor_hidden_in_game(True)
spawn('Fireplace','Fireplace',80,-530,0,-90,blocking=True)
# Move the entire shelf stock with its reused V3 shelf, away from the fireplace.
delta=unreal.Vector(240,-55,0)
for a in before:
 if a.get_actor_label()=='HH_V3_HerbShelf' or a.get_actor_label().startswith(('HH_V3_ShelfVial','HH_V3_ShelfHerb')):a.add_actor_world_offset(delta,False,False)
# Reused bookcase and books stay by the left waiting area. Softer green beds.
spawn('BenchWaiting','Bench',-230,-375,0,0,blocking=True)
spawn('BenchCompanion','Bench',-75,-300,0,90,blocking=True)
spawn('TableWaiting','Table',-230,-285,0,0,blocking=True)
spawn('WaitingRug','Rug',-240,-320,3,0,scale=(1.3,1.7,1))
# Rug overlays old aqua debug mats without modifying existing V3 source assets.
for a in before:
 if a.get_actor_label().startswith(('HH_V3_AisleRug','HH_V3_RugBorder')):a.static_mesh_component.set_visibility(False);a.set_actor_hidden_in_game(True)
spawn('MainRunner','Rug',-115,5,3,0,scale=(2.1,1.2,1))
spawn('ReceptionRug','Rug',135,-80,3,0,scale=(.7,1.7,1))
# Right treatment beds remain the existing V3 meshes/collisions.
spawn('PillowSmall','Pillow',-85,415,64)
spawn('PillowLarge','Pillow',105,415,64)
for label,z in [('HH_V3_CounterBandage',107),('HH_V3_CounterBowl',86)]:
 a=by[label];v=a.get_actor_location();v.z=z;a.set_actor_location(v,False,False)
# Reception grouping, all grounded on existing or new surfaces.
for i,(x,y) in enumerate(((214,-155),(215,-70),(225,-205),(220,35))):spawn('CounterVial_%d'%i,'Vial',x,y,80 if y<-166 else 105,scale=(.65,.65,.65))
spawn('CounterJar','CeramicJar',220,-30,105,scale=(.65,.65,.65));spawn('CounterPlant','HerbPot',224,-220,80,scale=(.70,.70,.70));spawn('CounterBasket','Basket',215,53,105,scale=(.62,.62,.62))
spawn('BannerReception','Banner',465,-80,145)
# Seating details are supported by the75cm table; no loose floor clutter.
spawn('WaitingPot','HerbPot',-240,-280,75,scale=(.65,.65,.65));spawn('WaitingJar','CeramicJar',-200,-300,75,scale=(.65,.65,.65));spawn('WaitingBasket','Basket',-265,-303,75,scale=(.45,.45,.45))
# New stock attaches to reused shelves/tables, filling coherent clusters.
for i,z in enumerate((15.5,61.5,109.5)):spawn('HerbShelfStock_%d'%i,'ShelfStock',350,-508,z,0,scale=(1.2,1,1))
for i,z in enumerate((15.5,61.5,109.5)):spawn('BookStock_%d'%i,'ShelfStock',-165,-440,z,0)
for i in range(3):spawn('RearHerb_%d'%i,'DriedHerbs',455,-440+i*50,215,0,scale=(.7,.7,.7))
for side in (-1,1):
 for i,x in enumerate((-270,310)):
  spawn('WindowPot_%s_%s'%(side,i),'HerbPot',x,side*560,98.5,scale=(.70,.70,.70))
  spawn('WallHerb_%s_%s'%(side,i),'DriedHerbs',x+60,side*569,215,0,scale=(.8,.8,.8))
for i,(x,y) in enumerate(((-395,-390),(-380,520),(380,510),(395,-405))):spawn('FloorHerb_%d'%i,'HerbPot',x,y,1,scale=(1.25,1.25,1.25))
for i,(x,y,z) in enumerate(((-330,390,85),(-350,420,85),(-300,380,84),(-310,415,84),(400,280,70))):
 spawn('TreatmentJar_%d'%i,'CeramicJar',x,y,z,scale=(.6,.6,.6))
# Existing room glows unchanged; additional warm islands are localized.
def light(name,x,y,z,intensity,radius,color):
 a=actors.spawn_actor_from_class(unreal.PointLight,unreal.Vector(20000+x,y,z));a.set_actor_label('HH_Art_Light_'+name);a.set_folder_path('HealingHouse/ExpandedInterior/ArtV1/Lighting');a.tags=['HealingHouse_ExpandedArt'];c=a.point_light_component;c.set_editor_property('mobility',unreal.ComponentMobility.MOVABLE);c.set_editor_property('intensity',intensity);c.set_editor_property('attenuation_radius',radius);c.set_editor_property('cast_shadows',False);c.set_light_color(unreal.LinearColor(*color,1));c.set_editor_property('source_radius',35);c.set_editor_property('source_length',40)
light('Fire',80,-470,80,9,390,(1,.55,.25));light('Waiting',-230,-340,180,3.5,300,(1,.72,.40));light('Reception',340,-80,185,4,310,(1,.76,.48));light('Treatment',130,465,210,3.5,330,(1,.78,.52))
lantern=unreal.load_asset('/Game/Environment/HealingHouse/V3/Meshes/SM_HH_V3_Lantern')
for i,(x,y,z) in enumerate(((450,-230,230),(450,210,230),(-150,-555,220),(220,555,225))):
 a=actors.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(20000+x,y,z));a.set_actor_label('HH_Art_Lantern_%d'%i);a.set_folder_path('HealingHouse/ExpandedInterior/ArtV1');a.tags=['HealingHouse_ExpandedArt'];a.static_mesh_component.set_static_mesh(lantern);a.static_mesh_component.set_collision_profile_name('NoCollision');a.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION);a.static_mesh_component.set_editor_property('cast_shadow',False)
# Verify no change to any cutaway setting or functional actor transform.
assert list(cut.get_editor_property('occluding_actors'))==original_occluders
assert healer.get_actor_transform()==healer_transform
assert cut.get_editor_property('door_threshold').get_unscaled_box_extent()==door
assert cut.get_editor_property('interior_camera_distance')==2600 and cut.get_editor_property('interior_camera_pitch')==-50
assert cut.get_editor_property('fade_duration')==.4 or abs(cut.get_editor_property('fade_duration')-.4)<1e-6
pp=actors.spawn_actor_from_class(unreal.PostProcessVolume,unreal.Vector(19000,0,1200));pp.set_actor_label('HH_Art_InteriorLighting');pp.set_folder_path('HealingHouse/ExpandedInterior/ArtV1/Lighting');pp.tags=['HealingHouse_ExpandedArt'];o,e=pp.get_actor_bounds(False,False)
Path('/private/tmp/HealingArt/PPBounds.txt').write_text(str((o,e)))
assert e.x>0 and e.y>0 and e.z>0,'Volume has no brush'
pp.set_actor_scale3d(unreal.Vector(2000/e.x,1500/e.y,1500/e.z));pp.set_actor_enable_collision(False);pp.set_editor_property('unbound',False);pp.set_editor_property('blend_radius',50)
settings=pp.get_editor_property('settings')
for k,v in {'override_auto_exposure_bias':True,'auto_exposure_bias':-.7,'override_color_saturation':True,'color_saturation':unreal.Vector4(.9,.9,.9,1),'override_ambient_occlusion_intensity':True,'ambient_occlusion_intensity':.5,'override_ambient_occlusion_radius':True,'ambient_occlusion_radius':90}.items():settings.set_editor_property(k,v)
pp.set_editor_property('settings',settings)

# Reuse bookcases on the rear wall; no changes to their shared assets.
book=unreal.load_asset('/Game/Environment/HealingHouse/V3/Meshes/SM_HH_V3_Bookcase')
for idx,y in enumerate((-350,420)):
 a=actors.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(20460,y,0),unreal.Rotator(roll=0,pitch=0,yaw=90));a.set_actor_label('HH_Art_RearApothecary_%d'%idx);a.tags=['HealingHouse_ExpandedArt'];a.set_folder_path('HealingHouse/ExpandedInterior/ArtV1');c=a.static_mesh_component;c.set_static_mesh(book);c.set_collision_profile_name('BlockAll');c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_IGNORE);c.set_editor_property('cast_shadow',False)
 for i,m in enumerate(c.get_materials()):
  key=m.get_name().split('_')[-1];mat=unreal.load_asset(DEST+'/Materials/M_HH_Art_'+key)
  if mat:c.set_material(i,mat)
 for row,z in enumerate((16,62,110)):
  for col,dy in enumerate((-25,25)):
   p=actors.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(20440,y+dy,z),unreal.Rotator(roll=0,pitch=0,yaw=90));p.set_actor_label('HH_Art_RearStock_%d_%d_%d'%(idx,row,col));p.tags=['HealingHouse_ExpandedArt'];p.set_folder_path('HealingHouse/ExpandedInterior/ArtV1');stock=('Vial' if row==1 else 'CeramicJar') if (row,col) in ((0,0),(1,1),(2,0)) else 'ShelfStock';p.static_mesh_component.set_static_mesh(unreal.load_asset(DEST+'/Meshes/SM_HH_Art_'+stock));p.set_actor_scale3d(unreal.Vector(1,1,1) if stock!='ShelfStock' else unreal.Vector(.7,.7,.8));p.static_mesh_component.set_collision_profile_name('NoCollision');p.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION);p.static_mesh_component.set_editor_property('cast_shadow',False)

unreal.EditorLoadingAndSavingUtils.save_map(world,'/Game/Maps/Dev_HealingHouseTestMap')
(OUT/'Placement.json').write_text(json.dumps({'props':placed,'occluders_unchanged':True,'healer_unchanged':True},indent=2))
unreal.log('HH_EXPANDED_ART_DRESSING_PASSED')
