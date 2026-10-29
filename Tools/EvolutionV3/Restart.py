"""Cross-process save/load of the evolved isolated QA team; never canonical user storage."""
import unreal,time,json,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/EvolutionV3';q=json.loads((D/'Active.json').read_text());O=D/q['label'];start=time.monotonic();stage='init';at=start;W=PC=None;r={'cases':[]}
def finish(error=None):
 r.update(passed=error is None,error=error,seconds=time.monotonic()-start);(O/'Result.json').write_text(json.dumps(r,indent=2));unreal.unregister_slate_post_tick_callback(unreal._evo_v3_restart)
 if W:unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
def tick(dt):
 global W,PC,E,I,C,S,P,stage,at
 try:
  now=time.monotonic();assert now-start<100
  if stage=='init':
   if now-start<12:return
   worlds=[w for w in unreal.ObjectIterator(unreal.World)if w.get_name().endswith('Dev_TestMap_VisualV2')and unreal.GameplayStatics.get_player_pawn(w,0)]
   if not worlds:return
   W=worlds[0];PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
   def sub(t):return next(x for x in unreal.ObjectIterator(t)if x.get_outer()==GI)
   E=sub(unreal.PokeMonsterEncounterSubsystem);S=sub(unreal.PokeMonsterSaveSubsystem);I=sub(unreal.PokeMonsterInventorySubsystem);C=sub(unreal.PokeMonsterWorldClock)
   assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D)
   unreal.SystemLibrary.execute_console_command(W,'pm.Evolution.Auto 0',PC);assert S.load_game();at=now;stage='loaded';return
  if stage=='loaded':
   if S.is_load_in_progress()or now-at<.6:return
   assert PC.open_menu(unreal.PokeMonsterOverworldMenuSection.MAIN)
   team=[x.export_text()for x in E.get_player_party()];item=unreal.load_asset('/Game/Data/Items/DA_TestEvolutionItem');quantity=I.get_quantity(item)
   if q['restart']=='write':
    old=json.loads((D/q.get('source_result','NativeEvolution04/Result.json')).read_text());assert team==old['final_party']and quantity==2
    unreal.SystemLibrary.execute_console_command(W,'setnopec '+C.get_path_name()+' Time (Day=4,SecondsOfDay=60120)',PC)
    assert C.get_day()==4 and C.get_hour()==16 and C.get_minute()==42
    assert S.save_current_game()
    expected={'party':team,'stock':quantity,'clock':C.get_time().export_text(),'position':P.get_actor_location().to_tuple()}
    (D/'RestartExpected.json').write_text(json.dumps(expected,indent=2));r['cases'].append({'step':'Reloaded evolved team, wrote schema11 at paused day4 16:42','expected':expected})
   else:
    expected=json.loads((D/'RestartExpected.json').read_text());assert team==expected['party']and quantity==expected['stock']
    assert C.get_day()==4 and C.get_hour()==16 and C.get_minute()==42
    assert sum((a-b)**2 for a,b in zip(P.get_actor_location().to_tuple(),expected['position']))<.01
    comp=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==W)
    assert comp.get_visual()and comp.get_visual().mesh.get_skeletal_mesh_asset()==E.get_player_party()[0].species.get_visuals().presentation.mesh
    r['cases'].append({'step':'Fresh process restored evolved IDs/XP/HP/status/repertoire/AP/item count, world time, position and companion','actual_clock':C.get_time().export_text()})
   r['graphics']={n:unreal.SystemLibrary.get_console_variable_float_value(n)for n in ['r.Lumen.HardwareRayTracing','r.Lumen.FinalGatherMethod','r.ScreenPercentage','r.TemporalAA.Upsampling']};assert list(r['graphics'].values())==[0.,0.,75.,1.];finish()
 except Exception:finish(traceback.format_exc())
unreal._evo_v3_restart=unreal.register_slate_post_tick_callback(tick)
