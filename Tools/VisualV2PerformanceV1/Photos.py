"""Matched genuine QHD pairs. World paused only for photographs, never timings."""
import unreal,json,time,traceback,gc
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1';req=json.loads((D/'PhotoRequest.json').read_text());O=D/req['label'];O.mkdir(exist_ok=False);W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W and unreal._perf1_isolated;GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0);C=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterWorldClock)if x.get_outer()==GI)
hills=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.StaticMeshActor):
 c=a.static_mesh_component;m=c.get_material(0)
 if m and m.get_base_material().get_name()=='M_EQ3_Ground':hills.append((c,m))
assert len(hills)==4;new=unreal.load_asset(req.get('material','/Game/Environment/VisualV2PerformanceV1/Materials/M_PV1_BakedGround'));assert new
route=[];state={'i':0,'last':time.monotonic()};result={'shots':[],'actual_unreal_pie':True,'render_resolution':[2560,1440],'timing_measurement':False,'candidate_material':new.get_path_name()};original=P.get_actor_transform()
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def act(n,f,delay=1):route.append((n,f,delay))
def material(baked):
 for c,m in hills:c.set_material(0,new if baked else m)
def place(row):
 unreal.GameplayStatics.set_game_paused(W,False);material(False);cmd('pm.WorldClock pause');cmd('pm.WorldClock set 1 '+str(row['hour'])+' 0');P.set_actor_location(unreal.Vector(*row['position']),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
def shot(name,variant):
 file=O/(name+'_'+variant+'.png');assert not file.exists();cmd('HighResShot 2560x1440 filename="'+str(file)+'"');result['shots'].append({'name':name,'variant':variant,'file':str(file.relative_to(R)),'world_seconds':unreal.SystemLibrary.get_game_time_in_seconds(W),'clock':C.get_time().export_text(),'player':P.get_actor_location().to_tuple(),'camera':PC.player_camera_manager.get_camera_location().to_tuple(),'rotation':PC.player_camera_manager.get_camera_rotation().to_tuple(),'fov':PC.player_camera_manager.get_fov_angle(),'world_paused':unreal.GameplayStatics.is_game_paused(W)})
for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']:cmd('sg.'+n+'Quality 2')
cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');cmd('r.DynamicRes.OperationMode 0')
for row in req['rows']:
 name=row['name'];act(name+' place',lambda r=row:place(r));act(name+' freeze',lambda:unreal.GameplayStatics.set_game_paused(W,True),2);act(name+' original',lambda n=name:shot(n,'Original'),2);act(name+' candidate',lambda:material(True),1);act(name+' baked',lambda n=name:shot(n,'Baked'),2)
act('Wait for final render request',lambda:None,2)
def finish(error=None):
 material(False);unreal.GameplayStatics.set_game_paused(W,False);cmd('pm.WorldClock resume');P.set_actor_transform(original,False,True);unreal.unregister_slate_post_tick_callback(unreal._perf1_photos);result.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(result,indent=2));route.clear();unreal.log('PERF1_PHOTOS_DONE '+str(error))
def tick(dt):
 try:
  n,f,delay=route[state['i']]
  if time.monotonic()-state['last']<delay:return
  f();state.update(i=state['i']+1,last=time.monotonic());(O/'Progress.json').write_text(json.dumps({'step':state['i'],'last':n}))
  if state['i']==len(route):finish()
 except Exception:finish(traceback.format_exc())
unreal._perf1_photos=unreal.register_slate_post_tick_callback(tick)
