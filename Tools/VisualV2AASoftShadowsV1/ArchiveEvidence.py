"""Copy locally measured evidence outside Git and verify every copy by SHA-256."""
from pathlib import Path
import hashlib,json,shutil,csv,zipfile
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2AASoftShadowsV1';O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18');dest=O/'Evidence';assert not dest.exists();dest.mkdir()
records=[]
for p in sorted(S.rglob('*')):
 if not p.is_file() or any(v in p.parts for v in ['Output','Intermediate','DerivedDataCache']):continue
 target=dest/p.relative_to(S);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
 digest=hashlib.sha256(p.read_bytes()).hexdigest();assert hashlib.sha256(target.read_bytes()).hexdigest()==digest
 records.append({'source':str(p),'copy':str(target),'bytes':p.stat().st_size,'sha256':digest})
raw=list((R/'Saved/EnvironmentPerfV2').glob('VGB1_AASoftShadows_*'))+list((R/'Saved/Profiling/CSV').glob('ENV2_VGB1_AASoftShadows_*.csv'))
archive=O/'RawMeasurements.zip';assert not archive.exists()
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(raw):
  if p.is_file():z.write(p,str(p.relative_to(R/'Saved')))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None;members=len(z.namelist())
(O/'EvidenceManifest.json').write_text(json.dumps({'files':records,'copied_bytes':sum(r['bytes'] for r in records),'raw_zip_members':members,'raw_zip_bytes':archive.stat().st_size,'raw_zip_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()},indent=2))
print('Evidence verified',len(records),'files;',members,'raw measurements')
