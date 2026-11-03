"""Read-only final scene, path, field, asset and original-actor audit."""
import unreal,json,math,sys,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2'and not E.get_game_world();A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);actors={a.get_actor_label():a for a in A.get_all_level_actors()};sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
s=scene(W);before=json.loads((D/'SceneBefore.json').read_text());allowed={'Slice_Waldhueterin_Liora','Slice_Archivarin_Abzweig','Slice_Ruhepunkt','Slice_Ziel_Alter_Archivstein','V2_House_HouseCutaway'};changes=[]
for k,b in before['actors'].items():
 assert k in s['actors'],('Removed original actor',k);a=s['actors'][k]
 if a!=b:
  assert b['class']in ['/Script/Engine.StaticMeshActor','/Script/Engine.Actor']or b['label']in allowed,('Unexpected functional change',b['label']);changes.append(b['label'])
assert before['world_settings']==s['world_settings'];added=[a for k,a in s['actors'].items()if k not in before['actors']];assert all(a['label'].startswith('GEV5_')for a in added);(D/'SceneFinal.json').write_text(json.dumps(s,indent=2))
paths=json.loads((R/'Tools/VisualV2EnvironmentPolishV2/PathMaskSource.json').read_text());seg=runpy.run_path(str(R/'Tools/VisualV2WorldRefinementV4/Design.py'))['seg'];segments=[(n,a,b,paths['halfwidths_cm'][n])for n,p in paths['paths'].items()for a,b in zip(p,p[1:])];violations=[];checked=0
for name,a in actors.items():
 if a.hidden or a.get_class().get_path_name().startswith('/Script/PokeMonster.')or name.startswith(('WR4_','WOV3_Bridge'))or name in ['GEV5_Slice_Ruhepunkt_Stone','GEV5_Slice_Ziel_Alter_Archivstein_Stone']:continue
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  m=c.static_mesh
  if name.startswith('V2_House_')and(m is None or 'grass'not in m.get_path_name().lower()):continue
  if not m or not c.is_visible()or c.hidden_in_game or not any(k in m.get_path_name().lower()for k in ['grass','flower','fern','bush','shrub','stump','small_rock']):continue
  b=m.get_bounding_box();size=b.max-b.min
  for i in range(c.get_instance_count()if isinstance(c,unreal.InstancedStaticMeshComponent)else 1):
   t=c.get_instance_transform(i,True)if isinstance(c,unreal.InstancedStaticMeshComponent)else c.get_world_transform();p=unreal.MathLibrary.transform_location(t,(b.min+b.max)*.5)
   if p.x>3500:continue
   radius=.5*math.hypot(size.x*t.scale3d.x,size.y*t.scale3d.y);distance,n=min((seg(p.x,p.y,v,w)-half,n)for n,v,w,half in segments);checked+=1
   if distance<radius:violations.append(dict(actor=name,index=i,road=n,intrusion_cm=radius-distance))
assert not violations,violations[:20]
# Existing path minimum is the real painted halfwidth; no extra collision on small plants.
fields=[];auth=json.loads((D/'Author.json').read_text());zones=unreal.get_default_object(unreal.load_class(None,'/Script/PokeMonster.PokeMonsterHabitatSettings')).get_editor_property('VisualV2Zones')
for f in auth['fields']:
 z=next(z for z in zones if str(z.get_editor_property('Id'))==f['habitat']);cx,cy=f['center'];rx,ry=f['extent'];assert abs(cx-z.get_editor_property('Center').x)+rx<z.get_editor_property('Extent').x and abs(cy-z.get_editor_property('Center').y)+ry<z.get_editor_property('Extent').y;assert all(seg(cx+sx*rx,cy+sy*ry,a,b)>half+35 for _,a,b,half in segments for sx in [-1,1]for sy in [-1,1]);v=actors['GEV5_BushField_'+f['habitat']].get_component_by_class(unreal.InstancedStaticMeshComponent);assert v.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION;trigger=actors[f['actor']];assert trigger.get_editor_property('distance_based_bush_encounters');fields.append(dict(**f,habitat_type=str(z.get_editor_property('Type')),walk_through=True,fully_inside_existing_habitat=True))
cut=actors['V2_House_HouseCutaway'];assert cut.get_editor_property('stable_doorway_transition')and cut.get_editor_property('constrain_third_person_to_room');assert all(a.get_actor_location().x<15000 for a in cut.occluding_actors if a)
registry=unreal.AssetRegistryHelpers.get_asset_registry();opts=unreal.AssetRegistryDependencyOptions(include_hard_package_references=True,include_soft_package_references=True);missing=[]
for dep in registry.get_dependencies('/Game/Maps/Dev_TestMap_VisualV2',opts):
 p=str(dep)
 if p.startswith('/Game/')and not unreal.EditorAssetLibrary.does_asset_exist(p):missing.append(p)
assert not missing;assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();result=dict(changed_original_actors=changes,added_own_actors=len(added),all_original_actors_retained=True,world_settings_unchanged=True,vegetation_footprints_checked=checked,path_intrusions=violations,fields=fields,missing_map_dependencies=missing,navigation='Existing habitat terrain projection and collision sweeps retained; no parallel navigation system or new NavMesh. Physical route/barrier tests are separate.');(D/'Audit.json').write_text(json.dumps(result,indent=2));print(result)
