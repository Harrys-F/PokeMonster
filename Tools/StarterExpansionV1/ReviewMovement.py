"""Real-time PIE observation + Enhanced Input sprint route; never writes a save or map."""
import unreal,json,time,math,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();label=json.loads((R/'Saved/StarterExpansionV1/MovementReviewRequest.json').read_text())['label'];O=R/'Saved/StarterExpansionV1'/label;assert O.exists()and not(O/'Result.json').exists();w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w)
def sub(cls,outer):return next(x for x in unreal.ObjectIterator(cls)if x.get_outer()==outer)
e=sub(unreal.PokeMonsterEncounterSubsystem,gi);comp=sub(unreal.PokeMonsterCreatureCompanionSubsystem,w);inp=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if x.get_world()==w);move=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==p and x.get_name()=='MoveAction');sprint=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==p and x.get_name()=='SprintHoldAction');wild=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor);assert len(wild)==3
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
def cmd(t):unreal.SystemLibrary.execute_console_command(w,t,pc)
def inject(dx=0,dy=0,run=False):
 yaw=math.radians(p.get_movement_basis_yaw());sx=-math.sin(yaw)*dx+math.cos(yaw)*dy;sy=math.cos(yaw)*dx+math.sin(yaw)*dy;n=max(1,math.hypot(sx,sy));inp.inject_input_vector_for_action(move,unreal.Vector(sx/n,sy/n,0),[],[]);inp.inject_input_vector_for_action(sprint,unreal.Vector(1 if run else 0,0,0),[],[])
cmd('pm.StarterReview.Party Schiggy Bisasam Zunderlauf');cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100')
route=[(-760,-1160),(-760,-820),(-500,-540),(-350,-490),(-350,-130),(-20,-40),(220,160),(-20,-40),(-350,-130),(-350,-490),(-500,-540),(-760,-820),(-760,-1160),(-760,-1410)]
s={'phase':'observe','time':0.,'total':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'rows':[],'wild':{str(a.encounter_id):{'origin':a.get_actor_location().to_tuple(),'maximum_displacement':0.,'maximum_step':0.,'last':a.get_actor_location().to_tuple()}for a in wild},'route_index':0,'max_player_speed':0.,'max_companion_speed':0.,'max_companion_distance':0.,'recall_samples':0,'last_sample':-1.,'companion_clips':{},'no_test_teleports':True};log=(O/'Frames.jsonl').open('w')
def phase(v):s.update(phase=v,time=0.)
def shot(n):
 cmd('Shot showui filename='+str(O/(n+'.png')));cmd('pm.CreatureReview.CaptureLiveUI Starter_'+label+'_'+n)
def finish(error=None):
 inject();unreal.unregister_slate_post_tick_callback(unreal._starter_movement);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);log.close();slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';s.update(passed=error is None,error=error,save_after_sha256=hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None);(O/'Result.json').write_text(json.dumps(s,indent=2));unreal.log('STARTER_MOVEMENT_REVIEW_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);delta=now-s['last'];s['last']=now;s['time']+=delta;s['total']+=delta;assert time.monotonic()-s['wall']<420
  v=comp.get_visual();m=comp.get_movement()
  if (not v or not m)and s['total']<2:return
  assert v and m,'No companion';ps=p.get_velocity().length();s['max_player_speed']=max(s['max_player_speed'],ps);distance=p.get_actor_location().distance(v.get_actor_location());s['max_companion_distance']=max(s['max_companion_distance'],distance)
  if s['total']-s['last_sample']>.2:
   elapsed=s['total']-s['last_sample'];s['last_sample']=s['total'];row={'t':s['total'],'phase':s['phase'],'player':p.get_actor_location().to_tuple(),'companion':v.get_actor_location().to_tuple(),'distance':distance,'recall':m.recalling,'companion_plans':m.successful_plans,'companion_blocks':m.blocked_steps,'goal':m.current_goal.to_tuple(),'wild':{}}
   s['max_companion_speed']=max(s['max_companion_speed'],v.motion_speed)
   s['last_companion']=v.get_actor_location().to_tuple();s['recall_samples']+=int(m.recalling)
   assert all(c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION for c in v.get_components_by_class(unreal.PrimitiveComponent))
   for a in wild:
    k=str(a.encounter_id);d=s['wild'][k];q=a.get_actor_location();d['maximum_displacement']=max(d['maximum_displacement'],q.distance(unreal.Vector(*d['origin'])));d['maximum_step']=max(d['maximum_step'],q.distance(unreal.Vector(*d['last'])));d['last']=q.to_tuple();mm=a.overworld_movement;assert mm.is_inside_habitat(q-unreal.Vector(0,0,a.get_component_by_class(unreal.CapsuleComponent).get_scaled_capsule_half_height())),k;row['wild'][k]={'position':q.to_tuple(),'distance_travelled':mm.distance_travelled,'plans':mm.successful_plans,'blocked':mm.blocked_steps}
   log.write(json.dumps(row)+'\n')
  if s['phase']=='observe':
   inject()
   if s['time']>3 and not s.get('initial_shot'):shot('Idle');s['initial_shot']=True
   if s['time']>25:
    for a in wild:
     k=str(a.encounter_id);d=s['wild'][k];mm=a.overworld_movement;d.update(distance_travelled=mm.distance_travelled,plans=mm.successful_plans,blocked=mm.blocked_steps);assert d['maximum_displacement']>100,(k,d)
    s['rows'].append({'free_wild_pass':True});phase('route')
  elif s['phase']=='route':
   if e.is_encounter_active():
    inject();view=e.get_presenter().get_view()
    if not view.busy and not view.finished:assert e.get_presenter().try_select_flee();assert e.get_presenter().resolve_selection()
    return
   if p.is_overworld_input_locked():inject();return
   idx=s['route_index']
   if idx==len(route):inject();assert s['max_player_speed']>=314 and s['recall_samples']>0;phase('settle');return
   target=route[idx];q=p.get_actor_location();dx=target[0]-q.x;dy=target[1]-q.y
   if math.hypot(dx,dy)<20:inject();s['route_index']+=1;s['time']=0.;s['rows'].append({'waypoint':idx,'position':q.to_tuple(),'companion_distance':distance});return
   inject(dx,dy,True)
   if idx in [1,4] and s['total']-s.get('last_sequence',0)>.35:
    count=s.get('sequence_count',0);shot('WalkSequence_'+str(count).zfill(3));s['sequence_count']=count+1;s['last_sequence']=s['total']
   assert s['time']<25,('Route stuck',idx,q)
   if s['total']-s.get('last_shot',0)>3:shot('Sprint_'+str(idx));s['last_shot']=s['total']
  elif s['phase']=='settle':
   inject()
   if distance<300 and s['time']>4:phase('battle_start')
   assert s['time']<25,('Recall failed',distance)
  elif s['phase']=='battle_start':
   cmd('pm.StarterReview.Start classic Schiggy Bisasam');assert e.is_encounter_active();assert v.get_editor_property('hidden');s['paused_positions']={str(a.encounter_id):a.get_actor_location().to_tuple()for a in wild};phase('battle_pause')
  elif s['phase']=='battle_pause'and s['time']>3:
   assert v.get_editor_property('hidden');assert all(a.get_actor_location().distance(unreal.Vector(*s['paused_positions'][str(a.encounter_id)]))<.01 for a in wild);shot('ClassicPaused');s['rows'].append({'classic_pause_pass':True});phase('flee')
  elif s['phase']=='flee':
   if not e.is_encounter_active()and not p.is_overworld_input_locked():phase('returned');return
   if e.is_encounter_active():
    pr=e.get_presenter();view=pr.get_view()
    if not view.busy and not view.finished:assert pr.try_select_flee();assert pr.resolve_selection()
  elif s['phase']=='returned'and s['time']>3:
   assert not v.get_editor_property('hidden');assert len([a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterCreatureVisualActor)if 'CreaturePartyCompanion'in [str(t)for t in a.tags]])==1;s['rows'].append({'battle_return_one_companion':True});s['companion_clips']['Schiggy']=v.mesh.get_skeletal_mesh_asset().get_path_name();cmd('pm.StarterReview.Party Bisasam Schiggy Zunderlauf');phase('bisasam')
  elif s['phase']=='bisasam'and s['time']>4:
   assert 'Bisasam'in comp.get_visual().mesh.get_skeletal_mesh_asset().get_path_name();shot('BisasamCompanion');s['companion_clips']['Bisasam']=True;cmd('pm.StarterReview.Party Zunderlauf Schiggy Bisasam');phase('zunderlauf')
  elif s['phase']=='zunderlauf'and s['time']>4:
   assert 'Glumanda'in comp.get_visual().mesh.get_skeletal_mesh_asset().get_path_name();shot('GlumandaCompanion');s['companion_clips']['Zunderlauf']=True;finish()
 except Exception:
  import traceback
  finish(traceback.format_exc())
unreal._starter_movement=unreal.register_slate_post_tick_callback(tick)
