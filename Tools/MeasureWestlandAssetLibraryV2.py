"""Same-resolution PIE cost decomposition. All quality/visibility changes runtime only."""
import unreal,json,time,statistics
from pathlib import Path
R=Path(unreal.Paths.project_dir());O=R/'Saved/WestlandAssetLibraryV2';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and 'Dev_WestlandAssetLibrary' in w.get_name()
pc=unreal.GameplayStatics.get_player_controller(w,0);p=unreal.GameplayStatics.get_player_pawn(w,0);mode=json.loads((O/'PerformanceJob.json').read_text())['mode'];actors=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)
vegetation=[a for a in actors if a.get_actor_label().startswith('Instancing_') or (a.get_actor_label().startswith('Library_') and any(n in a.get_actor_label() for n in ('Oak','Birch','FruitTree','Bush','Fern','Grass','Herb','Wildflowers')))];hidden=[];shadow=[]
if mode=='NoVegetation':
 for a in vegetation:a.set_actor_hidden_in_game(True);hidden.append(a)
if mode=='NoLibraryShadows':
 for a in actors:
  if not a.get_actor_label().startswith(('Library_','Instancing_')):continue
  for c in a.get_components_by_class(unreal.PrimitiveComponent):
   shadow.append((c,c.get_editor_property('cast_shadow')));c.set_cast_shadow(False)
for cmd in ['t.MaxFPS 0','r.VSync 0','r.GPUCsvStatsEnabled 1','sg.ViewDistanceQuality 1','sg.AntiAliasingQuality 1','sg.ShadowQuality 1','sg.GlobalIlluminationQuality 1','sg.ReflectionQuality 1','sg.PostProcessQuality 1','sg.TextureQuality 1','sg.EffectsQuality 1','sg.FoliageQuality 1','r.ScreenPercentage 75']:unreal.SystemLibrary.execute_console_command(w,cmd)
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old_throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_set_viewport_realtime(False)
start=time.monotonic();last=start;frames=[];started=False
name='WLA_V2_'+mode+'_PIE'
def tick(dt):
 global last,started
 now=time.monotonic()
 if now-start<8:last=now;return
 if not started:
  unreal.SystemLibrary.execute_console_command(w,'csvprofile startfile='+name);unreal.SystemLibrary.execute_console_command(w,'csvprofile start');started=True
 frames.append((now-last)*1000);last=now
 if now-start<38:return
 unreal.SystemLibrary.execute_console_command(w,'csvprofile stop');unreal.unregister_slate_post_tick_callback(unreal._wla_perf);del unreal._wla_perf
 settings.set_editor_property('bThrottleCPUWhenNotForeground',old_throttle)
 for a in hidden:a.set_actor_hidden_in_game(False)
 for c,h in shadow:c.set_cast_shadow(h)
 data={'mode':mode,'viewport':list(pc.get_viewport_size()),'seconds':now-start-8,'mean_fps':1000/statistics.mean(frames),'median_ms':statistics.median(frames),'p95_ms':sorted(frames)[int(len(frames)*.95)],'samples':len(frames),'location_cm':list(p.get_actor_location().to_tuple()),'quality':'Medium 75%, VSync off, no FPS cap','camera_cm':p.get_component_by_class(unreal.SpringArmComponent).target_arm_length,'visibility_restored':True};(O/('Performance_'+mode+'.json')).write_text(json.dumps(data,indent=2));unreal.log('WLA_V2_PERFORMANCE_DONE '+mode)
assert not hasattr(unreal,'_wla_perf');unreal._wla_perf=unreal.register_slate_post_tick_callback(tick)
