import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();w=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0));gi=unreal.GameplayStatics.get_game_instance(w);enc=next(s for s in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if s.get_outer()==gi)
O=R/'Saved/MeshyGlumandaV1/Acceptance'/json.loads((R/'Saved/MeshyGlumandaV1/AcceptanceRequest.json').read_text())['label'];state={'t':0.,'battle_shots':0,'seen_reactions':set(),'samples':[],'last_shot':0.,'party_zunderlauf':False,'deactivated_source_hidden_checked':False};pc=unreal.GameplayStatics.get_player_controller(w,0)
def observe(dt):
 try:
  state['t']+=dt
  if enc.is_encounter_active():
   actors=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterCreatureVisualActor)
   visible=[a for a in actors if not a.get_editor_property('hidden')]
   reactions=[str(a.reaction)for a in visible];state['seen_reactions'].update(reactions)
   if state['battle_shots']<28 and state['t']-state['last_shot']>.6:
    ui=state['battle_shots']%2==1;name=('BattleUI_'if ui else'BattleWorld_')+str(state['battle_shots']).zfill(3)+'.png';unreal.SystemLibrary.execute_console_command(w,('Shot showui'if ui else'Shot')+' filename="'+str(O/name)+'"',pc);state['battle_shots']+=1;state['last_shot']=state['t'];state['samples'].append({'time':state['t'],'file':name,'capture_kind':'editor_ui'if ui else'game_viewport_qhd','visible_3d_creatures':len(visible),'reactions':reactions,'creatures':[{'position':a.get_actor_location().to_tuple(),'foot_l':a.mesh.get_socket_location('foot_L').to_tuple(),'foot_r':a.mesh.get_socket_location('foot_R').to_tuple()}for a in visible]})
  if any(str(c.species.get_path_name()).endswith('DA_Zunderlauf.DA_Zunderlauf')for c in enc.get_player_party()):state['party_zunderlauf']=True
  if not enc.is_encounter_active():
   for owner in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor):
    if owner.get_editor_property('hidden'):
     for child in owner.get_attached_actors():
      if isinstance(child,unreal.PokeMonsterCreatureVisualActor):assert child.get_editor_property('hidden'),'Captured creature presentation still visible';state['deactivated_source_hidden_checked']=True
  if (O/'FootTest.json').exists():
   unreal.unregister_slate_post_tick_callback(unreal._zunderlauf_gameplay_observer);state['seen_reactions']=sorted(state['seen_reactions']);(O/'CreatureGameplay.json').write_text(json.dumps(state,indent=2));return
 except Exception:
  import traceback
  unreal.unregister_slate_post_tick_callback(unreal._zunderlauf_gameplay_observer);(O/'ObserverFailure.txt').write_text(traceback.format_exc());raise
unreal._zunderlauf_gameplay_observer=unreal.register_slate_post_tick_callback(observe)
