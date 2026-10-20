"""Load every existing map, request Map Check, and preserve the Ranger V3 regression audit."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ArtPassV4';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world() and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();rows=[]
for p in sorted((R/'Content/Maps').glob('*.umap')):
 path='/Game/Maps/'+p.stem;assert unreal.EditorLoadingAndSavingUtils.load_map(path);w=E.get_editor_world();unreal.log('ART_V4_MAPCHECK_BEGIN '+path);unreal.SystemLibrary.execute_console_command(w,'MAP CHECK');unreal.log('ART_V4_MAPCHECK_END '+path);rows.append({'map':path,'actors':len(unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor))});assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
 if p.stem=='Dev_TestMap_NPCMotionV3':
  source=(R/'Tools/RangerAnimationV3/FinalMapAudit.py').read_text().replace("O=R/'Saved/RangerAnimationV3'","O=R/'Saved/ArtPassV4'");exec(compile(source,'existing_Ranger_V3_regression','exec'),{'__name__':'__main__'})
assert len(rows)==11;assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2');(S/'MapChecksRequested.json').write_text(json.dumps(rows,indent=2));unreal.log('ART_V4_ALL_MAPCHECKS_REQUESTED')
