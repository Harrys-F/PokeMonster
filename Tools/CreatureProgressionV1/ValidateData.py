"""Current read-only validation; immutable V1 snapshot remains provenance, not current support state."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).resolve().parents[1]/'MoveEffectsV4/ValidateCrystalData.py'),run_name='__main__')
