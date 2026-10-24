"""Transient Unreal SceneCapture overview, explicitly separate from fixed gameplay camera evidence."""
import unreal,json,time,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();w=E.get_editor_world();assert w.get_name()=='Dev_BiomeTestMap_V1';ES=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
c=ES.spawn_actor_from_class(unreal.SceneCapture2D,unreal.Vector(*L.world(0,-8000,18000)),unreal.Rotator(),True)
c.set_actor_rotation(unreal.MathLibrary.find_look_at_rotation(c.get_actor_location(),unreal.Vector(0,0,50)),False)
cap=c.capture_component2d;target=unreal.RenderingLibrary.create_render_target2d(w,2560,1440,unreal.TextureRenderTargetFormat.RTF_RGBA8_SRGB)
cap.set_editor_property('texture_target',target);cap.set_editor_property('capture_source',unreal.SceneCaptureSource.SCS_FINAL_COLOR_LDR);cap.set_editor_property('fov_angle',55);cap.set_editor_property('capture_every_frame',True)
culled=[]
for a in ES.get_all_level_actors():
 for x in a.get_components_by_class(unreal.HierarchicalInstancedStaticMeshComponent):
  culled.append((x,x.instance_start_cull_distance,x.instance_end_cull_distance));x.set_cull_distances(25000,30000)
start=time.monotonic()
def done(dt):
 if time.monotonic()-start<3:return
 unreal.unregister_slate_post_tick_callback(unreal._biome_overview)
 try:
  cap.capture_scene();unreal.RenderingLibrary.export_render_target(w,target,str(R/'Saved/BiomeTestV1'),'Overview_Unreal_sRGB.png')
  (R/'Saved/BiomeTestV1/Overview.json').write_text(json.dumps({'type':'Actual Unreal SceneCapture overview; NOT fixed gameplay camera','color_encoding':'Native sRGB render target, no external image editing','size':[2560,1440],'location':c.get_actor_location().to_tuple(),'fov':55,'gameplay_camera_changed':False,'not_saved_to_map':True},indent=2))
 finally:
  for x,a,b in culled:x.set_cull_distances(a,b)
  ES.destroy_actor(c)
  # Discard only temporary overview actor/culling transaction on the newly authored map.
  assert all(p.get_path_name()=='/Game/Maps/Dev_BiomeTestMap_V1'for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages())
  assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
  assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_BiomeTestMap_V1')
unreal._biome_overview=unreal.register_slate_post_tick_callback(done)
