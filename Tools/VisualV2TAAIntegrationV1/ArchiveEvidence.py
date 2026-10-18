"""Copy only this task's local proof outside Git; hash every copy. No deletion."""
from pathlib import Path
import shutil,hashlib,json,zipfile
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2TAAIntegrationV1';O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18');D=O/'Evidence';assert not D.exists();D.mkdir();pairs=[]
for p in sorted(S.rglob('*')):
 if not p.is_file() or any(n in p.relative_to(S).parts for n in ['VideoSources']):continue
 if p.name=='EncodeRecording':continue
 pairs.append((p,D/p.relative_to(S)))
for p in sorted((R/'Saved/EnvironmentPerfV2').glob('VGB1_TAAIntegration_*')):
 if p.is_file():pairs.append((p,D/'RawProbe'/p.name))
for p in sorted((R/'Saved/Profiling/CSV').glob('ENV2_VGB1_TAAIntegration_*.csv')):pairs.append((p,D/'ProfilingCSV'/p.name))
manifest=[]
for source,target in pairs:
 target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target);a=hashlib.sha256(source.read_bytes()).hexdigest();b=hashlib.sha256(target.read_bytes()).hexdigest();assert a==b;manifest.append({'source':str(source),'copy':str(target),'bytes':source.stat().st_size,'sha256':a})
# Label the explicitly rejected first screenshots so they cannot be mistaken for final comparisons.
invalid=D/'Screenshots/VGB1_TAAIntegration_PIE_C1';(invalid/'INVALID_PHOTOGRAPHS.md').write_text('These initial photograph segments are invalid: the inventory removed the runtime AA entry. Use CPhotoC1 and Photos.json instead. Regular timing segments 0–17 in the original run independently passed method verification. See PhotoReadbackCorrection.json.\n')
(O/'EvidenceManifest.json').write_text(json.dumps({'files':len(manifest),'bytes':sum(x['bytes'] for x in manifest),'all_copies_sha256_verified':True,'items':manifest},indent=2))
archive=O/'RawEvidence.zip';assert not archive.exists()
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_STORED,allowZip64=True) as z:
 for p in sorted(D.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(D))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None;members=len(z.namelist())
(O/'ArchiveCheck.json').write_text(json.dumps({'archive':str(archive),'members':members,'crc_passed':True,'bytes':archive.stat().st_size},indent=2));print('External evidence copied and verified',len(manifest),'files',sum(x['bytes'] for x in manifest),'bytes')
