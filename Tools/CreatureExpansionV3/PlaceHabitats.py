"""Add one small existing-system habitat per reviewed species. No old actor/property edits."""
import unreal,json,hashlib,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/CreatureExpansionV3';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);w=E.get_editor_world();assert not E.get_game_world()and w.get_name()=='Dev_TestMap_VisualV2';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not(O/'HabitatPlacement.json').exists();specs=json.loads((R/'Tools/CreatureExpansionV3/Species.json').read_text())
import sys
sys.path.insert(0,str(R/'Tools/CreatureExpansionV3'));from MapState import snapshot as capture_state
def snapshot():return capture_state(A)
plans={
 'Pikachu':('Forest',[(-1450,100),(-1350,250),(-1600,200),(-1700,0)],(400,300)),
 'Myrapla':('Meadow',[(-400,1050),(-650,1100),(-200,1250),(-800,900)],(400,300)),
 'Enton':('River',[(1120,-900),(1150,-1100),(1000,-1150),(350,-1000)],(260,250)),
 'Machomei':('Rocky',[(1350,200),(1450,0),(1150,350),(1500,500)],(350,300)),
 'Nebulak':('Ruins',[(-1200,-600),(-1400,-550),(-1250,-800),(-1450,-900)],(300,300)),
 'Gengar':('Ruins',[(1100,1000),(1300,1150),(850,1250),(1500,900)],(350,300)),
 'Glurak':('Meadow',[(-1450,900),(-1500,1200),(-1250,800),(-1700,900),(-600,1350),(0,1350)],(450,350))}
before=snapshot();rows=[];mapfile=R/'Content/Maps/Dev_TestMap_VisualV2.umap';beforehash=hashlib.sha256(mapfile.read_bytes()).hexdigest()
for i,(name,spec)in enumerate(specs.items()):
 # Every source passed seven real FBX roundtrips and a separate native PIE review.
 review=json.loads((O/(name+'UnrealQA')/'Result.json').read_text());assert review['passed'],name
 ident='Dev_'+name+'_Wild_V3';assert all(str(x.encounter_id)!=ident for x in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor));species=unreal.load_asset('/Game/Data/Creatures/DA_'+name);profile=unreal.load_asset('/Game/Data/Encounters/DA_'+name+'_Wild');assert species and profile and not species.get_visuals().presentation.get_validation_errors();radius=float(spec['radius']);hh=max(radius,spec['height']/2);biome,points,extent=plans[name];a=A.spawn_actor_from_class(unreal.PokeMonsterVisibleWildCreatureActor,unreal.Vector(points[0][0],points[0][1],hh));a.set_actor_label('Slice_Wild_'+name+'_V3');capsule=a.get_component_by_class(unreal.CapsuleComponent);capsule.set_capsule_size(radius,hh,False);sprite=a.get_component_by_class(unreal.PaperSpriteComponent);sprite.set_relative_location(unreal.Vector(0,0,15-hh),False,False)
 for key,value in dict(profile=profile,visual_species=species,ambient_motion=True,encounter_id=ident,seed=93100+i,group_size=1).items():a.set_editor_property(key,value)
 a.tags=[unreal.Name('CreatureExpansionV3'),unreal.Name(biome)];movement=a.overworld_movement;movement.set_editor_property('habitat_half_extent',unreal.Vector2D(*extent));movement.set_editor_property('habitat_radius_override',float(max(extent)));chosen=None;attempts=[]
 for x,y in points:
  a.set_actor_location(unreal.Vector(x,y,hh),False,False);movement.configure(species,hh,radius,hh,None,a.seed);ground=movement.project_walkable(unreal.Vector(x,y,0));attempts.append({'xy':[x,y],'valid':ground is not None})
  if ground is not None:chosen=ground;break
 if chosen is None:raise RuntimeError('No safe '+name+' placement; do not save map; own candidate actor requires inspection')
 a.set_actor_location(chosen+unreal.Vector(0,0,hh),False,False);rows.append(dict(species=name,id=ident,actor=a.get_path_name(),location=a.get_actor_location().to_tuple(),capsule_radius_cm=radius,half_height_cm=hh,navigation_radius_cm=spec.get('navigation_radius',radius),biome=biome,habitat_half_extent=list(extent),attempts=attempts))
after=snapshot();diff={key:{'before':before[key],'after':after.get(key)}for key in before if before[key]!=after.get(key)};(O/'HabitatOldActorDiff.json').write_text(json.dumps(diff,indent=2));assert not diff,'An existing actor changed';assert len(after)==len(before)+7;assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();(O/'HabitatPlacement.json').write_text(json.dumps(dict(rows=rows,existing_actors=len(before),existing_actor_values_unchanged=True,before_sha256=beforehash,after_sha256=hashlib.sha256(mapfile.read_bytes()).hexdigest()),indent=2));unreal.log('CREATURE_EXPANSION_HABITATS_PLACED')
