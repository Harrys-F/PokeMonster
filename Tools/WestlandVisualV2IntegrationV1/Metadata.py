"""Read actual runtime CVars and imported texture dimensions from asset metadata, not placeholder GPU sizes."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualV2IntegrationV1';label=json.loads((D/'Request.json').read_text())['label'];reg=unreal.AssetRegistryHelpers.get_asset_registry();textures=[]
for root in ['Jayant_Chakradhari_Assets','Megaplant_Library','Pack_Bonus','RockEnv_Pack','SimpleRocks','StyleHex_Studio','Fab/VisualV2TrialLocal']:
 for d in reg.get_assets_by_path('/Game/'+root,recursive=True):
  if str(d.asset_class_path.asset_name)!='Texture2D':continue
  textures.append(dict(path=str(d.package_name),imported_dimensions=unreal.AssetRegistryHelpers.get_tag_value(d,'Dimensions')))
cv=['r.ScreenPercentage','r.AntiAliasingMethod','r.TemporalAA.Upsampling','r.Lumen.HardwareRayTracing','r.Lumen.FinalGatherMethod','r.Shadow.Virtual.Enable','r.Shadow.Virtual.SMRT.RayCountDirectional']+['sg.'+s+'Quality'for s in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']]
(D/(label+'_Metadata.json')).write_text(json.dumps(dict(cvars={k:unreal.SystemLibrary.get_console_variable_float_value(k)for k in cv},textures=textures,warning='Blueprint_GetSizeX during initial asynchronous texture compilation returned the engine default 32x32 placeholder; source dimensions must use Dimensions metadata.'),indent=2))
