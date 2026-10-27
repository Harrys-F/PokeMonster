"""Native Shot, not HighResShot: preserve the live 75% TAAU pipeline."""
import unreal,json,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GraphicsVariantC';q=json.loads((D/'PhotoRequest.json').read_text());O=D/q['label'];O.mkdir(exist_ok=False);W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W and unreal._perf1_isolated;PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0);GI=unreal.GameplayStatics.get_game_instance(W);clock=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterWorldClock)if x.get_outer()==GI);original=P.get_actor_transform();route=[];s={'i':0,'last':time.monotonic()};r={'shots':[],'actual_pie':True,'native_viewport_shot':True,'timing_measurement':False}
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def step(n,f,d=2):route.append((n,f,d))
def place(row):
 unreal.GameplayStatics.set_game_paused(W,False);cmd('pm.WorldClock pause');cmd('pm.WorldClock set 1 '+str(row['hour'])+' 0');P.set_actor_location(unreal.Vector(*row['position']),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
def shot(row,profile):
 file=O/(row['name']+'_'+profile+'.png');assert not file.exists();cmd('Shot filename="'+str(file)+'" -nosuffix');r['shots'].append({'file':str(file.relative_to(R)),'profile':profile,'percentage':unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage'),'clock':clock.get_time().export_text(),'world_seconds':unreal.GameplayStatics.get_time_seconds(W),'position':P.get_actor_location().to_tuple(),'camera':PC.player_camera_manager.get_camera_location().to_tuple(),'rotation':PC.player_camera_manager.get_camera_rotation().to_tuple(),'fov':PC.player_camera_manager.get_fov_angle()})
for row in q['rows']:
 step(row['name']+' place',lambda row=row:place(row));step('freeze',lambda:unreal.GameplayStatics.set_game_paused(W,True))
 for p in ['100','C']:
  step('profile '+p,lambda p=p:cmd('pm.Graphics '+p));step('settle '+p,lambda:None,3);step('shot '+p,lambda row=row,p=p:shot(row,p),1)
step('Final shot complete',lambda:None,2)
def finish(error=None):

 for entry in r['shots']:
  expected=R/entry['file'];matches=list(expected.parent.glob(expected.stem+'*.png'));assert len(matches)==1,(expected,matches);entry['file']=str(matches[0].relative_to(R))
 cmd('pm.Graphics C');unreal.GameplayStatics.set_game_paused(W,False);cmd('pm.WorldClock reset');P.set_actor_transform(original,False,True);unreal.unregister_slate_post_tick_callback(unreal._graphics_photos);r.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(r,indent=2));route.clear()
def tick(dt):
 try:
  n,f,d=route[s['i']]
  if time.monotonic()-s['last']<d:return
  f();s.update(i=s['i']+1,last=time.monotonic());(O/'Progress.json').write_text(json.dumps({'step':s['i'],'name':n}))
  if s['i']==len(route):finish()
 except Exception:finish(traceback.format_exc())
unreal._graphics_photos=unreal.register_slate_post_tick_callback(tick)
