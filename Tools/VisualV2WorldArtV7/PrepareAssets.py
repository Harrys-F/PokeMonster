"""Private V7 ground and ribbon materials: extend the approved route surface field only."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir());S=R/'Saved/VisualV2WorldArtV7';A=R/'Art/World/VisualV2WorldArtV7';D='/Game/Environment/VisualV2WorldArtV7';L=unreal.MaterialEditingLibrary
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert not unreal.EditorAssetLibrary.does_directory_exist(D)
old=(R/'Art/World/VisualV2WorldArtV6/RouteField.hlsl').read_text();new=(A/'RouteField.hlsl').read_text();rows=[]
for key in ['Ground','NorthPath','MainPath']:
 src='/Game/Environment/VisualV2WorldArtV6/Materials/M_WA6_'+key;dst=D+'/Materials/M_WA7_'+key
 m=unreal.EditorAssetLibrary.duplicate_asset(src,dst);assert m
 changes=[]
 for n in L.get_material_expressions(m):
  if not isinstance(n,unreal.MaterialExpressionCustom):continue
  code=n.get_editor_property('code')
  if old not in code:continue
  assert code.count(old)==1;after=code.replace(old,new)
  if n.get_editor_property('output_type')==unreal.CustomMaterialOutputType.CMOT_FLOAT3:
   needle='g=lerp(g,v6ForestSurface,v6F*.76);';assert needle in after
   after=after.replace(needle,needle+'g=lerp(g,waMeadow*float3(.75,.83,.70)*(1+.055*waNoise),v6M*.72);')
  n.set_editor_property('code',after);changes.append(n.get_name());assert all(L.get_inputs_for_material_expression(m,n))
 assert len(changes)==(1 if key=='Ground' else 2)
 L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
 rows.append({'key':key,'old':unreal.load_asset(src).get_path_name(),'new':m.get_path_name(),'changed_custom_nodes':changes})
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(S/'Prepared.json').write_text(json.dumps({'materials':rows},indent=2));(A/'AssetManifest.json').write_text(json.dumps({'materials':rows,'new_meshes':0,'new_textures':0,'shadow_change':False},indent=2));unreal.log('WA7_PRIVATE_MATERIALS_READY')
