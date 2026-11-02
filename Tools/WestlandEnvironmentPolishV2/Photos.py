"""Eight genuine paired Westland captures; own PIE only. No assets/maps saved."""
import unreal,json,time,math,traceback,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandEnvironmentPolishV2';label=json.loads((D/'PhotoRequest.json').read_text())['label'];O=D/label;O.mkdir(exist_ok=False);assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D)
sys.path.insert(0,str(R/'Tools'));import WestlandRegionLayout as L
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);state={'i':0,'stage':0,'at':time.monotonic()};rows=[];start=time.monotonic();W=P=PC=None;overview=None
cases=[('Dorf',-222,-47,-205,-42),('Waldrand',183,52,205,80),('DichterWald',247,250,265,264),('Waldweg',202,120,225,175),('Flussoberflaeche',L.river(-145)+10,-145,L.river(-145),-142),('Flussufer',L.river(-90)+11,-90,L.river(-90),-85),('Blumenwiese',150,13,180,25),('Huegelland',-155,265,-100,220),('Felsformation',105,-174,115,-173)]
def cmd(x):unreal.SystemLibrary.execute_console_command(W,x,PC)
def finish(error=None):
 global overview
 if overview:PC.set_view_target_with_blend(P,0);overview.destroy_actor()
 if W:cmd('pm.WorldClock reset')
 (O/'Result.json').write_text(json.dumps(dict(passed=error is None,error=error,rows=rows,positioning='diagnostic captures, not foot run',seconds=time.monotonic()-start),indent=2));unreal.unregister_slate_post_tick_callback(unreal._wvuphotos);unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
def tick(dt):
 global W,P,PC,overview
 try:
  assert time.monotonic()-start<200
  if W is None:
   W=E.get_game_world()
   if W is None:return
   assert 'Dev_WestlandRegion'in W.get_name();P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0)
   if not P:return
   cmd('pm.WorldClock set 1 12 0');cmd('pm.WorldClock pause');state['at']=time.monotonic();return
  if state['i']>=len(cases):finish();return
  name,e,n,te,tn=cases[state['i']]
  if state['stage']==0:
   x,y,z=L.world(e,n,L.height(e,n));P.set_actor_location(unreal.Vector(x,y,z+50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();tx,ty,_=L.world(te,tn);yaw=math.degrees(math.atan2(ty-y,tx-x));P.third_person_boom.set_world_rotation(unreal.Rotator(yaw=yaw),False,False)
   state.update(stage=1,at=time.monotonic());return
  if state['stage']==1:
   if time.monotonic()-state['at']<4:return
   if name!='Gesamtansicht':assert abs(PC.player_camera_manager.get_camera_rotation().pitch+12)<.02 and P.third_person_distance==350
   f=O/(name+'.png');cmd('Shot filename="'+str(f)+'" -nosuffix');rows.append(dict(name=name,file=str(f),player=P.get_actor_location().to_tuple(),camera=PC.player_camera_manager.get_camera_location().to_tuple(),rotation=PC.player_camera_manager.get_camera_rotation().to_tuple(),fov=PC.player_camera_manager.get_fov_angle(),viewport=PC.get_viewport_size(),screen_percentage=unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage')));state.update(stage=2,at=time.monotonic());return
  if time.monotonic()-state['at']>.4:
   assert Path(rows[-1]['file']).is_file();state.update(i=state['i']+1,stage=0)
 except Exception:finish(traceback.format_exc())
unreal._wvuphotos=unreal.register_slate_post_tick_callback(tick)
