"""Actual PIE menu/position/interior/defeat flow; only explicitly isolated disk slots."""
import unreal,json,time,traceback,hashlib,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/SaveSystemV2';req=json.loads((D/'Request.json').read_text());O=D/req['label'];W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
def sub(c):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==GI)
E=sub(unreal.PokeMonsterEncounterSubsystem);S=sub(unreal.PokeMonsterSaveSubsystem);C=sub(unreal.PokeMonsterCheckpointSubsystem);I=sub(unreal.PokeMonsterInventorySubsystem);Dialog=sub(unreal.PokeMonsterDialogueSubsystem);Cut=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterBuildingCutaway)if'V2_House'in a.get_actor_label())
assert S.use_isolated_pie_test_slot(req['slot']);slot=R/'Saved/SaveGames'/(req['slot']+'.sav');recovery=slot.with_stem(slot.stem+'_Recovery');original=R/'Saved/SaveGames/PokeMonster_Dev.sav';original_sha=hashlib.sha256(original.read_bytes()).hexdigest()
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor):a.overworld_movement.set_movement_paused(True);a.set_actor_enable_collision(False)
# These isolated placement tests retain terrain/building collision; ordinary wild encounters are separately covered by the connected regression.
route=[];state={};result={'checks':[],'steps':[],'isolated_slot':req['slot'],'ordinary_pie':True,'physical_controller_test':False,'diagnostic_start_positions':True,'original_save_before_sha256':original_sha};s={'i':0,'t':0.,'last':unreal.GameplayStatics.get_time_seconds(W),'wall':time.monotonic()}
backend=unreal.SystemLibrary.get_console_variable_int_value('Slate.MacControllerPreferGCImpl');B='Gamepad_FaceButton_Right'if backend else'Gamepad_FaceButton_Bottom';A='Gamepad_FaceButton_Bottom'if backend else'Gamepad_FaceButton_Right'
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def key(k):
 for edge in ['down','up']:cmd('pm.Input.Key '+k+' '+edge)
def axis(x=0,y=0):
 yaw=math.radians(P.get_movement_basis_yaw());cmd('pm.Input.Axis Gamepad_LeftX '+str(-math.sin(yaw)*x+math.cos(yaw)*y));cmd('pm.Input.Axis Gamepad_LeftY '+str(math.cos(yaw)*x+math.sin(yaw)*y))
def place(x,y):
 axis();P.set_actor_location(unreal.Vector(x,y,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
def snap():
 def moves(c,f):return[{'move':m.get_editor_property('move').get_path_name()if m.get_editor_property('move')else None,'pp':m.get_editor_property('current_pp')}for m in c.get_editor_property(f)]
 return {'party':[{'id':c.instance_id.to_string(),'species':c.species.get_path_name(),'level':c.level,'xp':c.experience,'hp':c.current_hp,'max_hp':c.calculated_stats.max_hp,'status':str(c.status),'turns':c.status_turns,'active':moves(c,'move_slots'),'known':moves(c,'learned_moves'),'pending':[m.get_path_name()for m in c.pending_moves],'evolution':c.pending_evolution_target.export_text(),'growth_override':c.get_editor_property('bHasExperienceGrowthOverride'),'growth':str(c.experience_growth_override)}for c in E.get_player_party()],'inventory':[x.export_text()for x in I.get_stacks()],'checkpoint':{'id':str(C.get_active_checkpoint().checkpoint_id),'map':str(C.get_active_checkpoint().map_package),'position':list(C.get_active_checkpoint().location.to_tuple()),'rotation':list(C.get_active_checkpoint().rotation.to_tuple())}}
def pose():return{'position':P.get_actor_location().to_tuple(),'rotation':P.get_actor_rotation().to_tuple(),'facing':P.get_interaction_world_direction().to_tuple()}
def restored(name):
 before=state[name];now=pose();assert math.dist(before['pose']['position'],now['position'])<.3,(name,before['pose'],now)
 assert math.dist(before['pose']['facing'],now['facing'])<.001,(name,'Facing not restored',before['pose'],now)
 assert snap()==before['data'],(name,'Persistent data mismatch',before['data'],snap())
 assert not PC.is_menu_open()and not P.is_overworld_input_locked()
 visible=[a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterCreatureVisualActor)if 'CreaturePartyCompanion'in[str(t)for t in a.tags]and not a.get_editor_property('hidden')]
 assert len(visible)==1,'Expected exactly one companion after load'
 assert visible[0].mesh.get_skeletal_mesh_asset()==E.get_player_party()[0].species.get_visuals().presentation.mesh
 result['checks'].append(name+' exact position/facing, team XP HP AP repertoire pending inventory checkpoint restored')
def remember(name):state[name]={'pose':pose(),'data':snap()};result[name]=state[name]
def act(name,fn,delay=.4):route.append((name,fn,delay,None))
def check(name,fn):
 def f():assert fn(),name;result['checks'].append(name)
 act(name,f)
def wait(name,pred,timeout=35):route.append((name,lambda:None,timeout,pred))
def shot(n):cmd('HighResShot 2560x1440 filename="'+str(O/(n+'.png'))+'"');cmd('pm.CreatureReview.CaptureLiveUI SaveV2'+req['label']+n)
def menu(index,confirm=True):
 act('Plus opens main '+str(index),lambda:key('Gamepad_Special_Right'))
 if req.get('mode')=='restart'and index==3:act('Actual main-menu load options',lambda:shot('MenuLoadOptions'))
 for i in range(index):act('Dpad '+str(i),lambda:key('Gamepad_DPad_Down'))
 act('B requests storage action '+str(index),lambda:key(B))
 if confirm:
  if req.get('mode')=='restart'and index==3:act('Actual manual-load confirmation',lambda:shot('ConfirmLoad'))
  act('B explicitly confirms storage action '+str(index),lambda:key(B))
def close():
 if PC.is_menu_open():key(A)

action=req.get('mode','main')
if action=='restart':
 assert slot.exists();state['C']=json.loads((D/req['source_label']/'Result.json').read_text())['C']
 menu(3);act('G new PIE session restores previous manual slot',lambda:restored('C'),1.)
 check('G fresh GameInstance reads the isolated on-disk save',lambda:len(E.get_player_party())==2)
 act('G real screenshot',lambda:shot('FreshSessionLoaded'))
else:
 assert not slot.exists()and not recovery.exists()
 act('Existing nontrivial party fixture',lambda:cmd('pm.EvolutionReview.Party Zunderlauf 18'))
 act('Existing XP service makes a real pending level19 move',lambda:cmd('pm.EvolutionReview.XP next'))
 act('Forest diagnostic start',lambda:place(-1900,530),.8)
 act('Face along existing world-input direction',lambda:axis(0,1),.2);act('Stop before saving',axis,.6)
 check('Pending learn offer exists and PP are spent',lambda:len(E.get_player_party()[0].pending_moves)>0 and E.get_player_party()[0].get_editor_property('move_slots')[0].current_pp<E.get_player_party()[0].get_editor_property('move_slots')[0].get_editor_property('move').max_pp)
 menu(2,False);check('First B does not write a save',lambda:not slot.exists());act('A cancels before any write',lambda:key(A));check('Cancel preserves absent slot',lambda:not slot.exists());act('Close',close)
 menu(2);act('Remember A',lambda:remember('A'));check('A uses isolated actual disk slot',slot.exists);act('A close menu',close);act('A forest screenshot',lambda:shot('ForestSaved'))
 act('Move away with normal stick input',lambda:axis(1,0),.8);act('Stop',axis,.5)
 act('Change team order before Load',lambda:E.reorder_party(E.get_player_party()[1].instance_id,0));act('Record changed state',lambda:state.update(cancel_pose=pose(),cancel_data=snap(),cancel_sha=hashlib.sha256(slot.read_bytes()).hexdigest()))
 menu(3,False);act('Cancel Load with A',lambda:key(A));check('Cancelling Load changes no data or file',lambda:snap()==state['cancel_data']and hashlib.sha256(slot.read_bytes()).hexdigest()==state['cancel_sha']);act('Close',close)
 menu(3);act('A real saved world position restored',lambda:restored('A'),.8);act('A loaded screenshot',lambda:shot('ForestLoaded'))
 act('Keep manual hash before automatic healing',lambda:state.update(manual_before_heal=hashlib.sha256(slot.read_bytes()).hexdigest()));act('Door diagnostic approach',lambda:place(-3610,500),.8);act('Walk through original entrance',lambda:axis(1,0),.85);act('Stop after door',axis,1.5)
 check('Actual doorway enters existing relocated room',lambda:Cut.is_viewer_relocated()and P.is_using_interior_movement_basis())
 act('Healer diagnostic approach in same room',lambda:place(17230,555),.8);act('Face Healer',lambda:axis(0,-1),.12);act('Stop',axis,.4);act('B speaks to existing healer',lambda:key(B))
 check('Dialog blocks both save and load',lambda:Dialog.is_dialogue_active()and not S.save_current_game()and not S.load_game())
 act('B accepts healing/checkpoint',lambda:key(B));act('B closes healing result',lambda:key(B),.6)
 check('Existing healer activates independent checkpoint',lambda:str(C.get_active_checkpoint().checkpoint_id)=='VisualV2_HealingHouse'and not Dialog.is_dialogue_active())
 check('Automatic healing save preserves the manual slot',lambda:S.has_recovery_game()and hashlib.sha256(slot.read_bytes()).hexdigest()==state['manual_before_heal'])
 menu(2);act('Remember B',lambda:remember('B'));act('Close',close);act('B interior saved screenshot',lambda:shot('InteriorSaved'))
 act('Outside diagnostic relocation',lambda:place(-4100,450),1.2);check('Outside camera returns before load',lambda:not P.is_using_interior_movement_basis())
 menu(3);act('B indoor pose and data restore',lambda:restored('B'),1.)
 check('B indoor cutaway camera and room restored immediately',lambda:Cut.is_viewer_relocated()and Cut.get_cutaway_amount()==1. and P.is_using_interior_movement_basis());act('B loaded interior screenshot',lambda:shot('InteriorLoaded'))
 act('Inside doorway approach',lambda:place(16460,500),.8);act('Walk through existing exit',lambda:axis(-1,0),.85);act('Stop outside',axis,1.5);check('Original room exit works after Load',lambda:not Cut.is_viewer_relocated()and not P.is_using_interior_movement_basis())
 act('C forest saved position distinct from healer',lambda:place(-1900,530),.8);act('Reinstall existing injured/spent-PP level18 fixture',lambda:cmd('pm.EvolutionReview.Party Zunderlauf 18'));act('Pending level19 offer',lambda:cmd('pm.EvolutionReview.XP next'))
 menu(2);act('Remember C',lambda:remember('C'));act('Record immutable manual file before defeat',lambda:state.update(manual_sha=hashlib.sha256(slot.read_bytes()).hexdigest()));act('Close',close)
 check('C normal save did not change healer checkpoint',lambda:str(C.get_active_checkpoint().checkpoint_id)=='VisualV2_HealingHouse'and P.get_actor_location().distance(C.get_active_checkpoint().location)>10000)
 act('C move away',lambda:axis(1,0),.6);act('Stop',axis,.5);menu(3);act('C load returns to forest not checkpoint',lambda:restored('C'),1.)
 act('Existing actual defeat encounter',lambda:cmd('pm.BattleV3.Start classic defeat'),1.)
 check('Battle blocks save and load without changing file',lambda:E.is_encounter_active()and not S.save_current_game()and not S.load_game()and hashlib.sha256(slot.read_bytes()).hexdigest()==state['manual_sha'])
 def lose():
  if E.is_encounter_active():
   pr=E.get_presenter();v=pr.get_view()
   if not v.busy and not v.finished:assert pr.try_select_move(0);assert pr.resolve_selection()
   return False
  return not P.is_overworld_input_locked()
 wait('Actual battle, defeat and existing recovery sequence finish',lose,90)
 check('D defeat returns only to saved checkpoint and heals team',lambda:E.get_last_result().outcome==unreal.PokeMonsterEncounterOutcome.DEFEAT and C.was_last_recovery_saved()and P.get_actor_location().distance(C.get_active_checkpoint().location)<.5 and all(c.current_hp==c.calculated_stats.max_hp for c in E.get_player_party()))
 check('D separate recovery file exists; manual file byte-identical',lambda:recovery.exists()and hashlib.sha256(slot.read_bytes()).hexdigest()==state['manual_sha'])
 check('D interior camera restored after checkpoint return',lambda:Cut.is_viewer_relocated()and P.is_using_interior_movement_basis());act('D recovery screenshot',lambda:shot('DefeatRecovery'))
 act('Remember separate recovery state',lambda:remember('D'));act('Move outside before recovery-slot load',lambda:place(-4100,450),1.)
 menu(4);act('Recovery menu restores healed checkpoint state',lambda:restored('D'),1.)
 check('Recovery load does not replace the manual slot',lambda:hashlib.sha256(slot.read_bytes()).hexdigest()==state['manual_sha'])
 menu(3);act('E manual load restores pre-defeat pose and full earlier state',lambda:restored('C'),1.);act('E normal scene screenshot',lambda:shot('ManualAfterDefeat'))
 check('F team level XP HP spent PP known moves pending preserved',lambda:snap()==state['C']['data']and len(E.get_player_party()[0].pending_moves)>0)

def finish(error=None):
 axis();unreal.unregister_slate_post_tick_callback(unreal._save_v2_review);result.update(passed=error is None,error=error,original_save_unchanged=hashlib.sha256(original.read_bytes()).hexdigest()==original_sha,final_position=pose(),final_data=snap(),elapsed_game_seconds=unreal.GameplayStatics.get_time_seconds(W)-s['start_time']);(O/'Result.json').write_text(json.dumps(result,indent=2));unreal.log('SAVE_V2_REVIEW_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(W);s['t']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<540,'Review timeout'
  name,fn,delay,pred=route[s['i']]
  if pred:
   if not pred():assert s['t']<delay,name;return
  elif s['t']<delay:return
  fn();result['steps'].append({'name':name,'position':pose(),'time':now});s['i']+=1;s['t']=0.;(O/'Progress.json').write_text(json.dumps({'step':s['i'],'last':name,'time':now},indent=2))
  if s['i']==len(route):finish()
 except Exception:finish(traceback.format_exc())
s['start_time']=unreal.GameplayStatics.get_time_seconds(W);cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');unreal._save_v2_review=unreal.register_slate_post_tick_callback(tick)
