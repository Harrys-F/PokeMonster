import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();rows=[]
for p in ['/Game/Data/Creatures/'+n for n in ['DA_TestGrass','DA_TestWater','DA_TestFire','DA_Zunderlauf']]:
 a=unreal.load_asset(p)
 if a:rows.append({'path':a.get_path_name(),'id':str(a.get_internal_id()),'visible_name':str(a.get_display_name()),'presentation':a.visuals.presentation.get_path_name()if a.visuals.presentation else None})
(R/'Saved/GlumandaV11/SpeciesNames.json').write_text(json.dumps(rows,indent=2));print(rows)
