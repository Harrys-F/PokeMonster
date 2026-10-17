import unreal,json,runpy,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();P=R/'Art/Characters/NPCs/Ranger/Review/V2';last=0;busy=False
assert not hasattr(unreal,'_rv2_queue')
def poll(dt):
 global last,busy
 if busy:return
 f=P/'Job.json'
 if not f.exists():return
 j=json.loads(f.read_text())
 if j['id']==last:return
 last=j['id'];busy=True
 try:
  target=(R/j['path']).resolve();assert target.is_relative_to(R/'Tools/PerformanceRangerV2');runpy.run_path(str(target),run_name='__main__');a={'id':last,'ok':True}
 except Exception:a={'id':last,'ok':False,'error':traceback.format_exc()};unreal.log_error(a['error'])
 finally:busy=False
 (P/'Ack.json').write_text(json.dumps(a,indent=2))
unreal._rv2_queue=unreal.register_slate_post_tick_callback(poll)
