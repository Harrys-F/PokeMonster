"""Explicit authorized deletion of the exact unwanted, now unreferenced Raichu asset set."""
import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/RaichuMeshyCorrection';P='/Game/Characters/Creatures/Raichu/V4';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();reg=unreal.AssetRegistryHelpers.get_asset_registry();reg.search_all_assets(True);opts=unreal.AssetRegistryDependencyOptions(include_soft_package_references=True,include_hard_package_references=True,include_searchable_names=True,include_soft_management_references=True,include_hard_management_references=True)
s=unreal.load_asset('/Game/Data/Creatures/DA_Raichu');p=s.get_visuals().presentation;assert p.get_path_name().startswith('/Game/Characters/Creatures/Raichu/MeshyV1/');assert not p.get_validation_errors();assets=list(reg.get_assets_by_path(P,True));plan=json.loads((D/'RemovalPlan.json').read_text());expected={str((R/x['path']).resolve())for x in plan if x['path'].startswith('Content/')};actual={str((R/'Content'/(str(a.package_name)[6:]+'.uasset')).resolve())for a in assets};assert actual==expected,(actual^expected)
for a in assets:
 name=str(a.package_name);external=[str(x)for x in reg.get_referencers(name,opts)if not str(x).startswith(P+'/')];assert not external,(name,external)
for x in plan:
 if x['path'].startswith('Content/'):assert hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256']
assert len(assets)==16;assert unreal.EditorAssetLibrary.delete_loaded_assets([a.get_asset()for a in assets]),'Authorized batch deletion failed'
assert not list(reg.get_assets_by_path(P,True));assert not list((R/'Content/Characters/Creatures/Raichu/V4').rglob('*.uasset'));assert not p.get_validation_errors();assert s.get_visuals().presentation==p
(D/'AssetDeletion.json').write_text(json.dumps({'removed':[str(a.package_name)for a in assets],'count':len(assets),'external_references_before_delete':[],'active_mesh':p.mesh.get_path_name(),'filesystem_old_uassets_remaining':False},indent=2));print('UNWANTED_RAICHU_ASSETS_DELETED',len(assets))
