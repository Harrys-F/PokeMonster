"""Read-only-to-disk runtime door diagnosis; compare regular speed, factor3 and original terrain."""
import unreal,json,time,math,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandEnvironmentPolishV2';cfg=json.loads((D/'ActiveNative.json').read_text());O=D/cfg['label'];assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(O)
W=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_WestlandRegion'and unreal.GameplayStatics.get_player_pawn(w,0));P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);CM=P.get_component_by_class(unreal.CharacterMovementComponent);actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)};C=actors['HouseCutaway'];sub=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if x.get_world()==W);move=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==P and x.get_name()=='MoveAction');start=time.monotonic();state={'i':0,'phase':'place','at':start};cases=[(1,False,False),(3,False,False),(3,True,False),(3,True,True)];rows=[];frames=[];restores=[]
def cmd(x):unreal.SystemLibrary.execute_console_command(W,x,PC)
def inject(v=unreal.Vector()):sub.inject_input_vector_for_action(move,v,[],[])
def door(offset,inside=False):
 t=C.relocated_door_threshold if inside else C.door_threshold;q=t.get_world_location();yaw=math.radians(t.get_world_rotation().yaw);return q+unreal.Vector(offset*math.cos(yaw),offset*math.sin(yaw),0)
def steer(q):
 p=P.get_actor_location();dx=q.x-p.x;dy=q.y-p.y;yaw=math.radians(P.get_movement_basis_yaw());x=-math.sin(yaw)*dx+math.cos(yaw)*dy;y=math.cos(yaw)*dx+math.sin(yaw)*dy;t=round(math.atan2(x,y)/(math.pi/4))*math.pi/4;a=round(math.sin(t));b=round(math.cos(t));d=max(1,math.hypot(a,b));inject(unreal.Vector(a/d,b/d,0))
def finish():
 inject();cmd('pm.Input.Key LeftShift up');cmd('pm.Speed 1');(O/'Result.json').write_text(json.dumps(dict(cases=rows,frames=frames,seconds=time.monotonic()-start,diagnostic_only=True),indent=2));unreal.unregister_slate_post_tick_callback(unreal._wep_door);unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
def nextcase(error=None):
 rows.append(dict(case=cases[state['i']],passed=error is None,error=error,position=P.get_actor_location().to_tuple(),flag=C.is_viewer_relocated(),physically_inside=C.is_viewer_in_relocated_room(P.get_actor_location())));inject();cmd('pm.Input.Key LeftShift up');state.update(i=state['i']+1,phase='place',at=time.monotonic());(O/'Progress.json').write_text(json.dumps(rows,indent=2))
def tick(dt):
 try:
  now=time.monotonic();assert now-start<180
  if state['i']>=len(cases):finish();return
  factor,sprint,original=cases[state['i']];phase=state['phase'];elapsed=now-state['at'];p=P.get_actor_location()
  if phase=='place':
   if original:
    for label,a in actors.items():
     if label.startswith('WR_Terrain_'):
      c=a.get_component_by_class(unreal.StaticMeshComponent);src=unreal.load_asset('/Game/Environment/WestlandRegion/Meshes/'+c.static_mesh.get_name().replace('SM_WEP_','SM_WR_'));c.set_static_mesh(src)
     if label.startswith('WEP_'):
      for c in a.get_components_by_class(unreal.PrimitiveComponent):c.set_collision_profile_name('NoCollision')
   q=door(-300);z=q.z-C.door_threshold.get_scaled_box_extent().z+50.15;P.set_actor_location(unreal.Vector(q.x,q.y,z),False,True);CM.stop_movement_immediately();cmd('pm.Speed '+str(factor));state.update(phase='settle',at=now);return
  if elapsed>12:nextcase('door timeout '+phase);return
  if p.z<-500:nextcase('Fell below interior');return
  if phase=='settle'and elapsed>.7:
   if sprint:cmd('pm.Input.Key LeftShift down')
   state.update(phase='enter',at=now)
  elif phase=='enter':
   steer(door(300))
   if C.is_viewer_relocated()and C.is_viewer_in_relocated_room(p):inject();state.update(phase='pause_inside',at=now)
  elif phase=='pause_inside'and elapsed>.6:state.update(phase='center',at=now)
  elif phase=='center':
   q=C.relocated_interior_area.get_world_location();steer(q)
   if math.hypot(q.x-p.x,q.y-p.y)<28:inject();state.update(phase='inner_door',at=now)
  elif phase=='inner_door':
   q=door(90,True);steer(q)
   if math.hypot(q.x-p.x,q.y-p.y)<28:inject();state.update(phase='exit',at=now)
  elif phase=='exit':
   inside=C.is_viewer_in_relocated_room(p);steer(door(-130,True))
   # Mirror the production doorway's absolute mapping for read-only collision inspection.
   fr=C.relocated_door_threshold;to=C.door_threshold;local=unreal.MathLibrary.inverse_transform_location(fr.get_world_transform(),p);dest=unreal.MathLibrary.transform_location(to.get_world_transform(),local);cap=P.get_component_by_class(unreal.CapsuleComponent);parts=unreal.SystemLibrary.capsule_overlap_components(W,dest,cap.get_scaled_capsule_radius(),cap.get_scaled_capsule_half_height(),[unreal.ObjectTypeQuery.ECC_WORLD_STATIC,unreal.ObjectTypeQuery.ECC_WORLD_DYNAMIC],unreal.PrimitiveComponent,[P]);frames.append(dict(case=state['i'],phase=phase,cutaway=C.get_cutaway_amount(),flag=C.is_viewer_relocated(),physically_inside=inside,position=p.to_tuple(),mapped_destination=dest.to_tuple(),overlap=[dict(actor=c.get_owner().get_actor_label(),component=c.get_name())for c in(parts or [])]));
   if not inside and(p-C.door_threshold.get_world_location()).length()<1200:inject();nextcase()
 except Exception:nextcase(traceback.format_exc())
unreal._wep_door=unreal.register_slate_post_tick_callback(tick)
