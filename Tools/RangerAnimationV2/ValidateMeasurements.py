import json,math,statistics,csv,shutil,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[2];S=R/'Saved/RangerAnimationV2';O=R/'Art/Characters/NPCs/Ranger/Review/AnimationV2/Data';a=json.loads((S/'Measurements.json').read_text());issues=[];table=[];settings={};allfiles=[]
configs=[(1280,740,1,75),(1280,740,1,100),(2560,1440,1,75),(2560,1440,1,100),(2560,1440,2,75),(2560,1440,2,100)]
for mode,prefix in [('PIE','PIE'),('Standalone','Native')]:
 for i,(w,h,q,sp) in enumerate(configs,1):
  label=prefix+'Matrix'+str(i);rows=a.get(label,[])
  if len(rows)!=6:issues.append((label,'segment count',len(rows)))
  assert len(rows)==6
  for state in ['V1','V2']:
   rs=[x for x in rows if x['condition']==state];assert sorted(int(x['repeat']) for x in rs)==[1,2,3]
   for r in rs:
    expected=[w,h,w,h,w,h,math.ceil(w*sp/100),math.ceil(h*sp/100)]
    if r['extent']!=[expected]:issues.append((label,r['segment'],'extent',r['extent'],expected))
    if r['fractions']!=[[sp/100,1.]]:issues.append((label,r['segment'],'fraction',r['fractions']))
    if r.get('active_window_fraction')!=1:issues.append((label,r['segment'],'focus',r.get('active_window_fraction')))
    if not r.get('csv'):issues.append((label,r['segment'],'missing CSV'))
    if r['samples']<30:issues.append((label,r['segment'],'short sample'))
    for k,target in [('pitch',-50),('yaw',-45),('fov',35)]:
     if max(abs(v-target) for v in r['camera'][k])>.001:issues.append((label,r['segment'],'camera',k,r['camera'][k]))
  def med(state,key):return statistics.median(x[key] for x in rows if x['condition']==state)
  def counter(state,key):
   vals=[x['csv'][key]['median'] for x in rows if x['condition']==state and key in x.get('csv',{})];return statistics.median(vals) if vals else None
  pairdiff=[next(x['median_ms'] for x in rows if x['condition']=='V2' and int(x['repeat'])==j)-next(x['median_ms'] for x in rows if x['condition']=='V1' and int(x['repeat'])==j) for j in [1,2,3]]
  table.append({'mode':mode,'config':[w,h,q,sp],'V1_ms':med('V1','median_ms'),'V2_ms':med('V2','median_ms'),'V1_fps':1000/med('V1','median_ms'),'V2_fps':1000/med('V2','median_ms'),'V1_p95':med('V1','p95_ms'),'V2_p95':med('V2','p95_ms'),'pair_deltas_ms':pairdiff,'median_pair_delta_ms':statistics.median(pairdiff),'V1_gpu':counter('V1','GPUTime'),'V2_gpu':counter('V2','GPUTime'),'V1_game':counter('V1','GameThreadTime'),'V2_game':counter('V2','GameThreadTime'),'V1_render':counter('V1','RenderThreadTime'),'V2_render':counter('V2','RenderThreadTime')})
  settings[label]=(S/(label+'_Settings.txt')).read_text()
  allfiles.extend([S/(label+'_Frames.csv'),S/(label+'_Segments.csv'),S/(label+'_Settings.txt'),S/(label+'_Preset.json')] if mode=='PIE' else [S/(label+'_Frames.csv'),S/(label+'_Segments.csv'),S/(label+'_Settings.txt'),S/(label+'_Launch.json')])
  allfiles.extend(R/'Saved/Profiling/CSV'/('NPC2_'+label+'_'+str(n).zfill(3)+'.csv') for n in range(6))
# Camera position must match across all paired samples, not merely rotation.
poses=[tuple(tuple(x['camera'][k]) for k in ['camera_x','camera_y','camera_z']) for rows in a.values() for x in rows]
reference=poses[0]
for j,p in enumerate(poses):
 if max(abs(p[i][k]-reference[i][k]) for i in range(3) for k in range(2))>.01:issues.append(('camera position',j,p,reference))
validation={'segments':sum(len(v) for v in a.values()),'issues':issues,'camera_reference_ranges_cm':reference,'configurations':12,'repeats_per_state_configuration':3,'source':'Renderer observer extents plus native viewport/target/window/camera, exact raw frames preserved','internal_resolution_method':'Renderer resolution fraction upper bound with dynamic resolution off, ceil dimensions, not GPU allocation readback'}
(O/'MeasurementValidation.json').write_text(json.dumps(validation,indent=2));(O/'PerformanceTable.json').write_text(json.dumps(table,indent=2));shutil.copy2(S/'Measurements.json',O/'Measurements.json');(O/'BenchmarkSettings.json').write_text(json.dumps(settings,indent=2))
with zipfile.ZipFile(O/'RawMeasurements.zip','w',zipfile.ZIP_DEFLATED,6) as z:
 for f in allfiles:
  assert f.exists(),str(f);z.write(f,str(f.relative_to(R)))
assert not issues,issues
print('VALIDATED',validation['segments'],'segments')
for x in table:print(x['mode'],x['config'],'FPS',round(x['V1_fps'],2),round(x['V2_fps'],2),'ms',round(x['V1_ms'],2),round(x['V2_ms'],2),'delta',round(x['median_pair_delta_ms'],3))
