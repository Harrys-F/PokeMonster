# V5 optional evidence gate: no gameplay/build validation is skipped here.
import sys as _evidence_sys
from pathlib import Path as _EvidencePath
_evidence_root = next(p for p in _EvidencePath(__file__).resolve().parents if (p/'PokeMonster.uproject').is_file())
_evidence_sys.path.insert(0, str(_evidence_root/'Tools/DevelopmentEvidence'))
from evidence import review_preflight as _review_preflight
_review_preflight(__file__)
"""Preserve genuine captures and reproducible counters after all timing is complete."""
from pathlib import Path
import json,shutil,zipfile,hashlib
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV2';D=R/'Art/World/EnvironmentPerfV2/Review';assert not D.exists(),'Do not overwrite prior review evidence'
for label in ['FinalPairedPIE']+['StandalonePair'+str(i) for i in range(1,7)]+['SustainedQHD']:
 assert (O/(label+'_Done.txt')).read_text()=='Complete',label
D.mkdir(parents=True);screens=D/'Screenshots';screens.mkdir();sources=[]
for i in [0,3,4,7,8,11,12,15]:sources+=list((O/'Screenshots/LightingCandidatesQHD').glob(str(i).zfill(2)+'_*.png'))
sources+=list((O/'Screenshots/FinalExteriorQHD').glob('*.png'))
for pattern in ['Interior_V*_QHD*.png','Native_Dorf*.png','Native_DichterWald*.png','Native_BachBruecke*.png','Native_Ruinen*.png','Native_CrownReveal_On*.png','Native_Heilhaus*.png','Ranger_Conversation*.png']:
 sources+=list((O/'FootTest').glob(pattern))
records=[]
for p in sorted(set(sources)):
 name=p.parent.name+'_'+p.name;t=screens/name;assert not t.exists();shutil.copy2(p,t);records.append({'source':str(p.relative_to(R)),'review':str(t.relative_to(R)),'synthetic':False})
for name in ['Measurements.json','MeasurementsResolved.json','MeasurementSelection.json','MetricTables.md','FactorPairs.json','MeasurementValidation.json','StrictValidation.json','SustainedAnalysis.json','EngineEvidence.json','GPUProfile_QHD_Verified.txt','GPUCaptureVerified_Proof.json','HostContext.json','FinalMapAudit.json','MapCheck.json','PersistedCandidate.json','SelectedCandidate.json','DevSaveRestored.json','FootProfileActive.json','FootSessionAfter.json','ProtectedFinal.json','CubeGroundAudit.json','GitBefore.txt']:
 assert (O/name).is_file(),name;shutil.copy2(O/name,D/name)
shutil.copy2(O/'FootTest/FootTest.json',D/'FootTest.json');shutil.copy2(O/'FootTest/FootProgress.json',D/'FootProgress.json')
for p in [O/'Screenshots/LightingCandidatesQHD/Review.json',O/'Screenshots/FinalExteriorQHD/Review.json']:shutil.copy2(p,D/(p.parent.name+'_Review.json'))
for name in ['Build_FinalProfile.log','Build_WindowValidationFixed.log','AutomationExit.json','AutomationFinalExit.json']:shutil.copy2(O/name,D/name)
if (O/'AutomationFinal/index.json').exists():shutil.copy2(O/'AutomationFinal/index.json',D/'Automation.json')
raw=[]
for pattern in ['*_Frames.csv','*_Segments.csv','*_Settings.txt','*_Done.txt','*_Launch.json']:
 raw+=list(O.glob(pattern))
raw += [O/'Thermal.jsonl',O/'ThermalRepair.jsonl',O/'FootTest/FootFrames.jsonl']
raw += list((R/'Saved/Profiling/CSV').glob('ENV2_*.csv'))
for name in ['Automation.log','AutomationFinal.log','Build_WindowValidation.log','Build_WindowValidationFixed.log','EditorSession_FinalReview.log','EditorSession_FinalProfile.log','PacingWindowed.log','PacingFullscreen.log']+[f'StandalonePair{i}.log' for i in range(1,7)]+['SustainedQHD.log','RepairNative1.log','RepairNative2.log','RepairNativeHighDorf.log']:
 raw.append(O/name)
with zipfile.ZipFile(D/'RawMeasurements.zip','x',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for p in sorted(set(raw)):
  assert p.is_file(),p;z.write(p,str(p.relative_to(R)))
(D/'Screenshots.json').write_text(json.dumps(records,indent=2))
manifest=[]
for p in sorted(D.rglob('*')):
 if p.is_file():manifest.append({'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(D/'EvidenceManifest.json').write_text(json.dumps(manifest,indent=2));print(len(manifest)+1,'files;',round(sum(r['bytes'] for r in manifest)/1024**2,2),'MiB;',len(records),'screenshots')
