"""Read-only analysis of the final state. No historical A/B or additive GPU-pass claims."""
import csv,json,statistics as st
from pathlib import Path
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2QualityV2';P=R/'Saved/EnvironmentPerfV1';M=json.loads((S/'Measurements.json').read_text())
configs=[(1280,720,1,75),(1280,720,1,100),(2560,1440,1,75),(2560,1440,1,100),(2560,1440,2,75),(2560,1440,2,100)]
results=[];validation=[]
for mode in ['PIE','Standalone']:
 for number,(width,height,quality,percent) in enumerate(configs,1):
  label=f'VEQ2_{mode}_{number}';assert (P/(label+'_Done.txt')).read_text()=='Complete';allrows=M[label];rows=[r for r in allrows if r['site']!='CSVDrain'];assert len(rows)==9
  for r in rows:
   assert r['extent']==[[width,height,width,height,width,height,width*percent//100,height*percent//100]],(label,r['extent'])
   assert r['fractions']==[[percent/100,1.0]] and int(r['quality'])==quality and r['condition']=='Control'
   assert r.get('csv',{}).get('GPUTime') and r['samples']>=20,(label,r['segment'])
   for field,value in [('pitch',-50),('yaw',-45),('fov',35)]:assert all(abs(v-value)<.001 for v in r['camera'][field])
  for site in ['Dorf','Wald','Weg']:
   group=[r for r in rows if r['site']==site];assert len(group)==3 and {r['repeat'] for r in group}=={'1','2','3'}
   for field in ['camera_x','camera_y','camera_z']:
    v=[v for r in group for v in r['camera'][field]];assert max(v)-min(v)<.2
   out={'mode':mode,'config':number,'width':width,'height':height,'quality':quality,'percent':percent,'site':site,'repeats':3,'frame_ms':st.median(r['median_ms'] for r in group),'p95_ms':st.median(r['p95_ms'] for r in group),'run_frame_range_ms':[min(r['median_ms'] for r in group),max(r['median_ms'] for r in group)],'gpu_counters':{}}
   out['fps']=1000/out['frame_ms'];names=set.intersection(*(set(r['csv']) for r in group))
   for n in names:
    values=[r['csv'][n]['median'] for r in group]
    if any(r['csv'][n]['all_zero'] for r in group):continue
    if n=='RenderThreadTime' and min(values)<.05:continue
    out['gpu_counters'][n]=st.median(values)
   out['motion_blur_counter_reported']=any('GPU/MotionBlur' in r['csv'] for r in group)
   out['largest_named_gpu_counters']=sorted([(n,v) for n,v in out['gpu_counters'].items() if n.startswith('GPU/')],key=lambda item:item[1],reverse=True)[:15]
   results.append(out)
  validation.append({'label':label,'measured_segments':len(rows),'excluded_drain_segments':len(allrows)-len(rows),'output':[width,height],'derived_internal':[width*percent//100,height*percent//100],'window_extents':sorted({tuple(v) for r in rows for v in r['window']}),'all_gpu_captures_nonempty':True})
assert len(results)==36;assert sum(r['measured_segments'] for r in validation)==108
(S/'GPUSummary.json').write_text(json.dumps(results,indent=2));(S/'MatrixValidation.json').write_text(json.dumps(validation,indent=2))
fields=['mode','config','width','height','quality','percent','site','fps','frame_ms','p95_ms','run_frame_range_ms','GPUTime','GameThreadTime','RenderThreadTime','GPU/ShadowProjection','GPU/ShadowDepths','GPU/LumenScreenProbeGather','GPU/LumenIrradianceFieldGather','GPU/Basepass','GPU/Unaccounted']
with (S/'PerformanceSummary.csv').open('w') as f:
 writer=csv.DictWriter(f,fields,extrasaction='ignore');writer.writeheader();writer.writerows(dict(r,**r['gpu_counters']) for r in results)
print('Validated 108 measured segments, 36 summaries; six native CSV drain segments excluded')
for r in results:
 if r['quality']==2 and r['percent']==100:print(r['mode'],r['site'],r['fps'],r['frame_ms'],r['largest_named_gpu_counters'])
