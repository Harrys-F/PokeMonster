
# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import unreal,json,collections
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV3';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=e.get_editor_world();assert not e.get_game_world();assert w.get_name()=='Dev_TestMap_EnvironmentPerfV3'
meshes={};lights=[];volumes=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  sm=c.static_mesh
  if not sm or not sm.get_name().startswith('SM_WLA_'):continue
  if not any(x in sm.get_name() for x in ['Oak','Birch','Bush','Fern','Grass','Flower','Herb']):continue
  row=meshes.setdefault(sm.get_path_name(),{'components':[],'materials':[],'lods':[]})
  row['components'].append({'actor':a.get_actor_label(),'component_class':c.get_class().get_name(),'instances':c.get_instance_count() if isinstance(c,unreal.InstancedStaticMeshComponent) else 1,'shadow':c.cast_shadow,'forced_lod':c.get_editor_property('forced_lod_model'),'cull_start':c.get_editor_property('instance_start_cull_distance') if isinstance(c,unreal.InstancedStaticMeshComponent) else None,'cull_end':c.get_editor_property('instance_end_cull_distance') if isinstance(c,unreal.InstancedStaticMeshComponent) else None})
  if not row['materials']:
   for mi in range(sm.get_num_sections(0)):
    m=c.get_material(mi);b=m.get_base_material() if m else None
    row['materials'].append({'instance':m.get_path_name() if m else None,'base':b.get_path_name() if b else None,'blend':str(b.get_editor_property('blend_mode')) if b else None,'two_sided':b.get_editor_property('two_sided') if b else None,'clip':b.get_editor_property('opacity_mask_clip_value') if b else None,'wpo':str(unreal.MaterialEditingLibrary.get_material_property_input_node(b,unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET)) if b else None,'texture_parameters':[str(x) for x in unreal.MaterialEditingLibrary.get_texture_parameter_names(b)] if b else []})
   for i in range(sm.get_num_lods()):row['lods'].append({'index':i,'triangles':sm.get_num_triangles(i),'sections':sm.get_num_sections(i)})
 for c in a.get_components_by_class(unreal.LightComponent):lights.append({'actor':a.get_actor_label(),'class':c.get_class().get_name(),'rotation':a.get_actor_rotation().to_tuple(),'intensity':c.get_editor_property('intensity'),'shadow':c.cast_shadows})
 if isinstance(a,unreal.PostProcessVolume):
  s=a.get_editor_property('settings');volumes.append({'label':a.get_actor_label(),'unbound':a.get_editor_property('unbound'),'settings':str(s)})
(O/'VegetationLightingAudit.json').write_text(json.dumps({'world':w.get_path_name(),'meshes':meshes,'lights':lights,'postprocess':volumes},indent=2))
