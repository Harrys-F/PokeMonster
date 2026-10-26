import unreal,json
from pathlib import Path
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor):
 m=a.overworld_movement
 if m.activities_enabled:rows.append({'actor':a.get_name(),'species':str(a.visual_species.get_internal_id()),'position':a.get_actor_location().to_tuple(),'rhythm_enabled':m.rhythm_enabled,'rhythm':m.rhythm.export_text(),'factor':m.rhythm_activity,'offset':m.rhythm_offset_minutes,'state':str(m.behavior_state)})
(Path(unreal.Paths.project_dir())/'Saved/ProjectRefinement/DayNightV11AI22/InspectRhythm.json').write_text(json.dumps(rows,indent=2))
del W,rows,a,m
