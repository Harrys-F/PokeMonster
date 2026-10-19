"""Independent V5 regional ground and new botanical imports. Never edits a map/shared asset."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtV5';A=R/'Art/World/VisualV2WorldArtV5';D='/Game/Environment/VisualV2WorldArtV5';L=unreal.MaterialEditingLibrary;AT=unreal.AssetToolsHelpers.get_asset_tools();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not E.get_game_world() and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not (S/'Prepared.json').exists()
marker=S/'AssetWorkSession.json'
if not marker.exists():assert not unreal.EditorAssetLibrary.does_directory_exist(D);marker.write_text(json.dumps({'baseline':'507fa818f5c9445810262ed0f37053ded730df97','private_root':D}))
assert all(p.get_path_name().startswith(D+'/') for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages())
paths=[]
def clone(src,dst):
 m=unreal.load_asset(dst) if unreal.EditorAssetLibrary.does_asset_exist(dst) else unreal.EditorAssetLibrary.duplicate_asset(src,dst);assert m;paths.append(dst);return m
def node(m,typ,x=0,y=0):return L.create_material_expression(m,typ,x,y)
def wire(a,p,b,q):assert L.connect_material_expressions(a,p,b,q)
def tex(name):
 path=D+'/Textures/T_WA5_'+name
 if not unreal.EditorAssetLibrary.does_asset_exist(path):
  t=unreal.AssetImportTask();t.filename=str(A/'Textures'/('T_WA5_'+name+'.png'));t.destination_path=D+'/Textures';t.destination_name='T_WA5_'+name;t.automated=True;t.save=False;AT.import_asset_tasks([t])
 t=unreal.load_asset(path);assert t;t.set_editor_property('srgb',True);t.set_editor_property('power_of_two_mode',unreal.TexturePowerOfTwoSetting.STRETCH_TO_POWER_OF_TWO);t.set_editor_property('max_texture_size',2048);paths.append(path);return t
textures={'Forest':tex('ForestFloor'),'Bank':tex('WetBank'),'Meadow':unreal.load_asset('/Game/Environment/VisualV2HealingArtV4/Textures/T_HA4_Meadow')};assert textures['Meadow']
# Elliptical domains plus a deformed edge, always outside the protected Heilhaus pocket.
masks='''
float waNoise=sin(p.x*.009+sin(p.y*.007))*cos(p.y*.012-p.x*.003);
float waF=(1-smoothstep(.68,1.0,length((p-float2(-3400,1810))/float2(1080,640))+.045*waNoise))*smoothstep(1220,1390,p.y);
float waM=1-smoothstep(.68,1.0,length((p-float2(-2320,-1960))/float2(800,570))+.065*waNoise);
float waRiverRegion=1-smoothstep(.68,1.0,length((p-float2(-250,-320))/float2(950,480))+.045*waNoise);
float waDistance=abs(p.y+320)-66;float waU=waRiverRegion*smoothstep(-5,18,waDistance)*(1-smoothstep(85,205,waDistance));
float waClear=1-.24*(1-smoothstep(.45,1,length((p-float2(-3210,2190))/float2(220,160))));
'''
(A/'RegionalMasks.hlsl').write_text(masks.strip()+'\n')
rows=[];groundlist=[('Ground','/Game/Environment/VisualV2HealingArtV4/Materials/M_HA4_HealingMeadow'),('NorthPath','/Game/Environment/VisualV2HealingArtV4/Materials/M_HA4_HealingPath'),('MainPath','/Game/Environment/DevTestMapVisualV2/Materials/M_V2_PathBlend')]
for key,src in groundlist:
 m=clone(src,D+'/Materials/M_WA5_'+key);color=next(n for n in L.get_material_expressions(m) if isinstance(n,unreal.MaterialExpressionCustom) and n.get_editor_property('output_type')==unreal.CustomMaterialOutputType.CMOT_FLOAT3);code=color.get_editor_property('code');before=code
 args=list(color.get_editor_property('inputs'))
 for name,t in textures.items():
  inp=unreal.CustomInput();inp.set_editor_property('input_name','WA5'+name);args.append(inp)
 color.set_editor_property('inputs',args)
 for i,(name,t) in enumerate(textures.items()):
  n=node(m,unreal.MaterialExpressionTextureObjectParameter,-1300,1200+i*170);n.set_editor_property('parameter_name','WA5'+name);n.set_editor_property('texture',t);wire(n,'',color,'WA5'+name)
 assert 'float2 p=P.xy;' in code;code=code.replace('float2 p=P.xy;','float2 p=P.xy;'+masks,1)
 needle='if(Mode<.5)return g;';assert needle in code
 code=code.replace(needle,'''float2 waTurn=float2(p.y,-p.x);
float3 waForest=Texture2DSample(WA5Forest,WA5ForestSampler,p/155.0+float2(.17,.43)).rgb*.78+Texture2DSample(WA5Forest,WA5ForestSampler,waTurn/267.0+float2(.51,.28)).rgb*.22;
float3 waMeadow=Texture2DSample(WA5Meadow,WA5MeadowSampler,p/240.0+float2(.21,.37)).rgb*.78+Texture2DSample(WA5Meadow,WA5MeadowSampler,waTurn/391.0+float2(.41,.13)).rgb*.22;
float3 waBank=Texture2DSample(WA5Bank,WA5BankSampler,p/170.0+float2(.31,.19)).rgb;
g=lerp(g,waForest*float3(.78,.84,.72)*(1+.06*waNoise)*waClear,waF);
g=lerp(g,waMeadow*float3(.75,.83,.70)*(1+.055*waNoise),waM);
g=lerp(g,waBank*float3(.73,.76,.68),waU*.84);
'''+needle)
 needle='if(Mode<1.5)return d;';assert needle in code
 code=code.replace(needle,'''float waEdge=smoothstep(.45,.96,abs(UV.y*2-1));
float3 waSoil=lerp(d,waForest*float3(.78,.76,.62),waEdge*.38);
d=lerp(d,waSoil*(1+.025*waNoise),waF);
d=lerp(d,lerp(d,g,waEdge*.20),waM);
float waBridgeProtected=smoothstep(105,195,abs(p.x+350));d=lerp(d,waBank*float3(.79,.78,.69),waU*waBridgeProtected*.42);
'''+needle)
 color.set_editor_property('code',code);assert all(L.get_inputs_for_material_expression(m,color));L.recompile_material(m);rows.append({'key':key,'old':unreal.load_asset(src).get_path_name(),'new':m.get_path_name(),'code_before':before,'code_after':code})
# Shared graph mechanics retained for the new vertex-colour botanical forms.
materials={}
for key,src in [('Foliage','Foliage'),('Seed','Blossom')]:
 m=clone('/Game/Environment/VisualV2HealingArtV4/Materials/M_HA4_'+src,D+'/Materials/M_WA5_'+key);m.set_editor_property('used_with_instanced_static_meshes',True);L.recompile_material(m);materials[key]=m
SM=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);meshes=[]
for family,info in json.loads((A/'Details.json').read_text()).items():
 name='SM_WA5_'+family;path=D+'/Meshes/'+name
 if not unreal.EditorAssetLibrary.does_asset_exist(path):
  ui=unreal.FbxImportUI();ui.import_mesh=True;ui.import_materials=False;ui.import_textures=False;ui.import_as_skeletal=False;ui.automated_import_should_detect_type=False;ui.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
  for k,v in {'combine_meshes':True,'auto_generate_collision':False,'convert_scene':True,'convert_scene_unit':True,'transform_vertex_to_absolute':True,'import_uniform_scale':1}.items():ui.static_mesh_import_data.set_editor_property(k,v)
  ui.static_mesh_import_data.set_editor_property('vertex_color_import_option',unreal.VertexColorImportOption.REPLACE)
  t=unreal.AssetImportTask();t.filename=str(A/'Exports'/(name+'.fbx'));t.destination_path=D+'/Meshes';t.destination_name=name;t.options=ui;t.automated=True;t.save=False;AT.import_asset_tasks([t])
 m=unreal.load_asset(path);assert m
 for i,slot in enumerate(m.get_editor_property('static_materials')):
  key=str(slot.get_editor_property('imported_material_slot_name')).split('_')[-1];assert key in materials;m.set_material(i,materials[key])
 assert SM.get_simple_collision_count(m)==0 and m.get_num_triangles(0)==info['triangles'];paths.append(path);meshes.append({'family':family,'path':m.get_path_name(),'triangles':m.get_num_triangles(0)})
for p in paths:assert unreal.EditorAssetLibrary.save_asset(p,False)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
result={'assets':paths,'ground':rows,'meshes':meshes};(S/'Prepared.json').write_text(json.dumps(result,indent=2));(A/'AssetManifest.json').write_text(json.dumps(result,indent=2));unreal.log('WA5_PRIVATE_ASSETS_PREPARED')
