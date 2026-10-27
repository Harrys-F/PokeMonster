"""Opt-in comparison of 8/4 VSM rays; no map, asset, config or user-save writes.
The launcher must supply a fresh private UserDir containing a copied QA save.
"""
import unreal,json,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/MaterialShadowV3';q=json.loads((D/'VSMRequest.json').read_text());O=D/q['label'];DATA=Path(unreal.Paths.project_saved_dir()).resolve();assert DATA.is_relative_to(O/'UserData')
s={'start':time.monotonic(),'phase':'startup','loaded':False,'i':0,'new':True};r={'cases':[],'isolated_data':str(DATA),'no_recording':True};original={}
VARS='r.ScreenPercentage r.TemporalAA.Upsampling r.DynamicRes.OperationMode r.Shadow.Virtual.Enable r.Shadow.Virtual.SMRT.RayCountDirectional r.Shadow.Virtual.SMRT.SamplesPerRayDirectional r.Shadow.Virtual.ResolutionLodBiasDirectional r.DistanceFieldShadowing r.Lumen.HardwareRayTracing r.Lumen.HardwareRayTracing.Inline r.Lumen.TraceMeshSDFs.Allow r.Lumen.ScreenProbeGather.DownsampleFactor r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor r.Lumen.Reflections.Allow r.RayTracing.Enable r.VSync t.MaxFPS'.split()
def val(n):return unreal.SystemLibrary.get_console_variable_float_value(n)
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def change(n,v):
 if n not in original:original[n]=val(n)
 cmd(n+' '+str(v))
def place(p):P.set_actor_location(unreal.Vector(*p),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
def clock(h):
 assert C.get_path_name().startswith('/Engine/Transient.')
 cmd('setnopec '+C.get_path_name()+' Time (Day=1,SecondsOfDay='+str(h*3600.)+')');assert C.get_hour()==h;L.refresh_lighting()
def finish(error=None):
 try:
  cmd('pm.EnvPerf2.Stop')
  for k,v in original.items():cmd(k+' '+str(v))
  r['cvars_restored']={k:val(k)==v for k,v in original.items()}
 except Exception:r['restore_error']=traceback.format_exc()
 unreal.unregister_slate_post_tick_callback(unreal._msv3_vsm_probe);r.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(r,indent=2));unreal.SystemLibrary.quit_game(W if'W'in globals()else None,PC if'PC'in globals()else None,unreal.QuitPreference.QUIT,False)
def tick(dt):
 global W,GI,PC,P,C,S,E,L
 try:
  assert time.monotonic()-s['start']<q['timeout'],'Observation timeout'
  if s['phase']=='startup':
   if time.monotonic()-s['start']<12:return
   worlds=[w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0)]
   if not worlds:return
   W=worlds[0];GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0)
   def sub(t,outer=GI):return next(x for x in unreal.ObjectIterator(t)if x.get_outer()==outer)
   C=sub(unreal.PokeMonsterWorldClock);S=sub(unreal.PokeMonsterSaveSubsystem);E=sub(unreal.PokeMonsterEncounterSubsystem);L=sub(unreal.PokeMonsterDayNightSubsystem,W)
   if not s['loaded']:assert S.load_game();s['loaded']=True;return
   if S.is_load_in_progress():return
   assert C.get_real_minutes_per_day()==120 and not E.is_encounter_active()
   wild=unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor)
   for a in wild:a.set_editor_property('profile',None) # RAM-only contact suppression; movement stays active.
   r['wild_instances']=len(wild);r['cvars']={n:val(n)for n in VARS};r['high']={n:val('sg.'+n+'Quality')for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading','Landscape']}
   assert all(v==2 for v in r['high'].values())and val('r.ScreenPercentage')==75
   assert val('r.Shadow.Virtual.Enable')==1 and val('r.DistanceFieldShadowing')==1 and val('r.Lumen.HardwareRayTracing')==1
   r['request']=q;(O/'InitialInventory.json').write_text(json.dumps(r,indent=2));s.update(phase='bench',new=True);return
  if s['i']==len(q['cases']):finish();return
  case=q['cases'][s['i']];label='MSV3_'+q['label']+'_'+case['name']
  if s['new']:
   if 'vsm_rays'in case:change('r.Shadow.Virtual.SMRT.RayCountDirectional',case['vsm_rays'])
   if q.get('expected_production_rays')is not None:assert val('r.Shadow.Virtual.SMRT.RayCountDirectional')==q['expected_production_rays']
   clock(case['hour']);place(case['position']);plan=O/(case['name']+'.tsv');plan.write_text(label+'\tNative\t'+str(q['warmup'])+'\t'+str(q['duration'])+'\nS_'+case['site']+'\tGraphicsProfileActive\t'+str(case['repeat'])+'\t2560\t1440\t2\t75\n');s.update(new=False,at=time.monotonic());cmd('pm.EnvPerf2.Run '+str(plan));return
  p=P.get_actor_location()
  if abs(p.x+36.6)<.15 and abs(p.y+47.1)<.15:place(case['position'])
  assert not E.is_encounter_active()and not C.is_clock_paused()
  done=DATA/'EnvironmentPerfV2'/(label+'_Done.txt')
  if not done.exists():return
  assert done.read_text()=='Complete';row={**case,'label':label,'runtime_vsm_rays':val('r.Shadow.Virtual.SMRT.RayCountDirectional'),'wall_seconds':time.monotonic()-s['at'],'position':P.get_actor_location().to_tuple(),'interior_basis':P.is_using_interior_movement_basis()};r['cases'].append(row);(O/'Progress.json').write_text(json.dumps(row));(O/'Partial.json').write_text(json.dumps(r,indent=2));s.update(i=s['i']+1,new=True)
 except Exception:finish(traceback.format_exc())
unreal._msv3_vsm_probe=unreal.register_slate_post_tick_callback(tick)
