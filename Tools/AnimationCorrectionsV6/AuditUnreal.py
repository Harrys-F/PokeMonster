import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();assert not (R/'Saved/AnimationCorrectionsV6/UnrealBaseline.json').exists(),'Preserve the original audit; use a new review label';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();rows={}
for n in ['Zunderlauf','Schiggy','Bisasam','Pikachu','Myrapla','Enton','Machomei','Nebulak','Gengar','Glurak']:
 s=unreal.load_asset('/Game/Data/Creatures/DA_'+n);p=s.get_visuals().presentation;o=s.overworld
 rows[n]=dict(id=str(s.get_internal_id()),profile=p.get_path_name(),mesh=p.mesh.get_path_name(),walk=p.walk_speed,run=p.run_speed,walk_override=o.walk_speed_override,run_override=o.run_speed_override,reference_size=p.reference_size_cm,materials=[x.material_interface.get_path_name()for x in p.mesh.materials],clips={str(k):v.get_path_name()for k,v in p.clips.items()})
(R/'Saved/AnimationCorrectionsV6/UnrealBaseline.json').write_text(json.dumps(rows,indent=2));unreal.log('V6_BASELINE_AUDIT_OK')
