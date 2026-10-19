"""Create private art variants only. Never modifies the open map or shared assets."""
import unreal,json,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2HealingArtV3';A=R/'Art/World/VisualV2HealingArtV3';D='/Game/Environment/VisualV2HealingArtV3';L=unreal.MaterialEditingLibrary;AT=unreal.AssetToolsHelpers.get_asset_tools();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not (S/'Prepared.json').exists()
marker=S/'AssetWorkSession.json'
if not marker.exists():
 assert not unreal.EditorAssetLibrary.does_directory_exist(D), 'Existing private assets require their owned work-session marker; do not overwrite'
 marker.write_text(json.dumps({'baseline':'716d0c3dfc23e9c5ffa95e57c1a1627f8d6d945b','private_root':D}))
assert all(p.get_path_name().startswith(D+'/') for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()), 'Foreign dirty assets'
paths=[]
def clone(src,dst):
 m=unreal.load_asset(dst) if unreal.EditorAssetLibrary.does_asset_exist(dst) else unreal.EditorAssetLibrary.duplicate_asset(src,dst);assert m;paths.append(dst);return m
def node(m,typ,x,y):return L.create_material_expression(m,typ,x,y)
def wire(a,ao,b,bi):assert L.connect_material_expressions(a,ao,b,bi)
def texfile(file,name):
 task=unreal.AssetImportTask();task.filename=str(file);task.destination_path=D+'/Textures';task.destination_name=name;task.automated=True;task.save=False
 if not unreal.EditorAssetLibrary.does_asset_exist(task.destination_path+'/'+name):AT.import_asset_tasks([task])
 t=unreal.load_asset(task.destination_path+'/'+name);assert t;t.set_editor_property('srgb',True);t.set_editor_property('power_of_two_mode',unreal.TexturePowerOfTwoSetting.STRETCH_TO_POWER_OF_TWO);t.set_editor_property('max_texture_size',2048);paths.append(t.get_path_name().split('.')[0]);return t
g=texfile(A/'Textures/T_HA3_Meadow.png','T_HA3_Meadow');d=texfile(A/'Textures/T_HA3_Earth.png','T_HA3_Earth');ground=[]
for family in ['HealingMeadow','HealingPath','HealingForecourt','LegacyApproach']:
 old='/Game/Environment/VisualV2WorldArtV2/Materials/M_WAQ2_'+family;m=clone(old,D+'/Materials/M_HA3_'+family)
 color=next(n for n in unreal.ObjectIterator(unreal.MaterialExpressionCustom) if n.get_outer()==m and n.get_editor_property('output_type')==unreal.CustomMaterialOutputType.CMOT_FLOAT3);code=next(n for n in unreal.ObjectIterator(unreal.MaterialExpressionCustom) if n.get_outer()==unreal.load_asset(old) and n.get_editor_property('output_type')==unreal.CustomMaterialOutputType.CMOT_FLOAT3).get_editor_property('code');color.set_editor_property('inputs',[i for i in color.get_editor_property('inputs') if str(i.get_editor_property('input_name')) not in ['NewGrass','NewEarth']])
 for key,t in [('NewGrass',g),('NewEarth',d)]:
  inputs=list(color.get_editor_property('inputs'));i=unreal.CustomInput();i.set_editor_property('input_name',key);inputs.append(i);color.set_editor_property('inputs',inputs)
  n=node(m,unreal.MaterialExpressionTextureObjectParameter,-800,1200+200*len(inputs));n.set_editor_property('parameter_name',key);n.set_editor_property('texture',t);wire(n,'',color,key)
 code=re.sub(r'Texture2DSample\((GTex|DTex),\1Sampler,([^;]+?)\)\.rgb',lambda q:'lerp('+q.group(0)+',Texture2DSample('+('NewGrass' if q.group(1)=='GTex' else 'NewEarth')+','+('NewGrass' if q.group(1)=='GTex' else 'NewEarth')+'Sampler,'+q.group(2)+').rgb,localPaint)',code)
 assert code.count('NewGrassSampler')==3 and code.count('NewEarthSampler')==2
 # Small additional macro color drift; avoid a new texture layer or changing path geometry.
 code=code.replace('g*=1+.075*macro;','g*=1+.075*macro;g*=1+localPaint*.035*sin(p.x*.0043+p.y*.0021)*cos(p.y*.0057);')
 color.set_editor_property('code',code);assert all(L.get_inputs_for_material_expression(m,color)), 'Missing ground input';L.delete_unused_expressions(m);L.recompile_material(m);ground.append({'old':old+'.M_WAQ2_'+family,'new':m.get_path_name()})
# Preserve the existing HouseCutaway graph and mask on foliage material copies.
materials={}
for key,original in [('Pot','Ceramic'),('Foliage','Leaf'),('Soil','Ceramic'),('Blossom','FlowerCream')]:
 m=clone('/Game/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_'+original,D+'/Materials/M_HA3_'+key)
 if key in ['Foliage','Blossom']:
  vc=node(m,unreal.MaterialExpressionVertexColor,-600,0);uv=node(m,unreal.MaterialExpressionTextureCoordinate,-600,220);custom=node(m,unreal.MaterialExpressionCustom,-200,0);custom.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT3)
  inputs=[]
  for name in ['C','UV']:
   i=unreal.CustomInput();i.set_editor_property('input_name',name);inputs.append(i)
  custom.set_editor_property('inputs',inputs);wire(vc,'',custom,'C');wire(uv,'',custom,'UV')
  custom.set_editor_property('code','float3 a=lerp(C/12.92,pow(max((C+.055)/1.055,0),2.4),step(.04045,C));float vein=exp(-abs(UV.x-.5)*95)*sin(UV.y*3.14159);float minor=(1-smoothstep(.03,.07,abs(frac(UV.y*7+abs(UV.x-.5)*2.3)-.5)))*sin(UV.y*3.14159);return a*(1+.16*vein+.045*minor);' if key=='Foliage' else 'float3 a=lerp(C/12.92,pow(max((C+.055)/1.055,0),2.4),step(.04045,C));return a;')
  assert L.connect_material_property(custom,'',unreal.MaterialProperty.MP_BASE_COLOR)
 elif key=='Pot':
  sample=node(m,unreal.MaterialExpressionTextureSample,-500,0);sample.set_editor_property('texture',unreal.load_asset('/Game/Environment/HealingHouse/QualityV3/Textures/T_HH_PaintedTerracotta'));assert sample.get_editor_property('texture')
  tint=node(m,unreal.MaterialExpressionMultiply,-160,0);tint.set_editor_property('const_b',.52);wire(sample,'RGB',tint,'A');assert L.connect_material_property(tint,'',unreal.MaterialProperty.MP_BASE_COLOR)
 else:
  c=node(m,unreal.MaterialExpressionConstant3Vector,-200,0);c.set_editor_property('constant',unreal.LinearColor(.045,.026,.012,1));assert L.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR)
 L.delete_unused_expressions(m);L.recompile_material(m);materials[key]=m
SM=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);meshes=[]
for family,info in json.loads((A/'Plants.json').read_text()).items():
 name='SM_HA3_'+family;assert not unreal.EditorAssetLibrary.does_asset_exist(D+'/Meshes/'+name)
 ui=unreal.FbxImportUI();ui.import_mesh=True;ui.import_materials=False;ui.import_textures=False;ui.import_as_skeletal=False;ui.automated_import_should_detect_type=False;ui.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
 for key,value in {'combine_meshes':True,'auto_generate_collision':False,'convert_scene':True,'convert_scene_unit':True,'transform_vertex_to_absolute':True,'import_uniform_scale':1}.items():ui.static_mesh_import_data.set_editor_property(key,value)
 ui.static_mesh_import_data.set_editor_property('vertex_color_import_option',unreal.VertexColorImportOption.REPLACE)
 task=unreal.AssetImportTask();task.filename=str(A/'Exports'/(name+'.fbx'));task.destination_path=D+'/Meshes';task.destination_name=name;task.options=ui;task.automated=True;task.save=False;AT.import_asset_tasks([task]);mesh=unreal.load_asset(D+'/Meshes/'+name);assert mesh
 for i,slot in enumerate(mesh.get_editor_property('static_materials')):
  key=str(slot.get_editor_property('imported_material_slot_name')).split('_')[-1];assert key in materials,key;mesh.set_material(i,materials[key])
 assert SM.get_simple_collision_count(mesh)==0;assert SM.get_number_verts(mesh,0)>0;paths.append(mesh.get_path_name().split('.')[0]);meshes.append({'family':family,'path':mesh.get_path_name(),'triangles':info['triangles'],'materials':mesh.get_num_sections(0) if hasattr(mesh,'get_num_sections') else len(mesh.get_editor_property('static_materials'))})
for p in paths:assert unreal.EditorAssetLibrary.save_asset(p,False),p
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(S/'Prepared.json').write_text(json.dumps({'assets':paths,'ground':ground,'plants':meshes},indent=2));(A/'AssetManifest.json').write_text((S/'Prepared.json').read_text());unreal.log('HA3_PRIVATE_ASSETS_PREPARED')
