"""Bounded QHD High matrix using the existing native CSV profiler. No recording."""
import unreal,json,time,traceback,gc,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2StabilityV1';q=json.loads((D/'MotionRequest.json').read_text());O=D/q['label'];O.mkdir(exist_ok=False)
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0)
def sub(c):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==GI)
P=unreal.GameplayStatics.get_player_pawn(W,0)
C=sub(unreal.PokeMonsterWorldClock);E=sub(unreal.PokeMonsterEncounterSubsystem);assert unreal._stability_isolated and not E.is_encounter_active()
actors=[a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)if isinstance(a,(unreal.PokeMonsterCreatureVisualActor,unreal.PokeMonsterVisibleWildCreatureActor))];flags=[]
for a in actors:
 cs=[(c,c.is_component_tick_enabled(),c.is_visible()if isinstance(c,unreal.SceneComponent)else None)for c in a.get_components_by_class(unreal.ActorComponent)];flags.append((a,a.is_actor_tick_enabled(),cs))
def population(enabled):
 for a,t,cs in flags:
  a.set_actor_tick_enabled(t if enabled else False)
  for c,t,v in cs:
   c.set_component_tick_enabled(t if enabled else False)
   if isinstance(c,unreal.SceneComponent):c.set_visibility(v if enabled else False,False)
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
cases=q['cases'];result={'cases':[],'actor_count':len(actors),'wild_count':len(unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor)),'without_definition':'None in this recording comparison; all Pokemon enabled' };s={'i':0,'start':True,'wall':time.monotonic()}
def axis(x=0,y=0):
 yaw=math.radians(P.get_movement_basis_yaw());cmd('pm.Input.Axis Gamepad_LeftX '+str(-math.sin(yaw)*x+math.cos(yaw)*y));cmd('pm.Input.Axis Gamepad_LeftY '+str(math.cos(yaw)*x+math.sin(yaw)*y))
def sprint(enabled):
 if P.is_sprint_mode_enabled()!=enabled:cmd('pm.Input.Key Gamepad_LeftThumbstick tap')
def finish(error=None):
 axis();sprint(False)
 cmd('pm.TAAReview.CaptureStop');cmd('pm.EnvPerf2.Stop');population(True);unreal.unregister_slate_post_tick_callback(unreal._stability_perf);result.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(result,indent=2))
 for n in ['W','GI','PC','P','C','E','actors','flags','a','cs','c']:globals().pop(n,None)
 gc.collect()
def tick(dt):
 try:
  assert time.monotonic()-s['wall']<650
  if s['i']==len(cases):finish();return
  case=cases[s['i']];label='VGB1_'+q['label']+'_'+case['name']
  if s['start']:
   axis();sprint(case['activity']=='sprint');population(True);cmd('pm.WorldClock pause');cmd('pm.WorldClock set 1 '+str(case['hour'])+' 0');cmd('pm.WorldClock speed 1');cmd('pm.WorldClock resume');plan=O/(case['name']+'.tsv');rows=[label+'\tPIE\t2\t4']
   for rep in [1,2,3]:
    for site in case.get('sites',['Wald']):rows.append(site+'\tControl\t'+str(rep)+'\t2560\t1440\t2\t100')
   plan.write_text('\n'.join(rows)+'\n');s.update(start=False,time=time.monotonic(),before=C.get_time().seconds_of_day,draining=False,input_index=-1);cmd('pm.EnvPerf2.Run '+str(plan))
   if case.get('mode','none')!='none':
    cmd('pm.TAAReview.ReadbackSlots '+str(case.get('slots',3)))
    capture=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/(q['label']+'_'+case['name']);s['capture']=str(capture);cmd('pm.TAAReview.CaptureStart '+str(capture)+(' slate 30'if case['mode']=='slate'else''))
   (O/'Current.json').write_text(json.dumps({'case':case,'started':time.time()}));return
  assert not E.is_encounter_active()and not C.is_clock_paused(),'Unexpected battle/pause invalidates timing'
  directions=[(1,0),(-1,0)]if case['activity']!='follow'else[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
  index=int((time.monotonic()-s['time'])/.8)%len(directions)
  if index!=s['input_index']:axis(*directions[index]);s['input_index']=index
  done=R/'Saved/EnvironmentPerfV2'/(label+'_Done.txt')
  if not done.exists():return
  assert done.read_text()=='Complete';axis();sprint(False)
  if case.get('mode','none')!='none':
   if not s['draining']:cmd('pm.TAAReview.CaptureStop');s['draining']=True
   if not (Path(s['capture'])/'Complete.txt').exists():return
  result['cases'].append({'label':label,**case,'clock_before':s['before'],'clock_after':C.get_time().seconds_of_day,'wall_seconds':time.monotonic()-s['time']});s.update(i=s['i']+1,start=True);(O/'Progress.json').write_text(json.dumps(result['cases'][-1]))
 except Exception:finish(traceback.format_exc())
unreal._stability_perf=unreal.register_slate_post_tick_callback(tick)
