"""Create independent V4 art assets; no map or original asset changes."""
import unreal,json,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2HealingArtV4';A=R/'Art/World/VisualV2HealingArtV4';D='/Game/Environment/VisualV2HealingArtV4';L=unreal.MaterialEditingLibrary;AT=unreal.AssetToolsHelpers.get_asset_tools();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not E.get_game_world() and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
marker=S/'AssetWorkSession.json'
if not marker.exists():
 assert not unreal.EditorAssetLibrary.does_directory_exist(D);marker.write_text(json.dumps({'baseline':'86685a6','root':D}))
assert all(p.get_path_name().startswith(D+'/') for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages());assert not (S/'Prepared.json').exists()
paths=[]
def clone(src,dst):
 m=unreal.load_asset(dst) or unreal.EditorAssetLibrary.duplicate_asset(src,dst);assert m;paths.append(dst);return m
def node(m,t,x=0,y=0):return L.create_material_expression(m,t,x,y)
def wire(a,ao,b,bi):assert L.connect_material_expressions(a,ao,b,bi),(a,ao,b,bi)
def custom(m,code,inputs,typ=unreal.CustomMaterialOutputType.CMOT_FLOAT3):
 n=node(m,unreal.MaterialExpressionCustom);n.set_editor_property('output_type',typ);args=[]
 for key in inputs:i=unreal.CustomInput();i.set_editor_property('input_name',key);args.append(i)
 n.set_editor_property('inputs',args);n.set_editor_property('code',code)
 for key,(a,pin) in inputs.items():wire(a,pin,n,key)
 return n
def scalar(m,value,prop):
 n=node(m,unreal.MaterialExpressionConstant);n.set_editor_property('r',value);assert L.connect_material_property(n,'',prop)
def texture(name):
 path=D+'/Textures/T_HA4_'+name
 if not unreal.EditorAssetLibrary.does_asset_exist(path):
  t=unreal.AssetImportTask();t.filename=str(A/'Textures'/('T_HA4_'+name+'.png'));t.destination_path=D+'/Textures';t.destination_name='T_HA4_'+name;t.automated=True;t.save=False;AT.import_asset_tasks([t])
 t=unreal.load_asset(path);assert t;t.set_editor_property('srgb',True);t.set_editor_property('power_of_two_mode',unreal.TexturePowerOfTwoSetting.STRETCH_TO_POWER_OF_TWO);t.set_editor_property('max_texture_size',2048);paths.append(path);return t
textures={n:texture(n) for n in ['Meadow','Earth','Wood']};ground=[];graphrows=[]
for family in ['HealingMeadow','HealingPath','HealingForecourt','LegacyApproach']:
 src='/Game/Environment/VisualV2HealingArtV3/Materials/M_HA3_'+family;m=clone(src,D+'/Materials/M_HA4_'+family)
 for n in L.get_material_expressions(m):
  if isinstance(n,unreal.MaterialExpressionTextureObjectParameter):
   key=str(n.get_editor_property('parameter_name'))
   if key in ['NewGrass','NewEarth']:n.set_editor_property('texture',textures['Meadow' if key=='NewGrass' else 'Earth'])
  if not isinstance(n,unreal.MaterialExpressionCustom):continue
  code=n.get_editor_property('code');before=code
  if n.get_editor_property('output_type')==unreal.CustomMaterialOutputType.CMOT_FLOAT3:
   # Preserve every old sample/colour outside the local art mask. Larger readable art locally.
   for axis in ['a','b','c']:
    code=code.replace('Texture2DSample(NewGrass,NewGrassSampler,'+axis+')','Texture2DSample(NewGrass,NewGrassSampler,painted/255.0+float2(.13,.27))')
   # New layers now use the same readable motif, rather than averaging away individual blades.
   code=code.replace('Texture2DSample(NewEarth,NewEarthSampler,painted/220.0+float2(.19,.43))','Texture2DSample(NewEarth,NewEarthSampler,painted/255.0+float2(.19,.43))')
   code=code.replace('Texture2DSample(NewEarth,NewEarthSampler,float2(painted.x*.6+painted.y*.8,-painted.x*.8+painted.y*.6)/337.0+float2(.73,.27))','Texture2DSample(NewEarth,NewEarthSampler,painted/255.0+float2(.19,.43))')
   code=code.replace('g*=1+.075*macro;','g*=1+.075*macro;g*=lerp(float3(1,1,1),float3(1.08,1.08,1.02),localPaint);')
   code=code.replace('edgeVegetation*fleck*.30','edgeVegetation*fleck*.53')
  else:
   if 'float edge=abs(UV.y*2-1)+irregular;' in code:code=code.replace('float edge=abs(UV.y*2-1)+irregular;','irregular+=art*(.045*sin(p.x*.061+sin(p.y*.047))+.026*cos(p.y*.087-p.x*.035));float edge=abs(UV.y*2-1)+irregular;')
   if 'float e=art*' in code:code=code.replace('float e=art*','float e=art*(.045*sin(p.x*.061+sin(p.y*.047))+.026*cos(p.y*.087-p.x*.035))+art*')
   if 'float2 a=float2(-4050,460)' in code:code=code.replace('float2 a=float2(-4050,460)','r+=.025*sin(P.x*.061+sin(P.y*.047))+.018*cos(P.y*.087-P.x*.035);float2 a=float2(-4050,460)')
  n.set_editor_property('code',code);graphrows.append({'family':family,'before':before,'after':code})
 L.recompile_material(m);ground.append({'old':unreal.load_asset(src).get_path_name(),'new':m.get_path_name()})
# Private copies retain the existing cutaway graph, fixed linear vertex colour and pot surface.
materials={}
for key in ['Pot','Foliage','Soil','Blossom']:
 m=clone('/Game/Environment/VisualV2HealingArtV3/Materials/M_HA3_'+key,D+'/Materials/M_HA4_'+key)
 m.set_editor_property('used_with_instanced_static_meshes',True);L.recompile_material(m);materials[key]=m
# Exterior-only material bindings. Original graphs and their opacity/cutaway behavior preserved.
facade=[]
for key in ['Wood','Timber','Stone','Plaster','Roof']:
 src='/Game/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_Fade_'+key;m=clone(src,D+'/Materials/M_HA4_Facade'+key)
 expr=L.get_material_expressions(m);oldsample=next(n for n in expr if isinstance(n,unreal.MaterialExpressionTextureSample));tex=textures['Wood'] if key in ['Wood','Timber'] else oldsample.get_editor_property('texture')
 t=node(m,unreal.MaterialExpressionTextureObjectParameter,-800,0);t.set_editor_property('parameter_name','ArtSurface');t.set_editor_property('texture',tex)
 uv=node(m,unreal.MaterialExpressionTextureCoordinate,-800,200)
 code={
 'Wood':'float2 uv=UV*float2(1.8,.55);float3 c=Texture2DSample(Tex,TexSampler,uv).rgb;float grain=sin(UV.y*37+sin(UV.x*11));return c*float3(.94,.84,.71)*(1+.035*grain);',
 'Timber':'float2 uv=UV*float2(2.3,.70);float3 c=Texture2DSample(Tex,TexSampler,uv).rgb;return c*float3(.46,.38,.29);',
 'Stone':'float2 uv=UV*.82;float3 c=Texture2DSample(Tex,TexSampler,uv).rgb;float mott=.5+.25*sin(UV.x*19+cos(UV.y*17))+.25*cos(UV.y*23-UV.x*7);return c*lerp(float3(.70,.70,.64),float3(.95,.88,.74),mott);',
 'Plaster':'float2 uv=UV*.55;float3 c=Texture2DSample(Tex,TexSampler,uv).rgb;float broad=sin(UV.x*4.1+sin(UV.y*3.3))*cos(UV.y*5.4);float fine=sin(UV.x*177+sin(UV.y*149))*sin(UV.y*183);return c*float3(1.02,.98,.86)*(1+.055*broad+.022*fine);',
 'Roof':'float2 uv=UV;float3 c=Texture2DSample(Tex,TexSampler,uv*.52).rgb;float2 tile=uv*float2(3.2,3.0);float row=floor(tile.y);tile.x+=fmod(row,2)*.5;float2 f=frac(tile);float seam=1-smoothstep(.018,.045,min(f.x,1-f.x));float lip=1-smoothstep(.016,.044,f.y);float hash=frac(sin(dot(floor(tile),float2(12.9898,78.233)))*43758.5453);float var=.86+.22*hash;float moss=smoothstep(.82,.99,hash)*(1-smoothstep(.08,.28,f.y))*.30;return lerp(c*float3(.76,.73,.63)*var*(1-.30*seam-.25*lip),float3(.065,.095,.026),moss);'
 }[key]
 c=custom(m,code,{'Tex':(t,''),'UV':(uv,'')});assert L.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR)
 scalar(m,.88 if key!='Stone' else .93,unreal.MaterialProperty.MP_ROUGHNESS)
 # Gentle bump response from the actual existing/new painted surface, no baked illumination.
 normalcode='float2 uv=UV*float2('+('1.8,.55' if key in ['Wood','Timber'] else '.55,.55' if key=='Plaster' else '.82,.82' if key=='Stone' else '.52,.52')+');float2 d=float2(.001,0);float h=dot(Texture2DSample(Tex,TexSampler,uv).rgb,float3(.299,.587,.114));float hx=dot(Texture2DSample(Tex,TexSampler,uv+d).rgb,float3(.299,.587,.114));float hy=dot(Texture2DSample(Tex,TexSampler,uv+d.yx).rgb,float3(.299,.587,.114));return normalize(float3((h-hx)*'+('2.0' if key=='Plaster' else '4.0')+',(h-hy)*4.0,1));'
 n=custom(m,normalcode,{'Tex':(t,''),'UV':(uv,'')});assert L.connect_material_property(n,'',unreal.MaterialProperty.MP_NORMAL)
 m.set_editor_property('used_with_instanced_static_meshes',True);L.delete_unused_expressions(m);assert any(isinstance(n,unreal.MaterialExpressionScalarParameter) and str(n.get_editor_property('parameter_name'))=='HouseCutaway' for n in L.get_material_expressions(m));L.recompile_material(m);facade.append({'key':key,'old':unreal.load_asset(src).get_path_name(),'new':m.get_path_name()});materials[key]=m
# Static meshes with no gameplay collision. Bind only private/new or existing approved art surfaces.
SM=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);meshes=[];catalog={**json.loads((A/'Plants.json').read_text()),**json.loads((A/'Details.json').read_text())}
for family,info in catalog.items():
 name='SM_HA4_'+family;path=D+'/Meshes/'+name
 if not unreal.EditorAssetLibrary.does_asset_exist(path):
  ui=unreal.FbxImportUI();ui.import_mesh=True;ui.import_materials=False;ui.import_textures=False;ui.import_as_skeletal=False;ui.automated_import_should_detect_type=False;ui.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
  for key,value in {'combine_meshes':True,'auto_generate_collision':False,'convert_scene':True,'convert_scene_unit':True,'transform_vertex_to_absolute':True,'import_uniform_scale':1}.items():ui.static_mesh_import_data.set_editor_property(key,value)
  ui.static_mesh_import_data.set_editor_property('vertex_color_import_option',unreal.VertexColorImportOption.REPLACE)
  task=unreal.AssetImportTask();task.filename=str(A/'Exports'/(name+'.fbx'));task.destination_path=D+'/Meshes';task.destination_name=name;task.options=ui;task.automated=True;task.save=False;AT.import_asset_tasks([task])
 mesh=unreal.load_asset(path);assert mesh
 for i,slot in enumerate(mesh.get_editor_property('static_materials')):
  key=str(slot.get_editor_property('imported_material_slot_name')).split('_')[-1];assert key in materials,key;mesh.set_material(i,materials[key])
 assert SM.get_simple_collision_count(mesh)==0;paths.append(path);meshes.append({'family':family,'path':mesh.get_path_name(),'triangles':info['triangles'],'slots':len(mesh.get_editor_property('static_materials'))})
for p in paths:assert unreal.EditorAssetLibrary.save_asset(p,False)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
record={'assets':paths,'ground':ground,'facade':facade,'meshes':meshes};(S/'Prepared.json').write_text(json.dumps(record,indent=2));(A/'AssetManifest.json').write_text(json.dumps(record,indent=2));(A/'GroundChanges.json').write_text(json.dumps(graphrows,indent=2));unreal.log('HA4_PRIVATE_ASSETS_PREPARED')
