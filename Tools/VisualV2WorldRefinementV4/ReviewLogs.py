"""Separate engine/external/fixture messages from exported functional test outcomes."""
from pathlib import Path
import re,json
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2WorldRefinementV4';out={}
for label in ['NativeBefore01','NativeAfter02','FullAutomationRelease','Editor03','Editor01_AuthoringAndPIE','NativeGameplay02','PairedMaterials01','SceneCostPair02','FreshFinalStandard02']:
 p=D/label/'Engine.log'
 if label=='Editor01_AuthoringAndPIE':p=D/'Editor01/Engine.log'
 if not p.exists():continue
 text=p.read_text(errors='replace');lines=text.splitlines();first=text.find('LogAutomationController: Display: Test Started.');conditions=[m.start()for m in re.finditer('LogAutomationTest: Error: Condition failed',text)]
 iOS=[l for l in lines if 'idevice_id'in l or'Bad CPU type'in l];fatal=[l for l in lines if re.search(r'Fatal error:|Unhandled Exception:|Assertion failed:',l)];own=[l for l in lines if 'WR4_'in l and re.search(r'Warning:.*(?:Material|shader)|Failed to compile Material',l,re.I)];legacy=[l for l in lines if 'MI_WLA_LeafOak'in l and('Warning'in l or'Error'in l)]
 out[label]=dict(log=str(p),ios_helper_lines=len(iOS),ios_examples=iOS[:3],fatal_lines=len(fatal),fatal_examples=fatal[:3],own_v4_shader_warning_lines=len(own),own_examples=own[:3],existing_leaf_material_warning_lines=len(legacy),existing_leaf_examples=legacy[:3],python_error_lines=sum('LogPython: Error:'in l for l in lines),condition_failed_lines=len(conditions),condition_failed_before_project_queue=sum(x<first for x in conditions)if first>=0 else None,toolset_startup_present='has no attribute \'ToolsetDefinition\''in text or'has no attribute \'PythonTestRunner\''in text,project_test_export_is_authoritative='FullAutomationRelease/Report/index.json',raw_log_is_not_claimed_clean=True)
 for key in ['fatal_lines','own_v4_shader_warning_lines']:
  if label in ['NativeAfter02','Editor03','NativeGameplay02','FreshFinalStandard02']:assert out[label][key]==0,(label,key,out[label])
out['rejected_diagnostic']=json.loads((D/'SceneCostPair01/DiagnosticRejected.json').read_text());out['authoring_failures_corrected']=['Initial mask sampler Color/Masks mismatch: fixed before binding, final graph recompiles passed','Repeated plaster/ripple appearance rejected in real images and revised','Initial two Wald photos placed below raised ground: fixture corrected and all 21 repeated','GeometryAudit initial non-grid probes corrected; final actual collision rays and route preservation pass']
(D/'RawLogReview.json').write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({k:{n:v[n]for n in ['fatal_lines','own_v4_shader_warning_lines','ios_helper_lines','python_error_lines','condition_failed_lines']}for k,v in out.items()if isinstance(v,dict)and'fatal_lines'in v},indent=2))
