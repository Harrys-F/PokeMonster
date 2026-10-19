"""Read-only SHA-256 verification of LFS objects in a pushed commit; never persist credentials."""
from pathlib import Path
import subprocess,json,urllib.request,hashlib,sys,time
R=Path(__file__).resolve().parents[2];commit=sys.argv[1];out=R/'Saved/ProjectRefinement/RemoteLFS.json';assert subprocess.check_output(['git','remote','get-url','origin'],cwd=R,text=True).strip()=='git@github.com:Harrys-F/PokeMonster.git'
paths=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r',commit],cwd=R,text=True).splitlines();objects={}
for p in paths:
 b=subprocess.check_output(['git','show',commit+':'+p],cwd=R)
 if not b.startswith(b'version https://git-lfs.github.com/spec/v1\n'):continue
 lines=b.decode().splitlines();oid=next(x[11:] for x in lines if x.startswith('oid sha256:'));size=int(next(x[5:] for x in lines if x.startswith('size ')));assert (R/p).is_file() and hashlib.sha256((R/p).read_bytes()).hexdigest()==oid;objects[oid]={'oid':oid,'size':size,'path':p}
auth=json.loads(subprocess.check_output(['ssh','-o','BatchMode=yes','git@github.com','git-lfs-authenticate','Harrys-F/PokeMonster.git','download'],text=True));headers=dict(auth['header']);headers.update({'Accept':'application/vnd.git-lfs+json','Content-Type':'application/vnd.git-lfs+json'});url=auth['href'].rstrip('/')+'/objects/batch';req=urllib.request.Request(url,data=json.dumps({'operation':'download','transfers':['basic'],'objects':[{'oid':o['oid'],'size':o['size']} for o in objects.values()]}).encode(),headers=headers)
with urllib.request.urlopen(req,timeout=60) as response:rows=json.load(response)['objects']
assert {x['oid'] for x in rows}==set(objects);verified=[]
for x in rows:
 assert 'error' not in x,(x['oid'],x.get('error'));a=x['actions']['download'];q=urllib.request.Request(a['href'],headers=a.get('header',{}));h=hashlib.sha256();total=0
 with urllib.request.urlopen(q,timeout=60) as f:
  while True:
   chunk=f.read(1024*1024)
   if not chunk:break
   h.update(chunk);total+=len(chunk)
 assert h.hexdigest()==x['oid'] and total==objects[x['oid']]['size'];verified.append({'oid':x['oid'],'bytes':total,'path':objects[x['oid']]['path'],'remote_download_sha256_verified':True})
r={'commit':commit,'objects':verified,'count':len(verified),'bytes':sum(x['bytes'] for x in verified),'verified':True,'no_credentials_or_download_urls_saved':True};out.write_text(json.dumps(r,indent=2));print('REMOTE_LFS_SHA256_VERIFIED',r['count'],r['bytes'])
