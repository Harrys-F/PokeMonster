"""Actual existing UMG/service acceptance in an explicitly isolated EvolutionV3 UserDir.
The item fixture is technical only; no new production stone evolution is authored.
"""
import unreal,time,json,traceback,os
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/EvolutionV3';q=json.loads((D/'Active.json').read_text());O=D/q['label'];s={'stage':'init','start':time.monotonic(),'i':0,'at':time.monotonic()};r={'checks':[],'cases':[],'technical_item_fixture':False,'physical_controller_test':False};route=[];state={};W=PC=E=S=I=None

def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def party():return list(E.get_player_party())
def snapshot():return [x.export_text()for x in party()]
def ui():return PC.get_evolution_widget()
def phase(p):return bool(ui())and ui().get_phase()==p
def shot(name):cmd('Shot filename="'+str(O/(name+'.png'))+'" -nosuffix')
def add(name,fn,delay=.4):route.append((name,fn,delay))
def check(name,fn,delay=.4):
 def run():assert fn(),name;r['checks'].append(name)
 add(name,run,delay)
def fixture(name,level):cmd('pm.EvolutionReview.Party '+name+' '+str(level))
def equivalent(before,after):
 assert before.instance_id.to_string()==after.instance_id.to_string(),(before.instance_id.to_string(),after.instance_id.to_string())
 for k in ['Level','Experience','Status','StatusTurns']:
  assert str(before.get_editor_property(k))==str(after.get_editor_property(k)),k
 for k in ['MoveSlots','LearnedMoves']:assert [x.export_text()for x in before.get_editor_property(k)]==[x.export_text()for x in after.get_editor_property(k)],k
 assert before.calculated_stats.max_hp-before.current_hp==after.calculated_stats.max_hp-after.current_hp
 return True
def roundtrip():
 assert not ui()and not PC.is_menu_open();state['saved']=snapshot();assert S.save_current_game(),S.get_last_storage_message();assert S.load_game(),S.get_last_storage_message()
def companion_ok():
 c=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==W)
 v=c.get_visual();return v is not None and v.mesh.get_skeletal_mesh_asset()==party()[0].species.get_visuals().presentation.mesh

def build():
 add('read fresh graphics defaults',lambda:r.update(graphics={n:unreal.SystemLibrary.get_console_variable_float_value(n)for n in ['r.Lumen.HardwareRayTracing','r.Lumen.FinalGatherMethod','r.ScreenPercentage','r.TemporalAA.Upsampling','r.Shadow.Virtual.SMRT.RayCountDirectional']}))
 check('Fresh profile C remains Software-Lumen/IFG TAAU 75% VSM4',lambda:list(r['graphics'].values())==[0.,0.,75.,1.,4.])
 add('pause auto for explicit fixtures',lambda:cmd('pm.Evolution.Auto 0'))
 # Each real level route uses the normal offer and unchanged presentation.
 for source,level,target in [('Karpador',19,'Garados')]:
  def prep(source=source,level=level):fixture(source,level);state['source']=source;state['target']=target
  add('prepare '+source,prep)
  add('normal polling '+source,lambda:cmd('pm.Evolution.Auto 1'),1)
  check(source+' does not evolve early',lambda:not ui())
  add('gain exact threshold '+source,lambda:cmd('pm.EvolutionReview.XP next'),1.4)
  check(source+' offers correct target',lambda target=target:phase('offer')and str(party()[0].pending_evolution_target.primary_asset_name)==target)
  add('snapshot '+source,lambda:state.update(before=party(),before_text=snapshot()))
  add('begin reversible sequence '+source,lambda:ui().confirm())
  check(source+' preview preserves individual until commit',lambda:phase('transform')and snapshot()==state['before_text'],3.2)
  add('cancel running sequence '+source,lambda:ui().cancel(),.6)
  check(source+' A cancellation keeps species AP HP and reserve',lambda:phase('cancelled')and equivalent(state['before'][0],party()[0])and party()[0].species==state['before'][0].species and party()[1].export_text()==state['before'][1].export_text())
  add('cancel screenshot '+source,lambda source=source:shot(source+'_Cancelled'),1.2)
  add('acknowledge cancellation '+source,lambda:ui().confirm(),1)
  check(source+' no immediate duplicate offer',lambda:not ui())
  add('save cancelled state '+source,roundtrip,1.4)
  check(source+' cancelled save reload remains same species',lambda:not S.is_load_in_progress()and snapshot()==state['saved'],1.5)
  add('later actual level permits retry '+source,lambda:cmd('pm.EvolutionReview.XP next'),1.5)
  check(source+' later retry',lambda:phase('offer'))
  add('snapshot retry '+source,lambda:state.update(retry=party()))
  add('confirm existing sequence '+source,lambda:ui().confirm())
  check(source+' full reveal and successful evolution',lambda target=target:phase('complete')and str(party()[0].species.get_internal_id())==target and equivalent(state['retry'][0],party()[0])and party()[1].export_text()==state['retry'][1].export_text(),8.8)
  add('full color success '+source,lambda source=source:shot(source+'_Complete'),1.5)
  add('acknowledge complete '+source,lambda:ui().confirm(),.6)
  def learning():
   if phase('learning'):r['cases'].append({'evolution_learning':[x.get_path_name()for x in party()[0].pending_moves]});ui().cancel()
  add('normal target-level learning '+source,learning,1)
  check(source+' existing companion updates model',lambda:not ui()and companion_ok())
  add('save evolved state '+source,roundtrip,1.5)
  check(source+' evolved save restores every individual field',lambda:not S.is_load_in_progress()and snapshot()==state['saved'],1.5)
  add('hold auto between fixtures',lambda:cmd('pm.Evolution.Auto 0'))

 add('Garados gallery visit',lambda:cmd('pm.TestGround.Go Garados'),1)
 for mode in ['idle','walk','run','turn','directions','auto']:
  add('Existing gallery '+mode,lambda mode=mode:cmd('pm.TestGround.Mode '+mode),1)
 add('Return to normal world',lambda:cmd('pm.TestGround.Return'),1.5)
 check('Land buddy preserves original coil rig after water gallery',lambda:companion_ok(),2)

 def player():return unreal.GameplayStatics.get_player_pawn(W,0)
 def place(pos):player().set_actor_location(unreal.Vector(*pos),False,True);player().get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
 def approach():
  H=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterHabitatSubsystem)if x.get_outer()==W);available=[a for a in H.population if a.life_state==unreal.PokeMonsterWildLifeState.ACTIVE and a.overworld_movement.biome_habitat.medium!=unreal.PokeMonsterBiomeMedium.WATER_ONLY and str(a.encounter_id)not in state.get('used',[])]
  assert available,'No distinct active land encounter';a=next((a for a in available if a.get_challenge_name()=='Enton'),available[0]);state['wild']=a;state.setdefault('used',[]).append(str(a.encounter_id));t=a.get_actor_location();place((t.x-95,t.y,t.z-9.85));aim=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if 'LocalPlayer'in x.get_outer().get_class().get_name());move=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==player()and x.get_name()=='MoveAction');import math;yaw=math.radians(player().get_movement_basis_yaw());aim.inject_input_vector_for_action(move,unreal.Vector(-math.sin(yaw),math.cos(yaw),0),[],[]);assert I.add_item(unreal.load_asset('/Game/Data/Items/DA_MasterBall'),2)
 add('Approach actual natural encounter',approach,1)
 add('Player uses existing interaction',lambda:player().try_interact(),1)
 check('Actual ClassicBattle with evolved Garados',lambda:E.is_encounter_active()and C.is_clock_paused(),3)
 def stage_check():
  scene=unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterClassicBattleScene)[0];v=scene.player_visual;assert v.mesh.get_skeletal_mesh_asset()==party()[0].species.get_visuals().presentation.mesh and not v.using_swim_mesh;state['stage']=v;r['checks'].append('ClassicBattle keeps original Garados mesh and skeleton')
 add('Inspect exact battle mesh',stage_check)
 def attack():
  view=E.get_presenter().get_view();assert not view.busy and not view.presentation_pending;slots=party()[0].get_editor_property('move_slots');idx=next(i for i,m in enumerate(view.moves)if m.enabled and m.current_pp>0 and slots[i].get_editor_property('move').base_power>0);state.update(attack_slot=idx,attack_pp=view.moves[idx].current_pp);assert E.get_presenter().try_select_move(idx);assert E.get_presenter().resolve_selection()
 add('Garados uses inherited damaging attack',attack,1)
 def round_check():
  if E.is_encounter_active():assert E.get_presenter().get_view().moves[state['attack_slot']].current_pp==state['attack_pp']-1
  else:assert party()[0].get_editor_property('move_slots')[state['attack_slot']].get_editor_property('current_pp')==state['attack_pp']-1
  r['checks'].append('Actual battle resolver consumes exactly one inherited AP')
 add('Verify completed battle round',round_check,4)
 def capture_or_start():
  if not E.is_encounter_active():approach();player().try_interact();state['new_capture_encounter']=True
 add('Keep a live encounter for normal capture',capture_or_start,1)
 def capture():
  assert E.is_encounter_active();state['party_before_capture']=len(party());presenter=E.get_presenter();assert presenter.try_select_capture_item(unreal.load_asset('/Game/Data/Items/DA_MasterBall'));assert presenter.resolve_selection()
 add('Existing selected MasterBall capture',capture,3)
 check('Capture adds actual Pokemon and returns to world',lambda:not E.is_encounter_active()and len(party())==state['party_before_capture']+1,7)
 check('Garados land companion resumes original rig after battle',lambda:companion_ok(),2)
 def restart_export():
  import shutil
  assert not ui()and not PC.is_menu_open();assert S.save_current_game(),S.get_last_storage_message();state['saved']=snapshot();p=Path(unreal.Paths.project_saved_dir())/'SaveGames/PokeMonster_Dev.sav';assert p.is_relative_to(O);shutil.copyfile(p,O/'EvolvedGarados.sav');(O/'Expected.json').write_text(json.dumps({'party':snapshot()},indent=2));assert S.load_game(),S.get_last_storage_message()
 add('Save and export exact own restart fixture',restart_export,1)
 check('Full evolved captured team survives normal load',lambda:not S.is_load_in_progress()and snapshot()==state['saved']and companion_ok(),2)

def finish(error=None):
 try:
  if 'failure_dir'in state:os.chmod(state.pop('failure_dir'),state.pop('failure_mode'))
  if PC:
   cmd('pm.Evolution.Auto 0')
   cmd('pm.EvolutionReview.ItemFixture off')
 except Exception:r['cleanup_error']=traceback.format_exc()
 r.update(passed=error is None,error=error,seconds=time.monotonic()-s['start'])
 (O/'Result.json').write_text(json.dumps(r,indent=2,ensure_ascii=False));unreal.unregister_slate_post_tick_callback(unreal._evo_v3_gameplay)
 if q.get('pie'):unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
 elif W:unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)

def tick(dt):
 global W,PC,E,S,I,C
 try:
  now=time.monotonic();assert now-s['start']<620,'Bounded evolution acceptance'
  if s['stage']=='init':
   if now-s['start']<12:return
   worlds=[w for w in unreal.ObjectIterator(unreal.World)if w.get_name().endswith('Dev_TestMap_VisualV2')and unreal.GameplayStatics.get_player_pawn(w,0)]
   if not worlds:return
   W=worlds[0];PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
   def sub(cls):return next(x for x in unreal.ObjectIterator(cls)if x.get_outer()==GI)
   E=sub(unreal.PokeMonsterEncounterSubsystem);S=sub(unreal.PokeMonsterSaveSubsystem);I=sub(unreal.PokeMonsterInventorySubsystem);C=sub(unreal.PokeMonsterWorldClock)
   assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D),'No user save storage allowed'
   cmd('pm.Evolution.Auto 0');cmd('pm.EnvPerf2.Viewport 2560 1440');build();s['stage']='actions';s['at']=now
  elif s['i']<len(route):
   name,fn,delay=route[s['i']]
   if now-s['at']<delay:return
   fn();r['cases'].append({'step':name});s['i']+=1;s['at']=now;(O/'Progress.json').write_text(json.dumps({'step':s['i'],'total':len(route),'name':name}))
  else:finish()
 except Exception:finish(traceback.format_exc())
unreal._evo_v3_gameplay=unreal.register_slate_post_tick_callback(tick)
