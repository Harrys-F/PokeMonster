"""Targeted steady-outdoor companion distance and sprint catch-up, excluding relocated-interior transitions."""
import unreal,json,math,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GameplayPraxisV1';req=json.loads((D/'Request.json').read_text());O=D/req['label'];W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W);E=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==GI);C=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==W)
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor):a.overworld_movement.set_movement_paused(True);a.set_actor_enable_collision(False)
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def axis(x,y):cmd('pm.Input.Axis Gamepad_LeftX '+str(x));cmd('pm.Input.Axis Gamepad_LeftY '+str(y))
def l3():
 for k in ['down','up']:cmd('pm.Input.Key Gamepad_LeftThumbstick '+k)
original=P.is_sprint_mode_enabled()
if original:l3()
cmd('pm.StarterReview.Party Zunderlauf Schiggy Bisasam');P.set_actor_location(unreal.Vector(-2100,-1760,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();s={'time':0.,'last':unreal.GameplayStatics.get_time_seconds(W),'samples':[]};start=time.monotonic()
def finish(error=None):
 axis(0,0)
 if P.is_sprint_mode_enabled()!=original:l3()
 unreal.unregister_slate_post_tick_callback(unreal._praxis_follower);s.update(passed=error is None,error=error,isolated_setup='Existing starter party; outdoor diagnostic start, wild encounters paused only in this fixture',no_in_motion_teleports=True);(O/'Result.json').write_text(json.dumps(s,indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(W);s['time']+=now-s['last'];s['last']=now;t=s['time'];assert time.monotonic()-start<70;assert not E.is_encounter_active();v=C.get_visual()
  if t<1:axis(0,0)
  elif t<3.5:axis(0,1)
  elif t<6:
   if not P.is_sprint_mode_enabled():l3()
   axis(1,0)
  elif t<8.5:
   if P.is_sprint_mode_enabled():l3()
   axis(0,-1)
  else:axis(0,0)
  if t>1 and v and not v.get_editor_property('hidden'):
   assert len([a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterCreatureVisualActor)if'CreaturePartyCompanion'in[str(x)for x in a.tags]])==1
   d=P.get_actor_location()-v.get_actor_location();distance=math.hypot(d.x,d.y);assert distance<850,('Companion failed to follow outdoors',distance);s['samples'].append({'time':t,'distance_xy_cm':distance,'player':P.get_actor_location().to_tuple(),'companion':v.get_actor_location().to_tuple(),'player_speed':P.get_velocity().length(),'sprint':P.is_sprinting()})
  if t>11.5:
   assert v and not v.get_editor_property('hidden')and s['samples'][-1]['distance_xy_cm']<400;assert len(s['samples'])>30;s['max_distance_xy_cm']=max(x['distance_xy_cm']for x in s['samples']);s['settled_distance_xy_cm']=s['samples'][-1]['distance_xy_cm'];s['max_player_speed_cm_s']=max(x['player_speed']for x in s['samples']);cmd('HighResShot 2560x1440 filename="'+str(O/'FollowerSettled.png')+'"');finish()
 except Exception:finish(traceback.format_exc())
unreal._praxis_follower=unreal.register_slate_post_tick_callback(tick)
