"""Only move two newly added encounters after larger silhouette clearance exposed tight starts."""
import unreal,json,math,hashlib,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/CreatureExpansionV3'));from MapState import snapshot
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);w=E.get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2'and not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();O=R/'Saved/CreatureExpansionV3';assert not(O/'RefinedHabitatPositions.json').exists();before=snapshot(A);rows=[];changed=set()
plans={'Nebulak':[(-1400,-800),(-1500,-700),(-1600,-500),(-1500,-350),(-1100,-850),(-1300,-1000),(-1600,-1000),(-1700,-300)],'Gengar':[(-1500,500),(-1600,650),(-1200,500),(-1000,850),(1450,1400),(1600,1200),(1600,800),(1450,550)]}
for name,points in plans.items():
 a=next(x for x in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor)if str(x.encounter_id)=='Dev_'+name+'_Wild_V3');assert 'CreatureExpansionV3'in [str(t)for t in a.tags];changed.add(a.get_path_name());original=a.get_actor_location();c=a.get_component_by_class(unreal.CapsuleComponent);hh=c.get_scaled_capsule_half_height();m=a.overworld_movement;attempts=[];chosen=None
 for x,y in points:
  a.set_actor_location(unreal.Vector(x,y,hh),False,False);m.configure(a.visual_species,hh,c.get_scaled_capsule_radius(),hh,None,a.seed);g=m.project_walkable(unreal.Vector(x,y,0));routes=0
  if g is not None and abs(g.z)<20:
   for i in range(8):
    end=m.project_walkable(g+unreal.Vector(math.cos(i*math.tau/8)*200,math.sin(i*math.tau/8)*200,0))
    if end is not None and m.can_traverse(g,end):routes+=1
  attempts.append(dict(x=x,y=y,ground=g.to_tuple()if g else None,routes=routes))
  if routes>=3:chosen=g;break
 if chosen is None:a.set_actor_location(original,False,False);raise RuntimeError('No sufficiently connected '+name+' location; no map saved')
 a.set_actor_location(chosen+unreal.Vector(0,0,hh),False,False);a.tags=[unreal.Name('CreatureExpansionV3'),unreal.Name('Forest')];rows.append(dict(species=name,before=original.to_tuple(),after=a.get_actor_location().to_tuple(),attempts=attempts))
after=snapshot(A);diff={p:dict(before=before[p],after=after.get(p))for p in before if p not in changed and before[p]!=after.get(p)};(O/'RefinedHabitatOtherActorDiff.json').write_text(json.dumps(diff,indent=2));assert not diff;assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();(O/'RefinedHabitatPositions.json').write_text(json.dumps(dict(rows=rows,all_other_actors_unchanged=True),indent=2))
