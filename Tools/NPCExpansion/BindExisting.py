"""Adopt reviewed presentation only; source NPCs, healing, light and scenery remain unchanged."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/NPCExpansion';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();W=E.get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2';A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors();rows=[]
for label,id in [('NPCVisual_Wanderer_Ranger_V1','Ranger'),('V2_House_SilverLady_HealerVisual','SilverLady')]:
 V=next(x for x in A if x.get_actor_label()==label);S=V.source_actor;before={'source':S.get_path_name(),'source_transform':str(S.get_actor_transform()),'visual_transform':str(V.get_actor_transform()),'shadowless':V.get_editor_property('bShadowlessInteriorPresentation')}
 assert V.apply_presentation(unreal.load_asset('/Game/Characters/NPCs/Library/Profiles/DA_NPC_'+id));assert before['source_transform']==str(S.get_actor_transform());assert before['visual_transform']==str(V.get_actor_transform());assert before['shadowless']==V.get_editor_property('bShadowlessInteriorPresentation')
 rows.append({'label':label,'profile':id,'preserved':before,'mesh':V.visual.get_skeletal_mesh_asset().get_path_name()})
assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2');(O/'ExistingNPCBindings.json').write_text(json.dumps(rows,indent=2))
