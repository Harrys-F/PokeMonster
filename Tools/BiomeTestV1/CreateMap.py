"""Author only Dev_BiomeTestMap_V1. Never copies, clears, saves or edits an existing map."""
import unreal,json,sys,math,random
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
D='/Game/Environment/BiomeTestV1';MAP='/Game/Maps/Dev_BiomeTestMap_V1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);ES=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);SUB=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
assert not E.get_game_world() and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert E.get_editor_world().get_name()=='Dev_TestMap_VisualV2';assert not unreal.EditorAssetLibrary.does_asset_exist(MAP)
# Snapshot only the approved exterior lighting/post processing. Map-owned AA object is re-created.
lights=[];settings=None;tree_mats={}
for a in ES.get_all_level_actors():
 if isinstance(a,(unreal.DirectionalLight,unreal.SkyLight)) and a.get_actor_label()in['DirectionalLight_Dev','SkyLight_Dev','VS_SoftSkyFill']:
  c=a.get_editor_property('light_component');props={}
  for k in ['mobility','intensity','light_color','temperature','use_temperature','light_source_angle','light_source_soft_angle','indirect_lighting_intensity','cast_shadows','volumetric_scattering_intensity','source_type','cubemap','real_time_capture','sky_distance_threshold','lower_hemisphere_is_black','lower_hemisphere_color','shadow_bias','shadow_slope_bias','shadow_resolution_scale','contact_shadow_length','dynamic_shadow_distance_movable_light']:
   try:props[k]=c.get_editor_property(k)
   except Exception:pass
  lights.append((type(a),a.get_actor_location(),a.get_actor_rotation(),a.get_actor_label(),props))
 if isinstance(a,unreal.PostProcessVolume)and a.get_actor_label()=='V2_OutdoorExposure':
  settings=a.get_editor_property('settings');settings.set_editor_property('weighted_blendables',unreal.WeightedBlendables())
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if c.static_mesh and c.static_mesh.get_name()in['SM_WLA_OakAncient_V3','SM_WLA_Birch_A']:
   mats=[c.get_material(i)for i in range(c.get_num_materials())]
   if any(m and ('Reveal' in m.get_name())for m in mats):tree_mats[c.static_mesh.get_name()]=mats
assert len(lights)==3 and settings
w=unreal.EditorLoadingAndSavingUtils.new_blank_map(False);assert w
w.get_world_settings().set_editor_property('default_game_mode',unreal.PokeMonsterBiomeTestGameMode)
created=[];groups={};rng=random.Random(23102026)
def actor(cls,label,u=0,v=0,z=0,yaw=0,folder='BiomeV1'):
 a=ES.spawn_actor_from_class(cls,unreal.Vector(*L.world(u,v,z)),unreal.Rotator(yaw=yaw));assert a;a.set_actor_label(label);a.set_folder_path(folder);a.tags=['BiomeTestV1'];created.append(a);return a
for cls,loc,rot,label,props in lights:
 a=ES.spawn_actor_from_class(cls,loc,rot);a.set_actor_label('Biome_'+label);a.set_folder_path('BiomeV1/Lighting');created.append(a)
 c=a.get_editor_property('light_component')
 for k,v in props.items():c.set_editor_property(k,v)
 assert c.get_editor_property('intensity')==props['intensity']
pp=actor(unreal.PostProcessVolume,'Biome_ApprovedExteriorSettings');pp.set_editor_property('unbound',True);pp.set_editor_property('priority',-10);pp.set_editor_property('settings',settings)
aa=unreal.new_object(unreal.PokeMonsterTemporalAABlendable,outer=pp,name='Biome_TAA');pp.add_or_update_blendable(aa,1.)
def mesh(path):
 m=unreal.load_asset(path);assert m,path;return m
MESH='/Game/Environment/WestlandAssetLibrary/Meshes/';MAT='/Game/Environment/WestlandAssetLibrary/Materials/'
def static(path,label,u,v,z=None,scale=(1,1,1),yaw=0,collision=False,materials=None):
 a=actor(unreal.StaticMeshActor,label,u,v,L.height(u,v)if z is None else z,yaw,'BiomeV1/Structures');c=a.static_mesh_component;c.set_static_mesh(mesh(path));a.set_actor_scale3d(unreal.Vector(*scale))
 c.set_collision_profile_name('BlockAll'if collision else'NoCollision')
 if materials:
  for i,m in enumerate(materials):c.set_material(i,m)
 return a
terrain=static(D+'/Meshes/SM_BiomeTerrain','Biome_Terrain_Actual3mPlateau',0,0,0,collision=True);terrain.tags.append('BiomeWalkableGround')
water=static(D+'/Meshes/SM_BiomeWater','Biome_StreamAndPond',0,0,0);water.tags.append('Water')
def component(a,cls):
 root=SUB.k2_gather_subobject_data_for_instance(a)[0];h,reason=SUB.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=cls,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h));assert c,reason;return c
def box(label,u,v,z,size,tag=None):
 a=actor(unreal.Actor,label,u,v,z,45,'BiomeV1/Collision');c=component(a,unreal.BoxComponent);c.set_box_extent(unreal.Vector(*(x/2 for x in size)));c.set_collision_profile_name('BlockAll');c.set_hidden_in_game(True)
 if tag:a.tags.append(tag)
 return a
# Existing bridge is 16.19m long; scaled to 8.4m with the original board/rail proportions.
bridge=static('/Game/Environment/WestlandRegion/Meshes/WR_WoodBridge','Biome_WoodBridge',L.stream(0,4100),4100,15,(.52,1.16,.9),45)
box('Biome_BridgeDeck',L.stream(0,4100),4100,5,(830,308,20))
for side in [-1,1]:box('Biome_BridgeRail_'+str(side),L.stream(0,4100),4100+side*164,58,(830,12,86),'CreatureNoWalk')
# Player cannot wade into the deep test water. Creature traces explicitly ignore these barriers.
barriers=0
for u in range(1900,4401,120):
 for v in range(1800,5200,120):
  if L.height(u,v)>-48:continue
  if abs(v-4100)<230:continue
  box('Biome_WaterBarrier_'+str(barriers),u,v,75,(124,124,250),'BiomePlayerWaterBarrier');barriers+=1
# Explicit visible map limits, backed by blockers inside the stone/hedge rim.
for i in [-1,1]:
 box('Biome_MapLimitU'+str(i),i*5100,0,150,(100,10400,400),'CreatureNoWalk')
 box('Biome_MapLimitV'+str(i),0,i*5100,150,(10400,100,400),'CreatureNoWalk')
# A roofless cutaway cave built from native rocks. Entrance width ~4m, interior ~12x10m.
for i,(u,v,sx,sy,sz)in enumerate([(-3500,-3850,1.2,3.7,1.05),(-1900,-3850,1.2,3.7,1.05),(-2700,-4550,4.9,1.0,1.15)]):
 static(MESH+'Landscape/SM_WLA_Boulder_A','Biome_CaveRockWall_'+str(i),u,v,0,(sx,sy,sz),45,True)
 box('Biome_CaveWallCollision_'+str(i),u,v,120,(270 if i<2 else 1500,1300 if i<2 else 250,240),'CreatureNoWalk')
for i,u in enumerate([-3190,-2210]):static(MESH+'Landscape/SM_WLA_Boulder_B','Biome_CaveEntrancePier_'+str(i),u,-3200,0,(.85,.7,1.1),45,True)
# Front top arch is deliberately omitted for an unobstructed game camera cutaway.
# Ruin walls and columns are reused at real scale; the camera-facing side and roof remain open.
wall=mesh(MESH+'Ruins/SM_WLA_WallRemnant_A');b=wall.get_bounding_box();ws=b.max-b.min
for i,(u,v,du,dv,yaw)in enumerate([(3000,-4030,1600,75,45),(2200,-3500,70,980,45),(3800,-3500,70,980,45)]):
 static(wall.get_path_name(),'Biome_RuinWall_'+str(i),u,v,0,(du/ws.x,dv/ws.y,230/ws.z),yaw,False);box('Biome_RuinWallCollision_'+str(i),u,v,100,(du,dv,200),'CreatureNoWalk')
for i,u in enumerate([2300,3700]):static(MESH+'Ruins/SM_WLA_Column_A','Biome_RuinEntryColumn_'+str(i),u,-2900,0,(1.15,1.15,1.15),45,True)
static(MESH+'Ruins/SM_WLA_Runestone_A','Biome_RuinRunestone',3000,-3860,0,(.8,.8,.8),225)
# Botany instancing: uneven overlapping pockets, intentional paths and creature clearings.
def instance(path,family,u,v,scale=(1,1,1),yaw=0,shadow=False,materials=None):
 key=(path,family)
 if key not in groups:
  a=actor(unreal.Actor,'Biome_'+family,folder='BiomeV1/Vegetation');c=component(a,unreal.HierarchicalInstancedStaticMeshComponent);c.set_static_mesh(mesh(path));c.set_collision_profile_name('NoCollision');c.set_cast_shadow(shadow);c.set_cull_distances(6500,9000)
  if materials:
   for i,m in enumerate(materials):c.set_material(i,m)
  groups[key]=c
 c=groups[key];c.add_instance(unreal.Transform(location=unreal.Vector(*L.world(u,v,L.height(u,v))),rotation=unreal.Rotator(yaw=yaw),scale=unreal.Vector(*scale)),True)
clear=[(-3300,2600,260),(-2200,3000,230),(-1550,1300,700),(2050,2700,250),(2650,2400,250),(-2800,-1800,300),(-2700,-3830,350),(1700,-1700,220),(3000,-3400,400)]
def keep_clear(u,v,r=0):return any(math.hypot(u-x,v-y)<s+r for x,y,s in clear)
# Trees use exactly the approved camera-reveal material opt-ins.
tree_points=[]
for biome,center,count,spread in [('Meadow',(-3600,3400),24,(1150,1100)),('Forest',(3000,-2800),61,(1500,1600)),('Bank',(4350,3000),9,(280,1200)),('Rock',(-4050,-3150),9,(450,1200))]:
 accepted=0
 for attempt in range(10000):
  if accepted>=count:break
  u=rng.gauss(center[0],spread[0]*.6);v=rng.gauss(center[1],spread[1]*.6)
  if not(-4850<u<4850 and -4850<v<4850)or L.path_distance(u,v)<260 or L.height(u,v)<-5 or keep_clear(u,v,70):continue
  if biome=='Forest'and 2050<u<3950 and -4250<v<-2700:continue
  if biome=='Rock'and (-3700<u<-1600 and -4700<v<-3000 or -3700<u<-1700 and -2600<v<-1000):continue
  if any(math.hypot(u-a,v-b)<260 for a,b in tree_points):continue
  oak=rng.random()<(.75 if biome=='Forest'else .35);path='/Game/Environment/WestlandAssetLibrary/QualityV3/Meshes/Trees/SM_WLA_OakAncient_V3'if oak else MESH+'Trees/SM_WLA_Birch_A';scale=rng.uniform(.55,.82)if oak else rng.uniform(.68,1.0)
  overrides=tree_mats.get('SM_WLA_OakAncient_V3'if oak else'SM_WLA_Birch_A')
  if oak and not overrides:overrides=[mesh('/Game/Environment/DevTestMapVisualV2/Materials/M_V2_BarkRevealBase'),mesh('/Game/Environment/DevTestMapVisualV2/Materials/M_V2_CrownReveal')]
  instance(path,biome+'_Trees',u,v,(scale,scale,scale*rng.uniform(.9,1.1)),rng.uniform(0,360),True,overrides)
  box('Biome_Trunk_'+str(len(tree_points)),u,v,L.height(u,v)+130,(55,55,260),'CreatureNoWalk');tree_points.append((u,v));accepted+=1
plants={'Grass':'/Game/Environment/VisualV2WorldArtV2/Meshes/SM_WAQ2_GrassSmall','GrassTall':'/Game/Environment/VisualV2WorldArtV2/Meshes/SM_WAQ2_GrassMedium','Clover':'/Game/Environment/VisualV2WorldArtV5/Meshes/SM_WA5_CloverPatch','Moss':'/Game/Environment/VisualV2WorldArtV5/Meshes/SM_WA5_MossCushion','Fern':'/Game/Environment/VisualV2WorldArtV7/Meshes/SM_WA7_Fern_A','Flowers':MESH+'Vegetation/SM_WLA_Wildflowers_A','Herbs':MESH+'Vegetation/SM_WLA_Herb_A','Reeds':'/Game/Environment/VisualV2WorldArtV5/Meshes/SM_WA5_ReedTuft','Shrub':'/Game/Environment/WestlandAssetLibrary/QualityV3/Meshes/Vegetation/SM_WLA_WildBush_V3_A','Stones':MESH+'Landscape/SM_WLA_SmallStones_A','Root':MESH+'Landscape/SM_WLA_Root_A'}
# Use the source meshes' own, already-correct instanced vegetation materials wherever present.
base_materials={}
for key,path in plants.items():
 sm=mesh(path);base_materials[key]=[x.material_interface for x in sm.static_materials]
for biome,center,counts in [('Meadow',(-2700,2700),{'Grass':390,'GrassTall':180,'Clover':140,'Flowers':95,'Herbs':55,'Shrub':18,'Stones':30}),('Forest',(2700,-2700),{'Grass':170,'Moss':240,'Fern':145,'Shrub':32,'Herbs':70,'Root':26,'Stones':40}),('Rock',(-2700,-2700),{'Grass':70,'Moss':80,'Fern':20,'Stones':110,'Herbs':35}),('Bank',(3100,3000),{'Grass':160,'Reeds':95,'Moss':110,'Stones':90,'Fern':40})]:
 pockets=[(center[0]+rng.uniform(-1500,1500),center[1]+rng.uniform(-1500,1500),rng.uniform(150,430))for _ in range(15)]
 for family,count in counts.items():
  placed=0
  for attempt in range(count*150):
   if placed>=count:break
   x,y,spread=rng.choice(pockets);u=rng.gauss(x,spread);v=rng.gauss(y,spread)
   if not(-4800<u<4800 and -4800<v<4800):continue
   if biome in ['Meadow','Forest','Rock']and not((u< -600 if center[0]<0 else u>600)and(v< -600 if center[1]<0 else v>600)):continue
   if biome=='Bank'and not(1500<u<4600 and 1300<v<4900):continue
   h=L.height(u,v)
   if h<-18 or L.path_distance(u,v)<(120 if family=='Stones'else 210):continue
   if keep_clear(u,v,0):
    if family!='Grass' or rng.random()<.8:continue
   if -3660<u<-1740 and -4700<v<-3050:continue
   if 2100<u<3900 and -4200<v<-2750:continue
   if family=='Reeds'and not(-16<h<2 and u>1800 and v>1500):continue
   scale={'Grass':.85,'GrassTall':.9,'Clover':1.0,'Moss':1.0,'Fern':.65,'Flowers':.6,'Herbs':.65,'Shrub':.45,'Stones':.33,'Root':.32,'Reeds':.85}[family]*rng.uniform(.60,1.25)
   zscale=scale*rng.uniform(.75,1.1)
   if family in ['Grass','GrassTall']and keep_clear(u,v):zscale*=.35
   instance(plants[family],biome+'_'+family,u,v,(scale,scale,zscale),rng.uniform(0,360),False,base_materials[family]);placed+=1
# Accent boulders, path-edge stones and occasional deadwood. No rows or path blockages.
for i in range(45):
 for attempt in range(100):
  u=rng.uniform(-4700,4700);v=rng.uniform(-4700,4700)
  if L.path_distance(u,v)<270 or keep_clear(u,v,90)or L.height(u,v)<-5:continue
  if -3700<u<-1600 and -4800<v<-2800 or 2000<u<4000 and -4300<v<-2700:continue
  scale=rng.uniform(.22,.6);static(MESH+'Landscape/SM_WLA_Boulder_'+('A'if i%2 else'B'),'Biome_AccentRock_'+str(i),u,v,None,(scale,scale,scale*rng.uniform(.7,1.2)),rng.uniform(0,360),True);break
# Noninteractive test labels are deliberately confined to the hub/shore, never fake NPC services.
def text(label,body,u,v,z=180):
 a=actor(unreal.TextRenderActor,label,u,v,z,135,'BiomeV1/Information');c=a.text_render;c.set_text(body);c.set_world_size(22);c.set_horizontal_alignment(unreal.HorizTextAligment.EHTA_CENTER);c.set_text_render_color(unreal.Color(225,218,171,255));return a
text('Biome_HubLabel','BIOME-TEST V1\nWiese / Wasser / Felsen / Wald\nNur Bewegung und Darstellung',0,80,155)
text('Biome_WaterDiagnosticLabel','Wasser-Pruefkoerper\nGoldini-Modell fehlt',4050,2350,130)
text('Biome_CaveLabel','Offener Hoehlenschnitt',-2500,-3120,220)
# Saved habitat definitions. They spawn visual-only specimens during ordinary Play.
def habitat(name,mode,center,half,specs,points=(),draft=20,radius=24,flight=False,float_height=45):
 a=actor(unreal.PokeMonsterBiomeHabitat,'Biome_Habitat_'+name,*center,0,45,'BiomeV1/Habitats');a.set_editor_property('HabitatName',name);a.set_editor_property('Medium',mode);a.bounds.set_box_extent(unreal.Vector(half[0],half[1],600));a.set_editor_property('WaterDraftCm',draft);a.set_editor_property('ClearanceRadiusCm',radius);a.set_editor_property('bAllowGroundFlight',flight);a.set_editor_property('FloatClearanceCm',float_height)
 arr=[]
 for idx,(species,u,v,diag)in enumerate(specs):
  q=unreal.PokeMonsterBiomeSpecimen();q.set_editor_property('Species',unreal.load_asset('/Game/Data/Creatures/DA_'+species));q.set_editor_property('LocalPosition',unreal.Vector(u-center[0],-(v-center[1]),L.height(u,v)));q.set_editor_property('Seed',23100+len(created)*13+idx*31);q.set_editor_property('bWaterDiagnostic',diag);arr.append(q)
 a.set_editor_property('Specimens',arr);a.set_editor_property('TravelPoints',[unreal.Vector(u-center[0],-(v-center[1]),0)for u,v in points]);a.set_editor_property('DiagnosticMaterial',unreal.load_asset(D+'/Materials/M_WaterDiagnostic'));return a
B=unreal.PokeMonsterBiomeMedium
habitat('Wiese',B.LAND,(-2850,2900),(1450,1250),[('Bisasam',-3300,2600,False),('Pikachu',-2200,3000,False)])
habitat('BodennaherFlug',B.LAND,(-1550,1350),(760,650),[('Glurak',-1550,1300,False)],[(-2000,1350),(-1300,1100),(-1300,1700)],radius=90,flight=True)
habitat('SchiggyUfer',B.AMPHIBIOUS,(2520,2700),(900,650),[('Schiggy',2050,2700,False)],[(1950,2700),(2350,2700),(2800,2700),(3000,2900)],draft=23,radius=25)
habitat('EntonUfer',B.AMPHIBIOUS,(2800,2400),(850,550),[('Enton',2650,2400,False)],[(2500,2200),(2950,2200),(3250,2500)],draft=35,radius=48)
habitat('NurWasser_Diagnose',B.WATER_ONLY,(3350,2950),(570,400),[('Schiggy',3400,3000,True)],[(3150,2800),(3600,2950),(3250,3150)],draft=12,radius=18)
habitat('Felsoberseite',B.LAND,(-2800,-1800),(580,420),[('Machomei',-2800,-1800,False)],radius=100)
habitat('Hoehle',B.LAND,(-2700,-3850),(560,550),[('Glutexo',-2700,-3830,False)],radius=60)
habitat('Waldschweben',B.FLOATING,(1650,-1750),(650,600),[('Nebulak',1700,-1700,False)],[(1300,-1600),(1900,-1600),(1700,-2100)],radius=75,float_height=45)
habitat('Ruine',B.LAND,(3000,-3450),(570,400),[('Gengar',3000,-3400,False)],radius=100)
spawn=actor(unreal.PlayerStart,'Biome_PlayerStart',0,-200,110,315,'BiomeV1')
# Fog is new-map-only and nonvolumetric; existing lighting values and TAA remain the source baseline.
fog=actor(unreal.ExponentialHeightFog,'Biome_DistanceHaze',0,0,-200,folder='BiomeV1/Lighting');fog.component.set_editor_property('fog_density',.003);fog.component.set_editor_property('fog_height_falloff',.5)
assert unreal.EditorLoadingAndSavingUtils.save_map(w,MAP)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
# Complete with IsolateMaterials.py before PIE; never save auto-dirtied originals.
rows={'map':MAP,'biome_area_cm':4400,'world_basis':'u screen right, v screen up, camera unchanged','actors':len(created),'water_barriers':barriers,'trees':len(tree_points),'instanced_groups':{a[1]:c.get_instance_count()for a,c in groups.items()},'specimens':{'Wiese':['Bisasam','Pikachu','Glurak'],'Wasser':['Schiggy','Enton','explicit water-only diagnostic marker, NOT Goldini'],'Felsen':['Machomei','Glutexo'],'Wald':['Nebulak','Gengar']},'source_lights':[x[3]for x in lights],'canopy_material_optins':{k:[m.get_path_name()for m in v]for k,v in tree_mats.items()},'no_existing_map_saved':True,'no_gameplay_ids':True,'swimming_animation':'Idle/buoyancy prototype; no authored swim clip present','cave_and_ruin':'roofless open cutaway'}
(R/'Saved/BiomeTestV1/MapBuild.json').write_text(json.dumps(rows,indent=2));unreal.log('BIOME_MAP_SAVED '+MAP)
