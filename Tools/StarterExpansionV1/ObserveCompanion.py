"""Read-only companion acceptance alongside the unchanged full walking/gameplay route."""
import unreal,json,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();request=json.loads((R/'Saved/GlumandaV11/AcceptanceRequest.json').read_text());O=R/'Saved/GlumandaV11/Acceptance'/request['label'];w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();p=unreal.GameplayStatics.get_player_pawn(w,0);gi=unreal.GameplayStatics.get_game_instance(w);e=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi);c=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==w);log=(O/'CompanionFrames.jsonl').open('w');state={'samples':0,'battle_hidden_samples':0,'interior_shadowless_samples':0,'max_distance':0.,'issues':[]};last=[-1.];room=[False,0.];previous=[None];buildings=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterBuildingCutaway)
def tick(dt):
 try:
  if (O/'FootTest.json').exists():
   log.close();(O/'CompanionResult.json').write_text(json.dumps(state,indent=2));unreal.unregister_slate_post_tick_callback(unreal._starter_companion_observer);return
  now=unreal.GameplayStatics.get_time_seconds(w)
  if now-last[0]<.25:return
  last[0]=now;v=c.get_visual();m=c.get_movement();visuals=[a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterCreatureVisualActor)if 'CreaturePartyCompanion'in [str(t)for t in a.tags]];assert len(visuals)<=1
  interior=p.is_using_interior_movement_basis()
  if room[0]!=interior:room[:]=[interior,now]
  row={'time':now,'player':p.get_actor_location().to_tuple(),'interior':interior,'battle':e.is_encounter_active(),'companion':None}
  if v:
   hidden=v.get_editor_property('hidden');distance=v.get_actor_location().distance(p.get_actor_location());state['max_distance']=max(distance,state['max_distance']);row.update(companion=v.get_actor_location().to_tuple(),distance=distance,hidden=hidden,recall=m.recalling,mesh=v.mesh.get_skeletal_mesh_asset().get_path_name());assert all(x.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION for x in v.get_components_by_class(unreal.PrimitiveComponent))
   if e.is_encounter_active():assert hidden;state['battle_hidden_samples']+=1
   elif not hidden and any(b.is_viewer_in_relocated_room(v.get_actor_location()+unreal.Vector(0,0,30))for b in buildings):
    assert not v.mesh.cast_shadow and v.mesh.get_editor_property('lighting_channels').channel1,{'player':row['player'],'companion':row['companion'],'player_shadow':p.get_component_by_class(unreal.SkeletalMeshComponent).cast_shadow,'companion_shadow':v.mesh.cast_shadow};state['interior_shadowless_samples']+=1
  log.write(json.dumps(row)+'\n');state['samples']+=1
 except Exception:
  import traceback
  state['issues'].append(traceback.format_exc());log.close();(O/'CompanionResult.json').write_text(json.dumps(state,indent=2));unreal.unregister_slate_post_tick_callback(unreal._starter_companion_observer)
unreal._starter_companion_observer=unreal.register_slate_post_tick_callback(tick)
