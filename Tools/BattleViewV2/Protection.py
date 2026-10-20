"""Compare all initially protected paths; no restoration or Git mutation."""
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[2];label=sys.argv[1];assert label.isalnum();O=R/'Saved/BattleViewV2'/(label+'.json');assert not O.exists();initial=json.loads((O.parent/'Initial.json').read_text());rows={};bad=[]
for group in['untracked','maps','sight']:
 rows[group]=len(initial[group])
 for name,sha in initial[group].items():
  p=R/name
  if not p.is_file()or hashlib.sha256(p.read_bytes()).hexdigest()!=sha:bad.append(name)
save=hashlib.sha256((R/'Saved/SaveGames/PokeMonster_Dev.sav').read_bytes()).hexdigest();assert save==initial['save_sha256'],'Original developer save differs; do not overwrite blindly'
refs={p:subprocess.check_output(['git','rev-parse',p],cwd=R,text=True).strip()for p in['backup/full-03492bd','refs/archive/pokemonster/full-backup-03492bd']};assert set(refs.values())=={'03492bd96b4dba44692f675c19d5f11abfa86b4b'}
x={'passed':not bad,'checked':rows,'differences':bad,'save_sha256':save,'backup_refs':refs};O.write_text(json.dumps(x,indent=2));print(json.dumps(x));assert not bad
