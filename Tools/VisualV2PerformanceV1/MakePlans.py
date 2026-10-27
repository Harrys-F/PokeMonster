"""Create explicit benchmark requests only. Does not launch UE or alter assets."""
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1';prefix=sys.argv[1];assert prefix.isalnum();D.mkdir(exist_ok=True)
sites={'Dorf':[-4100,450,50.15],'Wiese':[-300,2100,50.15],'Wald':[-4300,1550,50.15],'Waldweg':[-2600,1250,50.15],'Gewaesser':[-350,-320,75.15],'Gruppe':[-650,1000,110.15]}
def case(n,p,**kw):return dict(name=n,site='S_'+kw.pop('site',n),position=p,hour=12,**kw)
def save(n,cases,repeats=1):
 p=D/(prefix+n+'Plan.json');assert not p.exists();p.write_text(json.dumps(dict(label=prefix+n,warmup=4,duration=6,repeats=repeats,cases=cases),indent=2));print(p)
for name,action in [('OriginalPIE','OriginalGround'),('OptimizedPIE','BakedSRGB')]:save(name,[case(n,p,action=action)for n,p in sites.items()],3)
rows=[]
for n,p in sites.items():
 for rep,order in enumerate([['OriginalGround','BakedSRGB'],['BakedSRGB','OriginalGround'],['OriginalGround','BakedSRGB']]):
  for action in order:rows.append(case(n+str(rep)+action,p,site=n,action=action,pair=n+str(rep)))
save('NativeMatrix',rows)
rows=[]
for rep,order in enumerate([['High100','High75','Medium100','Medium75'],['Medium75','Medium100','High75','High100'],['High100','High75','Medium100','Medium75']]):
 for n in order:rows.append(case(n+str(rep),[-2960,1700,50.15],site='Wald',action='BakedSRGB',quality=1 if n.startswith('Medium')else 2,percentage=75 if n.endswith('75')else 100))
save('Alternatives',rows)
