import unreal
from pathlib import Path
Path(unreal.Paths.project_saved_dir(),'ProjectRefinement/GameplayPraxisV1/TraceAPI.txt').write_text(str(unreal.SystemLibrary.capsule_trace_single.__doc__))
