"""Real input, interactions, capture, isolated Save/Load and travel. No production mutation."""
import unreal,json,time,math,statistics,traceback,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5';cfg=json.loads((D/'GameplayRequest.json').read_text());O=D/cfg['label'];O.mkdir(exist_ok=True);assert not(O/'Result.json').exists();assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D);ed=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=ed.get_game_world()if ed else None;pie=W is not None
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
 p=O/(name+'.png');cmd('Shot showui filename="'+str(p)+'" -nosuffix');shots.append(str(p))
def snapshot():return dict(party=[x.export_text()for x in E.get_player_party()],inventory=[x.export_text()for x in I.get_stacks()],position=P.get_actor_location().to_tuple(),clock=C.get_time().export_text())
def run():
 bind(W)
 if pie:assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_TrainerGEV5_'+cfg['label'])
 cmd('pm.EnvPerf2.Viewport 2560 1440');assert E.get_player_party();actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)};npc=actors['Slice_Waldhueterin_Liora'];place(npc,(-130,0));until=time.monotonic()+.6
 while time.monotonic()<until:steer(npc.get_actor_location().x,npc.get_actor_location().y);yield
 inject(0,0);yield from wait(.2);assert P.find_interactable_in_range()==npc;assert P.try_interact();assert P.is_overworld_input_locked();until=time.monotonic()+10
 while not E.is_encounter_active():assert time.monotonic()<until;yield
 yield from wait(2);shot('Liora_Unveraenderter_Trainerkampf');pr=E.get_presenter();until=time.monotonic()+180;actions=[]
 while E.is_encounter_active():
  assert time.monotonic()<until,('Trainer battle timeout',pr.get_view().export_text());v=pr.get_view()
  if v.busy or v.presentation_pending:yield;continue
  if v.learning_move:assert pr.resolve_move_learning(-1);yield;continue
  if v.must_switch:
   idx=next(i for i,m in enumerate(v.player_team)if m.can_switch);assert pr.try_select_switch(idx);assert pr.resolve_selection();actions.append(dict(switch=idx))
  elif not v.finished:
   idx=1 if len(v.moves)>1 and v.moves[1].enabled else next(i for i,m in enumerate(v.moves)if m.enabled);assert pr.try_select_move(idx);assert pr.resolve_selection();actions.append(dict(move=idx))
  yield
 result=E.get_last_result();assert result.outcome==unreal.PokeMonsterEncounterOutcome.VICTORY;assert not P.is_overworld_input_locked();checks.append(dict(trainer=npc.get_actor_label(),source_profile=npc.get_editor_property('profile').get_path_name(),result=result.export_text(),normal_actions=actions));yield from wait(.5)

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
   lastsample=now;distribution.append(dict(seconds=now-start,position=P.get_actor_location().to_tuple(),population=[dict(species=str(a.visual_species.get_internal_id()),zone=str(a.overworld_movement.biome_habitat.zone_id),state=str(a.overworld_movement.behavior_state),speed=a.overworld_movement.current_speed)for a in H.population if valid(a)]));(O/'Progress.json').write_text(json.dumps(dict(last_check=checks[-1]if checks else None,seconds=now-start,population=len(H.population)),indent=2))
  next(gen)
 except StopIteration:finish()
 except Exception:finish(traceback.format_exc())
 finally:busy=False
unreal._fab_gameplay=unreal.register_slate_post_tick_callback(tick)
