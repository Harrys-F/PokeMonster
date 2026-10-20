"""Timed real game-camera idle evidence with runtime bone sampling, not a benchmark."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ArtPassV4/IdleFinal';S.mkdir(exist_ok=False);w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0));p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);h=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor) if a.source_actor and a.source_actor.get_actor_label()=='V2_House_HouseHealer');p.set_actor_location(unreal.Vector(16900,670,50.15),False,True);bones=[str(h.visual.get_bone_name(i)) for i in range(h.visual.get_num_bones())];assert 'chest'in bones and 'head'in bones;state={'t':0.,'last':0.,'frames':[],'bone_names':bones}
def tick(dt):
 try:
  state['t']+=dt
  if state['t']>2 and state['t']-state['last']>.4:
   row={'time':state['t'],'chest_cm':h.visual.get_socket_location('chest').to_tuple(),'head_cm':h.visual.get_socket_location('head').to_tuple(),'actor_cm':h.get_actor_location().to_tuple()};state['frames'].append(row);state['last']=state['t'];unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(S/('Idle_'+str(len(state['frames'])).zfill(3)+'.png'))+'"',pc)
  if state['t']>10:
   assert len(state['frames'])>=18;assert len({tuple(r['actor_cm']) for r in state['frames']})==1;assert len({tuple(round(v,4) for v in r['head_cm']) for r in state['frames']})>4;unreal.unregister_slate_post_tick_callback(unreal._artv4_idle);state['passed']=True;(S/'Result.json').write_text(json.dumps(state,indent=2))
 except Exception:
  import traceback
  unreal.unregister_slate_post_tick_callback(unreal._artv4_idle);(S/'Failure.txt').write_text(traceback.format_exc());raise
unreal._artv4_idle=unreal.register_slate_post_tick_callback(tick)
