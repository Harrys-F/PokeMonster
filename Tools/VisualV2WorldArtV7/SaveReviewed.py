"""Save only the reviewed central map; no Save All."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtV7';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();w=E.get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert [p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()]==['/Game/Maps/Dev_TestMap_VisualV2']
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
current=scene(w);expected=json.loads((S/'CandidateScene.json').read_text())
for x in [current,expected]:
 for a in x['actors'].values():a['components'].sort(key=lambda c:c['name'])
assert current==expected;assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');(S/'AfterScene.json').write_text(json.dumps(current,indent=2));assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();unreal.log('WA7_REVIEWED_MAP_SAVED')
