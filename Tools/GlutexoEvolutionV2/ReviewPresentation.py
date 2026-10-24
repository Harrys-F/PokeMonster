"""Complete ordinary PIE evolution review, using existing RAM guard and real Slate inputs.
Technical fixture only: no authored maps, save-file copies, or user-save writes.
"""
import unreal,json,time,hashlib,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();Q=R/'Saved/ProjectRefinement/EvolutionPresentationV21';req=json.loads((Q/'Request.json').read_text());O=Q/req['label'];assert O.is_dir()
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name().endswith('Dev_TestMap_VisualV2')
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w)
def sub(c):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==gi)
e=sub(unreal.PokeMonsterEncounterSubsystem);save=sub(unreal.PokeMonsterSaveSubsystem);slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest()
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
def cmd(v):unreal.SystemLibrary.execute_console_command(w,v,pc)
def snap():
 def moves(c,f):return [(x.get_editor_property('move').get_path_name()if x.get_editor_property('move')else None,x.get_editor_property('current_pp'))for x in c.get_editor_property(f)]
 return [dict(id=c.instance_id.to_string(),species=c.species.get_path_name(),level=c.level,xp=c.experience,hp=c.current_hp,max=c.calculated_stats.max_hp,status=str(c.status),active=moves(c,'move_slots'),known=moves(c,'learned_moves'),pending=[x.get_path_name()for x in c.pending_moves])for c in e.get_player_party()]
def ui():return pc.get_evolution_widget()
def phase():return ui().get_phase()if ui()else 'overworld'
def key(k):cmd('pm.Input.Key '+k+' down');cmd('pm.Input.Key '+k+' up')
apple=unreal.SystemLibrary.get_console_variable_int_value('Slate.MacControllerPreferGCImpl')!=0
confirm_key='Gamepad_FaceButton_Right'if apple else 'Gamepad_FaceButton_Bottom'
cancel_key='Gamepad_FaceButton_Bottom'if apple else 'Gamepad_FaceButton_Right'
cmd('pm.Evolution.Auto 0')
if ui():pc.close_evolution_presentation()
assert not e.is_encounter_active();assert save.load_game();cmd('pm.Evolution.Auto 1');baseline=snap();guard_slot=next(i+1 for i,x in enumerate(baseline)if x['species'].endswith(('DA_Glutexo.DA_Glutexo','DA_Zunderlauf.DA_Zunderlauf')));cmd('pm.EvolutionTest.Start '+str(guard_slot));cmd('pm.Evolution.Auto 0')
if ui():pc.close_evolution_presentation()
cmd('pm.Evolution.Auto 0');cmd('pm.EvolutionReview.Party Zunderlauf 15');cmd('pm.EnvPerf2.Viewport 1280 720');cmd('r.ScreenPercentage 100');cmd('DisableAllScreenMessages 1');cmd('pm.Evolution.Auto 1')
original_dilation=unreal.GameplayStatics.get_global_time_dilation(w)
if req.get('slate'):unreal.GameplayStatics.set_global_time_dilation(w,.25)
s={'recording_dilation':.25 if req.get('slate')else original_dilation,'route':0,'step':'prepare','t':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'recording':False,'phases':[],'checks':[],'shots':[],'old_phase':None,'sample':-1.,'samples':[],'software_controller_backend':'Apple GC'if apple else 'legacy HID','confirm_key':confirm_key,'cancel_key':cancel_key};targets=['Glutexo','Glurak']
def shot(name):
 label='EvolutionV21_'+req['label']+'_'+name;cmd('pm.CreatureReview.CaptureLiveUI '+label);p=R/'Saved/GlumandaV11/LiveUI'/label/'ActualSlateViewport.png';assert p.is_file();s['shots'].append(str(p.relative_to(R)))
def step(n):s.update(step=n,t=0.)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._evolution_presentation_review)
 if s['recording']:cmd('pm.TAAReview.CaptureStop')
 settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);unreal.GameplayStatics.set_global_time_dilation(w,original_dilation)
 s.update(passed=error is None,error=error,save_before=before,save_after=hashlib.sha256(slot.read_bytes()).hexdigest(),actual_editor_PIE=True,fixture='Existing EvolutionReview party under existing RAM-only save guard',original_party=baseline)
 (O/'Result.json').write_text(json.dumps(s,indent=2));unreal.log('EVOLUTION_PRESENTATION_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['t']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<240;assert hashlib.sha256(slot.read_bytes()).hexdigest()==before,'User save changed: stop without overwrite'
  ph=phase()
  if ph!=s['old_phase']:s['phases'].append({'route':s['route'],'phase':ph,'game_time':now});s['old_phase']=ph
  if ui()and now-s['sample']>.1:
   v=ui().stage.opponent_visual if req.get('slate')and ph in ['reveal','complete']else ui().stage.player_visual;s['samples'].append({'route':s['route'],'time':now,'phase':ph,'scale':v.get_actor_scale3d().to_tuple(),'overlay':str(v.mesh.get_editor_property('overlay_material')),'reaction':str(v.reaction),'framing':ui().stage.framing_distance});s['sample']=now
  if ph=='reveal'and not s.get('post_commit_'+str(s['route'])):
   assert not ui().can_cancel_evolution();old=snap();key(cancel_key);assert ui()and phase()=='reveal'and snap()==old;s['post_commit_'+str(s['route'])]=True;s['checks'].append(targets[s['route']]+' A after commit cannot cancel or skip reveal')
  if s['step']=='prepare'and s['t']>1:
   if ui():pc.close_evolution_presentation()
   cmd('pm.EvolutionTest.Start 1');step('offer')
  elif s['step']=='offer':
   if ph=='learning':key('Escape');return
   if ph=='offer'and s['t']>1:
    s['before']=snap();shot(targets[s['route']]+'_Before');rec=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('EvolutionV21_'+req['label']+'_'+targets[s['route']]);assert not rec.exists();cmd('pm.TAAReview.CaptureStart "'+str(rec)+'"'+(' slate 60'if req.get('slate')else ''));s['recording']=True;step('begin')
  elif s['step']=='begin'and s['t']>1: key(confirm_key if s['route']==0 else 'Enter');step('running')
  elif s['step']=='running':
   assert ph!='error','Evolution presentation error'
   if ph=='complete':
    after=snap();a=s['before'][0];b=after[0];assert all(a[k]==b[k]for k in ['id','level','xp','status','active','known']);assert b['species'].endswith('DA_'+targets[s['route']]+'.DA_'+targets[s['route']]);assert all(x==y for x,y in zip(s['before'][1:],after[1:]));assert ui().stage.player_visual.mesh.get_editor_property('overlay_material')is None
    if req.get('slate'):
     assert ui().stage.opponent_visual.mesh.get_editor_property('overlay_material')is None;assert any(x['route']==s['route']and x['phase']=='reveal'and x['reaction'].endswith('HAPPY: 6>')for x in s['samples']), 'No actual colored Happy animation sampled'
    s['checks'].append(targets[s['route']]+' colored committed model, unchanged ID/XP/AP/repertoire/reserve');step('success')
   else:
    if 3<s['t']<3.3 and not s.get('midshot_'+str(s['route'])):shot(targets[s['route']]+'_White');s['midshot_'+str(s['route'])]=True
    assert s['t']<25,'No full reveal'
  elif s['step']=='success':
   if s['t']>.6 and not s.get('color_shot_'+str(s['route'])):shot(targets[s['route']]+'_Revealed');s['color_shot_'+str(s['route'])]=True
   if s['t']>3:key(confirm_key);step('return')
  elif s['step']=='return':
   if ph=='learning':key('Escape');return
   if ph=='overworld':s['return_position']=p.get_actor_location().to_tuple();step('gameplay')
   else:assert s['t']<15,'No return to game'
  elif s['step']=='gameplay'and s['t']>2:
   assert not pc.is_menu_open();assert save.save_current_game();state=snap();assert save.load_game();assert snap()==state;s['checks'].append(targets[s['route']]+' return to unlocked game and RAM Save/Load')
   cmd('pm.TAAReview.CaptureStop');s['recording']=False;s['route']+=1
   if s['route']==2:
    cmd('pm.EvolutionTest.End');assert not ui()and snap()==baseline;s['checks'].append('Original user team restored exactly, disk save unchanged');finish();return
   step('prepare')
  (O/'Progress.json').write_text(json.dumps({'route':s['route'],'step':s['step'],'phase':ph,'t':s['t']}))
 except Exception:finish(traceback.format_exc())
unreal._evolution_presentation_review=unreal.register_slate_post_tick_callback(tick)
