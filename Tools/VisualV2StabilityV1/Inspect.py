"""Read existing editor lighting, scoped foliage shader and original quality settings."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2StabilityV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();result={'lights':[],'materials':[],'cvars':{}}
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 for c in a.get_components_by_class(unreal.LightComponent):
  row={'actor':a.get_actor_label(),'component':c.get_path_name(),'rotation':str(a.get_actor_rotation())}
  for key in ['intensity','light_color','temperature','cast_shadows','indirect_lighting_intensity','light_source_angle']:
   try:row[key]=str(c.get_editor_property(key))
   except Exception:pass
  result['lights'].append(row)
for path in ['/Game/Environment/DevTestMapVisualV2/Materials/M_V2_CrownReveal','/Game/Environment/DevTestMapVisualV2/Materials/M_V2_BarkRevealBase']:
 m=unreal.load_asset(path);row={'path':path,'properties':{}}
 for key in ['blend_mode','shading_model','two_sided','opacity_mask_clip_value','use_material_attributes','material_domain']:
  try:row['properties'][key]=str(m.get_editor_property(key))
  except Exception:pass
 nodes=unreal.MaterialEditingLibrary.get_material_expressions(m)if hasattr(unreal.MaterialEditingLibrary,'get_material_expressions')else [o for o in unreal.ObjectIterator(unreal.MaterialExpression)if o.get_outer()==m]
 row['nodes']=[]
 for o in nodes:
  n={'path':o.get_path_name(),'class':o.get_class().get_name()}
  for key in ['code','parameter_name','default_value','output_type','description']:
   try:n[key]=str(o.get_editor_property(key))
   except Exception:pass
  row['nodes'].append(n)
 result['materials'].append(row)
for key in ['r.AntiAliasingMethod','r.ScreenPercentage','sg.ViewDistanceQuality','sg.ShadowQuality','sg.GlobalIlluminationQuality','sg.ReflectionQuality','sg.PostProcessQuality','sg.EffectsQuality','sg.FoliageQuality','r.VSync','t.MaxFPS','r.Shadow.Virtual.Enable']:
 result['cvars'][key]=unreal.SystemLibrary.get_console_variable_float_value(key)
(D/'InitialInspect.json').write_text(json.dumps(result,indent=2));unreal.log('STABILITY_INSPECTION_COMPLETE')
