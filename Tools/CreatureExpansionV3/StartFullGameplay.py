"""Existing full walking route with real additional habitat battles; no test teleports.
Canonical development Glurak/Machomei/Glumanda party is an explicit route fixture.
"""
import unreal,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve()
ns=runpy.run_path(str(R/'Tools/WildEncountersV2/StartFullGameplay.py'),run_name='__main__');original=ns['tick'];ctx=original.__globals__['ctx'];w=ctx['w'];e=ctx['enc'];p=ctx['p'];O=ctx['O'];unreal.unregister_slate_post_tick_callback(unreal._visualenv_foot)
unreal.SystemLibrary.execute_console_command(w,'pm.StarterReview.Party Glurak Machomei Zunderlauf')
ctx['out']['party_fixture']='Existing canonical development Glurak/Machomei/Zunderlauf party, no modified stats or production balance.'
state={'active':False,'time':0.,'entries':[]}
def tick(dt):
 try:
  kind,name,_=ctx['route'][ctx['i']] if ctx['i']<len(ctx['route']) else ('end','end',None)
  incidental=e.is_encounter_active() and kind not in ['battle','interact','dialog'] and name not in ['WildBranchEntry','WildApproach','WildFacing','WildContact','Wild']
  if incidental:
   ctx['inject'](0,0);ctx['sprint_input'](False);ctx['last']=p.get_actor_location();ctx['stuck']=0
   if not state['active']:
    state.update(active=True,time=0.);state['entries'].append({'step':name,'player':p.get_actor_location().to_tuple(),'opponent':str(e.get_presenter().get_view().opponent.name)})
   state['time']+=dt;assert state['time']<140,'Additional battle timeout';pr=e.get_presenter();v=pr.get_view()
   if not v.busy and not v.finished:
    if v.must_switch:assert pr.try_select_switch(next(i for i,m in enumerate(v.player_team)if m.can_switch))
    else:assert pr.try_select_flee()
    assert pr.resolve_selection()
   return
  if state['active']:
   state['entries'][-1]['result']=str(e.get_last_result().outcome);assert e.get_last_result().outcome in [unreal.PokeMonsterEncounterOutcome.VICTORY,unreal.PokeMonsterEncounterOutcome.FLED];state['active']=False;ctx['out']['additional_habitat_battles']=state['entries'];ctx['stuck']=0
  original(dt)
 except Exception:
  import traceback
  ctx['finish'](traceback.format_exc())
unreal._visualenv_foot=unreal.register_slate_post_tick_callback(tick)
