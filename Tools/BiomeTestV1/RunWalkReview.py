from pathlib import Path
import sys,time,json,hashlib
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label=sys.argv[1];assert label.isalnum();D=R/'Saved/BiomeTestV1'/label;D.mkdir(exist_ok=False);(D.parent/'WalkRequest.json').write_text(json.dumps({'label':label,'capture_sequences':'--no-sequence'not in sys.argv[2:],'details':'--details'in sys.argv[2:]}))
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest()
job('start_pie');time.sleep(3);job('script','Tools/BiomeTestV1/WalkReview.py');start=time.monotonic();last=None
while not(D/'Result.json').exists():
 time.sleep(3);assert time.monotonic()-start<1000
 if (D/'Progress.json').exists():
  v=json.loads((D/'Progress.json').read_text())
  if v['last']!=last:print(v,flush=True);last=v['last']
r=json.loads((D/'Result.json').read_text());job('stop_pie');assert hashlib.sha256(slot.read_bytes()).hexdigest()==before,'Do not overwrite a changed user save'
assert r['passed'],r['error'];print('BIOME_FULL_WALK_PASS',r['distance_m'],len(r['checks']),flush=True)
