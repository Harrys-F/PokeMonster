"""Verify every pre-existing actor, transform, collision, instance and PP setting against baseline."""
import unreal,json,copy,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/EnvironmentV3';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert not E.get_game_world();sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
before=json.loads((D/'BeforeScene.json').read_text());after=scene(W);scope=json.loads((R/'Art/World/VisualV2EnvironmentV3/Scope.json').read_text());assert before['world_settings']==after['world_settings'];assert set(before['actors']).issubset(after['actors']);assert set(after['actors'])-set(before['actors'])=={g['actor']for g in scope['groups']}
for name,old in before['actors'].items():
 actual=copy.deepcopy(after['actors'][name])
 for b in [x for x in scope['bindings']if x['actor']==name]:
  c=next(x for x in actual['components']if x['name']==b['component']);assert c['materials'][b['slot']]==b['after'];c['materials'][b['slot']]=b['before']
 for b in [x for x in scope['light_changes']if x['actor']==name]:
  c=next(x for x in actual['components']if 'intensity'in x['props']);assert abs(float(c['props']['intensity'])-b['after'])<1e-6;c['props']['intensity']=str(b['before'])
 assert actual==old,('UNEXPECTED_CHANGE',old['label'])
for g in scope['groups']:
 a=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)if a.get_name()==g['actor']);c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);assert c.get_instance_count()==g['count'];assert c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION and not c.cast_shadow;assert not c.get_editor_property('affect_distance_field_lighting') and not c.get_editor_property('affect_dynamic_indirect_lighting')
(D/'AfterScene.json').write_text(json.dumps(after,indent=2));(D/'ScopeValidation.json').write_text(json.dumps({'passed':True,'original_actors':len(before['actors']),'new_groups':len(scope['groups']),'new_instances':scope['new_instances'],'material_bindings':len(scope['bindings']),'lighting_changes':scope['light_changes'],'original_collisions_transforms_instances_pp_gameplay_unchanged':True,'map_count':len(list((R/'Content/Maps').glob('*.umap')))},indent=2));assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();unreal.log('ENV3_SCOPE_PASS')
