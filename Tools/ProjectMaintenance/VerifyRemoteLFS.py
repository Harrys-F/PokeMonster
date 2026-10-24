"""Read-only SHA-256 verification of LFS objects in a pushed commit; never persist credentials."""
from pathlib import Path
import subprocess,json,urllib.request,hashlib,sys,time
R=Path(__file__).resolve().parents[2];commit=subprocess.check_output(['git','rev-parse',sys.argv[1]],cwd=R,text=True).strip();out=R/'Saved/ProjectRefinement/RemoteLFS.json';assert subprocess.check_output(['git','remote','get-url','origin'],cwd=R,text=True).strip()=='git@github.com:Harrys-F/PokeMonster.git'
paths=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r',commit],cwd=R,text=True).splitlines();objects={}
for p in paths:
 b=subprocess.check_output(['git','show',commit+':'+p],cwd=R)
 if not b.startswith(b'version https://git-lfs.github.com/spec/v1\n'):continue
 lines=b.decode().splitlines();oid=next(x[11:] for x in lines if x.startswith('oid sha256:'));size=int(next(x[5:] for x in lines if x.startswith('size ')))
 local=R/p;basis='working_file'
 # A subsequent approved package may already modify the same map. Verify the exact
 # committed LFS object instead; never overwrite the current map with the earlier version.
 if not local.is_file() or hashlib.sha256(local.read_bytes()).hexdigest()!=oid:
  env=subprocess.check_output(['git','lfs','env'],cwd=R,text=True);media=Path(next(line.split('=',1)[1] for line in env.splitlines() if line.startswith('LocalMediaDir=')));local=media/oid[:2]/oid[2:4]/oid;basis='immutable_local_lfs_object'
 assert local.is_file() and local.stat().st_size==size and hashlib.sha256(local.read_bytes()).hexdigest()==oid,(p,oid)
 objects[oid]={'oid':oid,'size':size,'path':p,'local_validation_basis':basis}
# A documentation-only commit has no LFS objects. GitHub rejected an empty batch
# with HTTP 422; do not request credentials or send a meaningless network request.
if not objects:
 r={'commit':commit,'objects':[],'count':0,'bytes':0,'verified':True,'network_requested':False,'scope':'No LFS file changes in this commit; no object download claimed','no_credentials_or_download_urls_saved':True}
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(r,indent=2));print('REMOTE_LFS_NOT_REQUIRED 0 0 (no LFS changes; no network request)');sys.exit(0)
auth=json.loads(subprocess.check_output(['ssh','-o','BatchMode=yes','git@github.com','git-lfs-authenticate','Harrys-F/PokeMonster.git','download'],text=True));headers=dict(auth['header']);headers.update({'Accept':'application/vnd.git-lfs+json','Content-Type':'application/vnd.git-lfs+json'});url=auth['href'].rstrip('/')+'/objects/batch';rows=[];values=list(objects.values())
# The server rejects an oversized single metadata batch (HTTP 413). Fixed small
# batches validate the same object set; this is not an upload or a retry loop.
for start in range(0,len(values),32):
 req=urllib.request.Request(url,data=json.dumps({'operation':'download','transfers':['basic'],'objects':[{'oid':o['oid'],'size':o['size']} for o in values[start:start+32]]}).encode(),headers=headers)
 with urllib.request.urlopen(req,timeout=60) as response:rows.extend(json.load(response)['objects'])
assert {x['oid'] for x in rows}==set(objects);verified=[]
for x in rows:
 assert 'error' not in x,(x['oid'],x.get('error'));a=x['actions']['download'];q=urllib.request.Request(a['href'],headers=a.get('header',{}));h=hashlib.sha256();total=0
 with urllib.request.urlopen(q,timeout=60) as f:
  while True:
   chunk=f.read(1024*1024)
   if not chunk:break
   h.update(chunk);total+=len(chunk)
 assert h.hexdigest()==x['oid'] and total==objects[x['oid']]['size'];verified.append({'oid':x['oid'],'bytes':total,'path':objects[x['oid']]['path'],'remote_download_sha256_verified':True,'local_validation_basis':objects[x['oid']]['local_validation_basis']})
r={'commit':commit,'objects':verified,'count':len(verified),'bytes':sum(x['bytes'] for x in verified),'verified':True,'no_credentials_or_download_urls_saved':True};out.write_text(json.dumps(r,indent=2));print('REMOTE_LFS_SHA256_VERIFIED',r['count'],r['bytes'])
