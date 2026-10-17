import unreal,json,runpy,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/TreeShadowProxyV1';last=json.loads((O/'Job.json').read_text()).get('id',0) if (O/'Job.json').exists() else 0;busy=False
assert not hasattr(unreal,'_treeshadow_queue')
def poll(dt):
 global last,busy
 f=O/'Job.json'
 if busy or not f.exists():return
 j=json.loads(f.read_text())
 if j['id']==last:return
 last=j['id'];busy=True
 try:
  p=(R/j['path']).resolve();assert p.is_relative_to(R/'Tools/TreeShadowProxyV1');runpy.run_path(str(p),run_name='__main__');a={'id':last,'ok':True}
 except Exception:a={'id':last,'ok':False,'error':traceback.format_exc()};unreal.log_error(a['error'])
 finally:busy=False
 (O/'Ack.json').write_text(json.dumps(a,indent=2))
unreal._treeshadow_queue=unreal.register_slate_post_tick_callback(poll)
