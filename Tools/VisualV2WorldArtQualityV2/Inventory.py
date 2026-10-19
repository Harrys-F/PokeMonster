"""Read-only inventory of precisely the 175 additions and material/shader properties."""
import unreal,json,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtQualityV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();w=E.get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2';rows=[];mats={}
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 if not a.get_actor_label().startswith('WAQ1_'):continue
 c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);m=c.static_mesh;row={'actor':a.get_name(),'label':a.get_actor_label(),'mesh':m.get_path_name(),'count':c.get_instance_count(),'triangles':[m.get_num_triangles(i) for i in range(m.get_num_lods())],'sections':[m.get_num_sections(i) for i in range(m.get_num_lods())],'materials':[c.get_material(i).get_path_name() for i in range(c.get_num_materials())],'transforms':[c.get_instance_transform(i,True).export_text() for i in range(c.get_instance_count())],'forced_lod':c.forced_lod_model};rows.append(row)
 for mi in [c.get_material(i) for i in range(c.get_num_materials())]:
  if mi.get_path_name() in mats:continue
  base=mi.get_base_material();stats=unreal.MaterialEditingLibrary.get_statistics(mi);mats[mi.get_path_name()]={'parent':base.get_path_name(),'two_sided':base.get_editor_property("two_sided"),'blend':str(base.get_editor_property("blend_mode")),'instructions':{n:stats.get_editor_property(n) for n in ['num_vertex_shader_instructions','num_pixel_shader_instructions','num_samplers','num_pixel_texture_samples']},'nodes':[]}
  for x in unreal.ObjectIterator(unreal.MaterialExpression):
   if x.get_outer()!=base:continue
   v={'class':x.get_class().get_name()}
   for prop in ['constant','r','parameter_name','default_value','code']:
    try:value=x.get_editor_property(prop);v[prop]=value.export_text() if hasattr(value,'export_text') else str(value)
    except Exception:pass
   mats[mi.get_path_name()]['nodes'].append(v)
(S/'Inventory.json').write_text(json.dumps({'groups':rows,'materials':mats},indent=2));unreal.log('WORLD_ART_V2_INVENTORY_READY')
