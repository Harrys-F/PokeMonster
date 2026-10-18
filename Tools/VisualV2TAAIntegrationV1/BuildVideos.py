"""Encode only genuine chronological frames. Trim explicit test repositioning out of forest clips."""
from pathlib import Path
import json,csv,os,subprocess
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2TAAIntegrationV1';O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/Videos');O.mkdir(exist_ok=True);encoder=S/'EncodeRecording';manifest=[]
choices=[('TSR_720p_Medium75','PreMotion_1280_720_Q1_SP75_A'),('TAA_Integrated_720p_Medium75','IntegratedMotion_1280_720_Q1_SP75'),('TSR_QHD_Medium75','PreMotion_2560_1440_Q1_SP75_A'),('TAA_Integrated_QHD_Medium75','IntegratedMotion_2560_1440_Q1_SP75'),('TSR_QHD_High100','PreMotion_2560_1440_Q2_SP100_A'),('TAA_Integrated_QHD_High100','IntegratedMotion_2560_1440_Q2_SP100')]
for label,source_label in choices:
 output=O/(label+'.mp4')
 if output.exists():continue
 d=json.loads((S/'Motion'/source_label/'Result.json').read_text());start=next(x['t'] for x in d['records'] if x['stage']=='IdleForest');end=next(x['t'] for x in d['records'] if x['stage']=='TalkSetup')-start-.1;directory=S/'Recordings'/source_label;rows=list(csv.DictReader((directory/'Frames.csv').open()));rows=[x for x in rows if float(x['game_seconds'])<=end];assert rows;inputs=S/'VideoSources'/label;inputs.mkdir(parents=True,exist_ok=True)
 for f in rows:
  target=inputs/f['file']
  if target.exists():assert os.path.samefile(directory/f['file'],target)
  else:os.link(directory/f['file'],target)
 offset=float(rows[0]['game_seconds'])
 for i,f in enumerate(rows):f['frame']=i;f['game_seconds']=f"{float(f['game_seconds'])-offset:.9f}"
 with (inputs/'Frames.csv').open('w') as f:writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
 result=subprocess.run([str(encoder),str(inputs),str(output)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(O/(label+'_Encode.log')).write_text(result.stdout);print(label,result.stdout.splitlines()[-1] if result.stdout else result.returncode,flush=True);result.check_returncode();manifest.append({'video':str(output),'source':source_label,'frames':len(rows),'last_game_seconds':float(rows[-1]['game_seconds']),'trimmed_before_explicit_reposition':True,'interpolated':False})
for p in (S/'Acceptance').glob('*/DoorRecording.json'):
 d=json.loads(p.read_text());directory=Path(d['recording']);output=O/('Door_'+p.parent.name+'.mp4')
 if output.exists():continue
 result=subprocess.run([str(encoder),str(directory),str(output)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(O/(output.stem+'_Encode.log')).write_text(result.stdout);print(output.name,result.stdout.splitlines()[-1] if result.stdout else result.returncode,flush=True);result.check_returncode();manifest.append({'video':str(output),'source':str(directory),'full_real_gameplay_segment':True,'test_teleports':False,'interpolated':False})
# Append without losing proof from previously encoded clips.
p=O/'Manifest.json';previous=json.loads(p.read_text()) if p.exists() else [];p.write_text(json.dumps(previous+manifest,indent=2))
