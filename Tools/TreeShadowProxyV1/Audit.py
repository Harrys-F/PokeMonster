import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/TreeShadowProxyV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not e.get_game_world()
w=e.get_editor_world()
def prop(o,n):
 try:return str(o.get_editor_property(n))
 except Exception:return None
out={'map':w.get_path_name(),'dirty_maps':[str(x) for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[str(x) for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()],'cvars':{},'lights':[],'trees':[],'materials':{},'post':[]}
for n in ['r.Shadow.Virtual.Enable','r.Lumen.FinalGatherMethod','r.Lumen.HardwareRayTracing','r.Shadow.Virtual.SMRT.RayCountDirectional','r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor','r.DynamicGlobalIlluminationMethod','r.ReflectionMethod','r.ScreenPercentage','r.VSync','t.MaxFPS']:
 out['cvars'][n]=unreal.SystemLibrary.get_console_variable_float_value(n)
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 for c in a.get_components_by_class(unreal.LightComponent):
  out['lights'].append({'actor':a.get_actor_label(),'class':c.get_class().get_name(),'rotation':a.get_actor_rotation().to_tuple(),**{n:prop(c,n) for n in ['mobility','intensity','cast_shadows','light_source_angle','dynamic_shadow_distance_movable_light','shadow_bias','use_ray_traced_distance_field_shadows']}})
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  m=c.static_mesh
  if not m or not any(s in m.get_name() for s in ['Oak','Birch','FruitTree']):continue
  if c.get_editor_property('hidden_in_game'):continue
  out['trees'].append({'actor':a.get_actor_label(),'object':a.get_name(),'mesh':m.get_path_name(),'position':a.get_actor_location().to_tuple(),'rotation':a.get_actor_rotation().to_tuple(),'scale':a.get_actor_scale3d().to_tuple(),'shadow':prop(c,'cast_shadow'),'materials':[c.get_material(i).get_path_name() if c.get_material(i) else None for i in range(c.get_num_materials())]})
  for j in range(c.get_num_materials()):
   mat=c.get_material(j)
   if not mat or mat.get_path_name() in out['materials']:continue
   base=mat.get_base_material();expr=unreal.MaterialEditingLibrary.get_material_expressions(base) if hasattr(unreal.MaterialEditingLibrary,'get_material_expressions') else []
   out['materials'][mat.get_path_name()]={'base':base.get_path_name(),'blend':prop(base,'blend_mode'),'two_sided':prop(base,'two_sided'),'expressions':[x.get_class().get_name() for x in expr]}
 if isinstance(a,unreal.PostProcessVolume):out['post'].append({'actor':a.get_actor_label(),'unbound':prop(a,'unbound'),'settings':str(a.settings)})
(O/'SceneBefore.json').write_text(json.dumps(out,indent=2))
unreal.log('TREE_SHADOW_AUDIT_DONE '+str(len(out['trees'])))
