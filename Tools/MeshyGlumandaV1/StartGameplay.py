import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();w=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0))
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Viewport 2560 1440');unreal.SystemLibrary.execute_console_command(w,'r.ScreenPercentage 100')
source=(R/'Tools/VisualV2QualityV2/FootTest.py').read_text().replace('Saved/VisualV2QualityV2','Saved/MeshyGlumandaV1')
source=source.replace('next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor))',"next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor) if a.source_actor and a.source_actor.get_actor_label()=='Slice_Wanderer_Hinweis')")
source=source.replace("elif kind=='verifyinside':assert","elif kind=='verifyinside':assert all(not c.cast_shadow and c.get_editor_property('lighting_channels').channel1 and not c.get_editor_property('lighting_channels').channel0 for c in p.get_components_by_class(unreal.PrimitiveComponent));assert")
source=source.replace("elif kind=='verifyoutside':assert","elif kind=='verifyoutside':assert p.get_component_by_class(unreal.SkeletalMeshComponent).cast_shadow and p.get_component_by_class(unreal.SkeletalMeshComponent).get_editor_property('lighting_channels').channel0;assert")
# A real party switch validates the captured creature as the player's own battle presentation.
source=source.replace("elif name=='WildCapture' and view.capture_enabled","elif name=='TrainerBattle' and not local.get('zunderlauf_switched') and any(m.can_switch and str(m.name)=='Zunderlauf' for m in view.player_team):assert pr.try_select_switch(next(j for j,m in enumerate(view.player_team) if m.can_switch and str(m.name)=='Zunderlauf'));local['zunderlauf_switched']=True\n    elif name=='WildCapture' and view.capture_enabled")
source=source.replace("if request.get('battle_review_only') and enc.is_encounter_active()","if False and enc.is_encounter_active()")
source=source.replace("duration=.12 if kind=='face'","duration=.28 if kind=='face'")
source=source.replace("local['sent']=True;assert p.try_interact()","local['sent']=True;target=p.find_interactable_in_range();out.setdefault('interaction_attempts',[]).append({'step':name,'direction':p.get_interaction_world_direction().to_tuple(),'target':target.get_name() if target else None});assert p.try_interact()")
# Approach the current paused encounter from interaction range; never walk through its capsule.
source=source.replace('dx=arg[0]-q.x;dy=arg[1]-q.y;distance=math.hypot(dx,dy)',"if name=='WildApproach':\n    target=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor)).get_actor_location();arg=(target.x+105,target.y)\n   dx=arg[0]-q.x;dy=arg[1]-q.y;distance=math.hypot(dx,dy)")
exec(compile(source,'existing_complete_gameplay_route','exec'),globals())
import runpy
runpy.run_path(str(R/'Tools/MeshyGlumandaV1/ObserveGameplay.py'),run_name='__main__')
