"""Existing regional gameplay regression, scoped to this task's isolated editor."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualV2IntegrationV1';label=json.loads((D/'Request.json').read_text())['label'];(D/'Active.json').write_text(json.dumps(dict(label=label)))
source=R/'Tools/WestlandIntegrationV1/QuickReview.py';s=source.read_text().replace("D=R/'Saved/ProjectRefinement/WestlandIntegrationV1'","D=R/'Saved/ProjectRefinement/WestlandVisualV2IntegrationV1'").replace('PokeMonster_SaveV2_Test_WestlandIntegrationV1_','PokeMonster_SaveV2_Test_WVI_');s=s.replace('times=[6,12,19,22]','times=[0,5,6,9,12,16,19,22]');exec(compile(s,str(source),'exec'),{'__name__':'__main__'})
