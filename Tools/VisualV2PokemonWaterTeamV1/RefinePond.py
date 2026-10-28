"""Resolve verified legacy floor/mask overlap, without changing shared materials."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PokemonWaterTeamV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2'and not E.get_game_world()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
path='/Game/Environment/VisualV2PokemonWaterTeamV1/Materials/M_V2PondWater';assert not unreal.EditorAssetLibrary.does_asset_exist(path)
m=unreal.EditorAssetLibrary.duplicate_asset('/Game/Environment/VisualV2EnvironmentV3/Materials/M_EQ3_Stream',path);assert m;changed=0
for n in unreal.MaterialEditingLibrary.get_material_expressions(m):
 if not isinstance(n,unreal.MaterialExpressionCustom):continue
 code=n.get_editor_property('code')
 if 'float2(264,190)'in code:
  assert 'float2(720,-720)'in code
  n.set_editor_property('code',code.replace('float2(720,-720)','float2(720,-1000)').replace('float2(264,190)','float2(900,650)'));changed+=1
assert changed==1;unreal.MaterialEditingLibrary.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
by={a.get_actor_label():a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()};surface=by['P2D_Surface_Pond_Water'];surface.static_mesh_component.set_material(0,m);surface.set_actor_hidden_in_game(False);mesh=surface.static_mesh_component.static_mesh;mesh.set_material(0,m);assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,False)
# Retain the existing full stream surface but remove its old pond mask. The
# expanded pond is a separate, non-overlapping map-owned surface at its bank.
river=by['P2D_OrganicWater'];source=river.static_mesh_component.get_material(0);riverpath='/Game/Environment/VisualV2PokemonWaterTeamV1/Materials/M_V2RiverConnection'
assert not unreal.EditorAssetLibrary.does_asset_exist(riverpath)
rm=unreal.EditorAssetLibrary.duplicate_asset(source.get_path_name(),riverpath);assert rm;nchanged=0
for n in unreal.MaterialEditingLibrary.get_material_expressions(rm):
 if isinstance(n,unreal.MaterialExpressionCustom):
  code=n.get_editor_property('code')
  if 'min(min(stream,outlet),pond)'in code:n.set_editor_property('code',code.replace('min(min(stream,outlet),pond)','min(stream,outlet)'));nchanged+=1
assert nchanged==1;unreal.MaterialEditingLibrary.recompile_material(rm);assert unreal.EditorAssetLibrary.save_loaded_asset(rm,False);river.static_mesh_component.set_material(0,rm)
legacy=[]
for name in ['SM_DevFloor','P2D_BackgroundGround']:
 a=by[name];legacy.append({'name':name,'hidden_before':str(a.get_editor_property('hidden')),'collision_before':a.get_actor_enable_collision()});a.set_actor_hidden_in_game(True);a.set_actor_enable_collision(False)
by['VS_WaterBlockPond'].set_actor_rotation(unreal.Rotator(),False)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert all(p.get_path_name()=='/Game/Maps/Dev_TestMap_VisualV2'for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages())
assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2')
(D/'PondRefined.json').write_text(json.dumps({'material':path,'shared_source_unchanged':True,'legacy':legacy,'barrier_axis_aligned':True},indent=2))
