"""Observe actual existing habitats/actors. No forced state, profile, spawn or creature relocation.
B-only turns the lighting cycle off; joint review also traverses a full accelerated day.
"""
import unreal,json,time,traceback,gc
from pathlib import Path
gc.collect();R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/DayNightV11AI22';q=json.loads((D/'ReviewRequest.json').read_text());O=D/q['label'];O.mkdir(exist_ok=False);W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0)
def sub(c):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==GI)
C=sub(unreal.PokeMonsterWorldClock);E=sub(unreal.PokeMonsterEncounterSubsystem);S=sub(unreal.PokeMonsterSaveSubsystem);L=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterDayNightSubsystem)if x.get_outer()==W);assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_'+q['label'])
actors=list(unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor));subjects=[a for a in actors if a.overworld_movement.activities_enabled];assert len(subjects)==8 and all(a.overworld_movement.rhythm_enabled for a in subjects)
initial={a.get_name():a.get_actor_transform().export_text()for a in subjects};r={'ordinary_habitats':True,'creature_relocations':False,'forced_activities':False,'joint_lighting':q.get('joint',False),'initials':initial,'samples':[],'checks':[]};s={'i':0,'last':time.monotonic(),'start':time.monotonic(),'sample':0};route=[];memory={}
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def place(x,y):P.set_actor_location(unreal.Vector(x,y,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
def act(n,f,d=.5):route.append((n,f,d))
def check(n,p):
 def f():assert p(),n;r['checks'].append(n)
 act(n,f)
def shot(n):cmd('HighResShot 2560x1440 filename="'+str(O/(n+'.png'))+'"')
def sample():
 t=C.get_time();rows=[]
 for a in subjects:
  m=a.overworld_movement;peer=m.social_partner;body=a.get_component_by_class(unreal.CapsuleComponent)
  assert m.is_inside_habitat(a.get_actor_location()-unreal.Vector(0,0,body.get_scaled_capsule_half_height())),(a.get_name(),'outside original habitat')
  if peer:assert peer.social_partner==m and m.behavior_state==unreal.PokeMonsterOverworldState.SOCIAL and peer.behavior_state!=unreal.PokeMonsterOverworldState.SLEEP
  if m.behavior_state==unreal.PokeMonsterOverworldState.SLEEP:assert m.current_speed==0 and not peer
  rows.append({'actor':a.get_name(),'species':str(a.visual_species.get_internal_id()),'state':str(m.behavior_state),'factor':m.rhythm_activity,'rhythm':str(m.rhythm.rhythm),'offset':m.rhythm_offset_minutes,'remaining':m.activity_remaining,'decisions':m.activity_decisions,'forage':m.forage_completed,'social':m.social_completed,'requests':m.social_requests,'declined':m.social_declined,'partner':peer.get_owner().get_name()if peer else None,'position':a.get_actor_location().to_tuple(),'speed':m.current_speed,'refreshes':m.rhythm_refreshes,'distant':m.activity_distant})
 r['samples'].append({'seconds':time.monotonic()-s['start'],'clock_day':t.day,'clock_seconds':t.seconds_of_day,'phase':str(C.get_phase()),'paused':C.is_clock_paused(),'step':route[s['i']][0],'actors':rows})
 (O/'Progress.json').write_text(json.dumps({'step':s['i'],'last':route[s['i']][0],'clock':t.export_text(),'states':[(x['species'],x['state'])for x in rows]}))
def factors(day):
 for a in subjects:
  m=a.overworld_movement;id=str(a.visual_species.get_internal_id())
  expected=(1 if day else 0)if id in ['Bisasam','Pikachu']else(0 if day else 1)if id in ['Myrapla','Nebulak']else .85 if day and id=='Zunderlauf'else .75 if id=='Zunderlauf'else 0
  assert abs(m.rhythm_activity-expected)<.002,(id,m.rhythm_activity,expected)
 return True
assert not E.is_encounter_active(),'Fresh PIE required'
place(-300,2100);cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');cmd('pm.WorldClock reset');L.set_cycle_enabled(q.get('joint',False))
act('Exact noon for independent day activity',lambda:cmd('pm.WorldClock set 1 12 0'))
check('All six profiles immediately use central noon time',lambda:factors(True))
act('Observe ordinary autonomous noon activities',lambda:None,35)
act('Noon QHD actual game camera',lambda:shot('Noon'),1)
act('Exact night jump',lambda:cmd('pm.WorldClock set 1 22 0'))
check('12 to 22 jump immediately updates every profile',lambda:factors(False))
act('Observe ordinary autonomous night activities',lambda:None,35)
act('Night QHD actual game camera',lambda:shot('Night'),1)
act('Debug clock pause',lambda:cmd('pm.WorldClock pause'))
act('Remember ambient timers and positions',lambda:memory.update(paused=[(a.overworld_movement.activity_remaining,a.get_actor_location().to_tuple())for a in subjects]))
act('Hold actual paused clock',lambda:None,2)
check('Paused world clock freezes ambient activity timers and movement',lambda:memory['paused']==[(a.overworld_movement.activity_remaining,a.get_actor_location().to_tuple())for a in subjects])
for h in [6,18,4,12,22]:
 act('Direct debug jump '+str(h),lambda h=h:cmd('pm.WorldClock set 2 '+str(h)+' 0'))
 act('Weight refresh snapshot '+str(h),lambda:sample())
act('Resume normal existing clock',lambda:cmd('pm.WorldClock reset'))
act('Observe recovery after pause and jumps',lambda:None,5)
if q.get('joint',False):
 for h,mi in [(6,0),(9,0),(12,0),(16,0),(19,0),(22,0),(0,0),(4,30)]:
  act('Joint time '+str(h),lambda h=h,mi=mi:cmd('pm.WorldClock set 3 '+str(h)+' '+str(mi)))
  if h==12:
   act('View original Bisasam group',lambda:place(-650,1000))
   act('Start actual joint behavior clip',lambda:cmd('pm.TAAReview.CaptureStart '+str(R/'Saved/VisualV2TAAIntegrationV1/Recordings/DayRhythmJoint01')+' slate 30'))
  act('Observe joint phase '+str(h),lambda:None,12)
  if h==12:act('Finish actual joint behavior clip',lambda:cmd('pm.TAAReview.CaptureStop'))
  act('Joint QHD '+str(h),lambda n='%02d%02d'%(h,mi):shot('Joint'+n),1)
 act('Full-day start',lambda:(cmd('pm.WorldClock set 8 4 30'),cmd('pm.WorldClock speed 60')))
 act('Observe complete accelerated real clock day',lambda:None,122)
 check('Accelerated day crosses midnight and returns beyond dawn',lambda:C.get_day()>=9 and C.get_time().seconds_of_day>=4.5*3600)
 act('Normal speed restored',lambda:cmd('pm.WorldClock reset'))
check('No unintended encounter throughout ambient observation',lambda:not E.is_encounter_active())
check('Every subject keeps valid enabled native activity and rhythm',lambda:all(a.overworld_movement.activities_enabled and a.overworld_movement.rhythm_enabled and a.overworld_movement.activity_decisions>0 for a in subjects))
def finish(error=None):
 cmd('pm.TAAReview.CaptureStop');cmd('pm.WorldClock reset');L.set_cycle_enabled(True);unreal.unregister_slate_post_tick_callback(unreal._rhythm_review);r.update(passed=error is None,error=error,elapsed=time.monotonic()-s['start']);(O/'Result.json').write_text(json.dumps(r,indent=2));route.clear()
 for n in ['W','GI','P','PC','C','E','S','L','actors','subjects','a','m','peer']:globals().pop(n,None)
def tick(dt):
 try:
  now=time.monotonic();assert now-s['start']<650;assert not E.is_encounter_active(),'Unexpected battle'
  if now-s['sample']>.5:s['sample']=now;sample()
  n,f,d=route[s['i']]
  if now-s['last']<d:return
  f();s.update(i=s['i']+1,last=time.monotonic())
  if s['i']==len(route):finish()
 except Exception:finish(traceback.format_exc())
unreal._rhythm_review=unreal.register_slate_post_tick_callback(tick)
