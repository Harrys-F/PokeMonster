import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Art/Characters/NPCs/Ranger/Review/AnimationV3/Data'
e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=e.get_editor_world();a=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
assert not e.get_game_world() and w.get_name()=='Dev_TestMap_NPCMotionV3'
v=next(x for x in a.get_all_level_actors() if isinstance(x,unreal.PokeMonsterNPCMotionV3VisualActor) and x.source_actor.get_class().get_name()=='PokeMonsterNPC')
src=v.source_actor;before=json.loads((D/'MapBefore.json').read_text())
assert src.get_actor_location().to_tuple()==tuple(before['position'])
assert src.get_actor_rotation().to_tuple()==tuple(before['rotation'])
assert src.dialogue.get_path_name()==before['dialogue'] and str(src.display_name)==before['display_name']
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_NPCMotionV3')
unreal.SystemLibrary.execute_console_command(w,'MAP CHECK')
(D/'MapConfigured.json').write_text(json.dumps({'source_position':src.get_actor_location().to_tuple(),'source_rotation':src.get_actor_rotation().to_tuple(),'dialogue':src.dialogue.get_path_name(),'source_preserved':True,'visual':v.get_path_name(),'mesh':v.visual.get_skeletal_mesh_asset().get_path_name(),'note':'Configuration stopped at an invalid comparison of Python struct display strings (embedded addresses). Actual numeric position/rotation and dialogue verified unchanged, then only the new V3 map was saved.'},indent=2))
