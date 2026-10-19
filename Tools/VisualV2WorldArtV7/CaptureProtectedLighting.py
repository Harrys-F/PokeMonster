import unreal,json,re
from pathlib import Path
R=Path(unreal.Paths.project_dir());S=R/'Saved/VisualV2WorldArtV7';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 for c in a.get_components_by_class(unreal.LightComponentBase):
  props={}
  for k in ['intensity','light_color','indirect_lighting_intensity','volumetric_scattering_intensity','cast_shadows','cast_dynamic_shadows','cast_static_shadows','shadow_amount','shadow_bias','shadow_slope_bias','shadow_sharpen','contact_shadow_length','source_angle','soft_source_angle','temperature','use_temperature','mobility','lower_hemisphere_color','lower_hemisphere_is_black','real_time_capture','cubemap','source_type']:
   try:props[k]=re.sub(r'0x[0-9a-fA-F]+','ADDRESS',str(c.get_editor_property(k)))
   except Exception:pass
  rows.append({'actor':a.get_name(),'component':c.get_name(),'location':a.get_actor_location().to_tuple(),'rotation':a.get_actor_rotation().to_tuple(),'properties':props})
rows.sort(key=lambda x:(x['actor'],x['component']));base=S/'ProtectedLightingBefore.json'
if base.exists():
 assert json.loads(json.dumps(rows))==json.loads(base.read_text()),'Unexpected lighting or shadow change';(S/'ProtectedLightingAfter.json').write_text(json.dumps(rows,indent=2))
else:base.write_text(json.dumps(rows,indent=2))
unreal.log('WA7_PROTECTED_LIGHTS_VERIFIED')
