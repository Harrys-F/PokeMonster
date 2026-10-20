"""Read-only comparison of initial untracked files, every map, developer save and full-backup refs."""
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[2];label=sys.argv[1];assert label.isalnum();O=R/'Saved/BattleSystemV3'/(label+'.json');assert not O.exists();initial=json.loads((O.parent/'Initial.json').read_text());bad=[]
for group in ['untracked','maps']:
 for name,sha in initial[group].items():
  p=R/name
  if not p.is_file()or hashlib.sha256(p.read_bytes()).hexdigest()!=sha:bad.append(name)
save=hashlib.sha256((R/'Saved/SaveGames/PokeMonster_Dev.sav').read_bytes()).hexdigest();assert save==initial['save_sha256'],'Developer save differs; do not overwrite blindly'
refs={p:subprocess.check_output(['git','rev-parse',p],cwd=R,text=True).strip()for p in ['backup/full-03492bd','refs/archive/pokemonster/full-backup-03492bd']};assert set(refs.values())=={'03492bd96b4dba44692f675c19d5f11abfa86b4b'}
# All original art sources and creature presentation binaries remain byte-identical to the initial commit.
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',initial['head'],'--','Art','Content/Characters/Creatures'],cwd=R,text=True).splitlines();unchanged=0
for name in paths:
 raw=subprocess.check_output(['git','show',initial['head']+':'+name],cwd=R)
 if raw.startswith(b'version https://git-lfs.github.com/spec/v1\n'):sha=next(x[11:]for x in raw.decode().splitlines()if x.startswith('oid sha256:'))
 else:sha=hashlib.sha256(raw).hexdigest()
 p=R/name
 if not p.is_file()or hashlib.sha256(p.read_bytes()).hexdigest()!=sha:bad.append(name)
 unchanged+=1
result={'passed':not bad,'untracked':len(initial['untracked']),'maps':len(initial['maps']),'art_and_creature_presentation_files':unchanged,'differences':bad,'save_sha256':save,'backup_refs':refs};O.write_text(json.dumps(result,indent=2));print(json.dumps(result));assert not bad
