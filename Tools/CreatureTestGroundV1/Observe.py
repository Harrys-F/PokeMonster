"""Read an already running ordinary PIE; never spawns specimens, ground, party or habitats."""
import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/TestGroundV1'
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_game_world();assert w and w.get_name().endswith('Dev_TestMap_VisualV2')
g=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureTestGround)if x.get_outer()==w)
p=unreal.GameplayStatics.get_player_pawn(w,0);gi=unreal.GameplayStatics.get_game_instance(w)
e=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi)
rows=[]
names=['Zunderlauf','Schiggy','Bisasam','Pikachu','Myrapla','Enton','Machomei','Nebulak','Gengar','Glurak']
for i,v in enumerate(g.specimens):
 profile=unreal.load_asset('/Game/Data/Creatures/DA_'+names[i]).get_visuals().presentation
 m=v.get_component_by_class(unreal.PokeMonsterCreatureRoamingComponent)
 rows.append(dict(actor=v.get_path_name(),mesh=profile.mesh.get_path_name(),position=v.get_actor_location().to_tuple(),height=profile.reference_size_cm,clips=[str(c)for c in profile.clips.keys()],distance_cm=m.distance_travelled,origin=m.habitat_origin.to_tuple(),radius=m.habitat_radius_override,tagged=v.actor_has_tag('PokemonDevelopmentSpecimen'),collision=str(v.mesh.get_collision_enabled())))
f=R/'Saved/SaveGames/PokeMonster_Dev.sav'
s=dict(world=w.get_path_name(),ordinary_pie=True,read_only_observation=True,specimens=rows,player=p.get_actor_location().to_tuple(),encounter_active=e.is_encounter_active(),party_ids=[c.instance_id.to_string()for c in e.get_player_party()],save_sha256=hashlib.sha256(f.read_bytes()).hexdigest()if f.exists()else None,dirty_maps=[x.get_path_name()for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],dirty_content=[x.get_path_name()for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
assert len(rows)==10 and all(x['tagged']for x in rows)
q=O/'ObserveRequest.json';label=json.loads(q.read_text())['label']if q.exists()else'OrdinaryPIEBeforeAnyReview';assert label.isalnum();pth=O/(label+'.json');assert not pth.exists();pth.write_text(json.dumps(s,indent=2));unreal.log('TESTGROUND_ORDINARY_PIE_OBSERVED_10')
