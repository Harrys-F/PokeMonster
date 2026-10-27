"""Read-only scene/asset/render inventory, outside timed measurements."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_game_world()or E.get_editor_world();runtime=bool(E.get_game_world());meshes={};materials={};skel={};lights=[];pp=[]
def prop(o,n):
 try:
  v=o.get_editor_property(n);return v.get_path_name()if isinstance(v,unreal.Object)else str(v)
 except Exception:return None
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  m=c.static_mesh
  if not m:continue
  key=m.get_path_name()
  if key not in meshes:meshes[key]={'lods':[{'triangles':m.get_num_triangles(i),'sections':m.get_num_sections(i)}for i in range(m.get_num_lods())],'nanite':prop(m,'nanite_settings'),'components':[]}
  meshes[key]['components'].append({'actor':a.get_actor_label(),'position':a.get_actor_location().to_tuple(),'class':c.get_class().get_name(),'visible':c.is_visible(),'hidden':prop(c,'hidden_in_game'),'instances':c.get_instance_count()if isinstance(c,unreal.InstancedStaticMeshComponent)else 1,'properties':{n:prop(c,n)for n in ['cast_shadow','cast_dynamic_shadow','cast_contact_shadow','affect_distance_field_lighting','forced_lod_model','min_lod','instance_start_cull_distance','instance_end_cull_distance','ld_max_draw_distance']},'materials':[c.get_material(i).get_path_name()if c.get_material(i)else None for i in range(c.get_num_materials())]})
 for c in a.get_components_by_class(unreal.SkeletalMeshComponent):
  m=c.get_editor_property('skeletal_mesh_asset')
  if not m:continue
  key=m.get_path_name();row=skel.setdefault(key,{'materials':[x.material_interface.get_path_name()if x.material_interface else None for x in m.get_editor_property('materials')],'components':[],'lod_info':prop(m,'lod_info')});row['components'].append({'actor':a.get_actor_label(),'shadow':c.cast_shadow,'position':a.get_actor_location().to_tuple()})
 for c in a.get_components_by_class(unreal.PrimitiveComponent):
  for i in range(c.get_num_materials()):
   mi=c.get_material(i)
   if not mi:continue
   b=mi.get_base_material();key=b.get_path_name()
   if key in materials:continue
   row={'properties':{n:prop(b,n)for n in ['blend_mode','shading_model','two_sided','fully_rough','used_with_instanced_static_meshes','used_with_skeletal_mesh','opacity_mask_clip_value']},'textures':{},'stats':{},'noise_nodes':[]};materials[key]=row
   try:row['stats']={n:str(getattr(unreal.MaterialEditingLibrary.get_statistics(b),n))for n in ['num_pixel_shader_instructions','num_vertex_shader_instructions','num_pixel_texture_samples','num_vertex_texture_samples']}
   except Exception as ex:row['stats_error']=str(ex)
   for name in unreal.MaterialEditingLibrary.get_texture_parameter_names(b):
    tex=unreal.MaterialEditingLibrary.get_material_default_texture_parameter_value(b,name)
    if tex:row['textures'][str(name)]={'asset':tex.get_path_name(),'size':[tex.blueprint_get_size_x(),tex.blueprint_get_size_y()]if isinstance(tex,unreal.Texture2D)else None}
   for x in unreal.ObjectIterator(unreal.MaterialExpression):
    if x.get_outer()==b and('Noise'in x.get_class().get_name()or'Custom'in x.get_class().get_name()):row['noise_nodes'].append({'class':x.get_class().get_name(),'name':x.get_name(),'properties':{n:prop(x,n)for n in ['quality','levels','scale','noise_function','code','b_tiling','repeat_size','output_min','output_max']}})
 for c in a.get_components_by_class(unreal.LightComponent):lights.append({'actor':a.get_actor_label(),'rotation':a.get_actor_rotation().to_tuple(),'properties':{n:prop(c,n)for n in ['intensity','cast_shadows','light_source_angle','dynamic_shadow_distance_movable_light','num_dynamic_shadow_cascades','cast_volumetric_shadow','volumetric_scattering_intensity','lighting_channels']}})
 if isinstance(a,unreal.PostProcessVolume):pp.append({'label':a.get_actor_label(),'unbound':a.unbound,'settings':a.settings.export_text()})
cv=['r.AntiAliasingMethod','r.ScreenPercentage','r.DynamicRes.OperationMode','r.Shadow.Virtual.Enable','r.Shadow.Virtual.Cache','r.Shadow.Virtual.SMRT.RayCountDirectional','r.Shadow.Virtual.SMRT.SamplesPerRayDirectional','r.Shadow.Virtual.ResolutionLodBiasDirectional','r.Shadow.MaxResolution','r.Lumen.DiffuseIndirect.Allow','r.Lumen.Reflections.Allow','r.Lumen.HardwareRayTracing','r.Lumen.ScreenProbeGather.DownsampleFactor','r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor','r.Lumen.ScreenProbeGather.RadianceCache.ProbeResolution','r.Nanite','r.RayTracing','r.BloomQuality','r.DepthOfFieldQuality','r.MotionBlurQuality','r.VolumetricFog','r.SkyLight.RealTimeReflectionCapture','r.VSync','r.VSyncEditor','rhi.SyncInterval','t.MaxFPS']+['sg.'+x+'Quality'for x in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']]
result={'world':W.get_path_name(),'runtime':runtime,'actor_count':len(unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)),'meshes':meshes,'skeletal_meshes':skel,'materials':materials,'lights':lights,'postprocess':pp,'cvars':{n:unreal.SystemLibrary.get_console_variable_float_value(n)for n in cv}}
(D/('RuntimeInventory.json'if runtime else'EditorInventory.json')).write_text(json.dumps(result,indent=2));unreal.log('PERFORMANCE_INVENTORY_COMPLETE')
