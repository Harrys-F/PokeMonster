"""Read-only exact movement/presentation values and complete relocated healing-room inventory."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2InteriorPokemonTeleportV6';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2'and not E.get_game_world();out=dict(species={},room=[],lights=[])
for name in ['Pikachu','Karpador']:
 s=unreal.load_asset('/Game/Data/Creatures/DA_'+name);p=s.get_visuals().presentation;out['species'][name]=dict(overworld=s.get_editor_property('overworld').export_text(),presentation=p.get_path_name(),mesh=p.mesh.get_path_name(),clips={str(k):dict(path=v.get_path_name(),seconds=v.get_play_length())for k,v in p.clips.items()},walk=p.walk_speed,run=p.run_speed,swim_reference=p.swim_reference_speed,swim_clip=p.swim_clip.get_path_name()if p.swim_clip else None,swim_idle=p.swim_idle_clip.get_path_name()if p.swim_idle_clip else None,swim_mesh=p.swim_mesh.get_path_name()if p.swim_mesh else None,height=p.reference_size_cm)
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 if 16000<a.get_actor_location().x<17700:
  row=dict(label=a.get_actor_label(),class_path=a.get_class().get_path_name(),position=a.get_actor_location().to_tuple(),hidden=a.hidden,components=[])
  for c in a.get_components_by_class(unreal.StaticMeshComponent):row['components'].append(dict(name=c.get_name(),mesh=c.static_mesh.get_path_name()if c.static_mesh else None,position=c.get_world_location().to_tuple(),scale=c.get_world_scale().to_tuple(),visible=c.is_visible(),hidden=c.hidden_in_game,collision=str(c.get_collision_enabled()),materials=[c.get_material(i).get_path_name()if c.get_material(i)else None for i in range(c.get_num_materials())]))
  out['room'].append(row)
  for c in a.get_components_by_class(unreal.LightComponent):out['lights'].append(dict(actor=a.get_actor_label(),component=c.get_class().get_name(),intensity=c.intensity,color=str(c.light_color),shadow=c.cast_shadows))
(D/'InspectionBefore.json').write_text(json.dumps(out,indent=2));print(out['species'])
