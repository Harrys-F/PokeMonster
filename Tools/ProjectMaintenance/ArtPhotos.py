"""Real fixed game-camera QHD photos, not a gameplay footrun or benchmark."""
import unreal,json,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ProjectRefinement';j=json.loads((S/'PhotoRequest.json').read_text());D=S/j['label'];D.mkdir(exist_ok=False)
w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0));p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0)
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Viewport 2560 1440');unreal.SystemLibrary.execute_console_command(w,'r.ScreenPercentage 100');unreal.SystemLibrary.execute_console_command(w,'r.SecondaryScreenPercentage.GameViewport 100')
points=[('Wald',-3300,2050),('Wiese',-2100,-1760),('Flussufer',-350,-130),('Uferabzweig',500,-1000),('Heilhaus',-4100,450),('Fassade',-3850,450),('Innenraum',16900,670),('Empfang',17230,650),('Heilbereich',16950,780)]
state={'i':0,'t':0.,'placed':False,'shot':False,'rows':[]}
def tick(dt):
 try:
  state['t']+=dt;i=state['i']
  if i>=len(points):
   unreal.unregister_slate_post_tick_callback(unreal._refine_photos);(D/'Result.json').write_text(json.dumps(state['rows'],indent=2));return
  name,x,y=points[i]
  if not state['placed']:
   p.set_actor_location(unreal.Vector(x,y,48.15),False,True);p.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();state['placed']=True
  if state['t']>4 and not state['shot']:
   unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(D/(name+'.png'))+'"',pc);state['shot']=True;state['rows'].append({'name':name,'player':p.get_actor_location().to_tuple(),'camera':pc.player_camera_manager.get_camera_location().to_tuple(),'rotation':pc.player_camera_manager.get_camera_rotation().to_tuple(),'fov':pc.player_camera_manager.get_fov_angle(),'viewport':list(pc.get_viewport_size()),'screen_percentage':unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage')})
  if state['t']>5.5 and list(D.glob(name+'*.png')):state.update(i=i+1,t=0.,placed=False,shot=False)
 except Exception:
  import traceback
  unreal.unregister_slate_post_tick_callback(unreal._refine_photos);(D/'Failure.txt').write_text(traceback.format_exc());raise
unreal._refine_photos=unreal.register_slate_post_tick_callback(tick)
