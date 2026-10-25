"""Original Wanderer and healer source interactions, under the NPC-ground RAM save guard."""
import unreal,json,time,traceback,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/NPCExpansion';W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W
P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W);D=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterDialogueSubsystem)if x.get_outer()==GI);Save=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==GI);Enc=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==GI);slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';sha=hashlib.sha256(slot.read_bytes()).hexdigest();G=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterNPCTestGround)if x.get_outer()==W);assert G.set_mode('idle') and G.visit(1)
S=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=S.get_editor_property('bThrottleCPUWhenNotForeground');S.set_editor_property('bThrottleCPUWhenNotForeground',False)
visuals=unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterNPCVisualActor);wander=next(v for v in visuals if v.source_actor and isinstance(v.source_actor,unreal.PokeMonsterNPC) and str(v.source_actor.display_name)=='Wanderer');healer=next(v for v in visuals if v.get_editor_property('bShadowlessInteriorPresentation') and v.source_actor);cases=[('Wanderer',wander),('Heilerin',healer)];state={'case':0,'phase':'position','since':0.,'last':unreal.GameplayStatics.get_time_seconds(W),'checks':[]};start=time.monotonic()
backend=unreal.SystemLibrary.get_console_variable_int_value('Slate.MacControllerPreferGCImpl');B='Gamepad_FaceButton_Right'if backend else'Gamepad_FaceButton_Bottom'
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def key(t):cmd('pm.Input.Key '+t+' down');cmd('pm.Input.Key '+t+' up')
def step(s):state['phase']=s;state['since']=0.
def finish(error=None):
 if D.is_dialogue_active():D.close_dialogue()
 cmd('pm.Input.Axis Gamepad_LeftY 0');G.return_to_world();S.set_editor_property('bThrottleCPUWhenNotForeground',throttle);unreal.unregister_slate_post_tick_callback(unreal._npc_existing);state.update(passed=error is None,error=error,save_unchanged=hashlib.sha256(slot.read_bytes()).hexdigest()==sha);(O/'ExistingInteractions.json').write_text(json.dumps(state,indent=2));unreal.log('PM_NPC_EXISTING_INTERACTIONS '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(W);state['since']+=now-state['last'];state['last']=now;assert time.monotonic()-start<180
  name,V=cases[state['case']];N=V.source_actor;pos=N.get_actor_location();phase=state['phase'];t=state['since']
  if phase=='position':
   # Diagnostic positioning, not a claimed door/landscape footrun.
   P.set_actor_location(unreal.Vector(pos.x-80,pos.y+80,49),False,True);cmd('pm.Input.Axis Gamepad_LeftY 1');step('face')
  elif phase=='face'and t>.15:
   cmd('pm.Input.Axis Gamepad_LeftY 0');f=P.get_interaction_world_direction();P.set_actor_location(unreal.Vector(pos.x-f.x*105,pos.y-f.y*105,49),False,True);step('settle')
  elif phase=='settle'and t>2:key(B);step('check')
  elif phase=='check'and t>.6:
   assert D.is_dialogue_active() and D.get_active_source()==N,(name,'Existing B interaction did not reach original source');assert V.is_conversing();state['checks'].append(name+' original dialogue source and presentation response');cmd('HighResShot 2560x1440 filename="'+str(O/(name+'_Interaction_QHD.png'))+'"');step('talk')
  elif phase=='talk'and t>3.2:step('advance')
  elif phase=='advance':
   if D.is_dialogue_active():key(B);step('waitpage')
   else:
    if name=='Heilerin':
     assert all(c.current_hp==c.calculated_stats.max_hp for c in Enc.get_player_party());state['checks'].append('Original healer restores party HP; RAM save only')
    state['case']+=1
    if state['case']==len(cases):
     assert Save.save_current_game() and Save.load_game();state['checks'].append('Existing interaction Save/Load roundtrip');finish();return
    step('position')
  elif phase=='waitpage'and t>.3:step('advance')
 except Exception:finish(traceback.format_exc())
unreal._npc_existing=unreal.register_slate_post_tick_callback(tick)
