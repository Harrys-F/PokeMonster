"""Sequential standalone matrix, then actual gameplay. Requires closed editor."""
from pathlib import Path
import subprocess,os
R=Path(__file__).resolve().parents[2]
def run(script,*args):subprocess.run(['python3',str(R/'Tools/VisualV2TAAIntegrationV1'/script),*map(str,args)],check=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
for ci in range(1,7):run('RunPhase.py','Standalone',ci)
run('RunAcceptance.py','Standalone','Integrated_Standalone_720p_Medium75',1280,720,75)
run('RunAcceptance.py','Standalone','Integrated_Standalone_QHD_Medium100',2560,1440,100)
# Complete paired replacements for diagnosed terminal-counter output loss.
run('RunPhase.py','Standalone','Recheck2')
run('RunPhase.py','Standalone','Recheck3')
run('RunPhase.py','Standalone','Recheck4')
run('RunPhase.py','Standalone','Recheck5')
print('NATIVE_VALIDATION_COMPLETE',flush=True)
