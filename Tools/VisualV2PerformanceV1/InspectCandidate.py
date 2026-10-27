import unreal,json
from pathlib import Path
D=Path(unreal.Paths.project_dir())/'Saved/ProjectRefinement/VisualV2PerformanceV1';m=unreal.load_asset('/Game/Environment/VisualV2PerformanceV1/Materials/M_PV1_Ground');src=unreal.load_asset('/Game/Environment/VisualV2EnvironmentV3/Materials/M_EQ3_Ground');rows=[]
for x in unreal.ObjectIterator(unreal.MaterialExpressionCustom):
 if any(s in x.get_path_name()for s in ['M_PV1_Ground','M_EQ3_Ground']):rows.append({'path':x.get_path_name(),'outer':x.get_outer().get_path_name(),'has_route':'W6Route'in x.get_editor_property('code'),'code_chars':len(x.get_editor_property('code'))})
(D/'CandidateInspection.json').write_text(json.dumps({'candidate':m.get_path_name()if m else None,'nodes':rows,'dirty_maps':[x.get_path_name()for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[x.get_path_name()for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]},indent=2))
