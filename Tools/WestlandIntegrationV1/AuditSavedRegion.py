"""Read-only saved-scene audit; no packages/assets are written."""
import unreal,json,collections
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandIntegrationV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();W=E.get_editor_world();assert W.get_name()=='Dev_WestlandRegion'
actors=list(unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors());counts=dict(collections.Counter(a.get_class().get_name()for a in actors));before=json.loads((D/'Dev_WestlandRegion_Before.json').read_text());before_by={a['name']:a for a in before['actors']};by={a.get_name():a for a in actors};assert set(before_by)<=set(by)
rows=[]
for v in [a for a in actors if isinstance(a,unreal.PokeMonsterNPCVisualActor)]:
 a=v.source_actor;b=before_by[a.get_name()];assert str(a.display_name)==b['properties']['display_name'];p=a.get_actor_location();assert abs(p.x-b['location'][0])<.001 and abs(p.y-b['location'][1])<.001
 if isinstance(a,unreal.PokeMonsterNPC):assert a.dialogue.get_path_name()==b['properties']['dialogue']
 assert v.visual.skeletal_mesh_asset and v.idle_animation and v.visual.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
 rows.append({'source':a.get_actor_label(),'visual':v.get_actor_label(),'mesh':v.visual.skeletal_mesh_asset.get_path_name(),'scale':v.get_actor_scale3d().to_tuple(),'source_location':p.to_tuple(),'capsule_halfheight':a.get_component_by_class(unreal.CapsuleComponent).get_unscaled_capsule_half_height(),'idle':v.idle_animation.get_path_name(),'walk':v.walk_animation.get_path_name()if v.walk_animation else None,'run':v.run_animation.get_path_name()if v.run_animation else None,'talk':v.conversation_animation.get_path_name(),'original_dialogue_and_xy':True})
assert len(rows)==4
for c,n in [('PokeMonsterNPC',3),('PokeMonsterRestPoint',1),('PlayerStart',1),('PokeMonsterBuildingCutaway',12),('PokeMonsterVisibleWildCreatureActor',3),('PokeMonsterNPCVisualActor',4),('PokeMonsterHabitatZone',16),('PokeMonsterWorldItem',3),('DirectionalLight',2)]:assert counts.get(c)==n,(c,counts.get(c))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(D/'SavedRegionAudit.json').write_text(json.dumps({'passed':True,'before_actors':len(before['actors']),'after_actors':len(actors),'class_counts':counts,'original_actor_names_all_retained':True,'npc_bindings':rows,'dirty_maps':[],'dirty_assets':[]},indent=2));unreal.log('WESTLAND_FINAL_SAVED_AUDIT_PASSED')
