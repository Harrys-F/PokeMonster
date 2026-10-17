# V5 optional evidence gate: no gameplay/build validation is skipped here.
import sys as _evidence_sys
from pathlib import Path as _EvidencePath
_evidence_root = next(p for p in _EvidencePath(__file__).resolve().parents if (p/'PokeMonster.uproject').is_file())
_evidence_sys.path.insert(0, str(_evidence_root/'Tools/DevelopmentEvidence'))
from evidence import review_preflight as _review_preflight
_review_preflight(__file__)
"""Copy only this task's evidence to a durable review folder; preserve raw originals."""
from pathlib import Path
import json,shutil,zipfile,hashlib
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV1';A=R/'Art/World/EnvironmentPerfV1/Review'
assert (O/'StandalonePair6_Done.txt').read_text()=='Complete'
A.mkdir(parents=True,exist_ok=True)
def copy(src,dst):
 dst.parent.mkdir(parents=True,exist_ok=True)
 if dst.exists():
  assert dst.read_bytes()==src.read_bytes(),str(dst)+' already contains different evidence'
 else:shutil.copy2(src,dst)
for f in (O/'Screenshots/QHD_FinalComparison').glob('*'):
 if f.is_file():copy(f,A/'Screenshots'/f.name)
for f in (O/'FootTest').glob('*'):
 if f.suffix.lower() in ['.png','.json']:copy(f,A/'FootTest'/f.name)
for name in ['Measurements.json','MetricTables.md','FactorPairs.json','MeasurementValidation.json','EditorAudit.json','VegetationAudit.json','PersistedCandidate.json','FinalMapAudit.json','MapCheckLog.json','ProtectionAudit.json','DevSaveRestored.json','FootProfileActive.json','FootSessionBefore.json','FootSessionAfter.json','Build_FinalProfile.log','AutomationExit.json','Thermal.jsonl','StrictValidation.json','MapCheckLog_Reopened.json','FinalEditorState.json','WarningsSummary.md']:
 copy(O/name,A/'Data'/name)
copy(O/'Automation/index.json',A/'Data/AutomationIndex.json')
archive=A/'Data/RawMeasurements.zip';assert not archive.exists(),'Do not overwrite earlier archives'
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=3) as z:
 z.write(O/'Automation.log','Automation.log')
 for glob in ['*_Frames.csv','*_Segments.csv','*_Settings.txt','*_Launch.json','RuntimeSettings.jsonl']:
  for p in sorted(O.glob(glob)):z.write(p,'EnvironmentPerfV1/'+p.name)
 for p in sorted((R/'Saved/Profiling/CSV').glob('ENV1_*.csv')):z.write(p,'UnrealCSV/'+p.name)
rows=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(A.rglob('*')) if p.is_file()]
(A/'EvidenceManifest.json').write_text(json.dumps(rows,indent=2))
print('Archived',len(rows),'files,',sum(p['bytes'] for p in rows),'bytes')
