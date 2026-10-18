"""Read-only QA of the map supplied on the editor command line. Never changes or saves it."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2TAAIntegrationV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world()
assert w and not E.get_game_world()
name=w.get_name();assert name in ['Dev_TestMap_VisualV2','Dev_TestMap_VisualV2GPUBottleneckV1','Dev_WestlandAssetLibrary']
if name in ['Dev_TestMap_VisualV2','Dev_TestMap_VisualV2GPUBottleneckV1']:
 sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
 current=scene(w)
 if name=='Dev_TestMap_VisualV2':assert current==json.loads((O/'AfterScene.json').read_text())
 else:assert json.loads(json.dumps(current).replace('Dev_TestMap_VisualV2GPUBottleneckV1','Dev_TestMap_VisualV2'))==json.loads((O/'BeforeScene.json').read_text())

unreal.SystemLibrary.execute_console_command(w,'MAP CHECK')
state={'map':w.get_path_name(),'scene_unchanged':name!='Dev_WestlandAssetLibrary','dirty_maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
assert not state['dirty_maps'] and not state['dirty_content']
(O/'MapChecks').mkdir(exist_ok=True);(O/'MapChecks'/(name+'.json')).write_text(json.dumps(state,indent=2))
