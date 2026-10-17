import unreal,json,collections
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not E.get_game_world()
out={'map':E.get_editor_world().get_path_name(),'dirty_maps':[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
assert not out['dirty_maps'] and not out['dirty_content'],'Existing editor changes must be preserved'
unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2');w=E.get_editor_world()
def prop(o,n):
 try:return str(o.get_editor_property(n))
 except Exception:return None
out['cvars']={n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in ['r.Shadow.Virtual.Enable','r.ShadowQuality','r.Shadow.MaxResolution','r.Shadow.DistanceScale','r.Shadow.CSM.MaxCascades','r.Shadow.Virtual.ResolutionLodBiasDirectional','r.Shadow.Virtual.SMRT.RayCountDirectional','r.AmbientOcclusionLevels','r.BloomQuality','r.Tonemapper.Quality','r.AntiAliasingMethod','r.PostProcessAAQuality','r.TemporalAA.Upsampling','r.TSR.History.ScreenPercentage','r.SSR.Quality','r.Lumen.DiffuseIndirect.Allow','r.Lumen.Reflections.Allow','r.MotionBlurQuality','r.DepthOfFieldQuality','r.SceneColorFringeQuality','r.EyeAdaptationQuality','r.ScreenPercentage','r.SecondaryScreenPercentage.GameViewport','r.Editor.Viewport.OverridePIEScreenPercentage']}
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors();out['actor_count']=len(actors);out['static_components']=[];out['lights']=[];out['postprocessing']=[];meshes={};materials={}
for a in actors:
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  m=c.static_mesh
  if not m:continue
  name=m.get_path_name();count=c.get_instance_count() if isinstance(c,unreal.InstancedStaticMeshComponent) else 1
  out['static_components'].append({'actor':a.get_actor_label(),'component':c.get_name(),'mesh':name,'instances':count,'visible':c.is_visible(),'shadow':prop(c,'cast_shadow'),'mobility':prop(c,'mobility'),'min_draw_distance':prop(c,'min_draw_distance'),'max_draw_distance':prop(c,'ld_max_draw_distance'),'instance_cull_start':prop(c,'instance_start_cull_distance'),'instance_cull_end':prop(c,'instance_end_cull_distance'),'bounds':str(c.get_world_location()),'materials':[c.get_material(i).get_path_name() if c.get_material(i) else None for i in range(c.get_num_materials())]})
  if name not in meshes:
   meshes[name]={'lod_count':unreal.EditorStaticMeshLibrary.get_lod_count(m),'lod_triangles':[unreal.EditorStaticMeshLibrary.get_lod_count(m)]}
   try:meshes[name]['lod_triangles']=[unreal.EditorStaticMeshLibrary.get_number_verts(m,i) for i in range(unreal.EditorStaticMeshLibrary.get_lod_count(m))];meshes[name]['counts_are_vertices']=True
   except Exception:pass
  for i in range(c.get_num_materials()):
   mat=c.get_material(i)
   if mat and mat.get_path_name() not in materials:materials[mat.get_path_name()]={'blend_mode':prop(mat,'blend_mode'),'two_sided':prop(mat,'two_sided'),'parent':prop(mat,'parent')}
 for c in a.get_components_by_class(unreal.LightComponent):
  out['lights'].append({'actor':a.get_actor_label(),'class':c.get_class().get_name(),'visible':c.is_visible(),**{n:prop(c,n) for n in ['mobility','cast_shadows','cast_dynamic_shadows','intensity','attenuation_radius','dynamic_shadow_distance_movable_light','dynamic_shadow_distance_stationary_light','num_dynamic_shadow_cascades']}})
 if isinstance(a,unreal.PostProcessVolume):
  s=a.get_editor_property('settings');out['postprocessing'].append({'actor':a.get_actor_label(),'unbound':prop(a,'unbound'),'enabled':prop(a,'enabled'),'blend_weight':prop(a,'blend_weight'),'settings':str(s)})
out['meshes']=meshes;out['materials']=materials
(O/'EditorAudit.json').write_text(json.dumps(out,indent=2))
