"""Temporary settings-object study after confirmed overly dark first night; no asset writes."""
import unreal,json,time,traceback,gc
from pathlib import Path
gc.collect();R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/DayNightV1';O=D/'NightStudy04';O.mkdir(exist_ok=False);W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0);S=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterDayNightSubsystem)if x.get_outer()==W);C=unreal.get_default_object(unreal.load_class(None,'/Script/PokeMonster.PokeMonsterDayNightSettings'));old=(C.get_editor_property('MoonIntensity'),C.get_editor_property('NightFillIntensity'))
C.set_editor_property('MoonIntensity',.5);C.set_editor_property('NightFillIntensity',.9)
unreal.SystemLibrary.execute_console_command(W,'pm.WorldClock set 2 22 0',PC);S.refresh_lighting()
rows=json.loads((D/'Comparison01/Result.json').read_text())['rows'];points=[('Wiese',next(r['player']for r in rows if r['variant']=='Cycle'and r['view']=='Time2200')),('Baumkrone',next(r['player']for r in rows if r['view']=='NightCanopy')),('NPC',next(r['player']for r in rows if r['view']=='NightNPC'))];s={'i':0,'last':0,'placed':False};result={'parameters':{'moon':.5,'night_fill':.9},'shots':[]}
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._night_study);C.set_editor_property('MoonIntensity',old[0]);C.set_editor_property('NightFillIntensity',old[1]);S.refresh_lighting();result.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(result,indent=2))
def tick(dt):
 try:
  n,pos=points[s['i']]
  if not s['placed']:
   P.set_actor_location(unreal.Vector(*pos),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();s.update(placed=True,last=time.monotonic());return
  if time.monotonic()-s['last']<3:return
  unreal.SystemLibrary.execute_console_command(W,'HighResShot 2560x1440 filename="'+str(O/(n+'.png'))+'"',PC);result['shots'].append({'view':n,'position':P.get_actor_location().to_tuple(),'sample':S.get_lighting_sample().export_text()});s.update(i=s['i']+1,placed=False)
  if s['i']==len(points):finish()
 except Exception:finish(traceback.format_exc())
unreal._night_study=unreal.register_slate_post_tick_callback(tick)
