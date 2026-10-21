"""QHD real-world observation, explicitly using the existing runtime party fixture; no asset/save edits."""
import unreal,time,math,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/StarterPolishV2/VisualAfter02';O.mkdir(exist_ok=False);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);c=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==w);inp=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if x.get_world()==w);move=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==p and x.get_name()=='MoveAction');sprint=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==p and x.get_name()=='SprintHoldAction');e=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==unreal.GameplayStatics.get_game_instance(w));names=['Schiggy','Bisasam','Zunderlauf'];s={'index':-1,'time':100.,'last':unreal.GameplayStatics.get_time_seconds(w),'nextshot':0.,'rows':[],'fixture':'existing runtime party review, unchanged map/camera/scale'}
def cmd(t):unreal.SystemLibrary.execute_console_command(w,t,pc)
def inject(dx=0,dy=0,run=False):
 yaw=math.radians(p.get_movement_basis_yaw());sx=-math.sin(yaw)*dx+math.cos(yaw)*dy;sy=math.cos(yaw)*dx+math.sin(yaw)*dy;inp.inject_input_vector_for_action(move,unreal.Vector(sx,sy,0),[],[]);inp.inject_input_vector_for_action(sprint,unreal.Vector(1 if run else 0,0,0),[],[])
def finish(error=None):
 inject();cmd('pm.TAAReview.CaptureStop');unreal.unregister_slate_post_tick_callback(unreal._polish_visual);s.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(s,indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);delta=now-s['last'];s['last']=now
  if e.is_encounter_active():
   inject();cmd('pm.TAAReview.CaptureStop');v=e.get_presenter().get_view()
   if not v.busy and not v.finished:assert e.get_presenter().try_select_flee();assert e.get_presenter().resolve_selection()
   return
  if p.is_overworld_input_locked():inject();return
  s['time']+=delta
  if s['time']>20:
   cmd('pm.TAAReview.CaptureStop');s['index']+=1
   if s['index']>=len(names):finish();return
   name=names[s['index']];cmd('pm.StarterReview.Party '+name+' '+ ' '.join(x for x in names if x!=name));s.update(time=0.,nextshot=3.,record=False);return
  t=s['time'];name=names[s['index']]
  inject(0 if t<5 or t>=16 else -1 if t<10 else 1,0,t>=11)
  if t>=5 and not s['record']:cmd('pm.TAAReview.CaptureStart '+str(R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('PolishAfter02_'+name)));s['record']=True
  if t>=15:cmd('pm.TAAReview.CaptureStop')
  if t>=s['nextshot']:
   v=c.get_visual();assert v and not v.get_editor_property('hidden');assert pc.get_viewport_size()==(2560,1440);f=O/(name+'_'+str(int(t))+'_QHD.png');cmd('Shot filename='+str(f));s['rows'].append({'name':name,'time':t,'file':str(f),'viewport':pc.get_viewport_size(),'camera':pc.player_camera_manager.get_camera_location().to_tuple(),'rotation':str(pc.player_camera_manager.get_camera_rotation()),'position':v.get_actor_location().to_tuple(),'camera_distance_cm':pc.player_camera_manager.get_camera_location().distance(v.get_actor_location()),'speed_cm_s':v.motion_speed});s['nextshot']+=5
 except Exception:
  import traceback
  finish(traceback.format_exc())
unreal._polish_visual=unreal.register_slate_post_tick_callback(tick)
