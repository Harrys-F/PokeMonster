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
def snapshot():return dict(party=[x.export_text()for x in E.get_player_party()],inventory=[x.export_text()for x in I.get_stacks()],position=P.get_actor_location().to_tuple(),clock=C.get_time().export_text(),facing=P.get_interaction_world_direction().to_tuple())
def run():
 bind(W);assert not P.is_overworld_input_locked()
 if pie:assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_GEV5_'+cfg['label'])
 cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('pm.BushEncounters.Debug 1');assert E.get_player_party();yield from wait(2)
 actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)};geo=runpy.run_path(str(R/'Tools/VisualV2WorldRefinementV4/Design.py'));floorz=geo['height'];auth=json.loads((D/'Author.json').read_text())
 # Only actual visible decorative sprites matter; the authored gallery is suspended by habitats.
 visible=[]
 for a in actors.values():
  for c in a.get_components_by_class(unreal.PaperSpriteComponent):
   if c.is_visible()and not c.hidden_in_game and not a.hidden:visible.append(a.get_actor_label())
 assert not visible,('Remaining active placeholder sprites',visible);checks.append(dict(runtime_visible_sprites=visible,population=len(H.population)))
 for name in ['Slice_Waldhueterin_Liora','Slice_Archivarin_Abzweig']:
  a=actors[name];v=actors['GEV5_'+name+'_3D'];assert v.source_actor==a and v.visual.get_skeletal_mesh_asset()and v.idle_animation and not a.get_component_by_class(unreal.PaperSpriteComponent).is_visible();p=a.get_actor_location();P.set_actor_location(unreal.Vector(p.x-170,p.y-230,floorz(p.x,p.y)+50.15),False,True);P.third_person_boom.set_world_rotation(unreal.Rotator(yaw=55),False,False);yield from wait(2);shot(name);checks.append(dict(npc=name,mesh=v.visual.get_skeletal_mesh_asset().get_path_name(),location=v.get_actor_location().to_tuple(),capsule_half=a.get_component_by_class(unreal.CapsuleComponent).get_scaled_capsule_half_height()))
 npc=actors['Slice_Archivarin_Abzweig'];place(npc,(-130,0));until=time.monotonic()+.55
 while time.monotonic()<until:steer(npc.get_actor_location().x,npc.get_actor_location().y);yield
 inject(0,0);yield from wait(.2);hit=unreal.SystemLibrary.line_trace_single(W,P.get_actor_location(),npc.get_actor_location(),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[P,npc],unreal.DrawDebugTrace.NONE);checks.append(dict(interaction_trace=hit.export_text()if hit else None,position=P.get_actor_location().to_tuple(),npc_position=npc.get_actor_location().to_tuple(),dialogue=str(npc.dialogue),facing=P.get_interaction_world_direction().to_tuple(),target=str(P.find_interactable_in_range()),locked=P.is_overworld_input_locked(),encounter=E.is_encounter_active(),dialogue_active=Dlg.is_dialogue_active(),service=str(npc.get_editor_property('service'))));assert P.try_interact()and Dlg.is_dialogue_active(),('NPC interaction',P.get_actor_location(),P.get_actor_rotation());assert Dlg.get_active_source()==npc;yield from wait(1);shot('Archivarin_Dialog');PC.close_dialogue();assert not P.is_overworld_input_locked();checks.append('Existing archivist dialogue, source and player control preserved')
 # Actual physical collision against one large shrub, then a route around the cluster.
 b=auth['barriers'][7];x,y=b['center'];P.set_actor_location(unreal.Vector(x+190,y,floorz(x+190,y)+50.15),False,True);yield from wait(.4);until=time.monotonic()+1.5
 while time.monotonic()<until:steer(x,y);yield
 inject(0,0);assert math.dist(P.get_actor_location().to_tuple()[:2],(x,y))>75;shot('Grosser_Kollisionsbusch');checks.append(dict(large_bush_blocked=True,actual_distance=math.dist(P.get_actor_location().to_tuple()[:2],(x,y))))
 # Stay in an actual field, exercise standing/menu/dialogue suppression and existing habitat selection.
 f=auth['fields'][0];z=actors[f['actor']];x,y=f['center'];rx,ry=f['extent'];P.set_actor_location(unreal.Vector(x-150,y,floorz(x-150,y)+50.15),False,True);yield from wait(.7);base=z.get_bush_checks();yield from wait(2);assert z.get_bush_checks()==base;shot('Begehbares_Buschfeld')
 PC.toggle_main_menu();assert PC.is_menu_open();yield from wait(.7);assert z.get_bush_checks()==base and not E.is_encounter_active();assert PC.close_menu();yield from wait(.3);base=z.get_bush_checks()
 assert Dlg.start_dialogue(P,npc,npc.dialogue,E);yield from wait(.7);assert z.get_bush_checks()==base and not E.is_encounter_active(),('Dialogue guard',base,z.get_bush_checks(),E.is_encounter_active());PC.close_dialogue();yield from wait(.4);checks.append('Standing, pause menu and active dialogue do not roll; companion/NPC are not local-player initiators')
 until=time.monotonic()+150;target=x+180;begun=False
 while not E.is_encounter_active():
  assert time.monotonic()<until,('No random bush battle',z.get_bush_checks(),z.get_bush_starts(),P.get_actor_location(),H.get_bush_cooldown_remaining(),H.get_bush_travel_remaining());steer(target,y)
  if abs(P.get_actor_location().x-target)<35:target=x-180 if target>x else x+180
  yield
 inject(0,0);assert z.get_bush_starts()==1 and z.get_bush_checks()>base;pr=E.get_presenter()
 while pr.get_view().busy or pr.get_view().presentation_pending:yield
 yield from wait(2);assert E.is_encounter_active();shot('Tatsaechliche_Zufallsbegegnung');yield from wait(.4);checks.append(dict(real_random_bush_battle=True,checks=z.get_bush_checks(),starts=z.get_bush_starts(),party=[q.export_text()for q in E.get_player_party()],population=len(H.population)))
 assert pr.try_select_move(1)and pr.resolve_selection();yield from wait(.4)
 while E.is_encounter_active()and(pr.get_view().busy or pr.get_view().presentation_pending):yield
 assert E.is_encounter_active();checks.append('A normal battle turn consumes PP before the later healer restoration check');assert I.add_item(unreal.load_asset('/Game/Data/Items/DA_MasterBall'),1);assert pr.try_select_capture_item(unreal.load_asset('/Game/Data/Items/DA_MasterBall'));assert pr.resolve_selection()
 while E.is_encounter_active():yield
 assert H.get_bush_cooldown_remaining()>10 and H.get_bush_travel_remaining()==800;starts=z.get_bush_starts();checks_at=z.get_bush_checks();until=time.monotonic()+3
 while time.monotonic()<until:steer(x+160 if P.get_actor_location().x<x else x-160,y);yield
 inject(0,0);assert z.get_bush_starts()==starts and z.get_bush_checks()==checks_at;checks.append(dict(shared_cooldown_seconds=H.get_bush_cooldown_remaining(),remaining_travel_cm=H.get_bush_travel_remaining(),capture_party_size=len(E.get_player_party())))
 P.set_actor_location(unreal.Vector(-3700,500,50.15),False,True);yield from wait(.5)
 # Real input at each supported transient speed crosses both directions under the existing black mask.
 cut=actors['V2_House_HouseCutaway'];q=cut.door_threshold.get_world_location();inner=cut.relocated_door_threshold.get_world_location()
 for speed in [1,2,3]:
  cmd('pm.Speed '+str(speed));P.set_actor_location(unreal.Vector(q.x-200,q.y,50.15),False,True);yield from wait(.6);until=time.monotonic()+12
  while not cut.is_viewer_relocated():
   assert time.monotonic()<until,('House entry',speed,P.get_actor_location());steer(q.x+170,q.y);yield
  inject(0,0)
  while cut.is_doorway_transition_active():yield
  yield from wait(.4);assert P.get_component_by_class(unreal.CharacterMovementComponent).movement_mode==unreal.MovementMode.MOVE_WALKING
  if speed==1:
   yield from walk(16800,500);yield from wait(.3)
   walls=[a for n,a in actors.items()if n.startswith(('V2_House_HH_Expanded_RearWall','V2_House_HH_Expanded_SideWall','V2_House_HH_Expanded_FrontWall'))];assert len(walls)==18
   assert all(not a.hidden and all(c.is_visible()and not c.hidden_in_game for c in a.get_components_by_class(unreal.StaticMeshComponent))for a in walls)
   for yaw in [0,90,180,270]:
    P.third_person_boom.set_world_rotation(unreal.Rotator(yaw=yaw),False,False);yield from wait(1);cam=PC.player_camera_manager.get_camera_location();assert 16420<cam.x<17300 and -20<cam.y<1030;assert abs(PC.player_camera_manager.get_camera_rotation().pitch+12)<.03;shot('Heilhaus_VierWaende_'+str(yaw))
   checks.append(dict(four_wall_groups_visible=True,wall_actors=[a.get_actor_label()for a in walls]));healer=actors['V2_House_HouseHealer'];yield from walk(17000,690);yield from walk(17230,690);yield from walk(17230,560);until=time.monotonic()+.6
   while time.monotonic()<until:steer(17230,420);yield
   inject(0,0);pp_before=[(m.current_pp,m.max_pp)for q in E.get_player_party()for m in q.move_slots if m.max_pp>0];assert any(v<m for v,m in pp_before);assert P.find_interactable_in_range()==healer;assert P.try_interact()and Dlg.is_dialogue_active();assert Dlg.advance_dialogue();yield from wait(.5)
   if Dlg.is_dialogue_active():PC.close_dialogue()
   assert all(q.current_hp==q.calculated_stats.max_hp for q in E.get_player_party());assert all(m.current_pp==m.max_pp for q in E.get_player_party()for m in q.move_slots if m.max_pp>0);checks.append(dict(healer_pp_before=pp_before,all_hp_and_pp_restored=True));checks.append('Existing healer dialogue and full-party healing preserve the shared checkpoint/save mechanism');yield from walk(17230,690);yield from walk(17000,690);yield from walk(16800,500);PC.toggle_main_menu();expected=snapshot();assert S.save_current_game()and S.load_game();yield from wait(1)
   while S.is_load_in_progress():yield
   actual=snapshot();(O/'SaveRoundTrip.json').write_text(json.dumps(dict(expected=expected,actual=actual),indent=2));assert all(actual[k]==expected[k]for k in ['party','inventory','clock']);assert math.dist(actual['position'],expected['position'])<.001;assert math.dist(actual['facing'],expected['facing'])<1e-6;assert PC.close_menu();assert cut.is_viewer_relocated()and not cut.is_doorway_transition_active();checks.append('Interior menu Save/Load preserves exact team, PP, inventory, position, yaw and clock with four opaque walls')
  yield from walk(inner.x+100,inner.y);until=time.monotonic()+12
  while cut.is_viewer_relocated():
   assert time.monotonic()<until,('House exit',speed,P.get_actor_location());steer(inner.x-170,inner.y);yield
  inject(0,0)
  while cut.is_doorway_transition_active():yield
  yield from wait(.3);assert P.third_person_pitch==-12 and P.third_person_distance==350 and not P.is_using_interior_movement_basis();checks.append(dict(house_speed=speed,entry_exit=True,controllable=not P.is_overworld_input_locked(),actual=P.get_actor_location().to_tuple()))
 cmd('pm.Speed 1');cmd('pm.BushEncounters.Debug 0');yield from wait(.3)

def finish(error=None):
 cmd('csvprofile stop');cmd('pm.Speed 1');cmd('pm.BushEncounters.Debug 0')
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
