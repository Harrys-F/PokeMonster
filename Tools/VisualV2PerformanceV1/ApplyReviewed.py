"""Save only the four reviewed VisualV2 floor material bindings.
All actors, transforms, collisions, instances, lights and postprocess compare equal.
"""
import unreal,json,sys,copy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world()
assert not E.get_game_world() and W.get_name()=='Dev_TestMap_VisualV2'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert not (D/'Applied.json').exists()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
before=scene(W);source='/Game/Environment/VisualV2EnvironmentV3/Materials/M_EQ3_Ground.M_EQ3_Ground';path='/Game/Environment/VisualV2PerformanceV1/Materials/M_PV1_BakedGroundSRGB';m=unreal.load_asset(path);assert m
expected={'V2_Ground','Hill_Step_Low','Hill_Step_Mid','Hill_Lookout'};changed=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  for i in range(c.get_num_materials()):
   old=c.get_material(i)
   if old and old.get_path_name()==source:
    assert a.get_actor_label() in expected and i==0
    c.set_material(i,m);changed.append({'actor':a.get_name(),'label':a.get_actor_label(),'component':c.get_name(),'slot':i,'old':source,'new':m.get_path_name()})
assert len(changed)==4 and {x['label']for x in changed}==expected
after=scene(W);normalized=copy.deepcopy(after)
for x in changed:
 row=normalized['actors'][x['actor']];cr=next(c for c in row['components']if c['name']==x['component']);assert cr['materials'][0]==x['new'];cr['materials'][0]=x['old']
assert normalized==before,'Unexpected scene change outside the four material slots'
assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2')
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(D/'AfterScene.json').write_text(json.dumps(after,indent=2));(D/'Applied.json').write_text(json.dumps({'bindings':changed,'only_four_material_slots':True,'all_other_audited_scene_properties_equal':True},indent=2));unreal.log('PERF1_REVIEWED_BINDINGS_SAVED')
