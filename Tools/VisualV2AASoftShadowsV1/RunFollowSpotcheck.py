"""Explicit test runner. No save/asset changes; renderer settings restored by probe."""
import subprocess,time,json,sys,csv
from pathlib import Path
from Control import job,R,O
mode=sys.argv[1];assert mode in ['PIE','Standalone'];label='VGB1_AASoftShadows_FinalFollow_'+mode;config=[2560,1440,2,100];P=R/'Saved/EnvironmentPerfV2';assert not (P/(label+'_Done.txt')).exists();(O/'Request.json').write_text(json.dumps({'label':label,'mode':mode,'config':config}));p=None
if mode=='PIE':
 job('Preset.py');time.sleep(10);job('StartPIE.py');time.sleep(4);job('BeginPhase.py')
else:
 running=subprocess.run(['pgrep','-alf','UnrealEditor'],text=True,capture_output=True).stdout;assert 'Contents/MacOS/UnrealEditor ' not in running
 args=['/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor',str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1','-game','-windowed','-ResX='+str(config[0]),'-ResY='+str(config[1]),'-ForceRes','-NoVSync','-NoSplash','-NoLiveCoding','-ModelContextProtocolPort=8016','-ExecCmds='+','.join(['sg.'+n+'Quality '+str(config[2]) for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']]+['py '+str(R/'Tools/VisualV2AASoftShadowsV1/NativePhase.py')]),'-ABSLOG='+str(O/(label+'_Engine.log'))]
 f=(O/(label+'_Console.log')).open('w');p=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT)
start=time.monotonic();last=-1
while not (P/(label+'_Done.txt')).exists():
 time.sleep(3);seg=P/(label+'_Segments.csv');n=len(list(csv.DictReader(seg.open()))) if seg.exists() else 0
 if n!=last:print(label,n,'/'+str(len((R/'Tools/VisualV2AASoftShadowsV1/Plans'/(label+'.tsv')).read_text().splitlines())-1),flush=True);last=n
 if p and p.poll() is not None and not (P/(label+'_Done.txt')).exists():raise RuntimeError('Unexpected native exit '+str(p.returncode))
 assert time.monotonic()-start<1400,'Timeout: preserve process for inspection'
assert (P/(label+'_Done.txt')).read_text()=='Complete'
if mode=='PIE':time.sleep(4);job('StopPIE.py')
else:assert p.wait(timeout=40)==0;f.close()
print('PHASE COMPLETE',label,flush=True)
