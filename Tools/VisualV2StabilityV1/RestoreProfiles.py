import unreal
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor):
 path=unreal._stability_profiles.get(a.get_name());a.set_editor_property('profile',unreal.load_asset(path)if path else None)
