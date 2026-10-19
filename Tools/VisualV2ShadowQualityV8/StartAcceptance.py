import unreal,json,math,time,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2ShadowQualityV8';request=json.loads((S/'AcceptanceRequest.json').read_text());D=S/'Acceptance'/request['label'];w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0))
unreal.SystemLibrary.execute_console_command(w,f"pm.EnvPerf2.Viewport {request['width']} {request['height']}");unreal.SystemLibrary.execute_console_command(w,f"r.ScreenPercentage {request['percentage']}")
assert unreal.SystemLibrary.get_console_variable_int_value('r.AntiAliasingMethod')==4,'No console override permitted in integrated acceptance'
volumes=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PostProcessVolume);outside=next(v for v in volumes if v.get_actor_label()=='V2_OutdoorExposure');blends=outside.settings.weighted_blendables.array;assert len(blends)==1 and isinstance(blends[0].object,unreal.PokeMonsterTemporalAABlendable) and blends[0].weight==1
(D/'Graphics.json').write_text(json.dumps({'request':request,'global_aa_cvar':4,'map_aa_blendable':blends[0].object.get_path_name(),'original_shadow_system':True,'renderer_aa_proof':'Existing map-specific TAA blendable retained; no AA override or performance probe requested'}))
import runpy
variant=json.loads((S/'AcceptanceVariant.json').read_text()) if (S/'AcceptanceVariant.json').exists() else {'variant':'A','gain':0,'debug':0}
(S/'VariantRequest.json').write_text(json.dumps(variant));runpy.run_path(str(R/'Tools/VisualV2ShadowQualityV8/RuntimeVariant.py'),run_name='__main__')
(D/'ShadowVariant.json').write_text(json.dumps(variant,indent=2))
source=(R/'Tools/VisualV2QualityV2/FootTest.py').read_text().replace('Saved/VisualV2QualityV2','Saved/VisualV2ShadowQualityV8')
# Existing full route; still photographs and state assertions, no optional video capture.
exec(compile(source,'existing_complete_gameplay_route','exec'),globals())
