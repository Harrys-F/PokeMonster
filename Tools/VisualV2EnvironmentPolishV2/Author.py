"""One-time bounded VisualV2 surface/decor polish; preserve all shared assets and gameplay."""
import unreal,json,math,random,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2EnvironmentPolishV2';ROOT='/Game/Environment/VisualV2EnvironmentPolishV2';L='/Game/Fab/VisualV2TrialLocal/PolishV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);ML=unreal.MaterialEditingLibrary;AT=unreal.AssetToolsHelpers.get_asset_tools();SUB=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);assert W.get_name()=='Dev_TestMap_VisualV2'and not E.get_game_world();assert not(D/'Authored.json').exists();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();actors={a.get_actor_label():a for a in A.get_all_level_actors()};changed=[];removed=[];groups={};rng=random.Random(2611022);imports=json.loads((D/'ImportedFab.json').read_text());meshpaths={x['key']+(x.get('var')or''):x['mesh']for x in imports};paths=json.loads((R/'Tools/VisualV2FabAssetTrialV1/ExistingPaths.json').read_text());segments=[(a,b)for ps in paths.values()for a,b in zip(ps,ps[1:])]
def segment(x,y,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)));return math.hypot(x-a[0]-t*dx,y-a[1]-t*dy)
def pathdist(x,y):return min(segment(x,y,a,b)for a,b in segments)
def group(key,path,mat=None,shadow=False):
 if key in groups:return groups[key]
 m=unreal.load_asset(path);assert m,path;a=A.spawn_actor_from_class(unreal.Actor,unreal.Vector());a.set_actor_label('EP2_'+key);a.set_folder_path('VisualV2/EnvironmentPolishV2');a.tags=['VisualV2EnvironmentPolishV2'];h,r=SUB.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=SUB.k2_gather_subobject_data_for_instance(a)[0],new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h));assert c,r;c.set_static_mesh(m)
 if mat:
  for i in range(len(m.static_materials)):c.set_material(i,unreal.load_asset(mat))
 c.set_collision_profile_name('NoCollision');c.set_editor_property('generate_overlap_events',False);c.set_cast_shadow(shadow);c.set_editor_property('affect_distance_field_lighting',False);c.set_cull_distances(4500,6000);groups[key]=c;return c
def put(key,path,x,y,height,mat=None,z=0,yaw=None,shadow=False):
 c=group(key,path,mat,shadow);b=c.static_mesh.get_bounding_box();s=height/max(1,b.max.z-b.min.z);c.add_instance(unreal.Transform(location=unreal.Vector(x,y,z-b.min.z*s-.7),rotation=unreal.Rotator(yaw=rng.uniform(0,360)if yaw is None else yaw),scale=unreal.Vector(s,s,s)),True)
# The terrain is a StaticMesh, not Landscape. Integrate both path colour and normal into ONE surface.
m=unreal.EditorAssetLibrary.duplicate_asset('/Game/Environment/VisualV2FabAssetTrialV1/Materials/M_FAT_Ground',ROOT+'/Materials/M_EP2_Ground');assert m
sys.path.insert(0,str(R/'Tools/VisualV2FabAssetTrialV1'))
def node(cls):return ML.create_material_expression(m,cls)
def custom(code,inputs,typ=unreal.CustomMaterialOutputType.CMOT_FLOAT3):
 n=node(unreal.MaterialExpressionCustom);n.set_editor_property('code',code);n.set_editor_property('output_type',typ);lst=[]
 for key in inputs:i=unreal.CustomInput();i.set_editor_property('input_name',key);lst.append(i)
 n.set_editor_property('inputs',lst)
 for key,(src,pin)in inputs.items():assert ML.connect_material_expressions(src,pin,n,key)
 return n
def tex(path,uv,normal=False):
 n=node(unreal.MaterialExpressionTextureSample);n.texture=unreal.load_asset(path);assert n.texture,path
 if normal:n.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
 assert ML.connect_material_expressions(uv,'',n,'UVs');return n
oldnodes=list(ML.get_material_expressions(m));color=next(n for n in oldnodes if isinstance(n,unreal.MaterialExpressionCustom)and'float meadow='in n.get_editor_property('code'));normal=next(n for n in oldnodes if isinstance(n,unreal.MaterialExpressionCustom)and'normalize(lerp'in n.get_editor_property('code'));P=next(n for n in oldnodes if isinstance(n,unreal.MaterialExpressionWorldPosition));uv=custom('return (P.xy-float2(-6000,-3250))/float2(9000,6500);',{'P':(P,'')},unreal.CustomMaterialOutputType.CMOT_FLOAT2)
t=unreal.AssetImportTask();t.filename=str(D/'PathMask.png');t.destination_path=ROOT+'/Textures';t.destination_name='T_EP2_PathMask';t.automated=True;t.save=False;AT.import_asset_tasks([t]);maskasset=unreal.load_asset(ROOT+'/Textures/T_EP2_PathMask');assert maskasset;maskasset.set_editor_property('srgb',False);maskasset.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS);assert unreal.EditorAssetLibrary.save_loaded_asset(maskasset,False);mask=tex(maskasset.get_path_name(),uv);mask.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_MASKS);mask.set_editor_property('sampler_source',unreal.SamplerSourceMode.SSM_CLAMP_WORLD_GROUP_SETTINGS)
uv2=custom('return P.xy/240.0;',{'P':(P,'')},unreal.CustomMaterialOutputType.CMOT_FLOAT2);tc=tex('/Game/Fab/VisualV2TrialLocal/Ground/T_ugsnfawlw_2K_B',uv2);tn=tex('/Game/Fab/VisualV2TrialLocal/Ground/T_ugsnfawlw_2K_N',uv2,True)
c=custom('float g=dot(T,float3(.299,.587,.114));float3 dirt=lerp(T*float3(1.03,.90,.72),g*float3(1.08,.94,.76),.60);return lerp(C,dirt*.90,M);',{'T':(tc,'RGB'),'C':(color,''),'M':(mask,'R')});assert ML.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR);n=custom('return normalize(lerp(N,normalize(lerp(float3(0,0,1),P,.48)),M));',{'N':(normal,''),'P':(tn,'RGB'),'M':(mask,'R')});assert ML.connect_material_property(n,'',unreal.MaterialProperty.MP_NORMAL);ML.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);ground=actors['V2_Ground'];ground.modify();ground.static_mesh_component.set_material(0,m);changed.append(ground.get_name())
for key in paths:
 a=actors['V2_Path_'+key];assert a.static_mesh_component.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION;removed.append(dict(name=a.get_name(),label=a.get_actor_label(),reason='Nonblocking duplicate path skin 0.15–0.75cm above existing terrain; colour/normal now in ground layer'));assert A.destroy_actor(a)
# Pure decorative sprites only; no character, gameplay, particle or UI components.
style='/Game/StyleHex_Studio/Free_Packs/FREE_Stylized_Grass_Flowers_Foliage/Meshes/';replaced=[]
for a in list(A.get_all_level_actors()):
 if not isinstance(a,unreal.PaperSpriteActor)or a.get_editor_property('hidden'):continue
 c=a.render_component
 if not c.is_visible()or c.get_editor_property('hidden_in_game'):continue
 label=a.get_actor_label();assert label.startswith(('SliceDetail','EW_','V2_House_')),label;src=c.get_editor_property('source_sprite');name=src.get_name()if src else '';assert not src or src.get_editor_property('body_setup')is None; x,y,z=a.get_actor_location().to_tuple();kind=(name+' '+label).lower();category='grass'
 if not src:
  replaced.append(dict(name=a.get_name(),label=label,source=None,category='empty obsolete actor',position=[x,y,z]));assert A.destroy_actor(a);continue
 if 'oak'in kind:category='tree';put('ReplacementOak','/Game/Environment/WestlandAssetLibrary/QualityV3/Meshes/Trees/SM_WLA_OakAncient_V3',x,y,430,shadow=True)
 elif 'stump'in kind:category='stump';put('ReplacementStump','/Game/Environment/WestlandAssetLibrary/Meshes/Landscape/SM_WLA_Stump_A',x,y,35)
 elif 'stone'in kind or'rock'in kind:category='stone';put('ReplacementStone','/Game/RockEnv_Pack/Meshes/Small_Rocks/SM_Small_Rock_1',x,y,12)
 elif 'bush'in kind:category='shrub';put('ReplacementShrub',meshpaths['HydrangeaA'],x,y,65)
 elif 'flower'in kind:category='flower';put('ReplacementFlower',style+'SM_Fol_Flower_Clump_2',x,y,26,'/Game/Environment/VisualV2FabAssetTrialV1/Materials/MI_FAT_Flowers')
 else:put('ReplacementGrass',style+'SM_Fol_Grass_Clump_2',x,y,24,'/Game/Environment/VisualV2FabAssetTrialV1/Materials/MI_FAT_Grass')
 replaced.append(dict(name=a.get_name(),label=label,source=name,category=category,position=[x,y,z]));assert A.destroy_actor(a)
# 18 old grass clusters consist of three crossed flat plane actors each.
card_clusters={}
for a in list(A.get_all_level_actors()):
 if not a.get_actor_label().startswith('P2D_Grass_'):continue
 c=a.get_component_by_class(unreal.StaticMeshComponent);assert c and c.static_mesh.get_path_name()=='/Engine/BasicShapes/Plane.Plane'and c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
 assert c.get_material(0).get_path_name().startswith('/Game/Environment/Prototype2D/Materials/M_GrassTuft');label=a.get_actor_label();cluster='_'.join(label.split('_')[:3]);card_clusters.setdefault(cluster,[]).append(a.get_actor_location().to_tuple());removed.append(dict(name=a.get_name(),label=label,reason='Old flat crossed grass card replaced by one three-dimensional multi-blade clump per cluster'));assert A.destroy_actor(a)
for cluster,ps in card_clusters.items():
 x=sum(p[0]for p in ps)/len(ps);y=sum(p[1]for p in ps)/len(ps);put('ReplacementTuft',style+'SM_Fol_Grass_Clump_3',x,y,28,'/Game/Environment/VisualV2FabAssetTrialV1/Materials/MI_FAT_Grass')
# Low groundcovers and sparse garden shrubs frame routes without filling their walkable centres.
for i in range(180):
 x=rng.uniform(-5300,-3700);y=rng.uniform(-2750,-1400)
 if pathdist(x,y)<170 or math.sin(x*.008)*math.sin(y*.012)<-.25:continue
 key='Pratia'+('A'if i%2 else'B');put(key,meshpaths[key],x,y,rng.uniform(9,17))
for i in range(90):
 x=rng.uniform(-5050,-3700);y=rng.uniform(800,2400)
 if pathdist(x,y)<190:continue
 key='Mushroom'+('A'if i%2 else'B');put(key,meshpaths[key],x,y,rng.uniform(8,15))
for x,y in [(-4490,-250),(-4460,325),(-4320,680),(-3630,1110),(-2780,-1210),(-2820,-810)]:put('HydrangeaB',meshpaths['HydrangeaA'],x,y,rng.uniform(55,80))
# Small banks lie outside the water and away from the existing bridge; no second water sheet.
for x,y,yaw in [(-40,-439,0),(150,-198,180),(430,-441,0),(940,-195,180)]:put('MossyBank',meshpaths['Embankment'],x,y,23,z=-7,yaw=yaw,shadow=True)
# Existing five fence segments stay in the tested garden U; no invented new district.
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages(),'Never save imported originals';assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2');(D/'Authored.json').write_text(json.dumps(dict(changed=changed,removed=removed,replaced_sprites=replaced,groups=[dict(key=k,count=c.get_instance_count(),mesh=c.static_mesh.get_path_name(),collision=str(c.get_collision_enabled()))for k,c in groups.items()],path_strategy='StaticMesh ground material layer; no Landscape actor exists; unchanged underlying terrain geometry and collision',new_water_surface=False,gameplay_edits=False),indent=2))
