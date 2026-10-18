"""Generate opt-in test plans on the existing GPU map. No scene edits."""
from pathlib import Path
import sys,json
R=Path(__file__).resolve().parents[2];D=R/'Tools/VisualV2VegetationPerfV1/Plans';D.mkdir(exist_ok=True);S=R/'Saved/VisualV2VegetationPerfV1'
configs=[(1280,720,1,75),(1280,720,1,100),(1280,720,2,75),(1280,720,2,100),(2560,1440,1,75),(2560,1440,1,100),(2560,1440,2,75),(2560,1440,2,100)]
if sys.argv[1]=='Scout':
 label='VGB1_Vegetation_PIE_CScout';lines=[label+'\tPIE\t5\t4']
 for rep in [1,2,3]:
  for candidate in ['FullyRough','TreeLOD1','BushLOD1']:
   for factor in (['Control',candidate] if rep!=2 else [candidate,'Control']):lines.append('\t'.join(map(str,['Wald','VegPerf:'+factor,rep,*configs[-1]])))
 for candidate in ['Control','FullyRough','TreeLOD1','BushLOD1']:lines.append('\t'.join(map(str,['Wald','VegPerf:'+candidate,90,*configs[-1]])))
 lines.append('\t'.join(map(str,['Weg','VegPerf:Control',99,*configs[-1]])))
 (D/(label+'.tsv')).write_text('\n'.join(lines)+'\n')
else:
 candidate=sys.argv[2];assert candidate in ['FullyRough','TreeLOD1','BushLOD1'];(S/'ChosenCandidate.json').write_text(json.dumps({'candidate':candidate,'not_adopted_in_VisualV2':True}))
 for mode in ['PIE','Standalone']:
  for ci,c in enumerate(configs,1):
   label=f'VGB1_Vegetation_{mode}_C{ci}';lines=[label+'\t'+mode+'\t5\t4']
   for rep in [1,2,3]:
    for site in ['Dorf','Wald','Weg']:
     for factor in (['Control',candidate] if rep!=2 else [candidate,'Control']):lines.append('\t'.join(map(str,[site,'VegPerf:'+factor,rep,*c])))
   if ci in [1,8]:
    for site in ['Dorf','Wald','Weg','NPCWald']:
     for factor in ['Control',candidate]:lines.append('\t'.join(map(str,[site,'VegPerf:'+factor,90,*c])))
   lines.append('\t'.join(map(str,['Weg','VegPerf:Control',99,*c])))
   p=D/(label+'.tsv');assert not p.exists();p.write_text('\n'.join(lines)+'\n')
