"""Actual existing-map PIE and Slate input. The NPC/party fixture is explicitly transient."""
import unreal,json,time,hashlib,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/MoveManagementV2';label=json.loads((O/'ReviewRequest.json').read_text())['label'];D=O/label;D.mkdir(exist_ok=False)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);ui=pc.get_overworld_widget();gi=unreal.GameplayStatics.get_game_instance(w)
enc=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi);save=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==gi)
assert save.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_Master'+label)
slot=R/'Saved/SaveGames'/('PokeMonster_SaveV2_Test_Master'+label+'_Recovery.sav');assert not slot.exists(),'Use a fresh isolated label'
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
old_percentage=unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage')
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 if a.get_class().get_name()=='PokeMonsterVisibleWildCreatureActor':a.destroy_actor()
 if a.get_class().get_name()=='PokeMonsterWildEncounterZone':a.set_actor_enable_collision(False)
backend=unreal.SystemLibrary.get_console_variable_int_value('Slate.MacControllerPreferGCImpl');B='Gamepad_FaceButton_Right'if backend else'Gamepad_FaceButton_Bottom';A='Gamepad_FaceButton_Bottom'if backend else'Gamepad_FaceButton_Right';X='Gamepad_FaceButton_Left'if backend else'Gamepad_FaceButton_Top'
result={'simulated_inputs_not_hardware':True,'technical_unsaved_NPC':True,'checks':[],'shots':[],'backend':backend};route=[];state={};last=time.monotonic();index=0

def cmd(s):unreal.SystemLibrary.execute_console_command(w,s,pc)
def action(name,fn,delay=.3):route.append((name,fn,delay))
def check(name,fn):
 def run():
  assert fn(),name
  result['checks'].append(name)
 action(name,run)
def key(name,k,repeat=False):
 action(name+' down',lambda:cmd('pm.Input.Key '+k+' down'+(' repeat'if repeat else'')),.16)
 action(name+' up',lambda:cmd('pm.Input.Key '+k+' up'),.24)
def down(n):
 for i in range(n):key('next '+str(i),'Gamepad_DPad_Down')
def snap():
 def moves(c,field):
  return [dict(move=s.get_editor_property('move').get_path_name()if s.get_editor_property('move')else None,pp=s.get_editor_property('current_pp'),max=s.get_editor_property('max_pp'))for s in c.get_editor_property(field)]
 return [dict(id=c.instance_id.to_string(),level=c.level,xp=c.experience,hp=c.current_hp,active=moves(c,'move_slots'),known=moves(c,'learned_moves'),pending=[m.get_path_name()for m in c.pending_moves])for c in enc.get_player_party()]
def title():
 return str(next(x for x in unreal.ObjectIterator(unreal.TextBlock)if x.get_name()=='SectionTitle'and x.get_path_name().startswith(ui.get_path_name())).get_editor_property('text'))
def shot(name):
 capture=label+'_'+name;cmd('pm.CreatureReview.CaptureLiveUI '+capture);path=R/'Saved/GlumandaV11/LiveUI'/capture/'ActualSlateViewport.png';assert path.exists();result['shots'].append(str(path))
def save_hash():return hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None

cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');cmd('pm.MoveManagementV2.Prepare')
assert len(enc.get_player_party())==2;state['initial']=snap();result['before']=state['initial'];state['master']=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPC)if'TechnicalTest_MasterOfMemories'in a.get_name())
result['NPC']={'path':state['master'].get_path_name(),'position':state['master'].get_actor_location().to_tuple(),'not_a_valley_placement':True}
key('X existing menu',X);key('L read-only moves','Gamepad_LeftShoulder');check('Normal moves view is read-only',lambda:'Nur Ansicht'in title());key('B selects first pokemon',B);action('capture read-only repertoire',lambda:shot('ReadOnlyRepertoire'))
key('B inspects inactive attack',B);check('Normal menu cannot reactivate',lambda:snap()==state['initial']);action('capture inactive reminder',lambda:shot('InactiveReminder'))
key('A returns to pokemon list',A);key('A returns to team',A);key('A closes normal menu',A);check('World focus returns',lambda:not pc.is_menu_open()and not p.is_overworld_input_locked())
key('B interacts with actual temporary NPC',B);check('Existing B interaction opens master',lambda:pc.is_menu_open()and'Meister der Erinnerungen'in title());key('B selects first learner',B);action('capture master repertoire',lambda:shot('MasterRepertoire'))
key('B picks old Tackle at full set',B);key('Down selects replacement slot one','Gamepad_DPad_Down');key('B edits draft',B);check('Draft has not mutated creature',lambda:snap()==state['initial']);down(5);key('B opens review',B);action('capture explicit review',lambda:shot('MasterReview'));key('A cancels review',A);key('A discards draft',A);key('A closes master',A);check('Cancellation preserves complete individual state',lambda:snap()==state['initial']and not slot.exists())
key('B reopens master',B);key('B selects learner again',B);key('B picks remembered Tackle',B);key('Down chooses slot one again','Gamepad_DPad_Down');key('B replaces in draft',B);down(5);key('B reviews changes',B);key('B confirms and saves',B)
check('Confirmation closes master and saves',lambda:not pc.is_menu_open()and slot.exists());action('record first commit',lambda:state.update(committed=snap(),saved=save_hash()))
check('First individual retains five known moves',lambda:len(snap()[0]['known'])==5);check('Other individual remains distinct and unchanged',lambda:snap()[1]==state['initial'][1]);check('Old Tackle retains spent AP after reactivation',lambda:snap()[0]['active'][1]==state['initial'][0]['known'][0]);check('New Water Gun retains spent AP',lambda:snap()[0]['active'][0]==state['initial'][0]['active'][0])
action('load via existing save system',lambda:save.load_recovery_game());check('Saved loadout and inactive AP restore exactly',lambda:snap()==state['committed'])
# Remove and append an active move to reorder it. All changes remain a draft until reviewed.
key('B opens master for ordering',B);key('B selects same individual',B);down(4);key('B removes Water Gun from draft',B);key('B appends Water Gun at end',B);down(1);key('B reviews order',B);action('capture reordered draft',lambda:shot('MasterReorderedReview'));key('B saves order',B)
check('Order change preserved PP and complete repertoire',lambda:snap()[0]['known']==state['initial'][0]['known']and snap()[0]['active'][3]==state['initial'][0]['active'][0]and snap()[1]==state['initial'][1]);action('remember ordered save',lambda:state.update(ordered=snap()))
action('load order',lambda:save.load_recovery_game());check('Order survives save/load',lambda:snap()==state['ordered']);key('X final read-only view',X);key('L final moves','Gamepad_LeftShoulder');key('B final pokemon',B);action('capture saved result',lambda:shot('SavedRepertoire'));key('A leave details',A);key('A leave moves',A);key('A close',A)
# Actual battle lock uses the existing system; no new battle logic or UI.
action('existing classic fixture',lambda:cmd('pm.BattleV3.Start classic wild'),1.5);check('ClassicBattle active',lambda:enc.is_encounter_active());action('remember combat state',lambda:state.update(combat=snap()))
key('B is battle input, not NPC interaction',B);check('No master/menu during battle',lambda:not pc.is_menu_open());check('Normal menu API blocked during battle',lambda:not pc.open_menu(unreal.PokeMonsterOverworldMenuSection.MOVES));check('Battle input has not changed persistent loadout',lambda:snap()==state['combat'])

def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._move_management_v2_review);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);cmd('pm.EnvPerf2.Viewport 0 0');cmd('r.ScreenPercentage '+str(old_percentage))
 result.update(passed=error is None,error=error,after=snap(),save_after_sha256=save_hash());(D/'Result.json').write_text(json.dumps(result,indent=2));unreal.log('MOVE_MANAGEMENT_V2_PIE_RESULT '+str(result['passed']))
def tick(dt):
 global last,index
 try:
  if time.monotonic()-last<route[index][2]:return
  name,fn,_=route[index];fn();index+=1;last=time.monotonic();(D/'Progress.json').write_text(json.dumps({'step':name,'checks':result['checks']},indent=2))
  if index>=len(route):finish()
 except Exception:finish(traceback.format_exc())
unreal._move_management_v2_review=unreal.register_slate_post_tick_callback(tick)
