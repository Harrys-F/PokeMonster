from pathlib import Path
import sys,json,time,hashlib
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label=sys.argv[1];assert label.isalnum();O=R/'Saved/WildEncountersV2'/label;O.mkdir(parents=True,exist_ok=False);(O.parent/'WorldOutcomeRequest.json').write_text(json.dumps({'label':label}));slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest();job('start_pie');time.sleep(3);job('script','Tools/WildEncountersV2/ReviewWorldOutcome.py');start=time.monotonic()
while not(O/'Result.json').exists():time.sleep(1);assert time.monotonic()-start<120
r=json.loads((O/'Result.json').read_text());job('stop_pie');time.sleep(1);assert hashlib.sha256(slot.read_bytes()).hexdigest()==before;assert r['passed'],r['error'];print('WORLD_SOURCE_OUTCOME_PASS',r,flush=True)
