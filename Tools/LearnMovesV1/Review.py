"""Actual KO-XP, B/A learning decisions, repertoire, PP and menu Save/Load in existing VisualV2."""
from pathlib import Path
import unreal,json,time,traceback,hashlib
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/LearnMovesV1';q=json.loads((D/'Request.json').read_text());O=D/q['label'];W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0)
def sub(c):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==GI)
S=sub(unreal.PokeMonsterSaveSubsystem);E=sub(unreal.PokeMonsterEncounterSubsystem);assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_'+q['label'])
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor):a.overworld_movement.set_movement_paused(True);a.set_actor_enable_collision(False)
def cmd(x):unreal.SystemLibrary.execute_console_command(W,x,PC)
def key(k):
 for e in ['down','up']:cmd('pm.Input.Key '+k+' '+e)
backend=unreal.SystemLibrary.get_console_variable_int_value('Slate.MacControllerPreferGCImpl');B='Gamepad_FaceButton_Right'if backend else'Gamepad_FaceButton_Bottom';A='Gamepad_FaceButton_Bottom'if backend else'Gamepad_FaceButton_Right'
def known(c):return[str(x.get_editor_property('move').internal_id)for x in c.get_editor_property('learned_moves')]
def shot(n):cmd('pm.CreatureReview.CaptureLiveUI Learn'+q['label']+str(s['case'])+n)
cases=[('Bibor',20,'Twineedle','accept','classic','full'),('Garados',35,'Twister','accept','classic','full'),('Habitak',31,'MirrorMove','decline','classic','full'),('Karpador',30,'Flail','accept','classic','full'),('Smettbo',40,'Safeguard','accept','world','full'),('Karpador',30,'Flail','auto','classic','free')]
s={'phase':'prepare','case':0,'t':0.,'last':unreal.GameplayStatics.get_time_seconds(W),'wall':time.monotonic()};result={'cases':[],'technical_fixture':True,'physical_controller_test':False};runtime={}
def phase(n):s.update(phase=n,t=0.)
def menu_load():
 for k in ['Gamepad_Special_Right','Gamepad_DPad_Down','Gamepad_DPad_Down','Gamepad_DPad_Down',B,B]:runtime['keys'].append(k)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._learn_v1);result.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(W);s['t']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<500
  name,level,move,action,mode,slots=cases[s['case']]
  if s['phase']=='prepare'and s['t']>.6:
   assert not E.is_encounter_active()and not P.is_overworld_input_locked();cmd('pm.LearnMovesV1.Prepare '+name+' '+str(level)+' '+slots);c=E.get_player_party()[0];assert c.level==level-1 and str(c.species.get_internal_id())==name;runtime['id']=c.instance_id.to_string();result['cases'].append(dict(species=name,level=level,move=move,action=action,mode=mode,slots=slots));
   if mode=='classic':cmd('pm.EvolutionReview.Victory current')
   else:
    # Existing victory fixture chooses Classic; change only its runtime StartData via an explicit console option.
    cmd('pm.EvolutionReview.Victory current world')
   assert E.is_encounter_active();phase('ready')
  elif s['phase']=='ready'and s['t']>1:
   pr=E.get_presenter();v=pr.get_view();assert E.get_battle_widget().is_classic_presentation()==(mode=='classic');assert not v.busy;E.get_battle_widget().set_battle_menu(unreal.PokeMonsterBattleMenu.MOVES);
   if slots=='free':key('Gamepad_DPad_Right')
   key(B);phase('battle')
  elif s['phase']=='battle':
   if E.is_encounter_active():
    pr=E.get_presenter();v=pr.get_view()
    if v.learning_move:
     assert action!='auto','Unexpected offer for a free slot'
     row=result['cases'][-1];row['prompt']=str(v.learning_prompt);expected=unreal.load_asset('/Game/Data/Moves/LearnMovesV1/DA_'+move);assert str(expected.display_name)in row['prompt'];shot('Offer');phase('choose')
   elif not P.is_overworld_input_locked():phase('verify')
  elif s['phase']=='choose'and s['t']>1:
   key(B if action=='accept'else A);phase('waiting')
  elif s['phase']=='waiting'and not E.is_encounter_active()and not P.is_overworld_input_locked():phase('verify')
  elif s['phase']=='verify'and s['t']>.5:
   c=E.get_player_party()[0];assert c.instance_id.to_string()==runtime['id']and c.level>=level;assert not c.pending_moves;assert(move in known(c))==(action!='decline');assert len(c.get_editor_property('move_slots'))==4
   row=result['cases'][-1];row.update(outcome=str(E.get_last_result().outcome),known=known(c),pending=len(c.pending_moves));assert E.get_last_result().outcome==unreal.PokeMonsterEncounterOutcome.VICTORY;shot('After');assert S.save_current_game();runtime.update(party=[c.export_text()for c in E.get_player_party()],keys=[]);assert E.reorder_party(E.get_player_party()[1].instance_id,0);menu_load();phase('load')
  elif s['phase']=='load'and s['t']>.4:
   if runtime['keys']:key(runtime['keys'].pop(0));s['t']=0;return
   assert[c.export_text()for c in E.get_player_party()]==runtime['party'];assert not PC.is_menu_open()and not P.is_overworld_input_locked();result['cases'][-1]['native_disk_menu_load_exact']=True;shot('Loaded');s['case']+=1;(O/'Progress.json').write_text(json.dumps(dict(completed=s['case'],total=len(cases))))
   if s['case']==len(cases):finish();return
   phase('prepare')
 except Exception:finish(traceback.format_exc())
cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');unreal._learn_v1=unreal.register_slate_post_tick_callback(tick)
