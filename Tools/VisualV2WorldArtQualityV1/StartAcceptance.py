import unreal,json,math,time,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtQualityV1';request=json.loads((S/'AcceptanceRequest.json').read_text());D=S/'Acceptance'/request['label'];w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0))
unreal.SystemLibrary.execute_console_command(w,f"pm.EnvPerf2.Viewport {request['width']} {request['height']}");unreal.SystemLibrary.execute_console_command(w,f"r.ScreenPercentage {request['percentage']}");unreal.SystemLibrary.execute_console_command(w,'r.VSync 0');unreal.SystemLibrary.execute_console_command(w,'t.MaxFPS 0');unreal.SystemLibrary.execute_console_command(w,'r.DynamicRes.OperationMode 0')
assert unreal.SystemLibrary.get_console_variable_int_value('r.AntiAliasingMethod')==4,'No console override permitted in integrated acceptance'
volumes=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PostProcessVolume);outside=next(v for v in volumes if v.get_actor_label()=='V2_OutdoorExposure');blends=outside.settings.weighted_blendables.array;assert len(blends)==1 and isinstance(blends[0].object,unreal.PokeMonsterTemporalAABlendable) and blends[0].weight==1
(D/'Graphics.json').write_text(json.dumps({'request':request,'global_aa_cvar':4,'map_aa_blendable':blends[0].object.get_path_name(),'original_shadow_system':True,'renderer_aa_proof':'Independent per-view renderer observer in paired timing runs; cvar alone is not AA proof'}))
source=(R/'Tools/VisualV2QualityV2/FootTest.py').read_text().replace('Saved/VisualV2QualityV2','Saved/VisualV2WorldArtQualityV1')
# Capture only the real door/interior/exit segment, outside timing measurements.
recording=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('WorldArtV1_Door_'+request['label']);recording.parent.mkdir(exist_ok=True)
door_recording={'started':False,'stopped':False,'steps':[]}
def capture_door(name,seconds):
 if name=='DoorEntry' and not door_recording['started']:
  unreal.SystemLibrary.execute_console_command(w,'pm.TAAReview.CaptureStart "'+str(recording)+'"');door_recording['started']=True
 if door_recording['started'] and not door_recording['stopped']:
  door_recording['steps'].append({'step':name,'game_seconds':seconds})
  if name=='CutawayOutside':
   unreal.SystemLibrary.execute_console_command(w,'pm.TAAReview.CaptureStop');door_recording['stopped']=True
   (D/'DoorRecording.json').write_text(json.dumps({'recording':str(recording),'steps':door_recording['steps']},indent=2))
needle='kind,name,arg=route[i];elapsed=seconds-stage;';assert needle in source
source=source.replace(needle,needle+'capture_door(name,seconds);')
# Existing input and gameplay route remains unchanged on disk.
exec(compile(source,'existing_complete_gameplay_route','exec'),globals())
