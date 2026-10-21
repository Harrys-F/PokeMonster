"""Read-only inventory of active lighting, player materials and tree collision."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_game_world()or E.get_editor_world();rows=[];channel2=[];trees=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 for c in a.get_components_by_class(unreal.LightComponentBase):
  d={'actor':a.get_name(),'label':a.get_actor_label(),'class':c.get_class().get_name(),'location':a.get_actor_location().to_tuple(),'rotation':a.get_actor_rotation().to_tuple()}
  for k in ['intensity','cast_shadows','mobility','light_color','lighting_channels','indirect_lighting_intensity','real_time_capture']:
   try:d[k]=str(c.get_editor_property(k))
   except Exception:pass
  rows.append(d)
 for c in a.get_components_by_class(unreal.PrimitiveComponent):
  if c.get_editor_property('lighting_channels').channel2:channel2.append({'actor':a.get_name(),'component':c.get_name()})
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if c.static_mesh and ('Oak'in c.static_mesh.get_name()or'Birch'in c.static_mesh.get_name()):
   if len(trees)<10:trees.append({'actor':a.get_name(),'mesh':c.static_mesh.get_path_name(),'collision':str(c.get_collision_enabled()),'profile':str(c.get_collision_profile_name()),'cast_shadow':c.cast_shadow,'location':c.get_world_location().to_tuple()})
p=unreal.GameplayStatics.get_player_pawn(w,0);player=None
if p:
 m=p.get_component_by_class(unreal.PokeMonsterMeshyVisualComponent);player={'position':p.get_actor_location().to_tuple(),'mesh':m.get_skeletal_mesh_asset().get_path_name(),'materials':[x.get_path_name()for x in m.get_materials()],'channels':str(m.get_editor_property('lighting_channels')),'sight_scale':p.get_component_by_class(unreal.PokeMonsterCameraVisibilityComponent).reveal_radius_scale}
r={'lights':rows,'channel2_receivers':channel2,'trees':trees,'player':player,'vsm':unreal.SystemLibrary.get_console_variable_int_value('r.Shadow.Virtual.Enable'),'aa':unreal.SystemLibrary.get_console_variable_int_value('r.AntiAliasingMethod')};(R/'Saved/OverworldAIV2/LightingInventory.json').write_text(json.dumps(r,indent=2))
