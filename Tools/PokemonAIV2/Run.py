"""Start one ordinary PIE test and always end it normally; never stop an editor process."""
from pathlib import Path
import json,time,sys,hashlib
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
kind,label=sys.argv[1:];assert label.isalnum();D=R/'Saved/ProjectRefinement/PokemonAIV2';user=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(user.read_bytes()).hexdigest()
assert kind in ['connected','performance','visual'];(D/'ReviewRequest.json').write_text(json.dumps({'label':label}));script={'connected':'Review','performance':'Performance','visual':'Visual'}[kind];out=D/label/'Result.json'
assert not out.exists();job('start_pie');time.sleep(.3)
try:
 job('script','Tools/PokemonAIV2/'+script+'.py');start=time.monotonic();last=''
 while not out.exists():
  assert time.monotonic()-start<700,'Review timeout; leave diagnostic result visible'
  p=out.parent/'Progress.json'
  if p.exists():
   v=json.loads(p.read_text());now=str(v.get('phase',v))
   if now!=last:print(now,flush=True);last=now
  time.sleep(2)
 result=json.loads(out.read_text());assert result['passed'],result.get('error')
finally:job('stop_pie');assert hashlib.sha256(user.read_bytes()).hexdigest()==before
print('POKEMON_AI_PIE_PASS',kind,label,flush=True)
