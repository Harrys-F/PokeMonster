"""Finalize only this task's owned assets outside PIE; check disk references and terrain sections."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/WestlandRegion';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert E.get_editor_world().get_name()=='Dev_WestlandRegion';ss=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);assets=[];sections=[];textures=[]
for path in unreal.EditorAssetLibrary.list_assets('/Game/Environment/WestlandRegion',True,False):
 obj=unreal.load_asset(path);assert obj,path
 if isinstance(obj,unreal.StaticMesh) and obj.get_name().startswith('SM_WR_Terrain_'):
  assert ss.is_section_collision_enabled(obj,0,0),path;sections.append(path)
 assert unreal.EditorAssetLibrary.save_loaded_asset(obj,False),path;assets.append(path)
for x in unreal.ObjectIterator(unreal.MaterialExpressionTextureObjectParameter):
 if x.get_outer().get_path_name().startswith('/Game/Environment/WestlandRegion'):
  t=x.get_editor_property('texture');assert t and unreal.load_asset(t.get_path_name());textures.append(t.get_path_name())
assert len(sections)==80;assert any('T_WR_PathCoverage' in p for p in textures);assert unreal.EditorLoadingAndSavingUtils.save_map(E.get_editor_world(),'/Game/Maps/Dev_WestlandRegion');(O/'FinalAssetAudit.json').write_text(json.dumps({'passed':True,'saved_assets':assets,'collision_terrain_sections':len(sections),'resolved_textures':sorted(set(textures))},indent=2));unreal.log('REGION_SAVED_ASSET_AUDIT_PASS')
