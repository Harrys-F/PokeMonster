"""Only reject this task's unused drafts after checking on-disk referencers."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
b=json.loads((D/'Baseline.json').read_text());root='/Game/Environment/VisualV2PerformanceV1/';names=['Materials/M_PV1_Ground','Materials/M_PV1_MainPath','Materials/M_PV1_NorthPath','Materials/M_PV1_BakedGround','Textures/T_PV1_RouteField','Textures/T_PV1_GroundColor'];paths=[root+n for n in names];rows=[]
for p in paths:
 file='Content/'+p.removeprefix('/Game/')+'.uasset';assert file not in b['files'] and (R/file).is_file()
 refs=list(unreal.EditorAssetLibrary.find_package_referencers_for_asset(p,True));assert all(x in paths for x in refs),(p,refs);rows.append({'asset':p,'file':file,'referencers':refs,'original_protected_file':False})
for f in ['Art/World/VisualV2PerformanceV1/GroundColor.png','Art/World/VisualV2PerformanceV1/RouteField.png']:assert f not in b['files'] and (R/f).is_file()
(D/'RejectedDraftDependencies.json').write_text(json.dumps(rows,indent=2));unreal.log('PERF1_REJECTED_DRAFTS_HAVE_NO_PRODUCTION_REFERENCERS')
