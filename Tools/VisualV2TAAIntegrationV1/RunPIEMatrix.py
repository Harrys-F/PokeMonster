"""Finish the first completed pilot, then the remaining paired PIE matrix."""
from pathlib import Path
import subprocess,time,os
R=Path(__file__).resolve().parents[2];P=R/'Saved/EnvironmentPerfV2';start=time.monotonic();f=P/'VGB1_TAAIntegration_PIE_C1_Done.txt'
while not f.exists():time.sleep(3);assert time.monotonic()-start<900
assert f.read_text()=='Complete';time.sleep(6)
for ci in range(2,7):subprocess.run(['python3',str(R/'Tools/VisualV2TAAIntegrationV1/RunPhase.py'),'PIE',str(ci)],check=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
print('PIE_MATRIX_COMPLETE',flush=True)
