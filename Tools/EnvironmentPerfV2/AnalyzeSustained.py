"""Postprocess only after the graphics benchmarks have stopped."""
import json,csv,statistics,datetime,collections
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV2';m=json.loads((O/'Measurements.json').read_text());rows=m['SustainedQHD'];assert len(rows)==9
segments=list(csv.DictReader((O/'SustainedQHD_Segments.csv').open()));assert len(segments)==9
parse=lambda s:datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
start=parse(segments[0]['start_utc'])-datetime.timedelta(seconds=5);end=parse(segments[-1]['end_utc'])
thermal=[json.loads(l) for l in (O/'Thermal.jsonl').read_text().splitlines()];thermal=[r for r in thermal if start<=parse(r['utc'])<=end]
assert all(r['extent']==[[2560,1440,2560,1440,2560,1440,2560,1440]] and r['fractions']==[[1.,1.]] and r['active_window_fraction']==1. for r in rows)
out={'mode':'Native Development -game, editor closed','resolution':[2560,1440],'quality':'High','percentage':100,'continuous_process_elapsed_seconds_including_warmup':(end-start).total_seconds(),'utc':[start.isoformat(),end.isoformat()],'segments':[],'same_site_drift':{},'thermal_state_counts':dict(collections.Counter(r['thermal_label'] for r in thermal)),'thermal_samples':len(thermal),'temperature_or_clock_readback_available':False,'causal_throttling_claim':False}
for r in rows:out['segments'].append({k:r[k] for k in ['site','repeat','samples','median_fps','median_ms','p95_ms','utc','extent','window','fractions','active_window_fraction','csv']})
for site in ['Dorf','Wald','Weg']:
 rs=[r for r in rows if r['site']==site];assert [r['repeat'] for r in rs]==['1','2','3'];a,b=rs[0],rs[-1]
 out['same_site_drift'][site]={'round_fps':[r['median_fps'] for r in rs],'round_frame_ms':[r['median_ms'] for r in rs],'round_p95_ms':[r['p95_ms'] for r in rs],'last_vs_first_frame_percent':(b['median_ms']/a['median_ms']-1)*100}
assert 600<out['continuous_process_elapsed_seconds_including_warmup']<900
(O/'SustainedAnalysis.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='segments'},indent=2))
