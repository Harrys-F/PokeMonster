"""Existing full real walking route, updated for actual territorial contact instead of E/proximity."""
import unreal,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();ns=runpy.run_path(str(R/'Tools/GlumandaV11/StartGameplay.py'),run_name='__main__');original=ns['tick'];ctx=original.__globals__;unreal.unregister_slate_post_tick_callback(unreal._visualenv_foot)
idx=next(i for i,(kind,name,arg)in enumerate(ctx['route'])if kind=='interact'and name=='Wild');ctx['route'].insert(idx,('hold','WildContact',(-1,0,1.4)))
def tick(dt):
 if ctx['i']<len(ctx['route']):
  kind,name,_=ctx['route'][ctx['i']]
  if ctx['enc'].is_encounter_active()and name in ['WildBranchEntry','WildApproach','WildFacing','WildContact','Wild']and kind!='battle':
   ctx['seconds']+=dt;ctx['inject'](0,0);ctx['progress']({'territorial_actual_contact_start':True,'manual_interaction_not_used':True});return
 original(dt)
unreal._visualenv_foot=unreal.register_slate_post_tick_callback(tick)
runpy.run_path(str(R/'Tools/StarterExpansionV1/ObserveCompanion.py'),run_name='__main__')
