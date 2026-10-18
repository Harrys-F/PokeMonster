"""Extra matched PIE image BEFORE measurements. Its scoped CSV is excluded."""
import unreal,time,json,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2GPUBottleneckV1';P=R/'Saved/EnvironmentPerfV2';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
j=json.loads((O/'Request.json').read_text());label='VGB1_PIEPhoto';plan=R/'Tools/VisualV2GPUBottleneckV1/Plans'/(label+'.tsv');assert not plan.exists();plan.write_text(label+'\tPIE\t8\t6\nWald\tControl\t1\t2560\t1440\t2\t100\n');folder=O/'Screenshots/PIE_Baseline';folder.mkdir(parents=True,exist_ok=False)
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Run "'+str(plan)+'"');start=time.monotonic();sent=False

def tick(dt):
 global sent
 if not sent and time.monotonic()-start>5:
  pc=unreal.GameplayStatics.get_player_controller(w,0);assert tuple(pc.get_viewport_size())==(2560,1440)
  mats=[]
  for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
   for c in a.get_components_by_class(unreal.HierarchicalInstancedStaticMeshComponent):
    if c.static_mesh and 'WildBush' in c.static_mesh.get_name():
     for i in range(c.get_num_materials()):
      m=c.get_material(i);b=m.get_base_material() if m else None
      try:used=b.get_editor_property('used_with_instanced_static_meshes')
      except Exception as ex:used=str(ex)
      mats.append({'actor':a.get_name(),'instances':c.get_instance_count(),'material':m.get_path_name() if m else None,'base':b.get_path_name() if b else None,'instanced_usage':used})
  cam=pc.player_camera_manager;(folder/'Proof.json').write_text(json.dumps({'world':w.get_path_name(),'viewport':list(pc.get_viewport_size()),'camera':cam.get_camera_location().to_tuple(),'rotation':cam.get_camera_rotation().to_tuple(),'fov':cam.get_fov_angle(),'instanced_bush_materials':mats,'outside_benchmarks':True},indent=2))
  unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(folder/'PIE_Original.png')+'"');sent=True
 if (P/(label+'_Done.txt')).exists():
  unreal.unregister_slate_post_tick_callback(unreal._vgb_pie_photo)
  actual=R/'Tools/VisualV2GPUBottleneckV1/Plans'/(j['label']+'.tsv');unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Run "'+str(actual)+'"')
  runpy.run_path(str(R/'Tools/VisualV2GPUBottleneckV1/Monitor.py'),run_name='__main__')
unreal._vgb_pie_photo=unreal.register_slate_post_tick_callback(tick)
