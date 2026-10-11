"""Same world/camera A-B-B-A comparison. Changes exist only in the PIE duplicate.
Diagnostic shadow/foliage modes are restored; no quality reduction is saved.
Run after walking to the measurement point. Never moves the pawn/camera.
"""
import unreal,json,time,statistics
from pathlib import Path
R=Path(unreal.Paths.project_dir());O=R/'Saved/WestlandAssetLibraryV3';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and 'Dev_WestlandAssetLibrary' in w.get_name();pc=unreal.GameplayStatics.get_player_controller(w,0);p=unreal.GameplayStatics.get_player_pawn(w,0);job=json.loads((O/'PerformanceJob.json').read_text());mode=job['mode'];run=job['run'];assert mode in ('V2','V3','V3NoShadows','V3Hidden','V3OpaqueDiagnostic')
actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};comps=[actors['V3_Forest_'+k].static_mesh_component for k in ('Oak','BushA','BushB')];original=[(c,c.static_mesh,c.get_editor_property('cast_shadow'),list(c.get_editor_property('override_materials')),c.is_visible(),c.mobility) for c in comps];D='/Game/Environment/WestlandAssetLibrary';swaps=['Trees/SM_WLA_OakAncient_A','Vegetation/SM_WLA_Bush_A','Vegetation/SM_WLA_Bush_B']
# Runtime SetStaticMesh rejects static components. Make all three comparison
# components equally movable only in this PIE world, and verify the actual swap.
for c in comps:c.set_mobility(unreal.ComponentMobility.MOVABLE)
if mode=='V2':
 for c,path in zip(comps,swaps):
  c.set_editor_property('override_materials',[]);mesh=unreal.load_asset(D+'/Meshes/'+path);assert c.set_static_mesh(mesh) and c.static_mesh==mesh
elif mode=='V3NoShadows':
 for c in comps:c.set_cast_shadow(False)
elif mode=='V3Hidden':
 for c in comps:c.set_visibility(False,False)
elif mode=='V3OpaqueDiagnostic':
 # A transient material copy with the same base colour/roughness, alpha test disabled.
 # It is a cost diagnostic only: opaque cards are visibly unsuitable as final art.
 opaque=unreal.new_object(unreal.MaterialInstanceConstant);L=unreal.MaterialEditingLibrary;L.set_material_instance_parent(opaque,unreal.load_asset(D+'/QualityV3/Materials/M_WLA_FoliageGroups_V3'));over=opaque.get_editor_property('base_property_overrides');over.set_editor_property('override_blend_mode',True);over.set_editor_property('blend_mode',unreal.BlendMode.BLEND_OPAQUE);opaque.set_editor_property('base_property_overrides',over);L.update_material_instance(opaque)
 for c in comps:c.set_material(1,opaque)
for cmd in ['t.MaxFPS 0','r.VSync 0','r.GPUCsvStatsEnabled 1','sg.ViewDistanceQuality 1','sg.AntiAliasingQuality 1','sg.ShadowQuality 1','sg.GlobalIlluminationQuality 1','sg.ReflectionQuality 1','sg.PostProcessQuality 1','sg.TextureQuality 1','sg.EffectsQuality 1','sg.FoliageQuality 1','r.ScreenPercentage 75']:unreal.SystemLibrary.execute_console_command(w,cmd)
measured_meshes=[{'mesh':c.static_mesh.get_path_name(),'materials':[c.get_material(i).get_path_name() for i in range(c.get_num_materials()) if c.get_material(i)],'mobility':str(c.mobility)} for c in comps]
name='WLA_V3_'+run;start=time.monotonic();last=start;frames=[];started=False;captured=False;loc=p.get_actor_location();arm=p.get_component_by_class(unreal.SpringArmComponent);cam=p.get_component_by_class(unreal.CameraComponent)
def restore():
 for c,mesh,shadow,overrides,visible,mobility in original:
  c.set_static_mesh(mesh);c.set_editor_property('override_materials',overrides);c.set_cast_shadow(shadow);c.set_visibility(visible,False);c.set_mobility(mobility)
def tick(dt):
 global last,started,captured
 now=time.monotonic()
 if not captured and now-start>=5:
  unreal.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+str(O/('PIE_Performance_'+run+'.png'))+'"',pc);captured=True
 if now-start<10:last=now;return
 if not started:
  # Capture before profiling so screenshot stalls cannot contaminate the timing.
  unreal.SystemLibrary.execute_console_command(w,'csvprofile startfile='+name);unreal.SystemLibrary.execute_console_command(w,'csvprofile start');started=True
 frames.append((now-last)*1000);last=now
 if now-start<40:return
 unreal.SystemLibrary.execute_console_command(w,'csvprofile stop');unreal.unregister_slate_post_tick_callback(unreal._wla_v3_perf);del unreal._wla_v3_perf;restore()
 assert (p.get_actor_location()-loc).length()<1 and arm.target_arm_length==2500 and cam.field_of_view==35
 out={'mode':mode,'run':run,'seconds':now-start-10,'viewport':list(pc.get_viewport_size()),'quality':'Medium, 75%, VSync off, uncapped','fps_wall':1000/statistics.mean(frames),'median_ms':statistics.median(frames),'p95_ms':sorted(frames)[int(len(frames)*.95)],'samples':len(frames),'location_cm':list(loc.to_tuple()),'camera':[2500,arm.get_world_rotation().pitch,arm.get_world_rotation().yaw,cam.field_of_view],'meshes_rendered':measured_meshes,'runtime_changes_restored':True,'csv':name+'.csv'};(O/('Performance_'+run+'.json')).write_text(json.dumps(out,indent=2));unreal.log('WLA_V3_PERF_DONE '+run)
assert not hasattr(unreal,'_wla_v3_perf');unreal._wla_v3_perf=unreal.register_slate_post_tick_callback(tick)
