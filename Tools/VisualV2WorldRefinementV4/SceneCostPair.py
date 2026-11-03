"""Real target-map QHD photos and three CSV samples/site; no persistent runtime changes."""
import unreal,json,time,math,statistics,traceback,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2WorldRefinementV4';label=json.loads((D/'Request.json').read_text())['label'];O=D/label;O.mkdir(exist_ok=True);assert not(O/'Result.json').exists();assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D)
editor=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=editor.get_game_world()if editor else None;pie=W is not None
if not W:W=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0))
assert W and 'Dev_TestMap_VisualV2'in W.get_name();P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);sites=json.loads((R/'Tools/VisualV2WorldRefinementV4/Sites.json').read_text());cases=[(rep,[kind+'_'+n,x,y,yaw])for rep in range(3)for n,x,y,yaw in [['Dorf',-3950,-450,55],['Wiese',-4800,-2100,15]]for kind in (['V3','V4']if rep%2==0 else ['V4','V3'])];rows=[];samples=[];state={'i':0,'phase':'place','at':time.monotonic(),'busy':False};start=last=time.monotonic()
# Position capture fixtures above the actual authored ground, never inside a new hill.
grid={(x,y):z for x,y,z in json.loads((D/'GroundHeightGrid.json').read_text())['new']}
def floorz(x,y):
 xx=math.floor(x/50)*50;yy=math.floor(y/50)*50;t=(x-xx)/50;u=(y-yy)/50
 return (1-u)*((1-t)*grid.get((xx,yy),0)+t*grid.get((xx+50,yy),0))+u*((1-t)*grid.get((xx,yy+50),0)+t*grid.get((xx+50,yy+50),0))
def cmd(s):unreal.SystemLibrary.execute_console_command(W,s,PC)
cv=['r.GPUCsvStatsEnabled','r.VSync','t.MaxFPS'];old={k:unreal.SystemLibrary.get_console_variable_float_value(k)for k in cv}
for k,v in [('r.GPUCsvStatsEnabled',1),('r.VSync',0),('t.MaxFPS',0)]:cmd(k+' '+str(v))
runpy.run_path(str(R/'Tools/VisualV2WorldRefinementV4/Metadata.py'),run_name='__main__');cmd('pm.EnvPerf2.Viewport 2560 1440')
GI=unreal.GameplayStatics.get_game_instance(W);Clock=next(c for c in unreal.ObjectIterator(unreal.PokeMonsterWorldClock)if c.get_outer()==GI);Light=next(c for c in unreal.ObjectIterator(unreal.PokeMonsterDayNightSubsystem)if c.get_outer()==W);original_time=Clock.get_time()
if pie:cmd('pm.WorldClock set 1 12 0');cmd('pm.WorldClock pause')
else:
 Save=next(c for c in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if c.get_outer()==GI);runpy.run_path(str(R/'Tools/VisualV2WorldRefinementV4/ClockFixture.py'))['set_hour'](W,PC,Save,12)

# Reconstruct only saved static scenery in RAM. Never modify a functional actor or disk package.
scenes={k:json.loads((D/v).read_text())['actors']for k,v in [('V3','SceneBefore.json'),('V4','SceneFinal.json')]};runtime={a.get_name():a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)};added=[a for a in runtime.values()if a.get_actor_label().startswith('WR4_')];original_hidden=[a.get_editor_property('hidden')for a in added];scene_proof=[]
def transform(v):
 t=unreal.Transform();t.translation=unreal.Vector(*v[0]);t.rotation=unreal.Quat(*v[1]);t.scale3d=unreal.Vector(*v[2]);return t
assert all(k in runtime for k,v in scenes['V3'].items()if v['class']in ['/Script/Engine.StaticMeshActor','/Script/Engine.Actor'])
def variant(name):
 key='V3'if name.startswith('V3')else'V4'
 for k,row in scenes[key].items():
  if row['class']not in ['/Script/Engine.StaticMeshActor','/Script/Engine.Actor']or row['label'].startswith('WR4_'):continue
  a=runtime[k];a.set_actor_hidden_in_game(row['props'].get('hidden')=='True');components={c.get_name():c for c in a.get_components_by_class(unreal.SceneComponent)}
  for cr in row['components']:
   if cr['name']not in components:
    assert cr['class']in ['/Script/Engine.BillboardComponent','/Script/Engine.ArrowComponent'],('Missing runtime scenery component',k,cr['name'],cr['class']);continue
   c=components[cr['name']];target=transform(cr['transform'])
   if (c.get_world_transform().translation-target.translation).length()>.01:
    mobility=c.mobility;c.set_mobility(unreal.ComponentMobility.MOVABLE);c.set_world_transform(target,False,False);c.set_mobility(mobility)
   assert (c.get_world_transform().translation-target.translation).length()<.02,('Incomplete static transform restoration',k,cr['name'])
   if not isinstance(c,unreal.StaticMeshComponent):continue
   if cr['props'].get('static_mesh')not in [None,'None','']:c.set_static_mesh(unreal.load_asset(cr['props']['static_mesh']))
   for i,path in enumerate(cr.get('materials',[])):c.set_material(i,unreal.load_asset(path)if path else None)
   c.set_visibility(cr['props'].get('visible')=='True',False);c.set_hidden_in_game(cr['props'].get('hidden_in_game')=='True',False);c.set_cast_shadow(cr['props'].get('cast_shadow')=='True')
   if isinstance(c,unreal.InstancedStaticMeshComponent):
    assert c.get_instance_count()==len(cr['instances'])
    for i,t in enumerate(cr['instances']):c.update_instance_transform(i,transform(t),False,False,True)
    if cr['instances']:c.update_instance_transform(0,transform(cr['instances'][0]),False,True,True)
 for a,h in zip(added,original_hidden):a.set_actor_hidden_in_game(True if key=='V3'else h)
 scene_proof.append(dict(variant=key,original_static_actor_transforms_verified=True,all_original_instance_counts_verified=True,temporary_mobility_restored_before_measurement=True))
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._fab_capture)
 try:variant('V4')
 except Exception:error=(error or '')+'\nFixture restore failure: '+traceback.format_exc()
 cmd('csvprofile stop')
 for k,v in old.items():cmd(k+' '+str(v))
 cmd('pm.WorldClock reset')if pie else PC.close_menu();cmd('pm.EnvPerf2.Viewport 0 0');(O/'Result.json').write_text(json.dumps(dict(passed=error is None,error=error,rows=rows,scene_fixture_proof=scene_proof,seconds=time.monotonic()-start,pie=pie,method='Same-process full saved static-scenery V3/V4 reconstruction in RAM, 3 repeats at Dorf/Wiese alternating order, 6s settle+6s samples. Functional actors and gameplay code excluded, no video. Restores V4 before quit. Not a separately booted original V3 map.'),indent=2));unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()if pie else unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
def tick(dt):
 global samples,last
 if state['busy']:return
 state['busy']=True
 try:

  if not pie:
   if Save.is_load_in_progress():return
   assert Clock.get_hour()==12 and Clock.is_clock_paused()
   assert abs(Light.get_lighting_sample().sun_elevation-75)<.03
  now=time.monotonic();delta=(now-last)*1000;last=now;assert now-start<450
  if state['i']>=len(cases):finish();return
  rep,(name,x,y,yaw)=cases[state['i']];elapsed=now-state['at']
  if state['phase']=='place':
   variant(name)
   P.set_actor_location(unreal.Vector(x,y,floorz(x,y)+100.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();P.third_person_boom.set_world_rotation(unreal.Rotator(yaw=yaw),False,False);state.update(phase='warm',at=now);return
  if state['phase']=='warm'and elapsed>6:
   cmd('csvprofile startfile=FAB_'+label+'_'+str(state['i']));cmd('csvprofile start');samples=[];state.update(phase='sample',at=now);return
  if state['phase']=='sample':
   samples.append(delta)
   if elapsed>6:
    cmd('csvprofile stop');ss=sorted(samples);h=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterHabitatSubsystem)if x.get_outer()==W);rows.append(dict(site=name,repeat=rep+1,frames=len(samples),fps=1000/statistics.mean(samples),frame_mean_ms=statistics.mean(samples),p95_ms=ss[int(len(ss)*.95)],player=P.get_actor_location().to_tuple(),camera=PC.player_camera_manager.get_camera_location().to_tuple(),rotation=PC.player_camera_manager.get_camera_rotation().to_tuple(),viewport=PC.get_viewport_size(),screen_percentage=unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage'),active_population=len(h.population),clock=Clock.get_time().export_text(),sun_elevation=Light.get_lighting_sample().sun_elevation,csv_prefix='FAB_'+label+'_'+str(state['i'])))
    assert abs(P.get_actor_location().z-floorz(x,y)-50.15)<90,('Fixture is not on the ground',name,P.get_actor_location());assert PC.get_viewport_size()==(2560,1440),PC.get_viewport_size();assert abs(PC.player_camera_manager.get_camera_rotation().pitch+12)<.03
    if False:cmd('Shot filename="'+str(O/(name+'.png'))+'" -nosuffix')
    state.update(phase='after',at=now);return
  if state['phase']=='after'and elapsed>1:state.update(phase='place',i=state['i']+1,at=now)
 except Exception:finish(traceback.format_exc())
 finally:state['busy']=False
unreal._fab_capture=unreal.register_slate_post_tick_callback(tick)
