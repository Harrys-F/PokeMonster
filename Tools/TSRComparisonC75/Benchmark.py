"""Compare the production profiles; never set quality, percentage or viewport here."""
import unreal,json,time,traceback,gc
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/TSRComparisonC75';q=json.loads((D/'Request.json').read_text());O=D/q['label'];mode=q.get('mode','PIE');O.mkdir(exist_ok=mode=='Native');assert not(O/'Result.json').exists();assert unreal._perf1_isolated
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()if mode=='PIE'else next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0));GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0)
def sub(t):return next(x for x in unreal.ObjectIterator(t)if x.get_outer()==GI)
C=sub(unreal.PokeMonsterWorldClock);S=sub(unreal.PokeMonsterSaveSubsystem);E=sub(unreal.PokeMonsterEncounterSubsystem);DATA=Path(unreal.Paths.project_saved_dir()).resolve()
if mode=='Native':assert DATA.is_relative_to(D/q['label']/'UserData')
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
s={'i':0,'new':True,'wall':time.monotonic()};r={'cases':[],'request':q,'mode':mode,'data_root':str(DATA),'recording':False,'controlled_existing_MapTAA_probe':True};original=P.get_actor_transform()
def finish(error=None):
 cmd('pm.EnvPerf2.Stop');cmd('pm.Graphics C');P.set_actor_transform(original,False,True);unreal.unregister_slate_post_tick_callback(unreal._graphics_benchmark);r.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(r,indent=2))
 if mode=='Native':unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
 for n in ['W','GI','PC','P','C','S','E']:globals().pop(n,None)
 gc.collect()
def tick(dt):
 try:
  assert time.monotonic()-s['wall']<q.get('timeout',1800)
  if s['i']==len(q['cases']):finish();return
  case=q['cases'][s['i']];label='VGB1_TSR75_'+q['label']+'_'+case['name']
  if s['new']:
   if mode=='Native':
    if not s.get('loading',False):assert S.load_game();s['loading']=True;return
    if S.is_load_in_progress():return
    s['loading']=False
   else:
    cmd('pm.WorldClock pause');cmd('pm.WorldClock set 1 '+str(case.get('hour',12))+' 0');cmd('pm.WorldClock speed 1');cmd('pm.WorldClock resume')
   if case.get('profile'):cmd('pm.Graphics '+case['profile'])
   sp=unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage');assert sp==case['percentage'],('Profile failed',sp,case)
   s['effective']={n:unreal.SystemLibrary.get_console_variable_float_value(n)for n in ['r.ScreenPercentage','r.DynamicRes.OperationMode','r.TemporalAA.Upsampling','r.AntiAliasingMethod','r.TSR.History.ScreenPercentage','r.TSR.History.UpdateQuality']+['sg.'+n+'Quality'for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading','Landscape']]}
   assert all(v==2 for n,v in s['effective'].items()if n.startswith('sg.'))and s['effective']['r.DynamicRes.OperationMode']==0
   plan=O/(case['name']+'.tsv');plan.write_text('\n'.join([label+'\t'+mode+'\t'+str(q.get('warmup',4))+'\t'+str(q.get('duration',6))]+[case['site']+'\t'+case['condition']+'\t'+str(i+1)+'\t2560\t1440\t2\t'+str(case['percentage'])for i in range(q.get('repeats',1))])+'\n');s.update(new=False,time=time.monotonic(),clock=C.get_time().seconds_of_day);cmd('pm.EnvPerf2.Run '+str(plan));return
  assert not E.is_encounter_active()and not C.is_clock_paused()
  pos=P.get_actor_location()
  if abs(pos.x+36.6)<.15 and abs(pos.y+47.1)<.15:P.set_actor_location(unreal.Vector(*case['position']),False,True)
  done=DATA/'EnvironmentPerfV2'/(label+'_Done.txt')
  if not done.exists():return
  assert done.read_text()=='Complete';r['cases'].append({'label':label,**case,'effective':s['effective'],'clock_before':s['clock'],'clock_after':C.get_time().seconds_of_day,'wall_seconds':time.monotonic()-s['time']});(O/'Progress.json').write_text(json.dumps(r['cases'][-1]));s.update(i=s['i']+1,new=True)
 except Exception:finish(traceback.format_exc())
unreal._graphics_benchmark=unreal.register_slate_post_tick_callback(tick)
