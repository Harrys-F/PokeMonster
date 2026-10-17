import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();m=unreal.load_asset('/Game/Environment/WestlandAssetLibrary/QualityV3/Meshes/Trees/SM_WLA_OakAncient_V3')
out={'mesh_found':bool(m)}
if m:out['mesh_api']={n:str(getattr(m,n).__doc__) for n in dir(m) if any(k in n for k in ['triang','description','num_','lod_','render'])}
s=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);out['subsystem_api']={n:str(getattr(s,n).__doc__) for n in dir(s) if any(k in n for k in ['triang','description','num_','lod_'])}
(R/'Saved/EnvironmentPerfV1/MeshAPI.json').write_text(json.dumps(out,indent=2))
