from pathlib import Path
import sys,json,time,hashlib
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label=sys.argv[1];assert label.isalnum();O=R/'Saved/MotionRefinementV5';assert not(O/label).exists();(O/'PlayerRequest.json').write_text(json.dumps(dict(label=label,original_clips='--original-clips'in sys.argv,native_record=str(R/'Saved/VisualV2TAAIntegrationV1/Recordings'/label)if '--record'in sys.argv else None)));slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest();job('start_pie');time.sleep(2)
try:
 job('script','Tools/MotionRefinementV5/ReviewPlayer.py');start=time.monotonic()
 while not(O/label/'Result.json').exists():time.sleep(1);assert time.monotonic()-start<200
 d=json.loads((O/label/'Result.json').read_text());assert d['passed'],d['error'];assert d['save_unchanged'];
 if '--record'in sys.argv:
  start=time.monotonic()
  while not(R/'Saved/VisualV2TAAIntegrationV1/Recordings'/label/'Complete.txt').exists():time.sleep(.2);assert time.monotonic()-start<45
 print('PLAYER_REVIEW_PASS',label,len(d['rows']),flush=True)
finally:job('stop_pie')
assert hashlib.sha256(slot.read_bytes()).hexdigest()==before
