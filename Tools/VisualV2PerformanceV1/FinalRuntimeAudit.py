"""Read final live counts and validate saved bindings outside timed windows."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_game_world();assert W
wild=unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor);visual=unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterCreatureVisualActor);GI=unreal.GameplayStatics.get_game_instance(W);clock=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterWorldClock)if x.get_outer()==GI);light=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterDayNightSubsystem)if x.get_outer()==W)
rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.StaticMeshActor):
 if a.get_actor_label()in ['V2_Ground','Hill_Step_Low','Hill_Step_Mid','Hill_Lookout']:
  c=a.static_mesh_component;rows.append({'actor':a.get_actor_label(),'material':c.get_material(0).get_path_name()})
assert len(rows)==4 and all('M_PV1_BakedGroundSRGB.'in x['material']for x in rows)
(D/'FinalRuntimeAudit.json').write_text(json.dumps({'actor_count':len(unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)),'wild_actors':len(wild),'active_wild_activities':sum(a.overworld_movement.activities_enabled for a in wild),'wild_rhythms':sum(a.overworld_movement.rhythm_enabled for a in wild),'creature_visuals':len(visual),'visible_creature_visuals':sum(not a.get_editor_property('bHidden')for a in visual),'companions':len(unreal.GameplayStatics.get_all_actors_with_tag(W,'CreaturePartyCompanion')),'real_minutes_per_day':clock.get_real_minutes_per_day(),'cycle_enabled':light.is_cycle_enabled(),'current_lighting':light.get_lighting_sample().export_text(),'bindings':rows},indent=2))
