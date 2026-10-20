"""Read-only SHA audit against this task's initial inventory; no restore or Git mutation."""
from pathlib import Path
import json,hashlib,subprocess,sys
R=Path(__file__).resolve().parents[2];O=R/'Saved/GlumandaV11';initial=json.loads((O/'Initial.json').read_text());rows={};fail=[]
for group in ['untracked_sha256','map_sha256','source_sha256','unreal_v1_sha256']:
 rows[group]=0
 for name,expected in initial[group].items():
  p=R/name;actual=hashlib.sha256(p.read_bytes()).hexdigest()if p.is_file()else None
  if actual!=expected:fail.append({'group':group,'path':name,'expected':expected,'actual':actual})
  rows[group]+=1
refs={r:subprocess.check_output(['git','rev-parse',r],cwd=R,text=True).strip()for r in ['backup/full-03492bd','refs/archive/pokemonster/full-backup-03492bd']};assert set(refs.values())=={'03492bd96b4dba44692f675c19d5f11abfa86b4b'}
result={'passed':not fail,'counts':rows,'differences':fail,'backup_refs':refs};label=sys.argv[1]if len(sys.argv)>1 else 'ProtectionFinal';assert label.isalnum();p=O/(label+'.json');assert not p.exists();p.write_text(json.dumps(result,indent=2));print(json.dumps(result));assert not fail
