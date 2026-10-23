"""Matched QHD V6/V6.1 mesh comparison in ordinary PIE. Fixed real clip poses, no new actors/maps."""
import unreal,json,time,traceback,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/AnimationCorrectionsV61/AlignedAB05';D.mkdir(exist_ok=False);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w;g=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureTestGround)if x.get_outer()==w);assert g.visit(0)and g.set_mode('idle');p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);mesh=p.get_component_by_class(unreal.PokeMonsterMeshyVisualComponent);original_mesh=mesh.get_skeletal_mesh_asset();original_class=unreal.load_class(None,'/Script/PokeMonster.PokeMonsterMeshyAnimInstance');steps=[];shots=[];pairs=[];index=0;due=0;started=time.monotonic();save=R/'Saved/SaveGames/PokeMonster_Dev.sav';sha=hashlib.sha256(save.read_bytes()).hexdigest()
def cmd(s):unreal.SystemLibrary.execute_console_command(w,s,pc)
def action(n,fn,delay=1.):steps.append((n,fn,delay))
def shot(n):
 assert pc.get_viewport_size()==(2560,1440);cam=pc.player_camera_manager;cmd('Shot filename='+str(D/(n+'.png')));shots.append(dict(name=n,camera=cam.get_camera_location().to_tuple(),rotation=cam.get_camera_rotation().to_tuple(),player=p.get_actor_location().to_tuple()))
action('qhd',lambda:cmd('pm.EnvPerf2.Viewport 2560 1440'),2);action('screen',lambda:cmd('r.ScreenPercentage 100'))
v=g.specimens[9]
action('Glurak position',lambda:g.visit(10),2);action('rear',lambda:v.set_actor_rotation(unreal.Rotator(pitch=0,yaw=315,roll=0),False))
for view,yaw in [('Rear',315),('Side',45),('Front',135)]:
 action(view,lambda yaw=yaw:v.set_actor_rotation(unreal.Rotator(pitch=0,yaw=yaw,roll=0),False))
 for label,version in [('Before','V6'),('After','V61')]:
  profile=unreal.load_asset('/Game/Characters/Creatures/Glurak/Animation'+version+'/DA_Glurak_Presentation_'+version);assert profile
  action(view+label,lambda profile=profile:v.set_presentation(profile),1.5);action('shot',lambda n='Glurak'+view+label:shot(n),.4)
 pairs.append(('Glurak'+view+'Before','Glurak'+view+'After'))
action('player center',lambda:g.visit(0),2)
# A brief real input establishes a side view without changing the authored camera.
action('face side',lambda:cmd('pm.Input.Axis Gamepad_LeftX 1'),.25);action('stop',lambda:cmd('pm.Input.Axis Gamepad_LeftX 0'),2)
def pose(asset,role,t):
 mesh.set_skeletal_mesh_asset(asset);clip=unreal.load_asset('/Game/Characters/YoungTrainer/AnimationV6/A_Player_'+role+'_V6');mesh.play_animation(clip,True);mesh.set_play_rate(0.);mesh.set_position(t,False)
for role,t in [('Idle',0.),('Walk',.1375),('Run',.1125)]:
 for label,path in [('Before','/Game/Characters/YoungTrainer/MeshyV2/Meshes/SK_Player_Meshy_V2'),('After','/Game/Characters/YoungTrainer/AnimationV61/SK_Player_V61')]:
  asset=unreal.load_asset(path);assert asset;action(role+label,lambda asset=asset,role=role,t=t:pose(asset,role,t),1);action('shot',lambda n='Player'+role+label:shot(n),.4)
 pairs.append(('Player'+role+'Before','Player'+role+'After'))
def finish(error=None):
 mesh.set_skeletal_mesh_asset(original_mesh);mesh.set_anim_instance_class(original_class);cmd('pm.EnvPerf2.Viewport 0 0');unreal.unregister_slate_post_tick_callback(unreal._v61_aligned);d=[]
 for a,b in pairs:
  aa=next((s for s in shots if s['name']==a),None);bb=next((s for s in shots if s['name']==b),None)
  if aa and bb:d.append(dict(before=a,after=b,camera_delta_cm=sum((x-y)**2 for x,y in zip(aa['camera'],bb['camera']))**.5,rotation_delta=sum((x-y)**2 for x,y in zip(aa['rotation'],bb['rotation']))**.5))
 (D/'Result.json').write_text(json.dumps(dict(passed=error is None,error=error,shots=shots,pairs=d,save_unchanged=hashlib.sha256(save.read_bytes()).hexdigest()==sha),indent=2))
def tick(dt):
 global index,due
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);assert time.monotonic()-started<180
  if now<due:return
  if index==len(steps):finish();return
  n,fn,d=steps[index];fn();index+=1;due=now+d
 except Exception:finish(traceback.format_exc())
unreal._v61_aligned=unreal.register_slate_post_tick_callback(tick)
