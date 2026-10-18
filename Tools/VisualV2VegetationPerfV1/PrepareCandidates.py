"""Separate shader-only test copies; original graph, alpha and textures unchanged."""
import unreal,json,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2VegetationPerfV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
L=unreal.MaterialEditingLibrary;D='/Game/Environment/VegetationPerfV1/Materials';rows=[]
graph=runpy.run_path(str(R/'Tools/VisualV2MaterialFixV1/GraphAudit.py'))['graph']
for src,name in [('/Game/Environment/DevTestMapVisualV2/Materials/M_V2_CrownReveal','M_VVP1_CrownFullyRough'),('/Game/Environment/WestlandAssetLibrary/QualityV3/Materials/M_WLA_FoliageGroups_V3','M_VVP1_FoliageFullyRough')]:
 original=unreal.load_asset(src);assert original and not original.get_editor_property('fully_rough');dst=D+'/'+name;assert not unreal.EditorAssetLibrary.does_asset_exist(dst);m=unreal.EditorAssetLibrary.duplicate_asset(src,dst);assert m
 m.set_editor_property('fully_rough',True);L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
 a=graph(original);b=graph(m)
 assert a==b,'Shader graph changed beyond compile flag'
 rows.append({'original':src,'candidate':dst,'only_change':'fully_rough false -> true; graph/alpha/shadows unchanged','graph_equal':True,'original_stats':str(L.get_statistics(original)),'candidate_stats':str(L.get_statistics(m))})
(O/'Candidates.json').write_text(json.dumps(rows,indent=2));assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
