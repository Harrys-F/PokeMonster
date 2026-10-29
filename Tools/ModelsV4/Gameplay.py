"""Real existing bag, item-evolution sequence, buddy and native save in owned ModelsV4 UserDir only."""
import unreal,json,time,traceback,os,stat,math,shutil
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();review_root=os.environ.get('PM_REVIEW_ROOT','ModelsV4');assert review_root in ['ModelsV4','RaichuMeshyCorrection'];D=R/'Saved/ProjectRefinement'/review_root;q=json.loads((D/'Active.json').read_text());O=D/q['label'];route=[];s={'i':0,'start':time.monotonic(),'at':time.monotonic(),'ready':False};r={'checks':[],'cases':[],'performance':[],'test_team':'Original QA fixture, Pikachu level11; same individuals reordered, never replaces user team','physical_controller_test':False};state={};W=PC=P=E=S=I=C=Buddy=Input=Move=None

def cmd(x):unreal.SystemLibrary.execute_console_command(W,x,PC)
def key(x):cmd('pm.Input.Key '+x+' tap')
def party():return list(E.get_player_party())
def snapshot():return [x.export_text()for x in party()]
def item(n):return unreal.load_asset('/Game/Data/Items/DA_'+n)
def ui():return PC.get_evolution_widget()
def phase(p):return bool(ui())and ui().get_phase()==p
def add(name,fn,delay=.4):route.append((name,fn,delay))
def check(name,fn,delay=.4):
 def f():assert fn(),name;r['checks'].append(name)
 add(name,f,delay)
def shot(name):cmd('Shot filename="'+str(O/(name+'.png'))+'" -nosuffix -showui')
def feed(x=0,y=0):
 yaw=math.radians(P.get_movement_basis_yaw());Input.inject_input_vector_for_action(Move,unreal.Vector(-math.sin(yaw)*x+math.cos(yaw)*y,math.cos(yaw)*x+math.sin(yaw)*y,0),[],[])
def equivalent(before,after):
 assert before.instance_id.to_string()==after.instance_id.to_string()
 for k in ['Level','Experience','Status','StatusTurns']:assert str(before.get_editor_property(k))==str(after.get_editor_property(k)),k
 for k in ['MoveSlots','LearnedMoves']:assert [v.export_text()for v in before.get_editor_property(k)]==[v.export_text()for v in after.get_editor_property(k)],k
 assert before.calculated_stats.max_hp-before.current_hp==after.calculated_stats.max_hp-after.current_hp;return True
def buddy_ok(name='Raichu'):
 v=Buddy.get_visual();return v is not None and v.mesh.get_skeletal_mesh_asset()==unreal.load_asset('/Game/Data/Creatures/DA_'+name).get_visuals().presentation.mesh

def select_stone():
 assert not ui();assert PC.open_menu(unreal.PokeMonsterOverworldMenuSection.INVENTORY)
 ow=PC.get_overworld_widget();idx=next(j for j,v in enumerate(ow.get_view().inventory)if v.item==item('ThunderStone'))
 for n in range(idx):key('Down')
 key('Enter');assert ow.get_section()==unreal.PokeMonsterOverworldMenuSection.TEAM;assert ow.select_team_slot(0)
def roundtrip():
 assert not ui()and not PC.is_menu_open();state['saved']=snapshot();assert S.save_current_game(),S.get_last_storage_message();assert S.load_game(),S.get_last_storage_message()
def place(pos):P.set_actor_location(unreal.Vector(*pos),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
def perf(name,start=True):
 if start:cmd('csvprofile startfile=MV4_'+name);cmd('csvprofile start');state['perf']={'name':name,'frames':[],'start':time.monotonic()}
 else:
  cmd('csvprofile stop');state.setdefault('pending_csv',[]).append(name);x=state.pop('perf');x['seconds']=time.monotonic()-x['start'];r['performance'].append(x)
def export_restart():
 assert S.save_current_game();folder=Path(unreal.Paths.project_saved_dir())/'SaveGames';src=next(p for p in folder.glob('*.sav')if p.stem==('PokeMonster_SaveV2_Test_ModelsV4'if q.get('pie')else'PokeMonster_Dev'));assert src.resolve().is_relative_to(D);shutil.copyfile(src,O/'RestartFixture.sav');(O/'RestartExpected.json').write_text(json.dumps({'party':snapshot(),'stock':I.get_quantity(item('ThunderStone'))},indent=2))

def build():
 add('Load original isolated team fixture',lambda:state.update(load=S.load_game()),.1)
 check('Original three members and Pikachu level11',lambda:not S.is_load_in_progress()and len(party())>=3 and (q.get('restart')or any(str(x.species.get_internal_id())=='Pikachu'and x.level==11 for x in party())),2.)
 if q.get('restart'):
  expected=json.loads(Path(q['expected']).read_text());check('Fresh process restores exact evolved team and stock',lambda:snapshot()==expected['party']and I.get_quantity(item('ThunderStone'))==expected['stock'],1.5);check('Fresh process restores active Raichu buddy',lambda:buddy_ok(),2);add('Restart QHD',lambda:shot('Restart_Raichu'),.7);return
 def setup():
  pikachu=next(x for x in party()if str(x.species.get_internal_id())=='Pikachu');assert E.reorder_party(pikachu.instance_id,0);assert I.add_item(item('ThunderStone'),3);state['initial']=party();state['stock']=I.get_quantity(item('ThunderStone'));r['initial_party']=snapshot()
 add('Choose original Pikachu as first-slot companion and stock three real stones',setup)
 check('Original Pikachu companion visible',lambda:buddy_ok('Pikachu'),1.2)
 add('Remember single companion actor',lambda:state.update(buddy_path=Buddy.get_visual().get_path_name()))
 def invalid():
  before=snapshot();count=I.get_quantity(item('ThunderStone'));assert E.prepare_item_evolution_offer(item('ThunderStone'),1)==-1;assert E.prepare_item_evolution_offer(item('ThunderStone'),99)==-1;assert E.prepare_item_evolution_offer(item('FireStone'),0)==-1;assert snapshot()==before and I.get_quantity(item('ThunderStone'))==count
 add('Invalid species, slot and stone leave data untouched',invalid)
 add('Enable normal presentation polling',lambda:cmd('pm.Evolution.Auto 1'))
 add('Open real bag and target Pikachu',select_stone,1)
 check('Existing stone offer at level11 without early consumption',lambda:phase('offer')and I.get_quantity(item('ThunderStone'))==state['stock']and str(party()[0].pending_evolution_target.primary_asset_name)=='Raichu')
 add('Offer QHD',lambda:shot('Stone_Offer'),.7)
 add('Snapshot source and begin sequence',lambda:(state.update(before=party()),key('Enter')))
 check('Sequence stays reversible before commit',lambda:phase('transform')and str(party()[0].species.get_internal_id())=='Pikachu',2.8)
 add('A cancels running sequence',lambda:key('Escape'))
 check('Cancel keeps Pikachu, AP, individual and stone',lambda:phase('cancelled')and str(party()[0].species.get_internal_id())=='Pikachu'and equivalent(state['before'][0],party()[0])and I.get_quantity(item('ThunderStone'))==state['stock'])
 add('Cancellation QHD',lambda:shot('Stone_Cancelled'),.8)
 add('Acknowledge cancellation',lambda:key('Enter'))
 add('Same-level explicit retry',select_stone,1)
 check('Retry uses same existing offer UI',lambda:phase('offer'))
 def failure():
  folder=Path(unreal.Paths.project_saved_dir()).resolve()/'SaveGames';assert folder.is_relative_to(D);state['blocked']=(folder,stat.S_IMODE(folder.stat().st_mode));state['failed_before']=snapshot();os.chmod(folder,0o555);key('Enter')
 add('Start sequence with only isolated save folder write-blocked',failure)
 def failed():
  folder,mode=state.pop('blocked');os.chmod(folder,mode);assert phase('error')and snapshot()==state['failed_before']and I.get_quantity(item('ThunderStone'))==state['stock'];r['checks'].append('Actual UI save failure rolls back Pokemon and real ThunderStone')
 add('Restore own storage and inspect rollback',failed,6.2)
 add('Acknowledge recoverable save failure',lambda:key('Enter'))
 add('Explicit retry after failure',select_stone,1)
 add('Snapshot real source then confirm',lambda:(state.update(accepted=party()),key('Enter')))
 check('Full reveal produces Raichu and consumes exactly one stone',lambda:phase('complete')and str(party()[0].species.get_internal_id())=='Raichu'and equivalent(state['accepted'][0],party()[0])and I.get_quantity(item('ThunderStone'))==state['stock']-1,8.8)
 add('Complete original-colour reveal QHD',lambda:shot('Stone_Complete'),1)
 add('Finish existing sequence',lambda:key('Enter'))
 add('Resolve any existing target learning offer explicitly',lambda:ui().cancel()if phase('learning')else None,1)
 check('Single existing companion actor now uses Raichu',lambda:not ui()and buddy_ok()and Buddy.get_visual().get_path_name()==state['buddy_path'],1.2)
 check('Other two team individuals unchanged',lambda:all(party()[j].export_text()==state['accepted'][j].export_text()for j in [1,2]))
 check('No second item consumption from repeated resolve',lambda:not E.resolve_evolution(party()[0].instance_id,state['accepted'][0].pending_evolution_target,True)and I.get_quantity(item('ThunderStone'))==state['stock']-1)
 add('Team QHD open',lambda:PC.open_menu(unreal.PokeMonsterOverworldMenuSection.TEAM))
 add('Team after Raichu QHD',lambda:shot('Team_Raichu'),1)
 add('Close team',lambda:PC.close_menu())
 add('Save evolved real individual and load it',roundtrip)
 check('Exact all-field save/load and same companion',lambda:not S.is_load_in_progress()and snapshot()==state['saved']and buddy_ok(),2)
 add('Reorder Raichu behind reserve',lambda:E.reorder_party(party()[0].instance_id,2))
 check('Team reorder changes buddy without losing Raichu',lambda:str(party()[2].species.get_internal_id())=='Raichu'and not buddy_ok(),1)
 add('Restore same Raichu to active slot',lambda:E.reorder_party(party()[2].instance_id,0))
 check('Raichu is active again',lambda:buddy_ok(),1)
 for label,pos in [('Village',(-2500,-1700,50.15)),('Forest',(-4350,1200,50.15))]:
  add('Place for '+label,lambda pos=pos:place(pos),1)
  add('Warmup '+label,lambda:None,2)
  add('Start CSV '+label,lambda label=label:perf(label))
  add('End CSV '+label,lambda label=label:perf(label,False),12)
  add('QHD companion '+label,lambda label=label:shot('Buddy_'+label),1)
 # Actual movement input, one rig for all eight directions. Bounded world travel; AI stays enabled.
 add('Start eight direction walk',lambda:state.update(walk_start=P.get_actor_location().to_tuple(),walk_distance=0.))
 for index,(x,y)in enumerate([(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]):
  add('Move direction '+str(index),lambda x=x,y=y:state.update(move=(x,y)))
  add('Pause direction '+str(index),lambda:(state.pop('move',None),feed()),.65)
 add('Wait for companion to settle',lambda:None,3)
 check('Actual player movement and existing companion remain valid',lambda:buddy_ok()and state['walk_distance']>200)
 add('Model list and visit existing terrain',lambda:(cmd('pm.TestGround.List'),cmd('pm.TestGround.Go Raichu')),1)
 check('Raichu centrally available alongside existing18',lambda:len(unreal.PokeMonsterCreatureSpeciesData.get_registered_playable_species())==19,1.2)
 add('Model terrain QHD',lambda:shot('TestGround_Raichu'),1)
 def comparison():
  G=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureTestGround)if x.get_outer()==W);assert G.set_mode('idle');a=next(v for v,sp in zip(G.specimens,G.species)if str(sp.get_internal_id())=='Raichu');b=next(v for v,sp in zip(G.specimens,G.species)if str(sp.get_internal_id())=='Pikachu');state['comparison']=(b,b.get_actor_location(),b.get_actor_rotation());assert b.set_actor_location(a.get_actor_location()+unreal.Vector(-140,0,0),False,True);state['specimen']=a
 add('Actual unscaled Pikachu and Raichu comparison',comparison)
 add('QHD Raichu alongside Pikachu and140cm player',lambda:shot('Raichu_Pikachu_Player'),1)
 def undo_comparison():
  b,pos,rot=state.pop('comparison');b.set_actor_location(pos,False,True);b.set_actor_rotation(rot,False)
 add('Restore existing Pikachu specimen',undo_comparison)

 for mode in ['idle','walk','run','turn','directions','auto','reset']:
  add('Existing test ground '+mode,lambda mode=mode:cmd('pm.TestGround.Mode '+mode)if mode!='reset'else cmd('pm.TestGround.Reset'),1)
 add('Return from model terrain',lambda:cmd('pm.TestGround.Return'),1.5)
 check('World control and buddy restored',lambda:buddy_ok(),2)
 # Genuine existing wild actor; existing focus/encounter/capture services and the evolved team.
 def approach_wild():
  H=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterHabitatSubsystem)if x.get_outer()==W);available=[a for a in H.population if a.life_state==unreal.PokeMonsterWildLifeState.ACTIVE and a.overworld_movement.biome_habitat.medium!=unreal.PokeMonsterBiomeMedium.WATER_ONLY];assert available
  a=next((a for a in available if a.get_challenge_name()=='Myrapla'),available[0]);state['wild']=a;state['party_before_battle']=party();state['wild_id']=str(a.encounter_id);assert I.add_item(item('MasterBall'),2);t=a.get_actor_location();place((t.x-95,t.y,t.z-9.85));r['actual_encounter']={'id':str(a.encounter_id),'species':a.get_challenge_name()}
 add('Approach genuine land habitat Pokemon',approach_wild,1)
 add('Use normal player interaction',lambda:P.try_interact(),.8)
 check('Real ClassicBattle starts with Raichu and clock pause',lambda:E.is_encounter_active()and C.is_clock_paused()and str(party()[0].species.get_internal_id())=='Raichu',3)
 add('ClassicBattle Raichu QHD',lambda:shot('Raichu_ClassicBattle'),1)
 def attack():
  v=E.get_presenter().get_view();assert not v.busy and not v.presentation_pending
  slots=party()[0].get_editor_property('move_slots');idx=next(i for i,m in enumerate(v.moves)if m.enabled and m.current_pp>0 and slots[i].get_editor_property('move').base_power>0);state['attack_slot']=idx;state['attack_pp']=v.moves[idx].current_pp;assert E.get_presenter().try_select_move(idx);assert E.get_presenter().resolve_selection()
 add('Raichu uses inherited real attack',attack,1)
 def attacked():
  assert E.is_encounter_active(),'Wild source defeated before capture; inspect explicit result instead of claiming capture';v=E.get_presenter().get_view();assert not v.busy and not v.presentation_pending;assert v.moves[state['attack_slot']].current_pp==state['attack_pp']-1;r['checks'].append('Raichu attack consumes one inherited AP in genuine encounter')
 add('Inspect completed round and inherited AP',attacked,4)
 add('Throw selected real MasterBall',lambda:(E.get_presenter().try_select_capture_item(item('MasterBall'))or (_ for _ in ()).throw(AssertionError('Capture selection refused')),E.get_presenter().resolve_selection()),.7)
 check('Actual capture updates team and removes source',lambda:not E.is_encounter_active()and len(party())==len(state['party_before_battle'])+1 and E.is_encounter_completed(state['wild_id'])and state['wild'].get_editor_property('hidden'),7)
 check('Companion resumes as Raichu after capture',lambda:buddy_ok(),1.5)
 add('Export exact isolated restart fixture',export_restart)
 check('Renderer and clock unchanged',lambda:unreal.SystemLibrary.get_console_variable_int_value('r.Lumen.HardwareRayTracing')==0 and unreal.SystemLibrary.get_console_variable_int_value('r.Lumen.FinalGatherMethod')==0 and unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage')==75 and C.get_real_minutes_per_day()==120)
 r['rendering']={n:unreal.SystemLibrary.get_console_variable_float_value(n)for n in ['r.Lumen.HardwareRayTracing','r.Lumen.FinalGatherMethod','r.ScreenPercentage','r.TemporalAA.Upsampling','r.Shadow.Virtual.SMRT.RayCountDirectional']}

def finish(error=None):
 try:
  if 'blocked'in state:folder,mode=state.pop('blocked');os.chmod(folder,mode)
  if P:feed()
  if 'perf'in state:perf('Interrupted',False)
 except Exception:r['cleanup_error']=traceback.format_exc()
 r.update(passed=error is None,error=error,seconds=time.monotonic()-s['start']);(O/'Result.json').write_text(json.dumps(r,indent=2,ensure_ascii=False));unreal.unregister_slate_post_tick_callback(unreal._modelsv4_gameplay)
 if q.get('pie'):unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
 elif W:unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
def tick(dt):
 global W,PC,P,E,S,I,C,Buddy,Input,Move
 try:
  now=time.monotonic();frame=(now-s.get('last',now))*1000;s['last']=now;assert now-s['start']<800,'Bounded own acceptance'
  if not s['ready']:
   if now-s['start']<12:return
   worlds=[w for w in unreal.ObjectIterator(unreal.World)if w.get_name().endswith('Dev_TestMap_VisualV2')and unreal.GameplayStatics.get_player_pawn(w,0)]
   if not worlds:return
   W=worlds[0];PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
   def sub(cls):return next(x for x in unreal.ObjectIterator(cls)if x.get_outer()==GI)
   E=sub(unreal.PokeMonsterEncounterSubsystem);S=sub(unreal.PokeMonsterSaveSubsystem);I=sub(unreal.PokeMonsterInventorySubsystem);C=sub(unreal.PokeMonsterWorldClock);Buddy=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==W)
   assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D),'User save storage forbidden'
   Input=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if 'LocalPlayer'in x.get_outer().get_class().get_name());Move=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==P and x.get_name()=='MoveAction')
   cmd('pm.Evolution.Auto 0');cmd('pm.EnvPerf2.Viewport 2560 1440');build();s.update(ready=True,at=now);return
  if 'perf'in state:state['perf']['frames'].append(frame)
  if 'move'in state:
   pos=P.get_actor_location();previous=state.get('last_move_pos',pos.to_tuple());state['walk_distance']+=float((pos-unreal.Vector(*previous)).length());state['last_move_pos']=pos.to_tuple();feed(*state['move'])
  for name in list(state.get('pending_csv',[])):
   p=Path(unreal.Paths.project_saved_dir())/'Profiling/CSV'/('MV4_'+name+'.csv')
   if p.exists()and p.stat().st_size>1000:shutil.copyfile(p,O/('Perf_'+name+'.csv'));state['pending_csv'].remove(name)
  if s['i']>=len(route):finish();return
  name,fn,delay=route[s['i']]
  if name=='Real ClassicBattle starts with Raichu and clock pause'and not E.is_encounter_active():
   assert now-s['at']<35,'No valid normal interaction after bounded approach retries'
   if now-state.get('approach_retry',0)>1.5:
    state['approach_retry']=now;n=state.get('approach_n',0);state['approach_n']=n+1;x,y=[(1,0),(0,1),(-1,0),(0,-1)][n%4];a=state['wild'];t=a.get_actor_location();place((t.x-x*95,t.y-y*95,t.z-9.85))
    if a.can_interact(P):a.interact(P)
    else:P.try_interact()
   return
  if now-s['at']<delay:return
  fn();r['cases'].append({'step':name});s['i']+=1;s['at']=now;(O/'Progress.json').write_text(json.dumps({'step':s['i'],'total':len(route),'name':name}))
 except Exception:finish(traceback.format_exc())
unreal._modelsv4_gameplay=unreal.register_slate_post_tick_callback(tick)
