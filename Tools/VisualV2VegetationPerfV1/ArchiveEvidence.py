"""Copy completed evidence outside Git, verify every SHA256, preserve originals."""
from pathlib import Path
import shutil,json,hashlib,zipfile
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2VegetationPerfV1';O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18');assert (S/'PipelineComplete.json').exists();D=O/'Evidence';assert not D.exists();D.mkdir();manifest=[]
def copy(src,dst):
 dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);a=hashlib.sha256(src.read_bytes()).hexdigest();b=hashlib.sha256(dst.read_bytes()).hexdigest();assert a==b;manifest.append({'source':str(src),'copy':str(dst),'bytes':src.stat().st_size,'sha256':a})
for p in S.rglob('*'):
 if p.is_file() and 'VideoSources' not in p.parts and p.name!='EncodeRecording':copy(p,D/p.relative_to(S))
for p in (R/'Saved/EnvironmentPerfV2').glob('VGB1_Vegetation_*'):
 if p.is_file():copy(p,D/'RawProbe'/p.name)
for p in (R/'Saved/Profiling/CSV').glob('ENV2_VGB1_Vegetation_*.csv'):copy(p,D/'ProfilingCSV'/p.name)
for p in (R/'Saved/VisualV2TAAIntegrationV1/Recordings').glob('VegetationPerfV1_*'):
 assert p.is_dir()
 for f in p.rglob('*'):
  if f.is_file():copy(f,D/'Recordings'/p.name/f.relative_to(p))
(O/'EvidenceManifest.json').write_text(json.dumps({'files':len(manifest),'bytes':sum(x['bytes'] for x in manifest),'all_sha256_verified':True,'entries':manifest},indent=2));print('ARCHIVE COPIES VERIFIED',len(manifest),'files',sum(x['bytes'] for x in manifest),'bytes',flush=True)
archive=O/'RawEvidence.zip';assert not archive.exists()
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_STORED,allowZip64=True) as z:
 for p in sorted(D.rglob('*')):
  if p.is_file():z.write(p,str(p.relative_to(O)))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
(O/'ArchiveCheck.json').write_text(json.dumps({'archive':str(archive),'bytes':archive.stat().st_size,'crc_verified':True},indent=2));print('ZIP CRC VERIFIED',flush=True)
