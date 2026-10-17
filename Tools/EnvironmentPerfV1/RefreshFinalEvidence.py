# V5 optional evidence gate: no gameplay/build validation is skipped here.
import sys as _evidence_sys
from pathlib import Path as _EvidencePath
_evidence_root = next(p for p in _EvidencePath(__file__).resolve().parents if (p/'PokeMonster.uproject').is_file())
_evidence_sys.path.insert(0, str(_evidence_root/'Tools/DevelopmentEvidence'))
from evidence import review_preflight as _review_preflight
_review_preflight(__file__)
"""Refresh only our manifest-verified final audit copies; never touch original project assets."""
from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV1';A=R/'Art/World/EnvironmentPerfV1/Review';m=A/'EvidenceManifest.json';old={x['path']:x for x in json.loads(m.read_text())}
for name in ['ProtectionAudit.json','FinalGitChecks.json']:
 src=O/name;dst=A/'Data'/name
 if dst.exists():
  key=str(dst.relative_to(R));assert key in old and hashlib.sha256(dst.read_bytes()).hexdigest()==old[key]['sha256']
 shutil.copy2(src,dst)
rows=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(A.rglob('*')) if p.is_file() and p!=m]
m.write_text(json.dumps(rows,indent=2));print('Final evidence manifest:',len(rows),'files')
