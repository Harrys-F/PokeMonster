"""Reuse the exact same real PIE/Slate instrumentation, replace only steps before the first tick."""
import runpy
from pathlib import Path
R=Path(__file__).resolve().parents[2];n=runpy.run_path(str(R/'Tools/GlutexoEvolutionV2/ReviewEvolution.py'),run_name='__main__');g=n['tick'].__globals__;g['route'].clear()
action,check,key,cmd,snap,phase,ui,shot,fixture=[g[x]for x in ['action','check','key','cmd','snap','phase','ui','shot','fixture']];e=g['e'];pc=g['pc'];save=g['save'];B=g['B'];A=g['A'];state=g['state'];unreal=g['unreal']
def drain():
 count=0
 while phase('learning'):
  ui().cancel();count+=1;assert count<40
 state.setdefault('declined_learning_offers',[]).append(count)
def xp_to(level):
 c=e.get_player_party()[0];amount=unreal.PokeMonsterCreatureProgression.experience_for_level(c.species.get_growth_rate(),level)-c.experience;cmd('pm.EvolutionReview.XP '+str(amount))
def move():
 pr=e.get_presenter();assert pr and not pr.get_view().busy
 e.get_battle_widget().set_battle_menu(unreal.PokeMonsterBattleMenu.MOVES);cmd('pm.Input.Key '+B+' tap')
action('multi-level source fixture',lambda:fixture('Zunderlauf',15));action('award level40 cumulatively',lambda:xp_to(40));action('normal polling resumes',lambda:cmd('pm.Evolution.Auto 1'),1)
check('Multiple level learning is handled first',lambda:phase('learning'));action('decline only pending genuine offers',drain,1);action('wait for first development',lambda:None,1)
check('Level40 offers middle species first',lambda:phase('offer')and str(e.get_player_party()[0].pending_evolution_target.primary_asset_name)=='Glutexo'and e.get_player_party()[0].level==40)
action('capture multi identity',lambda:state.update(multi_id=snap()[0]['id']));key('B confirms middle stage',B);action('wait first complete form',lambda:None,5.8)
check('No direct Glumanda Glurak shortcut',lambda:phase('complete')and snap()[0]['species'].endswith('DA_Glutexo.DA_Glutexo')and snap()[0]['id']==state['multi_id']);action('middle stage at level40',lambda:shot('MultiMiddle'))
key('B acknowledges middle stage',B);action('second route waits for its own confirmation',lambda:None,1)
check('Second eligible stage has separate offer',lambda:phase('offer')and str(e.get_player_party()[0].pending_evolution_target.primary_asset_name)=='Glurak');key('B confirms final stage separately',B);action('wait final stage',lambda:None,5.8)
check('Multi-level final stage retains one individual',lambda:phase('complete')and snap()[0]['species'].endswith('DA_Glurak.DA_Glurak')and snap()[0]['id']==state['multi_id']and len(e.get_player_party())==2);key('B closes multi chain',B)
action('normal classic battle fixture',lambda:cmd('pm.EvolutionReview.Victory'),2)
check('Development stays closed during battle',lambda:e.is_encounter_active()and not ui());action('classic battle before XP',lambda:shot('BattleBeforeXP'));action('real attack through existing menu',move,1);action('battle and XP finish normally',lambda:None,5)
check('Normal victory offers level16 evolution after battle',lambda:not e.is_encounter_active()and phase('offer')and snap()[0]['level']==16 and e.get_last_result().outcome==unreal.PokeMonsterEncounterOutcome.VICTORY)
action('post victory offer screenshot',lambda:shot('AfterBattleVictory'));key('A declines post victory',A);key('B closes declined offer',B)
action('level100 fixture',lambda:cmd('pm.Evolution.Auto 0'));action('prepare capped source',lambda:fixture('Zunderlauf',100));action('normal polling at cap',lambda:cmd('pm.Evolution.Auto 1'),1)
check('Late eligible source can evolve at level100',lambda:phase('offer')and snap()[0]['level']==100);action('remember capped identity',lambda:state.update(capped=snap()[0]['id']));key('A cancels capped offer',A);key('B closes capped cancellation',B)
action('same-level repeat guard',lambda:None,1);check('No capped offer spam after cancellation',lambda:not ui())
action('later legitimate victory with same capped individual',lambda:cmd('pm.EvolutionReview.Victory current'),2);action('attack through unchanged classic menu',move,1);action('battle returns safely',lambda:None,5)
check('Later victory retries even at cap without changing identity',lambda:phase('offer')and snap()[0]['id']==state['capped']and snap()[0]['level']==100);key('A cancels cap retry',A);key('B closes cap retry',B)
action('suspend auto to select missing model source',lambda:cmd('pm.Evolution.Auto 0'));action('existing Bisasam fixture',lambda:cmd('pm.StarterReview.Party Bisasam'));action('reach existing unavailable target level',lambda:xp_to(16));action('resume normal offers',lambda:cmd('pm.Evolution.Auto 1'),1);action('decline pending Bisasam level offers',drain);action('allow unavailable model evaluation',lambda:None,1)
check('Missing target never substitutes a placeholder',lambda:not ui()and snap()[0]['species'].endswith('DA_Bisasam.DA_Bisasam')and snap()[0]['level']==16)
action('record missing-model source',lambda:state.update(missing=snap()));action('save reload still eligible source',g['original_save_roundtrip']);check('Missing target save remains undamaged',lambda:snap()==state['missing'])
action('stop fixture automation before cleanup',lambda:cmd('pm.Evolution.Auto 0'))
