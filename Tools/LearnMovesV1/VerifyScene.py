"""Reuse the exact scene/protected-world comparison with a distinct phase B result."""
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve();s=(R/'Tools/SaveSystemV2/VerifyScene.py').read_text().replace("D/'SceneUnchanged_A.json'","R/'Saved/ProjectRefinement/LearnMovesV1/SceneUnchanged_B.json'");exec(compile(s,'existing_scene_comparison_phase_b','exec'),globals())
