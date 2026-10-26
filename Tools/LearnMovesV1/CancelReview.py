"""End only this explicitly owned review callback; retain a failed result and ordinary PIE teardown."""
from pathlib import Path
import unreal,json
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/LearnMovesV1';q=json.loads((D/'Request.json').read_text());O=D/q['label'];assert q['kind']=='learning'and q['label']=='Learning01'and not(O/'Result.json').exists();unreal.unregister_slate_post_tick_callback(unreal._learn_v1)
(O/'Result.json').write_text(json.dumps(dict(passed=False,cases=[],error='Review adapter selected Splash for free-slot Karpador; a no-damage move cannot defeat the one-HP target. First five completed cases retained in Progress and actual captures. No gameplay failure; cancel owned test and select Tackle in corrected adapter.'),indent=2))
