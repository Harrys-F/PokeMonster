"""Summarize actual V7 CSV windows, natural routes and scene protection. No measurements invented."""
from pathlib import Path
import csv,json,math,statistics,re,collections
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2PokemonTestGroundHealhouseV7'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def read(p):
 raw=list(csv.reader(p.open()));headers=next((r for r in reversed(raw)if r and r[0]=='EVENTS'),raw[0]);cols={k:[]for k in headers}
 for row in raw[1:]:
  if not row or row[0]=='EVENTS'or row[0].startswith('[HasHeaderRowAtEnd]'):continue
  values=dict(zip(headers,row))
  try:frame=float(values['FrameTime'])
  except(ValueError,TypeError,KeyError):continue
  if not math.isfinite(frame)or frame<=0:continue
  for k,v in values.items():
   try:x=float(v)
   except(ValueError,TypeError):continue
   if math.isfinite(x)and x>=0:cols[k].append(x)
 return cols
def stats(cols):
 ts=sorted(x for x in cols['FrameTime']if x>0);wanted=['FrameTime','GPUTime','GameThreadTime','RenderThreadTime','GPU/Basepass','GPU/ShadowDepths','GPU/LumenIrradianceFieldGather'];return dict(frames=len(ts),fps=1000/statistics.mean(ts),p95_ms=ts[min(len(ts)-1,int(len(ts)*.95))],one_percent_low_fps=1000/statistics.mean(ts[-max(1,math.ceil(len(ts)*.01)):]),max_frame_ms=max(ts),counters={k:statistics.mean(cols[k])if cols.get(k)and any(cols[k])else None for k in wanted})
results={}
for label in ['NativeBefore01','NativeAfter01']+[x for x in ['NativeAfter02','NativeAfterFinal01']if(D/x/'Result.json').exists()]:
 data=load(D/label/'Result.json');assert data['passed'];groups={};windows=[]
 for row in data['rows']:
  cols=read(D/label/'UserData/Saved/Profiling/CSV'/(row['csv_prefix']+'.csv'));windows.append(dict(site=row['site'],repeat=row['repeat'],**stats(cols)));group=groups.setdefault(row['site'],{})
  for k,v in cols.items():group.setdefault(k,[]).extend(v)
 results[label]=dict(windows=windows,sites={k:stats(v)for k,v in groups.items()})
results['pond']={}
for label in ['NativePondBefore01','NativePondAfter01','NativePondCoverage01']+(['NativePondFinal01']if(D/'NativePondFinal01/Result.json').exists()else[]):
 data=load(D/label/'Result.json');assert data['passed'],data['error'];c=next(x for x in data['checks']if isinstance(x,dict)and'samples'in x);ss=c['samples'];cx,cy=c['zone'][:2];ex,ey=c['zone_extent'][:2];sectors=collections.Counter();normr=[]
 for s in ss:
  x,y=s['foot'][:2];a=math.atan2((y-cy)/ey,(x-cx)/ex);sectors[max(0,min(7,int((a+math.pi)/(math.pi/4))))]+=1;normr.append(math.hypot((x-cx)/(ex-50),(y-cy)/(ey-50)))
 results['pond'][label]=dict(seconds=c['observation_seconds'],distance_m=sum(math.dist(a['foot'][:2],b['foot'][:2])for a,b in zip(ss,ss[1:]))/100,component_counter_since_spawn_m=c.get('distance_total_cm',c['distance_cm'])/100,plans=c['plans'],blocked_steps=c['blocked'],samples=len(ss),moving_percent=100*sum(s['speed']>1 for s in ss)/len(ss),states=dict(collections.Counter(s['state']for s in ss)),x_range_cm=[min(s['foot'][0]for s in ss),max(s['foot'][0]for s in ss)],y_range_cm=[min(s['foot'][1]for s in ss),max(s['foot'][1]for s in ss)],sectors=dict(sectors),max_eroded_ellipse_radius=max(normr),mean_tick_us=c['tick_us']/max(1,c['ticks']),planning_us=c['planning_us'],settings=c['settings'],activities=c['activities'])
# Actual measured routes, explicitly a data visualization rather than an Unreal screenshot.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="650" viewBox="0 0 1200 650"><rect width="1200" height="650" fill="#15242b"/>']
for j,label in enumerate(['NativePondBefore01','NativePondFinal01'if(D/'NativePondFinal01/Result.json').exists()else'NativePondCoverage01']):
 c=next(x for x in load(D/label/'Result.json')['checks']if isinstance(x,dict)and'samples'in x);x0=40+j*600;y0=80;cx,cy=c['zone'][:2];ex,ey=c['zone_extent'][:2]
 def xy(x,y):return x0+260+(x-cx)*.29,y0+240-(y-cy)*.29
 svg.append(f'<text x="{x0}" y="35" fill="white" font-family="sans-serif" font-size="20">'+('Vorher: 240 s'if j==0 else'Nachher: 360 s, entfernter Uferstandpunkt')+'</text>');svg.append(f'<ellipse cx="{x0+260}" cy="{y0+240}" rx="{ex*.29}" ry="{ey*.29}" fill="#24454d" stroke="#7aaeb3"/>')
 if j==1:
  for g in load(D/label/'SwimmableGrid.json')['points']:
   if g['safe_foot']:
    x,y=xy(g['x'],g['y']);svg.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2" fill="#9ac594"/>')
 points=' '.join(f'{xy(s["foot"][0],s["foot"][1])[0]:.2f},{xy(s["foot"][0],s["foot"][1])[1]:.2f}'for s in c['samples']);svg.append(f'<polyline points="{points}" fill="none" stroke="#ffd783" stroke-width="2"/>');x,y=xy(*c['samples'][0]['foot'][:2]);svg.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5" fill="white"/>');v=results['pond'][label];svg.append(f'<text x="{x0}" y="560" fill="white" font-family="sans-serif" font-size="17">Strecke {v["distance_m"]:.1f} m; {v["blocked_steps"]} blockierte Schritte</text>')
svg.append('<text x="40" y="610" fill="#bfccd1" font-family="sans-serif" font-size="16">Draufsicht aus echten Positionsdaten; gruen: erfolgreich tiefen-/kollisionsgepruefte Rasterpunkte; weiss: Start</text></svg>');(D/'KarpadorRoute.svg').write_text(''.join(svg))
if(D/'NativeGameplay01/Result.json').exists():
 assert load(D/'NativeGameplay01/Result.json')['passed'];results['native_dynamic_tour']=stats(read(D/'NativeGameplay01/UserData/Saved/Profiling/CSV/FAB_NativeGameplay01_Tour.csv'))
if(D/'SceneAfter.json').exists():
 before=load(D/'SceneBefore.json');after=load(D/'SceneAfter.json');assert before['world_settings']==after['world_settings'];assert set(before['actors'])==set(after['actors']);changed=[]
 for key,row in before['actors'].items():
  other=after['actors'][key]
  if row!=other:
   changed.append(row['label']);assert 16000<row['transform'][0][0]<17700,(row['label'],'outside protected room')
   for v in [row,other]:
    for c in v['components']:c.pop('materials',None)
   assert row==other,(row['label'],'non-material scene change')
 results['scene_protection']=dict(actor_count=len(before['actors']),changed_room_material_actors=changed,other_actor_data_identical=True)
pair=D/'NativePairedCost01/Result.json'
if pair.exists():
 data=load(pair);assert data['passed'];groups={};windows=[]
 for row in data['rows']:
  cols=read(pair.parent/'UserData/Saved/Profiling/CSV'/(row['csv_prefix']+'.csv'));windows.append(dict(site=row['site'],repeat=row['repeat'],**stats(cols)));g=groups.setdefault(row['site'],{})
  for k,v in cols.items():g.setdefault(k,[]).extend(v)
 results['paired_cost']=dict(windows=windows,sites={k:stats(v)for k,v in groups.items()})
(D/'Analysis.json').write_text(json.dumps(results,indent=2));print({k:{s:round(v['fps'],2)for s,v in results[k]['sites'].items()}for k in ['NativeBefore01','NativeAfter01']+[x for x in ['NativeAfter02','NativeAfterFinal01']if x in results]});print('Pond',{k:(round(v['distance_m'],1),round(v['moving_percent'],1),v['sectors'])for k,v in results['pond'].items()})
