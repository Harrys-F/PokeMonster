"""Short real Enhanced Input walk/sprint in the already isolated PIE, no save writes."""
import unreal,math,time,json,traceback
from pathlib import Path
D=Path(unreal.Paths.project_dir())/'Saved/ProjectRefinement/GaradosWaterV2';W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);I=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if 'LocalPlayer'in x.get_outer().get_class().get_name());actions=[x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==P];Move=next(x for x in actions if x.get_name()=='MoveAction');Sprint=next(x for x in actions if x.get_name()=='SprintToggleAction');s={'start':time.monotonic(),'sprint':False,'origin':P.get_actor_location().to_tuple()};r={'samples':[]};assert not P.is_overworld_input_locked()
def axis(x):
 y=math.radians(P.get_movement_basis_yaw());I.inject_input_vector_for_action(Move,unreal.Vector(-math.sin(y)*x,math.cos(y)*x,0),[],[])
def finish(error=None):
 axis(0)
 if s['sprint']:I.inject_input_vector_for_action(Sprint,unreal.Vector(1,0,0),[],[])
 P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();P.set_actor_location(unreal.Vector(*s['origin']),False,True);unreal.unregister_slate_post_tick_callback(unreal._garados_foot);r.update(passed=error is None,error=error);(D/'PIEFoot.json').write_text(json.dumps(r,indent=2))
def tick(dt):
 try:
  elapsed=time.monotonic()-s['start'];axis(1);r['samples'].append({'time':elapsed,'position':P.get_actor_location().to_tuple(),'velocity':P.get_velocity().length()})
  if elapsed>1.5 and not s['sprint']:I.inject_input_vector_for_action(Sprint,unreal.Vector(1,0,0),[],[]);s['sprint']=True
  if elapsed>2.6:
   assert max(x['velocity']for x in r['samples']if x['time']<1.5)>100;assert max(x['velocity']for x in r['samples']if x['time']>1.5)>250;assert (P.get_actor_location()-unreal.Vector(*s['origin'])).length()>200;finish()
 except Exception:finish(traceback.format_exc())
unreal._garados_foot=unreal.register_slate_post_tick_callback(tick)
