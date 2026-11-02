"""Factor-three barrier + natural water population; camera faces away during initial spawn window.
No AI/spawn overrides: the existing off-screen admission rule remains authoritative.
"""
import unreal,json,time,math,sys,re,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualUpgradeV1';cfg=json.loads((D/'ActiveNative.json').read_text());O=D/cfg['label'];assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(O);sys.path.insert(0,str(R/'Tools'));import WestlandRegionLayout as L
W=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_WestlandRegion'and unreal.GameplayStatics.get_player_pawn(w,0));P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);M=P.get_component_by_class(unreal.CharacterMovementComponent);H=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterHabitatSubsystem)if x.get_outer()==W);start=time.monotonic();state={'phase':'settle','at':start};samples=[];checks=[];last=0
n=-145;e=L.river(n);x,y,z=L.world(e+10,n,L.height(e+10,n));P.set_actor_location(unreal.Vector(x,y,z+50.15),False,True);M.stop_movement_immediately();P.third_person_boom.set_world_rotation(unreal.Rotator(yaw=-135),False,False)
def cmd(x):unreal.SystemLibrary.execute_console_command(W,x,PC)
def finish(error=None):
 cmd('pm.Input.Key W up');cmd('pm.Input.Key LeftShift up');cmd('pm.Speed 1');fish=[a for s in samples for a in s['population']if a['species']=='Karpador'and a['water']];passed=error is None and bool(fish);(O/'Result.json').write_text(json.dumps(dict(passed=passed,error=error,checks=checks,samples=samples,natural_karpador_samples=len(fish),maximum_active=max([len(x['population'])for x in samples]or[0]),states_observed=sorted(set(a['state']for s in samples for a in s['population'])),seconds=time.monotonic()-start,no_ai_or_spawn_overrides=True),indent=2));unreal.unregister_slate_post_tick_callback(unreal._wvu_water);unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
def tick(dt):
 global last
 try:
  assert time.monotonic()-start<140
  elapsed=time.monotonic()-state['at']
  if state['phase']=='settle'and elapsed>.8:
   cmd('pm.Speed 3');cmd('pm.Input.Key W down');cmd('pm.Input.Key LeftShift down');state.update(phase='barrier',at=time.monotonic())
  elif state['phase']=='barrier':
   pe,pn=L.en(P.get_actor_location().x,P.get_actor_location().y);assert pe>L.river(pn)+3.2,'Crossed existing river barrier'
   if elapsed>3:
    cmd('pm.Input.Key W up');cmd('pm.Input.Key LeftShift up');cmd('pm.Speed 1');checks.append(dict(test='Existing river barrier blocks factor3 sprint',east_m=pe,north_m=pn,distance_from_center_m=pe-L.river(pn),reset_limit_cm_s=M.max_walk_speed));P.third_person_boom.set_world_rotation(unreal.Rotator(yaw=45),False,False);state.update(phase='observe',at=time.monotonic())
  elif state['phase']=='observe':
   if elapsed-last>=1:
    last=elapsed;rows=[]
    for a in H.population:
     if a.life_state!=unreal.PokeMonsterWildLifeState.ACTIVE:continue
     movement=a.overworld_movement;assert not movement.controlled_model_preview;body=a.get_component_by_class(unreal.CapsuleComponent);foot=a.get_actor_location()-unreal.Vector(0,0,body.get_scaled_capsule_half_height());assert movement.is_inside_habitat(foot);zone=movement.biome_habitat;rows.append(dict(species=str(a.visual_species.get_internal_id()),state=str(movement.behavior_state),speed_cm_s=movement.current_speed,water=zone.medium==unreal.PokeMonsterBiomeMedium.WATER_ONLY,zone=str(zone.zone_id),foot=foot.to_tuple()))
    assert len(rows)<=14;samples.append(dict(elapsed=elapsed,population=rows,spawned=H.spawned,retired=H.retired,rejected=H.rejected_positions,updates=H.updates,last_update_us=H.last_update_microseconds))
   if elapsed>60 and not state.get('view_fish'):
    fish=[a for a in H.population if a.life_state==unreal.PokeMonsterWildLifeState.ACTIVE and str(a.visual_species.get_internal_id())=='Karpador']
    if fish:
     target=fish[0].get_actor_location();origin=P.get_actor_location();P.third_person_boom.set_world_rotation(unreal.Rotator(yaw=math.degrees(math.atan2(target.y-origin.y,target.x-origin.x))),False,False);state['view_fish']=True
   if elapsed>75:
    cmd('Shot filename="'+str(O/'Karpador_Fluss.png')+'" -nosuffix');state.update(phase='finish',at=time.monotonic())
  elif state['phase']=='finish'and elapsed>1:
   assert(O/'Karpador_Fluss.png').is_file();finish()
 except Exception:finish(traceback.format_exc())
# Read-only simple-collision sweeps against every actual tree variant in this native world.
allactors=list(actors.values())if 'actors'in globals()else list(unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor))
for tree in allactors:
 if not tree.get_actor_label().startswith('WVU_Trees_'):continue
 component=tree.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);t=component.get_instance_transform(0,True);q=t.translation;ignored=[a for a in allactors if a!=tree]
 hit=unreal.SystemLibrary.capsule_trace_single_for_objects(W,unreal.Vector(q.x-500,q.y,q.z+150),unreal.Vector(q.x+500,q.y,q.z+150),28,48,[unreal.ObjectTypeQuery.ECC_WORLD_STATIC],False,ignored,unreal.DrawDebugTrace.NONE,True)
 assert hit,('No actual authored trunk sweep hit',tree.get_actor_label());checks.append(dict(test='Native authored trunk hull sweep',variant=tree.get_actor_label(),hit=True,trace_complex=False))
unreal._wvu_water=unreal.register_slate_post_tick_callback(tick)
