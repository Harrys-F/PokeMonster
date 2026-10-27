"""Real OpenLevel round trip: one clock, no lighting controller outside VisualV2."""
import unreal,json,time,traceback,gc
from pathlib import Path
gc.collect();R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/GraphicsVariantC/Travel01';O.mkdir(exist_ok=False);Editor=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=Editor.get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);Clock=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterWorldClock)if x.get_outer()==GI)
Encounter=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==GI);assert not Encounter.is_encounter_active()
# Existing developer fixture; the GPU runner already selected an isolated QA slot.
unreal.SystemLibrary.execute_console_command(W,'pm.EvolutionReview.Party Zunderlauf 15');expected_team=[x.export_text()for x in Encounter.get_player_party()];assert len(expected_team)==2 and 'DA_Zunderlauf'in expected_team[0];del Encounter
unreal.SystemLibrary.execute_console_command(W,'pm.WorldClock pause');unreal.SystemLibrary.execute_console_command(W,'pm.WorldClock set 11 22 0');expected=Clock.get_time().export_text();unreal.GameplayStatics.get_player_pawn(W,0).set_overworld_input_locked(True);del W
s={'stage':0,'wall':time.monotonic(),'stable':None};result={'checks':[],'maps':[],'clock':expected,'initial_party':expected_team,'fixture':'Existing pm.EvolutionReview.Party Zunderlauf 15, real models, RAM-only isolated QA state'}
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._daynight_travel);result.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(result,indent=2))
 for n in ['GI','Clock','Editor']:globals().pop(n,None)
def tick(dt):
 try:
  assert time.monotonic()-s['wall']<150,'Travel timeout';world=Editor.get_game_world()
  if not world:return
  assert unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage')==75,'Travel lost graphics profile C'
  if s['stage']==3:
   if time.monotonic()-s['stable']<1:return
   GI2=unreal.GameplayStatics.get_game_instance(world);encounter=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==GI2);companion=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==world);pawn=unreal.GameplayStatics.get_player_pawn(world,0);copies=unreal.GameplayStatics.get_all_actors_with_tag(world,'CreaturePartyCompanion')
   assert not encounter.is_encounter_active()and not pawn.is_overworld_input_locked()and not Clock.is_clock_paused()
   assert[x.export_text()for x in encounter.get_player_party()]==expected_team,'Party identity/HP/PP changed during map travel'
   assert len(copies)==1 and copies[0]==companion.get_visual()and not copies[0].get_editor_property('bHidden')
   assert not companion.get_movement().activities_enabled and not companion.get_movement().rhythm_enabled
   wild=[a for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.PokeMonsterVisibleWildCreatureActor)if a.overworld_movement.activities_enabled];assert len(wild)==8 and all(a.overworld_movement.rhythm_enabled for a in wild)
   result['checks'].append('One visible companion outside wild rhythms; eight configured wild instances, clock and player control active after return')
   (O.parent/'Return01.json').write_text(json.dumps({'passed':True,'companions':len(copies),'wild_instances':len(wild),'safe_observer_point':[-300,2100,50.15],'no_forced_wild_state':True},indent=2));finish();return
  if s['stage']==0:s['stage']=1;unreal.GameplayStatics.open_level(world,'/Game/Maps/Dev_TestMap');return
  target='Dev_TestMap'if s['stage']==1 else'Dev_TestMap_VisualV2'
  if not world.get_name().endswith(target)or not unreal.GameplayStatics.get_player_pawn(world,0):return
  unreal.GameplayStatics.get_player_pawn(world,0).set_overworld_input_locked(True)
  if s['stable']is None:s['stable']=time.monotonic();return
  if time.monotonic()-s['stable']<2:return
  assert unreal.GameplayStatics.get_game_instance(world)==GI and Clock.get_time().export_text()==expected and Clock.is_clock_paused()
  cycle=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterDayNightSubsystem)if x.get_outer()==world)
  ownsky=[a for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.StaticMeshActor)if a.get_name()=='VisualV2_DayNightSky']
  if s['stage']==1:
   assert not cycle.is_cycle_enabled()and not ownsky;result['checks'].append('Other existing map has neither active cycle nor added sky; exact world clock preserved')
   result['maps'].append(world.get_name());s.update(stage=2,stable=None);unreal.GameplayStatics.open_level(world,'/Game/Maps/Dev_TestMap_VisualV2');return
  assert all(not a.overworld_movement.activities_enabled or a.overworld_movement.rhythm_enabled for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.PokeMonsterVisibleWildCreatureActor))
  assert cycle.is_cycle_enabled()and cycle.is_sky_ready()and len(ownsky)==1 and cycle.get_lighting_sample().stars>.99
  result['maps'].append(world.get_name());result['checks'].append('Return to VisualV2 immediately restores night lighting from unchanged shared clock')
  pawn=unreal.GameplayStatics.get_player_pawn(world,0);pawn.set_actor_location(unreal.Vector(-300,2100,50.15),False,True);pawn.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
  unreal.SystemLibrary.execute_console_command(world,'pm.WorldClock reset');assert not Clock.is_clock_paused();pawn.set_overworld_input_locked(False);result['checks'].append('Clock resumes after loading and normal player control restored');s.update(stage=3,stable=time.monotonic())
 except Exception:finish(traceback.format_exc())
unreal._daynight_travel=unreal.register_slate_post_tick_callback(tick)
