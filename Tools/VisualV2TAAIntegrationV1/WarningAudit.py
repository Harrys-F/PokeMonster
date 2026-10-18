"""Preserve raw logs, classify final rendering failures separately from setup failures."""
from pathlib import Path
import json,re
from collections import Counter
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2TAAIntegrationV1';O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18')
paths=[O/'Editor3.log']+sorted(S.glob('VGB1_TAAIntegration_Standalone_C[1-6]_Engine.log'))+sorted(S.glob('VGB1_TAAIntegration_Standalone_CRecheck[2-5]_Engine.log'))+sorted((S/'Acceptance').glob('*/Engine.log'))
assert len(paths)==13
patterns={'fatal':r'appError called|Fatal error:|Caught signal|Assertion failed:','python_error':r'LogPython: Error','shader_material_compile':r'Failed to compile Material|LogMaterial: Error|LogShaderCompilers: Error','instancing_fallback':r'not marked for usage with instanced static meshes|was not compiled with bUsedWithInstancedStaticMeshes|will be rendered using the default material','aa_control_failure':r'MapTAA expected one|MapTAA control requires'}
baseline=R/'Saved/VisualV2AASoftShadowsV1/VGB1_AASoftShadows_Standalone_C1_Engine.log'
def python_errors(p):return Counter(x.split('LogPython: Error:',1)[-1].strip() for x in p.read_text(errors='replace').splitlines() if 'LogPython: Error:' in x)
base_errors=python_errors(baseline);assert sum(base_errors.values())==58
rows=[]
for p in paths:
 text=p.read_text(errors='replace');counts={n:len(re.findall(v,text,re.I)) for n,v in patterns.items()};general=[x for x in text.splitlines() if re.search(r'\bWarning:|\bError:',x)];rows.append({'log':str(p),'critical_counts':counts,'warning_error_line_count':len(general),'general_examples':general[:12]})
 expected=Counter() if p==O/'Editor3.log' else base_errors
 actual=python_errors(p);assert actual==expected,(p,'New Python error fingerprint',actual-expected)
 rows[-1].update(known_baseline_native_toolset_error_lines=sum(expected.values()),new_python_error_lines=0)
 assert all(v==0 for n,v in counts.items() if n!='python_error'),(p,counts)
result={'final_engine_logs':rows,'all_final_rendering_error_checks_passed':True,'preserved_failed_preparations':['Automation_InitialFixtureFailure','Initial C1 photograph inventory','Sandbox video-encoder startup; successful authorized retry'],'does_not_claim_all_historical_logs_warning_free':True,'baseline_native_plugin_log':str(baseline),'baseline_native_toolset_error_lines':58,'baseline_error_fingerprint':dict(base_errors)};(O/'WarningAudit.json').write_text(json.dumps(result,indent=2));print('Final logs checked',len(rows),'no new task/rendering failures; known 58-line native engine-toolset Python fingerprint and generic messages preserved')
