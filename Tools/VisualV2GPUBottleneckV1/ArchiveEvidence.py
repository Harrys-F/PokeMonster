"""Copy/verify optional evidence outside Git after every GPU measurement has finished."""
import sys,json,hashlib,shutil,zipfile,csv,struct
from pathlib import Path
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2GPUBottleneckV1';P=R/'Saved/EnvironmentPerfV2';D=Path(sys.argv[1]);assert D.is_absolute() and not D.is_relative_to(R)
E=D/'Evidence';E.mkdir(exist_ok=False);manifest=[]
for source in sorted(S.rglob('*')):
 if not source.is_file():continue
 target=E/source.relative_to(S);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
 digest=hashlib.sha256(source.read_bytes()).hexdigest();assert digest==hashlib.sha256(target.read_bytes()).hexdigest()
 row={'source':str(source),'copy':str(target),'bytes':source.stat().st_size,'sha256':digest}
 if source.suffix.lower()=='.png':
  raw=source.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n';row['extent']=struct.unpack('>II',raw[16:24])
  if 'Screenshots' in source.parts:assert row['extent']==(2560,1440)
 manifest.append(row)
raws=sorted(P.glob('VGB1_*'));csvs=sorted((R/'Saved/Profiling/CSV').glob('ENV2_VGB1_*.csv'))
archive=D/'RawMeasurements.zip';assert not archive.exists()
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for f in raws+csvs:
  if f.is_file():z.write(f,str(f.relative_to(R/'Saved')))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
(D/'EvidenceManifest.json').write_text(json.dumps({'files':manifest,'verified_files':len(manifest),'raw_archive':str(archive),'archive_bytes':archive.stat().st_size,'raw_members':len(raws)+len(csvs),'archive_crc_checked':True},indent=2));print('Verified evidence files',len(manifest),'raw members',len(raws)+len(csvs))
