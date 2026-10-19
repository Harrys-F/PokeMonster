import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir());S=R/'Saved/VisualV2WorldArtV7';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 for c in a.get_components_by_class(unreal.LightComponent):
  props={}
  for k in ['intensity','light_color','indirect_lighting_intensity','volumetric_scattering_intensity','cast_shadows','cast_dynamic_shadows','cast_static_shadows','shadow_amount','shadow_bias','shadow_slope_bias','shadow_sharpen','contact_shadow_length','source_angle','soft_source_angle','temperature','use_temperature','mobility']:
   try:props[k]=str(c.get_editor_property(k))
   except Exception:pass
  rows.append({'actor':a.get_name(),'label':a.get_actor_label(),'component':c.get_name(),'class':c.get_class().get_name(),'location':a.get_actor_location().to_tuple(),'rotation':a.get_actor_rotation().to_tuple(),'properties':props})
cvars={}
for k in ['r.Shadow.Virtual.Enable','r.ShadowQuality','r.DynamicGlobalIlluminationMethod','r.ReflectionMethod','r.AntiAliasingMethod','sg.ShadowQuality','r.Shadow.CSM.MaxCascades']:
 cvars[k]=unreal.SystemLibrary.get_console_variable_int_value(k)
(S/'ShadowSetup.json').write_text(json.dumps({'lights':rows,'cvars':cvars},indent=2));unreal.log('WA7_SHADOW_SETUP_READONLY')
