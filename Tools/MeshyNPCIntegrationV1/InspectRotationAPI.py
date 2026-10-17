import unreal,json
from pathlib import Path
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();v=next(x for x in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor));r=v.get_actor_rotation();o={'rotator_doc':unreal.Rotator.__doc__,'visual_rotation':str(r),'values':{'pitch':r.pitch,'yaw':r.yaw,'roll':r.roll},'constructor_keyword_test':str(unreal.Rotator(pitch=0,yaw=135,roll=0))};Path(unreal.Paths.project_dir(),'Art/Characters/NPCs/IntegrationV1/RotationAPI.json').write_text(json.dumps(o,indent=2))
