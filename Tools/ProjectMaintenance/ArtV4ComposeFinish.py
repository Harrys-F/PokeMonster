"""Measured game-camera corrections: unobscured hearth, cloth above stone, compatible skeletal forward axis."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ArtPassV4';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert not E.get_game_world() and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 label=a.get_actor_label();old=a.get_actor_location().to_tuple()
 if label.startswith('ArtV4_Hearth'):a.set_actor_location(unreal.Vector(17342,150,0),False,True)
 if label.startswith('ArtV4_RemedyCabinet'):a.set_actor_location(unreal.Vector(17342,660,0),False,True)
 if label=='V2_House_HH_Art_MainRunner':p=a.get_actor_location();p.z=1.9;a.set_actor_location(p,False,True)
 if label=='V2_House_SilverLady_HealerVisual':a.set_actor_rotation(unreal.Rotator(yaw=180),False);a.set_editor_property('forward_yaw_offset',0)
 if a.get_actor_location().to_tuple()!=old or label=='V2_House_SilverLady_HealerVisual':rows.append({'actor':a.get_name(),'label':label,'position':a.get_actor_location().to_tuple(),'rotation':a.get_actor_rotation().to_tuple()})
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');(R/'Art/HealingHouse/ArtV4_FinalLayout.json').write_text(json.dumps(rows,indent=2))
