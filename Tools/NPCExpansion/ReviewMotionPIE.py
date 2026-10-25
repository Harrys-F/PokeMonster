"""Higher-density, native presented-frame movement proof; all real rendered frames."""
import unreal,json,time,traceback,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();label='Motion02';O=R/'Saved/ProjectRefinement/NPCExpansion'/label;O.mkdir(exist_ok=False);W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W
P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);G=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterNPCTestGround) if x.get_outer()==W);assert G.set_mode('idle') and G.visit(1)
S=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=S.get_editor_property('bThrottleCPUWhenNotForeground');S.set_editor_property('bThrottleCPUWhenNotForeground',False);dilation=unreal.GameplayStatics.get_global_time_dilation(W);unreal.GameplayStatics.set_global_time_dilation(W,.25)
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';sha=hashlib.sha256(slot.read_bytes()).hexdigest();configs=json.loads((R/'Tools/NPCExpansion/Library.json').read_text());steps=[];index=0;due=0;stage='setup';recording=False;start=time.monotonic();rows=[];sample=0

def cmd(v):unreal.SystemLibrary.execute_console_command(W,v,PC)
def action(n,fn,wait=.3):steps.append((n,fn,wait))
def prepare(i):assert G.set_mode('idle') and G.visit(i+1)
def record(i):
 global recording
 path=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('NPCLibrary_'+label+'_'+configs[i]['id']);assert not path.exists();cmd('pm.TAAReview.CaptureStart "'+str(path)+'" slate 60');recording=True

def stop():
 global recording
 cmd('pm.TAAReview.CaptureStop');recording=False
cmd('pm.EnvPerf2.Viewport 2560 1440')
for i,a in enumerate(configs):
 action(a['id']+' prepare',lambda i=i:prepare(i),.8)
 action(a['id']+' record idle',lambda i=i:record(i),1.2)
 if a['walk']>0:
  action(a['id']+' walk',lambda:G.set_mode('walk'),3.6)
  if a['run']>0:action(a['id']+' run',lambda:G.set_mode('run'),2.5)
  action(a['id']+' stop',lambda:G.set_mode('idle'),.8)
 action(a['id']+' greeting',lambda i=i:G.visuals[i].play_greeting(),2.8)
 action(a['id']+' final idle',lambda:G.set_mode('idle'),.7)
 action(a['id']+' stop recording',stop,.4)

def finish(error=None):
 if recording:stop()
 G.set_mode('idle');G.return_to_world();unreal.GameplayStatics.set_global_time_dilation(W,dilation);cmd('pm.EnvPerf2.Viewport 0 0');S.set_editor_property('bThrottleCPUWhenNotForeground',throttle);unreal.unregister_slate_post_tick_callback(unreal._npc_motion)
 (O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'samples':rows,'ordinary_pie':True,'save_unchanged':hashlib.sha256(slot.read_bytes()).hexdigest()==sha,'video_method':'Actual presented Slate frames. QHD game viewport (2560x1440), existing renderer settings, actual viewport crop dimensions recorded. PIE slowed to 0.25 during capture, encoded at original game timestamps; no synthetic/interpolated frames and no performance benchmark.'},indent=2));unreal.log('PM_NPC_MOTION_DONE '+str(error))
def tick(dt):
 global index,due,stage,sample
 try:
  now=unreal.GameplayStatics.get_time_seconds(W);assert time.monotonic()-start<1500;assert hashlib.sha256(slot.read_bytes()).hexdigest()==sha
  if now>=sample:
   sample=now+.10;rows.append({'time':now,'stage':stage,'render_size':PC.get_viewport_size(),'npcs':[{'id':configs[i]['id'],'position':n.get_actor_location().to_tuple(),'yaw':v.get_actor_rotation().yaw,'speed':v.presentation_speed,'walk_alpha':v.visual.get_anim_instance().walk_alpha,'run_alpha':v.visual.get_anim_instance().run_alpha,'greeting_alpha':v.visual.get_anim_instance().greeting_alpha,'foot_correction_cm':v.visual.get_anim_instance().foot_correction_cm}for i,(n,v)in enumerate(zip(G.specimens,G.visuals))]})
  if now<due:return
  if index==len(steps):finish();return
  stage,fn,wait=steps[index];fn();index+=1;due=now+wait;(O/'Progress.json').write_text(json.dumps({'step':index,'total':len(steps),'stage':stage}))
 except Exception:finish(traceback.format_exc())
unreal._npc_motion=unreal.register_slate_post_tick_callback(tick)
