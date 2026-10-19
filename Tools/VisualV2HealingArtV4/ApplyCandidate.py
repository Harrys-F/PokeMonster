"""Bounded V4 bindings and collision-free local art additions; not a save-all tool."""
import unreal,json,sys,copy,math,random
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2HealingArtV4';A=R/'Art/World/VisualV2HealingArtV4';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert w.get_path_name()=='/Game/Maps/Dev_TestMap_VisualV2.Dev_TestMap_VisualV2';assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not (S/'CandidateScene.json').exists()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
def canon(s):
 s=copy.deepcopy(s)
 for a in s['actors'].values():a['components'].sort(key=lambda c:c['name'])
 return s
B=canon(scene(w));assert B==canon(json.loads((S/'BeforeScene.json').read_text()))
actors={a.get_name():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};j=json.loads((S/'Prepared.json').read_text());ground={r['old']:r['new'] for r in j['ground']};facade={r['old']:r['new'] for r in j['facade']};mesh={r['family']:unreal.load_asset(r['path']) for r in j['meshes']};changes=[];plantcount=0;ivycount=0
exteriors=['Walls_Front','Walls_CameraSide','Walls_Rear','Walls_Far','Gable_Front','Gable_Rear','Windows_Front','Windows_CameraSide','Windows_Far','Windows_Loft','Roof_Main','Roof_Trim','Roof_Porch','Roof_Entry','Timber_Porch','Timber_Entry','Timber_Front','Timber_Rear','Timber_CameraSide','Timber_Far','Stone_Front','Stone_CameraSide','Stone_Rear','Stone_Far','Foundation','PorchFloor','DoorFrame','DoorLeaf','Chimney']
for name,a in actors.items():
 label=a.get_actor_label();c=a.get_component_by_class(unreal.StaticMeshComponent)
 if not c:continue
 oldmesh=c.static_mesh.get_path_name() if c.static_mesh else '';row={'name':name,'label':label,'mesh_before':oldmesh,'materials_before':[c.get_material(i).get_path_name() for i in range(c.get_num_materials())]};changed=False
 if label in ['V2_Ground','V2_House_Forecourt','V2_Path_VillageLoop','V2_Path_NorthLoop','V2_House_HH_Q2_OrganicApproach']:
  old=c.get_material(0).get_path_name();assert old in ground;c.set_material(0,unreal.load_asset(ground[old]));changed=True
 elif label.startswith('V2_House') and '/VisualV2HealingArtV3/Meshes/' in oldmesh:
  family=oldmesh.split('.')[-1].removeprefix('SM_HA3_');assert family in mesh;c.set_editor_property('override_materials',[]);assert c.set_static_mesh(mesh[family]);plantcount+=1;changed=True
 elif label.startswith('V2_House_HH_V3_Ivy_'):
  assert oldmesh.startswith('/Engine/BasicShapes/Sphere.');c.set_editor_property('override_materials',[]);assert c.set_static_mesh(mesh['IvySprig'+('A' if ivycount%2==0 else 'B')]);ivycount+=1;changed=True
 elif label.removeprefix('V2_House_HH_V2_') in exteriors and label.startswith('V2_House_HH_V2_') or label.startswith('V2_House_HH_Q3_WindowBox_') or label=='V2_House_HH_Q3_GuardianSign':
  for i in range(c.get_num_materials()):
   old=c.get_material(i).get_path_name()
   if old in facade:c.set_material(i,unreal.load_asset(facade[old]));changed=True
   # Window boxes use a non-fading original wood. Private graph still supports cutaway.
   elif label.startswith('V2_House_HH_Q3_WindowBox_') and old.split('.')[-1] in ['M_HH_Q2_Wood','M_HH_Q2_Timber']:
    key=old.split('_')[-1];c.set_material(i,unreal.load_asset(next(r['new'] for r in j['facade'] if r['key']==key)));changed=True
 if changed:row.update(mesh_after=c.static_mesh.get_path_name(),materials_after=[c.get_material(i).get_path_name() for i in range(c.get_num_materials())]);changes.append(row)
assert plantcount==26 and ivycount==14,(plantcount,ivycount)
# Supplemental species and paving pockets, with a protected 2.7m walking route.
rng=random.Random(41926);EA=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);groups=[]
centres=[(-4430,-380),(-3850,-300),(-4430,60),(-3790,150),(-4420,370),(-4460,710),(-4090,1000),(-3840,860),(-3700,1000),(-3770,80)]
route=[(-4150,-720),(-4100,450),(-3600,500)];north=[(-4100,450),(-4300,1190)]
def dist(x,y,a,b):
 dx=b[0]-a[0];dy=b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)));return math.hypot(x-a[0]-t*dx,y-a[1]-t*dy)
def safe(x,y,r):return -4510<x<-3630 and -610<y<1080 and not(x>-3800 and 300<y<720) and min(dist(x,y,a,b) for a,b in list(zip(route,route[1:]))+list(zip(north,north[1:])))>135+r
for family,count,base,rad in [('GrassTuft',72,1.0,20),('GardenHerb',18,.95,23),('GardenFlowers',12,.95,23),('Flagstone',45,1.0,0)]:
 a=EA.spawn_actor_from_class(unreal.Actor,unreal.Vector());a.set_actor_label('HA4_'+family);a.set_folder_path('VisualV2/HealingHouseArtV4');a.tags=['HealingHouseArtV4','VisualOnly_NoCollision'];root=sub.k2_gather_subobject_data_for_instance(a)[0];h,reason=sub.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h));assert c,reason;c.set_static_mesh(mesh[family]);c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False);c.set_cull_distances(4500,6500);c.set_editor_property('affect_distance_field_lighting',False);c.set_editor_property('affect_dynamic_indirect_lighting',False)
 # Paving accents use the private stone graph; set the instancing usage before this step.
 placed=[]
 for _ in range(15000):
  if len(placed)==count:break
  if family=='Flagstone':
   x=rng.uniform(-3920,-3610);y=500+rng.uniform(-105,105)
   if any(math.hypot(x-p[0],y-p[1])<21 for p in placed):continue
   z=.7;sc=rng.uniform(.65,1.05)
  else:
   cx,cy=rng.choice(centres);x=rng.gauss(cx,45);y=rng.gauss(cy,70)
   if not safe(x,y,rad) or any(math.hypot(x-p[0],y-p[1])<16 for p in placed):continue
   z=.5;sc=base*rng.uniform(.68,1.24)
  c.add_instance(unreal.Transform(location=unreal.Vector(x,y,z),rotation=unreal.Rotator(yaw=rng.uniform(0,360)),scale=unreal.Vector(sc*rng.uniform(.88,1.1),sc,sc*(.45 if family=='Flagstone' else rng.uniform(.8,1.15)))),True);placed.append([x,y,z,sc])
 assert len(placed)==count,(family,len(placed));assert c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION and not c.cast_shadow;groups.append({'name':a.get_name(),'label':a.get_actor_label(),'mesh':mesh[family].get_path_name(),'count':count,'placements':placed})
F=canon(scene(w));assert F['world_settings']==B['world_settings'];assert not set(B['actors'])-set(F['actors']);assert len(set(F['actors'])-set(B['actors']))==4
changed={r['name'] for r in changes}
for name,old in B['actors'].items():
 current=F['actors'][name]
 if name not in changed:assert current==old,('Protected actor changed',name);continue
 allowed=copy.deepcopy(current)
 for a,b in zip(old['components'],allowed['components']):b['materials']=a.get('materials');b['props']['static_mesh']=a['props'].get('static_mesh')
 assert allowed==old,('Out of scope delta',name)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(S/'CandidateScene.json').write_text(json.dumps(scene(w),indent=2));delta={'changed':changes,'groups':groups,'existing_pots':plantcount,'ivy_sprays':ivycount,'existing_actors_unchanged':len(B['actors'])-len(changed),'added_instances':sum(g['count'] for g in groups),'original_175_instances_unchanged':True,'lights_postprocess_collision_gameplay_camera_unchanged':True};(S/'Delta.json').write_text(json.dumps(delta,indent=2));(A/'Scope.json').write_text(json.dumps(delta,indent=2));unreal.log('HA4_CANDIDATE_APPLIED_NOT_SAVED')
