"""Sequential existing acceptance runners, stop at first failed outcome; never overlap PIE sessions."""
from pathlib import Path
import subprocess
R=Path(__file__).resolve().parents[2]
cases=[['Tools/CreatureExpansionV3/RunEncounter.py','PolishV4EntonKO','Enton','SHY','Victory'],['Tools/CreatureExpansionV3/RunEncounter.py','PolishV4NebulakKO','Nebulak','SHY','Victory'],['Tools/StarterExpansionV1/RunDefeatSave.py','PolishV4Defeat'],['Tools/WildEncountersV2/RunWorldOutcome.py','PolishV4WorldOutcome']]
for args in cases:
 print('BEGIN',args[1],flush=True);subprocess.run(['python3',*args],cwd=R,check=True)
