"""Visible earth, gravel and ecological forest-edge dressing; retained routes and all existing instances."""
import unreal,json,random,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ArtPassV4';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert not E.get_game_world() and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not (S/'LandscapeApplied.json').exists();L=unreal.MaterialEditingLibrary;changes=[]
for key in ['Ground','NorthPath','MainPath']:
 m=unreal.load_asset('/Game/Environment/VisualV2HealingArtV4/Materials/M_HH_Landscape'+key)
 for n in L.get_material_expressions(m):
  if not isinstance(n,unreal.MaterialExpressionCustom):continue
  before=n.get_editor_property('code');after=before;needle='float v6Coverage=1-smoothstep(v6Half-10,v6Half+17,v6Dist+v6EdgeNoise);';assert needle in after
  after=after.replace(needle,'v6Half+=(15*sin(v6p.x*.0061+sin(v6p.y*.0038))+11*cos(v6p.y*.0053-v6p.x*.0027))*v6BridgeProtected;\n'+needle)
  needle='float artValue=dot(v6PathColor,float3(.2126,.7152,.0722));v6PathColor=lerp(v6PathColor,artValue.xxx,.085);'
  if needle in after:
   after=after.replace(needle,needle+'''
// Three world-space soil scales. Embedded rounded chips, not a new picture layer.
float artSoil=.5+.27*sin(p.x*.019+sin(p.y*.013))+.22*cos(p.y*.031-p.x*.011);
v6PathColor*=lerp(float3(.72,.77,.74),float3(1.13,1.07,.91),saturate(artSoil));
float2 artCell=floor(p/14.0);float artHash=frac(sin(dot(artCell,float2(127.1,311.7)))*43758.5453);float2 artUv=frac(p/14.0)-float2(.3+.4*artHash,.35+.28*frac(artHash*17));float chip=1-smoothstep(.08,.15,length(artUv*float2(1.1+artHash,1.8-artHash*.5)));chip*=step(.58,artHash)*smoothstep(.3,.8,artSoil);
v6PathColor=lerp(v6PathColor,float3(.26,.235,.175)*(.75+.5*artHash),chip*.76);
float rootFleck=pow(saturate(sin(p.y*.115+sin(p.x*.026)*2)),18)*pow(saturate(cos(p.x*.034)),10);
v6PathColor*=1-.11*rootFleck;
''')
  n.set_editor_property('code',after);changes.append({'material':m.get_path_name(),'expression':n.get_name(),'before':before,'after':after})
 L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};routes=json.loads((R/'Art/World/VisualV2WorldArtV7/RouteField.json').read_text())['segments'];rng=random.Random(42102026)
def sd(x,y,a,b):
 dx=b[0]-a[0];dy=b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)));return math.hypot(x-a[0]-t*dx,y-a[1]-t*dy)
def edge(x,y):return min(sd(x,y,r['a'],r['b'])-r['base_half_width_cm'] for r in routes)
protected=[a.get_actor_location() for a in actors.values() if 'PokeMonster' in a.get_class().get_name() and abs(a.get_actor_location().x)<6000];AS=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);groups=[]
plans=[('Grass','WA5_Wiese_Grass',180,.95),('Clover','WA5_Wiese_Clover',110,.95),('Flowers','WA5_Wiese_Flowers',85,.90),('Ferns','WA5_Wald_FernA',55,.74),('Shrubs','WA5_Wald_Shrub',23,.48),('Moss','WA5_Wald_Moss',75,.90),('RoadPebbles','WA5_Wiese_Pebbles',160,.22),('Roots','WA5_Wald_Roots',12,.62),('Branches',None,15,.82),('Boulders','V2_Stone_P2D_LookoutRock',12,.22)]
pockets=[(-3780,2150,150,80),(-3410,2200,170,90),(-3160,1830,110,100),(-2950,2060,160,90),(-2690,2210,130,70),(-2460,-1830,150,105),(-2220,-2120,150,90),(-1950,-1820,150,100)]
for family,source,count,size in plans:
 ref=actors[source].get_component_by_class(unreal.StaticMeshComponent) if source else None;mesh=ref.static_mesh if ref else unreal.load_asset('/Game/Environment/HealingHouse/ArtV4/Meshes/SM_HH4_FallenBranch');a=AS.spawn_actor_from_class(unreal.Actor,unreal.Vector());a.set_actor_label('ArtV4_Edge_'+family);a.set_folder_path('VisualV2/Landscape/ArtV4');a.tags=['ArtV4','VisualOnly_NoCollision'];root=sub.k2_gather_subobject_data_for_instance(a)[0];h,reason=sub.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h));assert c,reason;c.set_static_mesh(mesh)
 if ref:
  for i in range(ref.get_num_materials()):c.set_material(i,ref.get_material(i))
 c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False);c.set_editor_property('affect_distance_field_lighting',False);c.set_editor_property('affect_dynamic_indirect_lighting',False);c.set_cull_distances(5000,7500);points=[]
 for attempt in range(50000):
  if len(points)==count:break
  choices=pockets[:5] if family in ['Ferns','Shrubs','Roots','Branches','Moss','Boulders'] else pockets;px,py,sx,sy=rng.choice(choices);x=rng.gauss(px,sx);y=rng.gauss(py,sy);d=edge(x,y)
  if family=='RoadPebbles':
   if not -85<d<60:continue
  elif not (125 if family=='Boulders' else 15)<d<220:continue
  if any(math.hypot(x-p.x,y-p.y)<190 for p in protected):continue
  if any(math.hypot(x-u,y-v)<(14 if family in ['Grass','Moss','Clover','RoadPebbles'] else 34) for u,v in points):continue
  if not -4500<x<-1600 or not -2450<y<2490:continue
  sc=size*rng.uniform(.64,1.35);sz=sc*rng.uniform(.70,1.2)
  if family=='RoadPebbles':sz=sc*.32
  t=unreal.Transform(location=unreal.Vector(x,y,.25),rotation=unreal.Rotator(yaw=rng.uniform(0,360)),scale=unreal.Vector(sc*rng.uniform(.8,1.2),sc,sz));c.add_instance(t,True);points.append((x,y))
 assert len(points)==count,(family,len(points));groups.append({'actor':a.get_name(),'label':a.get_actor_label(),'mesh':mesh.get_path_name(),'count':count,'instances':[{'position_cm':c.get_instance_transform(i,True).translation.to_tuple(),'scale':c.get_instance_transform(i,True).scale3d.to_tuple(),'quaternion_xyzw':[getattr(c.get_instance_transform(i,True).rotation,k) for k in ['x','y','z','w']]} for i in range(count)]})
# Reuse existing low fences only off the route; no arbitrary story NPC or new gameplay barriers.
fences=[]
for a in actors.values():
 c=a.get_component_by_class(unreal.StaticMeshComponent)
 if c and c.static_mesh and 'Fence' in c.static_mesh.get_name() and not isinstance(c,unreal.InstancedStaticMeshComponent):fences.append(c)
extra=[]
if fences:
 ref=fences[0]
 for pos,yaw in [((-3650,2350,0),18),((-2920,2380,0),-12)]:
  if edge(*pos[:2])<100:continue
  a=AS.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*pos),unreal.Rotator(yaw=yaw));a.set_actor_label('ArtV4_ForestFence_'+str(len(extra)));a.set_folder_path('VisualV2/Landscape/ArtV4');a.tags=['ArtV4','VisualOnly_NoCollision'];a.static_mesh_component.set_static_mesh(ref.static_mesh)
  for i in range(ref.get_num_materials()):a.static_mesh_component.set_material(i,ref.get_material(i))
  a.static_mesh_component.set_collision_profile_name('NoCollision');a.static_mesh_component.set_cast_shadow(False);a.set_actor_scale3d(unreal.Vector(.72,.72,.72));extra.append(a.get_name())
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');j={'groups':groups,'new_instances':sum(g['count'] for g in groups),'fences':extra,'existing_instances_and_lights_unchanged':True,'route_centrelines_and_collisions_retained':True};(S/'LandscapeApplied.json').write_text(json.dumps(j,indent=2));(R/'Art/World/VisualV2WorldArtV7/ArtV4_Landscape.json').write_text(json.dumps(j,indent=2));(R/'Art/World/VisualV2WorldArtV7/ArtV4_PathGraphs.json').write_text(json.dumps(changes,indent=2));unreal.log('ART_V4_LANDSCAPE_SAVED')
