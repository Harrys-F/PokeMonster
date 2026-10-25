"""Capture the unchanged Wanderer from the genuine player camera; RAM save protection only."""
import unreal,json,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/NPCExpansion';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_game_world();assert W
P=unreal.GameplayStatics.get_player_character(W,0);assert P
unreal.SystemLibrary.execute_console_command(W,'pm.NPCGround.Go 1');G=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterNPCTestGround) if x.get_outer()==W);assert G and len(G.specimens)==11
N=next(x for x in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterNPC) if x.get_name().startswith('PokeMonsterNPC_0'))
# Resolve by live source name as the level label is editor-only in PIE.
N=next(x for x in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterNPC) if str(x.display_name)=='Wanderer')
P.set_actor_location(unreal.Vector(-1080,-920,49),False,True);P.set_actor_rotation(unreal.Rotator(0,-45,0),True)
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
start=time.monotonic()
def tick(dt):
 if time.monotonic()-start<2:return
 unreal.unregister_slate_post_tick_callback(unreal._npc_before)
 unreal.SystemLibrary.execute_console_command(W,'HighResShot 2560x1440 filename="'+str(O/'Wanderer_After_QHD.png')+'"')
 (O/'AfterCamera.json').write_text(json.dumps({'player_location':P.get_actor_location().to_tuple(),'player_rotation':P.get_actor_rotation().to_tuple(),'target':N.get_actor_location().to_tuple(),'normal_player_camera':True,'dimensions':[2560,1440]},indent=2))
 settings.set_editor_property('bThrottleCPUWhenNotForeground',old)
unreal._npc_before=unreal.register_slate_post_tick_callback(tick)
