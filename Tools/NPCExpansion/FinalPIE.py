"""Final ordinary-PIE smoke test of final shared models, live motion, input, boundary and RAM save."""
import unreal,json,time,hashlib,traceback,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/NPCExpansion';W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W
P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W);G=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterNPCTestGround)if x.get_outer()==W);Save=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==GI);assert len(G.specimens)==len(G.visuals)==11 and G.set_mode('idle') and G.visit(0)
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';sha=hashlib.sha256(slot.read_bytes()).hexdigest();S=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=S.get_editor_property('bThrottleCPUWhenNotForeground');S.set_editor_property('bThrottleCPUWhenNotForeground',False);sprint=P.is_sprint_mode_enabled();steps=[];i=0;due=0;start=time.monotonic();checks=[];positions=[]
def cmd(v):unreal.SystemLibrary.execute_console_command(W,v,PC)
def axis(x,y):cmd('pm.Input.Axis Gamepad_LeftX '+str(x));cmd('pm.Input.Axis Gamepad_LeftY '+str(y))
def key(k):cmd('pm.Input.Key '+k+' down');cmd('pm.Input.Key '+k+' up')
def action(n,fn,wait=.3):steps.append((n,fn,wait))
for index,id in [(5,'WhiteHairedWarrior'),(6,'DwarfWarrior'),(8,'ElvenArcher')]:
 def verify(index=index,id=id):
  assert G.visit(index+1);m=G.visuals[index].visual.get_skeletal_mesh_asset();assert m.get_path_name().split('.')[0]=='/Game/Characters/NPCs/'+id+'/Meshes/SK_'+id+'_NPC_V1';checks.append(id+' uses original suitable mesh/skeleton')
 action(id+' verify',verify,1)
 action(id+' QHD final',lambda id=id:cmd('HighResShot 2560x1440 filename="'+str(O/(id+'_FinalShared_QHD.png'))+'"'),.4)
 action(id+' walk',lambda:G.set_mode('walk'),1.4)
 action(id+' run',lambda:G.set_mode('run'),1.4)
 action(id+' stop',lambda:G.set_mode('idle'),.4)

def begin_all():
 assert G.visit(0);positions[:]=[n.get_actor_location().to_tuple()for n in G.specimens];G.set_mode('walk')
action('all motion start',begin_all,5.5)
def check_all():
 moved=[]
 for j,(old,n)in enumerate(zip(positions,G.specimens)):
  distance=math.dist(old,n.get_actor_location().to_tuple());moving=j not in [1,2]
  assert distance>20 if moving else distance<.01,(j,distance);moved.append({'station':j+1,'distance_cm':distance,'stationary_by_design':not moving})
 checks.append({'nine_actual_walkers_two_stationary':moved});G.set_mode('idle')
action('all motion check',check_all,.3)
def edge():
 if P.is_sprint_mode_enabled():key('Gamepad_LeftThumbstick')
 P.set_actor_location(unreal.Vector(-7500+2300,3350,50),False,True);axis(1,1)
action('player real boundary walk',edge,2.2)
def boundary():
 axis(0,0);x=P.get_actor_location();assert x.x<-7500+2480 and x.z>45,(x.x,x.z);checks.append('Real player input/capsule stopped at new perimeter without falling')
action('boundary check',boundary,.4)
def save():
 assert Save.save_current_game() and Save.load_game();assert hashlib.sha256(slot.read_bytes()).hexdigest()==sha;checks.append('RAM Save/Load, disk save SHA unchanged');assert G.return_to_world()
action('save and return',save,.4)
def finish(error=None):
 axis(0,0)
 if P.is_sprint_mode_enabled()!=sprint:key('Gamepad_LeftThumbstick')
 S.set_editor_property('bThrottleCPUWhenNotForeground',throttle);unreal.unregister_slate_post_tick_callback(unreal._npc_final);(O/'FinalPIE.json').write_text(json.dumps({'passed':error is None,'error':error,'checks':checks,'save_unchanged':hashlib.sha256(slot.read_bytes()).hexdigest()==sha,'simulated_input_not_hardware':True,'ordinary_pie_no_qa_spawn':True},indent=2));unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
def tick(dt):
 global i,due
 try:
  now=unreal.GameplayStatics.get_time_seconds(W);assert time.monotonic()-start<180
  if now<due:return
  if i==len(steps):finish();return
  name,fn,wait=steps[i];fn();i+=1;due=now+wait;(O/'FinalPIEProgress.json').write_text(json.dumps({'step':i,'stage':name}))
 except Exception:finish(traceback.format_exc())
unreal._npc_final=unreal.register_slate_post_tick_callback(tick)
