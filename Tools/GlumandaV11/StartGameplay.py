"""Reuse the proven complete Enhanced Input route, with task-local evidence and classic observer."""
from pathlib import Path
import unreal,json
R=Path(unreal.Paths.project_dir()).resolve()
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));request=json.loads((R/'Saved/GlumandaV11/AcceptanceRequest.json').read_text());O=R/'Saved/GlumandaV11/Acceptance'/request['label'];(O/'EditorSettingsBefore.json').write_text(json.dumps({'throttle':settings.get_editor_property('bThrottleCPUWhenNotForeground')}))
source=(R/'Tools/MeshyGlumandaV1/StartGameplay.py').read_text().replace('Saved/MeshyGlumandaV1','Saved/GlumandaV11').replace('Tools/MeshyGlumandaV1/ObserveGameplay.py','Tools/GlumandaV11/ObserveGameplay.py')
exec(compile(source,'existing_complete_gameplay_route_v11','exec'),globals())
