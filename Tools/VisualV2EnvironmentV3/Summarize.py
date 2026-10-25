"""Record actual results, including the deliberately non-passing strict warning wrapper."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/EnvironmentV3';auto=json.loads((R/'Saved/ProjectRefinement/EnvironmentV3Automation/Report/index.json').read_text(encoding='utf-8-sig'));warnings=[]
for t in auto['tests']:
 for e in t.get('entries',[]):
  v=e.get('event',{})
  if v.get('type')in ['Warning','Error']:warnings.append({'test':t['fullTestPath'],**v})
assert auto['failed']==auto['notRun']==auto['inProcess']==0
foot=json.loads((D/'FootrunFinal/Result.json').read_text());assert foot['passed']and foot['save_unchanged'];pairs=json.loads((D/'Comparisons.json').read_text());assert len(pairs)==14;maps=json.loads((D/'MapCheckResults.json').read_text());assert len(maps)==12 and all(x['errors']==x['warnings']==0 for x in maps)
log=(D/'EditorFinal.log').read_text(errors='replace');assert not any(x in log for x in ['Failed to compile Material','Default Material will be used in game'])
v={'base_head':json.loads((D/'Baseline.json').read_text())['head'],'scope':json.loads((D/'ScopeValidation.json').read_text()),'editor_build':json.loads((R/'Saved/ProjectRefinement/EnvironmentV3Build02/Result.json').read_text()),'automation':{k:auto[k]for k in ['succeeded','succeededWithWarnings','failed','notRun','inProcess']},'automation_engine_exit':0,'strict_qa_wrapper_exit':1,'warnings':warnings,'map_checks':maps,'footrun':{k:v for k,v in foot.items()if k!='checks'},'footrun_steps':len(foot['checks']),'qhd_pairs':14,'quality':json.loads((D/'VerifiedFinal/Result.json').read_text())['quality_cvars'],'motion':json.loads((D/'MotionFinal/Videos.json').read_text()),'fresh_editor_material_fallbacks':0,'hardware_controller_retested':False,'performance_benchmark':False,'remaining':['Dark character at some canopy edges; existing targeted character fill retained; 1.35 global fill trial not adopted.','Existing foliage/card shapes, fine texture repetition and screen-space reflection limits remain.','Art approval remains with user.']}
(R/'Tools/VisualV2EnvironmentV3/Acceptance.json').write_text(json.dumps(v,indent=2)+'\n');print(v['automation'])
