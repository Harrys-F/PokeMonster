import unreal,json,math,time,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtV6';request=json.loads((S/'AcceptanceRequest.json').read_text());D=S/'Acceptance'/request['label'];w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0))
unreal.SystemLibrary.execute_console_command(w,f"pm.EnvPerf2.Viewport {request['width']} {request['height']}");unreal.SystemLibrary.execute_console_command(w,f"r.ScreenPercentage {request['percentage']}")
assert unreal.SystemLibrary.get_console_variable_int_value('r.AntiAliasingMethod')==4,'No console override permitted in integrated acceptance'
volumes=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PostProcessVolume);outside=next(v for v in volumes if v.get_actor_label()=='V2_OutdoorExposure');blends=outside.settings.weighted_blendables.array;assert len(blends)==1 and isinstance(blends[0].object,unreal.PokeMonsterTemporalAABlendable) and blends[0].weight==1
(D/'Graphics.json').write_text(json.dumps({'request':request,'global_aa_cvar':4,'map_aa_blendable':blends[0].object.get_path_name(),'original_shadow_system':True,'renderer_aa_proof':'Existing map-specific TAA blendable retained; no AA override or performance probe requested'}))
source=(R/'Tools/VisualV2QualityV2/FootTest.py').read_text().replace('Saved/VisualV2QualityV2','Saved/VisualV2WorldArtV6')
# Existing full route; still photographs and state assertions, no optional video capture.
exec(compile(source,'existing_complete_gameplay_route','exec'),globals())
