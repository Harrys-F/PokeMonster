import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 for c in a.get_components_by_class(unreal.LightComponentBase):
  row={'actor':a.get_actor_label(),'component':c.get_class().get_name()}
  for p in ['intensity','light_color','use_temperature','temperature','light_source_angle','shadow_amount','cast_shadows','indirect_lighting_intensity','volumetric_scattering_intensity']:
   try:row[p]=str(c.get_editor_property(p))
   except Exception:pass
  rows.append(row)
M=unreal.load_asset('/Game/Environment/WestlandAssetLibrary/Materials/MI_WLA_MossStone');L=unreal.MaterialEditingLibrary
rows.append({'stone_scalars':[str(x)for x in L.get_scalar_parameter_names(M)],'stone_vectors':[str(x)for x in L.get_vector_parameter_names(M)]})
(R/'Saved/ProjectRefinement/EnvironmentV3/DetailAudit.json').write_text(json.dumps(rows,indent=2))
