"""Fixed real game camera photographs; pose setup is separate from the no-teleport footrun."""
import unreal,json,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtQualityV1';j=json.loads((S/'PhotoRequest.json').read_text());D=S/'Photos'/j['label'];D.mkdir(parents=True,exist_ok=False)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name()=='Dev_TestMap_VisualV2'
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);unreal.SystemLibrary.execute_console_command(w,f"pm.EnvPerf2.Viewport {j['width']} {j['height']}");unreal.SystemLibrary.execute_console_command(w,f"r.ScreenPercentage {j['percentage']}");unreal.SystemLibrary.execute_console_command(w,'r.VSync 0');unreal.SystemLibrary.execute_console_command(w,'t.MaxFPS 0')
points=[('Heilhaus',-4100,450),('Vorplatz',-3850,520),('Wegsaum',-4140,-180)];state={'i':0,'t':0.,'shot':False,'placed':False,'rows':[]}
def tick(dt):
 try:
  state['t']+=dt;i=state['i']
  if i>=len(points):
   unreal.unregister_slate_post_tick_callback(unreal._worldart_photos);(D/'Result.json').write_text(json.dumps(state['rows'],indent=2));return
  name,x,y=points[i]
  if not state['placed']:
   p.set_actor_location(unreal.Vector(x,y,48.15),False,True);p.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();state['placed']=True
  if state['t']>5 and not state['shot']:
   file=D/(name+'.png');unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(file)+'"',pc);state['shot']=True;state['rows'].append({'name':name,'player':p.get_actor_location().to_tuple(),'camera':pc.player_camera_manager.get_camera_location().to_tuple(),'camera_rotation_rpy':pc.player_camera_manager.get_camera_rotation().to_tuple(),'fov':pc.player_camera_manager.get_fov_angle(),'viewport':list(pc.get_viewport_size()),'percentage':j['percentage']})
  if state['t']>7 and list(D.glob(name+'*.png')):state.update(i=i+1,t=0.,placed=False,shot=False)
 except Exception as ex:
  unreal.unregister_slate_post_tick_callback(unreal._worldart_photos);(D/'Error.txt').write_text(str(ex));raise
unreal._worldart_photos=unreal.register_slate_post_tick_callback(tick)
