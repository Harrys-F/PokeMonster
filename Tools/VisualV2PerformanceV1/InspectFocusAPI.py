import unreal,json
from pathlib import Path
p=Path(unreal.Paths.project_saved_dir())/'ProjectRefinement/VisualV2PerformanceV1/FocusAPI.json';p.write_text(json.dumps({n:[x for x in dir(getattr(unreal,n))if 'focus'in x.lower()or'input_mode'in x.lower()]for n in dir(unreal)if n.endswith('Library')and ('Widget'in n or'Gameplay'in n)},indent=2))
