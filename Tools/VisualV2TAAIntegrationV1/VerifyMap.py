import unreal,json,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2TAAIntegrationV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2' and not e.get_game_world()
scene=runpy.run_path(str(R/'Tools/VisualV2QualityV2/AuditScene.py'))['scene'];after=scene(w);assert after==json.loads((S/'AfterScene.json').read_text()),'Saved map differs on reopening'
outside=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PostProcessVolume) if a.get_actor_label()=='V2_OutdoorExposure');a=outside.settings.weighted_blendables.array;assert len(a)==1 and isinstance(a[0].object,unreal.PokeMonsterTemporalAABlendable) and a[0].weight==1
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();d=json.loads((S/'MapChangeAudit.json').read_text());d['reopened']=True;d['reopened_scene_equal']=True;(S/'MapChangeAudit.json').write_text(json.dumps(d,indent=2));unreal.log('VTA1_REOPENED_IDENTICAL')
