"""Isolated idle capture without screenshot/foot scripting; runtime-only visibility A/B."""
import unreal,json,time,statistics
from pathlib import Path
R=Path(unreal.Paths.project_dir());O=R/'Saved/WestlandAssetLibrary';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and 'Dev_WestlandAssetLibrary' in w.get_name();assert not hasattr(unreal,'_wla_walk')
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);mode=json.loads((O/'PerformanceJob.json').read_text())['mode'];actors=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor);hidden={a:False for a in actors if a.get_actor_label().startswith(('Library_','Instancing_'))}
if mode.startswith('Empty'):
 for a in hidden:a.set_actor_hidden_in_game(True)
for cmd in ['t.MaxFPS 0','r.VSync 0','r.GPUCsvStatsEnabled 1','sg.ViewDistanceQuality 1','sg.AntiAliasingQuality 1','sg.ShadowQuality 1','sg.GlobalIlluminationQuality 1','sg.ReflectionQuality 1','sg.PostProcessQuality 1','sg.TextureQuality 1','sg.EffectsQuality 1','sg.FoliageQuality 1','r.ScreenPercentage 75']:unreal.SystemLibrary.execute_console_command(w,cmd)
start=time.monotonic();last=start;frames=[];csv_started=False

def tick(dt):
 global last,csv_started
 now=time.monotonic()
 if now-start<5:last=now;return
 if not csv_started:
  for cmd in ['csvprofile startfile=WLA_'+mode+'PIE_Idle','csvprofile start']:unreal.SystemLibrary.execute_console_command(w,cmd)
  csv_started=True
 frames.append((now-last)*1000);last=now
 if now-start>=35:
  unreal.SystemLibrary.execute_console_command(w,'csvprofile stop');unreal.unregister_slate_post_tick_callback(unreal._wla_perf);del unreal._wla_perf
  for a,h in hidden.items():a.set_actor_hidden_in_game(h)
  data={'mode':mode,'scope':'Editor PIE idle Slate wall interval; separate CSV CPU/GPU counters','samples':len(frames),'seconds':now-start-5,'mean_fps':1000/statistics.mean(frames),'median_ms':statistics.median(frames),'p95_ms':sorted(frames)[int(len(frames)*.95)],'viewport':list(pc.get_viewport_size()),'quality':'Medium / 75%','camera_cm':p.get_component_by_class(unreal.SpringArmComponent).target_arm_length,'location_cm':list(p.get_actor_location().to_tuple()),'no_screenshots_during_capture':True};(O/('Performance_'+mode+'.json')).write_text(json.dumps(data,indent=2)+'\n');unreal.log('WLA_PERFORMANCE_DONE '+mode)
assert not hasattr(unreal,'_wla_perf');unreal._wla_perf=unreal.register_slate_post_tick_callback(tick)
