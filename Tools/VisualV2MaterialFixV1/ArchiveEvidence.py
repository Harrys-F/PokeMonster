"""Explicit optional review export. Does not move/delete sources or gate game/builds."""
from pathlib import Path
import json,hashlib,shutil,zipfile,sys
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2MaterialFixV1';P=R/'Saved/EnvironmentPerfV2';O=Path(sys.argv[1]).expanduser().resolve();assert O.is_relative_to(Path.home()/'Documents/Codex');E=O/'Evidence';E.mkdir(exist_ok=False);rows=[];excluded=[]
for f in S.rglob('*'):
 if not f.is_file():continue
 rel=f.relative_to(S)
 if str(rel).startswith('Cook/Output/'):
  excluded.append({'path':str(rel),'bytes':f.stat().st_size});continue
 d=E/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,d);h=hashlib.sha256(f.read_bytes()).hexdigest();assert hashlib.sha256(d.read_bytes()).hexdigest()==h;rows.append({'path':str(rel),'bytes':f.stat().st_size,'sha256':h})
files=list(P.glob('VGB1_MaterialFix_*_C*_*'));files+=list((R/'Saved/Profiling/CSV').glob('ENV2_VGB1_MaterialFix_*_C*_*.csv'))
archive=O/'RawMeasurements.zip';assert not archive.exists()
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for f in sorted(files):
  if f.is_file():z.write(f,str(f.relative_to(R/'Saved')))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None;members=len(z.infolist())
(O/'EvidenceManifest.json').write_text(json.dumps({'files':rows,'verified_files':len(rows),'raw_archive_members':members,'raw_archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'zip_crc_valid':True,'excluded_reproducible_cook_outputs':excluded,'excluded_cook_bytes':sum(x['bytes'] for x in excluded)},indent=2));print('Verified external files',len(rows),'raw zip members',members,'cook outputs retained only under ignored Saved',sum(x['bytes'] for x in excluded))
