"""Visual review correction: quieter painted boards, woven textiles, aligned joinery, own FBX QA."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ProjectRefinement';D='/Game/Environment/VisualV2HealingArtV4';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);L=unreal.MaterialEditingLibrary;w=E.get_editor_world();assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not (S/'SurfaceFinish.json').exists()
changed=[];tex=unreal.load_asset('/Game/Environment/HealingHouse/QualityV2/Textures/T_HH_PaintedWood')
for key in ['Floor','Wood','Timber']:
 m=unreal.load_asset(D+'/Materials/M_HH_Interior'+key)
 for n in L.get_material_expressions(m):
  if isinstance(n,unreal.MaterialExpressionTextureObjectParameter):n.set_editor_property('texture',tex)
  if key=='Floor' and isinstance(n,unreal.MaterialExpressionCustom):
   code=n.get_editor_property('code');assert 'q.x/162,q.y/46' in code;code=code.replace('q.x/162,q.y/46','q.y/175+row*.127,q.x/340+shift*.001').replace('*(.92+.16*h)','*(.93+.12*h)').replace('(.77,.70,.58)','(.84,.79,.69)');n.set_editor_property('code',code)
 L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);changed.append(m.get_path_name())
cloth=unreal.load_asset('/Game/Environment/HealingHouse/QualityV2/Textures/T_HH_PaintedCloth')
for key,col in [('Sage',(.19,.27,.17)),('Linen',(.68,.61,.46))]:
 m=unreal.load_asset(D+'/Materials/M_HH_Interior'+key);n=next(n for n in L.get_material_expressions(m) if isinstance(n,unreal.MaterialExpressionCustom));uv=next(n for n in L.get_material_expressions(m) if isinstance(n,unreal.MaterialExpressionTextureCoordinate));t=L.create_material_expression(m,unreal.MaterialExpressionTextureObjectParameter);t.set_editor_property('parameter_name','PaintedLinen');t.set_editor_property('texture',cloth);args=[]
 for k in ['UV','Tex']:i=unreal.CustomInput();i.set_editor_property('input_name',k);args.append(i)
 n.set_editor_property('inputs',args);assert L.connect_material_expressions(uv,'',n,'UV') and L.connect_material_expressions(t,'',n,'Tex')
 n.set_editor_property('code','float3 c=Texture2DSample(Tex,TexSampler,UV*.8).rgb;float value=dot(c,float3(.299,.587,.114));float weave=.5+.5*sin(UV.x*276)*sin(UV.y*251);return float3('+','.join(map(str,col))+')*(.65+value*1.5)*(1+.018*(weave-.5));');L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);changed.append(m.get_path_name())
# Reimport only the three newly authored assets; never touch original assets or sources.
AT=unreal.AssetToolsHelpers.get_asset_tools();stats=[]
for row in json.loads((R/'Art/HealingHouse/ApothecaryDetails.json').read_text())['assets']:
 key=row['name'];name='SM_HH_'+key;path=D+'/Meshes/'+name;assert unreal.load_asset(path)
 ui=unreal.FbxImportUI();ui.import_mesh=True;ui.import_materials=False;ui.import_textures=False;ui.import_as_skeletal=False;ui.automated_import_should_detect_type=False;ui.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
 for k,v in {'combine_meshes':True,'auto_generate_collision':False,'convert_scene':True,'convert_scene_unit':True,'transform_vertex_to_absolute':True}.items():ui.static_mesh_import_data.set_editor_property(k,v)
 ui.static_mesh_import_data.set_editor_property('vertex_color_import_option',unreal.VertexColorImportOption.REPLACE)
 task=unreal.AssetImportTask();task.filename=str(R/'Art/HealingHouse/Exports'/(name+'.fbx'));task.destination_path=D+'/Meshes';task.destination_name=name;task.replace_existing=True;task.options=ui;task.automated=True;task.save=False;AT.import_asset_tasks([task]);mesh=unreal.load_asset(path);mesh.set_material(0,unreal.load_asset(D+'/Materials/M_HH_HandcraftedSurface'));assert mesh.get_num_triangles(0)==row['triangles'],(name,mesh.get_num_triangles(0),row['triangles']);assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).get_simple_collision_count(mesh)==0;assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,False);stats.append({'asset':path,'triangles':mesh.get_num_triangles(0),'materials':len(mesh.get_editor_property('static_materials'))})
actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)}
for label,y in [('Refined_PorchCorbel_4',373),('Refined_PorchCorbel_5',627)]:
 a=actors[label];a.set_actor_location(unreal.Vector(-3593,y,184),False,True);a.static_mesh_component.set_material(0,unreal.load_asset(D+'/Materials/M_HH_RefinedTimber'))
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');(S/'SurfaceFinish.json').write_text(json.dumps({'changed_materials':changed,'new_mesh_export_reimport':stats,'only_new_joinery_transforms_changed':True},indent=2));unreal.log('REVIEWED_ART_SURFACES_SAVED')
