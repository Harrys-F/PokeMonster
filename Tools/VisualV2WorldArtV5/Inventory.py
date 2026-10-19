import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtV5';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();rows=[];graphs={}
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if not c.static_mesh:continue
  mats=[c.get_material(i) for i in range(c.get_num_materials())];row={'name':a.get_name(),'label':a.get_actor_label(),'location':a.get_actor_location().to_tuple(),'scale':a.get_actor_scale3d().to_tuple(),'rotation':a.get_actor_rotation().to_tuple(),'hidden':a.is_hidden_ed(),'visible':c.get_editor_property('visible'),'hidden_in_game':c.get_editor_property('hidden_in_game'),'mesh':c.static_mesh.get_path_name(),'materials':[m.get_path_name() if m else None for m in mats],'collision':str(c.get_collision_enabled()),'shadow':c.cast_shadow,'bounds':[p.to_tuple() for p in a.get_actor_bounds(False)]}
  if isinstance(c,unreal.InstancedStaticMeshComponent):row['instances']=[{'location':c.get_instance_transform(i,True).translation.to_tuple(),'scale':c.get_instance_transform(i,True).scale3d.to_tuple()} for i in range(c.get_instance_count())]
  if c.get_editor_property('visible') and not c.get_editor_property('hidden_in_game'):rows.append(row)
  for m in mats:
   if isinstance(m,unreal.Material) and m.get_path_name() not in graphs and (a.get_actor_label() in ['V2_Ground','V2_Path_Main','V2_Path_NorthLoop','V2_Path_VillageLoop','P2D_OrganicWater']):
    graphs[m.get_path_name()]=[{'class':n.get_class().get_name(),'name':n.get_name(),'code':n.get_editor_property('code') if isinstance(n,unreal.MaterialExpressionCustom) else ''} for n in unreal.MaterialEditingLibrary.get_material_expressions(m)]
(S/'Inventory.json').write_text(json.dumps({'visible_mesh_components':rows,'graphs':graphs},indent=2));unreal.log('WA5_INVENTORY_READONLY')
