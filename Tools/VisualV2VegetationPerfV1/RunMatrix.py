"""Run each config in a fresh play world; never change quality while reveal MIDs live."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2VegetationPerfV1';mode=sys.argv[1];assert mode in ['PIE','Standalone']
if mode=='Standalone':
 print('WAITING_FOR_PIE_VISUAL_AND_DATA_REVIEW',flush=True);start=__import__('time').monotonic()
 while not (S/'ReleaseNative.txt').exists():
  __import__('time').sleep(3);assert __import__('time').monotonic()-start<1800,'Native gate not released; preserve results'
for ci in range(1,9):
 dest=S/(f'Runner_{mode}_C{ci}.log');assert not dest.exists();print('START',mode,ci,flush=True)
 with dest.open('w') as f:r=subprocess.run(['python3',str(R/'Tools/VisualV2VegetationPerfV1/RunPhase.py'),mode,str(ci)],cwd=R,stdout=f,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 if r.returncode:print(dest.read_text()[-2500:],flush=True);raise SystemExit(r.returncode)
 print('COMPLETE',mode,ci,flush=True)
print('MATRIX_COMPLETE',mode,flush=True)
