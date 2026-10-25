"""Real normal-PIE NPC footage. Diagnostic travel, original gameplay camera; no map/save writes.
Videos use existing native framebuffer capture at half game speed, encoded with recorded game timestamps.
"""
import unreal,json,math,time,hashlib,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/NPCExpansion/PIE02';O.mkdir(exist_ok=False);W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W
P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
G=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterNPCTestGround) if x.get_outer()==W);assert len(G.specimens)==len(G.visuals)==11
D=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterDialogueSubsystem) if x.get_outer()==GI);Save=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem) if x.get_outer()==GI)
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest();assert G.set_mode('idle') and G.visit(1)
S=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=S.get_editor_property('bThrottleCPUWhenNotForeground');S.set_editor_property('bThrottleCPUWhenNotForeground',False)
old_dilation=unreal.GameplayStatics.get_global_time_dilation(W);unreal.GameplayStatics.set_global_time_dilation(W,.5)
steps=[];shots=[];rows=[];checks=[];index=0;due=0;sample=0;stage='setup';start=time.monotonic();recording=False
configs=json.loads((R/'Tools/NPCExpansion/Library.json').read_text())
def cmd(v):unreal.SystemLibrary.execute_console_command(W,v,PC)
def action(n,fn,wait=.4):steps.append((n,fn,wait))
def shot(n):
 path=O/(n+'.png');cmd('HighResShot 2560x1440 filename="'+str(path)+'"');shots.append({'name':n,'file':str(path),'player':P.get_actor_location().to_tuple(),'camera':PC.player_camera_manager.get_camera_location().to_tuple(),'camera_rotation':PC.player_camera_manager.get_camera_rotation().to_tuple(),'normal_game_camera':True})
def axis(x,y):cmd('pm.Input.Axis Gamepad_LeftX '+str(x));cmd('pm.Input.Axis Gamepad_LeftY '+str(y))
def key(k):cmd('pm.Input.Key '+k+' down');cmd('pm.Input.Key '+k+' up')
backend=unreal.SystemLibrary.get_console_variable_int_value('Slate.MacControllerPreferGCImpl');B='Gamepad_FaceButton_Right' if backend else 'Gamepad_FaceButton_Bottom'
def prepare(i):
 assert not D.is_dialogue_active();assert G.set_mode('idle') and G.visit(i+1);G.visuals[i].set_actor_rotation(unreal.Rotator(pitch=0,yaw=135,roll=0),True)
def record(i):
 global recording
 path=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('NPCLibrary_PIE02_'+configs[i]['id']);assert not path.exists();cmd('pm.TAAReview.CaptureStart "'+str(path)+'"');recording=True

def stop_record():
 global recording
 cmd('pm.TAAReview.CaptureStop');recording=False

def approach(i):
 assert G.set_mode('idle');n=G.specimens[i];pos=n.get_actor_location();# Controlled diagnostic positioning for interaction, separate from footrun below.
 P.set_actor_location(unreal.Vector(pos.x-85,pos.y+85,48.5),False,True);axis(0,1)
def challenge(i):
 axis(0,0);key(B)
def confirm_dialogue(i):
 assert D.is_dialogue_active() and D.get_active_source()==G.specimens[i],('Wrong interaction target',i)
 assert G.visuals[i].is_conversing();checks.append(configs[i]['id']+' existing B interaction and talk state')
def end_dialogue():
 key(B)
 if D.is_dialogue_active():key(B)
 assert not D.is_dialogue_active()

cmd('pm.EnvPerf2.Viewport 1280 720')
for i,a in enumerate(configs):
 action(a['id']+' prepare',lambda i=i:prepare(i),1.2)
 action(a['id']+' QHD front',lambda a=a:shot(a['id']+'_Front'),.5)
 action(a['id']+' record',lambda i=i:record(i),1.8)
 if a['walk']>0:
  action(a['id']+' walk',lambda:G.set_mode('walk'),4.6)
  if a['run']>0:action(a['id']+' run',lambda:G.set_mode('run'),3.8)
  action(a['id']+' stop',lambda:G.set_mode('idle'),.8)
 action(a['id']+' greet',lambda i=i:G.visuals[i].play_greeting(),2.8)
 action(a['id']+' approach',lambda i=i:approach(i),.18)
 action(a['id']+' interact B',lambda i=i:challenge(i),.5)
 action(a['id']+' check dialogue',lambda i=i:confirm_dialogue(i),3.1)
 action(a['id']+' close dialogue',end_dialogue,.4)
 action(a['id']+' stop record',stop_record,.7)
 action(a['id']+' side',lambda i=i:G.visuals[i].set_actor_rotation(unreal.Rotator(pitch=0,yaw=45,roll=0),True),.7)
 action(a['id']+' QHD side',lambda a=a:shot(a['id']+'_Side'),.4)
 action(a['id']+' rear',lambda i=i:G.visuals[i].set_actor_rotation(unreal.Rotator(pitch=0,yaw=-45,roll=0),True),.7)
 action(a['id']+' QHD rear',lambda a=a:shot(a['id']+'_Rear'),.4)

# A genuine walking/sprint section in the empty test aisle, driven by existing Slate input.
action('walkable center',lambda:G.visit(0),1)
action('player walk',lambda:axis(1,0),1.1)
action('player stop',lambda:axis(0,0),.5)
action('player sprint on',lambda:key('Gamepad_LeftThumbstick'),.2)
action('player sprint',lambda:axis(-1,0),1.0)
action('player stop sprint',lambda:axis(0,0),.4)
action('player sprint off',lambda:key('Gamepad_LeftThumbstick'),.2)
def roundtrip():
 assert Save.save_current_game() and Save.load_game();assert hashlib.sha256(slot.read_bytes()).hexdigest()==before;checks.append('Save/Load uses existing RAM transport, original save bytes unchanged')
action('RAM Save/Load',roundtrip,.4)
action('return to original position',lambda: G.return_to_world(),.7)
def finish(error=None):
 axis(0,0)
 if recording:stop_record()
 if D.is_dialogue_active():D.close_dialogue()
 if not error:G.return_to_world()
 unreal.GameplayStatics.set_global_time_dilation(W,old_dilation);cmd('pm.EnvPerf2.Viewport 0 0');S.set_editor_property('bThrottleCPUWhenNotForeground',throttle);unreal.unregister_slate_post_tick_callback(unreal._npc_review)
 (O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'checks':checks,'shots':shots,'samples':rows,'save_before':before,'save_after':hashlib.sha256(slot.read_bytes()).hexdigest(),'ordinary_pie':True,'simulated_controller_not_hardware':True,'video_method':'Native framebuffer frames at 0.5 game speed, original game timestamps for normal-speed encoding; not an FPS benchmark.'},indent=2));unreal.log('PM_NPC_REVIEW_DONE '+str(error))
def tick(dt):
 global index,due,sample,stage
 try:
  now=unreal.GameplayStatics.get_time_seconds(W);assert time.monotonic()-start<1500
  assert hashlib.sha256(slot.read_bytes()).hexdigest()==before,'Original save changed; stop without overwriting it'
  if now>=sample:
   sample=now+.12;rows.append({'time':now,'stage':stage,'player':P.get_actor_location().to_tuple(),'npc':[{'id':configs[i]['id'],'position':n.get_actor_location().to_tuple(),'speed':v.presentation_speed,'yaw':v.get_actor_rotation().yaw,'walk_alpha':v.visual.get_anim_instance().walk_alpha,'run_alpha':v.visual.get_anim_instance().run_alpha,'greeting_alpha':v.visual.get_anim_instance().greeting_alpha,'foot_correction':v.visual.get_anim_instance().foot_correction_cm} for i,(n,v) in enumerate(zip(G.specimens,G.visuals))]})
  if now<due:return
  if index==len(steps):finish();return
  stage,fn,wait=steps[index];fn();index+=1;due=now+wait;(O/'Progress.json').write_text(json.dumps({'step':index,'total':len(steps),'stage':stage}))
 except Exception:finish(traceback.format_exc())
unreal._npc_review=unreal.register_slate_post_tick_callback(tick)
