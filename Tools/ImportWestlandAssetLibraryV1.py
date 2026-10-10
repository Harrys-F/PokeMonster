"""Scoped, additive library import and independent review map. Shared assets read only."""
import unreal,json,math,random
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();ART=ROOT/'Art/World/WestlandAssetLibrary';OUT=ROOT/'Saved/WestlandAssetLibrary';DEST='/Game/Environment/WestlandAssetLibrary';MAP='/Game/Maps/Dev_WestlandAssetLibrary'
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);assert not E.get_game_world()
full=(ART/'Assets.json').exists();data=json.loads((ART/('Assets.json' if full else 'Heroes.json')).read_text());assert (OUT/('FamilyReviewAccepted.json' if full else 'HeroReviewAccepted.json')).exists()
T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;paths=[]
if not unreal.EditorAssetLibrary.does_asset_exist(MAP):assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).new_level(MAP)
elif E.get_editor_world().get_name()!='Dev_WestlandAssetLibrary':assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level(MAP)
w=E.get_editor_world();assert w.get_name()=='Dev_WestlandAssetLibrary'
def load(p):
 a=unreal.load_asset(p);assert a,p;return a

def master(name,two):
 p=DEST+'/Materials/'+name
 if unreal.EditorAssetLibrary.does_asset_exist(p):return load(p)
 m=T.create_asset(name,DEST+'/Materials',unreal.Material,unreal.MaterialFactoryNew());m.set_editor_property('two_sided',two)
 tex=L.create_material_expression(m,unreal.MaterialExpressionTextureSampleParameter2D,-700,0);tex.set_editor_property('parameter_name','Paint');tex.set_editor_property('texture',load('/Game/Environment/HealingHouse/QualityV2/Textures/T_HH_PaintedWood'))
 tint=L.create_material_expression(m,unreal.MaterialExpressionVectorParameter,-700,200);tint.set_editor_property('parameter_name','Tint');tint.set_editor_property('default_value',unreal.LinearColor(1,1,1,1))
 mix=L.create_material_expression(m,unreal.MaterialExpressionMultiply,-400,0);assert L.connect_material_expressions(tex,'RGB',mix,'A');assert L.connect_material_expressions(tint,'RGB',mix,'B')
 vert=L.create_material_expression(m,unreal.MaterialExpressionVertexColor,-400,220);mx=L.create_material_expression(m,unreal.MaterialExpressionMultiply,-200,0);L.connect_material_expressions(mix,'',mx,'A');L.connect_material_expressions(vert,'RGB',mx,'B');L.connect_material_property(mx,'',unreal.MaterialProperty.MP_BASE_COLOR)
 for param,default,prop,y in [('Roughness',.87,unreal.MaterialProperty.MP_ROUGHNESS,350),('Metallic',0,unreal.MaterialProperty.MP_METALLIC,450),('Specular',.15,unreal.MaterialProperty.MP_SPECULAR,550)]:
  n=L.create_material_expression(m,unreal.MaterialExpressionScalarParameter,-200,y);n.set_editor_property('parameter_name',param);n.set_editor_property('default_value',default);L.connect_material_property(n,'',prop)
 L.recompile_material(m);paths.append(p);return m
opaque=master('M_WLA_Painted',False);leaf=master('M_WLA_PaintedLeaf',True);materials={};used=set(n.removeprefix('WLA_') for a in data['assets'] for n in a['materials']);textures={}
for key in sorted(used):
 spec=data['materials'][key];source=spec['texture'];tex=None
 if source:
  if source.startswith('Art/World/WestlandAssetLibrary'):
   n=Path(source).stem;p=DEST+'/Textures/'+n
   if not unreal.EditorAssetLibrary.does_asset_exist(p):
    task=unreal.AssetImportTask();task.filename=str(ROOT/source);task.destination_path=DEST+'/Textures';task.destination_name=n;task.automated=True;task.save=False;T.import_asset_tasks([task]);paths.append(p)
   tex=load(p);tex.set_editor_property('srgb',True);tex.set_editor_property('max_texture_size',1024);tex.set_editor_property('never_stream',False);unreal.EditorAssetLibrary.save_loaded_asset(tex,False)
  else:tex=load('/Game/Environment/HealingHouse/QualityV2/Textures/'+Path(source).stem)
 else:
  # A shared tiny white engine texture supplies quiet accent materials through the same master.
  tex=load('/Engine/EngineResources/WhiteSquareTexture')
 p=DEST+'/Materials/MI_WLA_'+key
 if not unreal.EditorAssetLibrary.does_asset_exist(p):
  mi=T.create_asset('MI_WLA_'+key,DEST+'/Materials',unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew());L.set_material_instance_parent(mi,leaf if spec['two_sided'] else opaque);L.set_material_instance_texture_parameter_value(mi,'Paint',tex);L.set_material_instance_vector_parameter_value(mi,'Tint',unreal.LinearColor(*spec['color'],1));L.set_material_instance_scalar_parameter_value(mi,'Metallic',.25 if key in ('Iron','Gold') else 0);L.update_material_instance(mi);paths.append(p)
 materials['WLA_'+key]=load(p);textures[key]=tex.get_path_name()
subset=json.loads((OUT/'ReimportOnly.json').read_text()) if (OUT/'ReimportOnly.json').exists() else None
unreal.SystemLibrary.execute_console_command(w,'Interchange.FeatureFlags.Import.FBX 0');tasks=[]
for a in data['assets']:
 p=DEST+'/Meshes/'+a['family']+'/'+a['object']
 if subset and a['id'] not in subset and unreal.EditorAssetLibrary.does_asset_exist(p):continue
 ui=unreal.FbxImportUI()
 for k,v in {'import_mesh':True,'import_materials':False,'import_textures':False,'import_as_skeletal':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_STATIC_MESH}.items():ui.set_editor_property(k,v)
 for k,v in {'combine_meshes':True,'auto_generate_collision':False,'one_convex_hull_per_ucx':True,'transform_vertex_to_absolute':True,'convert_scene':True,'convert_scene_unit':True,'import_uniform_scale':1,'vertex_color_import_option':unreal.VertexColorImportOption.REPLACE,'generate_lightmap_u_vs':True,'normal_import_method':unreal.FBXNormalImportMethod.FBXNIM_COMPUTE_NORMALS}.items():ui.static_mesh_import_data.set_editor_property(k,v)
 task=unreal.AssetImportTask()
 for k,v in {'filename':str(ART/'Exports'/(a['object']+'.fbx')),'destination_path':DEST+'/Meshes/'+a['family'],'destination_name':a['object'],'automated':True,'save':False,'replace_existing':True,'replace_existing_settings':True,'options':ui}.items():task.set_editor_property(k,v)
 tasks.append(task);paths.append(p)
if tasks:T.import_asset_tasks(tasks)
meshes={};audit=[];SM=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
for a in data['assets']:
 sm=load(DEST+'/Meshes/'+a['family']+'/'+a['object']);meshes[a['id']]=sm
 slots=list(sm.get_editor_property('static_materials'))
 for slot in slots:
  n=str(slot.get_editor_property('imported_material_slot_name')).split('.')[0];assert n in materials,(a['id'],n);slot.set_editor_property('material_interface',materials[n])
 if any(x.get_editor_property('material_interface')!=y.get_editor_property('material_interface') for x,y in zip(slots,sm.get_editor_property('static_materials'))):sm.set_editor_property('static_materials',slots)
 body=sm.get_editor_property('body_setup');count=SM.get_simple_collision_count(sm)+SM.get_convex_collision_count(sm);assert count==len(a['collision_objects']),(a['id'],count)
 # Explicit reduction for owned meshes only. Thin botanical silhouettes must be rechecked after reduction.
 if SM.get_lod_count(sm)==1 and a['triangles']>1000:
  opts=unreal.StaticMeshReductionOptions();settings=[]
  for pc,screen in [(1.,1.),(.55,.45),(.25,.16)]:
   x=unreal.StaticMeshReductionSettings();x.percent_triangles=pc;x.screen_size=screen;settings.append(x)
  opts.reduction_settings=settings;opts.auto_compute_lod_screen_size=False;SM.set_lods(sm,opts)
 # Imported UCX supplies simple collision; changing every section needlessly rebuilds meshes.
 for lod in range(SM.get_lod_count(sm)):
  settings=SM.get_lod_build_settings(sm,lod)
  if settings.distance_field_resolution_scale==0 and settings.recompute_normals and settings.recompute_tangents and not settings.use_mikk_t_space:continue
  settings.set_editor_property('distance_field_resolution_scale',0);settings.set_editor_property('recompute_normals',True);settings.set_editor_property('recompute_tangents',True);settings.set_editor_property('use_mikk_t_space',False);SM.set_lod_build_settings(sm,lod,settings)
 bounds=sm.get_bounding_box();size=bounds.max-bounds.min;assert all(abs(v/100-t)<max(.02,t*.01) for v,t in zip((size.x,size.y,size.z),a['dimensions_m'])),(a['id'],size,a['dimensions_m'])
 assert all(sm.get_material(i) for i in range(SM.get_number_materials(sm)))
 assert unreal.EditorAssetLibrary.save_loaded_asset(sm,False)
 audit.append({'id':a['id'],'bounds_cm':[size.x,size.y,size.z],'triangles_blender':a['triangles'],'materials':SM.get_number_materials(sm),'lods':SM.get_lod_count(sm),'collision_bodies':count})

def world(e,n,z=0):return unreal.Vector((e+n)*math.sqrt(.5)*100,(e-n)*math.sqrt(.5)*100,z*100)
def actor(cls,name,e,n,z=0):
 old=next((a for a in A.get_all_level_actors() if a.get_actor_label()==name),None)
 if old:return old
 a=A.spawn_actor_from_class(cls,world(e,n,z),unreal.Rotator(yaw=-45));a.set_actor_label(name);a.set_folder_path('WestlandAssetLibrary');a.tags=['WLA_V1'];return a
floor=actor(unreal.StaticMeshActor,'WLA_Ground',0,4,-.12);floor.static_mesh_component.set_static_mesh(load('/Engine/BasicShapes/Cube'));floor.set_actor_scale3d(unreal.Vector(65,65,.24));floor.static_mesh_component.set_material(0,load('/Game/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_Grass'));floor.static_mesh_component.set_collision_profile_name('BlockAll');floor.static_mesh_component.set_cast_shadow(False)
start=actor(unreal.PlayerStart,'WLA_PlayerStart',-14,-9,.50);start.set_actor_rotation(unreal.Rotator(),False);w.get_world_settings().set_editor_property('default_game_mode',unreal.PokeMonsterGameMode.static_class())
sun=actor(unreal.DirectionalLight,'WLA_Sun',0,0,18);sun.set_actor_rotation(unreal.Rotator(pitch=-55,yaw=-20,roll=0),False);sun.light_component.set_editor_property('intensity',3.0);sun.light_component.set_editor_property('light_color',unreal.Color(255,243,218,255));sun.light_component.set_editor_property('light_source_angle',4.0)
sky=actor(unreal.SkyLight,'WLA_Sky',0,0,18);sky.light_component.set_editor_property('intensity',1.0)
# Reuse an existing sky sphere visual with no collision; native scene lighting, no new gameplay.
if not any(a.get_actor_label()=='WLA_SkyDome' for a in A.get_all_level_actors()):
 dome=actor(unreal.StaticMeshActor,'WLA_SkyDome',0,0,0);dome.static_mesh_component.set_static_mesh(load('/Engine/EngineSky/SM_SkySphere'));dome.set_actor_scale3d(unreal.Vector(100,100,100));dome.static_mesh_component.set_collision_profile_name('NoCollision');dome.static_mesh_component.set_material(0,load('/Engine/EngineSky/M_Sky_Panning_Clouds2'));dome.static_mesh_component.set_cast_shadow(False)
pp=actor(unreal.PostProcessVolume,'WLA_FixedExposure',0,0);pp.set_editor_property('unbound',True);st=pp.get_editor_property('settings')
for k,v in {'override_auto_exposure_method':True,'auto_exposure_method':unreal.AutoExposureMethod.AEM_MANUAL,'override_auto_exposure_apply_physical_camera_exposure':True,'auto_exposure_apply_physical_camera_exposure':False,'override_auto_exposure_bias':True,'auto_exposure_bias':0}.items():st.set_editor_property(k,v)
pp.set_editor_property('settings',st)
base={'WLA_OakAncient':(-14,14),'WLA_OakYoung':(-6,14),'WLA_Birch':(0,15),'WLA_FruitTree':(8,9),'WLA_Fern':(-12,2),'WLA_Bush':(-17,4),'WLA_Grass':(-10,1),'WLA_Herb':(-9,0),'WLA_Wildflowers':(-11,-1),'WLA_Boulder':(0,0),'WLA_SmallStones':(-3,0),'WLA_Stump':(-1,4),'WLA_Root':(-3,5),'WLA_Bench':(10,0),'WLA_Fence':(11,-1.8),'WLA_Signpost':(7,-1),'WLA_Cart':(16,2),'WLA_Barrel':(13,2),'WLA_Crate':(14,0),'WLA_Haybale':(15,9),'WLA_Woodpile':(17,11),'WLA_Column':(16,18),'WLA_Runestone':(10,16),'WLA_WallRemnant':(13,20)}
placed=[]
for a in data['assets']:
 prefix=a['id'][:-2];e,n=base[prefix]
 if a['variant']=='B':
  if a['family']=='Trees':e-=3;n+=14
  else:
   bank=[x['id'] for x in data['assets'] if x['variant']=='B' and x['family']!='Trees'];j=bank.index(a['id']);e=-26+(j%6)*4.4;n=-17-(j//6)*4.4
 obj=actor(unreal.StaticMeshActor,'Library_'+a['id'],e,n);obj.set_actor_location(world(e,n),False,False);c=obj.static_mesh_component;c.set_static_mesh(meshes[a['id']]);c.set_collision_profile_name('BlockAll' if a['collision_objects'] else 'NoCollision');c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_CAMERA,unreal.CollisionResponseType.ECR_IGNORE);c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_IGNORE);c.set_cast_shadow(a['family']!='Vegetation');c.set_editor_property('generate_overlap_events',False);obj.set_folder_path('WestlandAssetLibrary/'+a['family']);placed.append({'id':a['id'],'E_N_m':[e,n]})
if full:
 rng=random.Random(9034)
 for a in data['assets']:
  if a['family']!='Vegetation':continue
  label='Instancing_'+a['id']
  if any(x.get_actor_label()==label for x in A.get_all_level_actors()):continue
  obj=actor(unreal.Actor,label,0,0);sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);root=sub.k2_gather_subobject_data_for_instance(obj)[0];params=unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True);handle,reason=sub.add_new_subobject(params);c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle));assert c,reason;c.set_static_mesh(meshes[a['id']]);c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False);c.set_cull_distances(6500,9000)
  for j in range(12):
   e=rng.uniform(-19,-6);n=rng.uniform(-2,7)
   if -12.5<e<-9.5 and -2<n<2:continue
   c.add_instance(unreal.Transform(world(e,n),unreal.Rotator(yaw=rng.uniform(0,360)),unreal.Vector(1,1,1)),True)
  obj.set_folder_path('WestlandAssetLibrary/Instancing')
for m in [opaque,leaf]+list(materials.values()):assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
for p in paths:assert unreal.EditorAssetLibrary.save_asset(p,False),p
assert unreal.EditorLoadingAndSavingUtils.save_map(w,MAP)
(OUT/('ImportAudit.json' if full else 'HeroImportAudit.json')).write_text(json.dumps({'map':MAP,'new_assets':paths,'meshes':audit,'placements':placed,'texture_references':textures,'masters':2,'shader_samples_per_pixel':1,'alpha_overdraw':False,'gameplay_code_changed':False},indent=2)+'\n');unreal.log('WLA_IMPORT_COMPLETE '+str(len(audit)))
