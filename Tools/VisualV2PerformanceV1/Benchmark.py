"""One explicit benchmark batch. Reuses native pm.EnvPerf2; no game architecture."""
import unreal,json,time,traceback,gc
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1';q=json.loads((D/'Request.json').read_text());O=D/q['label']
if q.get('mode')=='Native':
 O.mkdir(exist_ok=True);assert not(O/'Result.json').exists()
else:O.mkdir(exist_ok=False)
mode=q.get('mode','PIE');W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()if mode=='PIE'else None
if mode=='Native':W=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0))
assert W and unreal._perf1_isolated
DATA=Path(unreal.Paths.project_saved_dir()).resolve()
if mode=='Native':assert DATA.is_relative_to(D/q['label']/'UserData')
GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0)
pp_state=[(a,a.settings.export_text())for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PostProcessVolume)]
material_state=[];component_state=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 for c in a.get_components_by_class(unreal.PrimitiveComponent):
  if mode=='Native'and(isinstance(a,unreal.PokeMonsterCreatureVisualActor)or not isinstance(c,unreal.StaticMeshComponent)):continue
  component_state.append((c,c.is_visible(),c.cast_shadow));material_state.extend((c,i,c.get_material(i))for i in range(c.get_num_materials()))
def restore_action():
 for a,text in pp_state:
  settings=unreal.PostProcessSettings();settings.import_text(text);a.set_editor_property('settings',settings)
 for c,v,sh in component_state:c.set_visibility(v,False);c.set_cast_shadow(sh)
 for c,i,m in material_state:c.set_material(i,m)
def action(name):
 restore_action()
 if name=='OriginalGround':
  source=unreal.load_asset('/Game/Environment/VisualV2EnvironmentV3/Materials/M_EQ3_Ground');assert source
  for c,i,m in material_state:
   if m and m.get_base_material().get_name()in ['M_EQ3_Ground','M_PV1_BakedGroundSRGB']:c.set_material(i,source)
 if name in ['BakedGround','BakedSRGB','BakedGIHalf','BakedGIQuarter','BakedSSGI']:
  new=unreal.load_asset('/Game/Environment/VisualV2PerformanceV1/Materials/M_PV1_BakedGround'+(''if name=='BakedGround'else'SRGB'));assert new
  for c,i,m in material_state:
   if m and m.get_base_material().get_name()=='M_EQ3_Ground':c.set_material(i,new)
 if name in ['BakedGIHalf','BakedGIQuarter','BakedSSGI']:
  for a,text in pp_state:
   if not a.unbound:continue
   settings=a.settings
   if name=='BakedSSGI':
    settings.set_editor_property('bOverride_DynamicGlobalIlluminationMethod',True);settings.set_editor_property('DynamicGlobalIlluminationMethod',unreal.DynamicGlobalIlluminationMethod.SCREEN_SPACE)
   else:
    settings.set_editor_property('bOverride_LumenFinalGatherQuality',True);settings.set_editor_property('LumenFinalGatherQuality',.5 if name=='BakedGIHalf'else .25)
   a.set_editor_property('settings',settings)
 if name in ['RouteField','FieldGround']:
  for c,i,m in material_state:
   if m and m.get_base_material().get_name()in ['M_EQ3_Ground','M_EQ3_MainPath','M_EQ3_NorthPath']:
    suffix=m.get_base_material().get_name().removeprefix('M_EQ3_')
    if name=='FieldGround'and suffix!='Ground':continue
    new=unreal.load_asset('/Game/Environment/VisualV2PerformanceV1/Materials/M_PV1_'+suffix);assert new;c.set_material(i,new)
 if name in ['GroundSimple','PaintSimple']:
  mat=unreal.load_asset('/Game/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_Grass')
  for c,i,m in material_state:
   if m and(m.get_base_material().get_name()=='M_EQ3_Ground'or(name=='PaintSimple'and m.get_base_material().get_name()in ['M_EQ3_MainPath','M_EQ3_NorthPath','M_EQ3_Stream'])):c.set_material(i,mat)
 if name in ['SmallPlantsHidden','SmallPlantsNoShadow']:
  for c,v,sh in component_state:
   m=c.static_mesh if isinstance(c,unreal.StaticMeshComponent)else None
   if m and any(k in m.get_name()for k in ['Grass','Fern','MeadowHerbs','GardenFlowers','GardenHerb']):
    if name=='SmallPlantsHidden':c.set_visibility(False,False)
    else:c.set_cast_shadow(False)
 if name=='SkeletalHidden':
  for c,v,sh in component_state:
   if isinstance(c,unreal.SkeletalMeshComponent):c.set_visibility(False,False)
C=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterWorldClock)if x.get_outer()==GI);E=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==GI);assert not E.is_encounter_active()
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
Save=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==GI)
s={'i':0,'start':True,'wall':time.monotonic()};result={'cases':[],'request':q,'mode':mode,'data_root':str(DATA),'recording':False};original_position=P.get_actor_transform()
def finish(error=None):
 cmd('pm.EnvPerf2.Stop');restore_action();unreal.unregister_slate_post_tick_callback(unreal._perf1_benchmark);P.set_actor_transform(original_position,False,True);result.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(result,indent=2));unreal.log('PERF1_BENCHMARK_DONE '+str(error))
 if mode=='Native':unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
 for n in ['W','GI','PC','P','C','E','original_position','material_state','component_state','c','m']:globals().pop(n,None)
 gc.collect()
def tick(dt):
 try:
  assert time.monotonic()-s['wall']<q.get('timeout',1800)
  if s['i']==len(q['cases']):finish();return
  case=q['cases'][s['i']];label='VGB1_PerfOpt_'+q['label']+'_'+case['name']
  if s['start']:
   if mode=='Native':
    if not s.get('loading',False):
     restore_action();assert Save.load_game();s['loading']=True;return
    if Save.is_load_in_progress():return
    s['loading']=False
   action(case.get('action','Control'))
   s['ground_bindings']=[{'actor':c.get_owner().get_name(),'component':c.get_name(),'slot':i,'material':c.get_material(i).get_path_name()}for c,i,m in material_state if m and m.get_base_material().get_name()in ['M_EQ3_Ground','M_PV1_BakedGroundSRGB']]
   assert len(s['ground_bindings'])==4
   if mode!='Native':
    cmd('pm.WorldClock pause');cmd('pm.WorldClock set 1 '+str(case.get('hour',12))+' 0');cmd('pm.WorldClock speed 1');cmd('pm.WorldClock resume')
   plan=O/(case['name']+'.tsv');rows=[label+'\t'+mode+'\t'+str(q.get('warmup',4))+'\t'+str(q.get('duration',5))]
   for rep in range(1,q.get('repeats',3)+1):rows.append(case['site']+'\t'+case.get('condition','Control')+'\t'+str(rep)+'\t2560\t1440\t'+str(case.get('quality',2))+'\t'+str(case.get('percentage',100)))
   assert not(DATA/'EnvironmentPerfV2'/(label+'_Done.txt')).exists();plan.write_text('\n'.join(rows)+'\n');s.update(start=False,time=time.monotonic(),clock=C.get_time().seconds_of_day);cmd('pm.EnvPerf2.Run '+str(plan));return
  assert not E.is_encounter_active()and not C.is_clock_paused(),'Battle/pause invalidates timing'
  pos=P.get_actor_location()
  if(abs(pos.x+36.6)<.15 and abs(pos.y+47.1)<.15):P.set_actor_location(unreal.Vector(*case['position']),False,True)
  done=DATA/'EnvironmentPerfV2'/(label+'_Done.txt')
  if not done.exists():return
  assert done.read_text()=='Complete';result['cases'].append({'label':label,**case,'ground_bindings':s['ground_bindings'],'clock_before':s['clock'],'clock_after':C.get_time().seconds_of_day,'wall_seconds':time.monotonic()-s['time']});(O/'Progress.json').write_text(json.dumps(result['cases'][-1]));s.update(i=s['i']+1,start=True)
 except Exception:finish(traceback.format_exc())
unreal._perf1_benchmark=unreal.register_slate_post_tick_callback(tick)
