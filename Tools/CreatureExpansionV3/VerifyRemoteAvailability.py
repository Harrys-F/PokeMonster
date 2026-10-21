"""Read-only LFS availability proof with one-byte GETs, not a full remote SHA audit.
Never store auth headers or signed URLs. Avoid downloading all source/FBX payloads again.
"""
from pathlib import Path
import subprocess,json,sys,hashlib,urllib.request
R=Path(__file__).resolve().parents[2];commit=subprocess.check_output(['git','rev-parse',sys.argv[1]],cwd=R,text=True).strip();assert subprocess.check_output(['git','remote','get-url','origin'],cwd=R,text=True).strip()=='git@github.com:Harrys-F/PokeMonster.git'
assert subprocess.check_output(['git','ls-remote','origin','refs/heads/main'],cwd=R,text=True).split()[0]==commit
paths=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r',commit],cwd=R,text=True).splitlines();objects={}
for p in paths:
 b=subprocess.check_output(['git','show',commit+':'+p],cwd=R)
 if not b.startswith(b'version https://git-lfs.github.com/spec/v1\n'):continue
 fields=b.decode().splitlines();oid=next(x[11:]for x in fields if x.startswith('oid sha256:'));size=int(next(x[5:]for x in fields if x.startswith('size ')));local=(R/p).read_bytes();assert len(local)==size and hashlib.sha256(local).hexdigest()==oid;objects[oid]={'oid':oid,'size':size,'path':p,'first_byte':local[:1]}
verified=[]
if objects:
 auth=json.loads(subprocess.check_output(['ssh','-o','BatchMode=yes','git@github.com','git-lfs-authenticate','Harrys-F/PokeMonster.git','download'],text=True));headers=dict(auth['header']);headers.update({'Accept':'application/vnd.git-lfs+json','Content-Type':'application/vnd.git-lfs+json'});allrows=list(objects.values())
 for start in range(0,len(allrows),100):
  group=allrows[start:start+100];payload={'operation':'download','transfers':['basic'],'objects':[{'oid':v['oid'],'size':v['size']}for v in group]};request=urllib.request.Request(auth['href'].rstrip('/')+'/objects/batch',data=json.dumps(payload).encode(),headers=headers)
  with urllib.request.urlopen(request,timeout=60)as response:rows=json.load(response)['objects']
  assert {x['oid']for x in rows}=={x['oid']for x in group}
  for row in rows:
   assert 'error'not in row,(row['oid'],row.get('error'));v=objects[row['oid']];assert row['size']==v['size'];action=row['actions']['download'];h=dict(action.get('header',{}));h['Range']='bytes=0-0';q=urllib.request.Request(action['href'],headers=h)
   with urllib.request.urlopen(q,timeout=60)as response:
    status=response.status
    if status==206:assert response.headers.get('Content-Range')=='bytes 0-0/'+str(v['size'])
    else:assert status==200 and int(response.headers['Content-Length'])==v['size']
    assert response.read(1)==v['first_byte']
   verified.append({'oid':v['oid'],'bytes':v['size'],'path':v['path'],'batch_and_read_available':True,'http_status':status,'local_sha256_verified':True,'remote_full_sha256_verified':False})
result={'commit':commit,'verified':True,'count':len(verified),'bytes':sum(x['bytes']for x in verified),'scope':'Authenticated download batch plus one-byte GET / server-declared total size; full local SHA-256. Not full remote payload SHA-256.','objects':verified,'no_credentials_or_signed_urls_saved':True};out=R/'Saved/CreatureExpansionV3/RemoteAvailability.json';out.write_text(json.dumps(result,indent=2));print('REMOTE_LFS_AVAILABLE',commit,len(verified),result['bytes'])
