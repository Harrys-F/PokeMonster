"""Move only Schiggy's start/travel points clear of the new actual jetty collision."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert not E.get_game_world()and w.get_name()=='Dev_BiomeTestMap_V1';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
live=json.loads((R/'Saved/BiomeTestV11/WaterLiveState.json').read_text());assert [r['habitat']for r in live if r['live']!=r['configured']]==['SchiggyUfer']
h=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterBiomeHabitat)if a.habitat_name=='SchiggyUfer');centre=L.local(h.get_actor_location().x,h.get_actor_location().y);arr=list(h.specimens);arr[0].set_editor_property('local_position',unreal.Vector(2050-centre[0],-(2450-centre[1]),L.height(2050,2450)));h.set_editor_property('specimens',arr);h.set_editor_property('travel_points',[unreal.Vector(u-centre[0],-(v-centre[1]),0)for u,v in [(1950,2450),(2350,2450),(2800,2550),(3000,2900)]])
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_BiomeTestMap_V1');(R/'Saved/BiomeTestV11/JettySpawnCorrection.json').write_text(json.dumps({'reason':'Real jetty collision correctly rejected old spawn under deck. Move specimen start and two waypoint entries clear; no collision disabled.','schiggy_start_uv':[2050,2450],'species_profile_unchanged':True},indent=2))
