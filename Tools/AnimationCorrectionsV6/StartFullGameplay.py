"""Existing full walking route; pause ONLY the walk watchdog during real late wild battles."""
import unreal,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();ns=runpy.run_path(str(R/'Tools/WildEncountersV2/StartFullGameplay.py'),run_name='__main__');original=ns['tick'];ctx=ns['ctx'];unreal.unregister_slate_post_tick_callback(unreal._visualenv_foot)
def tick(dt):
 if ctx['i']<len(ctx['route']):
  kind,name,_=ctx['route'][ctx['i']]
  if kind=='walk'and any(x['name']=='NorthEast'for x in ctx['out']['steps'])and ctx['enc'].is_encounter_active():
   ctx['seconds']+=dt;ctx['stage']+=dt;ctx['stuck']=0;ctx['last']=ctx['p'].get_actor_location();ctx['inject'](0,0);return
 original(dt)
unreal._visualenv_foot=unreal.register_slate_post_tick_callback(tick)
runpy.run_path(str(R/'Tools/AnimationCorrectionsV6/HandleAmbientBattles.py'),run_name='__main__')
