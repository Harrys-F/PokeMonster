"""Correct the confirmed new pier obstruction, moving only our three new entry actors."""
import unreal,sys,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert not E.get_game_world()and w.get_name()=='Dev_BiomeTestMap_V1';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();actors={x.get_actor_label():x for x in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};rows=[]
for label,u,z in [('WeatheredEntryArch',3000,L.height(3000,-3060)),('EntryPier-1',2830,135),('EntryPier1',3170,135)]:
 a=actors['Biome_RuinV11_'+label];before=a.get_actor_location();a.set_actor_location(unreal.Vector(*L.world(u,-3060,z)),False,True);rows.append({'label':a.get_actor_label(),'before':before.to_tuple(),'after':a.get_actor_location().to_tuple()})
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_BiomeTestMap_V1');(R/'Saved/BiomeTestV11/RuinAccessCorrection.json').write_text(json.dumps({'reason':'Actual first footwalk hit new left pier on existing junction at (2800,-2800); move new portal 250cm deeper, retaining real collisions and existing approach','actors':rows},indent=2))
