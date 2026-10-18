"""Fresh fixed-quality sessions; all four factors interleaved. Stop on the first failure."""
import subprocess,sys,time,json
from pathlib import Path
from Control import job,R,O
mode=sys.argv[1];assert mode in ['PIE','Standalone']
for k in range(1,9):
 p=subprocess.run([sys.executable,str(R/'Tools/VisualV2AASoftShadowsV1/RunPhase.py'),mode,str(k)],cwd=R)
 assert p.returncode==0,(mode,k,p.returncode)
print('ALL CONFIGURATIONS COMPLETE',mode,flush=True)
if mode=='Standalone':
 p=subprocess.run([sys.executable,str(R/'Tools/VisualV2AASoftShadowsV1/RunCost.py'),mode],cwd=R);assert p.returncode==0,('Cost',p.returncode)
if mode=='PIE':job('CloseEditor.py')
