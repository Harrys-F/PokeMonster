"""Only the existing biome map: graded 15m table, real rock doorway, existing same-map relocated interior."""
import unreal,json,sys,math,random
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);ES=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);SUB=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);w=E.get_editor_world();assert not E.get_game_world()and w.get_name()=='Dev_BiomeTestMap_V1'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
O=R/'Saved/BiomeTestV11/CavePlateauBuild.json';assert not O.exists();actors=ES.get_all_level_actors();by={a.get_actor_label():a for a in actors};assert 'Biome_CaveInterior_V11'not in by
created=[];raised=[];instances=0;rng=random.Random(241026)
def oldheight(u,v):
 h=3*math.sin(u/450)*math.sin(v/530)
 if u<-500 and v<-500:
  edge=max(abs(u+2800)-720,abs(v+1800)-570);hill=300*(1-L.smooth(edge/180));ramp=300*L.smooth((-1200-u)/850)*(1-L.smooth((abs(v+1800)-210)/110))if -2140<u<-1200 else 0;h=max(h,hill,ramp)
 border=max(abs(u),abs(v))-4920
 if border>0:h+=80*L.smooth(border/280)
 return h
for a in actors:
 if a.get_actor_label().startswith('Biome_Cave')or a.get_actor_label()in ['Biome_Terrain_Actual3mPlateau','Biome_StreamAndPond']:continue
 q=a.get_actor_location();u,v=L.local(q.x,q.y)
 if u<-500 and v<-500:
  dz=L.height(u,v)-oldheight(u,v)
  if abs(dz)>.01:a.set_actor_location(q+unreal.Vector(0,0,dz),False,True);raised.append(a.get_actor_label())
 for c in a.get_components_by_class(unreal.HierarchicalInstancedStaticMeshComponent):
  for i in range(c.get_instance_count()):
   t=c.get_instance_transform(i,True);q=t.translation;u,v=L.local(q.x,q.y)
   if u<-500 and v<-500:
    dz=L.height(u,v)-oldheight(u,v)
    if abs(dz)>.01:t.translation=q+unreal.Vector(0,0,dz);assert c.update_instance_transform(i,t,True,True,True);instances+=1
by['Biome_Terrain_Actual3mPlateau'].set_actor_label('Biome_Terrain_15mPlateau')
def component(a,cls):
 root=SUB.k2_gather_subobject_data_for_instance(a)[0];h,why=SUB.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=cls,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h));assert c,why;return c
def actor(cls,label,loc,yaw=-45):
 a=ES.spawn_actor_from_class(cls,unreal.Vector(*loc),unreal.Rotator(yaw=yaw));a.set_actor_label(label);a.set_folder_path('BiomeV11/CaveAndPlateau');a.tags=['BiomeTestV1','BiomeV11'];created.append(a);return a
def room(x,y,z=0):return(25000+L.C*(x+y),L.C*(-x+y),z)
def surface(a,loc,scale,interior=False,yaw=-45):
 a.set_actor_location(unreal.Vector(*loc),False,True);a.set_actor_rotation(unreal.Rotator(yaw=yaw),True);a.set_actor_scale3d(unreal.Vector(*scale));c=a.static_mesh_component;c.set_collision_profile_name('BlockAll');c.set_lighting_channels(not interior,interior,False)
 if interior:c.set_cast_shadow(False);c.set_editor_property('affect_dynamic_indirect_lighting',False);c.set_editor_property('affect_distance_field_lighting',False)
 return a
def rock(label,loc,scale,interior=False,kind='A',collision=True,yaw=-45):
 a=actor(unreal.StaticMeshActor,label,loc,yaw);a.static_mesh_component.set_static_mesh(unreal.load_asset('/Game/Environment/WestlandAssetLibrary/Meshes/Landscape/SM_WLA_Boulder_'+kind));surface(a,loc,scale,interior,yaw)
 if not collision:a.static_mesh_component.set_collision_profile_name('NoCollision')
 return a
def box(label,loc,size,existing=None):
 a=existing or actor(unreal.Actor,label,loc);a.set_actor_location(unreal.Vector(*loc),False,True);a.set_actor_rotation(unreal.Rotator(yaw=-45),True);c=a.get_component_by_class(unreal.BoxComponent)or component(a,unreal.BoxComponent);c.set_box_extent(unreal.Vector(*(x/2 for x in size)));c.set_collision_profile_name('BlockAll');c.set_hidden_in_game(True);a.tags=['BiomeTestV1','CreatureNoWalk'];return a
# Existing three open-cutaway rock walls become the actual side and rear walls of the relocated cave.
for i,(x,y,sc)in enumerate([(0,-1030,(7.1,1.7,2.2)),(0,1030,(7.1,1.7,2.2)),(1040,0,(1.6,8.6,2.4))]):
 surface(by['Biome_CaveRockWall_'+str(i)],room(x,y),sc,True);box('Biome_CaveWallCollision_'+str(i),room(x,y,240),(2100,220,500)if i<2 else(220,2100,500),by['Biome_CaveWallCollision_'+str(i)])
# Flat, colliding base is independent from irregular visible rock dressing.
floor=actor(unreal.StaticMeshActor,'Biome_CaveFloor_V11',room(0,0,-20));floor.static_mesh_component.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'));surface(floor,room(0,0,-20),(21,21,.4),True);floor.static_mesh_component.set_material(0,unreal.load_asset('/Game/Environment/WestlandAssetLibrary/Materials/MI_WLA_MossStone'))
for side in [-1,1]:
 rock('Biome_CaveFrontWall_V11_'+str(side),room(-980,side*700),(1.0,3.5,1.9),True)
 box('Biome_CaveFrontBlock_V11_'+str(side),room(-980,side*700,220),(220,850,440))
 for i in range(6):
  x=-650+i*290+rng.uniform(-50,50);y=side*rng.uniform(690,870);rock('Biome_CaveInteriorRocks_V11_'+str(side)+'_'+str(i),room(x,y),(rng.uniform(.45,.8),rng.uniform(.5,.8),rng.uniform(.65,1.3)),True,collision=True,yaw=rng.uniform(0,360))
# Original entrance piers reused at the visible foot of the fifteen-metre cliff.
for i,u in enumerate([-3350,-2450]):surface(by['Biome_CaveEntrancePier_'+str(i)],L.world(u,-3430,0),(1.45,1.45,2.05),False,45)
roof=rock('Biome_CaveEntranceArch_V11',L.world(-2900,-3430,355),(2.45,1.65,.8),kind='B',yaw=45)
for i,(u,v,z,sc)in enumerate([(-3530,-3270,200,(2.5,1.6,2.7)),(-2250,-3250,250,(2.1,1.6,3)),(-3480,-3050,760,(2,1.7,2.5)),(-2250,-3040,840,(2.3,1.7,2)),(-3860,-2600,850,(1.7,2.3,2.7)),(-3650,-2700,1220,(1.5,1.5,1.5))]):rock('Biome_PlateauCliffDressing_V11_'+str(i),L.world(u,v,z),sc,collision=False,yaw=rng.uniform(0,360))
cut=actor(unreal.PokeMonsterBuildingCutaway,'Biome_CaveInterior_V11',L.world(-2900,-3200,150));cut.interior_area.set_box_extent(unreal.Vector(400,430,320));cut.door_threshold.set_relative_location(unreal.Vector(-250,0,-35),False,False);cut.door_threshold.set_box_extent(unreal.Vector(45,210,200));cut.set_editor_property('bUseRelocatedInterior',True);cut.set_editor_property('bUseInteriorCamera',True);cut.set_editor_property('bUseShadowlessInteriorLighting',True)
area=cut.get_editor_property('relocated_interior_area');area.set_world_location(unreal.Vector(25000,0,150),False,False);area.set_box_extent(unreal.Vector(1000,950,370))
door=cut.get_editor_property('relocated_door_threshold');door.set_relative_location(unreal.Vector(-900,0,-35),False,False);door.set_box_extent(unreal.Vector(45,210,200));cut.set_editor_property('relocated_camera_target',unreal.Vector(0,0,-40));cut.set_editor_property('interior_camera_distance',3300.);cut.set_editor_property('interior_camera_pitch',-50.);cut.set_editor_property('interior_camera_yaw_offset',0.);cut.set_editor_property('OccludingActors',[roof])
# Only explicitly assigned cave specimens may roam this room; all other building exclusions remain.
h=by['Biome_Habitat_Hoehle'];h.set_actor_location(unreal.Vector(25000,0,150),False,True);h.set_actor_rotation(unreal.Rotator(yaw=-45),True);h.bounds.set_box_extent(unreal.Vector(650,580,600));h.set_editor_property('InteriorOwner',cut);h.set_editor_property('ActiveDistanceCm',4500.);arr=h.specimens;q=arr[0];q.local_position=unreal.Vector(0,0,-150);arr[0]=q;h.specimens=arr;h.travel_points=[unreal.Vector(x,y,-150)for x,y in [(-450,0),(400,250),(350,-250),(-200,-350)]]
h=by['Biome_Habitat_Felsoberseite'];h.set_actor_location(unreal.Vector(*L.world(-2800,-1800,1500)),False,True);arr=h.specimens;q=arr[0];q.local_position=unreal.Vector();arr[0]=q;h.specimens=arr
for i,(x,y,z,lm,color)in enumerate([(0,0,410,2600,(190,206,225)),(-600,0,350,1400,(212,218,231)),(600,0,390,1500,(224,193,145))]):
 a=actor(unreal.PointLight,'Biome_CaveLocalLight_V11_'+str(i),room(x,y,z));c=a.get_editor_property('light_component');c.set_mobility(unreal.ComponentMobility.MOVABLE);c.set_intensity(lm);c.set_light_color(unreal.LinearColor(*(q/255 for q in color),1));c.set_attenuation_radius(1600);c.set_cast_shadows(False);c.set_lighting_channels(False,True,False);c.set_editor_property('indirect_lighting_intensity',0.)
# Moss pockets and sparse fallen stones leave a broad clear central route.
for i in range(22):
 x=rng.uniform(-720,750);y=rng.choice([-1,1])*rng.uniform(540,760);a=actor(unreal.StaticMeshActor,'Biome_CaveMoss_V11_'+str(i),room(x,y,.5),rng.uniform(0,360));a.static_mesh_component.set_static_mesh(unreal.load_asset('/Game/Environment/VisualV2WorldArtV5/Meshes/SM_WA5_MossCushion'));a.set_actor_scale3d(unreal.Vector(1.4,1.2,.7));a.static_mesh_component.set_collision_profile_name('NoCollision');a.static_mesh_component.set_lighting_channels(False,True,False);a.static_mesh_component.set_cast_shadow(False)
label=by['Biome_CaveLabel'];label.set_actor_location(unreal.Vector(*L.world(-2900,-3820,180)),False,True);label.text_render.set_text('Hoehle / Rueckweg durch den Felsbogen')
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert all(p.get_path_name()=='/Game/Maps/Dev_BiomeTestMap_V1'for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages());assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_BiomeTestMap_V1')
O.write_text(json.dumps({'map':w.get_path_name(),'plateau_cm':1500,'approach_uv_cm':L.PLATEAU_APPROACH,'cave_approach_uv_cm':L.CAVE_ROUTE,'exterior_door_world':cut.door_threshold.get_world_location().to_tuple(),'room_world':area.get_world_location().to_tuple(),'interior_door_world':door.get_world_location().to_tuple(),'new_actors':[a.get_actor_label()for a in created],'raised_existing_actors':raised,'raised_existing_instances':instances,'new_map':False,'existing_building_transition':True},indent=2));unreal.log('BIOME_CAVE_PLATEAU_V11_SAVED')
