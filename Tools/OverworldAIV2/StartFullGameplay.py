"""Existing complete route; accept a real territorial auto-start before the old manual E step."""
import unreal,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();ns=runpy.run_path(str(R/'Tools/GlumandaV11/StartGameplay.py'),run_name='__main__');original=ns['tick'];ctx=original.__globals__;unreal.unregister_slate_post_tick_callback(unreal._visualenv_foot)
def tick(dt):
 if ctx['i']<len(ctx['route']):
  kind,name,_=ctx['route'][ctx['i']]
  if ctx['enc'].is_encounter_active()and name in ['WildBranchEntry','WildApproach','WildFacing','Wild']and kind!='battle':
   ctx['seconds']+=dt;ctx['inject'](0,0);ctx['progress']({'territorial_auto_start':True,'manual_interaction_superseded':True});return
 original(dt)
unreal._visualenv_foot=unreal.register_slate_post_tick_callback(tick)
runpy.run_path(str(R/'Tools/StarterExpansionV1/ObserveCompanion.py'),run_name='__main__');runpy.run_path(str(R/'Tools/OverworldAIV2/ObserveFill.py'),run_name='__main__')
