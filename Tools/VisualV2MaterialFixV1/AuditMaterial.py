"""Read-only material/instance/texture and scene audit. Does not check/set usage."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2MaterialFixV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
j=json.loads((O/'Request.json').read_text());phase=j['phase'];base='/Game/Environment/WestlandAssetLibrary/QualityV3/Materials/'
m=unreal.load_asset(base+'M_WLA_FoliageGroups_V3');mi=unreal.load_asset(base+'MI_WLA_FoliageGroups_V3');assert mi.parent==m
props=['material_domain','blend_mode','two_sided','opacity_mask_clip_value','shading_model','dithered_lod_transition','use_material_attributes','used_with_instanced_static_meshes','automatically_set_usage_in_editor','used_with_skeletal_mesh']
def properties(obj,names):
 d={}
 for name in names:
  try:d[name]=str(obj.get_editor_property(name))
  except Exception as ex:d[name]='Unavailable: '+str(ex)
 return d
params={}
for kind in ['scalar','vector','texture']:
 names=getattr(unreal.MaterialEditingLibrary,'get_'+kind+'_parameter_names')(m);values={}
 for name in names:
  value=getattr(unreal.MaterialEditingLibrary,'get_material_instance_'+kind+'_parameter_value')(mi,name)
  if kind=='texture' and value:
   values[str(name)]={'path':value.get_path_name(),'width':value.blueprint_get_size_x(),'height':value.blueprint_get_size_y(),'settings':properties(value,['srgb','compression_settings','lod_group','mip_gen_settings','never_stream'])}
  else:values[str(name)]=str(value)
 params[kind]=values
components=[];w=E.get_editor_world()
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if c.static_mesh and 'WildBush' in c.static_mesh.get_name():
   count=c.get_instance_count() if isinstance(c,unreal.InstancedStaticMeshComponent) else 1
   components.append({'actor':a.get_name(),'label':a.get_actor_label(),'component':c.get_name(),'class':c.get_class().get_name(),'mesh':c.static_mesh.get_path_name(),'instances':count,'materials':[c.get_material(i).get_path_name() if c.get_material(i) else None for i in range(c.get_num_materials())]})
inst=[x for x in components if x['class']=='HierarchicalInstancedStaticMeshComponent'];assert len(inst)==2 and sum(x['instances'] for x in inst)==58
registry=unreal.AssetRegistryHelpers.get_asset_registry();deps={}
for x in [m,mi]:
 try:deps[x.get_path_name()]=[str(n) for n in registry.get_referencers(x.get_outermost().get_name(),unreal.AssetRegistryDependencyOptions(include_soft_package_references=True,include_hard_package_references=True))]
 except Exception as ex:deps[x.get_path_name()]={'unavailable':str(ex)}
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
signature=scene(w);(O/(phase+'_Scene.json')).write_text(json.dumps(signature,indent=2))
result={'phase':phase,'world':w.get_path_name(),'master':m.get_path_name(),'instance':mi.get_path_name(),'parent':mi.parent.get_path_name(),'master_properties':properties(m,props),'instance_parameters':params,'instance_properties':properties(mi,['base_property_overrides','scalar_parameter_values','vector_parameter_values','texture_parameter_values','static_parameters']),'components':components,'instanced_groups':inst,'referencers':deps,'dirty_maps':[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
(O/(phase+'_MaterialAudit.json')).write_text(json.dumps(result,indent=2));unreal.SystemLibrary.execute_console_command(w,'MAP CHECK');unreal.log('VMF1_AUDIT '+phase)
