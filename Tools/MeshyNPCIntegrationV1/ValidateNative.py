import unreal,json
from pathlib import Path
P=Path(unreal.Paths.project_dir()).resolve()/'Art/Characters/NPCs/IntegrationV1';c=unreal.load_class(None,'/Script/PokeMonster.PokeMonsterNPCVisualActor');assert c
(P/'NativeClass.json').write_text(json.dumps({'class':c.get_path_name(),'dialogue_read_only_accessor':hasattr(unreal.PokeMonsterDialogueSubsystem,'get_active_source')},indent=2))
