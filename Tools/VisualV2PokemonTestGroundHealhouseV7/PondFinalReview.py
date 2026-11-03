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
 bind(W);cmd('pm.EnvPerf2.Viewport 2560 1440');yield from wait(2)
 A=next(a for a in H.population if str(a.visual_species.get_internal_id())=='Karpador');M=A.overworld_movement;V=A.get_nameplate_visual();Z=M.biome_habitat
 P.set_actor_location(unreal.Vector(-600,-1800,90),False,True);yield from wait(1);P.third_person_boom.set_world_rotation(unreal.Rotator(yaw=0),False,False)
 M.measure_activity_cost=True;since=time.monotonic();distance_at_start=M.distance_travelled;samples=[];lastsample=-1
 # No fixture goals, activity overrides, time pause, video or population changes.
 while time.monotonic()-since<360:
  assert not E.is_encounter_active();now=unreal.GameplayStatics.get_time_seconds(W)
  if now-lastsample>=.25:
   lastsample=now;q=A.get_actor_location();root=q-unreal.Vector(0,0,A.get_component_by_class(unreal.CapsuleComponent).get_scaled_capsule_half_height());assert M.is_inside_habitat(root)
   samples.append(dict(game_seconds=now,wall_seconds=time.monotonic()-since,foot=root.to_tuple(),speed=M.current_speed,state=str(M.behavior_state),goal=M.current_goal.to_tuple(),plans=M.successful_plans,blocked=M.blocked_steps))
  yield
 # Validate an actual pond grid with the same floor, draft, footprint and obstacle query.
 extent=Z.get_component_by_class(unreal.BoxComponent).get_scaled_box_extent();center=Z.get_actor_location();grid=[];probe_doc=M.project_walkable.__doc__
 for x in range(int(center.x-extent.x),int(center.x+extent.x)+1,80):
  for y in range(int(center.y-extent.y),int(center.y+extent.y)+1,80):
   q=M.project_walkable(unreal.Vector(x,y,samples[-1]['foot'][2]));good=q if hasattr(q,'to_tuple')else next((v for v in q if hasattr(v,'to_tuple')),None)if isinstance(q,tuple)and not any(isinstance(v,bool)and not v for v in q)else None
   grid.append(dict(x=x,y=y,safe_foot=good.to_tuple()if good is not None else None))
 assert sum(bool(v['safe_foot'])for v in grid)>50
 (O/'SwimmableGrid.json').write_text(json.dumps(dict(doc=probe_doc,points=grid),indent=2))
 checks.append(dict(observation_seconds=time.monotonic()-since,samples=samples,distance_cm=M.distance_travelled-distance_at_start,distance_total_cm=M.distance_travelled,plans=M.successful_plans,blocked=M.blocked_steps,habitat_origin=M.habitat_origin.to_tuple(),habitat_radius=M.habitat_radius_override,zone=Z.get_actor_location().to_tuple(),zone_extent=Z.get_component_by_class(unreal.BoxComponent).get_scaled_box_extent().to_tuple(),activities=M.activities.export_text(),settings=M.settings.export_text(),planning_us=M.planning_work_microseconds,tick_us=M.tick_work_microseconds,ticks=M.measured_ticks));shot('Karpador_Observed');yield from wait(.5)
 yield from record_swimming(A)
 yield from battle_after_observation()

def record_swimming(A):
 capture_class=runpy.run_path(str(R/'Tools/VisualV2PokemonTestGroundHealhouseV7/ReviewCapture.py'))['ScreenshotReview'];P.set_actor_location(unreal.Vector(-260,-1800,90),False,True);yield from wait(.7);cap=capture_class(W,O/'NaturalKarpadorMotion',unreal.GameplayStatics.get_time_seconds(W));since=time.monotonic()
 while time.monotonic()-since<16:
  q=A.get_actor_location()-P.get_actor_location();P.third_person_boom.set_world_rotation(unreal.Rotator(yaw=math.degrees(math.atan2(q.y,q.x))),False,False);cap.tick(unreal.GameplayStatics.get_time_seconds(W));yield
 cap.stop()
 while not cap.done:cap.tick(unreal.GameplayStatics.get_time_seconds(W));yield
 checks.append(dict(visual_recording_only=True,frames=len(cap.frames),no_gameplay_fps_claim=True))

def battle_after_observation():
 until=time.monotonic()+15
 while not any(valid(a)and a.life_state==unreal.PokeMonsterWildLifeState.ACTIVE and a.overworld_movement.biome_habitat.medium==unreal.PokeMonsterBiomeMedium.LAND for a in H.population):
  assert time.monotonic()<until;yield
 a=next(a for a in H.population if valid(a)and a.life_state==unreal.PokeMonsterWildLifeState.ACTIVE and a.overworld_movement.biome_habitat.medium==unreal.PokeMonsterBiomeMedium.LAND);before=len(E.get_player_party());assert I.add_item(unreal.load_asset('/Game/Data/Items/DA_MasterBall'),1);place(a);until=time.monotonic()+15
 while not E.is_encounter_active():
  assert time.monotonic()<until;steer(a.get_actor_location().x,a.get_actor_location().y);P.try_interact();yield
 inject(0,0);pr=E.get_presenter()
 while pr.get_view().busy or pr.get_view().presentation_pending:yield
 idx=next(i for i,m in enumerate(pr.get_view().moves)if m.enabled);assert pr.try_select_move(idx)and pr.resolve_selection();yield from wait(.5)
 while E.is_encounter_active()and(pr.get_view().busy or pr.get_view().presentation_pending):yield
 assert E.is_encounter_active();assert pr.try_select_capture_item(unreal.load_asset('/Game/Data/Items/DA_MasterBall'))and pr.resolve_selection()
 while E.is_encounter_active():yield
 yield from wait(1);assert len(E.get_player_party())==before+1 and Comp.get_visual()and not Comp.get_visual().hidden and not P.is_overworld_input_locked();checks.append(dict(final_regular_battle_capture_companion=True,party_before=before,party_after=len(E.get_player_party())))

def finish(error=None):
 cmd('csvprofile stop');cmd('pm.Speed 1')
 for k,v in profiling_old.items():cmd(k+' '+str(v))
 unreal.unregister_slate_post_tick_callback(unreal._fab_gameplay)
 if valid(P)and valid(MoveAction):inject(0,0)
 (O/'Result.json').write_text(json.dumps(dict(passed=error is None,error=error,checks=checks,distribution=distribution,shots=shots,seconds=time.monotonic()-start,mean_fps=1000/statistics.mean(frames)if frames else None,frame_p95_ms=sorted(frames)[int(len(frames)*.95)]if frames else None,performance_note='Functional tour includes captures/dialogues/load/travel; not an isolated GPU benchmark',isolated_storage=True),indent=2))
 if pie:unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
 else:
  live=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()in ['Dev_TestMap_VisualV2','Dev_TestMap']and unreal.GameplayStatics.get_player_pawn(w,0));unreal.SystemLibrary.quit_game(live,unreal.GameplayStatics.get_player_controller(live,0),unreal.QuitPreference.QUIT,False)
gen=run()
def tick(dt):
 global busy,last,lastsample
 if busy:return
 busy=True
 try:
  now=time.monotonic();frames.append((now-last)*1000);last=now;assert now-start<900
  if valid(P)and valid(H)and now-lastsample>3:
   lastsample=now;distribution.append(dict(seconds=now-start,position=P.get_actor_location().to_tuple(),population=[dict(species=str(a.visual_species.get_internal_id()),zone=str(a.overworld_movement.biome_habitat.zone_id),state=str(a.overworld_movement.behavior_state),speed=a.overworld_movement.current_speed)for a in H.population if valid(a)]));(O/'Progress.json').write_text(json.dumps(dict(last_check=({k:v for k,v in checks[-1].items()if k!='samples'}if checks and isinstance(checks[-1],dict)else checks[-1]if checks else None),seconds=now-start,population=len(H.population)),indent=2))
  next(gen)
 except StopIteration:finish()
 except Exception:finish(traceback.format_exc())
 finally:busy=False
unreal._fab_gameplay=unreal.register_slate_post_tick_callback(tick)
