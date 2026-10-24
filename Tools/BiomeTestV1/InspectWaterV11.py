"""Read-only live habitat diagnostics; no map or save write."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_game_world()or E.get_editor_world();rows=[]
for h in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterBiomeHabitat):
 rows.append({'habitat':h.habitat_name,'configured':len(h.specimens),'live':len(h.runtime_specimens),'spawn_world':[h.get_actor_transform().transform_location(s.local_position).to_tuple()for s in h.specimens],'positions':[a.get_actor_location().to_tuple()for a in h.runtime_specimens]})
(R/'Saved/BiomeTestV11/WaterLiveState.json').write_text(json.dumps(rows,indent=2))
