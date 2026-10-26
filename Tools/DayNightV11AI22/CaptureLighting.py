"""Real fixed-camera QHD comparison. Only transient reference specimens, no user saves."""
import unreal,json,time,traceback,gc
from pathlib import Path
gc.collect();R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/DayNightV11AI22';q=json.loads((D/'Request.json').read_text());O=D/q['label'];O.mkdir(exist_ok=False);W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0)
def sub(c,outer=GI):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==outer)
C=sub(unreal.PokeMonsterWorldClock);L=sub(unreal.PokeMonsterDayNightSubsystem,W);S=sub(unreal.PokeMonsterSaveSubsystem);G=sub(unreal.PokeMonsterCreatureTestGround,W);assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_'+q['label'])
profiles=[(a,a.get_editor_property('profile'))for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor)]
for a,p in profiles:a.set_editor_property('profile',None)
specs=list(G.specimens[:3]);transforms=[a.get_actor_transform()for a in specs]
for m in G.movements[:3]:m.set_movement_paused(True)
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
cmd('pm.WorldClock pause');cmd('pm.EnvPerf2.Viewport 2560 1440')
for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']:cmd('sg.'+n+'Quality 2')
for n,v in [('r.ScreenPercentage',100),('r.SecondaryScreenPercentage.GameViewport',100),('r.DynamicRes.OperationMode',0)]:cmd(n+' '+str(v))
route=[];s={'i':0,'last':time.monotonic()};result={'actual_pie':True,'rows':[]}
def act(n,f,d=.3):route.append((n,f,d))
def place(pos):
 P.set_actor_location(unreal.Vector(*pos),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();P.set_actor_rotation(unreal.Rotator(yaw=90),False)
 for i,a in enumerate(specs):a.set_actor_location(unreal.Vector(pos[0]+130+i*130,pos[1]+170+i*40,0),False,True)
def shot(n):
 cmd('HighResShot 2560x1440 filename="'+str(O/(n+'.png'))+'"');result['rows'].append({'name':n,'clock':C.get_time().export_text(),'sample':L.get_lighting_sample().export_text(),'player':P.get_actor_location().to_tuple(),'camera':PC.player_camera_manager.get_camera_location().to_tuple(),'rotation':PC.player_camera_manager.get_camera_rotation().to_tuple(),'fov':PC.player_camera_manager.get_fov_angle()})
for view,pos in [('Wiese',[-2100,-1760,50.15]),('Baumkrone',[-1353.161706774002,-775.1272881918381,50.22354983301621])]:
 act('Position '+view,lambda pos=pos:place(pos))
 for h in [6,9,12,19,22,0]:
  act('World time '+str(h),lambda h=h:cmd('pm.WorldClock set 1 '+str(h)+' 0'));act('QHD '+view+str(h),lambda n=view+'%02d00'%h:shot(n),4)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._lighting11capture)
 for a,p in profiles:a.set_editor_property('profile',p)
 for a,t in zip(specs,transforms):a.set_actor_transform(t,False,True)
 for m in G.movements[:3]:m.set_movement_paused(False)
 result.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(result,indent=2));route.clear()
 for n in ['W','GI','P','PC','C','L','S','G','profiles','specs','a','p','m']:globals().pop(n,None)
def tick(dt):
 try:
  n,f,d=route[s['i']]
  if time.monotonic()-s['last']<d:return
  f();s.update(i=s['i']+1,last=time.monotonic());(O/'Progress.json').write_text(json.dumps({'step':s['i'],'last':n}))
  if s['i']==len(route):finish()
 except Exception:finish(traceback.format_exc())
unreal._lighting11capture=unreal.register_slate_post_tick_callback(tick)
