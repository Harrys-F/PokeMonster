"""CSV summary; distinguish unavailable counters from measured zero costs."""
import csv,json,statistics
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'Saved/WestlandAssetLibrary';C=R/'Saved/Profiling/CSV'
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
  if k not in ['FrameTime','GameThreadTime','RenderThreadTime','GPUTime','RHI/DrawCalls','RHI/PrimitivesDrawn'] and not k.startswith('GPU/'):continue
  xs=[]
  for r in rows:
   try:xs.append(float(r[k]))
   except (ValueError,TypeError,KeyError):pass
  if not xs:continue
  stats[k]={'mean':statistics.mean(xs),'p95':sorted(xs)[int(len(xs)*.95)],'max':max(xs),'counter_status':'not reliable/unavailable on this capture' if max(xs)==0 and k in ['RenderThreadTime','RHI/DrawCalls','RHI/PrimitivesDrawn'] else 'measured'}
 return {'file':str(path.relative_to(R)),'frames_used':len(rows),'frames_discarded_for_warmup':skip,'fps_from_mean_frame_time':1000/stats['FrameTime']['mean'],'stats':stats,'note':'GPU passes overlap; do not add them. CSV scope differs from Slate wall interval.'}
result={}
for mode in ['Full','Empty','FullForest','EmptyForest']:
 p=C/('WLA_'+mode+'PIE_Idle.csv')
 if p.exists():result[mode]=summarize(p)
p=O/'StandaloneCSVPath.txt'
if p.exists():result['Standalone']=summarize(Path(p.read_text().strip()),600)
(O/'RenderingCosts.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({m:{'frames':d['frames_used'],'fps_csv':d['fps_from_mean_frame_time'],'gpu_mean_ms':d['stats'].get('GPUTime',{}).get('mean'),'top_gpu_passes':sorted([(k,v['mean']) for k,v in d['stats'].items() if k.startswith('GPU/')],key=lambda x:x[1],reverse=True)[:5]} for m,d in result.items()},indent=2))
