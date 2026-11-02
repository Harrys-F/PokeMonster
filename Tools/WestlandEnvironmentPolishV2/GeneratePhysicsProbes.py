"""Generate the bounded engine-collision QA fixture from the terrain authoring source."""
from pathlib import Path
import sys,json
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/WestlandEnvironmentPolishV2';D.mkdir(exist_ok=True);sys.path.insert(0,str(Path(__file__).parent));import Shapes as S
points=[]
for n in [-240,-120,-40,60,140,220,280]:
 for e in [-360,-320,-160,80,120,200,240,280,360]:
  base=S.L.height(e,n);z=S.bank_height(e,n,base+S.delta(e,n,base))
  if abs(z-base)>.25 and S.protection(e,n)>.7:points.append(dict(e=e,n=n,expected_z_cm=z*100,old_z_cm=base*100))
for n in [-280,-160,100,200,260,300]:
 for side in [-1,1]:
  e=round((S.L.river(n)+side*8)/2)*2;base=S.L.height(e,n);z=S.bank_height(e,n,base+S.delta(e,n,base))
  if S.protection(e,n)>.5:points.append(dict(e=e,n=n,expected_z_cm=z*100,old_z_cm=base*100))
p=D/'TerrainPhysicsProbes.json';text=json.dumps(points,indent=2)
if p.exists():assert json.loads(p.read_text())==points,'Existing probe fixture differs; do not overwrite'
else:p.write_text(text)
print(len(points),'read-only engine collision probes prepared')
