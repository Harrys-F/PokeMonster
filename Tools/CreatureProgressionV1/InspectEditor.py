"""Read-only inventory of progression data and the live editor state."""
import unreal,json
from pathlib import Path
r=Path(unreal.Paths.project_dir()).resolve();o=r/'Saved/CreatureProgressionV1'
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world(),'Stop PIE before asset work'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
rows=[]
for name in ['Zunderlauf','Schiggy','Bisasam','Pikachu','Myrapla','Enton','Machomei','Nebulak','Gengar','Glurak']:
 s=unreal.load_asset('/Game/Data/Creatures/DA_'+name);assert s
 rows.append(dict(name=name,id=str(s.get_internal_id()),dex=s.get_pokedex_number(),growth=str(s.get_growth_rate()),yield_xp=s.get_base_experience_yield(),stats=str(s.get_base_stats()),evolutions=[str(e) for e in s.get_evolutions()],moves=[dict(level=e.level,path=e.move.get_path_name() if e.move else None,name=str(e.move.display_name)if e.move else str(e.unavailable_move_name),power=e.move.base_power if e.move else None,pp=e.move.max_pp if e.move else None,effect=str(e.move.effect.effect_id)if e.move else str(e.unavailable_reason)) for e in s.level_up_moves]))
assert not (o/'SpeciesBefore.json').exists(),'Initial inventory is immutable; use ValidateData for the current state'
(o/'SpeciesBefore.json').write_text(json.dumps(rows,indent=2));unreal.log('PROGRESSION_EDITOR_INSPECTED')
