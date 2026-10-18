"""Synchronous scoped-state check in PIE, outside all performance windows."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2AASoftShadowsV1';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name()=='Dev_TestMap_VisualV2GPUBottleneckV1'
def snapshot():
 out={'components':{},'lights':{},'postprocess':{}}
 for c in unreal.ObjectIterator(unreal.PrimitiveComponent):
  if c.get_world()!=w or not c.get_owner():continue
  out['components'][c.get_path_name()]={'owner_class':c.get_owner().get_class().get_name(),'owner':c.get_owner().get_name(),'shadow':c.cast_shadow,'visible':c.is_visible(),'hidden':c.hidden_in_game,'transform':c.get_world_transform().export_text(),'collision':str(c.get_collision_enabled()),'mesh':c.static_mesh.get_path_name() if isinstance(c,unreal.StaticMeshComponent) and c.static_mesh else None,'materials':[c.get_material(i).get_path_name() if c.get_material(i) else None for i in range(c.get_num_materials())]}
 for cls in [unreal.LightComponent,unreal.SkyLightComponent]:
  for c in unreal.ObjectIterator(cls):
   if c.get_world()!=w:continue
   props={}
   for n in ['intensity','light_color','indirect_lighting_intensity','cast_shadows','source_angle','source_soft_angle','light_source_angle','light_source_soft_angle','temperature','use_temperature','real_time_capture','cubemap','volumetric_scattering_intensity']:
    try:
     value=c.get_editor_property(n);props[n]=value.get_path_name() if isinstance(value,unreal.Object) else value.export_text() if hasattr(value,'export_text') else str(value)
    except Exception:pass
   out['lights'][c.get_path_name()]={'transform':c.get_world_transform().export_text(),'properties':props}
 for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PostProcessVolume):out['postprocess'][a.get_name()]={'settings':a.settings.export_text(),'transform':a.get_actor_transform().export_text(),'priority':a.priority,'weight':a.blend_weight}
 return out
before=snapshot();unreal.SystemLibrary.execute_console_command(w,'pm.SoftShadows.Test 1');after=snapshot();changed=[]
assert before['lights']==after['lights'] and before['postprocess']==after['postprocess']
assert set(before['components'])==set(after['components'])
for path,old in before['components'].items():
 new=after['components'][path];rest=dict(new);rest['shadow']=old['shadow'];assert rest==old,(path,'Unexpected component change')
 if old['shadow']!=new['shadow']:
  assert old['shadow'] and not new['shadow'];changed.append({'path':path,'owner_class':old['owner_class']})
assert changed,'No shadow casters changed'
for row in changed:
 old=before['components'][row['path']]
 if old['owner_class'] in ['StaticMeshActor','Actor']:
  name=(old['mesh'] or '').rsplit('.',1)[-1];assert name.startswith('SM_WLA_') and any(k in name for k in ['Oak','Birch','Bush','Grass','Fern','Flower','Herb']),(row,name)
 assert old['owner_class'] in ['PokeMonsterPlayerCharacter','PokeMonsterNPCVisualActor','PokeMonsterNPC','PokeMonsterTrainerNPC','PokeMonsterVisibleWildCreatureActor','StaticMeshActor','Actor'],row
unreal.SystemLibrary.execute_console_command(w,'pm.SoftShadows.Test 0');restored=snapshot();assert before==restored,'Original primitive/light/postprocess state not restored'
(O/'RuntimeInvariant.json').write_text(json.dumps({'passed':True,'before':before,'after':after,'restored_exactly':True,'changed_shadow_components':changed,'unchanged_light_components':len(before['lights']),'unchanged_postprocess_volumes':len(before['postprocess'])},indent=2))
