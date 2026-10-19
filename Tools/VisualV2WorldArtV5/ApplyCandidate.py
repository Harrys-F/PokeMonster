"""Three bounded sample biomes, additive visual details only; every old actor audited."""
import unreal,json,sys,copy,math,random,ast
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtV5';A=R/'Art/World/VisualV2WorldArtV5';D='/Game/Environment/VisualV2WorldArtV5';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert w.get_path_name()=='/Game/Maps/Dev_TestMap_VisualV2.Dev_TestMap_VisualV2';assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not (S/'CandidateScene.json').exists()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
def canon(x):
 x=copy.deepcopy(x)
 for a in x['actors'].values():a['components'].sort(key=lambda c:c['name'])
 return x
B=canon(scene(w));assert B==canon(json.loads((S/'BeforeScene.json').read_text()));actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};prepared=json.loads((S/'Prepared.json').read_text());bykey={r['key']:r for r in prepared['ground']};changed=[]
for label,key in [('V2_Ground','Ground'),('V2_Path_NorthLoop','NorthPath'),('V2_Path_VillageLoop','NorthPath'),('V2_Path_Main','MainPath')]:
 a=actors[label];c=a.static_mesh_component;entry=bykey[key];assert c.get_material(0).get_path_name()==entry['old'];c.set_material(0,unreal.load_asset(entry['new']));changed.append({'name':a.get_name(),'label':label,'old':entry['old'],'new':entry['new']})
# Existing route samples are read from the original source, not invented or moved.
module=ast.parse((R/'Tools/ModernizeDevTestMapVisualV2.py').read_text());paths=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets));segments=[(a,b) for pts in paths.values() for a,b in zip(pts,pts[1:])]
# Additional true foot-tour/cottage links are protected too.
segments += [((-2100,-2060),(-1770,-1550)),((-1550,650),(-1900,530))]
protected=[a.get_actor_location() for a in actors.values() if 'PokeMonster' in a.get_class().get_name() and not a.get_actor_label().startswith('V2_House_')]
def dist(x,y,a,b):
 dx=b[0]-a[0];dy=b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)));return math.hypot(x-a[0]-t*dx,y-a[1]-t*dy)
def route_dist(x,y):return min(dist(x,y,a,b) for a,b in segments)
def inside(biome,x,y):
 if biome=='Wald':return ((x+3400)/1010)**2+((y-1810)/570)**2<.94 and y>1280
 if biome=='Wiese':return ((x+2320)/740)**2+((y+1960)/510)**2<.94
 return ((x+250)/875)**2+((y+320)/420)**2<.94
EA=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);L=unreal.MaterialEditingLibrary;rng=random.Random(5191026);groups=[];new_materials=[]
G='/Game/Environment/Westland/NaturalGroundV1/Meshes/SM_WL_NG_';V='/Game/Environment/WestlandAssetLibrary/QualityV3/Meshes/Vegetation/SM_WLA_';W='/Game/Environment/WestlandAssetLibrary/Meshes/';H='/Game/Environment/VisualV2HealingArtV4/Meshes/SM_HA4_';N=D+'/Meshes/SM_WA5_'
specs=[
 ('Wald','FernA',W+'Vegetation/SM_WLA_Fern_A',24,.48,40,'V2_Instanced_Fern'),
 ('Wald','FernB',W+'Vegetation/SM_WLA_Fern_B',16,.46,38,'V2_Instanced_Fern'),
 ('Wald','Shrub',V+'WildBush_V3_A',10,.20,38,'V2_Instanced_BushA'),
 ('Wald','Grass',H+'GrassTuft',42,.88,22,None),
 ('Wald','Moss',N+'MossCushion',30,1.05,26,None),
 ('Wald','Roots',W+'Landscape/SM_WLA_Root_A',8,.78,0,None),
 ('Wiese','Grass',H+'GrassTuft',78,1.0,23,None),
 ('Wiese','Clover',N+'CloverPatch',34,.90,20,None),
 ('Wiese','Flowers',H+'GardenFlowers',14,.76,22,None),
 ('Wiese','Herbs',H+'GardenHerb',15,.75,22,None),
 ('Wiese','Pebbles',G+'PebbleCluster',15,.38,11,None),
 ('Flussufer','Reeds',N+'ReedTuft',22,.85,25,None),
 ('Flussufer','Grass',H+'GrassTuft',30,.85,20,None),
 ('Flussufer','Moss',N+'MossCushion',22,.90,22,None),
 ('Flussufer','Fern',W+'Vegetation/SM_WLA_Fern_A',12,.36,28,'V2_Instanced_Fern'),
 ('Flussufer','Pebbles',G+'PebbleCluster',28,.46,13,None),
 ('Flussufer','BankStone',W+'Landscape/SM_WLA_Boulder_B',7,.13,24,None)]
# Deliberately uneven pockets, not a grid. Density varies between pockets; clearings protected.
pockets={'Wald':[(-3910,1710,80),(-3600,1600,110),(-2830,1700,130),(-2650,1860,80),(-3800,2210,100),(-3160,1460,75)],'Wiese':[(-2670,-2140,90),(-2260,-2240,80),(-1900,-2220,55),(-2780,-1780,110),(-2220,-1610,100),(-1710,-1770,70)],'Flussufer':[]}
root_bases=[(-3880,1580),(-2640,1670)]
def instance_materials(mesh,template):
 originals=[mesh.get_material(i) for i in range(len(mesh.get_editor_property('static_materials')))]
 if template:
  source=actors[template].get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
  originals=[source.get_material(i) for i in range(len(originals))]
 result=[]
 for m in originals:
  assert m;parent=m
  while isinstance(parent,unreal.MaterialInstance):parent=parent.parent
  if not parent.get_editor_property('used_with_instanced_static_meshes'):
   path=D+'/Materials/'+parent.get_name()+'_Instanced'
   p=unreal.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else unreal.EditorAssetLibrary.duplicate_asset(parent.get_path_name(),path);p.set_editor_property('used_with_instanced_static_meshes',True);L.recompile_material(p);assert unreal.EditorAssetLibrary.save_loaded_asset(p,False);new_materials.append(path)
   if isinstance(m,unreal.MaterialInstance):
    ip=D+'/Materials/'+m.get_name()+'_Instanced';mi=unreal.load_asset(ip) if unreal.EditorAssetLibrary.does_asset_exist(ip) else unreal.EditorAssetLibrary.duplicate_asset(m.get_path_name(),ip);L.set_material_instance_parent(mi,p);assert unreal.EditorAssetLibrary.save_loaded_asset(mi,False);new_materials.append(ip);m=mi
   else:m=p
  result.append(m)
 return result
for biome,key,path,count,base,rad,template in specs:
 mesh=unreal.load_asset(path);assert mesh,path;materials=instance_materials(mesh,template);a=EA.spawn_actor_from_class(unreal.Actor,unreal.Vector());a.set_actor_label('WA5_'+biome+'_'+key);a.set_folder_path('VisualV2/WorldArtV5/'+biome);a.tags=['WorldArtV5','VisualOnly_NoCollision'];root=sub.k2_gather_subobject_data_for_instance(a)[0];handle,reason=sub.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle));assert c,reason;c.set_static_mesh(mesh)
 for i,m in enumerate(materials):c.set_material(i,m)
 c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False);c.set_cull_distances(4500,6500);c.set_editor_property('affect_distance_field_lighting',False);c.set_editor_property('affect_dynamic_indirect_lighting',False);placed=[]
 for _ in range(25000):
  if len(placed)==count:break
  yaw=rng.uniform(0,360)
  if key=='Roots':
   bx,by=root_bases[len(placed)//4];yaw=(len(placed)%4)*90+27;angle=math.radians(yaw);x=bx+math.cos(angle)*12;y=by+math.sin(angle)*12
   if route_dist(x,y)<120:raise AssertionError('Chosen tree base intersects route')
  elif biome=='Flussufer':
   x=rng.uniform(-970,520);side=-1 if rng.random()<.5 else 1;waterdist=rng.uniform(85,123) if key in ['Reeds','Pebbles','BankStone'] else rng.uniform(125,220);y=-320+side*waterdist
   if not inside(biome,x,y) or -515<x<-185 or route_dist(x,y)<145+rad:continue
  else:
   px,py,spread=rng.choice(pockets[biome]);x=rng.gauss(px,spread);y=rng.gauss(py,spread*.65)
   if not inside(biome,x,y) or route_dist(x,y)<145+rad:continue
   if biome=='Wald' and ((x+3210)/215)**2+((y-2190)/155)**2<1:continue
   if biome=='Wiese' and ((x+2390)/190)**2+((y+1820)/150)**2<1:continue
  if any(math.hypot(x-p['location_cm'][0],y-p['location_cm'][1])<max(12,rad*.9) for p in placed):continue
  if any(math.hypot(x-p.x,y-p.y)<170+rad for p in protected):continue
  sc=base*rng.uniform(.73,1.22);sz=sc*rng.uniform(.72,1.25)
  if key in ['Roots','Pebbles','BankStone']:sz=sc*(.8 if key=='Roots' else .50)
  z=-.4 if key=='Roots' else -.15 if key in ['Pebbles','BankStone'] else .45
  transform=unreal.Transform(location=unreal.Vector(x,y,z),rotation=unreal.Rotator(yaw=yaw,pitch=rng.uniform(-4,4) if key in ['Pebbles','BankStone'] else 0),scale=unreal.Vector(sc*rng.uniform(.82,1.18),sc,sz));c.add_instance(transform,True);placed.append({'location_cm':[x,y,z],'yaw':yaw,'scale':transform.scale3d.to_tuple()})
 assert len(placed)==count,(biome,key,len(placed),count);assert c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION and not c.cast_shadow;groups.append({'name':a.get_name(),'label':a.get_actor_label(),'biome':biome,'family':key,'mesh':path,'triangles_lod0':mesh.get_num_triangles(0),'instances':placed,'materials':[m.get_path_name() for m in materials]})
F=canon(scene(w));assert F['world_settings']==B['world_settings'];assert not set(B['actors'])-set(F['actors']);assert len(set(F['actors'])-set(B['actors']))==len(groups)
for name,old in B['actors'].items():
 current=F['actors'][name]
 if name not in {r['name'] for r in changed}:assert current==old,('Protected actor changed',name);continue
 test=copy.deepcopy(current)
 for b,t in zip(old['components'],test['components']):t['materials']=b['materials']
 assert test==old,('Only a material binding is permitted',name)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();(S/'CandidateScene.json').write_text(json.dumps(scene(w),indent=2));delta={'changed_existing_bindings':changed,'new_groups':groups,'new_group_count':len(groups),'new_instances':sum(len(g['instances']) for g in groups),'unchanged_existing_actors':len(B['actors'])-len(changed),'protected_actor_deletions':0,'existing_trees_paths_water_bridge_collision_lights_gameplay_unchanged':True,'new_maps':0,'private_instancing_materials':sorted(set(new_materials))};(S/'Delta.json').write_text(json.dumps(delta,indent=2));(A/'Scope.json').write_text(json.dumps(delta,indent=2));unreal.log('WA5_THREE_SAMPLES_APPLIED_NOT_SAVED')
