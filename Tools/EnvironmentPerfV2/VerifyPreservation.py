# V5: current required-core guard; historical session algorithm is preserved below.
import os as _evidence_os, sys as _evidence_sys
from pathlib import Path as _EvidencePath
if _evidence_os.environ.get('POKEMONSTER_RUN_HISTORICAL_GUARD') != '1':
    _evidence_root = next(p for p in _EvidencePath(__file__).resolve().parents if (p/'PokeMonster.uproject').is_file())
    _evidence_sys.path.insert(0, str(_evidence_root/'Tools/DevelopmentEvidence'))
    from evidence import current_guard as _current_guard
    _current_guard()
"""Run after graphics benchmarks; never repair/reset/delete a mismatch."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV2';before=json.loads((O/'ProtectedBefore.json').read_text());changed=[];missing=[]
for name,v in before.items():
 p=R/name
 if not p.is_file():missing.append(name);continue
 if p.stat().st_size!=v['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=v['sha256']:changed.append(name)
save=R/'Saved/SaveGames/PokeMonster_Dev.sav';backup=O/'PokeMonster_Dev_Original.sav';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out={'protected_files_checked':len(before),'changed_preexisting_files':changed,'missing_preexisting_files':missing,'all_preexisting_files_byte_identical':not changed and not missing,'original_dev_save_sha256':sha(backup),'current_dev_save_sha256':sha(save),'save_byte_identical':sha(save)==sha(backup)}
(O/'ProtectedFinal.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));assert out['all_preexisting_files_byte_identical'] and out['save_byte_identical'],'Preserve mismatch; no automatic reset'
