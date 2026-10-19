"""Quality is set before PIE/native startup, never toggled over live reveal MIDs."""
from pathlib import Path
import subprocess,time,json,csv,sys
from Control import R,O,job
mode,q=sys.argv[1:];q=int(q);assert mode in ['PIE','Standalone'];label=f'VGB1_WAQ2_Final_{mode}_Q{q}';plan=R/'Tools/VisualV2WorldArtQualityV2/Plans'/(label+'.tsv');(O/'StudyRequest.json').write_text(json.dumps({'label':label,'mode':mode,'quality':q,'kind':'matrix'}));(O/'Request.json').write_text(json.dumps({'label':label,'config':[1280,720,q,75]}));P=R/'Saved/EnvironmentPerfV2';assert not (P/(label+'_Done.txt')).exists();process=None
if mode=='PIE':job('Preset.py');time.sleep(5);job('StartPIE.py');time.sleep(4);job('RuntimeMatrix.py')
else:
 assert 'Contents/MacOS/UnrealEditor ' not in subprocess.run(['pgrep','-alf','UnrealEditor'],text=True,capture_output=True).stdout
 args=['/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor',str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_VisualV2','-game','-windowed','-ResX=1280','-ResY=720','-ForceRes','-NoVSync','-NoSplash','-NoLiveCoding','-ModelContextProtocolPort=8016','-ExecCmds='+','.join(['sg.'+n+'Quality '+str(q) for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']]+['py '+str(R/'Tools/VisualV2WorldArtQualityV2/NativeStudy.py')]),'-ABSLOG='+str(O/(label+'_Engine.log'))];f=(O/(label+'_Console.log')).open('w');process=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT)
start=time.monotonic();last=-1
while not (P/(label+'_Done.txt')).exists():
 time.sleep(3);p=P/(label+'_Segments.csv');n=len(list(csv.DictReader(p.open()))) if p.exists() else 0
 if n!=last:print(label,n,'/',len(plan.read_text().splitlines())-1,flush=True);last=n
 if (O/(label+'_Error.txt')).exists():raise RuntimeError((O/(label+'_Error.txt')).read_text())
 if process and process.poll() is not None and not (P/(label+'_Done.txt')).exists():raise RuntimeError('Unexpected native exit '+str(process.returncode))
 assert time.monotonic()-start<1000
assert (P/(label+'_Done.txt')).read_text()=='Complete'
if mode=='PIE':time.sleep(2);job('StopPIE.py')
else:assert process.wait(timeout=40)==0;f.close()
print('MATRIX COMPLETE',label,flush=True)
