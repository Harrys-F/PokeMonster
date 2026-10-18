"""Read-only full scene mesh/LOD/Nanite inventory; run outside timing windows."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2GPUBottleneckV1';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();meshes={}
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  m=c.static_mesh
  if not m:continue
  key=m.get_path_name()
  if key not in meshes:
   d={'nanite_enabled':m.get_editor_property('nanite_settings').get_editor_property('enabled'),'lods':[{'triangles':m.get_num_triangles(i),'sections':m.get_num_sections(i)} for i in range(m.get_num_lods())],'components':[]};meshes[key]=d
  meshes[key]['components'].append({'actor':a.get_actor_label(),'visible':c.is_visible(),'hidden_in_game':c.get_editor_property('hidden_in_game'),'instances':c.get_instance_count() if isinstance(c,unreal.InstancedStaticMeshComponent) else 1,'class':c.get_class().get_name(),'forced_lod':c.get_editor_property('forced_lod_model'),'min_lod':c.get_editor_property('min_lod'),'override_min_lod':c.get_editor_property('override_min_lod')})
(O/'AllMeshInventory.json').write_text(json.dumps({'world':w.get_path_name(),'meshes':meshes},indent=2))
