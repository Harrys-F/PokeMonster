"""Explicit revision of this task's own uncommitted water assets; never a general reimport."""
import json,unreal
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GaradosWaterV2';previous=json.loads((D/'Import.json').read_text());prefix='/Game/Characters/Creatures/Garados/WaterV2/';assert len(previous['created'])==13 and all(p.startswith(prefix)for p in previous['created']);baseline=json.loads((D/'Baseline.json').read_text());assert not any('Content/Characters/Creatures/Garados/WaterV2/'in str(p)for p in baseline['files'])
code=(R/'Tools/GaradosWaterV2/ImportWater.py').read_text().replace("assert not unreal.EditorAssetLibrary.does_directory_exist(P)","assert unreal.EditorAssetLibrary.does_directory_exist(P)")
code=code.replace("assert not unreal.EditorAssetLibrary.does_asset_exist(folder+'/'+name);t=unreal.AssetImportTask()","assert folder+'/'+name+'.'+name in previous['created'];t=unreal.AssetImportTask()")
code=code.replace('replace_existing=False','replace_existing=True').replace("mesh=next(x for x in task(A/'Exports/WaterV2/Garados_SwimIdle_V2.fbx'","ui.set_editor_property('skeleton',profile.swim_mesh.skeleton);ui.skeletal_mesh_import_data.set_editor_property('update_skeleton_reference_pose',True)\n mesh=next(x for x in task(A/'Exports/WaterV2/Garados_SwimIdle_V2.fbx'")
code=code.replace("(D/'Import.json')","(D/'ImportFinal.json')").replace('swim_clearance_radius_cm=390.','swim_clearance_radius_cm=400.')
exec(compile(code,'OwnedGaradosWaterReimport','exec'))
