"""Prove the surface responsible; transient PIE changes only, restored on completion."""
import unreal,json,time,traceback,gc
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2StabilityV1';assert json.loads((D/'PerformanceBefore01/Result.json').read_text())['passed'];O=D/'SurfaceAblation01';O.mkdir(exist_ok=False)
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);hills=[a.static_mesh_component for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.StaticMeshActor)if a.get_actor_label()in ['Hill_Step_Low','Hill_Step_Mid','Hill_Lookout']];assert len(hills)==3;old=[(c,c.is_visible(),c.get_material(0))for c in hills];ground=unreal.load_asset('/Game/Environment/VisualV2EnvironmentV3/Materials/M_EQ3_Ground')
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def photo(n):cmd('HighResShot 2560x1440 filename="'+str(O/(n+'.png'))+'"')
def hide():
 for c,v,m in old:c.set_visibility(False,False)
def restore():
 for c,v,m in old:c.set_visibility(v,False);c.set_material(0,m)
def candidate():
 restore()
 for c,v,m in old:c.set_material(0,ground)
cmd('pm.WorldClock pause');cmd('pm.WorldClock set 1 19 0');cmd('pm.EnvPerf2.Viewport 2560 1440');P.set_actor_location(unreal.Vector(-650,1000,110.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
route=[('Control',lambda:None),('Original',lambda:photo('Original')),('Hide three old platforms',hide),('Hidden',lambda:photo('NoPlatformRendering')),('Existing ground material on same platforms',candidate),('Candidate',lambda:photo('GroundMaterial')),('Restore',restore)];s={'i':0,'last':time.monotonic()}
def finish(error=None):
 restore();unreal.unregister_slate_post_tick_callback(unreal._stability_ablate);(O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'platforms':[c.get_owner().get_actor_label()for c,v,m in old],'original':[m.get_path_name()for c,v,m in old],'candidate':ground.get_path_name(),'collision_unchanged':True},indent=2));route.clear()
 for n in ['W','P','PC','hills','old','c','m']:globals().pop(n,None)
 gc.collect()
def tick(dt):
 try:
  if time.monotonic()-s['last']<2:return
  name,f=route[s['i']];f();s.update(i=s['i']+1,last=time.monotonic())
  if s['i']==len(route):finish()
 except Exception:finish(traceback.format_exc())
unreal._stability_ablate=unreal.register_slate_post_tick_callback(tick)
