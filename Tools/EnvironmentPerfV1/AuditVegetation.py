import unreal,json,collections
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV1';a=json.loads((O/'EditorAudit.json').read_text());out={'meshes':{},'summary':{}}
for path in a['meshes']:
 if not any(x in path for x in ['/WestlandAssetLibrary/','/NaturalGroundV1/']):continue
 m=unreal.load_asset(path);comps=[c for c in a['static_components'] if c['mesh']==path and c['visible']];s=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
 out['meshes'][path]={'visible_components':len(comps),'placed_instances':sum(c['instances'] for c in comps),'components_casting_shadow':sum(c['shadow']=='True' for c in comps),'lods':[{'triangles':m.get_num_triangles(i),'vertices':m.get_num_vertices(i),'sections':m.get_num_sections(i),'uv_channels':m.get_num_tex_coords(i)} for i in range(m.get_num_lods())],'screen_sizes':list(s.get_lod_screen_sizes(m)),'material_slots':len(m.static_materials),'materials':[]}
 for slot in m.static_materials:
  mat=slot.material_interface;entry={'path':mat.get_path_name() if mat else None,'parent_chain':[]}
  while mat:
   entry['parent_chain'].append(mat.get_path_name())
   if isinstance(mat,unreal.Material):
    entry['blend_mode']=str(mat.get_editor_property('blend_mode'));entry['two_sided']=mat.get_editor_property('two_sided');break
   try:mat=mat.parent
   except Exception:break
  out['meshes'][path]['materials'].append(entry)
out['summary']={'placed_instances_not_per_view_visible_instances':sum(d['placed_instances'] for d in out['meshes'].values()),'all_lod0_instanced_triangles_upper_bound':sum(d['placed_instances']*d['lods'][0]['triangles'] for d in out['meshes'].values())}
(O/'VegetationAudit.json').write_text(json.dumps(out,indent=2))
