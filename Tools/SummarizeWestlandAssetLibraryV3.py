"""CSV summary; distinguish unavailable counters from measured zero costs."""
import csv,json,statistics
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'Saved/WestlandAssetLibraryV3';C=R/'Saved/Profiling/CSV'
def summarize(path,skip=0):
 csv.field_size_limit(32*1024*1024)
 with path.open() as f:
  raw=list(csv.reader(f))
 header=next(row for row in reversed(raw) if row and row[0]=='EVENTS');rows=[]
 for row in raw:
  if not row or row[0] in ['EVENTS','[HasHeaderRowAtEnd]']:continue
  record=dict(zip(header,row))
  try:
   if float(record.get('FrameTime',''))>0:rows.append(record)
  except (ValueError,TypeError):pass
 rows=rows[skip:];assert rows,path;stats={}
 for k in rows[0]:
  if k not in ['FrameTime','GameThreadTime','RenderThreadTime','GPUTime','RHI/DrawCalls','RHI/PrimitivesDrawn','RenderThreadTime_CriticalPath','GameThreadTime_CriticalPath','RHIThreadTime'] and not k.startswith(('GPU/','DrawCall/','Exclusive/RenderThread/')):continue
  xs=[]
  for r in rows:
   try:xs.append(float(r[k]))
   except (ValueError,TypeError,KeyError):pass
  if not xs:continue
  stats[k]={'mean':statistics.mean(xs),'p95':sorted(xs)[int(len(xs)*.95)],'max':max(xs),'counter_status':'not reliable/unavailable on this capture' if max(xs)==0 and (k in ['RenderThreadTime','RHI/DrawCalls','RHI/PrimitivesDrawn'] or k.startswith('DrawCall/')) else 'measured'}
 return {'file':str(path.relative_to(R)),'frames_used':len(rows),'frames_discarded_for_warmup':skip,'fps_from_mean_frame_time':1000/stats['FrameTime']['mean'],'stats':stats,'note':'GPU passes overlap; do not add them. CSV scope differs from Slate wall interval.'}
result={}
for p in sorted(C.glob('WLA_V3_*.csv')):
 if 'InvalidStaticSwap' in p.name:continue
 result[p.stem[len('WLA_V3_'):]]=summarize(p)
(O/'RenderingCosts.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({m:{'frames':d['frames_used'],'fps_csv':d['fps_from_mean_frame_time'],'frame_ms':d['stats']['FrameTime']['mean'],'game_thread_ms':d['stats'].get('GameThreadTime',{}).get('mean'),'gpu_mean_ms':d['stats'].get('GPUTime',{}).get('mean'),'top_gpu_passes':sorted([(k,v['mean']) for k,v in d['stats'].items() if k.startswith('GPU/')],key=lambda x:x[1],reverse=True)[:8]} for m,d in result.items()},indent=2))
