"""Run after timing: get_statistics may finish shader compilation. Does not edit assets."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV3';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
materials={};components=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  sm=c.static_mesh
  if not sm or not any(n in sm.get_name() for n in ['SM_WLA_Oak','SM_WLA_Birch','SM_WLA_WildBush','SM_WLA_Fern']):continue
  components.append({'actor':a.get_actor_label(),'mesh':sm.get_path_name(),'min_lod':c.get_editor_property('min_lod'),'override_min_lod':c.get_editor_property('override_min_lod'),'forced_lod':c.get_editor_property('forced_lod_model')})
  for i in range(c.get_num_materials()):
   m=c.get_material(i)
   if not m:continue
   b=m.get_base_material();key=b.get_path_name()
   if key in materials:continue
   d={'example_instance':m.get_path_name(),'blend':str(b.get_editor_property('blend_mode')),'clip':b.get_editor_property('opacity_mask_clip_value'),'two_sided':b.get_editor_property('two_sided'),'wpo_node':str(unreal.MaterialEditingLibrary.get_material_property_input_node(b,unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET)),'textures':[]}
   try:
    stats=unreal.MaterialEditingLibrary.get_statistics(m)
    d['compiled_statistics']={n:stats.get_editor_property(n) for n in ['num_vertex_shader_instructions','num_pixel_shader_instructions','num_samplers','num_vertex_texture_samples','num_pixel_texture_samples','num_virtual_texture_samples','num_uv_scalars','num_interpolator_scalars']}
   except Exception as ex:d['statistics_unavailable']=str(ex)
   for n in unreal.MaterialEditingLibrary.get_texture_parameter_names(b):
    try:
     tex=m.get_texture_parameter_value(n) if isinstance(m,unreal.MaterialInstanceDynamic) else unreal.MaterialEditingLibrary.get_material_instance_texture_parameter_value(m,n) if isinstance(m,unreal.MaterialInstanceConstant) else unreal.MaterialEditingLibrary.get_material_default_texture_parameter_value(b,n)
     d['textures'].append({'parameter':str(n),'texture':tex.get_path_name() if tex else None,'width':tex.blueprint_get_size_x() if tex else None,'height':tex.blueprint_get_size_y() if tex else None})
    except Exception as ex:d['textures'].append({'parameter':str(n),'unavailable':str(ex)})
   materials[key]=d
(O/'RuntimeMaterialAudit.json').write_text(json.dumps({'map':w.get_path_name(),'materials':materials,'components':components,'statistics_zero_not_proof_of_no_shader_cost':True},indent=2))
