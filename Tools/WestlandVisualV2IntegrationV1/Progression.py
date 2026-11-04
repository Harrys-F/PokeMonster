"""Existing PIE progression/evolution services on Westland, isolated fixtures only. No species-rule edits."""
import unreal,json,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualV2IntegrationV1';O=D/'PIEProgression01';O.mkdir(exist_ok=False)
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W and 'Dev_WestlandRegion'in W.get_name();assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D)
P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
def sub(t,o=GI):return next(x for x in unreal.ObjectIterator(t)if x.get_outer()==o)
E=sub(unreal.PokeMonsterEncounterSubsystem);S=sub(unreal.PokeMonsterSaveSubsystem);assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_WestlandProgressionV1')
old_auto=unreal.SystemLibrary.get_console_variable_int_value('pm.Evolution.Auto');route=[];s={'index':0,'at':time.monotonic(),'start':time.monotonic(),'busy':False};r={'checks':[],'source':'Existing pm.EvolutionReview.Party/XP and regular UMG; own explicitly isolated PIE state only','physical_controller':False};state={}
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def ui():return PC.get_evolution_widget()
def phase(n):return bool(ui())and ui().get_phase()==n
def party():return list(E.get_player_party())
def snap():return[x.export_text()for x in party()]
def same(a,b):
 assert a.instance_id.to_string()==b.instance_id.to_string()
 for k in ['Level','Experience','Status','StatusTurns']:assert str(a.get_editor_property(k))==str(b.get_editor_property(k)),k
 for k in ['MoveSlots','LearnedMoves']:assert[x.export_text()for x in a.get_editor_property(k)]==[x.export_text()for x in b.get_editor_property(k)],k
 assert a.calculated_stats.max_hp-a.current_hp==b.calculated_stats.max_hp-b.current_hp
 return True
def add(n,f,delay=.5):route.append((n,f,delay))
def check(n,f,delay=.5):
 def run():assert f(),n;r['checks'].append(n)
 add(n,run,delay)
def shot(n):cmd('Shot SHOWUI filename="'+str(O/(n+'.png'))+'" -nosuffix')
for source,level,target in [('Glumanda',15,'Glutexo'),('Glutexo',35,'Glurak')]:
 add('hold auto',lambda:cmd('pm.Evolution.Auto 0'))
 add('existing '+source+' fixture',lambda source=source,level=level:cmd('pm.EvolutionReview.Party '+source+' '+str(level)))
 add('auto on',lambda:cmd('pm.Evolution.Auto 1'),1)
 check(source+' no early evolution',lambda:not ui())
 add('normal XP level boundary',lambda:cmd('pm.EvolutionReview.XP next'),1.3)
 check(source+' correct normal offer',lambda target=target:phase('offer')and str(party()[0].pending_evolution_target.primary_asset_name)==target)
 add('snapshot source',lambda:state.update(before=party()))
 add('begin regular sequence',lambda:ui().confirm())
 check('sequence remains cancellable',lambda:phase('transform')and ui().can_cancel_evolution(),1.5)
 add('cancel sequence',lambda:ui().cancel(),.7)
 check(source+' cancellation preserves original individual/AP/HP and reserve',lambda:phase('cancelled')and same(state['before'][0],party()[0])and party()[0].species==state['before'][0].species and party()[1].export_text()==state['before'][1].export_text())
 add('ack cancellation',lambda:ui().confirm(),1)
 check('no immediate duplicate',lambda:not ui())
 add('later real level',lambda:cmd('pm.EvolutionReview.XP next'),1.3)
 check('later retry offered',lambda:phase('offer'))
 add('snapshot retry',lambda:state.update(retry=party()))
 add('confirm normal evolution',lambda:ui().confirm())
 check(source+' to '+target+' complete with independent reserve unchanged',lambda target=target:phase('complete')and str(party()[0].species.get_internal_id())==target and same(state['retry'][0],party()[0])and party()[1].export_text()==state['retry'][1].export_text(),8.8)
 add('full reveal',lambda target=target:shot('Westland_'+target+'_Enthuellung'),1)
 add('ack success',lambda:ui().confirm(),.7)
 add('existing learning offer if present',lambda:ui().cancel()if phase('learning')else None,1)
 check('companion uses evolved model',lambda:not ui()and sub(unreal.PokeMonsterCreatureCompanionSubsystem,W).get_visual().mesh.get_skeletal_mesh_asset()==party()[0].species.get_visuals().presentation.mesh)
 def save_load():
  PC.toggle_main_menu();state['saved']=snap();assert S.save_current_game();assert S.load_game()
 add('isolated evolved save/load',save_load,2)
 check('evolved individuals/AP restored',lambda:not S.is_load_in_progress()and snap()==state['saved'],2)
 add('close menu',lambda:PC.close_menu())
def finish(error=None):
 cmd('pm.Evolution.Auto '+str(old_auto));r.update(passed=error is None,error=error,seconds=time.monotonic()-s['start']);(O/'Result.json').write_text(json.dumps(r,indent=2));unreal.unregister_slate_post_tick_callback(unreal._westland_progression)
def tick(dt):
 if s['busy']:return
 s['busy']=True
 try:
  assert time.monotonic()-s['start']<180
  if s['index']==len(route):finish();return
  n,f,delay=route[s['index']]
  if time.monotonic()-s['at']<delay:return
  f();s.update(index=s['index']+1,at=time.monotonic());(O/'Progress.json').write_text(json.dumps({'step':n,'index':s['index'],'total':len(route)}))
 except Exception:finish(traceback.format_exc())
 finally:s['busy']=False
unreal._westland_progression=unreal.register_slate_post_tick_callback(tick)
