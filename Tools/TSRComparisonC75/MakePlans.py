"""Bounded repeatable AA comparison; emits requests, never maps or assets."""
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/TSRComparisonC75';tag=sys.argv[1];assert tag.isalnum()
for mode in ['PIE','Native']:
 cases=[]
 for site,pos in {'Dorf':[-4100,450,50.15],'Wiese':[-300,2100,50.15],'Wald':[-4300,1550,50.15]}.items():
  for rep,order in enumerate([['TAAU','TSR'],['TSR','TAAU'],['TAAU','TSR']]):
   for aa in order:cases.append({'name':site+str(rep)+aa,'site':site if site!='Wiese'else'S_Wiese','position':pos,'hour':12,'percentage':75,'quality':2,'condition':'MapTAA:TSR'if aa=='TSR'else'MapTAA:Native','pair':site+str(rep),'aa':aa})
 out=D/(mode+'Plan'+tag+'.json');assert not out.exists();out.write_text(json.dumps({'label':mode+'Compare'+tag,'mode':mode,'warmup':6,'duration':8,'repeats':1,'cases':cases},indent=2));print(out)
