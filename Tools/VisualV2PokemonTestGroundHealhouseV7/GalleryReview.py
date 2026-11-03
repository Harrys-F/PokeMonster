"""Real input, interactions, capture, isolated Save/Load and travel. No production mutation."""
import unreal,json,time,math,statistics,traceback,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PokemonTestGroundHealhouseV7';cfg=json.loads((D/'GameplayRequest.json').read_text());O=D/cfg['label'];O.mkdir(exist_ok=True);assert not(O/'Result.json').exists();assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D);ed=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=ed.get_game_world()if ed else None;pie=W is not None
if not W:W=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0))
P=PC=GI=E=C=S=H=Comp=I=Dlg=None;checks=[];distribution=[];shots=[];frames=[];start=last=time.monotonic();lastsample=0;busy=False;profiling_old={}

def valid(obj):
 try:return obj is not None and unreal.SystemLibrary.is_valid(obj)
 except Exception:return False
def sub(cls,outer):return next(x for x in unreal.ObjectIterator(cls)if x.get_outer()==outer)
def bind(w):
 global W,P,PC,GI,E,C,S,H,Comp,I,Dlg,MoveSub,MoveAction
 W=w;P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W);E=sub(unreal.PokeMonsterEncounterSubsystem,GI);C=sub(unreal.PokeMonsterWorldClock,GI);S=sub(unreal.PokeMonsterSaveSubsystem,GI);H=sub(unreal.PokeMonsterHabitatSubsystem,W);Comp=sub(unreal.PokeMonsterCreatureCompanionSubsystem,W);I=sub(unreal.PokeMonsterInventorySubsystem,GI);Dlg=sub(unreal.PokeMonsterDialogueSubsystem,GI);MoveSub=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if x.get_world()==W);MoveAction=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==P and x.get_name()=='MoveAction')
def cmd(s):unreal.SystemLibrary.execute_console_command(W,s,PC)
def inject(x,y):MoveSub.inject_input_vector_for_action(MoveAction,unreal.Vector(x,y,0),[],[])
def steer(x,y):
 p=P.get_actor_location();dx=x-p.x;dy=y-p.y;yaw=math.radians(P.get_movement_basis_yaw());a=-math.sin(yaw)*dx+math.cos(yaw)*dy;b=math.cos(yaw)*dx+math.sin(yaw)*dy;n=max(1,math.hypot(a,b));mag=min(1,max(.2,n/120));inject(a/n*mag,b/n*mag)
def wait(seconds):
 until=time.monotonic()+seconds
 while time.monotonic()<until:yield

def walk(x,y,seconds=35):
 since=time.monotonic()
 while math.dist(P.get_actor_location().to_tuple()[:2],(x,y))>28:
  assert time.monotonic()-since<seconds,('Blocked walk',x,y,P.get_actor_location());steer(x,y);yield
 inject(0,0);checks.append(dict(walk=[x,y],actual=P.get_actor_location().to_tuple()))
def place(a,offset=(-130,0)):
 p=a.get_actor_location();cap=a.get_component_by_class(unreal.CapsuleComponent);z=p.z-cap.get_scaled_capsule_half_height()+50.15 if cap else p.z+50.15;P.set_actor_location(unreal.Vector(p.x+offset[0],p.y+offset[1],z),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();P.set_actor_rotation(unreal.Rotator(yaw=math.degrees(math.atan2(-offset[1],-offset[0]))),False);steer(p.x,p.y)
def shot(name):
 p=O/(name+'.png');cmd('Shot filename="'+str(p)+'" -nosuffix');shots.append(str(p))
def snapshot():return dict(party=[x.export_text()for x in E.get_player_party()],inventory=[x.export_text()for x in I.get_stacks()],position=P.get_actor_location().to_tuple(),clock=C.get_time().export_text(),facing=P.get_interaction_world_direction().to_tuple())
def run():
 bind(W);cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('DisableAllScreenMessages');G=sub(unreal.PokeMonsterCreatureTestGround,W);yield from wait(2)
 party=[x.export_text()for x in E.get_player_party()];origin=P.get_actor_location();facing=P.get_interaction_world_direction();P.third_person_boom.set_world_rotation(unreal.Rotator(yaw=73),False,False);orbit=P.third_person_boom.get_world_rotation().yaw
 cmd('pm.TestGround.List');assert len(G.species)==19 and len(G.get_import_targets())==49
 names=[str(s.get_display_name())for s in G.species];cmd('pm.TestGround.Go');since=time.monotonic()
 while not G.is_collection_ready():assert time.monotonic()-since<240;yield
 assert G.get_physical_model_count()==68;checks.append(dict(collection_count=G.get_physical_model_count(),ready=len(names),static=len(G.import_names),first_load_seconds=time.monotonic()-since,cells=[dict(name=n,center=G.get_station(i).to_tuple(),half_cm=G.cell_half_sizes[i],motion_cm=G.motion_radii[i])for i,n in enumerate(names)],raw=[dict(name=n,center=G.import_stations[i].to_tuple(),dimensions_cm=G.import_dimensions[i].to_tuple())for i,n in enumerate(G.import_names)]))
 assert G.set_mode('idle');assert G.return_to_world();yield from wait(.5)
 for i,name in enumerate(names):
  if cfg.get('water_only')and name not in ['Karpador','Garados']:continue
  cmd('pm.TestGround.Go '+name);yield from wait(.65);assert G.has_return_position()and P.actor_has_tag('PokemonDevelopmentTestVisit');assert abs(P.get_actor_location().z+19949.85)<2
  v=Comp.get_visual();assert v and not v.hidden;assert (v.get_actor_location()-P.get_actor_location()).length()<1000;assert v.get_actor_location().z>-20150,(name,'companion below boardwalk',v.get_actor_location())
  assert G.get_physical_model_count()==68 and not G.specimens[i].hidden
  assert abs(PC.player_camera_manager.get_camera_rotation().pitch+12)<.03
  if name=='Karpador':P.third_person_boom.set_world_rotation(unreal.Rotator(yaw=P.third_person_boom.get_world_rotation().yaw+20),False,False);yield from wait(.4)
  if name in ['Raupy','Pikachu','Glurak','Machomei','Karpador','Garados']:shot('TestGround_'+name);yield from wait(.35)
  q=P.get_actor_location();yield from walk(q.x+35,q.y);yield from walk(q.x,q.y)
  cmd('pm.TestGround.Return');yield from wait(.4);assert (P.get_actor_location()-origin).length()<1;assert (P.get_interaction_world_direction()-facing).length()<1e-6;assert abs(P.third_person_boom.get_world_rotation().yaw-orbit)<.01
  assert [x.export_text()for x in E.get_player_party()]==party;checks.append(dict(ready_target=name,return_cm=(P.get_actor_location()-origin).length(),companion=True,physical=G.get_physical_model_count()))
 for target in ['','1','19','Zunderlauf']:
  cmd('pm.TestGround.Go '+target);yield from wait(.3);assert G.has_return_position();cmd('pm.TestGround.Return');yield from wait(.3)
 cmd('pm.TestGround.Go DefinitelyInvalid');yield from wait(.2);assert not G.has_return_position()and(P.get_actor_location()-origin).length()<1
 if pie:
  editor_world=ed.get_editor_world();unreal.SystemLibrary.execute_console_command(editor_world,'pm.TestGround.Go Pikachu');yield from wait(.5);assert G.has_return_position();unreal.SystemLibrary.execute_console_command(editor_world,'pm.TestGround.Return');yield from wait(.4);assert not G.has_return_position();checks.append('Editor-console context resolves active PIE')
 for index,target in enumerate([]if cfg.get('water_only')else G.get_import_targets()):
  assert G.visit_target(target if index%2 else 'Modell:'+target);yield from wait(.35)
  assert G.set_mode('idle');assert not G.set_mode('walk')and not G.set_mode('run')and not G.react('attack');assert G.set_mode('turn');yield from wait(.2);assert G.set_mode('reset')
  v=G.static_specimens[list(G.import_names).index(target)];b=v.get_actor_bounds(False);assert abs(b[0].z-b[1].z+20000)<.1,(target,b);assert v.static_mesh_component.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION;assert v.get_actor_scale3d()==unreal.Vector(1,1,1)
  assert G.get_physical_model_count()==68 and not v.hidden;assert abs(P.get_actor_location().z+19949.85)<2
  comp=Comp.get_visual();assert comp and(comp.get_actor_location()-P.get_actor_location()).length()<1000 and comp.get_actor_location().z>-20150
  if target in ['Aquana','Entoron','Onyx','Tauboss','Tangela','Zubat']:shot('Static_'+target);yield from wait(.35)
  checks.append(dict(import_target=target,mesh=v.static_mesh_component.static_mesh.get_path_name(),bounds=str(b),static_only=True,physical=G.get_physical_model_count()));assert G.return_to_world();yield from wait(.3)
 # Actual controlled preview paths in each medium, using unchanged animation clips.
 capture_class=runpy.run_path(str(R/'Tools/VisualV2PokemonTestGroundHealhouseV7/ReviewCapture.py'))['ScreenshotReview']
 for name in ([]if cfg.get('water_only')else['Pikachu','Karpador','Garados']):
  assert G.visit_target(name);yield from wait(.4);idx=names.index(name);V=G.specimens[idx];M=G.movements[idx];assert G.set_mode('reset');assert G.set_mode('walk');yield from wait(1)
  startloc=V.get_actor_location();samples=[];since=time.monotonic();cap=capture_class(W,O/('Motion_'+name),unreal.GameplayStatics.get_time_seconds(W))
  while time.monotonic()-since<10:
   cap.tick(unreal.GameplayStatics.get_time_seconds(W));samples.append(dict(seconds=unreal.GameplayStatics.get_time_seconds(W),position=V.get_actor_location().to_tuple(),speed=M.current_speed,swim=V.aquatic_pose_alpha));yield
  cap.stop()
  while not cap.done:cap.tick(unreal.GameplayStatics.get_time_seconds(W));yield
  assert max(x['speed']for x in samples)>0 and M.distance_travelled>50,(name,M.distance_travelled,M.blocked_steps)
  checks.append(dict(model_motion=name,max_speed=max(x['speed']for x in samples),distance_cm=M.distance_travelled,blocked=M.blocked_steps,samples=samples));assert G.set_mode('run');yield from wait(2);assert G.set_mode('turn');yield from wait(1);assert G.set_mode('idle');assert G.return_to_world();yield from wait(.3)
 # Explicit diagnostic overview camera only; the player's Third Person V3 stays untouched.
 assert G.visit(0);yield from wait(.5);transform=unreal.Transform(location=unreal.Vector(-7500,-24700,-13500),rotation=unreal.Rotator(pitch=-90,yaw=0))
 camera=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)if a.actor_has_tag('PokemonDevelopmentPlaque'));old_transform=camera.get_actor_transform();camera.set_actor_hidden_in_game(True);camera.set_actor_transform(transform,False,True);PC.set_view_target_with_blend(camera,0);yield from wait(.5);fov=PC.player_camera_manager.get_fov_angle();altitude=11000/(2*math.tan(math.radians(fov*.5)));camera.set_actor_location(unreal.Vector(-7500,-24700,-20000+altitude),False,True);yield from wait(1);checks.append(dict(diagnostic_overview=True,fov=fov,location=PC.player_camera_manager.get_camera_location().to_tuple(),pitch=PC.player_camera_manager.get_camera_rotation().pitch));shot('TestGround_DiagnosticOverview');yield from wait(.5);PC.set_view_target_with_blend(P,0);camera.set_actor_transform(old_transform,False,True);camera.set_actor_hidden_in_game(False);assert G.return_to_world();yield from wait(.4)
 assert G.is_collection_ready()and G.get_physical_model_count()==68;assert [x.export_text()for x in E.get_player_party()]==party;assert not G.has_return_position();assert (P.get_actor_location()-origin).length()<1;assert all(Path(p).exists()for p in shots);cmd('EnableAllScreenMessages')

def finish(error=None):
 cmd('csvprofile stop');cmd('pm.Speed 1')
 for k,v in profiling_old.items():cmd(k+' '+str(v))
 unreal.unregister_slate_post_tick_callback(unreal._fab_gameplay)
 if valid(P)and valid(MoveAction):inject(0,0)
 (O/'Result.json').write_text(json.dumps(dict(passed=error is None,error=error,checks=checks,distribution=distribution,shots=shots,seconds=time.monotonic()-start,mean_fps=1000/statistics.mean(frames)if frames else None,frame_p95_ms=sorted(frames)[int(len(frames)*.95)]if frames else None,performance_note='Functional tour includes captures/dialogues/load/travel; not an isolated GPU benchmark',isolated_storage=True),indent=2))
 if pie:unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
 else:
  live=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()in ['Dev_TestMap_VisualV2','Dev_TestMap']and unreal.GameplayStatics.get_player_pawn(w,0));unreal.SystemLibrary.quit_game(live,unreal.GameplayStatics.get_player_controller(live,0),unreal.QuitPreference.QUIT,False)
gen=run()if not globals().get('V7_IMPORT_ONLY',False)else None
def tick(dt):
 global busy,last,lastsample
 if busy:return
 busy=True
 try:
  now=time.monotonic();frames.append((now-last)*1000);last=now;assert now-start<900
  if valid(P)and valid(H)and now-lastsample>3:
   lastsample=now;distribution.append(dict(seconds=now-start,position=P.get_actor_location().to_tuple(),population=[dict(species=str(a.visual_species.get_internal_id()),zone=str(a.overworld_movement.biome_habitat.zone_id),state=str(a.overworld_movement.behavior_state),speed=a.overworld_movement.current_speed)for a in H.population if valid(a)]));(O/'Progress.json').write_text(json.dumps(dict(last_check=checks[-1]if checks else None,seconds=now-start,population=len(H.population)),indent=2))
  next(gen)
 except StopIteration:finish()
 except Exception:finish(traceback.format_exc())
 finally:busy=False
if not globals().get('V7_IMPORT_ONLY',False):unreal._fab_gameplay=unreal.register_slate_post_tick_callback(tick)
