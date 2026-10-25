"""Stage only the explicitly verified NPC package, verify all staged LFS pointers/objects."""
from pathlib import Path
import json,subprocess,hashlib
R=Path(__file__).resolve().parents[2];O=R/'Saved/ProjectRefinement/NPCExpansion';files=json.loads((O/'PackageFiles.json').read_text());base=json.loads((O/'Baseline.json').read_text());assert not set(files)&set(base['untracked'])
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
assert git('branch','--show-current').decode().strip()=='main'
assert git('rev-parse','HEAD')==git('rev-parse','origin/main')
existing=set(filter(None,git('diff','--cached','--name-only','-z').decode().split('\0')));assert not existing or existing==set(files),'Foreign staged changes must remain untouched'
assert all(not p.startswith('Saved/') and not p.endswith(('.png','.jpg','.mp4','.mov','.pyc','.glb')) for p in files)
subprocess.run(['git','add','--',*files],cwd=R,check=True);staged=git('diff','--cached','--name-only','-z').decode().strip('\0').split('\0');assert set(staged)==set(files),(set(staged)-set(files),set(files)-set(staged))
subprocess.run(['git','diff','--cached','--check'],cwd=R,check=True)
core=json.loads((R/'Tools/DevelopmentEvidence/CoreFiles.json').read_text());env=git('lfs','env').decode();root=next(x.split('=',1)[1]for x in env.splitlines()if x.startswith('LocalMediaDir='));objects={}
for p in files:
 if Path(p).suffix not in ['.uasset','.umap','.blend','.fbx']:continue
 pointer=git('show',':'+p).decode();assert pointer.startswith('version https://git-lfs.github.com/spec/v1\n');oid=next(x.split(':',1)[1]for x in pointer.splitlines()if x.startswith('oid sha256:'));size=int(next(x.split()[1]for x in pointer.splitlines()if x.startswith('size ')));expected=core['files'][p];assert oid==expected['sha256']and size==expected['bytes'],p
 obj=Path(root)/oid[:2]/oid[2:4]/oid;assert obj.is_file()and obj.stat().st_size==size;h=hashlib.sha256()
 with obj.open('rb')as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 assert h.hexdigest()==oid,p;objects[oid]=size
report={'staged_files':len(files),'staged_lfs_objects':len(objects),'lfs_total_bytes':sum(objects.values()),'lfs_gib':sum(objects.values())/1024**3,'all_local_lfs_checksums_valid':True,'foreign_untracked_excluded':len(base['untracked']),'files':files};(O/'StagedVerification.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items()if k!='files'}))
