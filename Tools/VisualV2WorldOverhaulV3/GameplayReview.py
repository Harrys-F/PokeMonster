"""Real input, interactions, capture, isolated Save/Load and travel. No production mutation."""
import unreal,json,time,math,statistics,traceback,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2WorldOverhaulV3';cfg=json.loads((D/'GameplayRequest.json').read_text());O=D/cfg['label'];O.mkdir(exist_ok=True);assert not(O/'Result.json').exists();assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D);ed=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=ed.get_game_world()if ed else None;pie=W is not None
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
def snapshot():return dict(party=[x.export_text()for x in E.get_player_party()],inventory=[x.export_text()for x in I.get_stacks()],position=P.get_actor_location().to_tuple(),clock=C.get_time().export_text())
def run():
 runpy.run_path(str(R/'Tools/VisualV2WorldOverhaulV3/Metadata.py'),run_name='__main__');bind(W);assert 'Dev_TestMap_VisualV2'in W.get_name();assert not P.is_overworld_input_locked()
 if pie:assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_FabAssetTrial_'+cfg['label'])
 cmd('pm.EnvPerf2.Viewport 2560 1440');assert P.is_third_person_camera()and P.third_person_pitch==-12 and P.third_person_distance==350 and C.get_real_minutes_per_day()==120
 cv={k:unreal.SystemLibrary.get_console_variable_float_value(k)for k in ['r.ScreenPercentage','r.TemporalAA.Upsampling','r.Lumen.HardwareRayTracing','r.Lumen.FinalGatherMethod','r.Shadow.Virtual.Enable','r.Shadow.Virtual.SMRT.RayCountDirectional']};assert list(cv.values())==[75,1,0,0,1,4];checks.append({'graphics':cv,'physical_controller_test':False});yield from wait(5)
 # Profile only continuous movement, before any screenshots/dialogues/save operations.
 for k,v in [('r.GPUCsvStatsEnabled',1),('r.VSync',0),('t.MaxFPS',0)]:profiling_old[k]=unreal.SystemLibrary.get_console_variable_float_value(k);cmd(k+' '+str(v))
 cmd('csvprofile startfile=FAB_'+cfg['label']+'_Tour');cmd('csvprofile start')
 # Walk the existing paths, with real player physics and active world clock/AI.
 for x,y in [(-760, -1370), (-880, -1410), (-1000, -1430), (-880, -1410), (-760, -1370), (-760, -1410), (-1150, -1920), (-2100, -2060), (-3350, -1700), (-3310, -1290), (-3150, -1020), (-3310, -1290), (-3350, -1700), (-4150, -700), (-4100, 450), (-3700, 500), (-4100, 450), (-4300, 1550), (-3300, 2050), (-2150, 2000), (-1700, 1220), (-1550, 650), (-1580, -100), (-1560, -860), (-1520, -1830), (-1150, -1920), (-760, -1410), (-760, -1110), (-780, -850), (-700, -640), (-440, -540), (-350, -480), (-350, -150), (-20, -40), (240, 170), (470, 360), (730, 600), (760, 850), (730, 600), (470, 360), (240, 170), (-20, -40)]:
  yield from walk(x,y)
 cmd('csvprofile stop');inject(0,0);checks.append('Continuous real-input path tour: meadow, village, forest edge, forest, habitat margins and bridge; no in-route positioning teleports');assert len(H.population)<=14 and H.is_population_enabled();assert Comp.get_visual()and not Comp.get_visual().get_editor_property('hidden')
 # Normal sprint switch and camera yaw remain existing implementations.
 old=P.is_sprint_mode_enabled();sprint=next(a for a in unreal.ObjectIterator(unreal.InputAction)if a.get_outer()==P and a.get_name()=='SprintToggleAction');MoveSub.inject_input_vector_for_action(sprint,unreal.Vector(1,0,0),[],[]);yield from wait(.2);assert P.is_sprint_mode_enabled()!=old;MoveSub.inject_input_vector_for_action(sprint,unreal.Vector(1,0,0),[],[]);yield from wait(.2);assert P.is_sprint_mode_enabled()==old;checks.append('Existing Enhanced Input sprint action toggled on/off; no physical gamepad claim')
 actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)}
 # Test both bridge rails and the non-relocated cottage with real physics/input.
 P.set_actor_location(unreal.Vector(-350,-320,74.15),False,True);yield from wait(.4);until=time.monotonic()+1.5
 while time.monotonic()<until:steer(-100,-320);yield
 inject(0,0);assert P.get_actor_location().x<-280,('Bridge rail failed',P.get_actor_location());yield from walk(-350,-320);checks.append('Bridge deck/ramp traversal on the full tour and actual lateral rail collision')
 cottage=actors['V2_Cottage_Cutaway'];q=cottage.door_threshold.get_world_location();P.set_actor_location(unreal.Vector(q.x-150,q.y,50.15),False,True);yield from wait(.4);yield from walk(q.x+130,q.y);yield from wait(1);assert cottage.is_viewer_inside(P.get_actor_location())and cottage.is_cutaway_active();shot('CottageInterior');yield from walk(q.x-160,q.y);yield from wait(1);assert not cottage.is_viewer_inside(P.get_actor_location());checks.append('Actual cottage doorway entry, cutaway, interior floor and return without changing its existing in-place interior technique')
 # Both independent test areas preserve commands and exact return position.
 origin=P.get_actor_location();g=sub(unreal.PokeMonsterCreatureTestGround,W);assert g.visit(1);yield from wait(.4);assert P.get_actor_location().y<-10000;assert g.return_to_world();yield from wait(.2);assert math.dist(P.get_actor_location().to_tuple(),origin.to_tuple())<1
 checks.append('Relocated registered Pokemon test-ground visit and exact return preserve all models/modes; NPC RAM-preview command checked in a separate normal PIE session')
 marker=actors['Dev_InteractionMarker_Separat'];place(marker);yield;inject(0,0);yield from wait(.2);oldcount=marker.get_interaction_count();assert P.try_interact()and marker.get_interaction_count()==oldcount+1;assert marker.is_interaction_active();assert P.try_interact()and not marker.is_interaction_active();checks.append('Existing prototype-marker interaction/collider retained with attached existing 3D crate; normal interaction count/light toggle verified')
 npc=actors['Slice_Wanderer_Hinweis'];place(npc);yield;inject(0,0);yield from wait(.2);assert P.try_interact()and Dlg.is_dialogue_active();PC.close_dialogue();assert not P.is_overworld_input_locked();checks.append('Original wanderer dialogue and return to control')
 # Real habitat Pokémon and existing capture transaction; fixture item only in isolated test RAM.
 until=time.monotonic()+12
 while not any(a and a.life_state==unreal.PokeMonsterWildLifeState.ACTIVE and a.overworld_movement.biome_habitat.medium==unreal.PokeMonsterBiomeMedium.LAND for a in H.population):
  assert time.monotonic()<until,'Natural population did not resume after test-ground return';yield
 a=next(a for a in H.population if a and a.life_state==unreal.PokeMonsterWildLifeState.ACTIVE and a.overworld_movement.biome_habitat.medium==unreal.PokeMonsterBiomeMedium.LAND);before=[x.instance_id.to_string()for x in E.get_player_party()];assert I.add_item(unreal.load_asset('/Game/Data/Items/DA_MasterBall'),1);place(a);until=time.monotonic()+12
 while not E.is_encounter_active():
  assert time.monotonic()<until,('Natural encounter failed',a);steer(a.get_actor_location().x,a.get_actor_location().y);P.try_interact();yield
 inject(0,0);pr=E.get_presenter()
 while pr.get_view().busy or pr.get_view().presentation_pending:yield
 view=pr.get_view();idx=1 if len(view.moves)>1 and view.moves[1].enabled else next(i for i,m in enumerate(view.moves)if m.enabled);E.get_battle_widget().call_method('Move'+str(idx));yield from wait(.5)
 while E.is_encounter_active()and(pr.get_view().busy or pr.get_view().presentation_pending):yield
 assert E.is_encounter_active(),'Encounter ended before capture';assert pr.try_select_capture_item(unreal.load_asset('/Game/Data/Items/DA_MasterBall'));assert pr.resolve_selection()
 while E.is_encounter_active():yield
 team=list(E.get_player_party());assert len(team)==len(before)+1 and[x.instance_id.to_string()for x in team[:len(before)]]==before;checks.append('Natural encounter, normal ClassicBattle move/AP action, normal MasterBall transaction, team grows by one distinct instance and returns to overworld')
 # Actual doorway crossing at normal speed, retaining all cutaway logic.
 cut=actors['V2_House_HouseCutaway'];box=cut.door_threshold;p=box.get_world_location();yaw=box.get_world_rotation().yaw
 def door(off,inside=False):
  b=cut.relocated_door_threshold if inside else cut.door_threshold;return b.get_world_location()+unreal.MathLibrary.rotate_angle_axis(unreal.Vector(off,0,0),b.get_world_rotation().yaw,unreal.Vector(0,0,1))
 q=door(-125);P.set_actor_location(unreal.Vector(q.x,q.y,q.z-box.get_scaled_box_extent().z+50.15),False,True);yield from wait(.5);until=time.monotonic()+15
 while not cut.is_viewer_relocated():
  assert time.monotonic()<until,'Interior entry';q=door(130);steer(q.x,q.y);yield
 inject(0,0);yield from wait(1);assert P.is_using_interior_movement_basis();shot('Innenraum');PC.toggle_main_menu();assert PC.is_menu_open();expected=snapshot();assert S.save_current_game()and S.load_game();yield from wait(2)
 while S.is_load_in_progress():yield
 assert snapshot()==expected;assert PC.close_menu();assert cut.is_viewer_relocated();checks.append('Real relocated healing-house entry and isolated menu Save/Load preserve exact team, PP, inventory, position and world time')
 q=door(90,True);yield from walk(q.x,q.y);until=time.monotonic()+15
 while cut.is_viewer_relocated():
  assert time.monotonic()<until,'Interior exit';q=door(-130,True);steer(q.x,q.y);yield
 inject(0,0);yield from wait(1);assert not P.is_using_interior_movement_basis();checks.append('Actual doorway exit restores exterior camera/control')
 for hour in [6,12,19,22]:

  if pie:cmd('pm.WorldClock set 1 '+str(hour)+' 0');cmd('pm.WorldClock pause')
  else:
   runpy.run_path(str(R/'Tools/VisualV2WorldOverhaulV3/ClockFixture.py'))['set_hour'](W,PC,S,hour)
  yield from wait(2);assert C.get_hour()==hour;sample=sub(unreal.PokeMonsterDayNightSubsystem,W).get_lighting_sample();shot('Tageszeit_'+str(hour));checks.append(dict(hour=hour,elevation=sample.sun_elevation,population=len(H.population)))

 if not pie and PC.is_menu_open():assert PC.close_menu()

 if pie:cmd('pm.WorldClock reset')
 assert E.reorder_party(E.get_player_party()[1].instance_id,0);yield from wait(1);assert Comp.get_visual();assert PC.open_menu(unreal.PokeMonsterOverworldMenuSection.TEAM);shot('Team');assert PC.close_menu();checks.append('Team sorting, current companion and existing team UI')
 if cfg.get('travel'):
  PC.toggle_main_menu();expected=snapshot();assert S.save_current_game();assert PC.close_menu();unreal.GameplayStatics.open_level(W,'/Game/Maps/Dev_TestMap');yield from wait(4)
  other=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap'and unreal.GameplayStatics.get_player_pawn(w,0));bind(other);assert C.get_real_minutes_per_day()==120;assert S.load_game();yield from wait(4)
  back=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0));bind(back)
  while S.is_load_in_progress():yield
  assert [x.export_text()for x in E.get_player_party()]==expected['party'];assert math.dist(P.get_actor_location().to_tuple(),expected['position'])<.1;assert Comp.get_visual()and P.is_third_person_camera();checks.append('Real map travel and normal save loader return to saved VisualV2/team/position/companion')
 yield from wait(1);assert all(Path(p).exists()for p in shots)

def finish(error=None):
 cmd('csvprofile stop')
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
