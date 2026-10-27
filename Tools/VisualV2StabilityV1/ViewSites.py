"""Bounded real-camera lighting regression outside the changed platforms; no scene writes."""
import unreal,json,time,traceback,gc
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2StabilityV1';O=D/'ViewSites01';O.mkdir(exist_ok=False);W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W);C=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterWorldClock)if x.get_outer()==GI);L=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterDayNightSubsystem)if x.get_outer()==W)
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
cmd('pm.WorldClock pause');cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100')
for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']:cmd('sg.'+n+'Quality 2')
shots=[('Wiese0900',-2100,-1760,9),('Wiese2200',-2100,-1760,22),('Waldweg1200',-4300,1550,12),('Waldweg0000',-4300,1550,0),('Krone0600',-1353.161706774002,-775.1272881918381,6),('Krone1900',-1353.161706774002,-775.1272881918381,19),('Krone2200',-1353.161706774002,-775.1272881918381,22),('Haus0900',-4100,450,9),('Haus2200',-4100,450,22)];s={'i':0,'placed':False,'last':time.monotonic()};rows=[]
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._stability_sites);rows2={p:str(unreal.load_asset(p).get_editor_property('shading_model'))for p in ['/Game/Environment/Prototype2D/Materials/M_PaintedGround','/Game/Environment/VisualV2EnvironmentV3/Materials/M_EQ3_Ground']};(O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'rows':rows,'shading_models':rows2},indent=2))
 for n in ['W','P','PC','GI','C','L']:globals().pop(n,None)
 gc.collect()
def tick(dt):
 try:
  name,x,y,h=shots[s['i']]
  if not s['placed']:
   P.set_actor_location(unreal.Vector(x,y,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();cmd('pm.WorldClock set 1 '+str(h)+' 0');s.update(placed=True,last=time.monotonic());return
  if time.monotonic()-s['last']<2.5:return
  cmd('HighResShot 2560x1440 filename="'+str(O/(name+'.png'))+'"');rows.append({'name':name,'position':P.get_actor_location().to_tuple(),'camera':PC.player_camera_manager.get_camera_location().to_tuple(),'clock':C.get_time().export_text(),'lighting':L.get_lighting_sample().export_text()});s.update(i=s['i']+1,placed=False)
  if s['i']==len(shots):finish()
 except Exception:finish(traceback.format_exc())
unreal._stability_sites=unreal.register_slate_post_tick_callback(tick)
