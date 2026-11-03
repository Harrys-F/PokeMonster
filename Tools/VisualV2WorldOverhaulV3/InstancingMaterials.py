"""Own UE5.8 material-instance usage overrides; preserve library material files."""
import unreal,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/VisualV2WorldOverhaulV3/Common.py')));assert not(D/'InstancingMaterials.json').exists();AT=unreal.AssetToolsHelpers.get_asset_tools();variants={};edits=[];usage=unreal.MaterialUsage.MATUSAGE_INSTANCED_STATIC_MESHES
for a in actors.values():
 if a.get_editor_property('hidden'):continue
 for c in a.get_components_by_class(unreal.InstancedStaticMeshComponent):
  if not c.static_mesh or not c.is_visible()or c.get_editor_property('hidden_in_game'):continue
  for i in range(c.get_num_materials()):
   old=c.get_material(i)
   if not old:continue
   p=old.get_path_name()
   if p.startswith('/Game/Environment/WestlandAssetLibrary/Materials/')and old.get_name()in ['MI_WLA_Timber','MI_WLA_LeafOak','MI_WLA_Apple']:
    if p not in variants:
     m=unreal.EditorAssetLibrary.duplicate_asset(p,ROOT+'/Materials/'+old.get_name()+'_WOV');assert m;ML.set_material_usage_override(m,usage,True,True);ML.update_material_instance(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);variants[p]=m
    a.modify();c.set_material(i,variants[p]);edits.append(dict(label=a.get_actor_label(),slot=i,before=p,after=variants[p].get_path_name()))
# Explicit serialized flags for the two earlier own Birch copies as well.
for name in ['MI_WLA_Birch_WOV','MI_WLA_LeafBirch_WOV']:
 m=unreal.load_asset(ROOT+'/Materials/'+name);assert m;ML.set_material_usage_override(m,usage,True,True);ML.update_material_instance(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
save('InstancingMaterials.json',dict(usage_overrides=edits,original_assets_untouched=True))
