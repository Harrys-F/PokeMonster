from pathlib import Path
import sys,json,time
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/GraphicsVariantC';sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
stops=[]
def start(slot):
 (D/'PrepareRequest.json').write_text(json.dumps({'slot':slot,'disable_contacts':False}));before=time.time();job('script','Tools/GraphicsVariantC/PrepareGameplay.py');job('start_pie');start=time.monotonic()
 while not(D/'EarlyPIE.json').exists()or(D/'EarlyPIE.json').stat().st_mtime<before:
  assert time.monotonic()-start<60;time.sleep(.2)
def run(script,path):
 job('script','Tools/GraphicsVariantC/'+script);start=time.monotonic()
 while not path.exists():
  assert time.monotonic()-start<350;time.sleep(.5)
 r=json.loads(path.read_text());assert r['passed'],r;begin=time.monotonic();job('stop_pie',timeout=90);stops.append({'script':script,'stop_seconds':time.monotonic()-begin,'result':r});(D/'GameplayStops.json').write_text(json.dumps(stops,indent=2));print(script,'PASS',flush=True)
start('PokeMonster_SaveV2_Test_PerfGCGameplay01');(D/'ReviewRequest.json').write_text(json.dumps({'label':'Gameplay01'}));run('Gameplay.py',D/'Gameplay01/Result.json')
start('PokeMonster_SaveV2_Test_PerfGCTravel01');run('Travel.py',D/'Travel01/Result.json')
(D/'Cycles01').mkdir(exist_ok=False)
for mode in ['movement','save']:
 start('PokeMonster_SaveV2_Test_PerfGCCycle'+mode);(D/'CycleRequest.json').write_text(json.dumps({'label':mode,'mode':mode}));run('Cycle.py',D/'Cycles01'/mode/'Result.json')
