import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve()
O=R/'Art/Characters/NPCs/Ranger/Review/AnimationV3/Data'
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert w and 'NPCMotionV3' in w.get_name()
v=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor) if a.source_actor.get_class().get_name()=='PokeMonsterNPC')
c=v.visual
v.set_actor_rotation(unreal.Rotator(yaw=0),False)
c.set_forced_lod(1)
c.play_animation(v.walk_animation,False)
c.set_position(.225,False);c.set_play_rate(0)
def record(dt):
 unreal.unregister_slate_post_tick_callback(unreal._r3_axes);del unreal._r3_axes
 bones={}
 for n in ['pelvis','thigh_l','shin_l','foot_l','thigh_r','shin_r','foot_r']:
  t=c.get_socket_transform(n,unreal.RelativeTransformSpace.RTS_COMPONENT)
  bones[n]={'position_cm':t.translation.to_tuple(),'quaternion':t.rotation.to_tuple()}
 (O/'V3_Unreal_Axes.json').write_text(json.dumps({'mesh':c.get_skeletal_mesh_asset().get_path_name(),'actor_rotation':v.get_actor_rotation().to_tuple(),'component_transform':str(c.get_relative_transform()),'bones':bones},indent=2))
unreal._r3_axes=unreal.register_slate_post_tick_callback(record)
