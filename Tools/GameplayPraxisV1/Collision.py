"""Existing player/input/physics versus three existing obstacles. Isolated positioning, no map edits."""
import unreal,json,math,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GameplayPraxisV1';req=json.loads((D/'Request.json').read_text());O=D/req['label'];W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W);E=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==GI)
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor):a.overworld_movement.set_movement_paused(True);a.set_actor_enable_collision(False)
actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)};cases=['Tree_01_Trunk','VS_BoundaryRock_0','V2_House_EntranceWall_-310'];s={'i':0,'phase':'place','t':0.,'last':unreal.GameplayStatics.get_time_seconds(W),'rows':[]};start=time.monotonic()
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def axis(x):
 yaw=math.radians(P.get_movement_basis_yaw());cmd('pm.Input.Axis Gamepad_LeftX '+str(-math.sin(yaw)*x));cmd('pm.Input.Axis Gamepad_LeftY '+str(math.cos(yaw)*x))
def phase(n):s.update(phase=n,t=0.)
def finish(error=None):
 axis(0);unreal.unregister_slate_post_tick_callback(unreal._praxis_collision);s.update(passed=error is None,error=error,isolated_positioning_not_footrun=True,input='existing pm.Input.Axis, actual player capsule physics');(O/'Result.json').write_text(json.dumps(s,indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(W);s['t']+=now-s['last'];s['last']=now;assert time.monotonic()-start<100;assert not E.is_encounter_active();name=cases[s['i']];a=actors[name];center,ext=a.get_actor_bounds(True,False);t=s['t']
  if s['phase']=='place':
   axis(0);P.set_actor_location(unreal.Vector(center.x-ext.x-135,center.y,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();s['rows'].append({'actor':name,'center':center.to_tuple(),'extent':ext.to_tuple(),'samples':[]});phase('settle')
  elif s['phase']=='settle'and t>.5:s['rows'][-1]['start']=P.get_actor_location().to_tuple();phase('push')
  elif s['phase']=='push':
   axis(1);row=s['rows'][-1];row['samples'].append(P.get_actor_location().to_tuple())
   if t>2.2:
    axis(0);row['blocked']=P.get_actor_location().to_tuple();assert row['blocked'][0]>row['start'][0]+15 and row['blocked'][0]<center.x-15,(name,'Collision not blocking',row['blocked']);row['forward_attempt_blocked']=True;cmd('HighResShot 2560x1440 filename="'+str(O/(name+'.png'))+'"');phase('back')
  elif s['phase']=='back':
   axis(-1)
   if t>.7:
    axis(0);row=s['rows'][-1];assert P.get_actor_location().x<row['blocked'][0]-45,'Cannot leave obstacle';row['back_away_unblocked']=True;s['i']+=1
    if s['i']==len(cases):finish();return
    phase('place')
 except Exception:finish(traceback.format_exc())
unreal._praxis_collision=unreal.register_slate_post_tick_callback(tick)
