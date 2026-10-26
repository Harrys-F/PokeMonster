"""Real VisualV2 PIE/Slate evolution review. Explicit runtime party/XP fixtures, no map writes."""
import unreal,json,time,hashlib,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/GlutexoEvolutionV2'/json.loads((R/'Saved/GlutexoEvolutionV2/EvolutionReviewRequest.json').read_text())['label'];assert D.is_dir()
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w)
def sub(cls):return next(x for x in unreal.ObjectIterator(cls)if x.get_outer()==gi)
e=sub(unreal.PokeMonsterEncounterSubsystem);save=sub(unreal.PokeMonsterSaveSubsystem)
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';backend=unreal.SystemLibrary.get_console_variable_int_value('Slate.MacControllerPreferGCImpl');B='Gamepad_FaceButton_Right'if backend else'Gamepad_FaceButton_Bottom';A='Gamepad_FaceButton_Bottom'if backend else'Gamepad_FaceButton_Right'
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
route=[];state={};result={'technical_runtime_fixture':True,'physical_controller_test':False,'checks':[],'shots':[],'frames':[]};s={'i':0,'t':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'frame':0,'frame_t':0.}
def cmd(v):unreal.SystemLibrary.execute_console_command(w,v,pc)
cmd('pm.Evolution.Auto 0');cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100')
for actor in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor):actor.set_actor_enable_collision(False);actor.overworld_movement.set_movement_paused(True)
for actor in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterWildEncounterZone):actor.set_actor_enable_collision(False)
cmd('pm.TestGround.Go 11')
def snap():
 def moves(c,f):return [dict(move=x.get_editor_property('move').get_path_name()if x.get_editor_property('move')else None,pp=x.get_editor_property('current_pp'),max=x.get_editor_property('max_pp'))for x in c.get_editor_property(f)]
 return [dict(id=c.instance_id.to_string(),species=c.species.get_path_name(),level=c.level,xp=c.experience,hp=c.current_hp,max=c.calculated_stats.max_hp,status=str(c.status),active=moves(c,'move_slots'),known=moves(c,'learned_moves'),pending=[m.get_path_name()for m in c.pending_moves])for c in e.get_player_party()]
def ui():return pc.get_evolution_widget()
def phase(v):return ui()and ui().get_phase()==v
Label=D.name

def shot(name):
 capture='Evolution'+Label+name;cmd('pm.CreatureReview.CaptureLiveUI '+capture);path=R/'Saved/GlumandaV11/LiveUI'/capture/'ActualSlateViewport.png';assert path.exists();result['shots'].append(str(path));cmd('pm.EvolutionReview.Capture '+capture);qhd=R/'Saved/GlutexoEvolutionV2/QHDCaptures'/(capture+'.png');
 if ui():assert qhd.exists();result.setdefault('qhd_native_umg_renders',[]).append(str(qhd))
def action(name,fn,delay=.5):route.append((name,fn,delay))
def check(name,fn):
 def test():assert fn(),name;result['checks'].append(name)
 action(name,test)
def key(name,k):action(name+' down',lambda:cmd('pm.Input.Key '+k+' down'),.15);action(name+' up',lambda:cmd('pm.Input.Key '+k+' up'),.3)
def equivalent(before,after):return all(before[k]==after[k]for k in ['id','level','xp','status','active','known'])and before['max']-before['hp']==after['max']-after['hp']
def fixture(name,level):cmd('pm.EvolutionReview.Party '+name+' '+str(level))
def original_save_roundtrip():
 if ui():pc.close_evolution_presentation()
 assert save.save_current_game()and save.load_game()
action('level15 fixture',lambda:fixture('Zunderlauf',15));action('normal safe-state polling',lambda:cmd('pm.Evolution.Auto 1'),1.5)
check('No evolution below level 16',lambda:not ui()and snap()[0]['level']==15)
action('award exact level16 XP',lambda:cmd('pm.EvolutionReview.XP next'),2)
check('Level16 offers exactly Glutexo',lambda:phase('offer')and str(e.get_player_party()[0].pending_evolution_target.primary_asset_name)=='Glutexo')
action('record original and reserve',lambda:state.update(before=snap()));action('pending offer screenshot',lambda:shot('Offer16'))
action('save and reload pending offer',original_save_roundtrip)
check('Pending offer survives reload without duplicate individual',lambda:phase('offer')and snap()==state['before']and len(e.get_player_party())==2)
key('B starts reversible sequence',B);action('show changed visual before cancellation',lambda:None,3.2)
check('Presentation is running, species not yet committed',lambda:phase('transform')and snap()==state['before']);action('mid sequence screenshot',lambda:shot('BeforeCancel'))
key('A cancels after preview morph',A)
check('Cancelled evolution restores original data',lambda:phase('cancelled')and snap()==state['before']);action('cancelled screenshot',lambda:shot('Cancelled'))
key('B closes cancellation',B);action('wait same-level guard',lambda:None,1.5)
check('No immediate duplicate offer at same level',lambda:not ui()and snap()==state['before'])
action('later level17 retry',lambda:cmd('pm.EvolutionReview.XP next'),2);check('Later level retries development',lambda:phase('offer')and snap()[0]['level']==17)
action('snapshot before confirmed evolution',lambda:state.update(retry=snap()));key('B confirms Glutexo',B);action('wait full Glutexo sequence',lambda:None,5.8)
check('Glutexo committed once with same identity XP PP and reserve',lambda:phase('complete')and snap()[0]['species'].endswith('DA_Glutexo.DA_Glutexo')and equivalent(state['retry'][0],snap()[0])and snap()[1]==state['retry'][1])
action('Glutexo success screenshot',lambda:shot('GlutexoComplete'));action('reload evolved state',original_save_roundtrip)
check('Evolved historical growth save reload exact',lambda:equivalent(state['retry'][0],snap()[0])and snap()[0]['species'].endswith('DA_Glutexo.DA_Glutexo'))
key('B returns to world',B);action('companion updates',lambda:None,1)
check('Menu closes and player unlocks',lambda:not ui()and not p.is_overworld_input_locked())
action('open team for evolved individual',lambda:pc.open_menu(unreal.PokeMonsterOverworldMenuSection.TEAM))
key('B selects evolved source for sorting',B);key('DPad selects reserve slot','Gamepad_DPad_Down');key('B swaps complete instances',B)
check('Evolved individual and repertoire move with its team slot',lambda:snap()[1]['id']==state['retry'][0]['id']and equivalent(state['retry'][0],snap()[1])and snap()[0]==state['retry'][1])
key('A leaves sorted team',A)
action('suspend auto presentation',lambda:cmd('pm.Evolution.Auto 0'));action('Glutexo level35 fixture',lambda:fixture('Glutexo',35));action('poll below second level',lambda:cmd('pm.Evolution.Auto 1'),1.5)
check('No Glurak below level36',lambda:not ui()and snap()[0]['level']==35)
action('reach level36',lambda:cmd('pm.EvolutionReview.XP next'),2);check('Glurak offered at level36',lambda:phase('offer')and str(e.get_player_party()[0].pending_evolution_target.primary_asset_name)=='Glurak')
action('snapshot Glutexo and independent Glurak',lambda:state.update(second=snap()));key('Enter confirms keyboard evolution','Enter');action('wait Glurak sequence',lambda:None,5.8)
check('Glurak has same individual and unchanged other Glurak',lambda:phase('complete')and snap()[0]['species'].endswith('DA_Glurak.DA_Glurak')and equivalent(state['second'][0],snap()[0])and snap()[1]==state['second'][1]);action('Glurak screenshot',lambda:shot('GlurakComplete'))
key('B opens evolution-time learning',B);check('Level36 WingAttack offered',lambda:phase('learning')and len(snap()[0]['pending'])==1 and 'WingAttack'in snap()[0]['pending'][0]);action('learning screenshot',lambda:shot('WingAttackOffer'))
key('DPad selects replacement','Gamepad_DPad_Right');key('B learns into selected slot',B);action('allow learning close',lambda:None,1)
check('Four moves, previous learned PP retained',lambda:not ui()and len(snap()[0]['active'])==4 and all(m in snap()[0]['known']for m in state['second'][0]['known'])and any('WingAttack'in str(m['move'])for m in snap()[0]['active']))
action('record final state',lambda:state.update(final=snap()));action('save reload after learning',original_save_roundtrip);check('Post evolution repertoire saves exactly',lambda:snap()==state['final'])
action('open ordinary team menu',lambda:pc.open_menu(unreal.PokeMonsterOverworldMenuSection.TEAM),1);action('team screenshot',lambda:shot('TeamAfter'));key('A returns from ordinary menu',A)
check('Original controller menu input remains functional',lambda:not pc.is_menu_open()and not p.is_overworld_input_locked())
action('disable automatic fixtures after test',lambda:cmd('pm.Evolution.Auto 0'))

def finish(error=None):
 cmd('pm.Evolution.Auto 0')
 if phase('offer')or phase('transform'):ui().cancel()
 unreal.unregister_slate_post_tick_callback(unreal._evolution_review);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle)
 result.update(passed=error is None,error=error,state=state,after=snap(),save_after_sha256=hashlib.sha256(slot.read_bytes()).hexdigest());(D/'Result.json').write_text(json.dumps(result,indent=2));unreal.log('EVOLUTION_V2_REVIEW_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['t']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<240
  if ui()and ui().get_phase()=='transform'and now-s['frame_t']>.18:
   s['frame_t']=now;s['frame']+=1;capture='Evolution'+Label+'Frame'+str(s['frame']).zfill(4);cmd('pm.CreatureReview.CaptureLiveUI '+capture);path=R/'Saved/GlumandaV11/LiveUI'/capture/'ActualSlateViewport.png';result['frames'].append({'time':now,'path':str(path),'phase':ui().get_phase(),'creature':str(e.get_player_party()[0].species)})
  if s['i']<len(route)and s['t']>=route[s['i']][2]:
   name,fn,delay=route[s['i']];fn();s['i']+=1;s['t']=0.;(D/'Progress.json').write_text(json.dumps({'completed':s['i'],'total':len(route),'last':name}))
  if s['i']==len(route):finish()
 except Exception:finish(traceback.format_exc())
unreal._evolution_review=unreal.register_slate_post_tick_callback(tick)
