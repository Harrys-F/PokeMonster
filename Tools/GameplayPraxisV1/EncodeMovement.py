"""Encode only genuine presented frames and original game timestamps, no interpolation."""
from pathlib import Path
R=Path(__file__).resolve().parents[2]
s=(R/'Tools/VisualV2EnvironmentV3/EncodeMotion.py').read_text().replace('Saved/ProjectRefinement/EnvironmentV3/MotionFinal','Saved/ProjectRefinement/GameplayPraxisV1/Movement01/Motion')
exec(compile(s,'existing_native_encoder','exec'),globals())
