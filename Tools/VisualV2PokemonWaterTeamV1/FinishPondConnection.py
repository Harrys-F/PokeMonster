"""Clip only the proven overlap of our local stream copy with the new pond."""
import unreal,json,hashlib
from pathlib import Path
D=Path(unreal.Paths.project_dir()).resolve()/'Saved/ProjectRefinement/VisualV2PokemonWaterTeamV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
path='/Game/Environment/VisualV2PokemonWaterTeamV1/Materials/M_V2RiverConnection';m=unreal.load_asset(path);assert m;nchanged=0
for n in unreal.MaterialEditingLibrary.get_material_expressions(m):
 if not isinstance(n,unreal.MaterialExpressionCustom):continue
 code=n.get_editor_property('code')
 if 'return float4(col,wet);'in code:
  assert 'float outlet='in code and 'float d=min(stream,outlet)'in code
  n.set_editor_property('code',code.replace('return float4(col,wet);','return float4(col,wet*step(1.0,length((P.xy-float2(720,-1000))/float2(900,650))));'));nchanged+=1
assert nchanged==1;unreal.MaterialEditingLibrary.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();(D/'WaterOverlapFixed.json').write_text(json.dumps({'material':path,'new_pond_ellipse_only':True,'preserved_shared_water_materials':True,'permanent_rendering_cvar_changes':False},indent=2))
