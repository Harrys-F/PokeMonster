"""Bounded, reproducible art pass on existing VisualV2; old sources and gameplay retained."""
import unreal,json,math,random,sys,copy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ProjectRefinement';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();L=unreal.MaterialEditingLibrary;AT=unreal.AssetToolsHelpers.get_asset_tools()
assert w.get_path_name()=='/Game/Maps/Dev_TestMap_VisualV2.Dev_TestMap_VisualV2' and not E.get_game_world()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert not (S/'ArtApplied.json').exists()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
before=scene(w);actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};assert not any(k.startswith('Refined_') for k in actors)
D='/Game/Environment/VisualV2HealingArtV4';assets=[];changes=[];graphs=[];bindings=[]
def node(m,t):return L.create_material_expression(m,t)
def clone(src,dst):
 assert not unreal.EditorAssetLibrary.does_asset_exist(dst),dst
 m=unreal.EditorAssetLibrary.duplicate_asset(src,dst);assert m;assets.append(m);return m
def custom(m,code,inputs,typ=unreal.CustomMaterialOutputType.CMOT_FLOAT3):
 n=node(m,unreal.MaterialExpressionCustom);n.set_editor_property('output_type',typ);arr=[]
 for key in inputs:i=unreal.CustomInput();i.set_editor_property('input_name',key);arr.append(i)
 n.set_editor_property('inputs',arr);n.set_editor_property('code',code)
 for key,(a,pin) in inputs.items():assert L.connect_material_expressions(a,pin,n,key)
 return n
def scalar(m,v,p):
 n=node(m,unreal.MaterialExpressionConstant);n.set_editor_property('r',v);assert L.connect_material_property(n,'',p)
def finish(m):
 m.set_editor_property('used_with_instanced_static_meshes',True);L.recompile_material(m)
def override(c,i,m):
 old=c.get_material(i);c.set_material(i,m);bindings.append({'actor':c.get_owner().get_name(),'component':c.get_name(),'slot':i,'before':old.get_path_name() if old else None,'after':m.get_path_name()})
# Reuse painted textures and existing field masks. Keep route geometry and alpha unchanged.
for key in ['Ground','NorthPath','MainPath']:
 src='/Game/Environment/VisualV2WorldArtV7/Materials/M_WA7_'+key;m=clone(src,D+'/Materials/M_HH_Landscape'+key)
 for n in L.get_material_expressions(m):
  if not isinstance(n,unreal.MaterialExpressionCustom) or n.get_editor_property('output_type')!=unreal.CustomMaterialOutputType.CMOT_FLOAT3:continue
  old=n.get_editor_property('code');code=old
  code=code.replace('(p+v6Warp)/169.0','(p+v6Warp)/238.0').replace('(waTurn+float2(17*sin(p.x*.013),14*cos(p.y*.017)))/281.0','(waTurn+float2(17*sin(p.x*.013),14*cos(p.y*.017)))/379.0')
  code=code.replace('(p+v6Warp*.85)/240.0','(p+v6Warp*.85)/296.0')
  needle='v6PathColor*=1+.045*v6Noise+.035*v6FootWear;';assert needle in code
  code=code.replace(needle,needle+'''
float artMottle=.5+.25*sin(p.x*.009+sin(p.y*.007))+.20*cos(p.y*.013-p.x*.004);
float tread=exp(-pow((v6Dist-v6Half*.43)/24.0,2));
v6PathColor=lerp(v6PathColor,v6PathColor*float3(.86,.95,1.04),.23+.26*artMottle);
v6PathColor*=1-.045*tread+.045*(artMottle-.5);
''')
  n.set_editor_property('code',code);graphs.append({'material':m.get_path_name(),'expression':n.get_name(),'before':old,'after':code})
 finish(m)
 for lab,a in actors.items():
  if lab in ['V2_Ground','V2_Path_Main','V2_Path_NorthLoop','V2_Path_VillageLoop','V2_Path_Wild','V2_Path_Cottage']:
   c=a.static_mesh_component
   if c.get_material(0).get_path_name().startswith(src+'.'):override(c,0,m)
# Subtle stream bands, shallow stones visible as a painted bed, original shoreline alpha retained.
m=clone('/Game/Environment/Prototype2D/Materials/M_OrganicWater',D+'/Materials/M_HH_StreamSurface')
for n in L.get_material_expressions(m):
 if not isinstance(n,unreal.MaterialExpressionCustom):continue
 old=n.get_editor_property('code');assert 'return float4(col,wet);' in old
 code=old.replace('return float4(col,wet);','''
float flow=sin(P.y*.075+sin(P.x*.018-T*.12)*1.8-T*.42);
float glint=pow(saturate(flow),14)*(.4+.6*small);
col+=float3(.018,.031,.029)*glint*deep;
float bed=f.noise(P.xy*.045)*f.noise(P.xy*.075+7);
col=lerp(col,col*lerp(float3(.77,.81,.64),float3(1.14,1.12,.96),bed),.30*(1-deep));
return float4(col,wet);''');n.set_editor_property('code',code);graphs.append({'material':m.get_path_name(),'expression':n.get_name(),'before':old,'after':code})
finish(m);override(actors['P2D_OrganicWater'].static_mesh_component,0,m)
# Exterior surfaces remain attached to their original cutaway graphs.
facade={}
for key in ['Wood','Timber','Stone','Plaster','Roof']:
 src=D+'/Materials/M_HA4_Facade'+key;m=clone(src,D+'/Materials/M_HH_Refined'+key)
 for n in L.get_material_expressions(m):
  if not isinstance(n,unreal.MaterialExpressionCustom) or n.get_editor_property('output_type')!=unreal.CustomMaterialOutputType.CMOT_FLOAT3:continue
  old=n.get_editor_property('code');code=old
  if key=='Roof':code=code.replace('float var=.86+.22*hash;','float var=.80+.28*hash;').replace('*.30;return','*.43;return').replace('1-.30*seam-.25*lip','1-.22*seam-.19*lip')
  elif key=='Wood':code=code.replace('float3(.94,.84,.71)','float3(.90,.79,.65)').replace('.035*grain','.055*grain')
  elif key=='Timber':code=code.replace('float3(.46,.38,.29)','float3(.52,.41,.30)')
  elif key=='Stone':code=code.replace('float3(.70,.70,.64)','float3(.66,.69,.65)')
  elif key=='Plaster':code=code.replace('.055*broad+.022*fine','.075*broad+.025*fine')
  if old!=code:n.set_editor_property('code',code);graphs.append({'material':m.get_path_name(),'expression':n.get_name(),'before':old,'after':code})
 finish(m);facade[key]=m
 for a in actors.values():
  if not a.get_actor_label().startswith('V2_House_') or a.get_actor_location().x>0:continue
  for c in a.get_components_by_class(unreal.StaticMeshComponent):
   for i in range(c.get_num_materials()):
    old=c.get_material(i)
    if old and old.get_path_name().startswith(src+'.'):override(c,i,m)
# Continuous, staggered floorboards use world coordinates across all existing floor modules.
wood=unreal.load_asset(D+'/Textures/T_HA4_Wood');src='/Game/Environment/HealingHouse/QualityV2/Materials/M_HH_Q2_Wood';floor=clone(src,D+'/Materials/M_HH_InteriorFloor')
p=node(floor,unreal.MaterialExpressionWorldPosition);t=node(floor,unreal.MaterialExpressionTextureObjectParameter);t.set_editor_property('parameter_name','PaintedOak');t.set_editor_property('texture',wood)
code='''float2 q=P.xy-float2(16400,-100);float row=floor(q.y/21);float shift=frac(sin(row*17.13)*427.31)*113;float2 cell=float2((q.x+shift)/127,q.y/21);float2 f=frac(cell);float h=frac(sin(dot(floor(cell),float2(31.17,57.3)))*14573.3);float edge=min(min(f.x,1-f.x)*127,min(f.y,1-f.y)*21);float seam=smoothstep(.10,.45,edge);float3 c=Texture2DSample(Tex,TexSampler,float2(q.x/162,q.y/46)).rgb;float grain=sin(q.y*2.4+sin(q.x*.043)*.75);return c*float3(.77,.70,.58)*(.92+.16*h)*(1+.025*grain)*lerp(.60,1,seam);'''
c=custom(floor,code,{'P':(p,''),'Tex':(t,'')});assert L.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR);scalar(floor,.83,unreal.MaterialProperty.MP_ROUGHNESS);finish(floor)
interior={}
for key,col in [('Wood',(.82,.76,.66)),('Timber',(.58,.48,.36)),('Linen',(.67,.59,.42)),('Sage',(.105,.19,.13)),('Plaster',(.59,.51,.36))]:
 source='/Game/Environment/HealingHouse/QualityV2/Materials/M_HH_Q2_'+key
 assert unreal.load_asset(source),source
 m=clone(source,D+'/Materials/M_HH_Interior'+key);uv=node(m,unreal.MaterialExpressionTextureCoordinate)
 if key in ['Wood','Timber']:
  tx=node(m,unreal.MaterialExpressionTextureObjectParameter);tx.set_editor_property('parameter_name','PaintedOak');tx.set_editor_property('texture',wood)
  code='float3 c=Texture2DSample(Tex,TexSampler,UV*float2(1.3,.72)).rgb;return c*float3('+','.join(map(str,col))+')*(1+.025*sin(UV.y*78+sin(UV.x*19)));'
  c=custom(m,code,{'UV':(uv,''),'Tex':(tx,'')})
 else:
  code='float weave=.5+.5*sin(UV.x*276)*sin(UV.y*251);float broad=sin(UV.x*8.3+sin(UV.y*6))*cos(UV.y*9.1);return float3('+','.join(map(str,col))+')*(1+.04*broad+.025*(weave-.5));'
  c=custom(m,code,{'UV':(uv,'')})
 assert L.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR);scalar(m,.93 if key in ['Linen','Sage'] else .86,unreal.MaterialProperty.MP_ROUGHNESS);finish(m);interior[key]=m
for a in actors.values():
 if not 16000<a.get_actor_location().x<18000:continue
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  for i in range(c.get_num_materials()):
   old=c.get_material(i)
   if not old:continue
   name=old.get_name();m=None
   if a.get_actor_label().startswith('V2_House_HH_Art_Floor_'):m=floor
   elif name.startswith('M_HH_Q2_'):
    key=name[len('M_HH_Q2_'):];m=interior.get(key)
    if key in ['WoodLight','WoodDark']:m=interior['Wood']
   if m:override(c,i,m)
# New, small Blender details use one opaque vertex-colour material; no glass overdraw.
mat=AT.create_asset('M_HH_HandcraftedSurface',D+'/Materials',unreal.Material,unreal.MaterialFactoryNew());assert mat;assets.append(mat)
v=node(mat,unreal.MaterialExpressionVertexColor);uv=node(mat,unreal.MaterialExpressionTextureCoordinate)
c=custom(mat,'float3 a=lerp(C/12.92,pow(max((C+.055)/1.055,0),2.4),step(.04045,C));return a*(.98+.02*sin(UV.x*61)*sin(UV.y*77));',{'C':(v,''),'UV':(uv,'')});assert L.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR);scalar(mat,.71,unreal.MaterialProperty.MP_ROUGHNESS);finish(mat);mat.set_editor_property('two_sided',True)
meshes={};SM=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
for key in ['HerbalRemedyTray','HerbalMortar','PorchCorbel']:
 name='SM_HH_'+key;path=D+'/Meshes/'+name;assert not unreal.EditorAssetLibrary.does_asset_exist(path)
 ui=unreal.FbxImportUI();ui.import_mesh=True;ui.import_materials=False;ui.import_textures=False;ui.import_as_skeletal=False;ui.automated_import_should_detect_type=False;ui.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
 for k,val in {'combine_meshes':True,'auto_generate_collision':False,'convert_scene':True,'convert_scene_unit':True,'transform_vertex_to_absolute':True}.items():ui.static_mesh_import_data.set_editor_property(k,val)
 ui.static_mesh_import_data.set_editor_property('vertex_color_import_option',unreal.VertexColorImportOption.REPLACE)
 task=unreal.AssetImportTask();task.filename=str(R/'Art/HealingHouse/Exports'/(name+'.fbx'));task.destination_path=D+'/Meshes';task.destination_name=name;task.options=ui;task.automated=True;task.save=False;AT.import_asset_tasks([task]);mesh=unreal.load_asset(path);assert mesh;mesh.set_material(0,mat);assert SM.get_simple_collision_count(mesh)==0;assets.append(mesh);meshes[key]=mesh
AS=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);new=[]
def prop(key,pos,yaw=0,scale=1):
 a=AS.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*pos),unreal.Rotator(yaw=yaw));a.set_actor_label('Refined_'+key+'_'+str(len(new)));a.set_folder_path('VisualV2/HealingHouse/HandcraftedDetails');a.tags=['VisualOnly_NoCollision','ProjectRefinement'];a.static_mesh_component.set_static_mesh(meshes[key]);a.static_mesh_component.set_collision_profile_name('NoCollision');a.set_actor_scale3d(unreal.Vector(scale,scale,scale));new.append(a.get_name());return a
prop('HerbalRemedyTray',(17115,340,105),90,.74);prop('HerbalMortar',(17110,505,105),10,.8);prop('HerbalRemedyTray',(16568,900,84),0,.76);prop('HerbalMortar',(16670,215,77),-15,.67)
# Existing porch is retained. Curved braces sit below existing canopy, outside the doorway/collision.
prop('PorchCorbel',(-3578,373,192),0,.80);prop('PorchCorbel',(-3578,627,192),0,.80)
# Reuse authored V4 flowers and leaf forms indoors; no replacement of main furniture.
for pos,kind,sc in [((17315,700,0),'FlowerPlant',.88),((16550,350,0),'NarrowHerb',.93)]:
 a=AS.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*pos));a.set_actor_label('Refined_HealingHerbs_'+str(len(new)));a.set_folder_path('VisualV2/HealingHouse/HandcraftedDetails');a.tags=['VisualOnly_NoCollision','ProjectRefinement'];a.static_mesh_component.set_static_mesh(unreal.load_asset(D+'/Meshes/SM_HA4_'+kind));a.static_mesh_component.set_collision_profile_name('NoCollision');a.set_actor_scale3d(unreal.Vector(sc,sc,sc));new.append(a.get_name())
# Existing fill system retained; small lift opens foliage shadows without a shadow-replacement trick.
lightchanges=[]
for label,values in {'VS_SoftSkyFill':{'intensity':.65},'V2_House_HH_Art_Light_Waiting':{'intensity':5.2,'attenuation_radius':320},'V2_House_HH_Art_Light_Reception':{'intensity':6.4,'attenuation_radius':340},'V2_House_HH_Art_Light_Treatment':{'intensity':5.0,'attenuation_radius':340},'V2_House_HH_V3_CounterGlow':{'intensity':2.4,'attenuation_radius':490},'V2_House_HH_V3_RestAreaGlow':{'intensity':2.1,'attenuation_radius':420}}.items():
 a=actors[label];c=next(c for c in a.get_components_by_class(unreal.ActorComponent) if c.get_class().get_name() in ['DirectionalLightComponent','PointLightComponent']);row={'actor':a.get_name(),'label':label,'changes':{}}
 for k,val in values.items():row['changes'][k]={'before':float(c.get_editor_property(k)),'after':val};c.set_editor_property(k,val)
 lightchanges.append(row)
for a in actors.values():
 if a.get_actor_label().startswith('V2_House_HH_Q3_WindowLight_'):
  c=a.get_component_by_class(unreal.SpotLightComponent);lightchanges.append({'actor':a.get_name(),'label':a.get_actor_label(),'changes':{'intensity':{'before':float(c.intensity),'after':6.0}}});c.set_intensity(6)
# Save only explicitly owned art assets. Map saved after the scope audit below.
for m in assets:assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
if hasattr(unreal,'AssetCompilingManager'):unreal.AssetCompilingManager.finish_all_compilation()
after=scene(w);allowed={b['actor'] for b in bindings}|{r['actor'] for r in lightchanges}
assert set(before['actors'])<=set(after['actors']) and set(after['actors'])-set(before['actors'])==set(new)
assert before['world_settings']==after['world_settings']
for name,b in before['actors'].items():
 if name not in allowed:assert after['actors'][name]==b,('UNEXPECTED_EXISTING_ACTOR_CHANGE',name)
 else:
  a=after['actors'][name];assert a['transform']==b['transform'] and a['props']==b['props'],name
  for c0 in b['components']:
   c1=next(c for c in a['components'] if c['name']==c0['name']);assert c0.get('collision')==c1.get('collision') and c0.get('instances')==c1.get('instances') and c0['transform']==c1['transform'],name
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2')
record={'new_assets':[a.get_path_name() for a in assets],'material_bindings':bindings,'new_actors':new,'light_changes':lightchanges,'old_actor_transforms_collision_instances_gameplay_unchanged':True,'new_maps':0,'source':str(Path(__file__).relative_to(R))}
(S/'ArtApplied.json').write_text(json.dumps(record,indent=2));(S/'ArtAfterScene.json').write_text(json.dumps(after,indent=2));(R/'Art/HealingHouse/Refinement.json').write_text(json.dumps(record,indent=2));(R/'Art/HealingHouse/RefinedGraphs.json').write_text(json.dumps(graphs,indent=2));unreal.log('VISUALV2_ART_REFINEMENT_SAVED')
