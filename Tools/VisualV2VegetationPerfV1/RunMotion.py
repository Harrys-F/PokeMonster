"""Same real input route for original/candidate, recorded separately from timings."""
import json,time,sys
from pathlib import Path
from Control import R,O,job
w,h,q,sp=map(int,sys.argv[1:5]);variant=sys.argv[5];assert variant in ['Control','FullyRough'];label=f'MotionR2_{w}_{h}_Q{q}_SP{sp}_{variant}';assert not (O/'Motion'/label).exists();probe='VGB1_Vegetation_'+label;recording=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('VegetationPerfV1_'+label)
plan=O/'MotionPlans'/(probe+'.tsv');plan.parent.mkdir(exist_ok=True);assert not plan.exists();plan.write_text(probe+'\tPIE\t5\t90\n'+'\t'.join(map(str,['Wald','VegPerf:'+variant,90,w,h,q,sp]))+'\n')
(O/'Request.json').write_text(json.dumps({'label':label,'config':[w,h,q,sp]}));(O/'MotionRequest.json').write_text(json.dumps({'label':label,'width':w,'height':h,'quality':q,'percentage':sp,'aa':2,'variant':variant,'probe_label':probe,'probe_plan':str(plan),'recording':str(recording)}));job('Preset.py');time.sleep(5);job('StartPIE.py');time.sleep(3);job('StartMotion.py');start=time.monotonic()
while not (O/'Motion'/label/'Result.json').exists():time.sleep(2);assert time.monotonic()-start<180
r=json.loads((O/'Motion'/label/'Result.json').read_text());assert r['error'] is None,r['error']
while not (recording/'Complete.txt').exists():time.sleep(1);assert time.monotonic()-start<210
job('StopProbe.py');job('StopPIE.py');print('MOTION_COMPLETE',label,'frames',(recording/'Complete.txt').read_text(),flush=True)
