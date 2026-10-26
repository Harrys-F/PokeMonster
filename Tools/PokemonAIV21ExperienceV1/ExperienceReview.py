"""Real PIE UI/input/battle/XP/isolated native disk SaveLoad. No user-slot writes.
Uses existing editor-only party and victory fixtures, explicitly labelled here.
"""
import unreal,json,time,traceback,math,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/PokemonAIV21ExperienceV1';label=json.loads((D/'ReviewRequest.json').read_text())['label'];O=D/label;O.mkdir(exist_ok=False)
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W
PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
def sub(c):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==GI)
E=sub(unreal.PokeMonsterEncounterSubsystem);S=sub(unreal.PokeMonsterSaveSubsystem)
assert not E.is_encounter_active();assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_AIV21'+label)
user=R/'Saved/SaveGames/PokeMonster_Dev.sav';sha=hashlib.sha256(user.read_bytes()).hexdigest()
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
backend=unreal.SystemLibrary.get_console_variable_int_value('Slate.MacControllerPreferGCImpl')
B='Gamepad_FaceButton_Right'if backend else'Gamepad_FaceButton_Bottom';A='Gamepad_FaceButton_Bottom'if backend else'Gamepad_FaceButton_Right';X='Gamepad_FaceButton_Left'if backend else'Gamepad_FaceButton_Top'
def key(k):cmd('pm.Input.Key '+k+' down');cmd('pm.Input.Key '+k+' up')
def info():return PC.get_overworld_widget()
def xp(v):return {'valid':v.valid,'level':v.level,'total':v.total,'floor':v.level_start,'next':v.next_level_start,'earned':v.earned,'required':v.required,'remaining':v.remaining,'fraction':v.fraction,'maximum':v.maximum_level,'growth':str(v.growth)}
def party():return [(c.instance_id.to_string(),c.level,c.experience,c.current_hp,[(str(m.move),m.current_pp)for m in c.move_slots])for c in E.get_player_party()]
def capture(n):
 name='AIV21'+label+n;cmd('pm.CreatureReview.CaptureLiveUI '+name+' qhd');result['captures'].append({'name':n,'directory':str(R/'Saved/GlumandaV11/LiveUI'/name),'method':'Native Slate plus separately labelled live PIE/UMG QHD render'})
result={'technical_party_fixture':True,'ordinary_pie':True,'isolated_slot':True,'physical_controller_test':False,'backend':backend,'software_keys':{'B':B,'A':A,'X':X},'checks':[],'captures':[],'battle_samples':[]}
s={'phase':'setup','time':0.,'last':unreal.GameplayStatics.get_time_seconds(W),'wall':time.monotonic(),'sample':0.,'levelshot':False}
def phase(n):s.update(phase=n,time=0.)
def finish(error=None):
 cmd('pm.TAAReview.CaptureStop');unreal.unregister_slate_post_tick_callback(unreal._aiv21_xp)
 result.update(passed=error is None,error=error,original_save_unchanged=hashlib.sha256(user.read_bytes()).hexdigest()==sha)
 assert result['original_save_unchanged'];(O/'Result.json').write_text(json.dumps(result,indent=2));unreal.log('AIV21_XP_DONE '+str(error))
P.set_actor_location(unreal.Vector(-200,-100,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('pm.EvolutionReview.Party Zunderlauf 15')
clip=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('AIV21'+label)
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(W);delta=now-s['last'];s['last']=now;s['time']+=delta
  assert time.monotonic()-s['wall']<500,'Wall timeout'
  if E.is_encounter_active():
   v=E.get_battle_widget().get_presented_experience()
   if now-s['sample']>.06:s['sample']=now;result['battle_samples'].append({'time':now,**xp(v)})
  (O/'Progress.json').write_text(json.dumps({'phase':s['phase'],'time':s['time'],'battle':E.is_encounter_active()}))
  if s['phase']=='setup'and s['time']>.7:
   v=info().get_view().team[0].experience;assert v.valid and v.level==15
   cmd('pm.EvolutionReview.XP '+str(v.remaining-1));cmd('pm.TAAReview.CaptureStart '+str(clip)+' slate 30');phase('open');return
  if s['phase']=='open'and s['time']>.7:key(X);phase('category');return
  if s['phase']=='category'and s['time']>.6:
   assert info().is_menu_open();key('Gamepad_LeftShoulder');phase('choose');return
  if s['phase']=='choose'and s['time']>.6:key(B);phase('statusbefore');return
  if s['phase']=='statusbefore'and s['time']>1:
   v=info().get_view().team[0].experience;assert v.remaining==1 and v.earned==v.required-1
   result['before']=xp(v);capture('StatusBefore');key(A);phase('back1');return
  if s['phase']=='back1'and s['time']>.5:key(A);phase('back2');return
  if s['phase']=='back2'and s['time']>.5:key(A);phase('startbattle');return
  if s['phase']=='startbattle'and s['time']>.6:
   assert not info().is_menu_open();cmd('pm.EvolutionReview.Victory current');phase('battlebefore');return
  if s['phase']=='battlebefore'and s['time']>2:
   assert E.is_encounter_active();v=E.get_battle_widget().get_presented_experience();assert v.remaining==1
   capture('BattleBefore');key('Enter');phase('chooseattack');return
  if s['phase']=='chooseattack'and s['time']>.7:key(B);phase('battle');return
  if s['phase']=='battle':
   if E.is_encounter_active():
    v=E.get_battle_widget().get_presented_experience()
    if v.level==16 and not s['levelshot']:capture('LevelUp');s['levelshot']=True
    if E.get_presenter().get_view().learning_move:key(A)
   else:
    assert s['levelshot'],'Actual level boundary not presented';phase('after');return
   assert s['time']<40,'Battle did not complete';return
  if s['phase']=='after'and s['time']>1:
   c=E.get_player_party()[0];assert c.level==16 and c.experience>result['before']['total'];result['after_party']=party();key(X);phase('aftercategory');return
  if s['phase']=='aftercategory'and s['time']>.6:key('Gamepad_LeftShoulder');phase('afterchoose');return
  if s['phase']=='afterchoose'and s['time']>.6:key(B);phase('afterstatus');return
  if s['phase']=='afterstatus'and s['time']>1:
   v=info().get_view().team[0].experience;result['after']=xp(v);assert v.level==16 and v.remaining==v.next_level_start-v.total
   capture('StatusAfter');PC.toggle_menu();phase('save');return
  if s['phase']=='save'and s['time']>1:
   assert not P.get_component_by_class(unreal.CharacterMovementComponent).is_falling();assert S.save_current_game();s['saved']=party();s['position']=P.get_actor_location().to_tuple()
   cmd('pm.EvolutionReview.XP 31');P.set_actor_location(unreal.Vector(100,0,50.15),False,True);assert S.load_game();phase('loaded');return
  if s['phase']=='loaded'and s['time']>2:
   assert party()==s['saved'],'XP/PP/identity changed across disk SaveLoad';assert math.dist(P.get_actor_location().to_tuple(),s['position'])<.5
   key(X);phase('loadcategory');return
  if s['phase']=='loadcategory'and s['time']>.6:key('Gamepad_LeftShoulder');phase('loadchoose');return
  if s['phase']=='loadchoose'and s['time']>.6:key(B);phase('loadstatus');return
  if s['phase']=='loadstatus'and s['time']>1:
   assert xp(info().get_view().team[0].experience)==result['after'];capture('AfterLoad');key(A);phase('other');return
  if s['phase']=='other'and s['time']>.5:key('Gamepad_DPad_Down');phase('otherchoose');return
  if s['phase']=='otherchoose'and s['time']>.5:key(B);phase('otherstatus');return
  if s['phase']=='otherstatus'and s['time']>1:
   assert info().get_view().team[1].experience.level==36;capture('OtherPokemon');PC.toggle_menu();phase('maxprepare');return
  if s['phase']=='maxprepare'and s['time']>.5:cmd('pm.EvolutionReview.Party Zunderlauf 100');phase('maxopen');return
  if s['phase']=='maxopen'and s['time']>.6:key(X);phase('maxcategory');return
  if s['phase']=='maxcategory'and s['time']>.5:key('Gamepad_LeftShoulder');phase('maxchoose');return
  if s['phase']=='maxchoose'and s['time']>.5:key(B);phase('maxstatus');return
  if s['phase']=='maxstatus'and s['time']>1:
   v=info().get_view().team[0].experience;assert v.maximum_level and v.fraction==1 and v.remaining==0
   result['max']=xp(v);capture('Maximum');PC.toggle_menu();assert S.load_game();phase('finish');return
  if s['phase']=='finish'and s['time']>2:
   assert party()==s['saved'];assert not P.is_overworld_input_locked()
   result['checks']=['Actual B/A/X/L/Dpad software navigation in existing read-only info screen','Real ClassicBattle victory awards XP across level 16','Native animated XP samples and level boundary recorded','Existing disk SaveLoad preserves identity/XP/HP/PP and pose','Other individual and maximum level display','No user save modification'];finish()
 except Exception:finish(traceback.format_exc());raise
unreal._aiv21_xp=unreal.register_slate_post_tick_callback(tick)
