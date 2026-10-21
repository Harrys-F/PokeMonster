"""Read-only map bounds, source profiles and existing lighting."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/CreaturePolishV4';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
sys.path.insert(0,str(R/'Tools/CreatureExpansionV3'));from MapState import snapshot
A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);actors=A.get_all_level_actors();(O/'MapBefore.json').write_text(json.dumps(snapshot(A),indent=2));rows=[]
for a in actors:
 c,b=a.get_actor_bounds(False)
 if b.x>1500 or b.y>1500 or isinstance(a,unreal.SkyLight):rows.append(dict(label=a.get_actor_label(),class_name=a.get_class().get_name(),center=c.to_tuple(),extent=b.to_tuple(),components=[dict(name=x.get_name(),mesh=x.static_mesh.get_path_name() if x.static_mesh else None,materials=[m.get_path_name()if m else None for m in x.get_materials()])for x in a.get_components_by_class(unreal.StaticMeshComponent)]))
profiles={}
for name in ['Zunderlauf','Schiggy','Bisasam','Pikachu','Myrapla','Enton','Machomei','Nebulak','Gengar','Glurak']:
 s=unreal.load_asset('/Game/Data/Creatures/DA_'+name);p=s.visuals.presentation
 profiles[name]=dict(profile=p.get_path_name(),mesh=p.mesh.get_path_name(),walk=p.walk_speed,run=p.run_speed,ground=p.ground_offset_cm,clips={str(k):v.get_path_name()for k,v in p.clips.items()},materials=[x.material_interface.get_path_name()for x in p.mesh.materials])
(O/'Inventory.json').write_text(json.dumps(dict(bounds=rows,profiles=profiles),indent=2));unreal.log('CREATURE_POLISH_INVENTORY_DONE')
