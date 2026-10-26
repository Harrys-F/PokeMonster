"""Regular existing evolution UI, then save/load only after return to safe play."""
from pathlib import Path
import unreal,json,time,traceback,hashlib,math
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/SaveSystemV2';q=json.loads((D/'Request.json').read_text());O=D/q['label'];W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0)
def sub(c):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==GI)
S=sub(unreal.PokeMonsterSaveSubsystem);E=sub(unreal.PokeMonsterEncounterSubsystem);assert S.use_isolated_pie_test_slot(q['slot']);slot=R/'Saved/SaveGames'/(q['slot']+'.sav');assert not slot.exists();original=R/'Saved/SaveGames/PokeMonster_Dev.sav';sha=hashlib.sha256(original.read_bytes()).hexdigest()
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor):a.overworld_movement.set_movement_paused(True);a.set_actor_enable_collision(False)
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def key(k):
 for edge in ['down','up']:cmd('pm.Input.Key '+k+' '+edge)
backend=unreal.SystemLibrary.get_console_variable_int_value('Slate.MacControllerPreferGCImpl');B='Gamepad_FaceButton_Right'if backend else'Gamepad_FaceButton_Bottom'
result={'checks':[],'isolated_slot':q['slot']};state={};route=[];s={'i':0,'t':0.,'last':unreal.GameplayStatics.get_time_seconds(W),'wall':time.monotonic()}
def act(n,f,d=.5):route.append((n,f,d,None))
def check(n,f):
 def run():assert f(),n;result['checks'].append(n)
 act(n,run)
def wait(n,f,d=25):route.append((n,lambda:None,d,f))
def phase(n):return PC.get_evolution_widget()and PC.get_evolution_widget().get_phase()==n
cmd('pm.EvolutionReview.Party Zunderlauf 15');assert S.save_current_game();before=hashlib.sha256(slot.read_bytes()).hexdigest();cmd('pm.Evolution.Auto 1');cmd('pm.EvolutionReview.XP next')
wait('Existing regular offer',lambda:phase('offer'))
act('B starts unchanged V2.1 sequence',lambda:key(B));act('Observe active transformation',lambda:None,2.)
check('Save and Load blocked during active evolution; file untouched',lambda:phase('transform')and not S.save_current_game()and not S.load_game()and hashlib.sha256(slot.read_bytes()).hexdigest()==before)
wait('Full original-color reveal and completion',lambda:phase('complete'))
check('Correct evolved species and original individual retained',lambda:str(E.get_player_party()[0].species.get_internal_id())=='Glutexo'and len(E.get_player_party())==2)
act('Actual completed evolution capture',lambda:cmd('pm.CreatureReview.CaptureLiveUI SaveV2'+q['label']+'Complete'))
act('B returns to normal play',lambda:key(B));wait('Evolution UI fully closed',lambda:not PC.get_evolution_widget())
act('Disable only further automatic review offers',lambda:cmd('pm.Evolution.Auto 0'))
act('Record exact evolved data and pose',lambda:state.update(party=[c.export_text()for c in E.get_player_party()],position=P.get_actor_location().to_tuple(),facing=P.get_interaction_world_direction().to_tuple()))
check('Saving immediately after evolution succeeds',lambda:S.save_current_game())
act('Change team order',lambda:E.reorder_party(E.get_player_party()[1].instance_id,0));act('Move diagnostic position away',lambda:P.set_actor_location(P.get_actor_location()+unreal.Vector(140,0,0),False,True),.7)
check('Loading evolved state succeeds',lambda:S.load_game())
check('Evolved identity, all PP, repertoire and position restored',lambda:[c.export_text()for c in E.get_player_party()]==state['party']and math.dist(P.get_actor_location().to_tuple(),state['position'])<.3 and math.dist(P.get_interaction_world_direction().to_tuple(),state['facing'])<.001 and not P.is_overworld_input_locked())
act('Capture evolved companion after Load',lambda:cmd('HighResShot 2560x1440 filename="'+str(O/'EvolvedLoaded.png')+'"'))
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._save_v2_evolution);result.update(passed=error is None,error=error,original_save_unchanged=hashlib.sha256(original.read_bytes()).hexdigest()==sha);(O/'Result.json').write_text(json.dumps(result,indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(W);s['t']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<150
  n,f,d,pred=route[s['i']]
  if pred:
   if not pred():assert s['t']<d,n;return
  elif s['t']<d:return
  f();s['i']+=1;s['t']=0;(O/'Progress.json').write_text(json.dumps({'step':s['i'],'last':n},indent=2))
  if s['i']==len(route):finish()
 except Exception:finish(traceback.format_exc())
unreal._save_v2_evolution=unreal.register_slate_post_tick_callback(tick)
