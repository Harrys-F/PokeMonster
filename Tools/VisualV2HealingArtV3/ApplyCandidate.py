"""Only current exterior pot bindings, bounded ground materials and proven decorative cube."""
import unreal,json,sys,copy,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2HealingArtV3';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert w.get_path_name()=='/Game/Maps/Dev_TestMap_VisualV2.Dev_TestMap_VisualV2';assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
before=scene(w)
def canon(s):
 s=copy.deepcopy(s)
 for r in s['actors'].values():r['components'].sort(key=lambda c:c['name'])
 return s
assert canon(before)==canon(json.loads((S/'BeforeScene.json').read_text()))
runpy.run_path(str(R/'Tools/VisualV2HealingArtV3/Inventory.py'),run_name='__main__');inv=json.loads((S/'Inventory.json').read_text());assert not inv['serialized_actor_referencers'];assert inv['cube']['name']=='StaticMeshActor_505' and inv['cube']['collision']=='<CollisionEnabled.NO_COLLISION: 0>' and not inv['cube']['shadow'];prepared=json.loads((S/'Prepared.json').read_text());by={a.get_name():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};changed=[];potrows=[]
ground={r['old']:r['new'] for r in prepared['ground']}
for row in inv['ground']:
 a=by[row['name']];c=a.static_mesh_component;old=c.get_material(0).get_path_name();assert old in ground;c.set_material(0,unreal.load_asset(ground[old]));changed.append(a.get_name())
new={r['family']:r['path'] for r in prepared['plants']}
for row in inv['plants']:
 if row['location'][0]>=0 or '/QualityV3/Meshes/' not in (row['mesh'] or ''):continue
 family=row['mesh'].split('.')[-1].removeprefix('SM_HH_Q3_');assert family in new,family;a=by[row['name']];c=a.static_mesh_component;c.set_editor_property('override_materials',[]);assert c.set_static_mesh(unreal.load_asset(new[family]));changed.append(a.get_name());potrows.append({'name':a.get_name(),'label':a.get_actor_label(),'family':family,'location_cm':row['location'],'old_mesh':row['mesh'],'new_mesh':new[family]})
assert len(potrows)==26
cube=by[inv['cube']['name']];assert unreal.get_editor_subsystem(unreal.EditorActorSubsystem).destroy_actor(cube)
after=scene(w);B=canon(before);F=canon(after);assert set(B['actors'])-set(F['actors'])=={inv['cube']['name']};assert not set(F['actors'])-set(B['actors']);assert F['world_settings']==B['world_settings']
for name,old in B['actors'].items():
 if name==inv['cube']['name']:continue
 current=F['actors'][name]
 if name not in changed:assert current==old,('Protected actor changed',name);continue
 allowed=copy.deepcopy(current)
 for a,b in zip(old['components'],allowed['components']):
  b['materials']=a.get('materials');b['props']['static_mesh']=a['props'].get('static_mesh')
 assert allowed==old,('Out-of-scope change',name)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(S/'CandidateScene.json').write_text(json.dumps(after,indent=2));(S/'Delta.json').write_text(json.dumps({'map':w.get_path_name(),'removed_cube':inv['cube'],'changed_actor_names':changed,'ground_actors':inv['ground'],'pots':potrows,'unchanged_actors':len(F['actors'])-len(changed),'instances_unchanged':175,'lights_postprocessing_gameplay_transforms_collision_shadows_unchanged':True,'new_maps':0,'performance_benchmarks':False},indent=2));unreal.log('HA3_CANDIDATE_APPLIED_NOT_SAVED')
