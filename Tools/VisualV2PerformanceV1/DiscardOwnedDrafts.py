"""Explicit bounded removal of this task's rejected drafts only. Never original inputs."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()
rows=json.loads((D/'RejectedDraftDependencies.json').read_text());allowed={x['asset']for x in rows};assert len(allowed)==6 and all(x.startswith('/Game/Environment/VisualV2PerformanceV1/')for x in allowed)
for row in rows:
 refs=list(unreal.EditorAssetLibrary.find_package_referencers_for_asset(row['asset'],True));assert all(x in allowed for x in refs),(row,refs)
removed=[]
for row in rows:
 assert unreal.EditorAssetLibrary.delete_asset(row['asset']);removed.append(row['file'])
for f in ['Art/World/VisualV2PerformanceV1/GroundColor.png','Art/World/VisualV2PerformanceV1/RouteField.png']:
 p=R/f;assert not p.is_symlink();p.unlink();removed.append(f)
(D/'DiscardedOwnedDrafts.json').write_text(json.dumps({'removed':removed,'original_files_removed':0,'no_mixed_folder_deleted':True},indent=2))
