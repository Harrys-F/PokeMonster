"""Extend V6 art without moving an existing actor, path mesh, tree, collider or gameplay component."""
import unreal,json,sys,copy,math,random
from pathlib import Path
R=Path(unreal.Paths.project_dir());S=R/'Saved/VisualV2WorldArtV7';A=R/'Art/World/VisualV2WorldArtV7';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world()
assert w.get_path_name()=='/Game/Maps/Dev_TestMap_VisualV2.Dev_TestMap_VisualV2' and not E.get_game_world()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert not (S/'CandidateScene.json').exists()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
def canon(x):
 x=copy.deepcopy(x)
 for a in x['actors'].values():a['components'].sort(key=lambda c:c['name'])
 return x
before=canon(scene(w));assert before==canon(json.loads((S/'BeforeScene.json').read_text()))
actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};materials={r['key']:r for r in json.loads((S/'Prepared.json').read_text())['materials']};bindings=[]
for label,key in [('V2_Ground','Ground'),('V2_Path_Main','MainPath'),('V2_Path_NorthLoop','NorthPath'),('V2_Path_VillageLoop','NorthPath'),('V2_Path_Wild','MainPath'),('V2_Path_Cottage','MainPath')]:
 a=actors[label];old=a.static_mesh_component.get_material(0);new=unreal.load_asset(materials[key]['new']);a.static_mesh_component.set_material(0,new);bindings.append({'name':a.get_name(),'label':label,'old':old.get_path_name(),'new':new.get_path_name()})
segments=json.loads((A/'RouteField.json').read_text())['segments']
def sd(x,y,u,v):
 dx=v[0]-u[0];dy=v[1]-u[1];t=max(0,min(1,((x-u[0])*dx+(y-u[1])*dy)/(dx*dx+dy*dy)));return math.hypot(x-u[0]-t*dx,y-u[1]-t*dy)
def road(x,y):return min(sd(x,y,r['a'],r['b'])-r['base_half_width_cm'] for r in segments)
def water(x,y):return min(sd(x,y,(-910,-320),(1100,-320))-66,sd(x,y,(720,-320),(720,-680))-64,(math.hypot((x-720)/264,(y+720)/190)-1)*185)
def oldsample(x,y):return ((x+3400)/1000)**2+((y-1810)/530)**2<1 or ((x+2320)/760)**2+((y+1960)/520)**2<1 or ((x+250)/900)**2+((y+320)/430)**2<1
protected=[a.get_actor_location() for a in actors.values() if 'PokeMonster' in a.get_class().get_name() and abs(a.get_actor_location().x)<6000 and not a.get_actor_label().startswith('V2_House_')]
# Deliberately unequal botanical pockets; low-density clearings are not filled.
pockets={
'Westwald':[(-4580,1190,130,150,5),(-4600,1780,140,180,3),(-4090,1050,125,100,2),(-3870,1040,110,95,1),(-4510,2150,170,115,2)],
'Ostwald':[(-1880,1450,140,180,5),(-2030,1050,140,155,2),(-1840,500,100,210,4),(-1330,1170,95,190,2),(-1190,390,90,180,1),(1110,1030,160,100,3),(1400,550,140,160,1)],
'Suedwiese':[(-3630,-1840,150,160,4),(-3890,-1380,120,190,3),(-3510,-1080,110,110,2),(-3100,-2450,200,90,2),(-1310,-2190,150,120,5),(-930,-2020,110,130,2),(-510,-1690,150,170,1),(210,-1340,160,130,2)],
'Ufer':[(1030,-455,100,50,3),(1070,-800,100,110,4),(750,-1020,150,65,2),(445,-730,70,115,5),(470,-475,65,60,2),(1120,-160,80,60,1)]}
plans={
'Westwald':{'Grass':62,'Moss':28,'FernA':16,'FernB':9,'Shrub':7,'Roots':4},
'Ostwald':{'Grass':78,'Moss':30,'FernA':19,'FernB':11,'Shrub':8,'Roots':4},
'Suedwiese':{'Grass':115,'Clover':49,'Flowers':19,'Herbs':20,'Pebbles':25},
'Ufer':{'Reeds':32,'Grass':44,'Moss':22,'Fern':13,'Pebbles':35,'BankStone':8}}
source={'Grass':'WA5_Wiese_Grass','Moss':'WA5_Wald_Moss','FernA':'WA5_Wald_FernA','FernB':'WA5_Wald_FernB','Shrub':'WA5_Wald_Shrub','Roots':'WA5_Wald_Roots','Clover':'WA5_Wiese_Clover','Flowers':'WA5_Wiese_Flowers','Herbs':'WA5_Wiese_Herbs','Pebbles':'WA5_Flussufer_Pebbles','Reeds':'WA5_Flussufer_Reeds','Fern':'WA5_Flussufer_Fern','BankStone':'WA5_Flussufer_BankStone'}
base={'Grass':.95,'Moss':.90,'FernA':.43,'FernB':.46,'Shrub':.20,'Roots':.14,'Clover':.82,'Flowers':.69,'Herbs':.65,'Pebbles':.40,'Reeds':.78,'Fern':.35,'BankStone':.12}
rad={'Grass':24,'Moss':27,'FernA':38,'FernB':38,'Shrub':40,'Roots':46,'Clover':24,'Flowers':27,'Herbs':27,'Pebbles':13,'Reeds':26,'Fern':31,'BankStone':28}
rng=random.Random(7191026);newgroups=[];used=[];sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);actor_sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for biome,families in plans.items():
 for family,count in families.items():
  points=[];candidates=pockets[biome]
  for attempt in range(100000):
   if len(points)==count:break
   cx,cy,sx,sy,weight=rng.choices(candidates,weights=[p[4] for p in candidates])[0];x=rng.gauss(cx,sx);y=rng.gauss(cy,sy)
   if not(-5050<x<1550 and -2670<y<2510) or oldsample(x,y):continue
   if -4720<x<-3500 and -850<y<1220:continue
   if -3110<x<-2380 and -1400<y<-650:continue
   if -1560<x<-1170 and -730<y<-500:continue
   if any(math.hypot(x-p.x,y-p.y)<185+rad[family] for p in protected):continue
   if road(x,y)<(5 if family=='Pebbles' else 5 if family in ['Moss','Clover'] else 28 if family=='Grass' else 65):continue
   wd=water(x,y)
   if wd<30:continue
   if biome=='Ufer' and not(36<wd<(98 if family in ['Reeds','Pebbles','BankStone'] else 190)):continue
   if biome!='Ufer' and wd<145:continue
   if (x<-900 and abs(y+320)<125) or (-550<x<-160 and -565<y<-80):continue
   if math.hypot((x+4310)/100,(y-2070)/160)<1 or math.hypot((x+1800)/130,(y-1000)/160)<1:continue
   if any(math.hypot(x-u,y-v)<(18 if family in ['Grass','Clover','Moss','Pebbles'] else 30) for u,v in used):continue
   scale=base[family]*rng.uniform(.67,1.28);sz=scale*rng.uniform(.65,1.20)
   if family=='Grass':sz=scale*rng.uniform(.48,1.3)
   if family in ['Pebbles','BankStone']:sz=scale*rng.uniform(.38,.57)
   z=-.15 if family in ['Pebbles','BankStone'] else .45
   t=unreal.Transform(location=unreal.Vector(x,y,z),rotation=unreal.Rotator(yaw=rng.uniform(0,360)),scale=unreal.Vector(scale*rng.uniform(.82,1.15),scale,sz));points.append(t);used.append((x,y))
  assert len(points)==count,(biome,family,len(points),count)
  ref=actors[source[family]].get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);assert ref
  a=actor_sub.spawn_actor_from_class(unreal.Actor,unreal.Vector());a.set_actor_label('WA7_'+biome+'_'+family);a.set_folder_path('VisualV2/WorldArtV7/'+biome);a.tags=['WorldArtV7','VisualOnly_NoCollision'];root=sub.k2_gather_subobject_data_for_instance(a)[0];handle,reason=sub.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle));assert c,reason;c.set_static_mesh(ref.static_mesh)
  for i in range(ref.get_num_materials()):c.set_material(i,ref.get_material(i))
  c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False);c.set_editor_property('affect_distance_field_lighting',False);c.set_editor_property('affect_dynamic_indirect_lighting',False);c.set_cull_distances(4500,6500)
  for t in points:c.add_instance(t,True)
  newgroups.append({'name':a.get_name(),'label':a.get_actor_label(),'biome':biome,'family':family,'count':count,'mesh':ref.static_mesh.get_path_name(),'materials':[ref.get_material(i).get_path_name() for i in range(ref.get_num_materials())],'instances':[{'position_cm':t.translation.to_tuple(),'scale':t.scale3d.to_tuple(),'rotation_xyzw':t.rotation.to_tuple(),'road_edge_clearance_cm':road(t.translation.x,t.translation.y),'water_clearance_cm':water(t.translation.x,t.translation.y)} for t in points]})
after=canon(scene(w));names={b['name'] for b in bindings};assert after['world_settings']==before['world_settings']
for name,old in before['actors'].items():
 actual=copy.deepcopy(after['actors'][name])
 if name in names:
  for u,v in zip(old['components'],actual['components']):v['materials']=u['materials']
 assert actual==old,('UNEXPECTED_EXISTING_CHANGE',name)
assert set(after['actors'])-set(before['actors'])=={g['name'] for g in newgroups}
result={'material_bindings':bindings,'new_groups':newgroups,'new_actors':len(newgroups),'new_instances':sum(g['count'] for g in newgroups),'existing_actor_count':len(before['actors']),'all_existing_actors_preserved_except_six_material_bindings':True,'shadow_change':False,'collision_gameplay_camera_lights_pp_water_bridge_unchanged':True}
(A/'Scope.json').write_text(json.dumps(result,indent=2));(S/'Delta.json').write_text(json.dumps(result,indent=2));(S/'CandidateScene.json').write_text(json.dumps(scene(w),indent=2));unreal.log('WA7_CANDIDATE_APPLIED_NOT_SAVED')
