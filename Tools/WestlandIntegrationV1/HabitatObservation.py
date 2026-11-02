"""Read-only sampling of the natural population after the isolated Ufer pickup review. No spawning/AI overrides."""
import unreal,time,json,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandIntegrationV1';O=D/'HabitatObservation01';O.mkdir(exist_ok=False)
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W and 'Dev_WestlandRegion'in W.get_name();assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D)
H=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterHabitatSubsystem)if x.get_outer()==W);P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);start=time.monotonic();last=0;samples=[]
def finish(error=None):
 rows=[a for s in samples for a in s['population']];fish=[a for a in rows if a['species']=='Karpador'and a['water']];r={'passed':error is None and bool(fish),'error':error,'seconds':time.monotonic()-start,'samples':samples,'maximum_active':max((len(s['population'])for s in samples),default=0),'states_observed':sorted(set(a['state']for a in rows)),'natural_karpador_samples':len(fish),'no_ai_or_spawn_overrides':True}
 (O/'Result.json').write_text(json.dumps(r,indent=2));unreal.unregister_slate_post_tick_callback(unreal._westland_habitat_observe)
def tick(dt):
 global last
 try:
  elapsed=time.monotonic()-start
  if elapsed-last<1:return
  last=elapsed;rows=[]
  for a in H.population:
   if a.life_state!=unreal.PokeMonsterWildLifeState.ACTIVE:continue
   m=a.overworld_movement;assert not m.controlled_model_preview;body=a.get_component_by_class(unreal.CapsuleComponent);foot=a.get_actor_location()-unreal.Vector(0,0,body.get_scaled_capsule_half_height());inside=m.is_inside_habitat(foot);assert inside,(a.get_name(),'outside habitat')
   z=m.biome_habitat;rows.append({'id':str(a.encounter_id),'species':str(a.visual_species.get_internal_id()),'state':str(m.behavior_state),'speed_cm_s':m.current_speed,'zone':str(z.zone_id),'inside':inside,'foot':foot.to_tuple(),'water':z.medium==unreal.PokeMonsterBiomeMedium.WATER_ONLY})
  assert len(rows)<=14;samples.append({'elapsed':elapsed,'player':P.get_actor_location().to_tuple(),'population':rows})
  if elapsed>=35:
   unreal.SystemLibrary.execute_console_command(W,'Shot filename="'+str(O/'Flussufer.png')+'" -nosuffix',PC);finish()
 except Exception:finish(traceback.format_exc())
unreal._westland_habitat_observe=unreal.register_slate_post_tick_callback(tick)
