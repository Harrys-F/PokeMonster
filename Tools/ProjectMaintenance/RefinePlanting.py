"""Unequal ecological pockets reusing approved vegetation. No existing instance is moved."""
import unreal,json,math,random,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir());S=R/'Saved/ProjectRefinement';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert (S/'ArtApplied.json').exists();assert not (S/'PlantingApplied.json').exists()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
before=scene(w);actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};rng=random.Random(202610197)
segments=json.loads((R/'Art/World/VisualV2WorldArtV7/RouteField.json').read_text())['segments']
def sd(x,y,u,v):
 dx=v[0]-u[0];dy=v[1]-u[1];t=max(0,min(1,((x-u[0])*dx+(y-u[1])*dy)/(dx*dx+dy*dy)));return math.hypot(x-u[0]-t*dx,y-u[1]-t*dy)
def road(x,y):return min(sd(x,y,r['a'],r['b'])-r['base_half_width_cm'] for r in segments)
def water(x,y):return min(sd(x,y,(-910,-320),(1100,-320))-66,sd(x,y,(720,-320),(720,-680))-64,(math.hypot((x-720)/264,(y+720)/190)-1)*185)
protected=[a.get_actor_location() for a in actors.values() if 'PokeMonster' in a.get_class().get_name() and abs(a.get_actor_location().x)<6000 and not a.get_actor_label().startswith('V2_House_')]
pockets={
'Forest':[(-4070,1630,100,80,2),(-3860,2220,100,70,3),(-3100,1630,110,60,2),(-2920,2350,130,70,1),(-2680,1860,100,80,4),(-1810,1350,110,140,3),(-1900,760,70,110,2)],
'Meadow':[(-2620,-2170,120,70,4),(-2340,-2240,90,65,3),(-1830,-2270,110,55,2),(-2720,-1660,80,65,3),(-3080,-2070,90,65,1),(-2080,-1640,90,65,3),(-1220,-2100,120,80,2)],
'River':[(-800,-170,100,30,3),(-150,-480,100,30,4),(200,-170,110,25,3),(570,-510,35,75,2),(1020,-610,45,90,3),(820,-970,85,30,2)],
'Entrance':[(-3920,800,70,70,3),(-3860,35,70,65,2),(-4170,-50,70,65,2),(-3730,1000,65,70,1)]}
plans={'Forest':{'Grass':90,'FernA':28,'FernB':18,'Moss':35},'Meadow':{'Grass':130,'Clover':45,'Flowers':28},'River':{'Reeds':32,'Grass':45,'Moss':24,'Pebbles':42},'Entrance':{'Grass':24,'Flowers':12,'Herbs':10}}
sources={'Grass':'WA5_Wiese_Grass','FernA':'WA5_Wald_FernA','FernB':'WA5_Wald_FernB','Moss':'WA5_Wald_Moss','Clover':'WA5_Wiese_Clover','Flowers':'WA5_Wiese_Flowers','Reeds':'WA5_Flussufer_Reeds','Pebbles':'WA5_Flussufer_Pebbles','Herbs':'WA5_Wiese_Herbs'}
base={'Grass':1.13,'FernA':.60,'FernB':.56,'Moss':1.05,'Clover':1.0,'Flowers':.82,'Reeds':.87,'Pebbles':.48,'Herbs':.72}
AS=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);out=[];used=[]
for biome,families in plans.items():
 for family,count in families.items():
  ref=actors[sources[family]].get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);a=AS.spawn_actor_from_class(unreal.Actor,unreal.Vector());a.set_actor_label('Refined_'+biome+'_'+family);a.set_folder_path('VisualV2/RefinedLandscape/'+biome);a.tags=['ProjectRefinement','VisualOnly_NoCollision'];root=sub.k2_gather_subobject_data_for_instance(a)[0];handle,reason=sub.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle));assert c,reason;c.set_static_mesh(ref.static_mesh)
  for i in range(ref.get_num_materials()):c.set_material(i,ref.get_material(i))
  c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False);c.set_editor_property('affect_distance_field_lighting',False);c.set_editor_property('affect_dynamic_indirect_lighting',False);c.set_cull_distances(4500,6500);placed=[]
  for attempt in range(50000):
   if len(placed)==count:break
   cx,cy,sx,sy,_=rng.choices(pockets[biome],weights=[p[4] for p in pockets[biome]])[0];x=rng.gauss(cx,sx);y=rng.gauss(cy,sy);rd=road(x,y);wd=water(x,y)
   if not(-4850<x<1400 and -2550<y<2480) or rd<(14 if family in ['Moss','Pebbles','Clover'] else 30 if family=='Grass' else 55):continue
   if wd<(24 if biome=='River' else 120):continue
   if biome=='River' and wd>180:continue
   if -515<x<-185 and -560<y<-75:continue
   if biome!='Entrance' and -4720<x<-3500 and -850<y<1200:continue
   if any(math.hypot(x-p.x,y-p.y)<190 for p in protected):continue
   if any(math.hypot(x-u,y-v)<(15 if family in ['Moss','Pebbles','Clover'] else 23) for u,v in used):continue
   if biome=='Forest' and ((x+3210)/215)**2+((y-2190)/155)**2<1:continue
   if biome=='Meadow' and ((x+2390)/190)**2+((y+1820)/150)**2<1:continue
   sc=base[family]*rng.uniform(.72,1.23);sz=sc*rng.uniform(.67,1.15)
   if family=='Pebbles':sz=sc*.40
   t=unreal.Transform(location=unreal.Vector(x,y,.45 if family!='Pebbles' else -.10),rotation=unreal.Rotator(yaw=rng.uniform(0,360)),scale=unreal.Vector(sc*rng.uniform(.8,1.18),sc,sz));c.add_instance(t,True);placed.append({'location_cm':t.translation.to_tuple(),'scale':t.scale3d.to_tuple(),'road_edge_distance':rd,'water_distance':wd});used.append((x,y))
  assert len(placed)==count,(biome,family,len(placed));out.append({'name':a.get_name(),'label':a.get_actor_label(),'mesh':ref.static_mesh.get_path_name(),'triangles':ref.static_mesh.get_num_triangles(0),'instances':placed})
after=scene(w)
for n,b in before['actors'].items():assert after['actors'][n]==b,('EXISTING_ACTOR_CHANGED',n)
assert after['world_settings']==before['world_settings'] and set(after['actors'])-set(before['actors'])=={g['name'] for g in out}
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');record={'groups':out,'group_count':len(out),'new_instances':sum(len(g['instances']) for g in out),'existing_actors_and_collision_unchanged':True};(S/'PlantingApplied.json').write_text(json.dumps(record,indent=2));(R/'Art/World/VisualV2WorldArtV7/RefinedPlanting.json').write_text(json.dumps(record,indent=2));unreal.log('REFINED_PLANTING_SAVED')
