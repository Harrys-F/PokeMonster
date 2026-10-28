"""Activate only the reused pond component; preserve the old stream and all other visibility."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PokemonWaterTeamV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();W=E.get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
a=next(a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()if a.get_actor_label()=='P2D_Surface_Pond_Water');c=a.static_mesh_component
r={'actor_hidden':a.get_editor_property('hidden'),'component_hidden':c.get_editor_property('hidden_in_game'),'component_visible':c.get_editor_property('visible'),'material':c.get_material(0).get_path_name(),'mesh':c.static_mesh.get_path_name()}
(D/'PondSurfaceBefore.json').write_text(json.dumps(r,indent=2));assert r['component_hidden']or not r['component_visible'],'Unexpected cause; do not modify unrelated flags'
c.set_hidden_in_game(False);c.set_visibility(True);assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2');(D/'PondSurfaceActivated.json').write_text(json.dumps({'before':r,'after_hidden':False,'after_visible':True},indent=2))
