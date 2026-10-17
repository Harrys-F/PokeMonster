from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');P=R/'Tools/PerformanceRangerV2/Plans';P.mkdir(exist_ok=True)
orders=[['Dorf','Wald','Weg'],['Weg','Wald','Dorf'],['Wald','Dorf','Weg']]
def plan(label,mode,w,h,rows,warm=8,duration=10):
 (P/(label+'.tsv')).write_text('\t'.join(map(str,[label,mode,w,h,warm,duration]))+'\n'+'\n'.join('\t'.join(map(str,row)) for row in rows)+'\n')
for phase,cond in [('Before','V1'),('After','V2')]:
 rows=[(site,cond,rep) for rep,sites in enumerate(orders,1) for site in sites]
 for mode,w,h,kind in [('PIE',1280,740,'A'),('PIE',2331,1346,'B'),('Standalone',1280,740,'C')]:plan(phase+kind,mode,w,h,rows)
plan('ResolutionSmoke','PIE',1280,740,[('Dorf','V1',1)],3,3)
conditions=['RangerHidden','RangerNoShadow','RangerNoAnimation','VegetationHidden','VegetationNoShadow','LocalLightsOff','AllDynamicShadowsOff','PostProcessingOff','RangerFlatMaterial']
# Interleaved control/variant/control at each site, two passes in reverse order to expose drift.
for site in ['Dorf','Wald','Weg']:
 rows=[]
 for rep,conds in [(1,conditions),(2,list(reversed(conditions)))]:
  for condition in conds:rows.extend([(site,'V1',rep),(site,condition,rep)])
 plan('Factors_'+site,'PIE',1280,740,rows,4,6)
# Repeated V1/V2 pairs at fixed sites, balanced order rather than a long one-sided run.
for size,w,h in [('A',1280,740),('B',2331,1346)]:
 rows=[]
 for rep,sites in enumerate(orders,1):
  for site in sites:
   for condition in (['V1','V2'] if rep%2 else ['V2','V1']):rows.append((site,condition,rep))
 plan('Paired'+size,'PIE',w,h,rows)
