"""Actual victory/KO presentation in existing ClassicBattle; one-HP runtime opponents explicitly labelled."""
import unreal,json,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/StarterPolishV2/FinalReactionsUI';O.mkdir(exist_ok=False);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w);e=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi);cases=[('Zunderlauf','Schiggy',2),('Schiggy','Bisasam',3),('Bisasam','Zunderlauf',3)];s={'case':0,'phase':'start','time':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'rows':[],'fixture':'explicit one-HP opponent QA; actual unchanged battle execution and animation playback','wall':time.monotonic()}
def cmd(t):unreal.SystemLibrary.execute_console_command(w,t,pc)
def phase(v):s.update(phase=v,time=0.)
def finish(err=None):
 cmd('pm.TAAReview.CaptureStop');unreal.unregister_slate_post_tick_callback(unreal._polish_reactions);s.update(passed=err is None,error=err);(O/'Result.json').write_text(json.dumps(s,indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['time']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<160
  own,other,slot=cases[s['case']]
  if s['phase']=='start'and s['time']>1:
   cmd('pm.StarterReview.Party '+own+' '+other);a,b=e.get_player_party();b.current_hp=1;d=unreal.PokeMonsterEncounterStartData(presentation_mode=unreal.PokeMonsterBattlePresentationMode.CLASSIC_BATTLE,encounter_id='ExplicitPolishKO_'+other,kind=unreal.PokeMonsterEncounterKind.WILD,source=unreal.PokeMonsterEncounterSource.VISIBLE_CREATURE,player_team=[a],opponent_team=[b],random_seed=3,allow_flee=True);assert e.start_encounter(d,p);phase('warm')
  elif s['phase']=='warm'and s['time']>3:
   cmd('pm.TAAReview.CaptureStart '+str(R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('PolishReactionsUI_'+own)));cmd('pm.CreatureReview.CaptureLiveUI PolishReactionsUI_'+own+'_Idle');phase('attack')
  elif s['phase']=='attack'and s['time']>.5:
   pr=e.get_presenter();assert pr.try_select_move(slot);assert pr.resolve_selection();events=[str(x.type)for x in pr.get_last_result().events];assert any('KNOCKED_OUT'in x for x in events);s['rows'].append({'winner':own,'faint':other,'events':events,'viewport':pc.get_viewport_size()});phase('observe')
  elif s['phase']=='observe':
   if s['time']-s.get('last_capture',-1)>.18:
    cmd('pm.CreatureReview.CaptureLiveUI PolishReactionsUI_'+other+'_'+str(s.get('frame',0)).zfill(3));s['last_capture']=s['time'];s['frame']=s.get('frame',0)+1
   if not e.is_encounter_active()and not p.is_overworld_input_locked():assert e.get_last_result().outcome==unreal.PokeMonsterEncounterOutcome.VICTORY;cmd('pm.TAAReview.CaptureStop');phase('gap')
  elif s['phase']=='gap'and s['time']>2:
   s['case']+=1;s['shot']=False;s['frame']=0;s['last_capture']=-1
   if s['case']==len(cases):finish();return
   phase('start')
 except Exception:
  import traceback
  finish(traceback.format_exc())
unreal._polish_reactions=unreal.register_slate_post_tick_callback(tick)
