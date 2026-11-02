"""Reuse the existing Westland gameplay review verbatim in this task's isolated storage."""
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve();source=R/'Tools/WestlandIntegrationV1/QuickReview.py'
text=source.read_text();assert text.count("D=R/'Saved/ProjectRefinement/WestlandIntegrationV1'")==1
text=text.replace("D=R/'Saved/ProjectRefinement/WestlandIntegrationV1'","D=R/'Saved/ProjectRefinement/WestlandVisualUpgradeV1'").replace('PokeMonster_SaveV2_Test_WestlandIntegrationV1_','PokeMonster_SaveV2_Test_WestlandVisualUpgradeV1_')
exec(compile(text,str(source),'exec'),{'__name__':'__main__'})
