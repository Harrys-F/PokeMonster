"""Unmodified lighting, real QHD game-camera baseline and existing native GPU probe."""
import unreal,json,time,traceback,gc
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/DayNightV1';O=D/'Before';O.mkdir(exist_ok=False);W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
S=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==GI);assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_DayNightBaseline01')
def cmd(s):unreal.SystemLibrary.execute_console_command(W,s,PC)
cmd('pm.WorldClock pause');cmd('pm.WorldClock set 1 12 0');cmd('pm.EnvPerf2.Viewport 2560 1440')
for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']:cmd('sg.'+n+'Quality 2')
for n,v in [('r.ScreenPercentage',100),('r.SecondaryScreenPercentage.GameViewport',100),('r.DynamicRes.OperationMode',0)]:cmd(n+' '+str(v))
points=[('Wiese',-2100,-1760),('Baumkrone',-1320,-720),('Gebaeude',-4100,450),('Waldweg',-3300,2050),('Felsen',450,470)]
s={'i':0,'placed':False,'t':time.monotonic()};rows=[]
def tick(dt):
 try:
  name,x,y=points[s['i']]
  if not s['placed']:
   P.set_actor_location(unreal.Vector(x,y,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();s.update(placed=True,t=time.monotonic());return
  if time.monotonic()-s['t']<3:return
  cmd('HighResShot 2560x1440 filename="'+str(O/(name+'.png'))+'"');actors={a.get_name():a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)}
  rows.append({'view':name,'player':P.get_actor_location().to_tuple(),'camera':PC.player_camera_manager.get_camera_location().to_tuple(),'rotation':PC.player_camera_manager.get_camera_rotation().to_tuple(),'fov':PC.player_camera_manager.get_fov_angle(),'sun':actors['DirectionalLight_1'].get_actor_rotation().to_tuple(),'fill':actors['DirectionalLight_0'].get_actor_rotation().to_tuple()});s['i']+=1;s['placed']=False
  (O/'Progress.json').write_text(json.dumps(rows[-1]))
  if s['i']==len(points):finish()
 except Exception:finish(traceback.format_exc())
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._daynight_before);(O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'rows':rows,'quality':'High=2 QHD 100% TAA'},indent=2))
 for n in ['W','P','PC','GI','S']:globals().pop(n,None)
unreal._daynight_before=unreal.register_slate_post_tick_callback(tick)
