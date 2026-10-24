"""Reuse the guarded in-project editor queue, then open only the existing sandbox map."""
import runpy,unreal
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();runpy.run_path(str(R/'Tools/ProjectMaintenance/ArtSession.py'),run_name='__main__')
assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_BiomeTestMap_V1')
