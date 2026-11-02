"""Validate own material input connections after graph edits, before visual acceptance."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualUpgradeV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();rows=[]
for key in ['Grass','PathBlend','River']:
 m=unreal.load_asset('/Game/Environment/WestlandVisualUpgradeV1/Materials/M_WVU_'+key);removed=0
 for n in unreal.MaterialEditingLibrary.get_material_expressions(m):
  if not isinstance(n,unreal.MaterialExpressionCustom):continue
  seen=set();valid=[]
  for v in n.get_editor_property('inputs'):
   name=str(v.get_editor_property('input_name'))
   if name in seen and 'Expression=None'in v.export_text():removed+=1;continue
   assert name not in seen,('Duplicate connected input',key,name);assert 'Expression=None'not in v.export_text(),(key,name);seen.add(name);valid.append(v)
  n.set_editor_property('inputs',valid)
 unreal.MaterialEditingLibrary.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);rows.append(dict(material=key,unconnected_duplicate_inputs_removed=removed,all_custom_inputs_connected=True))
(D/'SurfaceValidation.json').write_text(json.dumps(rows,indent=2));unreal.log('WESTLAND_VISUAL_FINAL_SURFACES_VALIDATED')
