"""Real three-tab controller navigation and pending-learning RAM persistence; no move/master system changes."""
import unreal,json,time,hashlib,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GameplayPraxisV1';req=json.loads((D/'Request.json').read_text());O=D/req['label'];W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W);E=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==GI);Save=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==GI);UI=PC.get_overworld_widget();s={'i':0,'t':0.,'last':unreal.GameplayStatics.get_time_seconds(W),'checks':[]};start=time.monotonic();route=[]
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def key(k):
 for state in ['down','up']:cmd('pm.Input.Key '+k+' '+state)
backend=unreal.SystemLibrary.get_console_variable_int_value('Slate.MacControllerPreferGCImpl');B='Gamepad_FaceButton_Right'if backend else'Gamepad_FaceButton_Bottom';A='Gamepad_FaceButton_Bottom'if backend else'Gamepad_FaceButton_Right';X='Gamepad_FaceButton_Left'if backend else'Gamepad_FaceButton_Top'
def party():return[c.export_text()for c in E.get_player_party()]
def act(name,fn):route.append((name,fn))
def check(name,fn):
 def f():assert fn(),name;s['checks'].append(name)
 act(name,f)
# A rare pending offer is prepared with existing native debug/progression APIs, not fabricated move values.
cmd('pm.EvolutionReview.Party Zunderlauf 18');cmd('pm.EvolutionReview.XP next');before=party();fire=E.get_player_party()[0];assert fire.level==19 and len(fire.pending_moves)>0;s['pending']=[x.get_path_name()for x in fire.pending_moves];s['original_pending_state']=before;assert Save.save_current_game()and Save.load_game()and party()==before;s['checks'].append('Open level19 learning offer, IDs, AP and repertoire survive exact RAM Save/Load');assert len(fire.get_editor_property('move_slots'))==4
act('X team',lambda:key(X));check('Team tab',lambda:UI.get_section()==unreal.PokeMonsterOverworldMenuSection.TEAM)
act('R inventory',lambda:key('Gamepad_RightShoulder'));check('Inventory tab',lambda:UI.get_section()==unreal.PokeMonsterOverworldMenuSection.INVENTORY)
act('R repertoire',lambda:key('Gamepad_RightShoulder'));check('Third repertoire tab',lambda:UI.get_section()==unreal.PokeMonsterOverworldMenuSection.MOVES)
act('B choose personal creature',lambda:key(B));act('Dpad repertoire choice',lambda:key('Gamepad_DPad_Down'));act('B views move without changing set',lambda:key(B));check('Normal repertoire is read-only including PP and pending offers',lambda:party()==before and not E.is_encounter_active())
act('Capture real repertoire UI',lambda:cmd('pm.CreatureReview.CaptureLiveUI Praxis'+req['label']+'ReadOnly'))
act('A back to creature choice',lambda:key(A));act('L inventory',lambda:key('Gamepad_LeftShoulder'));check('L goes back to inventory',lambda:UI.get_section()==unreal.PokeMonsterOverworldMenuSection.INVENTORY)
act('L team',lambda:key('Gamepad_LeftShoulder'));check('L goes back to team',lambda:UI.get_section()==unreal.PokeMonsterOverworldMenuSection.TEAM)
act('A close',lambda:key(A));check('Three-tab journey returns input and retains pending offer',lambda:not PC.is_menu_open()and not P.is_overworld_input_locked()and party()==before)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._praxis_repertoire);s.update(passed=error is None,error=error,software_inputs_not_hardware=True);(O/'Result.json').write_text(json.dumps(s,indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(W);s['t']+=now-s['last'];s['last']=now;assert time.monotonic()-start<50
  if s['t']>.35:
   name,fn=route[s['i']];fn();s['i']+=1;s['t']=0
   if s['i']==len(route):finish()
 except Exception:finish(traceback.format_exc())
unreal._praxis_repertoire=unreal.register_slate_post_tick_callback(tick)
