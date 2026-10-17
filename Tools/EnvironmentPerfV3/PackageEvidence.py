# V5 optional evidence gate: no gameplay/build validation is skipped here.
import sys as _evidence_sys
from pathlib import Path as _EvidencePath
_evidence_root = next(p for p in _EvidencePath(__file__).resolve().parents if (p/'PokeMonster.uproject').is_file())
_evidence_sys.path.insert(0, str(_evidence_root/'Tools/DevelopmentEvidence'))
from evidence import review_preflight as _review_preflight
_review_preflight(__file__)
"""Run only after timing and gameplay tests; preserve all source captures under Saved."""
from pathlib import Path
import json,shutil,zipfile,hashlib
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV3';D=R/'Art/World/EnvironmentPerfV3/Review'
assert (O/'ReviewAndFootDone.txt').read_text()=='Complete';assert not D.exists();D.mkdir(parents=True);S=D/'Screenshots';S.mkdir()
sources=list((O/'Screenshots').glob('Baseline_*/*.png'))
for i in [0,2,3,4,5,7,9,10,11,12,14,16,17,18,19]:sources+=list((O/'Screenshots/CandidatesQHD').glob(str(i).zfill(2)+'_*.png'))
for pattern in ['Native_Dorf*.png','Native_DichterWald*.png','Native_Heilhaus*.png','Native_CrownReveal_On*.png','Ranger_Conversation*.png','Interior_V*_QHD*.png']:sources+=list((O/'FootTest').glob(pattern))
manifest=[]
for p in sorted(set(sources)):
 target=S/(p.parent.name+'_'+p.name);assert not target.exists();shutil.copy2(p,target);manifest.append({'source':str(p.relative_to(R)),'review':str(target.relative_to(R)),'synthetic':False})
(D/'Screenshots.json').write_text(json.dumps(manifest,indent=2))
for name in ['InitialHEAD.txt','InitialStatus.txt','EditorDiskComparison.json','MapCopy.json','VegetationLightingAudit.json','RuntimeMaterialAudit.json','DiscoveryPairs.json','Measurements.json','PairedMetrics.json','MetricTables.md','MatrixValidation.json','PersistedState.json','FinalMapAudit.json','FootProfileActive.json','FootSessionAfter.json','DevSaveRestored.json','ProtectedFinal.json','MapCheck.json','Build_Initial.log','Build_MinLOD.log','AutomationExit.json']:
 assert (O/name).is_file(),name;shutil.copy2(O/name,D/name)
shutil.copy2(O/'FootTest/FootTest.json',D/'FootTest.json');shutil.copy2(O/'FootTest/FootProgress.json',D/'FootProgress.json');shutil.copy2(O/'Automation/index.json',D/'Automation.json')
raw=[]
for pat in ['*_Frames.csv','*_Segments.csv','*_Settings.txt','*_Done.txt','*_Launch.json']:raw+=list(O.glob(pat))
raw+=[O/'Thermal.jsonl',O/'FootTest/FootFrames.jsonl'];raw+=list((R/'Saved/Profiling/CSV').glob('ENV3_*.csv'));raw+=list((O/'Screenshots').glob('*/Review.json'))
with zipfile.ZipFile(D/'RawMeasurements.zip','x',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for p in sorted(set(raw)):assert p.is_file(),p;z.write(p,str(p.relative_to(R)))
(D/'EvidenceManifest.json').write_text(json.dumps([{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(D.rglob('*')) if p.is_file()],indent=2))
print('Preserved genuine screenshots',len(manifest),'raw files',len(raw))
