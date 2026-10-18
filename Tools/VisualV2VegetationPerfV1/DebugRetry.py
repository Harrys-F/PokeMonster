"""Wait for the actual capture file before switching debug mode. No timing claims."""
import unreal,time,json,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2VegetationPerfV1/DebugViewsR2';O.mkdir(exist_ok=False);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name()=='Dev_TestMap_VisualV2GPUBottleneckV1';p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);assert pc.get_editor_property('cheat_manager')
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Viewport 2560 1440');unreal.SystemLibrary.execute_console_command(w,'r.AntiAliasingMethod 2');p.set_actor_location(unreal.Vector(-4300,1550,50.15),False,True)
modes=['lit','shadercomplexity','quadoverdraw','lodcoloration','lit'];index=0;last=time.monotonic();sent=False;proof=[];unreal.SystemLibrary.execute_console_command(w,'viewmode '+modes[index],pc)
def tick(dt):
 global index,last,sent
 try:
  now=time.monotonic();file=O/(str(index)+'_'+modes[index]+'.png')
  if not sent:
   if now-last<10:return
   unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(file)+'"',pc);sent=True;last=now;return
  fs=list(O.glob(file.stem+'*.png'))
  if not fs or now-last<1:return
  assert len(fs)==1;proof.append({'mode':modes[index],'file':str(fs[0]),'viewport':list(pc.get_viewport_size()),'camera':pc.player_camera_manager.get_camera_location().to_tuple(),'mode_held_until_file_written':True});index+=1;sent=False;last=now
  if index==len(modes):
   unreal.unregister_slate_post_tick_callback(unreal._veg_debug2);(O/'Result.json').write_text(json.dumps({'captures':proof,'error':None,'interpretation_requires_actual_pixel_review':True},indent=2));return
  unreal.SystemLibrary.execute_console_command(w,'viewmode '+modes[index],pc)
 except Exception:
  unreal.SystemLibrary.execute_console_command(w,'viewmode lit',pc);unreal.unregister_slate_post_tick_callback(unreal._veg_debug2);(O/'Result.json').write_text(json.dumps({'error':traceback.format_exc()}))
unreal._veg_debug2=unreal.register_slate_post_tick_callback(tick)
