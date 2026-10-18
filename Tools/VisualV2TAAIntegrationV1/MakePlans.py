from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/'Tools/VisualV2TAAIntegrationV1/Plans';D.mkdir(exist_ok=True)
configs=[(1280,720,1,75),(1280,720,1,100),(2560,1440,1,75),(2560,1440,1,100),(2560,1440,2,75),(2560,1440,2,100)]
for mode in ['PIE','Standalone']:
 for ci,c in enumerate(configs,1):
  label=f'VGB1_TAAIntegration_{mode}_C{ci}';lines=['\t'.join([label,mode,'5','5'])]
  for rep in [1,2,3]:
   for site in ['Dorf','Wald','Weg']:
    for factor in (['MapTAA:TSR','MapTAA:Native'] if rep%2 else ['MapTAA:Native','MapTAA:TSR']):lines.append('\t'.join(map(str,[site,factor,rep,*c])))
  if ci in [1,6]:
   for site in ['Dorf','Wald','Weg','NPCWald']:
    for factor in ['MapTAA:TSR','MapTAA:Native']:lines.append('\t'.join(map(str,[site,factor,90,*c])))
   lines.append('\t'.join(map(str,['NPCWald','MapTAA:Native',99,*c])))
  p=D/(label+'.tsv');assert not p.exists();p.write_text('\n'.join(lines)+'\n')
print('12 plans, 216 regular segments, 32 photo requests')
