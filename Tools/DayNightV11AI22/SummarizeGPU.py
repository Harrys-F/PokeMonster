"""Summarize native CSV GPU/frame scopes; retain per-repetition medians/ranges."""
import csv,json,statistics
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/DayNightV11AI22';rows=[]
for result in sorted(D.glob('GPU*/Result.json')):
 data=json.loads(result.read_text())
 if not data.get('passed'):continue
 for case in data['cases']:
  label=case['label'];segments=list(csv.DictReader((R/'Saved/EnvironmentPerfV2'/(label+'_Segments.csv')).open()))
  for seg in segments:
   p=R/'Saved/Profiling/CSV'/('ENV2_'+label+'_%03d.csv'%int(seg['segment']));values={k:[] for k in ['FrameTime','GPUTime','GPU/ShadowDepths','GPU/ShadowProjection','GPU/DistanceFieldShadows','GPU/Lights','GPU/Basepass']}
   for row in csv.DictReader(p.open()):
    for k in values:
     try:
      v=float(row[k])
      if v>=0:values[k].append(v)
     except (KeyError,ValueError,TypeError):pass
   rows.append({'label':label,'site':seg['site'],'repeat':int(seg['repeat']),'frames':len(values['GPUTime']),**{k:statistics.median(v)if v else None for k,v in values.items()}})
(D/'GPUSummary.json').write_text(json.dumps(rows,indent=2))
for label in dict.fromkeys(r['label']for r in rows):
 for site in ['Dorf','Wald']:
  group=[r for r in rows if r['label']==label and r['site']==site]
  print(label,site,{k:[round(min(r[k]for r in group),3),round(statistics.median(r[k]for r in group),3),round(max(r[k]for r in group),3)]for k in ['GPUTime','FrameTime','GPU/ShadowDepths']})
