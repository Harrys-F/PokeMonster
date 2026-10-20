"""Bounded V7 path finish and replacement fern silhouettes; no lighting or collision changes."""
import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ArtPassV3';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert not E.get_game_world() and w.get_name()=='Dev_TestMap_VisualV2';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not (S/'LandscapeApplied.json').exists()
L=unreal.MaterialEditingLibrary;D='/Game/Environment/VisualV2WorldArtV7/Meshes';fol=unreal.load_asset('/Game/Environment/VisualV2HealingArtV4/Materials/M_HA4_Foliage');assert fol and fol.get_editor_property('used_with_instanced_static_meshes');meshes={};meshstats=[]
for row in json.loads((R/'Art/World/VisualV2WorldArtV7/FernRefinement.json').read_text())['meshes']:
 key=row['variant'];name='SM_WA7_Fern_'+key;path=D+'/'+name;assert not unreal.EditorAssetLibrary.does_asset_exist(path)
 ui=unreal.FbxImportUI();ui.import_mesh=True;ui.import_materials=False;ui.import_textures=False;ui.import_as_skeletal=False;ui.automated_import_should_detect_type=False;ui.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
 for k,v in {'combine_meshes':True,'auto_generate_collision':False,'convert_scene':True,'convert_scene_unit':True,'transform_vertex_to_absolute':True,'vertex_color_import_option':unreal.VertexColorImportOption.REPLACE,'normal_import_method':unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,'normal_generation_method':unreal.FBXNormalGenerationMethod.MIKK_T_SPACE}.items():ui.static_mesh_import_data.set_editor_property(k,v)
 t=unreal.AssetImportTask();t.filename=str(R/'Art/World/VisualV2WorldArtV7/Exports'/(name+'.fbx'));t.destination_path=D;t.destination_name=name;t.options=ui;t.automated=True;t.save=False;unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t]);m=unreal.load_asset(path);assert m and m.get_num_triangles(0)==row['triangles'];m.set_material(0,fol);assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).get_simple_collision_count(m)==0;assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);meshes['SM_WLA_Fern_'+key]=m;meshstats.append({'path':m.get_path_name(),'triangles':m.get_num_triangles(0),'material_slots':len(m.static_materials)})
changes=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if not c.static_mesh or c.static_mesh.get_name() not in meshes:continue
  old=c.static_mesh.get_path_name();count=c.get_instance_count() if isinstance(c,unreal.InstancedStaticMeshComponent) else 1;shadow=bool(c.cast_shadow);collision=c.get_collision_profile_name();c.set_static_mesh(meshes[c.static_mesh.get_name()]);c.set_editor_property('override_materials',[fol]);assert bool(c.cast_shadow)==shadow and c.get_collision_profile_name()==collision;changes.append({'actor':a.get_name(),'label':a.get_actor_label(),'component':c.get_name(),'before':old,'after':c.static_mesh.get_path_name(),'instances':count})
assert len(changes)==12 and sum(c['instances'] for c in changes)==224,changes
# Identical field correction in color and opacity. All centre-line segments remain byte-identical.
a='float v6EdgeNoise=4*sin(v6p.x*.077+sin(v6p.y*.05))+3*cos(v6p.y*.113-v6p.x*.027);'
b='v6Half+=(8*sin(v6p.x*.0047+sin(v6p.y*.0031))+4*cos(v6p.y*.0093-v6p.x*.0029))*v6BridgeProtected;\n'+a+'\nv6EdgeNoise+=3*sin(v6p.x*.039-v6p.y*.023)*v6BridgeProtected;'
oldcolor='v6PathColor*=1-.045*tread+.045*(artMottle-.5);'
newcolor=oldcolor+'\n// Quiet warm highlights through albedo only: no emissive shadow lift or lighting changes.\nfloat artValue=dot(v6PathColor,float3(.2126,.7152,.0722));v6PathColor=lerp(v6PathColor,artValue.xxx,.085);'
graphchanges=[]
for key in ['Ground','NorthPath','MainPath']:
 m=unreal.load_asset('/Game/Environment/VisualV2HealingArtV4/Materials/M_HH_Landscape'+key);assert m
 for n in L.get_material_expressions(m):
  if not isinstance(n,unreal.MaterialExpressionCustom):continue
  old=n.get_editor_property('code');assert old.count(a)==1;new=old.replace(a,b)
  if oldcolor in new:new=new.replace(oldcolor,newcolor)
  n.set_editor_property('code',new);graphchanges.append({'material':m.get_path_name(),'expression':n.get_name(),'before_code':old,'after_code':new})
 L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2')
j={'ferns':meshstats,'bindings':changes,'instances_preserved':224,'path_width_added_cm':[8,4],'edge_added_cm':3,'path_centrelines_and_collision_unchanged':True,'bridge_mask_preserved':True,'albedo_saturation_reduction':.085,'outdoor_light_shadow_settings_unchanged':True};(S/'LandscapeApplied.json').write_text(json.dumps(j,indent=2));(R/'Art/World/VisualV2WorldArtV7/ArtPassV3_Landscape.json').write_text(json.dumps(j,indent=2));(R/'Art/World/VisualV2WorldArtV7/ArtPassV3_PathGraphs.json').write_text(json.dumps(graphchanges,indent=2));unreal.log('ART_V3_LANDSCAPE_SAVED')
