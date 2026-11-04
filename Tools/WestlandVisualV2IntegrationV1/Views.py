"""Matched real QHD regional views; diagnostic placement, no source-map writes."""
import unreal,json,time,math,re,traceback,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualV2IntegrationV1';label=json.loads((D/'Request.json').read_text())['label'];O=D/label;O.mkdir(exist_ok=True);assert not(O/'Result.json').exists();assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D);editor=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=editor.get_game_world()if editor else None;pie=W is not None
if not W:W=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_WestlandRegion'and unreal.GameplayStatics.get_player_pawn(w,0))
P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W);S=next(s for s in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if s.get_outer()==GI);C=next(s for s in unreal.ObjectIterator(unreal.PokeMonsterWorldClock)if s.get_outer()==GI);actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)};ignore=[a for n,a in actors.items()if not n.startswith('WR_Terrain_')]
def cmd(s):unreal.SystemLibrary.execute_console_command(W,s,PC)
cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('DisableAllScreenMessages');rows=[];start=time.monotonic();busy=False
if pie:cmd('pm.WorldClock set 1 12 0');cmd('pm.WorldClock pause')
else:runpy.run_path(str(R/'Tools/WestlandVisualV2IntegrationV1/ClockFixture.py'))['set_hour'](W,PC,S,12)
def ground(x,y):
 hit=unreal.SystemLibrary.line_trace_single(W,unreal.Vector(x,y,16000),unreal.Vector(x,y,-10000),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,ignore,unreal.DrawDebugTrace.NONE);assert hit,(x,y);return float(re.search(r'ImpactPoint=\(X=[^,]+,Y=[^,]+,Z=([^\)]+)',hit.export_text())[1])
def wait(t):
 end=time.monotonic()+t
 while time.monotonic()<end:yield
cases=json.loads((R/'Tools/WestlandVisualV2IntegrationV1/Sites.json').read_text())
for name,a in sorted(actors.items()):
 if isinstance(a,unreal.PokeMonsterBuildingCutaway):
  door=a.door_threshold;t=door.get_world_transform();p=unreal.MathLibrary.transform_location(t,unreal.Vector(-540,0,0));cases.append([name+'_Aussen',p.x,p.y,ground(p.x,p.y),door.get_world_rotation().yaw])
 if isinstance(a,unreal.PokeMonsterNPC):
  p=a.get_actor_location();x,y=p.x+400,p.y+250;cases.append([name,x,y,ground(x,y),math.degrees(math.atan2(-250,-400))+18])
for name in ['WR_Holzbruecke','WR_Steinbruecke']:
 a=actors[name];p=unreal.MathLibrary.transform_location(a.get_actor_transform(),unreal.Vector(-1550,-650,0));q=a.get_actor_location();cases.append([name,p.x,p.y,ground(p.x,p.y),math.degrees(math.atan2(q.y-p.y,q.x-p.x))])
for name,a in sorted(actors.items()):
 if name.startswith('WVI_Encounter_')or name in ['WVI_BoundaryCollision_0_0','WVI_BoundaryCollision_1_0']:
  p=a.get_actor_location();x,y=p.x-420,p.y-320;cases.append([name,x,y,ground(x,y),math.degrees(math.atan2(320,420))])
for yaw in [0,90,180,270]:
 base=cases[5];cases.append(['Heilhaus_'+str(yaw),base[1],base[2],base[3],yaw])
def run():
 while not pie and S.is_load_in_progress():yield
 assert C.get_hour()==12 and C.is_clock_paused()
 for name,x,y,z,yaw in cases:
  P.set_actor_location(unreal.Vector(x,y,z+50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();P.third_person_boom.set_world_rotation(unreal.Rotator(yaw=yaw),False,False);yield from wait(3)
  assert abs(PC.player_camera_manager.get_camera_rotation().pitch+12)<.03;assert PC.get_viewport_size()==(2560,1440);f=O/(name+'.png');cmd('Shot filename="'+str(f)+'" -nosuffix');rows.append(dict(name=name,file=str(f),player=P.get_actor_location().to_tuple(),camera=PC.player_camera_manager.get_camera_location().to_tuple(),rotation=PC.player_camera_manager.get_camera_rotation().to_tuple(),fov=PC.player_camera_manager.get_fov_angle(),hour=C.get_hour(),screen_percentage=unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage')));yield from wait(.35);assert f.exists()
def finish(error=None):
 cmd('EnableAllScreenMessages');unreal.unregister_slate_post_tick_callback(unreal._wvi_views);(O/'Result.json').write_text(json.dumps(dict(passed=error is None,error=error,rows=rows,seconds=time.monotonic()-start,diagnostic_positioning=True),indent=2))
 if pie:unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
 else:unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
gen=run()
def tick(dt):
 global busy
 if busy:return
 busy=True
 try:
  assert time.monotonic()-start<350;next(gen)
 except StopIteration:finish()
 except Exception:finish(traceback.format_exc())
 finally:busy=False
unreal._wvi_views=unreal.register_slate_post_tick_callback(tick)
