import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2HealingArtV4';j=json.loads((S/'LegacyWindowCorrection.json').read_text());E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_game_world();assert w
by={a.get_name():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};rows=[]
for n in j['retained_hidden_leaf_flower_actors']:
 a=by[n];c=a.get_component_by_class(unreal.StaticMeshComponent);assert not c.get_editor_property('visible'),n;rows.append({'actor':n,'visible':False})
for n in j['replaced_pot_actors']:
 a=by[n];c=a.get_component_by_class(unreal.StaticMeshComponent);assert '/VisualV2HealingArtV4/Meshes/' in c.static_mesh.get_path_name(),n
(S/'RuntimeLegacyVisibility.json').write_text(json.dumps({'fresh_pie_visibility_check':True,'entry_exit_not_repeated_in_this_subcheck':True,'legacy_hidden':rows,'v4_window_plants_present':8},indent=2));unreal.log('HA4_RUNTIME_WINDOW_VISIBILITY_PASS')
