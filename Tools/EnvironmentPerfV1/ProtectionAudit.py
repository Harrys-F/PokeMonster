# V5: current required-core guard; historical session algorithm is preserved below.
import os as _evidence_os, sys as _evidence_sys
from pathlib import Path as _EvidencePath
if _evidence_os.environ.get('POKEMONSTER_RUN_HISTORICAL_GUARD') != '1':
    _evidence_root = next(p for p in _EvidencePath(__file__).resolve().parents if (p/'PokeMonster.uproject').is_file())
    _evidence_sys.path.insert(0, str(_evidence_root/'Tools/DevelopmentEvidence'))
    from evidence import current_guard as _current_guard
    _current_guard()
"""Hash every pre-task tracked/untracked file; never repair or overwrite discrepancies."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV1';before=json.loads((O/'ProtectedBefore.json').read_text());out={'initial_file_count':len(before),'unchanged':[],'intentional_changes':{},'unexpected_changes':{},'missing':[]};sha=lambda b:hashlib.sha256(b).hexdigest()
for name,v in before.items():
 p=R/name
 if not p.exists():out['missing'].append(name);continue
 b=p.read_bytes()
 if sha(b)==v['sha256']:out['unchanged'].append(name);continue
 if name in ['Docs/TECHNIK.md','Docs/ENTSCHEIDUNGEN.md'] and sha(b[:v['bytes']])==v['sha256']:
  out['intentional_changes'][name]={'append_only':True,'added_bytes':len(b)-v['bytes']};continue
 if name=='Source/PokeMonster/PokeMonster.Build.cs':
  reconstructed=b.replace(b'"RenderCore", ',b'').replace(b', "RenderCore"',b'')
  if sha(reconstructed)==v['sha256']:out['intentional_changes'][name]={'only_added_dependency':'RenderCore'};continue
 out['unexpected_changes'][name]={'before':v['sha256'],'after':sha(b)}
(O/'ProtectionAudit.json').write_text(json.dumps(out,indent=2));print({k:len(v) if isinstance(v,(dict,list)) else v for k,v in out.items()});assert not out['missing'] and not out['unexpected_changes'],'Unexpected change: inspect ProtectionAudit.json, do not restore automatically'
