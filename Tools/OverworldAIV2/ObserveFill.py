"""Read-only visibility observations during the existing real Enhanced Input footrun."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/OverworldAIV2';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();p=unreal.GameplayStatics.get_player_pawn(w,0);fill=p.get_component_by_class(unreal.PokeMonsterCharacterFillComponent);m=p.get_component_by_class(unreal.PokeMonsterMeshyVisualComponent);visibility=p.get_component_by_class(unreal.PokeMonsterCameraVisibilityComponent);rows=[];s={'t':0}
unreal.SystemLibrary.execute_console_command(w,'pm.PlayerFill.Mode 1')
def tick(dt):
 if not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world():unreal.unregister_slate_post_tick_callback(unreal._ai_fill_observer);return
 s['t']+=dt
 if s['t']<.25:return
 s['t']=0;channels=m.get_editor_property('lighting_channels');rows.append({'position':p.get_actor_location().to_tuple(),'fill_lumens':fill.fill_lumens,'estimated_shade':fill.estimated_shade,'interior':channels.channel1,'sight_scale':visibility.reveal_radius_scale});(O/'FillFootrun.json').write_text(json.dumps(rows,indent=2))
unreal._ai_fill_observer=unreal.register_slate_post_tick_callback(tick)
