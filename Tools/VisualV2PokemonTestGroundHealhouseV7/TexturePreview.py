import unreal
from pathlib import Path
D=Path(unreal.Paths.project_dir())/'Saved/ProjectRefinement/VisualV2PokemonTestGroundHealhouseV7/TexturePreviews';D.mkdir(exist_ok=True)
for name in ['Wall_1','Wall_2','Wall_3','Wooden_Floor_1','Wooden_Floor_2','Wooden_Floor_3']:
 a=unreal.load_asset('/Game/Pack_Bonus/Textures/'+name+'/T_Pack_Bonus_'+name+'_basecolor');t=unreal.AssetExportTask();t.object=a;t.filename=str(D/(name+'.tga'));t.automated=True;t.prompt=False;t.replace_identical=False;t.exporter=unreal.TextureExporterTGA();assert unreal.Exporter.run_asset_export_task(t)
