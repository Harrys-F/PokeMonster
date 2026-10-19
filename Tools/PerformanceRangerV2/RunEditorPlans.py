import json,time,sys
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster');P=R/'Art/Characters/NPCs/Ranger/Review/V2';O=R/'Saved/PerformanceRangerV2';num=int(sys.argv[1])
for name in sys.argv[2:]:
 done=O/(name+'_Done.txt');assert not done.exists(),'Keep existing measurements, use a new label';num+=1
 (P/'Request.json').write_text(json.dumps({'plan':name}));(P/'Job.json').write_text(json.dumps({'id':num,'path':'Tools/PerformanceRangerV2/StartProbe.py'}));start=time.monotonic();print('START',name,flush=True)
 while not done.exists():
  time.sleep(3)
  assert time.monotonic()-start<1400,'Timed out'
 assert done.read_text()=='Complete',done.read_text();print('DONE',name,flush=True)
print('LAST_JOB',num,flush=True)
