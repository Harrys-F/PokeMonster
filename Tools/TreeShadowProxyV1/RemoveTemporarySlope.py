import unreal,json
from pathlib import Path
e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_TreeShadowProxyV1'
actors=[a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor) if a.get_actor_label()=='TSP_TestOnly_SlopeReceiver8deg'];assert len(actors)==1 and 'TreeShadowProxyV1_TemporaryReceiver' in [str(x) for x in actors[0].tags]
assert unreal.get_editor_subsystem(unreal.EditorActorSubsystem).destroy_actor(actors[0]);assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
p=Path(unreal.Paths.project_dir())/'Art/World/TreeShadowProxyV1/Review/SlopeTest.json';d=json.loads(p.read_text());d['temporary_receiver_removed_after_test']=True;p.write_text(json.dumps(d,indent=2))
