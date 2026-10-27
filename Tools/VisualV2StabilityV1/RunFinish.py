from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2StabilityV1';assert json.loads((D/'InterleavedMaterial01/Result.json').read_text())['passed']
for args in [('stop_pie',),('script','Tools/VisualV2StabilityV1/MapChecksFinal.py'),('script','Tools/VisualV2StabilityV1/Restore.py'),('close',)]:subprocess.run(['python3','-B',str(R/'Tools/ProjectMaintenance/ArtControl.py'),*args],cwd=R,check=True)
print('EDITOR_REGULAR_CLOSE_REQUESTED',flush=True)
