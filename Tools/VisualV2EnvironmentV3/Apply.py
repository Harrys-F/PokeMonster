"""Map-local authored environment pass. No shared source asset, collision or gameplay edits."""
import unreal,json,math,random,sys,copy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();A=R/'Art/World/VisualV2EnvironmentV3';D=R/'Saved/ProjectRefinement/EnvironmentV3';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();L=unreal.MaterialEditingLibrary;AT=unreal.AssetToolsHelpers.get_asset_tools();AS=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);SUB=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);ROOT='/Game/Environment/VisualV2EnvironmentV3';assert W.get_name()=='Dev_TestMap_VisualV2' and not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not (A/'Scope.json').exists()
actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)};assets=[];bindings=[];groups=[];lights=[]
def expression(m,code,inputs,kind=unreal.CustomMaterialOutputType.CMOT_FLOAT3):
 n=L.create_material_expression(m,unreal.MaterialExpressionCustom);arr=[]
 for name in inputs:i=unreal.CustomInput();i.set_editor_property('input_name',name);arr.append(i)
 n.set_editor_property('inputs',arr);n.set_editor_property('code',code);n.set_editor_property('output_type',kind)
 for k,(obj,out) in inputs.items():assert L.connect_material_expressions(obj,out,n,k)
 return n
def constant(m,v,prop):
 n=L.create_material_expression(m,unreal.MaterialExpressionConstant);n.set_editor_property('r',v);assert L.connect_material_property(n,'',prop)
def finish(m):
 if isinstance(m,unreal.Material):m.set_editor_property('used_with_instanced_static_meshes',True);L.recompile_material(m)
 assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
def clone(src,name):
 dst=ROOT+'/Materials/'+name;assert not unreal.EditorAssetLibrary.does_asset_exist(dst);m=unreal.EditorAssetLibrary.duplicate_asset(src,dst);assert m;assets.append(dst);return m
def bind(c,slot,m):
 old=c.get_material(slot);bindings.append({'actor':c.get_owner().get_name(),'component':c.get_name(),'slot':slot,'before':old.get_path_name(),'after':m.get_path_name()});c.set_material(slot,m)
# Existing route SDF, edge masks, texture bindings and reveal code remain intact.
for key in ['Ground','MainPath','NorthPath']:
 src='/Game/Environment/HealingHouse/ArtV5/Materials/M_HH5_Landscape'+key;m=clone(src,'M_EQ3_'+key)
 for n in L.get_material_expressions(m):
  if not isinstance(n,unreal.MaterialExpressionCustom):continue
  code=n.get_editor_property('code')
  if 'float3 waMeadow='not in code:continue
  code=code.replace('/296.0','/485.0').replace('/391.0','/643.0').replace('/238.0','/335.0').replace('/379.0','/527.0')
  needle='g=lerp(g,v6PathColor,v6Scope*v6Coverage);';assert needle in code
  patch='''
// EQ3: low-frequency meadow/forest variation. No change to path coverage.
float eqMacro=v5.n(p/465+float2(39,17));float eqFine=v5.n(p/113+float2(3,71));
float eqMeadow=(1-v6F)*(1-v6BankMask);float3 eqTint=lerp(float3(.86,.97,.77),float3(1.025,1.035,.88),eqMacro);
g=lerp(g,g*eqTint,eqMeadow*.7);g*=.94+.10*eqFine;
'''
  code=code.replace(needle,patch+needle);n.set_editor_property('code',code)
 # Low-amplitude broad relief; no displacement or collision changes.
 p=L.create_material_expression(m,unreal.MaterialExpressionWorldPosition)
 normal=expression(m,'float2 q=P.xy;float dx=.055*cos(q.x*.13+sin(q.y*.047))+.025*cos(q.x*.43+q.y*.18);float dy=.045*sin(q.y*.16+q.x*.04);return normalize(float3(dx,dy,1));',{'P':(p,'')});assert L.connect_material_property(normal,'',unreal.MaterialProperty.MP_NORMAL);finish(m)
 for a in actors.values():
  for c in a.get_components_by_class(unreal.StaticMeshComponent):
   for i in range(c.get_num_materials()):
    old=c.get_material(i)
    if old and old.get_path_name().split('.')[0]==src:bind(c,i,m)
# Stream shape/shore alpha unchanged; lit moving normals replace painted-only glints.
src='/Game/Environment/VisualV2HealingArtV4/Materials/M_HH_StreamSurface';m=clone(src,'M_EQ3_Stream')
for n in L.get_material_expressions(m):
 if isinstance(n,unreal.MaterialExpressionCustom):
  code=n.get_editor_property('code');code=code.replace('return float4(col,wet);','col=lerp(col,col*float3(.88,1.04,.95),deep*.5);\nreturn float4(col,wet);');n.set_editor_property('code',code)
p=L.create_material_expression(m,unreal.MaterialExpressionWorldPosition);t=L.create_material_expression(m,unreal.MaterialExpressionTime)
n=expression(m,'float2 q=P.xy;float a=q.y*.065+sin(q.x*.018-T*.18)*1.7-T*.52;float b=q.y*.13+q.x*.022+T*.31;return normalize(float3(.065*cos(a)+.024*sin(b),.10*sin(a)+.032*cos(b),1));',{'P':(p,''),'T':(t,'')});L.connect_material_property(n,'',unreal.MaterialProperty.MP_NORMAL);constant(m,.28,unreal.MaterialProperty.MP_ROUGHNESS);constant(m,.32,unreal.MaterialProperty.MP_SPECULAR);finish(m)
for a in actors.values():
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  for i in range(c.get_num_materials()):
   old=c.get_material(i)
   if old and old.get_path_name().split('.')[0]==src:bind(c,i,m)
# Exterior wood/stone/roof only: duplicate cutaway-compatible parents, preserve original meshes.
for family in ['Wood','Timber','Roof','Stone','Plaster']:
 src='/Game/Environment/VisualV2HealingArtV4/Materials/M_HH_Refined'+family;m=clone(src,'M_EQ3_House'+family)
 for n in L.get_material_expressions(m):
  if not isinstance(n,unreal.MaterialExpressionCustom):continue
  code=n.get_editor_property('code')
  if 'return c' in code:
   code=code.replace('return c','float weather=.5+.26*sin(UV.x*9.7+sin(UV.y*6.3))+.18*cos(UV.y*13.1-UV.x*3.9);c*=lerp(float3(.87,.91,.86),float3(1.07,1.04,.98),saturate(weather));return c');n.set_editor_property('code',code)
 finish(m)
 for a in actors.values():
  if not a.get_actor_label().startswith('V2_House_') or a.get_actor_bounds(False)[0].x>6000:continue
  for c in a.get_components_by_class(unreal.StaticMeshComponent):
   for i in range(c.get_num_materials()):
    old=c.get_material(i)
    if old and old.get_path_name().split('.')[0]==src:bind(c,i,m)
# Import three small opaque blade meshes, retaining metre-to-centimetre conversion.
mat=AT.create_asset('M_EQ3_Grass',ROOT+'/Materials',unreal.Material,unreal.MaterialFactoryNew());assert mat;assets.append(mat.get_path_name().split('.')[0]);mat.set_editor_property('two_sided',True)
vc=L.create_material_expression(mat,unreal.MaterialExpressionVertexColor);p=L.create_material_expression(mat,unreal.MaterialExpressionWorldPosition)
n=expression(mat,'float patch=.5+.25*sin(P.x*.006+sin(P.y*.009))+.25*cos(P.y*.005-P.x*.002);return C.rgb*lerp(float3(.75,.90,.73),float3(1.10,1.08,.91),patch);',{'C':(vc,''),'P':(p,'')});L.connect_material_property(n,'',unreal.MaterialProperty.MP_BASE_COLOR);constant(mat,.91,unreal.MaterialProperty.MP_ROUGHNESS);constant(mat,.20,unreal.MaterialProperty.MP_SPECULAR)
# Only tips move, by less than 1 cm. Opaque leaves avoid alpha overdraw / temporal dither.
uv=L.create_material_expression(mat,unreal.MaterialExpressionTextureCoordinate);t=L.create_material_expression(mat,unreal.MaterialExpressionTime)
n=expression(mat,'float w=UV.y*UV.y;return float3(sin(T*1.15+P.x*.017+P.y*.008)*.65*w,cos(T*.87+P.y*.015)*.40*w,0);',{'UV':(uv,''),'T':(t,''),'P':(p,'')});L.connect_material_property(n,'',unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET);finish(mat)
meshes={}
for key in ['Short','Meadow','Woodland']:
 name='SM_EQ3_Grass'+key;task=unreal.AssetImportTask();task.filename=str(A/'Exports'/(name+'.fbx'));task.destination_path=ROOT+'/Meshes';task.destination_name=name;task.automated=True;task.save=False;task.replace_existing=False;ui=unreal.FbxImportUI();ui.import_mesh=True;ui.import_materials=False;ui.import_textures=False;ui.import_animations=False;ui.import_as_skeletal=False;ui.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
 for k,v in {'combine_meshes':True,'auto_generate_collision':False,'convert_scene':True,'convert_scene_unit':True,'transform_vertex_to_absolute':True,'vertex_color_import_option':unreal.VertexColorImportOption.REPLACE,'normal_import_method':unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS}.items():ui.static_mesh_import_data.set_editor_property(k,v)
 task.options=ui;AT.import_asset_tasks([task]);mesh=unreal.load_asset(ROOT+'/Meshes/'+name);assert isinstance(mesh,unreal.StaticMesh);mesh.set_material(0,mat);assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,False);assets.append(mesh.get_path_name().split('.')[0]);meshes[key]=mesh
# Existing analytic path and water fields govern every added detail.
routes=json.loads((R/'Art/World/VisualV2WorldArtV7/RouteField.json').read_text())['segments']
def seg(x,y,a,b):
 dx=b[0]-a[0];dy=b[1]-a[1];u=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)));return math.hypot(x-a[0]-dx*u,y-a[1]-dy*u)
def road(x,y):return min(seg(x,y,r['a'],r['b'])-r['base_half_width_cm']for r in routes)
def water(x,y):return min(seg(x,y,[-910,-320],[1100,-320])-66,seg(x,y,[720,-320],[720,-680])-64,(math.hypot((x-720)/264,(y+720)/190)-1)*185)
protected=[a.get_actor_location() for a in actors.values()if 'PokeMonster'in a.get_class().get_name()and abs(a.get_actor_location().x)<6000]
def safe(x,y,clear=80):
 if not -5500<x<2400 or not -2850<y<2800:return False
 if road(x,y)<clear or water(x,y)<55:return False
 if -4660<x<-3370 and -130<y<1680:return False
 if -2400<x<-1150 and -2820<y<-1920:return False
 if any(math.hypot(x-q.x,y-q.y)<185 for q in protected):return False
 return True
def group(label,mesh,points,materials=None):
 a=AS.spawn_actor_from_class(unreal.Actor,unreal.Vector());a.set_actor_label('EQ3_'+label);a.set_folder_path('VisualV2/EnvironmentV3');a.tags=['EnvironmentV3','VisualOnly_NoCollision'];root=SUB.k2_gather_subobject_data_for_instance(a)[0];handle,reason=SUB.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle));assert c,reason;c.set_static_mesh(mesh)
 if materials:
  for i,m in enumerate(materials):c.set_material(i,m)
 c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False);c.set_editor_property('affect_distance_field_lighting',False);c.set_editor_property('affect_dynamic_indirect_lighting',False);c.set_cull_distances(5000,7000)
 for x,y,z,s,yaw in points:c.add_instance(unreal.Transform(location=unreal.Vector(x,y,z),rotation=unreal.Rotator(yaw=yaw),scale=unreal.Vector(*s)),True)
 groups.append({'actor':a.get_name(),'label':a.get_actor_label(),'mesh':mesh.get_path_name(),'count':len(points),'instances':points})
rng=random.Random(251026);centers=[]
for k in range(165):
 for attempt in range(100):
  x=rng.uniform(-5000,2000);y=rng.uniform(-2600,2600)
  if safe(x,y,110):centers.append((x,y,rng.uniform(75,245),rng.uniform(55,160)));break
pts={k:[]for k in meshes};occupied=[]
for cx,cy,sx,sy in centers:
 for k in range(rng.randint(14,38)):
  x=rng.gauss(cx,sx);y=rng.gauss(cy,sy)
  if not safe(x,y,65) or any(math.hypot(x-u,y-v)<24 for u,v in occupied[-220:]):continue
  kind=rng.choices(['Short','Meadow','Woodland'],weights=[.47,.40,.13]if y<900 else[.52,.18,.30])[0];sc=rng.uniform(.70,1.13);pts[kind].append((x,y,-.4,[sc*rng.uniform(.8,1.15),sc,sc*rng.uniform(.83,1.08)],rng.uniform(0,360)));occupied.append((x,y))
for kind,points in pts.items():group('Grass'+kind,meshes[kind],points)
# Small forest/shore pockets of existing ferns, moss, roots and pebbles, not continuous ribbons.
for family,source,count,base in [('Ferns','ArtV4_Edge_Ferns',70,.65),('Flowers','WA7_Suedwiese_Flowers',55,.85),('Roots','ArtV4_Edge_Roots',25,.48),('Moss','Refined_River_Moss',70,.65),('Pebbles','Refined_River_Pebbles',85,.60)]:
 if source not in actors:continue
 ref=actors[source].get_component_by_class(unreal.StaticMeshComponent);points=[]
 for attempt in range(15000):
  if len(points)==count:break
  if family in ['Moss','Pebbles']:
   x=rng.uniform(-880,1050);y=-320+rng.choice([-1,1])*rng.uniform(95,200)
  else:cx,cy,sx,sy=rng.choice(centers);x=rng.gauss(cx,sx*.6);y=rng.gauss(cy,sy*.6)
  if not safe(x,y,90) or(family in ['Ferns','Roots']and y<700):continue
  sc=base*rng.uniform(.6,1.2);points.append((x,y,-.2,[sc,sc,sc*(.45 if family=='Pebbles' else 1)],rng.uniform(0,360)))
 assert len(points)==count,(family,len(points));group(family,ref.static_mesh,points,[ref.get_material(i)for i in range(ref.get_num_materials())])
# A small, reversible existing non-shadow-casting fill adjustment; shadow casters unchanged.
fill=actors['VS_SoftSkyFill'].get_component_by_class(unreal.DirectionalLightComponent);lights.append({'actor':actors['VS_SoftSkyFill'].get_name(),'field':'intensity','before':fill.intensity,'after':1.12});fill.set_intensity(1.12)
result={'assets':assets,'bindings':bindings,'groups':groups,'light_changes':lights,'new_instances':sum(g['count']for g in groups),'no_actor_removed':True,'collision_and_camera_unchanged':True};(A/'Scope.json').write_text(json.dumps(result,indent=2));(D/'Applied.json').write_text(json.dumps(result,indent=2));assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2');assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();unreal.log('ENV3_APPLIED '+str(result['new_instances']))
