"""Actual existing UMG/service acceptance in an explicitly isolated EvolutionV3 UserDir.
The item fixture is technical only; no new production stone evolution is authored.
"""
import unreal,time,json,traceback,os
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/EvolutionV3';q=json.loads((D/'Active.json').read_text());O=D/q['label'];s={'stage':'init','start':time.monotonic(),'i':0,'at':time.monotonic()};r={'checks':[],'cases':[],'technical_item_fixture':True,'physical_controller_test':False};route=[];state={};W=PC=E=S=I=None

def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def party():return list(E.get_player_party())
def snapshot():return [x.export_text()for x in party()]
def ui():return PC.get_evolution_widget()
def phase(p):return bool(ui())and ui().get_phase()==p
def shot(name):cmd('Shot filename="'+str(O/(name+'.png'))+'" -nosuffix -showui')
def add(name,fn,delay=.4):route.append((name,fn,delay))
def check(name,fn,delay=.4):
 def run():assert fn(),name;r['checks'].append(name)
 add(name,run,delay)
def fixture(name,level):cmd('pm.EvolutionReview.Party '+name+' '+str(level))
def equivalent(before,after):
 assert before.instance_id.to_string()==after.instance_id.to_string(),(before.instance_id.to_string(),after.instance_id.to_string())
 for k in ['Level','Experience','Status','StatusTurns']:
  assert str(before.get_editor_property(k))==str(after.get_editor_property(k)),k
 for k in ['MoveSlots','LearnedMoves']:assert [x.export_text()for x in before.get_editor_property(k)]==[x.export_text()for x in after.get_editor_property(k)],k
 assert before.calculated_stats.max_hp-before.current_hp==after.calculated_stats.max_hp-after.current_hp
 return True
def roundtrip():
 assert not ui()and not PC.is_menu_open();state['saved']=snapshot();assert S.save_current_game(),S.get_last_storage_message();assert S.load_game(),S.get_last_storage_message()
def companion_ok():
 c=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==W)
 v=c.get_visual();return v is not None and v.mesh.get_skeletal_mesh_asset()==party()[0].species.get_visuals().presentation.mesh

def build():
 add('read fresh graphics defaults',lambda:r.update(graphics={n:unreal.SystemLibrary.get_console_variable_float_value(n)for n in ['r.Lumen.HardwareRayTracing','r.Lumen.FinalGatherMethod','r.ScreenPercentage','r.TemporalAA.Upsampling','r.Shadow.Virtual.SMRT.RayCountDirectional']}))
 check('Fresh profile C remains Software-Lumen/IFG TAAU 75% VSM4',lambda:list(r['graphics'].values())==[0.,0.,75.,1.,4.])
 add('pause auto for explicit fixtures',lambda:cmd('pm.Evolution.Auto 0'))
 # Each real level route uses the normal offer and unchanged presentation.
 for source,level,target in [('Glumanda',15,'Glutexo'),('Glutexo',35,'Glurak'),('Karpador',19,'Garados')]:
  def prep(source=source,level=level):fixture(source,level);state['source']=source;state['target']=target
  add('prepare '+source,prep)
  add('normal polling '+source,lambda:cmd('pm.Evolution.Auto 1'),1)
  check(source+' does not evolve early',lambda:not ui())
  add('gain exact threshold '+source,lambda:cmd('pm.EvolutionReview.XP next'),1.4)
  check(source+' offers correct target',lambda target=target:phase('offer')and str(party()[0].pending_evolution_target.primary_asset_name)==target)
  add('snapshot '+source,lambda:state.update(before=party(),before_text=snapshot()))
  add('begin reversible sequence '+source,lambda:ui().confirm())
  check(source+' preview preserves individual until commit',lambda:phase('transform')and snapshot()==state['before_text'],3.2)
  add('cancel running sequence '+source,lambda:ui().cancel(),.6)
  check(source+' A cancellation keeps species AP HP and reserve',lambda:phase('cancelled')and equivalent(state['before'][0],party()[0])and party()[0].species==state['before'][0].species and party()[1].export_text()==state['before'][1].export_text())
  add('cancel screenshot '+source,lambda source=source:shot(source+'_Cancelled'),1.2)
  add('acknowledge cancellation '+source,lambda:ui().confirm(),1)
  check(source+' no immediate duplicate offer',lambda:not ui())
  add('save cancelled state '+source,roundtrip,1.4)
  check(source+' cancelled save reload remains same species',lambda:not S.is_load_in_progress()and snapshot()==state['saved'],1.5)
  add('later actual level permits retry '+source,lambda:cmd('pm.EvolutionReview.XP next'),1.5)
  check(source+' later retry',lambda:phase('offer'))
  add('snapshot retry '+source,lambda:state.update(retry=party()))
  add('confirm existing sequence '+source,lambda:ui().confirm())
  check(source+' full reveal and successful evolution',lambda target=target:phase('complete')and str(party()[0].species.get_internal_id())==target and equivalent(state['retry'][0],party()[0])and party()[1].export_text()==state['retry'][1].export_text(),8.8)
  add('full color success '+source,lambda source=source:shot(source+'_Complete'),1.5)
  add('acknowledge complete '+source,lambda:ui().confirm(),.6)
  def learning():
   if phase('learning'):r['cases'].append({'evolution_learning':[x.get_path_name()for x in party()[0].pending_moves]});ui().cancel()
  add('normal target-level learning '+source,learning,1)
  check(source+' existing companion updates model',lambda:not ui()and companion_ok())
  add('save evolved state '+source,roundtrip,1.5)
  check(source+' evolved save restores every individual field',lambda:not S.is_load_in_progress()and snapshot()==state['saved'],1.5)
  add('hold auto between fixtures',lambda:cmd('pm.Evolution.Auto 0'))
 # Real inventory selection on a real Pokemon with a missing target: safe refusal.
 add('real Pikachu fixture',lambda:cmd('pm.StarterReview.Party Pikachu'))
 add('stock technical test stone and explicit item fixture',lambda:cmd('pm.EvolutionReview.ItemFixture on'))
 def item_init():
  state['item']=unreal.load_asset('/Game/Data/Items/DA_TestEvolutionItem');state['stock']=I.get_quantity(state['item']);state['pikachu']=snapshot()
  assert state['stock']==3
  assert E.prepare_item_evolution_offer(state['item'],0)==-1
  assert snapshot()==state['pikachu']and I.get_quantity(state['item'])==3
  r['checks'].append('Wrong technical item never mutates Pikachu or inventory')
 add('wrong source and item refused',item_init)
 add('technical item fixture party',lambda:fixture('Karpador',20))
 add('resume normal presentation',lambda:cmd('pm.Evolution.Auto 1'))
 def select_item():
  assert PC.open_menu(unreal.PokeMonsterOverworldMenuSection.INVENTORY)
  ow=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterOverworldWidget)if x.get_owning_player()==PC)
  # Select in the actual existing bag with normal input, then its existing team UI.
  entries=list(ow.get_view().inventory);index=next(j for j,row in enumerate(entries)if row.item==state['item'])
  for j in range(index):cmd('pm.Input.Key Gamepad_DPad_Down tap')
  cmd('pm.Input.Key Enter tap')
  assert ow.get_section()==unreal.PokeMonsterOverworldMenuSection.TEAM
  assert ow.select_team_slot(0)
 add('bag item then ordinary team selection',select_item,1)
 check('Item offer uses same UI and has not consumed stock',lambda:phase('offer')and I.get_quantity(state['item'])==3 and str(party()[0].pending_evolution_item_id)=='TestEvolutionItem')
 add('cancel selected item',lambda:ui().cancel())
 check('Item cancellation costs nothing',lambda:phase('cancelled')and I.get_quantity(state['item'])==3 and not str(party()[0].pending_evolution_item_id)in ['TestEvolutionItem'])
 add('close cancelled item',lambda:ui().confirm())
 add('same-level explicit item retry',select_item,1)
 check('Same-level item retry allowed',lambda:phase('offer')and I.get_quantity(state['item'])==3)
 def failed_write():
  directory=Path(unreal.Paths.project_saved_dir()).resolve()/'SaveGames';assert directory.is_relative_to(D)
  before=snapshot();target=party()[0].pending_evolution_target;mode=directory.stat().st_mode&0o777
  try:
   os.chmod(directory,0o555)
   assert not E.resolve_evolution(party()[0].instance_id,target,True),'Injected unavailable storage must refuse commit'
  finally:os.chmod(directory,mode)
  assert snapshot()==before and I.get_quantity(state['item'])==3
  r['checks'].append('Injected storage failure rolls back species, offer, AP and item stock')
 add('failed save atomic rollback',failed_write)
 def unavailable():
  before=snapshot();assert I.remove_item(state['item'],3)
  assert not E.resolve_evolution(party()[0].instance_id,party()[0].pending_evolution_target,True)
  assert snapshot()==before and I.get_quantity(state['item'])==0
  assert I.add_item(state['item'],3);r['checks'].append('Removed reserved item blocks evolution without Pokemon mutation')
 add('reserved item revalidated on acceptance',unavailable)
 def begin_ui_failure():
  directory=Path(unreal.Paths.project_saved_dir()).resolve()/'SaveGames';assert directory.is_relative_to(D)
  state['failure_dir']=directory;state['failure_mode']=directory.stat().st_mode&0o777;state['failure_before']=snapshot()
  os.chmod(directory,0o555);ui().confirm()
 add('real sequence with unavailable storage',begin_ui_failure)
 def check_ui_failure():
  os.chmod(state.pop('failure_dir'),state.pop('failure_mode'))
  assert phase('error')and snapshot()==state['failure_before']and I.get_quantity(state['item'])==3
  r['checks'].append('Actual UI commit failure preserves Pokemon, selected offer and item stock')
 add('restore storage and inspect real UI error',check_ui_failure,6.)
 add('acknowledge recoverable item error',lambda:ui().confirm())
 add('explicit item selection retries after UI error',select_item,1.)
 check('Recoverable item error does not block new explicit selection',lambda:phase('offer'))
 add('item snapshot',lambda:state.update(item_before=party()))
 add('confirm item sequence',lambda:ui().confirm())
 check('Successful item evolution consumes exactly one',lambda:phase('complete')and str(party()[0].species.get_internal_id())=='Garados'and I.get_quantity(state['item'])==2 and equivalent(state['item_before'][0],party()[0]),8.8)
 add('item success screenshot',lambda:shot('Item_TechnicalFixture_Complete'),1.5)
 add('item completion',lambda:ui().confirm())
 add('normal learning decision',lambda:ui().cancel()if phase('learning')else None,1)
 check('Repeated confirm cannot consume twice',lambda:not ui()and not E.resolve_evolution(party()[0].instance_id,state['item_before'][0].pending_evolution_target,True)and I.get_quantity(state['item'])==2)
 add('restore genuine Karpador level route',lambda:cmd('pm.EvolutionReview.ItemFixture off'))
 add('save final genuine state',roundtrip,1.5)
 check('Final evolved team and spent stock survive load',lambda:snapshot()==state['saved']and I.get_quantity(state['item'])==2 and companion_ok(),1.5)
 add('team screenshot',lambda:PC.open_menu(unreal.PokeMonsterOverworldMenuSection.TEAM),.8)
 add('capture final team',lambda:shot('TeamAfter'),1.2)
 add('close team',lambda:PC.close_menu())
 add('collect final state',lambda:r.update(final_party=snapshot(),final_stock=I.get_quantity(state['item']),final_clock=C.get_time().export_text()))

def finish(error=None):
 try:
  if 'failure_dir'in state:os.chmod(state.pop('failure_dir'),state.pop('failure_mode'))
  if PC:
   cmd('pm.Evolution.Auto 0')
   cmd('pm.EvolutionReview.ItemFixture off')
 except Exception:r['cleanup_error']=traceback.format_exc()
 r.update(passed=error is None,error=error,seconds=time.monotonic()-s['start'])
 (O/'Result.json').write_text(json.dumps(r,indent=2,ensure_ascii=False));unreal.unregister_slate_post_tick_callback(unreal._evo_v3_gameplay)
 if q.get('pie'):unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
 elif W:unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)

def tick(dt):
 global W,PC,E,S,I,C
 try:
  now=time.monotonic();assert now-s['start']<620,'Bounded evolution acceptance'
  if s['stage']=='init':
   if now-s['start']<12:return
   worlds=[w for w in unreal.ObjectIterator(unreal.World)if w.get_name().endswith('Dev_TestMap_VisualV2')and unreal.GameplayStatics.get_player_pawn(w,0)]
   if not worlds:return
   W=worlds[0];PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
   def sub(cls):return next(x for x in unreal.ObjectIterator(cls)if x.get_outer()==GI)
   E=sub(unreal.PokeMonsterEncounterSubsystem);S=sub(unreal.PokeMonsterSaveSubsystem);I=sub(unreal.PokeMonsterInventorySubsystem);C=sub(unreal.PokeMonsterWorldClock)
   assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D),'No user save storage allowed'
   cmd('pm.Evolution.Auto 0');cmd('pm.EnvPerf2.Viewport 2560 1440');build();s['stage']='actions';s['at']=now
  elif s['i']<len(route):
   name,fn,delay=route[s['i']]
   if now-s['at']<delay:return
   fn();r['cases'].append({'step':name});s['i']+=1;s['at']=now;(O/'Progress.json').write_text(json.dumps({'step':s['i'],'total':len(route),'name':name}))
  else:finish()
 except Exception:finish(traceback.format_exc())
unreal._evo_v3_gameplay=unreal.register_slate_post_tick_callback(tick)
