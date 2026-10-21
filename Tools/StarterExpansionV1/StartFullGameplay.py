"""Reuse the project's established complete route; add read-only companion observations."""
import unreal,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();runpy.run_path(str(R/'Tools/GlumandaV11/StartGameplay.py'),run_name='__main__');runpy.run_path(str(R/'Tools/StarterExpansionV1/ObserveCompanion.py'),run_name='__main__')
