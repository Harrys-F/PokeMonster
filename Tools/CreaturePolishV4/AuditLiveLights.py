import unreal,json
from pathlib import Path
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()or unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();rows=[]
for cls in [unreal.SkyLight,unreal.DirectionalLight]:
 for a in unreal.GameplayStatics.get_all_actors_of_class(w,cls):
  for c in a.get_components_by_class(unreal.LightComponentBase):
   r=dict(actor=a.get_actor_label(),path=a.get_path_name(),component=c.get_class().get_name())
   for key in ['intensity','visible','hidden_in_game','affects_world','lighting_channels','mobility','indirect_lighting_intensity','cast_shadows']:
    try:r[key]=str(c.get_editor_property(key))
    except Exception as e:r[key]=str(e)
   r['hidden_actor']=str(a.get_editor_property('hidden'));rows.append(r)
(Path(unreal.Paths.project_dir())/'Saved/CreaturePolishV4/LiveLights.json').write_text(json.dumps(rows,indent=2))
