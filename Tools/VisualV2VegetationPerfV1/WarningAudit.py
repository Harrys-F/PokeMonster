"""Classify all final rendering logs; preserve pre-existing Engine Toolset failures."""
from pathlib import Path
import re,json
from collections import Counter
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2VegetationPerfV1';O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18')
paths=[O/'Editor2.log',O/'Editor3.log']+sorted(S.glob('VGB1_Vegetation_Standalone_C[1-8]_Engine.log'))+sorted((S/'Acceptance').glob('*/Engine.log'));assert len(paths)==12
base=R/'Saved/VisualV2AASoftShadowsV1/VGB1_AASoftShadows_Standalone_C1_Engine.log'
def errors(p):return Counter(x.split('LogPython: Error:',1)[-1].strip() for x in p.read_text(errors='replace').splitlines() if 'LogPython: Error:' in x)
known=errors(base);assert sum(known.values())==58
patterns={'fatal':r'appError called|Fatal error:|Caught signal|Assertion failed:','shader_material_compile':r'Failed to compile Material|LogMaterial: Error|LogShaderCompilers: Error','instancing_fallback':r'not marked for usage with instanced static meshes|was not compiled with bUsedWithInstancedStaticMeshes|will be rendered using the default material','probe_failure':r'VegPerf requires|Missing VegPerf candidate|MapTAA expected one|MapTAA control requires'}
rows=[]
for p in paths:
 text=p.read_text(errors='replace');counts={n:len(re.findall(v,text,re.I)) for n,v in patterns.items()};assert not any(counts.values()),(str(p),counts)
 expected=Counter() if p.parent==O else known;actual=errors(p);assert actual==expected,(str(p),'Unexpected Python errors',actual-expected)
 general=[x for x in text.splitlines() if re.search(r'\bWarning:|\bError:',x)];rows.append({'log':str(p),'critical_counts':counts,'known_native_toolset_error_lines':sum(expected.values()),'new_python_error_lines':0,'all_warning_error_lines':general})
result={'final_logs':rows,'all_final_rendering_error_checks_passed':True,'baseline_native_error_fingerprint':dict(known),'baseline_log':str(base),'does_not_claim_all_historical_logs_warning_free':True,'preserved_preparation_failures':['Initial Inventory Custom.code property access','Initial slot-log/segment association in analyzer','Initial source-atlas quadrant dimension assumption corrected before use','Concurrent CPU source analysis invalidated original whole PIE C1; repeated as CRecheck1','Initial real-input motion telemetry had no images due recorder output-root guard; four new R2 recordings completed using guarded existing recorder root','Initial debug screenshot filenames one mode late due deferred Shot; complete separate R2 diagnostic repeated']}
(O/'WarningAudit.json').write_text(json.dumps(result,indent=2));print('Final rendering audit PASS',len(rows),'logs; known native Toolset errors preserved')
