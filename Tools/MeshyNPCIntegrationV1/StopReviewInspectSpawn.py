import unreal,json
from pathlib import Path
if hasattr(unreal,'_npc_review'):unreal.unregister_slate_post_tick_callback(unreal._npc_review);del unreal._npc_review
p=Path(unreal.Paths.project_dir()).resolve()/'Art/Characters/NPCs/IntegrationV1';(p/'SpawnAPI.json').write_text(json.dumps({n:getattr(unreal.GameplayStatics,n).__doc__ for n in ['begin_deferred_actor_spawn_from_class','finish_spawning_actor']},indent=2))
