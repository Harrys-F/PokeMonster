"""Create three isolated derived material candidates; never save originals or a map."""
import unreal,json,sys,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert all(x.get_path_name().startswith('/Game/Environment/VisualV2PerformanceV1/')for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages())
sys.path.insert(0,str(R/'Tools/VisualV2PerformanceV1'));from SpatialRoute import accelerate
results=[]
for name in ['Ground','MainPath','NorthPath']:
 src='/Game/Environment/VisualV2EnvironmentV3/Materials/M_EQ3_'+name;dest='/Game/Environment/VisualV2PerformanceV1/Materials/M_PV1_'+name;source=unreal.load_asset(src)
 m=unreal.load_asset(dest)if unreal.EditorAssetLibrary.does_asset_exist(dest)else unreal.EditorAssetLibrary.duplicate_asset(src,dest);assert m
 originals={x.get_name():x.get_editor_property('code')for x in unreal.ObjectIterator(unreal.MaterialExpressionCustom)if x.get_outer()==source and'W6Route'in x.get_editor_property('code')};assert originals
 nodes={x.get_name():x for x in unreal.ObjectIterator(unreal.MaterialExpressionCustom)if x.get_outer()==m};proofs=[]
 for key,code in originals.items():
  candidate,proof=accelerate(code);node=nodes[key];assert node.get_editor_property('code')in [code,candidate],'Unrecognized candidate modification';node.set_editor_property('code',candidate);proofs.append({'node':key,'source_code_sha256':hashlib.sha256(code.encode()).hexdigest(),'candidate_code_sha256':hashlib.sha256(candidate.encode()).hexdigest(),'proof':proof})
 unreal.MaterialEditingLibrary.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);results.append({'source':src,'candidate':dest,'nodes':proofs});(D/'MaterialCandidatesProgress.json').write_text(json.dumps(results,indent=2))
if hasattr(unreal,'AssetCompilingManager'):unreal.AssetCompilingManager.finish_all_compilation()
(D/'MaterialCandidates.json').write_text(json.dumps(results,indent=2));unreal.log('PERF1_SPATIAL_CANDIDATES_READY')
