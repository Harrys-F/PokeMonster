"""Reproducible summaries; keep each repeat and actual render extents, never report zero draw counters as measurements."""
from pathlib import Path
import json,csv,statistics,collections,sys
from Summarize import summarize
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2WorldArtQualityV2'
def aggregate():
 data=summarize();groups=collections.defaultdict(list);metadata={};flat=[]
 for label,rows in data.items():
  kind='Cost' if '_Cost_' in label else 'Final';mode='Standalone' if '_Standalone_' in label else 'PIE';q=int(label[-1]);plan=list(csv.reader((R/'Tools/VisualV2WorldArtQualityV2/Plans'/(label+'.tsv')).open(),delimiter='\t'))[1:]
  assert len(rows)==len(plan),(label,'incomplete')
  assert (R/'Saved/EnvironmentPerfV2'/(label+'_Done.txt')).read_text()=='Complete'
  raw=list(csv.DictReader((R/'Saved/EnvironmentPerfV2'/(label+'_Frames.csv')).open()));assert {int(a['actual_aa_method']) for a in raw}=={2},'Actual TAA proof failed'
  assert all(float(a['fov'])==35 and float(a['pitch'])==-50 and float(a['yaw'])==-45 for a in raw)
  for row in rows:
   p=plan[row['segment']];width,height=int(p[3]),int(p[4]);sp=int(p[6]);expected=[width,height,width,height,width,height,round(width*sp/100),round(height*sp/100)]
   assert row['extent']==[tuple(expected)],(label,row['segment'],row['extent'],expected)
   assert row['resolution_samples_increment']>0
   key=(kind,mode,q,width,height,sp,row['site'],row['condition']);groups[key].append(row)
  metadata[label]={'segments':len(rows),'frames':len(raw),'actual_aa':2,'utc':[raw[0]['utc'],raw[-1]['utc']],'slate_window_dpi':sorted(set((r['window_slate_w'],r['window_slate_h'],r['window_dpi']) for r in raw)),'active_window_fraction':sum(int(r['window_active']) for r in raw)/len(raw)}
 result=[]
 for key,rs in sorted(groups.items()):
  assert len(rs)==3 and {int(r['repeat']) for r in rs}=={1,2,3},key
  kind,mode,q,width,height,sp,site,condition=key;x=dict(kind=kind,mode=mode,quality=q,width=width,height=height,percentage=sp,site=site,condition=condition,runs=3,samples=sum(r['samples'] for r in rs),median_fps=statistics.median(r['median_fps'] for r in rs),frame_ms=statistics.median(r['median_ms'] for r in rs),p95_min_ms=min(r['p95_ms'] for r in rs),p95_max_ms=max(r['p95_ms'] for r in rs),fps_run_min=min(r['median_fps'] for r in rs),fps_run_max=max(r['median_fps'] for r in rs),camera=rs[0]['camera'])
  for counter,field in [('GPUTime','gpu_ms'),('GameThreadTime','game_ms'),('GameThreadTime_CriticalPath','game_critical_ms'),('RenderThreadTime_CriticalPath','render_critical_ms'),('GPU/Basepass','basepass_ms'),('GPU/ShadowDepths','shadow_depths_ms'),('GPU/ShadowProjection','shadow_projection_ms')]:
   values=[r.get('csv',{}).get(counter) for r in rs];values=[v for v in values if v is not None and not v['all_zero']]
   x[field+'_runs']=len(values)
   if values:x[field]=statistics.median(v['median'] for v in values)
  # Raw CSV remains available separately; all-zero RHI/DrawCall series on this Metal build are unavailable.
  x['draw_calls']=None;x['draw_calls_reason']='All-zero CSV counters; not a valid draw-call measurement';result.append(x)
 out={'method':'Median of three repeat medians; P95 range across repeats; wall-frame FPS; independent renderer extents/AA','groups':result,'runs':metadata,'counter_gaps':{label:[r['segment'] for r in rows if not r.get('csv')] for label,rows in data.items() if any(not r.get('csv') for r in rows)}}
 (S/'Aggregate.json').write_text(json.dumps(out,indent=2))
 fields=[k for k in result[0] if k!='camera'];fields=list(dict.fromkeys(fields+[k for r in result for k in r if k!='camera']))
 with (S/'Aggregate.csv').open('w',newline='') as f:
  wr=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore',lineterminator='\n');wr.writeheader();wr.writerows(result)
 return out
if __name__=='__main__':
 a=aggregate();print('Verified',len(a['runs']),'completed series,',sum(x['segments'] for x in a['runs'].values()),'segments,',len(a['groups']),'three-repeat summaries')
