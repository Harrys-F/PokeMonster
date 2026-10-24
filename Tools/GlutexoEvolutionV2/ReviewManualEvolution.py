"""Ordinary VisualV2 PIE, real menus/sequence; no save-byte restoration or disk fixture writes."""
import unreal,json,time,hashlib,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/GlutexoEvolutionV2'/json.loads((R/'Saved/GlutexoEvolutionV2/ManualReviewRequest.json').read_text())['label'];assert D.is_dir()
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w)
def sub(cls):return next(x for x in unreal.ObjectIterator(cls)if x.get_outer()==gi)
e=sub(unreal.PokeMonsterEncounterSubsystem);save=sub(unreal.PokeMonsterSaveSubsystem)
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest()
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
def cmd(v):unreal.SystemLibrary.execute_console_command(w,v,pc)
def snap():
 def moves(c,f):return [dict(move=x.get_editor_property('move').get_path_name()if x.get_editor_property('move')else None,pp=x.get_editor_property('current_pp'))for x in c.get_editor_property(f)]
 return [dict(id=c.instance_id.to_string(),species=c.species.get_path_name(),level=c.level,xp=c.experience,hp=c.current_hp,max=c.calculated_stats.max_hp,status=str(c.status),active=moves(c,'move_slots'),known=moves(c,'learned_moves'),pending=[m.get_path_name()for m in c.pending_moves],target=str(c.pending_evolution_target.primary_asset_type.name)+':'+str(c.pending_evolution_target.primary_asset_name),last=c.last_evolution_offered_level)for c in e.get_player_party()]
def ui():return pc.get_evolution_widget()
def phase(n):return ui()and ui().get_phase()==n
def disk_unchanged():return hashlib.sha256(slot.read_bytes()).hexdigest()==before
assert save.load_game();baseline=snap();assert baseline and any(x['species'].endswith('DA_Glutexo.DA_Glutexo')or x['species'].endswith('DA_Zunderlauf.DA_Zunderlauf')for x in baseline)
index=next(i for i,x in enumerate(baseline)if x['species'].endswith('DA_Glutexo.DA_Glutexo')or x['species'].endswith('DA_Zunderlauf.DA_Zunderlauf'));user_slot=index+1
result={'normal_editor_pie':True,'technical_fixture_for_first_stage':True,'save_before_sha256':before,'checks':[],'screenshots':[]};state={};route=[];s={'i':0,'t':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic()}
def act(name,fn,delay=.5):route.append((name,fn,delay,None))
def check(name,fn):
 def f():assert fn(),name;result['checks'].append(name)
 act(name,f)
def wait(name,pred,timeout=25):route.append((name,lambda:None,timeout,pred))
def key(k):cmd('pm.Input.Key '+k+' down');cmd('pm.Input.Key '+k+' up')
def ready_offer():
 if phase('learning'):key('Escape')
 return phase('offer')
def shot(name):
 label=D.name+name;cmd('pm.CreatureReview.CaptureLiveUI '+label);p=R/'Saved/GlumandaV11/LiveUI'/label/'ActualSlateViewport.png';assert p.exists();result['screenshots'].append(str(p))
def same_individual(old,new):return all(old[k]==new[k]for k in ['id','xp','level','status','active','known'])
act('normal list',lambda:cmd('pm.EvolutionTest.List'))
act('invalid slot',lambda:cmd('pm.EvolutionTest.Start 99'));check('Invalid slot changes no team or save',lambda:snap()==baseline and disk_unchanged())
act('start selected actual team member',lambda:cmd('pm.EvolutionTest.Start '+str(user_slot)))
wait('actual member regular offer after explicit learning decisions',ready_offer)
check('Only selected actual member reaches required level',lambda:snap()[index]['id']==baseline[index]['id'] and all(snap()[i]==x for i,x in enumerate(baseline)if i!=index))
act('record before cancellation',lambda:state.update(cancel=snap()))
act('start real sequence',lambda:(state.update(sequence_start=unreal.GameplayStatics.get_time_seconds(w)),key('Enter')))
def late_cancel():
 elapsed=unreal.GameplayStatics.get_time_seconds(w)-state['sequence_start']
 assert 4.5<=elapsed<5 and phase('transform')and ui().can_cancel_evolution()and snap()==state['cancel']
 result['checks'].append('Actual late cancellation at %.3f game seconds before unchanged five-second boundary'%elapsed)
 shot('LatePreview');key('Escape')
act('cancel immediately after actual late preview',late_cancel,4.6)
check('Cancellation keeps species identity and AP',lambda:phase('cancelled')and same_individual(state['cancel'][index],snap()[index])and snap()[index]['species']==state['cancel'][index]['species'])
act('discard whole test while cancellation UI open',lambda:cmd('pm.EvolutionTest.End'))
check('End restores exact original team including pending metadata',lambda:not ui()and snap()==baseline and disk_unchanged())
# Start again on the same real individual, without adding or replacing the team.
act('repeat manual selection',lambda:cmd('pm.EvolutionTest.Start '+str(user_slot)));wait('normal second offer',ready_offer)
act('record real member before success',lambda:state.update(success=snap(),target=str(e.get_player_party()[index].pending_evolution_target.primary_asset_name)))
act('confirm full sequence',lambda:key('Enter'));wait('full normal committed presentation',lambda:phase('complete'),15)
check('Confirmed evolution preserves selected instance XP and spent AP',lambda:snap()[index]['species'].endswith('DA_'+state['target']+'.DA_'+state['target'])and same_individual(state['success'][index],snap()[index]))
act('success screenshot',lambda:shot('RealMemberSuccess'))
act('in memory save load',lambda:state.update(roundtrip=save.save_current_game()and save.load_game()))
check('Save Load reads evolved RAM state without touching disk',lambda:state['roundtrip']and snap()[index]['species'].endswith('DA_'+state['target']+'.DA_'+state['target'])and disk_unchanged())
check('Delete normal save blocked during preview',lambda:not save.delete_dev_save()and slot.exists()and disk_unchanged())
act('End also restores after success',lambda:cmd('pm.EvolutionTest.End'));check('End after success restores exact original team',lambda:snap()==baseline and not ui()and disk_unchanged())
# Establish a second-slot Glumanda fixture ONLY AFTER the same memory guard is active.
def fixture():
 cmd('pm.EvolutionTest.Start '+str(user_slot));cmd('pm.Evolution.Auto 0')
 if ui():pc.close_evolution_presentation()
 cmd('pm.EvolutionReview.Party Zunderlauf 15');fire=e.get_player_party()[0]
 assert e.reorder_party(fire.instance_id,1)
 state['fixture']=snap();cmd('pm.Evolution.Auto 1');cmd('pm.EvolutionTest.Start 2')
act('second-slot first-stage fixture under memory protection',fixture);wait('Glumanda slot2 first-stage offer',ready_offer)
check('Team slot2 selected without changing slot1',lambda:snap()[0]==state['fixture'][0]and snap()[1]['id']==state['fixture'][1]['id']and snap()[1]['level']==16)
act('record first stage',lambda:state.update(first=snap()))
act('start first stage',lambda:key('Enter'));wait('Glumanda Glutexo completed',lambda:phase('complete'),15)
check('First stage uses original selected ID and regular model',lambda:snap()[1]['species'].endswith('DA_Glutexo.DA_Glutexo')and same_individual(state['first'][1],snap()[1]))
act('first stage screenshot',lambda:shot('GlutexoComplete'))
act('continue after first stage',lambda:key('Enter'));wait('return after first stage',lambda:not ui())
act('same slot2 second stage',lambda:cmd('pm.EvolutionTest.Start 2'));wait('Glutexo slot2 regular offer',ready_offer)
check('Second stage reaches36 with no skipped individual',lambda:snap()[1]['level']==36 and snap()[1]['id']==state['first'][1]['id'])
act('record second stage',lambda:state.update(second=snap()))
act('start second stage',lambda:key('Enter'));wait('Glutexo Glurak completed',lambda:phase('complete'),15)
check('Second stage uses existing Glurak and retains independent reserve',lambda:snap()[1]['species'].endswith('DA_Glurak.DA_Glurak')and same_individual(state['second'][1],snap()[1])and snap()[0]==state['fixture'][0])
act('second stage screenshot',lambda:shot('GlurakComplete'))
act('End closes completed UI and restores all fixture changes',lambda:cmd('pm.EvolutionTest.End'));check('Fixture and both evolutions fully discarded',lambda:snap()==baseline and not ui()and disk_unchanged())
# Leave preview active: the external runner checks normal Stop/Play teardown isolation too.
act('test Stop PIE while memory-only session active',lambda:cmd('pm.EvolutionTest.Start '+str(user_slot)))
wait('leave active preview ready',ready_offer)
act('pause automatic presentation only for test teardown',lambda:cmd('pm.Evolution.Auto 0'))

def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._manual_evolution_review);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle)
 result.update(passed=error is None,error=error,original_party=baseline,after=snap(),save_after_sha256=hashlib.sha256(slot.read_bytes()).hexdigest());(D/'Result.json').write_text(json.dumps(result,indent=2));unreal.log('MANUAL_EVOLUTION_REVIEW_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['t']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<260
  assert disk_unchanged(),'Normal save changed during memory preview review: stop, do not overwrite'
  if s['i']<len(route):
   name,fn,delay,pred=route[s['i']]
   if pred:
    if not pred():assert s['t']<delay,'Timed out '+name;return
   elif s['t']<delay:return
   fn();s['i']+=1;s['t']=0.;(D/'Progress.json').write_text(json.dumps({'completed':s['i'],'total':len(route),'last':name}))
  if s['i']==len(route):finish()
 except Exception:finish(traceback.format_exc())
unreal._manual_evolution_review=unreal.register_slate_post_tick_callback(tick)
