"""Only three VisualV2 material assignments. Geometry, collision and all source materials unchanged."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2StabilityV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();W=E.get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
before=scene(W);old='/Game/Environment/Prototype2D/Materials/M_PaintedGround.M_PaintedGround';target=unreal.load_asset('/Game/Environment/VisualV2EnvironmentV3/Materials/M_EQ3_Ground');rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.StaticMeshActor):
 if a.get_actor_label()not in ['Hill_Step_Low','Hill_Step_Mid','Hill_Lookout']:continue
 c=a.static_mesh_component;assert c.get_material(0).get_path_name()==old;a.modify();c.modify();c.set_material(0,target);rows.append(a.get_name())
assert len(rows)==3;after=scene(W)
for name in before['actors']:
 if name not in rows:assert before['actors'][name]==after['actors'][name],name
 else:
  expected=json.loads(json.dumps(before['actors'][name]));expected['components'][0]['materials']=[target.get_path_name()];assert after['actors'][name]==expected,name
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2');assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
(D/'SurfaceFix.json').write_text(json.dumps({'actors':rows,'old':old,'new':target.get_path_name(),'exact_scene_difference':'Only material slot 0 on the three retained raised walking platforms','shared_assets_saved':False},indent=2));(D/'AfterScene.json').write_text(json.dumps(after,indent=2))
