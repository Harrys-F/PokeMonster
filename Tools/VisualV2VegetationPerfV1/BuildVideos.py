"""Actual timestamps and images only. Run AFTER all performance measurements."""
from pathlib import Path
import json,csv,os,subprocess
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2VegetationPerfV1';assert (S/'PipelineComplete.json').exists();O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/Videos');O.mkdir(exist_ok=False);encoder=R/'Saved/VisualV2TAAIntegrationV1/EncodeRecording'
if not encoder.exists():
 encoder=S/'EncodeRecording';assert not encoder.exists();subprocess.run(['swiftc',str(R/'Tools/VisualV2TAAIntegrationV1/EncodeRecording.swift'),'-o',str(encoder)],check=True)
manifest=[]
for w,h,q,sp,name in [(1280,720,1,75,'720p_Medium75'),(2560,1440,2,100,'QHD_High100')]:
 for variant in ['Control','FullyRough']:
  label=f'MotionR2_{w}_{h}_Q{q}_SP{sp}_{variant}';result=json.loads((S/'Motion'/label/'Result.json').read_text());assert result['error'] is None;directory=Path(result['recording']);rows=list(csv.DictReader((directory/'Frames.csv').open()));t0=next(x['t'] for x in result['records'] if x['stage']=='IdleForest');end=next(x['t'] for x in result['records'] if x['stage']=='TalkSetup')-t0-.5;rows=[x for x in rows if float(x['game_seconds'])<=end];assert len(rows)>50
  inputs=S/'VideoSources'/(variant+'_'+name);inputs.mkdir(parents=True,exist_ok=False)
  for f in rows:os.link(directory/f['file'],inputs/f['file'])
  offset=float(rows[0]['game_seconds'])
  for i,f in enumerate(rows):f['frame']=i;f['game_seconds']=f"{float(f['game_seconds'])-offset:.9f}"
  with (inputs/'Frames.csv').open('w') as f:writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
  output=O/(variant+'_'+name+'.mp4');r=subprocess.run([str(encoder),str(inputs),str(output)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(O/(output.stem+'_Encode.log')).write_text(r.stdout);r.check_returncode();assert output.stat().st_size>10000
  manifest.append({'video':str(output),'source':str(directory),'frames':len(rows),'duration_last_timestamp_s':float(rows[-1]['game_seconds']),'trimmed_before_explicit_test_reposition':True,'interpolated':False,'mean_source_fps':(len(rows)-1)/float(rows[-1]['game_seconds'])});print(output.name,'encoded',len(rows),'real frames',flush=True)
(O/'Manifest.json').write_text(json.dumps(manifest,indent=2))
