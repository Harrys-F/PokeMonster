import unreal,json
from pathlib import Path
p=Path(unreal.Paths.project_dir()).resolve()/'Art/Characters/NPCs/IntegrationV1'
x={'actor_component_api':[n for n in dir(unreal.Actor) if 'component' in n.lower() or 'attach' in n.lower()],'skeletal_actor_api':[n for n in dir(unreal.SkeletalMeshActor) if 'component' in n.lower() or 'anim' in n.lower()],'play_settings':unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.LevelEditorPlaySettings')).get_class().get_path_name(),'play_settings_props':[n for n in dir(unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.LevelEditorPlaySettings'))) if any(k in n for k in ['width','height','resolution','viewport','size'])]}
(p/'PresentationAPI.json').write_text(json.dumps(x,indent=2))
