"""Run after timing. Identical frozen game pose; ProfileGPU not used as benchmark."""
import unreal,time,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/TreeShadowProxyV1';D=R/'Art/World/TreeShadowProxyV1/Review';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);actors=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor)
trees=[next(a for a in actors if a.get_actor_label()=='V2_ForestOak_'+str(i)).static_mesh_component for i in range(3)];proxies=[a.static_mesh_component for a in actors if a.get_actor_label().startswith('TSP_V2_ForestOak_')]
original=p.get_actor_transform();saved=[(c,c.cast_shadow) for c in trees+proxies];paused=[(c,c.get_editor_property('pause_anims')) for c in unreal.ObjectIterator(unreal.SkeletalMeshComponent) if c.get_world()==w]
for c,_ in paused:c.set_editor_property('pause_anims',True)
for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']:unreal.SystemLibrary.execute_console_command(w,'sg.'+n+'Quality 2')
for n,v in [('r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor',1),('r.Shadow.Virtual.SMRT.RayCountDirectional',8),('r.Lumen.FinalGatherMethod',1),('r.Lumen.HardwareRayTracing',1),('r.ScreenPercentage',100),('r.VSync',0),('t.MaxFPS',0)]:unreal.SystemLibrary.execute_console_command(w,n+' '+str(v))
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Viewport 2560 1440');p.set_actor_location(unreal.Vector(-4300,1550,50.15),False,True)
start=time.monotonic();i=0;sent=False;records=[];stages=[('A',12),('B',12),('A_GPU',12),('B_GPU',12)]
def state(b):
 for c in trees:c.set_cast_shadow(not b)
 for c in proxies:c.set_cast_shadow(b)
state(False)
def tick(dt):
 global start,i,sent
 elapsed=time.monotonic()-start
 if elapsed<stages[i][1]:return
 if not sent:
  tag=stages[i][0];cam=pc.player_camera_manager
  if 'GPU' in tag:
   unreal.log('TREE_SHADOW_GPU_BEGIN '+tag)
   for cmd in ['r.ProfileGPU.ShowUI 0','r.ProfileGPU.ShowLeafEvents 1','r.ProfileGPU.ThresholdPercent 0.1','ProfileGPU']:unreal.SystemLibrary.execute_console_command(w,cmd)
  else:unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(D/('GameCamera_'+tag+'_QHD.png'))+'"',pc)
  records.append({'tag':tag,'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'player':p.get_actor_location().to_tuple(),'camera':cam.get_camera_location().to_tuple(),'rotation':cam.get_camera_rotation().to_tuple(),'fov':cam.get_fov_angle(),'viewport':tuple(pc.get_viewport_size()),'tree_shadow':[bool(c.cast_shadow) for c in trees],'proxy_shadow':[bool(c.cast_shadow) for c in proxies]})
  sent=True;return
 if elapsed<stages[i][1]+2:return
 i+=1;start=time.monotonic();sent=False
 if i==len(stages):
  for c,b in saved:c.set_cast_shadow(b)
  for c,b in paused:c.set_editor_property('pause_anims',b)
  p.set_actor_transform(original,False,True);(D/'MatchedCamera.json').write_text(json.dumps(records,indent=2));unreal.unregister_slate_post_tick_callback(unreal._tree_shots);del unreal._tree_shots;return
 state(stages[i][0].startswith('B'))
unreal._tree_shots=unreal.register_slate_post_tick_callback(tick)
