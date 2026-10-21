"""Sequential explicit PIE takes; no save backup or save writes, assert exact save hash."""
from pathlib import Path
import sys,json,time,hashlib
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
O=R/'Saved/CreaturePolishV4';label=sys.argv[1];assert label.isalnum();candidate='--candidate'in sys.argv;focus=next((v.split('=',1)[1]for v in sys.argv if v.startswith('--focus=')),None);seconds=float(next((v.split('=',1)[1]for v in sys.argv if v.startswith('--seconds=')),92));yaw=float(next((v.split('=',1)[1]for v in sys.argv if v.startswith('--yaw=')),135));assert not(O/label).exists();q=dict(label=label,seconds=seconds,yaw=yaw,stamps=[4,7,10]+[12+5*i for i in range(16)]+[13.25+5*i for i in range(16)])
if '--reactions'in sys.argv:q.update(mode='reactions',stamps=[4,7,10.2,10.45,10.7,13.2,13.35,16.3,16.65,17.2,19.25,19.6,20.2])
if focus:q['focus']=focus
if candidate:q['profiles']={x['species']:x['profile']for x in json.loads((O/'ImportedCandidates.json').read_text())['models']}
(O/'ShowcaseRequest.json').write_text(json.dumps(q));slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest();job('start_pie');time.sleep(2)
try:
 job('script','Tools/CreaturePolishV4/Showcase.py');start=time.monotonic()
 while not(O/label/'Result.json').exists():
  time.sleep(1);assert time.monotonic()-start<240,'Review callback failed; no forced close'
 result=json.loads((O/label/'Result.json').read_text());assert result['passed'],result.get('error');assert result['save_unchanged']
finally:job('stop_pie')
assert hashlib.sha256(slot.read_bytes()).hexdigest()==before,'Unexpected save change; stop, do not overwrite';print('SHOWCASE_PASS',label,flush=True)
