import unreal,json
from pathlib import Path
D=Path(unreal.Paths.project_dir())/'Saved/ProjectRefinement/VisualV2PokemonTestGroundHealhouseV7';rows=[]
for s in unreal.PokeMonsterCreatureSpeciesData.get_registered_playable_species():
 p=s.get_visuals().presentation;clips={str(k):v.get_path_name()if v else None for k,v in p.clips.items()};rows.append(dict(name=str(s.get_display_name()),internal=str(s.get_internal_id()),species=s.get_path_name(),presentation=p.get_path_name(),rig_family=str(p.rig_family),mesh=p.mesh.get_path_name(),skeleton=p.mesh.get_editor_property('skeleton').get_path_name(),reference_cm=p.reference_size_cm,mesh_dimensions_cm=(p.mesh.get_bounds().box_extent*2).to_tuple(),clips=clips,swim=p.swim_clip.get_path_name()if p.swim_clip else None,swim_bounds=(p.swim_mesh.get_bounds().box_extent*2).to_tuple()if p.swim_mesh else None,swim_submerged_depth=p.swim_submerged_depth_cm))
(D/'RegisteredSpecies.json').write_text(json.dumps(rows,indent=2));print('V7 REGISTERED',len(rows))
