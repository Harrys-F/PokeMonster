import unreal,json
from pathlib import Path
P=Path(unreal.Paths.project_dir(),'Art/Characters/NPCs/Ranger/Review/V2');out={};s=unreal.get_editor_subsystem(unreal.SkeletalMeshEditorSubsystem)
for n in ['V1','V2']:
 path='/Game/Characters/NPCs/Ranger/Meshes/SK_Ranger_NPC_V1' if n=='V1' else '/Game/Characters/NPCs/RangerV2/Meshes/SK_Ranger_NPC_V2';m=unreal.load_asset(path);row={'lods':[]}
 if n=='V2':row['reduction']=[str(g.get_editor_property('reduction_settings').to_dict()) for g in m.lod_settings.get_editor_property('lod_groups')]
 for i in range(s.get_lod_count(m)):
  d=unreal.DynamicMesh();r=unreal.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(m,d,unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD(lod_index=i));row['lods'].append({'lod':i,'result':str(r[1]),'mesh_info':unreal.GeometryScript_MeshQueries.get_mesh_info_string(d)})
 out[n]=row
(P/'ActualUELODs.json').write_text(json.dumps(out,indent=2))
