import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2HealingArtV4';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
rows=[];mats={};ground={}
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 c=a.get_component_by_class(unreal.StaticMeshComponent)
 if not c:continue
 label=a.get_actor_label()
 if label.startswith('V2_House'):
  row={'name':a.get_name(),'label':label,'location':a.get_actor_location().to_tuple(),'rotation':a.get_actor_rotation().to_tuple(),'scale':a.get_actor_scale3d().to_tuple(),'mesh':c.static_mesh.get_path_name() if c.static_mesh else None,'materials':[c.get_material(i).get_path_name() if c.get_material(i) else None for i in range(c.get_num_materials())],'collision':str(c.get_collision_enabled()),'shadow':c.cast_shadow,'bounds':[v.to_tuple() for v in a.get_actor_bounds(False)]};rows.append(row)
  for i in range(c.get_num_materials()):
   m=c.get_material(i)
   if m and m.get_path_name() not in mats and isinstance(m,unreal.Material):
    expr=[]
    for n in unreal.MaterialEditingLibrary.get_material_expressions(m):
     d={'class':n.get_class().get_name(),'name':n.get_name()}
     for p in ['texture','parameter_name','constant','r','const_b','code','output_type','u_tiling','v_tiling']:
      try:
       v=n.get_editor_property(p);d[p]=v.get_path_name() if isinstance(v,unreal.Object) else str(v)
      except Exception:pass
     expr.append(d)
    mats[m.get_path_name()]={'two_sided':m.get_editor_property('two_sided'),'blend_mode':str(m.get_editor_property('blend_mode')),'expressions':expr}
for f in ['HealingMeadow','HealingPath','HealingForecourt','LegacyApproach']:
 m=unreal.load_asset('/Game/Environment/VisualV2HealingArtV3/Materials/M_HA3_'+f);ground[f]=[{'name':n.get_name(),'code':n.get_editor_property('code'),'type':str(n.get_editor_property('output_type'))} for n in unreal.MaterialEditingLibrary.get_material_expressions(m) if isinstance(n,unreal.MaterialExpressionCustom)]
(S/'Inventory.json').write_text(json.dumps({'house':rows,'materials':mats,'ground':ground},indent=2));unreal.log('HA4_INVENTORY_COMPLETE')
