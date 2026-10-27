"""Create bounded paired benchmark requests, not maps or assets."""
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/GraphicsVariantC';tag=sys.argv[1];assert tag.isalnum()
sites={'Dorf':[-4100,450,50.15],'Wiese':[-300,2100,50.15],'Wald':[-4300,1550,50.15],'Waldweg':[-2600,1250,50.15],'Gewaesser':[-350,-320,75.15],'Gruppe':[-650,1000,110.15]}
for mode in ['PIE','Native']:
 cases=[]
 for site,position in sites.items():
  for repeat,order in enumerate([['C','100'],['100','C'],['C','100']]):
   for profile in order:
    row={'name':site+str(repeat)+profile,'site':'S_'+site,'position':position,'hour':12,'percentage':75 if profile=='C'else 100,'quality':2,'condition':'GraphicsProfileActive','pair':site+str(repeat)}
    if not cases:row['default_unforced']=True
    else:row['profile']=profile
    cases.append(row)
 out=D/(mode+'Plan'+tag+'.json');assert not out.exists();out.write_text(json.dumps({'label':mode+'Matrix'+tag,'mode':mode,'warmup':4,'duration':6,'repeats':1,'cases':cases},indent=2));print(out)
