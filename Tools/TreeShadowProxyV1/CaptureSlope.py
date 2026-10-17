import unreal,time,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Art/World/TreeShadowProxyV1/Review';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);assert any(a.get_actor_label()=='TSP_TestOnly_SlopeReceiver8deg' for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor))
p.set_actor_location(unreal.Vector(-4300,1550,50.15),False,True);unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Viewport 2560 1440');unreal.SystemLibrary.execute_console_command(w,'r.ScreenPercentage 100');start=time.monotonic();sent=False
def tick(dt):
 global sent
 if time.monotonic()-start<12:return
 if not sent:unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(D/'SlopeReceiver8deg_QHD.png')+'"',pc);sent=True;return
 if time.monotonic()-start<14:return
 (D/'SlopeTest.json').write_text(json.dumps({'receiver':'Temporary engine Plane, 4x3m, pitch8deg, z60cm, NoCollision, CastShadowFalse','position':[-3970,1075,60],'not_saved':True,'not_performance_timed':True,'natural_sloped_terrain':'Not available in selected group; controlled receiver only','viewport':tuple(pc.get_viewport_size())},indent=2));unreal.unregister_slate_post_tick_callback(unreal._tree_slope_capture);del unreal._tree_slope_capture
unreal._tree_slope_capture=unreal.register_slate_post_tick_callback(tick)
