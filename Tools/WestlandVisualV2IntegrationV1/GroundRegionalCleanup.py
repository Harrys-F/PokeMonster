"""Remove the inherited VisualV2-local pond term only from the private regional ground."""
import unreal,json,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualV2IntegrationV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();m=unreal.load_asset('/Game/Environment/WestlandVisualV2IntegrationV1/Materials/M_WI_RegionalGround');assert m;changed=[]
for node in unreal.MaterialEditingLibrary.get_material_expressions(m):
 if not isinstance(node,unreal.MaterialExpressionCustom):continue
 before=node.get_editor_property('code')
 if 'float pond=1-smoothstep'not in before:continue
 after,count=re.subn(r'float pond=1-smoothstep.*?c=lerp\(c,soil\*float3\(.55,.50,.43\),submerged\*\.9\);','',before);assert count==1 and 'submerged'not in after;node.set_editor_property('code',after);changed.append(dict(before=before,after=after))
assert len(changed)==1;assert not unreal.MaterialEditingLibrary.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();(D/'GroundRegionalCleanup.json').write_text(json.dumps(dict(passed=True,changes=changed,original_visualv2_unchanged=True),indent=2))
