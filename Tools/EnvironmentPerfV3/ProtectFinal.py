# V5: current required-core guard; historical session algorithm is preserved below.
import os as _evidence_os, sys as _evidence_sys
from pathlib import Path as _EvidencePath
if _evidence_os.environ.get('POKEMONSTER_RUN_HISTORICAL_GUARD') != '1':
    _evidence_root = next(p for p in _EvidencePath(__file__).resolve().parents if (p/'PokeMonster.uproject').is_file())
    _evidence_sys.path.insert(0, str(_evidence_root/'Tools/DevelopmentEvidence'))
    from evidence import current_guard as _current_guard
    _current_guard()
from pathlib import Path
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV3';initial=json.loads((O/'InitialHashes.json').read_text());changed=[];missing=[]
for name,expected in initial.items():
 p=R/name
 if not p.exists():missing.append(name)
 elif p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()!=expected:changed.append(name)
out={'checked_initial_versionable_files':len(initial),'changed_initial_files':changed,'missing_initial_files':missing,'all_initial_versionable_files_byte_identical':not changed and not missing}
(O/'ProtectedFinal.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));assert not changed and not missing,'Preserve and investigate; never restore external changes'
