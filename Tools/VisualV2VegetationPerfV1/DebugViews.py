"""Qualitative only; do not infer GPU milliseconds or pixel counts from debug colors."""
import unreal,time,json,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2VegetationPerfV1/DebugViews';O.mkdir(exist_ok=False);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name()=='Dev_TestMap_VisualV2GPUBottleneckV1';p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0)
try:cheats=pc.get_editor_property('cheat_manager')
except Exception:cheats=None
if not cheats:
 (O/'Result.json').write_text(json.dumps({'supported':False,'reason':'Existing controller has no CheatManager; viewmode command is gated by UE5.8 GameViewportClient.cpp. No gameplay architecture changed to force debug views.'}))
else:
 unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Viewport 2560 1440');unreal.SystemLibrary.execute_console_command(w,'r.AntiAliasingMethod 2');p.set_actor_location(unreal.Vector(-4300,1550,50.15),False,True)
 modes=['lit','shadercomplexity','quadoverdraw','lodcoloration','lit'];index=-1;start=time.monotonic();last=start;proof=[]
 def tick(dt):
  global index,last
  try:
   now=time.monotonic()
   if now-last<8:return
   if index>=0:
    f=O/(str(index)+'_'+modes[index]+'.png');unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(f)+'"',pc);proof.append({'requested_mode':modes[index],'file_request':str(f),'viewport':list(pc.get_viewport_size()),'camera':pc.player_camera_manager.get_camera_location().to_tuple()})
   index+=1;last=now
   if index==len(modes):
    unreal.unregister_slate_post_tick_callback(unreal._veg_debug);(O/'Result.json').write_text(json.dumps({'supported':'Verify command acceptance in log and actual pixels before treating as debug evidence','captures':proof},indent=2));return
   unreal.SystemLibrary.execute_console_command(w,'viewmode '+modes[index],pc)
  except Exception:
   unreal.SystemLibrary.execute_console_command(w,'viewmode lit',pc);unreal.unregister_slate_post_tick_callback(unreal._veg_debug);(O/'Result.json').write_text(json.dumps({'error':traceback.format_exc()}))
 unreal._veg_debug=unreal.register_slate_post_tick_callback(tick)
