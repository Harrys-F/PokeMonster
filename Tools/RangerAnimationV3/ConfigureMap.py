"""Replace presentation actors only, inside the new V3 map."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Art/Characters/NPCs/Ranger/Review/AnimationV3/Data'
e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=e.get_editor_world();a=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
assert not e.get_game_world() and w.get_name()=='Dev_TestMap_NPCMotionV3'
assert not any(isinstance(x,unreal.PokeMonsterNPCMotionV3VisualActor) for x in a.get_all_level_actors())
old=next(x for x in a.get_all_level_actors() if isinstance(x,unreal.PokeMonsterNPCVisualActor) and x.source_actor and x.source_actor.get_class().get_name()=='PokeMonsterNPC')
src=old.source_actor;before={'source':src.get_path_name(),'position':src.get_actor_location().to_tuple(),'rotation':src.get_actor_rotation().to_tuple(),'dialogue':src.dialogue.get_path_name(),'display_name':str(src.display_name),'old_visual':old.get_path_name()}
transform=old.get_actor_transform();old.set_editor_property('bUseVisual',False);old.refresh_presentation()
sprite=src.get_component_by_class(unreal.PaperSpriteComponent);sprite.set_visibility(True)
v=a.spawn_actor_from_class(unreal.PokeMonsterNPCMotionV3VisualActor,transform.translation,transform.rotation.rotator())
v.set_actor_transform(transform,False,True);v.set_actor_label('NPCVisual_Wanderer_AnimationQuality_V3');v.source_actor=src
def configure(v):
 v.visual.set_skeletal_mesh_asset(unreal.load_asset('/Game/Characters/NPCs/RangerMotionV3/Meshes/SK_Ranger_AQV3'))
 for prop,clip in [('idle_animation','Idle'),('walk_animation','Walk'),('conversation_animation','Talk'),('turn_left_animation','TurnLeft'),('turn_right_animation','TurnRight')]:
  v.set_editor_property(prop,unreal.load_asset('/Game/Characters/NPCs/RangerMotionV3/Animations/A_Ranger_'+clip+'_AQV3'))
 v.set_editor_property('bEnableMotionPresentation',True);v.set_editor_property('bEnableAccessoryMotion',True);v.authored_walk_speed=150.;v.refresh_presentation()
configure(v)
v.attach_to_actor(src,'',unreal.AttachmentRule.KEEP_WORLD,unreal.AttachmentRule.KEEP_WORLD,unreal.AttachmentRule.KEEP_WORLD,False)
assert a.destroy_actor(old)
preview=a.spawn_actor_from_class(unreal.PokeMonsterNPCMotionV3PreviewSource,unreal.Vector(-100,-150,3));preview.set_actor_label('NPCMotionV3_PreviewSource_NoGameplay');preview.tags=['NPCMotionV3_PreviewOnly'];preview.set_folder_path('NPCMotionV3/ExplicitPreviewOnly')
pv=a.spawn_actor_from_class(unreal.PokeMonsterNPCMotionV3VisualActor,preview.get_actor_location());pv.source_actor=preview;pv.set_actor_label('NPCMotionV3_PreviewVisual_DisabledUntilTest');pv.tags=['NPCMotionV3_PreviewOnly'];pv.set_folder_path('NPCMotionV3/ExplicitPreviewOnly');configure(pv);pv.set_editor_property('bUseVisual',False);pv.refresh_presentation();pv.attach_to_actor(preview,'',unreal.AttachmentRule.KEEP_WORLD,unreal.AttachmentRule.KEEP_WORLD,unreal.AttachmentRule.KEEP_WORLD,False)
unreal.SystemLibrary.execute_console_command(w,'pm.NPCMotion3.AuditLODs .22')
unreal.EditorAssetLibrary.save_loaded_asset(v.visual.get_skeletal_mesh_asset(),False)
assert before['position']==src.get_actor_location().to_tuple() and before['rotation']==src.get_actor_rotation().to_tuple() and before['dialogue']==src.dialogue.get_path_name()
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_NPCMotionV3')
unreal.SystemLibrary.execute_console_command(w,'MAP CHECK')
(D/'MapConfigured.json').write_text(json.dumps({'before':before,'source_preserved':True,'visual':v.get_path_name(),'mesh':v.visual.get_skeletal_mesh_asset().get_path_name(),'preview_source':preview.get_path_name(),'preview_visual':pv.get_path_name(),'preview_enabled_default':False,'note':'Two inherited V2 preview actors remain disabled and unchanged.'},indent=2))
