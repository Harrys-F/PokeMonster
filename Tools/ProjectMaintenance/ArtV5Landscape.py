"""Approved restrained V5 road-surface change and regrouping of existing V4 understory; no new map or trees."""
import unreal,json,math,random
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ArtPassV5';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();AS=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);L=unreal.MaterialEditingLibrary;assert not E.get_game_world() and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not (S/'LandscapeApplied.json').exists();actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};bindings=[];graphs=[]
patch=r'''
// V5: clay, sandy wear and weathered grey gravel in broken pockets; coverage/route unchanged.
struct V5Soil {
 float h(float2 q){return frac(sin(dot(q,float2(127.1,311.7)))*43758.5453);}
 float n(float2 q){float2 a=floor(q),u=frac(q);u=u*u*(3-2*u);return lerp(lerp(h(a),h(a+float2(1,0)),u.x),lerp(h(a+float2(0,1)),h(a+1),u.x),u.y);}
};V5Soil v5;
float soilPatch=v5.n(p/157+float2(12,39));float dryPatch=v5.n(p/73+float2(31,8));float grainPatch=v5.n(p/19);
float soilValue=dot(v6PathColor,float3(.3,.59,.11));
float3 clay=float3(.24,.195,.135)*(.68+soilValue*2.0);float3 sand=float3(.39,.315,.21)*(.67+soilValue*1.65);
float3 v5SoilColor=lerp(clay,sand,smoothstep(.26,.76,soilPatch)*(1-.26*v6F));
v6PathColor=lerp(v6PathColor,v5SoilColor,.67)*(1+.085*(grainPatch-.5));
float gravelPocket=smoothstep(.40,.70,v5.n(p/108+float2(73,21)))*(.35+.65*dryPatch);
float2 pebCell=floor(p/16.0);float seed=v5.h(pebCell);float2 local=frac(p/16.0)-float2(.22+.56*seed,.21+.55*frac(seed*7.13));float angle=seed*6.283185;local=mul(float2x2(cos(angle),-sin(angle),sin(angle),cos(angle)),local);
float pebble=1-smoothstep(.085,.19,length(local*float2(.9+seed,1.65)));pebble*=smoothstep(.32,.62,seed)*gravelPocket;
float3 pebbleColor=lerp(float3(.16,.155,.125),float3(.40,.365,.285),frac(seed*17.31));
v6PathColor=lerp(v6PathColor,pebbleColor,pebble*.86);
float leafPocket=smoothstep(.50,.75,v5.n(p/84+float2(5,44)))*v6F;float leaf=1-smoothstep(.08,.17,length(local*float2(.7,2.8)));leaf*=step(.79,seed)*leafPocket;v6PathColor=lerp(v6PathColor,float3(.18,.14,.075),leaf*.52);
'''
for key in ['Ground','NorthPath','MainPath']:
 source='/Game/Environment/VisualV2HealingArtV4/Materials/M_HH_Landscape'+key;target='/Game/Environment/HealingHouse/ArtV5/Materials/M_HH5_Landscape'+key;assert not unreal.EditorAssetLibrary.does_asset_exist(target);m=unreal.EditorAssetLibrary.duplicate_asset(source,target);assert m
 for n in L.get_material_expressions(m):
  if not isinstance(n,unreal.MaterialExpressionCustom):continue
  old=n.get_editor_property('code');needle='v6PathColor*=1-.11*rootFleck;'
  if needle in old:
   code=old.replace(needle,needle+'\n'+patch);n.set_editor_property('code',code);graphs.append({'material':m.get_path_name(),'expression':n.get_name(),'before':old,'after':code})
 L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
 for a in actors.values():
  for c in a.get_components_by_class(unreal.StaticMeshComponent):
   for slot in range(c.get_num_materials()):
    old=c.get_material(slot)
    if old and old.get_path_name()==source+'.'+source.rsplit('/',1)[1]:bindings.append({'actor':a.get_name(),'component':c.get_name(),'slot':slot,'before':old.get_path_name(),'after':m.get_path_name()});c.set_material(slot,m)
removed=[]
for name,a in actors.items():
 if name.startswith('ArtV4_ForestFence_'):
  assert a.static_mesh_component.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION;removed.append({'actor':a.get_name(),'label':name});assert AS.destroy_actor(a)
assert len(removed)==2
# Regroup only V4 fern and grass additions into uneven island sizes; retain total count and all older plants.
rng=random.Random(52102026);routes=json.loads((R/'Art/World/VisualV2WorldArtV7/RouteField.json').read_text())['segments']
def edge(x,y):
 distances=[]
 for r in routes:
  a,b=r['a'],r['b'];dx=b[0]-a[0];dy=b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)));distances.append(math.hypot(x-a[0]-dx*t,y-a[1]-dy*t)-r['base_half_width_cm'])
 return min(distances)
protected=[a.get_actor_location()for a in actors.values()if 'PokeMonster'in a.get_class().get_name() and abs(a.get_actor_location().x)<6000]
pockets=[(-3830,2220,85,55),(-3460,2220,115,60),(-3120,1740,70,90),(-2920,2110,95,70),(-2690,2230,70,60)]
groups=[]
for family in ['Ferns','Grass']:
 a=actors['ArtV4_Edge_'+family];c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);count=c.get_instance_count();old=[c.get_instance_transform(i,True) for i in range(count)];rows=[]
 for i,t in enumerate(old):
  # Meadow grass keeps its original distribution; changes stay within the existing woodland samples.
  if family=='Grass' and t.translation.y<0:continue
  for attempt in range(3000):
   px,py,sx,sy=rng.choices(pockets,weights=[1,2,1,3,1],k=1)[0];x=rng.gauss(px,sx);y=rng.gauss(py,sy)
   if not 22<edge(x,y)<255 or any(math.hypot(x-q.x,y-q.y)<190 for q in protected):continue
   if any(math.hypot(x-q['after']['position'][0],y-q['after']['position'][1])<(22 if family=='Ferns'else 12)for q in rows):continue
   break
  else:raise RuntimeError('No safe ecological position')
  before={'position':t.translation.to_tuple(),'scale':t.scale3d.to_tuple()};t.translation=unreal.Vector(x,y,.25)
  if family=='Ferns':
   sc=rng.uniform(.40,.90);t.scale3d=unreal.Vector(sc*rng.uniform(.85,1.15),sc,sc*rng.uniform(.9,1.25))
  t.rotation=unreal.Rotator(yaw=rng.uniform(0,360)).quaternion();assert c.update_instance_transform(i,t,True,True,True);rows.append({'index':i,'before':before,'after':{'position':t.translation.to_tuple(),'scale':t.scale3d.to_tuple()}})
 assert c.get_instance_count()==count;groups.append({'actor':a.get_name(),'label':a.get_actor_label(),'count':count,'changed_instances':rows})
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();j={'bindings':bindings,'removed_fences':removed,'groups':groups,'new_instances':0,'existing_trees_routes_and_collision_unchanged':True};(R/'Art/World/VisualV2WorldArtV7/ArtV5_Landscape.json').write_text(json.dumps(j,indent=2));(R/'Art/World/VisualV2WorldArtV7/ArtV5_PathGraphs.json').write_text(json.dumps(graphs,indent=2));(S/'LandscapeApplied.json').write_text(json.dumps(j,indent=2));unreal.log('ART_V5_LANDSCAPE_SAVED')
