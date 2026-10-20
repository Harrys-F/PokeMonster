"""Separate live-input collision probes. Diagnostic initial positioning, not the no-teleport full footrun."""
import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ArtPassV5';w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0));p=unreal.GameplayStatics.get_player_pawn(w,0);cm=p.get_component_by_class(unreal.CharacterMovementComponent);ss=next(s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if s.get_world()==w);move=next(a for a in unreal.ObjectIterator(unreal.InputAction) if a.get_outer()==p and a.get_name()=='MoveAction');state={'i':0,'t':0.,'placed':False,'rows':[]};points=[('RemedyCabinet',17220,660,17240,17315,1),('Hearth',17150,60,17180,17290,1),('ReadingChair',16940,145,16845,16895,-1)]
def inject(dx):
 yaw=math.radians(p.get_movement_basis_yaw());ss.inject_input_vector_for_action(move,unreal.Vector(-math.sin(yaw)*dx,math.cos(yaw)*dx,0),[],[])
def tick(dt):
 try:
  state['t']+=dt
  if state['i']==len(points):inject(0);unreal.unregister_slate_post_tick_callback(unreal._artv5_collision);(S/'FurnitureCollision.json').write_text(json.dumps({'passed':True,'method':'Diagnostic initial positioning then actual Enhanced Input into and away from each new collider','probes':state['rows']},indent=2));return
  name,x,y,lo,hi,direction=points[state['i']]
  if not state['placed']:p.set_actor_location(unreal.Vector(x,y,50.15),False,True);cm.stop_movement_immediately();state['placed']=True
  if state['t']<.6:inject(0)
  elif state['t']<2.8:inject(direction)
  elif 'blocked_x' not in state:
   inject(0);pos=p.get_actor_location();assert lo<pos.x<hi,(name,pos);assert p.get_velocity().length()<5 and not cm.is_falling();state['blocked_x']=pos.x
  elif state['t']<3.6:inject(-direction)
  else:
   inject(0);assert (p.get_actor_location().x-state['blocked_x'])*direction < -65;state['rows'].append({'furniture':name,'start_x':x,'stopped_x':state['blocked_x'],'walked_away_x':p.get_actor_location().x,'no_fall':True});state.update(i=state['i']+1,t=0.,placed=False);state.pop('blocked_x',None)
 except Exception:
  import traceback
  inject(0);unreal.unregister_slate_post_tick_callback(unreal._artv5_collision);(S/'FurnitureCollisionFailure.txt').write_text(traceback.format_exc());raise
unreal._artv5_collision=unreal.register_slate_post_tick_callback(tick)
