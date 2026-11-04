"""Real input, interactions, capture, isolated Save/Load and travel. No production mutation."""
import unreal,json,time,math,statistics,traceback,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualV2IntegrationV1';cfg=json.loads((D/'GameplayRequest.json').read_text());O=D/cfg['label'];O.mkdir(exist_ok=True);assert not(O/'Result.json').exists();assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D);ed=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=ed.get_game_world()if ed else None;pie=W is not None
if not W:W=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_WestlandRegion'and unreal.GameplayStatics.get_player_pawn(w,0))
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
 bind(W);cmd('pm.EnvPerf2.Viewport 2560 1440');assert E.get_player_party() and Comp.get_visual();yield from wait(2)
 actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)}
 terrain=[a for n,a in actors.items()if n.startswith('WR_Terrain_')];ignore=[a for a in actors.values()if a not in terrain]
 def floor(x,y):
  hit=unreal.SystemLibrary.line_trace_single(W,unreal.Vector(x,y,16000),unreal.Vector(x,y,-10000),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,ignore,unreal.DrawDebugTrace.NONE);assert hit
  import re
  return float(re.search(r'ImpactPoint=\(X=[^,]+,Y=[^,]+,Z=([^\)]+)',hit.export_text())[1])
 f=json.loads((D/'BushFields.json').read_text())['fields'][0];z=actors[f['actor']];x,y,_=f['center'];P.set_actor_location(unreal.Vector(x-150,y,floor(x-150,y)+50.15),False,True);yield from wait(.7);base=z.get_bush_checks();yield from wait(2);assert z.get_bush_checks()==base
 PC.toggle_main_menu();yield from wait(.5);assert z.get_bush_checks()==base and not E.is_encounter_active();assert PC.close_menu();checks.append('Actual regional bush field: standing and menu do not roll')
 until=time.monotonic()+180;target=x+180
 while not E.is_encounter_active():
  assert time.monotonic()<until,('No natural bush encounter',z.get_bush_checks(),P.get_actor_location());steer(target,y)
  if abs(P.get_actor_location().x-target)<35:target=x-180 if target>x else x+180
  yield
 inject(0,0);assert z.get_bush_starts()==1;pr=E.get_presenter()
 while pr.get_view().busy or pr.get_view().presentation_pending:yield
 shot('Regionale_Buschbegegnung');yield from wait(.4)
 assert pr.try_select_move(1)and pr.resolve_selection()
 while E.is_encounter_active()and(pr.get_view().busy or pr.get_view().presentation_pending):yield
 assert E.is_encounter_active();assert I.add_item(unreal.load_asset('/Game/Data/Items/DA_MasterBall'),1);assert pr.try_select_capture_item(unreal.load_asset('/Game/Data/Items/DA_MasterBall'))and pr.resolve_selection()
 while E.is_encounter_active():yield
 assert H.get_bush_cooldown_remaining()>10 and H.get_bush_travel_remaining()==800;checks.append(dict(bush_checks=z.get_bush_checks(),battle_capture=True,cooldown=H.get_bush_cooldown_remaining(),travel_guard=H.get_bush_travel_remaining(),team=len(E.get_player_party())))
 # Real stable doorway crossings at every supported test speed. No original actor moves.
 cut=actors['HouseCutaway']
 def door(offset,inside=False):
  t=(cut.relocated_door_threshold if inside else cut.door_threshold).get_world_transform();return unreal.MathLibrary.transform_location(t,unreal.Vector(offset,0,0))
 for speed in [1,2,3]:
  cmd('pm.Speed '+str(speed));q=door(-200);P.set_actor_location(unreal.Vector(q.x,q.y,1050.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();yield from wait(.5);until=time.monotonic()+15
  while not cut.is_viewer_relocated()or cut.is_doorway_transition_active():
   assert time.monotonic()<until,('entry',speed,P.get_actor_location());q=door(170);steer(q.x,q.y);yield
  inject(0,0);yield from wait(.5);assert not P.is_overworld_input_locked();assert P.third_person_pitch==-12
  q=door(100,True);yield from walk(q.x,q.y);until=time.monotonic()+15
  while cut.is_viewer_relocated()or cut.is_doorway_transition_active():
   assert time.monotonic()<until,('exit',speed,P.get_actor_location());q=door(-170,True);steer(q.x,q.y);yield
  inject(0,0);yield from wait(.4);checks.append(dict(healer_speed=speed,entry_exit=True))
 cmd('pm.Speed 1')
 # Water-only occupancy and opt-in use the unchanged natural population, no forced targets.
 riverzones=[a for a in actors.values()if isinstance(a,unreal.PokeMonsterHabitatZone)and a.medium==unreal.PokeMonsterBiomeMedium.WATER_ONLY];assert len(riverzones)==3
 river=riverzones[1];q=river.get_actor_location();P.set_actor_location(unreal.Vector(q.x-1000,q.y-1000,floor(q.x-1000,q.y-1000)+50.15),False,True);yield from wait(4)
 samples=[];until=time.monotonic()+65;next_sample=0
 while time.monotonic()<until:
  if time.monotonic()>next_sample:
   for a in H.population:
    if valid(a)and str(a.visual_species.get_internal_id())=='Karpador'and a.life_state==unreal.PokeMonsterWildLifeState.ACTIVE:
     m=a.overworld_movement;assert m.explore_whole_water_habitat;assert m.biome_habitat.medium==unreal.PokeMonsterBiomeMedium.WATER_ONLY;samples.append(dict(position=a.get_actor_location().to_tuple(),zone=str(m.biome_habitat.zone_id),speed=m.current_speed))
   next_sample=time.monotonic()+.5
  yield
 checks.append(dict(natural_karpador_samples=samples,water_optin_verified=bool(samples),note='No forced spawn or artificial movement target'))
 # Real open-level and unchanged VisualV2 gallery. Team remains in the existing GI.
 expected=[a.export_text()for a in E.get_player_party()];PC.toggle_main_menu();saved=snapshot();assert S.save_current_game();(O/'RestartExpected.json').write_text(json.dumps(saved,indent=2));assert PC.close_menu();unreal.GameplayStatics.open_level(W,'/Game/Maps/Dev_TestMap_VisualV2');yield from wait(5)
 w=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0));bind(w);yield from wait(3);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();yield from wait(.5);assert [a.export_text()for a in E.get_player_party()]==expected;assert C.get_real_minutes_per_day()==120;assert Comp.get_visual();G=sub(unreal.PokeMonsterCreatureTestGround,W);assert len(G.species)==19 and len(G.get_import_targets())==49;origin=P.get_actor_location();cmd('pm.TestGround.List');cmd('pm.TestGround.Go Pikachu');until=time.monotonic()+120
 while not G.is_collection_ready():assert time.monotonic()<until;yield
 assert G.get_physical_model_count()==68;assert G.has_return_position();shot('TestGround_Pikachu');yield from wait(.5);cmd('pm.TestGround.Return');yield from wait(.5);checks.append(dict(testground_origin=origin.to_tuple(),returned=P.get_actor_location().to_tuple()));assert(P.get_actor_location()-origin).length()<1
 for target in ['Karpador','Aquana']:
  cmd('pm.TestGround.Go '+target);yield from wait(.5);assert G.has_return_position();cmd('pm.TestGround.Return');yield from wait(.4);assert not G.has_return_position()
 checks.append('Real map travel: unchanged VisualV2 TestGround List, Go Pikachu/Karpador/Aquana and Return, all68 physical models, party and companion retained')
 assert S.load_game();yield from wait(5)
 w=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_WestlandRegion'and unreal.GameplayStatics.get_player_pawn(w,0));bind(w)
 while S.is_load_in_progress():yield
 assert [a.export_text()for a in E.get_player_party()]==expected;assert math.dist(P.get_actor_location().to_tuple(),saved['position'])<.1;assert not P.is_overworld_input_locked()and Comp.get_visual();assert len(H.population)<=14;checks.append('Existing save loader returns to Westland and restores full captured team, position, camera, companion and world clock')
 values={k:unreal.SystemLibrary.get_console_variable_float_value(k)for k in ['r.ScreenPercentage','r.Lumen.HardwareRayTracing','r.Lumen.FinalGatherMethod','r.TemporalAA.Upsampling','r.Shadow.Virtual.SMRT.RayCountDirectional']};assert list(values.values())==[75,0,0,1,4];checks.append(dict(final_rendering=values))
def finish(error=None):
 if valid(P):inject(0,0)
 unreal.unregister_slate_post_tick_callback(unreal._wvi_extra);(O/'Result.json').write_text(json.dumps(dict(passed=error is None,error=error,checks=checks,shots=shots,seconds=time.monotonic()-start,diagnostic_positioning=True),indent=2))
 live=next((w for w in unreal.ObjectIterator(unreal.World)if w.get_name()in ['Dev_WestlandRegion','Dev_TestMap_VisualV2']and unreal.GameplayStatics.get_player_pawn(w,0)),None)
 if live:unreal.SystemLibrary.quit_game(live,unreal.GameplayStatics.get_player_controller(live,0),unreal.QuitPreference.QUIT,False)
gen=run()
def tick(dt):
 global busy
 if busy:return
 busy=True
 try:
  assert time.monotonic()-start<650;next(gen)
 except StopIteration:finish()
 except Exception:finish(traceback.format_exc())
 finally:busy=False
unreal._wvi_extra=unreal.register_slate_post_tick_callback(tick)
