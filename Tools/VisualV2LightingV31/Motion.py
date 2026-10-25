"""Reuse native presented-frame movement evidence at canopy edge and dense forest."""
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve()
s=(R/'Tools/VisualV2EnvironmentV3/Motion.py').read_text().replace('Saved/ProjectRefinement/EnvironmentV3/MotionFinal','Saved/ProjectRefinement/LightingV31/Motion').replace("clips=[('Grass',-2100,-1760),('Water',-350,-130)]", "clips=[('CanopyEdge',-1500,500),('DenseForest',-1300,-850)]").replace('EnvironmentV3_Final_','LightingV31_Final_')
exec(compile(s,'existing_native_motion_capture','exec'),globals())
