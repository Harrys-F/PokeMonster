
# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=e.get_editor_world();assert not e.get_game_world() and w.get_name()=='Dev_TestMap_NPCMotionV2';a=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);assert not any(x.get_actor_label()=='NPCMotionV2_PreviewSource_NoGameplay' for x in a.get_all_level_actors())
src=a.spawn_actor_from_class(unreal.TargetPoint,unreal.Vector(-100,-150,3));src.set_actor_label('NPCMotionV2_PreviewSource_NoGameplay');src.set_folder_path('NPCMotionV2/ExplicitPreviewOnly');src.tags=['NPCMotionV2_PreviewOnly'];v=a.spawn_actor_from_class(unreal.PokeMonsterNPCVisualActor,src.get_actor_location());v.set_actor_label('NPCMotionV2_PreviewVisual_DisabledUntilTest');v.set_folder_path('NPCMotionV2/ExplicitPreviewOnly');v.source_actor=src;v.tags=['NPCMotionV2_PreviewOnly'];v.visual.set_skeletal_mesh_asset(unreal.load_asset('/Game/Characters/NPCs/RangerMotionV2/Meshes/SK_Ranger_AQV2'));v.visual.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
for prop,clip in [('idle_animation','Idle'),('walk_animation','Walk'),('conversation_animation','Talk'),('turn_left_animation','TurnLeft'),('turn_right_animation','TurnRight')]:v.set_editor_property(prop,unreal.load_asset('/Game/Characters/NPCs/RangerMotionV2/Animations/A_Ranger_'+clip+'_AQV2'))
v.set_editor_property('bEnableMotionPresentation',True);v.set_editor_property('bEnableAccessoryMotion',True);v.set_editor_property('bUseVisual',False);v.attach_to_actor(src,'',unreal.AttachmentRule.KEEP_WORLD,unreal.AttachmentRule.KEEP_WORLD,unreal.AttachmentRule.KEEP_WORLD,False);v.refresh_presentation();assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_NPCMotionV2');unreal.SystemLibrary.execute_console_command(w,'MAP CHECK')
(R/'Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/PreviewActors.json').write_text(json.dumps({'source':src.get_path_name(),'visual':v.get_path_name(),'source_class':src.get_class().get_name(),'active_by_default':False,'gameplay_collision':False,'purpose':'Explicit transform-driven animation preview, no AI/navigation or story actor'},indent=2))
