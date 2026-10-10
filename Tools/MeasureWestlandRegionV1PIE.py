"""Thirty-second PIE idle frame sample; no input or state mutation and no per-frame disk write."""
import unreal,time,json,statistics
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and 'Dev_WestlandRegion' in w.get_name();assert not hasattr(unreal,'_wr_tour') and not hasattr(unreal,'_wr_walk');start=time.monotonic();last=start;frames=[]
def tick(dt):
 global last
 now=time.monotonic();frames.append((now-last)*1000);last=now
 if now-start>=30:
  unreal.unregister_slate_post_tick_callback(unreal._wr_perf);del unreal._wr_perf;data={'mode':'PIE idle after final foot tour','seconds':now-start,'samples':len(frames),'median_ms':statistics.median(frames),'p95_ms':sorted(frames)[int(len(frames)*.95)],'mean_fps':1000/statistics.mean(frames),'quality':'Medium sg.*=1','screen_percentage':75,'viewport_px':[2331,1346],'hardware':'MacBook Air M4, 16 GB','scope':'Slate post-tick wall intervals; includes editor; not GPU-only or packaged game benchmark'};(R/'Saved/WestlandRegion/PerformanceFinal.json').write_text(json.dumps(data,indent=2));unreal.log('REGION_PERFORMANCE_DONE '+str(data['mean_fps']))
unreal._wr_perf=unreal.register_slate_post_tick_callback(tick)
