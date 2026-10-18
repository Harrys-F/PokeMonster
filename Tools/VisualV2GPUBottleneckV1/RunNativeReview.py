import subprocess,time,json
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/VisualV2GPUBottleneckV1';label='VGB1_Final_Native_Review';assert not (O/'Screenshots'/label).exists()
factors=['Control','CV:r.AntiAliasingMethod=2','CV:r.AntiAliasingMethod=0','CV:r.TSR.AsyncCompute=0','CV:r.Lumen.DiffuseIndirect.Allow=0','CV:r.Lumen.Reflections.Allow=0','CV:r.Shadow.Virtual.Enable=0','CV:r.Shadow.Virtual.SMRT.RayCountDirectional=2','CV:r.Shadow.Virtual.Cache=0','AllShadowsOff','VegetationNoShadow','VegetationHidden','VegetationDefaultMaterial','CV:r.Nanite=0','PostProcessingOff','CV:r.Lumen.HardwareRayTracing=0','Control']
rows=[]
for site,pos,conditions in [('Wald',[-4300,1550,50.15],factors),('Dorf',[-4100,450,50.15],['Control','CV:r.Lumen.DiffuseIndirect.Allow=0','CV:r.Shadow.Virtual.Enable=0','PostProcessingOff','Control']),('Weg',[-36.6,-47.1,50.15],['Control','CV:r.Lumen.DiffuseIndirect.Allow=0','AllShadowsOff','PostProcessingOff','Control'])]:
 for i,c in enumerate(conditions):rows.append({'site':site,'position':pos,'condition':c,'tag':str(i).zfill(2)})
(O/'ReviewRequest.json').write_text(json.dumps({'label':label,'mode':'ReviewNative','quality':2,'percentage':100,'rows':rows},indent=2))
commands=['sg.'+n+'Quality 2' for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']]+['py '+str(R/'Tools/VisualV2GPUBottleneckV1/NativeReview.py')]
a=['/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor',str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1','-game','-windowed','-ForceRes','-ResX=2560','-ResY=1440','-NoVSync','-NoLiveCoding','-ModelContextProtocolPort=8012','-ExecCmds='+','.join(commands),'-ABSLOG='+str(O/(label+'_Engine.log'))]
with (O/(label+'_Console.log')).open('w') as f:
 p=subprocess.Popen(a,stdout=f,stderr=subprocess.STDOUT);begin=time.monotonic()
 while p.poll() is None:
  time.sleep(3)
  assert not (O/(label+'_ReviewFailure.txt')).exists(),'Review callback failed; inspect surviving process'
  assert time.monotonic()-begin<700,'Timeout; process preserved'
 assert p.returncode==0
r=json.loads((O/'Screenshots'/label/'Review.json').read_text());assert not r['error'] and len(r['rows'])==len(rows);print('REAL NATIVE QHD REVIEW',len(rows),'captures')
