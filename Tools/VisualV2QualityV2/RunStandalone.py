import subprocess,json,time,sys,os,csv
from pathlib import Path
W=Path(__file__).resolve().parents[2];O=W/'Saved/VisualV2QualityV2';S=W/'Saved/EnvironmentPerfV1';exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor'
for label in sys.argv[1:]:
 plan=W/'Tools/VisualV2QualityV2/Plans'/(label+'.tsv');lines=plan.read_text().splitlines();row=lines[1].split('\t');width,height,q,percentage=row[3:7]
 assert all(l.split('\t')[3:]==row[3:] for l in lines[1:] if l);assert not (S/(label+'_Done.txt')).exists()
 running=subprocess.check_output(['pgrep','-alf','UnrealEditor'],text=True)
 assert 'Contents/MacOS/UnrealEditor ' not in running, 'Close only clean editors before native timings; do not force quit'
 commands=['getall Engine bSmoothFrameRate','getall Engine bUseFixedFrameRate','getall GameUserSettings FrameRateLimit','getall GameUserSettings bUseVSync']
 commands+=['sg.'+n+'Quality '+q for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']]
 commands+=['rhi.SyncInterval','r.MotionBlurQuality','r.BloomQuality','r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor','r.Lumen.FinalGatherMethod','r.Shadow.Virtual.SMRT.RayCountDirectional','pm.EnvPerf.Run '+str(plan)]
 args=[exe,str(W/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_VisualV2','-game','-windowed','-ResX='+width,'-ResY='+height,'-ForceRes','-NoVSync','-NoSplash','-NoLiveCoding','-ModelContextProtocolPort=8009','-stdout','-FullStdOutLogOutput','-ExecCmds='+','.join(commands),'-ABSLOG='+str(O/(label+'_Engine.log'))]
 (O/(label+'_Launch.json')).write_text(json.dumps({'args':args,'mode':'Native editor binary -game, not packaged Shipping'},indent=2));print('START',label,flush=True)
 with (O/(label+'_Console.log')).open('w') as f:p=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT)
 start=time.monotonic();last=-1
 while p.poll() is None:
  time.sleep(4);f=S/(label+'_Segments.csv');count=len(list(csv.DictReader(f.open()))) if f.exists() else 0
  if count!=last:print(label,count,'/',len(lines)-1,flush=True);last=count
  if time.monotonic()-start>1600:raise TimeoutError('Process remains intact; inspect '+label)
 assert p.returncode==0,(label,p.returncode)
 assert (S/(label+'_Done.txt')).read_text()=='Complete',label
 print('DONE',label,flush=True);time.sleep(8)
