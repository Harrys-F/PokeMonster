"""Temporary 8-degree receiver in PIE only. No map/mesh/material/light is saved or edited."""
import unreal,time,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();request=json.loads((R/'Saved/VisualV2AASoftShadowsV1/Request.json').read_text());open_site=request.get('slope_open',False);O=R/'Saved/VisualV2AASoftShadowsV1'/('SlopeOpen' if open_site else 'Slope');O.mkdir(exist_ok=False)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name()=='Dev_TestMap_VisualV2GPUBottleneckV1'
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Viewport 2560 1440');unreal.SystemLibrary.execute_console_command(w,'r.ScreenPercentage 75')
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);
if open_site:p.set_actor_location(unreal.Vector(-36.6,-47.1,50.15),False,False)
start=p.get_actor_location();assert open_site or (abs(start.x+760)<5 and abs(start.y+1410)<5)
unreal.SystemLibrary.execute_console_command(w,'pm.SoftShadows.Slope 1')
a=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor) if 'VAS_RuntimeOnly_Slope' in [str(t) for t in a.tags])
unreal.SystemLibrary.execute_console_command(w,'r.AntiAliasingMethod 2');unreal.SystemLibrary.execute_console_command(w,'pm.SoftShadows.Test 1')
s=next(s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if s.get_world()==w);move=next(a for a in unreal.ObjectIterator(unreal.InputAction) if a.get_outer()==p and a.get_name()=='MoveAction');records=[];begin=time.monotonic();stage=0;shot=False

def inject(dx,dy):
 yaw=math.radians(p.get_movement_basis_yaw());s.inject_input_vector_for_action(move,unreal.Vector(-math.sin(yaw)*dx+math.cos(yaw)*dy,math.cos(yaw)*dx+math.sin(yaw)*dy,0),[],[])
def finish(error=None):
 inject(0,0);unreal.SystemLibrary.execute_console_command(w,'pm.SoftShadows.Test 0');unreal.SystemLibrary.execute_console_command(w,'pm.SoftShadows.Slope 0');unreal.unregister_slate_post_tick_callback(unreal._vas_slope)
 (O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'temporary_actor_destroyed':True,'slope_degrees':8,'preparation_teleport':open_site,'viewport':list(pc.get_viewport_size()),'records':records},indent=2))
def tick(dt):
 global stage,shot
 try:
  assert time.monotonic()-begin<45,'Blocked or timed out'
  if time.monotonic()-begin<2:return
  q=p.get_actor_location();target=start.x+580 if stage==0 else start.x
  if abs(q.x-target)<12:
   inject(0,0)
   if stage==0:stage=1;return
   assert max(r['position'][2] for r in records)>start.z+20,'Ramp not reached';finish();return
  inject(1 if target>q.x else -1,0)
  blobs=[d for d in unreal.ObjectIterator(unreal.DecalComponent) if d.get_world()==w and d.get_decal_material() and 'FigureBlob' in d.get_decal_material().get_path_name()]
  nearest=min(blobs,key=lambda d:(d.get_world_location()-q).length()) if blobs else None
  record={'time':time.monotonic()-begin,'stage':stage,'position':q.to_tuple(),'blob':nearest.get_world_location().to_tuple() if nearest else None,'blob_rotation':nearest.get_world_rotation().to_tuple() if nearest else None};records.append(record)
  if nearest:assert math.hypot(nearest.get_world_location().x-q.x,nearest.get_world_location().y-q.y)<8,'Shadow lags horizontally'
  if stage==0 and q.x>start.x+400 and not shot:
   shot=True;unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(O/'SlopePlayer.png')+'"',pc)
 except Exception as e:finish(str(e))
unreal._vas_slope=unreal.register_slate_post_tick_callback(tick)
