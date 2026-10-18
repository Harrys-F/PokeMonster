"""Do not suppress engine errors: distinguish scope and preserve exact warning lines."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2MaterialFixV1'
logs=list(S.glob('VGB1_MaterialFix_*_Standalone_C*_Engine.log'))+[S/'Automation/Engine.log',S/'Cook/Engine.log']
result=[]
for p in sorted(logs):
 assert p.is_file(),p
 lines=p.read_text(errors='replace').splitlines();after='_After_' in p.name
 usage=[l for l in lines if 'missing usage flag InstancedStaticMeshes' in l]
 shader=[l for l in lines if re.search(r'Log(?:Material|Shaders|ShaderCompilers|Metal|Renderer):\s*(Error|Fatal)',l) or 'Failed to compile Material' in l]
 fatal=[l for l in lines if 'Critical error:' in l or 'Fatal error:' in l]
 all_warnings=[l for l in lines if re.search(r': (Warning|Error|Fatal):',l)]
 if after:assert not usage and not shader and not fatal,p
 result.append({'log':str(p),'is_after_native':after,'instancing_warning_lines':usage,'shader_error_lines':shader,'fatal_lines':fatal,'all_warning_error_lines':all_warnings})
assert len([r for r in result if r['is_after_native']])==8
(S/'WarningAudit.json').write_text(json.dumps(result,indent=2));print('All eight fresh corrected native sessions have no instancing fallback or shader/fatal errors')
