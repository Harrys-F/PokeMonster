"""Read-only current sprite, NPC presentation, interaction and healing-room inventory."""
import unreal,json,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();W=E.get_editor_world();out=dict(sprites=[],billboards=[],npcs=[],profiles=[],buildings=[])
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 for c in a.get_components_by_class(unreal.PaperSpriteComponent):out['sprites'].append(dict(label=a.get_actor_label(),actor=a.get_name(),class_path=a.get_class().get_path_name(),component=c.get_name(),sprite=c.get_sprite().get_path_name()if c.get_sprite()else None,visible=c.is_visible(),hidden=c.hidden_in_game or a.hidden,location=c.get_world_location().to_tuple()))
 for c in a.get_components_by_class(unreal.BillboardComponent):out['billboards'].append(dict(label=a.get_actor_label(),visible=c.is_visible(),hidden=c.hidden_in_game or a.hidden,editor_only=c.is_editor_only))
 if isinstance(a,(unreal.PokeMonsterNPC,unreal.PokeMonsterTrainerNPC,unreal.PokeMonsterRestPoint)):
  row=dict(label=a.get_actor_label(),location=a.get_actor_location().to_tuple(),rotation=a.get_actor_rotation().to_tuple())
  for n in ['dialogue','display_name','profile','service']:
   try:v=a.get_editor_property(n);row[n]=v.get_path_name()if isinstance(v,unreal.Object)else str(v)
   except Exception:pass
  out['npcs'].append(row)
 if isinstance(a,unreal.PokeMonsterBuildingCutaway):out['buildings'].append(dict(label=a.get_actor_label(),location=a.get_actor_location().to_tuple(),occluders=[x.get_actor_label()for x in a.occluding_actors if x],outer=a.door_threshold.get_world_location().to_tuple(),inner=a.relocated_door_threshold.get_world_location().to_tuple(),extent=a.relocated_interior_area.get_scaled_box_extent().to_tuple(),camera=[a.interior_camera_distance,a.interior_camera_pitch,a.interior_camera_yaw_offset],target=a.relocated_camera_target.to_tuple()))
for p in unreal.EditorAssetLibrary.list_assets('/Game/Characters/NPCs/Library/Profiles',True,False):
 a=unreal.load_asset(p)
 if isinstance(a,unreal.PokeMonsterNPCPresentationData):out['profiles'].append(dict(path=p,id=str(a.technical_id),height=a.reference_height_cm,mesh=a.mesh.get_path_name(),idle=a.idle.get_path_name()if a.idle else None,validation=list(a.get_validation_errors())))
(D/'InspectionBefore.json').write_text(json.dumps(out,indent=2));print(out['npcs']);print(out['buildings'])
