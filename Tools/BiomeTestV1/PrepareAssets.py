"""New sandbox-only ground/water/material assets; existing project assets are read-only."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D='/Game/Environment/BiomeTestV1';A=R/'Art/World/BiomeTestV1';L=unreal.MaterialEditingLibrary;T=unreal.AssetToolsHelpers.get_asset_tools();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not E.get_game_world() and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
assert all(p.get_path_name().startswith(D+'/') for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages())
def material(name):
 path=D+'/Materials/'+name
 if unreal.EditorAssetLibrary.does_asset_exist(path):
  m=unreal.load_asset(path)
  assert unreal.EditorAssetLibrary.get_metadata_tag(m,'BiomeTestOwner')=='V1' or not (R/'Content/Environment/BiomeTestV1/Materials'/(name+'.uasset')).exists()
  L.delete_all_material_expressions(m)
 else:m=T.create_asset(name,D+'/Materials',unreal.Material,unreal.MaterialFactoryNew())
 unreal.EditorAssetLibrary.set_metadata_tag(m,'BiomeTestOwner','V1');return m
def ci(name):
 x=unreal.CustomInput();x.set_editor_property('input_name',name);return x
def node(m,cls):return L.create_material_expression(m,cls)
def constant(m,v):
 n=node(m,unreal.MaterialExpressionConstant);n.set_editor_property('r',v);return n
m=material('M_BiomeGround');custom=node(m,unreal.MaterialExpressionCustom);custom.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT3)
custom.set_editor_property('inputs',[ci(x)for x in ['P','V','G','E','F','B','S']])
custom.set_editor_property('code','''float2 uv=P.xy/190.0;
float3 g=Texture2DSample(G,GSampler,uv).rgb;
float3 e=Texture2DSample(E,ESampler,P.xy/230.0).rgb;
float3 f=Texture2DSample(F,FSampler,P.xy/170.0).rgb;
float3 b=Texture2DSample(B,BSampler,P.xy/190.0).rgb;
float3 s=Texture2DSample(S,SSampler,P.xy/240.0).rgb;
float macro=.95+.035*sin(P.x*.0014+sin(P.y*.0009))+.025*sin(P.y*.0021);
float3 c=lerp(g,f,saturate(V.g));c=lerp(c,s*.83,saturate(V.b));c=lerp(c,b,saturate(V.a));c=lerp(c,e*.84,saturate(V.r));
return c*macro;''')
pos=node(m,unreal.MaterialExpressionWorldPosition);vc=node(m,unreal.MaterialExpressionVertexColor);L.connect_material_expressions(pos,'',custom,'P');append=node(m,unreal.MaterialExpressionAppendVector);assert L.connect_material_expressions(vc,'',append,'A');assert L.connect_material_expressions(vc,'A',append,'B');assert L.connect_material_expressions(append,'',custom,'V')
for name,path in {'G':'/Game/Environment/VisualV2HealingArtV4/Textures/T_HA4_Meadow','E':'/Game/Environment/VisualV2HealingArtV4/Textures/T_HA4_Earth','F':'/Game/Environment/VisualV2WorldArtV5/Textures/T_WA5_ForestFloor','B':'/Game/Environment/VisualV2WorldArtV5/Textures/T_WA5_WetBank','S':'/Game/Environment/HealingHouse/QualityV2/Textures/T_HH_PaintedStone'}.items():
 n=node(m,unreal.MaterialExpressionTextureObject);n.set_editor_property('texture',unreal.load_asset(path));assert n.get_editor_property('texture');L.connect_material_expressions(n,'',custom,name)
L.connect_material_property(custom,'',unreal.MaterialProperty.MP_BASE_COLOR);L.connect_material_property(constant(m,.92),'',unreal.MaterialProperty.MP_ROUGHNESS);L.connect_material_property(constant(m,.12),'',unreal.MaterialProperty.MP_SPECULAR);L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
water=material('M_BiomeWater');water.set_editor_property('blend_mode',unreal.BlendMode.BLEND_TRANSLUCENT);water.set_editor_property('translucency_lighting_mode',unreal.TranslucencyLightingMode.TLM_SURFACE_PER_PIXEL_LIGHTING)
n=node(water,unreal.MaterialExpressionCustom);n.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT3);n.set_editor_property('inputs',[ci(x)for x in ['P','T']])
n.set_editor_property('code','''float u=(P.x+P.y)*.70710678,v=(P.x-P.y)*.70710678;
float q=length(float2((u-3200)/1000,(v-2850)/760));float shore=smoothstep(.60,1.08,q);
float wave=pow(saturate(sin(v*.035+sin(u*.012)*2-T*.9)),18)*.020;
float3 c=lerp(float3(.020,.080,.085),float3(.095,.16,.12),shore);return c+wave*float3(.65,.85,.9);''')
p=node(water,unreal.MaterialExpressionWorldPosition);t=node(water,unreal.MaterialExpressionTime);L.connect_material_expressions(p,'',n,'P');L.connect_material_expressions(t,'',n,'T');L.connect_material_property(n,'',unreal.MaterialProperty.MP_BASE_COLOR)
for prop,value in [(unreal.MaterialProperty.MP_OPACITY,.67),(unreal.MaterialProperty.MP_ROUGHNESS,.27),(unreal.MaterialProperty.MP_SPECULAR,.35)]:L.connect_material_property(constant(water,value),'',prop)
L.recompile_material(water);assert unreal.EditorAssetLibrary.save_loaded_asset(water,False)
diag=material('M_WaterDiagnostic');n=node(diag,unreal.MaterialExpressionConstant3Vector);n.set_editor_property('constant',unreal.LinearColor(.1,.8,.55,1));L.connect_material_property(n,'',unreal.MaterialProperty.MP_BASE_COLOR);L.connect_material_property(constant(diag,.5),'',unreal.MaterialProperty.MP_ROUGHNESS);L.recompile_material(diag);assert unreal.EditorAssetLibrary.save_loaded_asset(diag,False)
unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0');tasks=[]
for name in ['SM_BiomeTerrain','SM_BiomeWater']:
 ui=unreal.FbxImportUI()
 for k,v in dict(import_mesh=True,import_materials=False,import_textures=False,import_as_skeletal=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH).items():ui.set_editor_property(k,v)
 for k,v in dict(combine_meshes=True,auto_generate_collision=False,transform_vertex_to_absolute=True,convert_scene=True,convert_scene_unit=True,import_uniform_scale=1.,vertex_color_import_option=unreal.VertexColorImportOption.REPLACE,generate_lightmap_u_vs=True,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS).items():ui.static_mesh_import_data.set_editor_property(k,v)
 task=unreal.AssetImportTask()
 for k,v in dict(filename=str(A/'Exports'/(name+'.fbx')),destination_path=D+'/Meshes',destination_name=name,automated=True,save=False,replace_existing=False,options=ui).items():task.set_editor_property(k,v)
 tasks.append(task)
T.import_asset_tasks(tasks);rows=[]
for name,mat in [('SM_BiomeTerrain',m),('SM_BiomeWater',water)]:
 sm=unreal.load_asset(D+'/Meshes/'+name);assert sm;slots=list(sm.get_editor_property('static_materials'))
 if not slots:slots=[unreal.StaticMaterial(material_interface=mat)]
 else:
  for x in slots:x.set_editor_property('material_interface',mat)
 sm.set_editor_property('static_materials',slots)
 if name=='SM_BiomeTerrain':sm.get_editor_property('body_setup').set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
 assert unreal.EditorAssetLibrary.save_loaded_asset(sm,False);b=sm.get_bounding_box();rows.append({'asset':sm.get_path_name(),'size_cm':(b.max-b.min).to_tuple(),'triangles':sm.get_num_triangles(0)})
(R/'Saved/BiomeTestV1/PreparedAssets.json').write_text(json.dumps(rows,indent=2));assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
