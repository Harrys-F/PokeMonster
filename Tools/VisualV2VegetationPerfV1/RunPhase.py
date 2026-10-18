import subprocess,time,json,sys,csv
from pathlib import Path
from Control import R,O,job
mode,ci=sys.argv[1:];assert mode in ['PIE','Standalone'];label=f'VGB1_Vegetation_{mode}_C{ci}';plan=R/'Tools/VisualV2VegetationPerfV1/Plans'/(label+'.tsv');config=list(map(int,plan.read_text().splitlines()[1].split('\t')[3:]));P=R/'Saved/EnvironmentPerfV2';assert not (P/(label+'_Done.txt')).exists();(O/'Request.json').write_text(json.dumps({'label':label,'mode':mode,'config':config}));process=None
if mode=='PIE':job('Preset.py');time.sleep(8);job('StartPIE.py');time.sleep(4);job('BeginPhase.py')
else:
 assert 'Contents/MacOS/UnrealEditor ' not in subprocess.run(['pgrep','-alf','UnrealEditor'],text=True,capture_output=True).stdout
 args=['/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor',str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1','-game','-windowed','-ResX='+str(config[0]),'-ResY='+str(config[1]),'-ForceRes','-NoVSync','-NoSplash','-NoLiveCoding','-ModelContextProtocolPort=8016','-ExecCmds='+','.join(['sg.'+n+'Quality '+str(config[2]) for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']]+['py '+str(R/'Tools/VisualV2VegetationPerfV1/NativePhase.py')]),'-ABSLOG='+str(O/(label+'_Engine.log'))];f=(O/(label+'_Console.log')).open('w');process=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT)
start=time.monotonic();last=-1
while not (P/(label+'_Done.txt')).exists():
 time.sleep(3);p=P/(label+'_Segments.csv');n=len(list(csv.DictReader(p.open()))) if p.exists() else 0
 if n!=last:print(label,n,'/',len(plan.read_text().splitlines())-1,flush=True);last=n
 if process and process.poll() is not None:assert (P/(label+'_Done.txt')).exists(),('Native process exited',process.returncode)
 assert time.monotonic()-start<1600,'Preserve timed-out editor for inspection'
assert (P/(label+'_Done.txt')).read_text()=='Complete'
if mode=='PIE':time.sleep(3);job('StopPIE.py')
else:assert process.wait(timeout=40)==0;f.close()
print('PHASE_COMPLETE',label,flush=True)
