"""Enrich only the existing biome ruin with reused real geometry. No lighting or gameplay edits."""
import unreal,json,sys,random,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);ES=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);SUB=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);w=E.get_editor_world();assert not E.get_game_world()and w.get_name()=='Dev_BiomeTestMap_V1'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();O=R/'Saved/BiomeTestV11/RuinBuild.json';assert not O.exists();rng=random.Random(240611);created=[];groups={};stone_path='/Game/Environment/BiomeTestV1/Materials/M_RuinStone_V11';assert not unreal.EditorAssetLibrary.does_asset_exist(stone_path)
stone=unreal.EditorAssetLibrary.duplicate_asset('/Game/Environment/HealingHouse/QualityV2/Materials/M_HH_Q2_Stone',stone_path);assert stone;stone.set_editor_property('used_with_instanced_static_meshes',True);unreal.MaterialEditingLibrary.recompile_material(stone);assert unreal.EditorAssetLibrary.save_loaded_asset(stone,False)
original_actors={a.get_actor_label():a for a in ES.get_all_level_actors()};original_trees=sum(x.startswith('Biome_RevealTree_')for x in original_actors)
def actor(cls,label,u,v,z=0,yaw=45):
 a=ES.spawn_actor_from_class(cls,unreal.Vector(*L.world(u,v,z)),unreal.Rotator(yaw=yaw));a.set_actor_label('Biome_RuinV11_'+label);a.set_folder_path('BiomeV11/Ruin');a.tags=['BiomeTestV1','BiomeV11'];created.append(a);return a
def component(a,cls):
 root=SUB.k2_gather_subobject_data_for_instance(a)[0];h,why=SUB.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=cls,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h));assert c,why;return c
def static(path,label,u,v,z,scale=(1,1,1),yaw=45,collision=False,rotation=None):
 a=actor(unreal.StaticMeshActor,label,u,v,z,yaw);c=a.static_mesh_component;c.set_static_mesh(unreal.load_asset(path));assert c.static_mesh;a.set_actor_scale3d(unreal.Vector(*scale));c.set_collision_profile_name('BlockAll'if collision else'NoCollision')
 if rotation:a.set_actor_rotation(rotation,False)
 # Per-component override only. Never edit the shared stone sources.
 for i in range(c.get_num_materials()):c.set_material(i,stone)
 return a
def box(label,u,v,z,size):
 a=actor(unreal.Actor,label,u,v,z);c=component(a,unreal.BoxComponent);c.set_box_extent(unreal.Vector(*(x/2 for x in size)));c.set_collision_profile_name('BlockAll');c.set_hidden_in_game(True);a.tags=['BiomeTestV1','BiomeV11','CreatureNoWalk'];return a
P='/Game/Environment/WestlandRegion/Meshes/'
for label in ['Biome_RuinWall_0','Biome_RuinWall_1','Biome_RuinWall_2']:
 original_actors[label].static_mesh_component.set_material(0,stone)
# 2.3m clear central portal; distinct collision on piers, never a convex hull across its opening.
static(P+'WR_RuinArch','WeatheredEntryArch',3000,-3060,L.height(3000,-3060),(1.,1.,.92))
for side in [-1,1]:box('EntryPier'+str(side),3000+side*170,-3060,135,(55,92,270))
# Old wall bases remain. Reused columns and caps add layers at the perimeter, leaving the nave clear.
for i,(u,v,s)in enumerate([(2390,-3260,.80),(3610,-3210,.66),(2400,-3770,.65),(3610,-3750,.90)]):
 static(P+'WR_RuinColumn','StandingColumn'+str(i),u,v,L.height(u,v),(s,s,s),45,False)
 box('StandingColumnCollision'+str(i),u,v,L.height(u,v)+145*s,(65*s,60*s,285*s))
# Fallen pillar fragments lie beside the walls, away from the 3m-wide central approach.
for i,(u,v,sc,yaw)in enumerate([(2460,-3500,.68,35),(3530,-3560,.60,65)]):
 a=static(P+'WR_RuinColumn','FallenColumn'+str(i),u,v,22,(sc,sc,sc),yaw,False,unreal.Rotator(pitch=83,yaw=yaw,roll=0))
 centre,extent=a.get_actor_bounds(False);b=ES.spawn_actor_from_class(unreal.Actor,centre,unreal.Rotator());b.set_actor_label('Biome_RuinV11_FallenColumnCollision'+str(i));b.set_folder_path('BiomeV11/Ruin');b.tags=['BiomeTestV1','BiomeV11','CreatureNoWalk'];created.append(b);c=component(b,unreal.BoxComponent);c.set_box_extent(extent);c.set_collision_profile_name('BlockAll');c.set_hidden_in_game(True)
# Central remembrance stone: existing runestone stays at the back; embedded low stone dais, no step obstruction.
for i,(u,v,sc)in enumerate([(2860,-3830,.43),(3140,-3845,.38),(2680,-3895,.26),(3330,-3905,.29)]):
 static('/Game/Environment/WestlandAssetLibrary/Meshes/Landscape/SM_WLA_Boulder_B','CollapsedRearStone'+str(i),u,v,-14,(sc,sc,sc*.45),rng.uniform(0,360),True)
paths={'Paving':'/Game/Environment/VisualV2HealingArtV4/Meshes/SM_HA4_Flagstone','Moss':'/Game/Environment/VisualV2WorldArtV5/Meshes/SM_WA5_MossCushion','Fern':'/Game/Environment/VisualV2WorldArtV7/Meshes/SM_WA7_Fern_A','Herbs':'/Game/Environment/WestlandAssetLibrary/Meshes/Vegetation/SM_WLA_Herb_A','Flowers':'/Game/Environment/WestlandAssetLibrary/Meshes/Vegetation/SM_WLA_Wildflowers_A','Rubble':'/Game/Environment/WestlandAssetLibrary/Meshes/Landscape/SM_WLA_SmallStones_A'}
# Private already-instancing-safe materials are set BEFORE assigning meshes, preventing auto-usage writes to shared originals.
matmap={'Moss':['M_HA4_Foliage_Biome'],'Fern':['M_WA5_Foliage_Biome'],'Herbs':['MI_WLA_Leaf_Biome'],'Flowers':['MI_WLA_Leaf_Biome','MI_WLA_FlowerCream_Biome','MI_WLA_FlowerBlue_Biome'],'Rubble':['M_RuinStone_V11'],'Paving':['M_RuinStone_V11']}
def instance(key,u,v,z,scale,yaw):
 if key not in groups:
  a=actor(unreal.Actor,key,0,0);c=component(a,unreal.HierarchicalInstancedStaticMeshComponent);sm=unreal.load_asset(paths[key]);assert sm
  materials=matmap[key]
  for j in range(len(sm.static_materials)):
   m=unreal.load_asset('/Game/Environment/BiomeTestV1/Materials/'+materials[min(j,len(materials)-1)]);assert m;c.set_material(j,m)
  c.set_static_mesh(sm);c.set_collision_profile_name('NoCollision');c.set_cast_shadow(key=='Rubble');c.set_cull_distances(6500,9000);groups[key]=c
 groups[key].add_instance(unreal.Transform(location=unreal.Vector(*L.world(u,v,z)),rotation=unreal.Rotator(yaw=yaw),scale=unreal.Vector(*scale)),True)
# Irregular surviving paving patches, embedded into the unchanged terrain; no artificial repeated full checkerboard.
for i in range(235):
 u=rng.uniform(2460,3540);v=rng.uniform(-3790,-2720)
 if rng.random()<.22 or (math.sin(u/110)+math.cos(v/150)<-.7):continue
 sc=rng.uniform(1.35,2.3);instance('Paving',u,v,L.height(u,v)-.8,(sc,sc*rng.uniform(.75,1.2),.32),rng.uniform(0,360))
# Asymmetric plant pockets retain generous clear routes in front of the central stone.
pockets=[(2260,-3070,110),(3750,-3100,130),(2330,-3740,100),(3650,-3870,115),(2800,-3980,70),(3220,-4000,75),(2570,-2860,65),(3420,-2900,80)]
for key,total,base in [('Moss',95,.85),('Fern',26,.52),('Herbs',30,.6),('Flowers',22,.48),('Rubble',40,.25)]:
 for i in range(total):
  x,y,spread=rng.choice(pockets);u=rng.gauss(x,spread);v=rng.gauss(y,spread)
  if not(2130<u<3870 and -4100<v<-2660):continue
  if 2750<u<3250 and -3790<v<-2740:continue
  sc=base*rng.uniform(.6,1.25);instance(key,u,v,L.height(u,v),[sc,sc,sc*rng.uniform(.7,1.1)],rng.uniform(0,360))
# Real ivy sprigs on the old walls. Individual static components reuse original shader without instancing usage changes.
for i,(u,v,z,yaw,sc)in enumerate([(2210,-3290,125,135,1.1),(2210,-3730,80,135,.9),(3780,-3400,150,315,1.2),(3480,-4020,130,225,1.0),(2670,-4020,70,225,.85)]):
 a=actor(unreal.StaticMeshActor,'WallIvy'+str(i),u,v,z,yaw);c=a.static_mesh_component;c.set_static_mesh(unreal.load_asset('/Game/Environment/VisualV2HealingArtV4/Meshes/SM_HA4_IvySprig'+('A'if i%2 else'B')));a.set_actor_scale3d(unreal.Vector(sc,sc,sc));c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False)
assert sum(a.get_actor_label().startswith('Biome_RevealTree_')for a in ES.get_all_level_actors())==original_trees
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages(),[p.get_path_name()for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
assert all(p.get_path_name()=='/Game/Maps/Dev_BiomeTestMap_V1'for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages());assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_BiomeTestMap_V1')
O.write_text(json.dumps({'new_actors':[a.get_actor_label()for a in created],'new_instances':{k:c.get_instance_count()for k,c in groups.items()},'existing_trees_retained':original_trees,'shared_material_assets_edited':False,'main_approach_clear_width_cm':230,'new_lights':0,'new_maps':0},indent=2))
