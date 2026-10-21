"""Actual UMG/Slate keyboard team selection, companion, save and battle-lock acceptance."""
import unreal,json,time,hashlib,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/CreaturePolishV4';q=json.loads((O/'TeamRequest.json').read_text());D=O/q['label'];w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w;p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w)
def sub(c):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==gi)
e=sub(unreal.PokeMonsterEncounterSubsystem);save=sub(unreal.PokeMonsterSaveSubsystem);comp=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==w)
def cmd(t):unreal.SystemLibrary.execute_console_command(w,t,pc)
def key(k):cmd('pm.BattleView2.Input '+k)
def shot(n):cmd('pm.CreatureReview.CaptureLiveUI PolishV4_'+q['label']+'_'+n)
def party():return [dict(id=c.instance_id.to_string(),species=str(c.species),level=c.level,xp=c.experience,hp=c.current_hp,status=str(c.status),moves=[dict(move=str(m.move),pp=m.current_pp,max_pp=m.max_pp)for m in c.move_slots])for c in e.get_player_party()]
s=dict(phase='prepare',time=0,last=unreal.GameplayStatics.get_time_seconds(w),wall=time.monotonic(),checks=[])
def phase(v):s.update(phase=v,time=0)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._polish_team);s.update(passed=error is None,error=error,save_after_sha256=hashlib.sha256((R/'Saved/SaveGames/PokeMonster_Dev.sav').read_bytes()).hexdigest());(D/'Result.json').write_text(json.dumps(s,indent=2));unreal.log('POLISH_TEAM_DONE '+str(error))
cmd('pm.StarterReview.Party Zunderlauf Schiggy Bisasam Pikachu Myrapla Enton')
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['time']+=now-s['last'];s['last']=now;t=s['time'];assert time.monotonic()-s['wall']<180
  if s['phase']=='prepare'and t>2:
   s['before']=party();assert len(s['before'])==6;assert pc.open_menu(unreal.PokeMonsterOverworldMenuSection.TEAM);shot('Before');phase('select')
  elif s['phase']=='select'and t>1:
   key('Focus')
   for i in range(4):key('KeyDown')
   key('Enter');shot('FifthSelected');phase('swap')
  elif s['phase']=='swap'and t>1:
   for i in range(4):key('KeyUp')
   key('Enter');expected=list(s['before']);expected[0],expected[4]=expected[4],expected[0];assert party()==expected,'Native Slate swap did not preserve exact instances';assert pc.get_overworld_widget().get_view().team[0].instance_id.to_string()==expected[0]['id'];s['after']=party();shot('After');s['checks'].append('Slate Up/Down/Enter: slot 5 to 1, all fields equal and immediate UI order');key('Escape');phase('companion')
  elif s['phase']=='companion'and t>1:
   assert not pc.is_menu_open();v=comp.get_visual();assert v and v.mesh.get_skeletal_mesh_asset()==unreal.load_asset('/Game/Data/Creatures/DA_Myrapla').visuals.presentation.mesh;assert len([a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterCreatureVisualActor)if 'CreaturePartyCompanion'in list(a.tags)])==1;s['checks'].append('Exactly one companion now uses Myrapla from slot zero');expected=party();assert save.save_current_game()and save.load_game();assert party()==expected;s['checks'].append('Actual Dev-slot save/load preserves reordered IDs, HP, XP, level, status and PP');cmd('pm.StarterReview.Party Myrapla Schiggy Bisasam');assert pc.open_menu(unreal.PokeMonsterOverworldMenuSection.TEAM);key('Focus');key('Enter')
   for i in range(5):key('KeyDown')
   before=party();key('Enter');assert party()==before[1:]+before[:1];assert len(party())==3;shot('FreeSlot');key('Escape');s['checks'].append('Free target slot 6 compacts and appends without loss or duplication');phase('battle')
  elif s['phase']=='battle'and t>1:
   cmd('pm.StarterReview.Start classic Glurak Zunderlauf');assert e.is_encounter_active();before=party();assert not e.reorder_party(e.get_player_party()[0].instance_id,1);assert party()==before;s['checks'].append('Active ClassicBattle rejects reorder without mutation');phase('flee')
  elif s['phase']=='flee':
   if not e.is_encounter_active():phase('end');return
   v=e.get_presenter().get_view()
   if t>1 and not v.busy and not v.finished:assert e.get_presenter().try_select_flee();assert e.get_presenter().resolve_selection();s['time']=0
  elif s['phase']=='end'and t>1 and not p.is_overworld_input_locked():s['checks'].append('Native battle flee returns to overworld');finish()
 except Exception:finish(traceback.format_exc())
unreal._polish_team=unreal.register_slate_post_tick_callback(tick)
