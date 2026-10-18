"""Read-only full scene, vegetation, shader graph, LOD and Nanite audit."""
import unreal,json,runpy,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2VegetationPerfV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=e.get_editor_world();assert not e.get_game_world()
scene=runpy.run_path(str(R/'Tools/VisualV2QualityV2/AuditScene.py'))['scene'];graph=runpy.run_path(str(R/'Tools/VisualV2MaterialFixV1/GraphAudit.py'))['graph'];before=scene(w);meshes={};materials={};ss=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  m=c.static_mesh
  if not m or not m.get_name().startswith('SM_WLA_') or not any(n in m.get_name() for n in ['Oak','Birch','Bush','Fern','Grass','Flower','Herb']):continue
  key=m.get_path_name()
  if key not in meshes:
   d={'nanite_settings':m.get_editor_property('nanite_settings').export_text(),'lods':[{'triangles':m.get_num_triangles(i),'sections':m.get_num_sections(i),'build':ss.get_lod_build_settings(m,i).export_text()} for i in range(m.get_num_lods())],'bounds':[x.to_tuple() for x in [m.get_bounding_box().min,m.get_bounding_box().max]],'components':[]};meshes[key]=d
  meshes[key]['components'].append({'actor':a.get_actor_label(),'component':c.get_name(),'class':c.get_class().get_name(),'instances':c.get_instance_count() if isinstance(c,unreal.InstancedStaticMeshComponent) else 1,'shadow':c.cast_shadow,'materials':[c.get_material(i).get_path_name() if c.get_material(i) else None for i in range(c.get_num_materials())],'forced_lod':c.forced_lod_model,'min_lod':c.min_lod,'override_min_lod':c.override_min_lod})
  for i in range(c.get_num_materials()):
   mi=c.get_material(i)
   if not mi:continue
   b=mi.get_base_material();key=b.get_path_name()
   if key in materials:continue
   d={'example':mi.get_path_name(),'graph':graph(b),'properties':{},'customs':[]}
   for n in ['blend_mode','two_sided','shading_model','opacity_mask_clip_value','used_with_instanced_static_meshes','dithered_lod_transition','use_full_precision','fully_rough','b_use_lightmap_directionality']:
    try:d['properties'][n]=str(b.get_editor_property(n))
    except Exception:pass
   for x in unreal.ObjectIterator(unreal.MaterialExpressionCustom):
    if x.get_outer()==b:d['customs'].append({'name':x.get_name(),'code':x.get_editor_property('code')})
   st=unreal.MaterialEditingLibrary.get_statistics(mi);d['stats']={n:st.get_editor_property(n) for n in ['num_vertex_shader_instructions','num_pixel_shader_instructions','num_samplers','num_pixel_texture_samples','num_vertex_texture_samples']};materials[key]=d
assert before==scene(w),'Audit mutated scene'
(O/'Inventory.json').write_text(json.dumps({'world':w.get_path_name(),'meshes':meshes,'materials':materials,'scene':before},indent=2));unreal.log('VVP1_INVENTORY_COMPLETE')
