import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Art/Characters/NPCs/Ranger/Review/V2';m=unreal.load_asset('/Game/Characters/NPCs/RangerV2/Meshes/SK_Ranger_NPC_V2');T=unreal.AssetToolsHelpers.get_asset_tools();out={}
# Only new task-owned LOD configuration; do not touch V1 or any existing shared settings asset.
f=unreal.DataAssetFactory();f.set_editor_property('data_asset_class',unreal.SkeletalMeshLODSettings);s=T.create_asset('DA_RangerV2_LODSettings','/Game/Characters/NPCs/RangerV2',unreal.SkeletalMeshLODSettings,f);groups=[]
for v in [1.,.12,.055]:
 g=unreal.SkeletalMeshLODGroupSettings();g.set_editor_property('screen_size',unreal.PerPlatformFloat(default=v));g.set_editor_property('lod_hysteresis',.015);groups.append(g)
s.set_editor_property('lod_groups',groups);m.set_editor_property('lod_settings',s);unreal.EditorAssetLibrary.save_loaded_asset(s,False);unreal.EditorAssetLibrary.save_loaded_asset(m,False);out={'settings':s.get_path_name(),'lod_settings':str(m.lod_settings),'groups':str(s.get_editor_property('lod_groups'))};(O/'LODSettings.json').write_text(json.dumps(out,indent=2))
