"""Add only the owner-authored northern forest to existing VisualV2.
Requires the locally licensed Fab EuropeanBeech import; never edits/resaves its assets.
Run once from the existing editor via ArtControl. Layout.py is the sole placement source.
"""
import unreal,json,collections,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/EuropeanBeechV1';P='/Game/Environment/EuropeanBeechV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();AS=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);L=unreal.MaterialEditingLibrary;T=unreal.AssetToolsHelpers.get_asset_tools()
assert not E.get_game_world() and W.get_path_name().startswith('/Game/Maps/Dev_TestMap_VisualV2.')
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
assert all(p.get_path_name().startswith(P+'/')for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages())
old=unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor);assert not any(a.get_actor_label().startswith('EBF1_') for a in old)
exec((R/'Tools/EuropeanBeechV1/Snapshot.py').read_text())
before=snapshot(old);(D/'ExistingActorsBefore.json').write_text(json.dumps(before,indent=2))
plan=json.loads((R/'Tools/EuropeanBeechV1/Layout.json').read_text());required=sorted({x['mesh'] for x in plan['objects']});meshes={p:unreal.load_asset(p) for p in required};assert all(meshes.values()),[p for p,v in meshes.items() if not v]
# Own numeric ground mask and own material graphs. Original textures are read-only references.
mask=unreal.load_asset(P+'/Textures/T_EBF_PathMask')
if not mask:
 task=unreal.AssetImportTask();task.filename=str(R/'Art/World/EuropeanBeechV1/PathMask.png');task.destination_path=P+'/Textures';task.destination_name='T_EBF_PathMask';task.automated=True;task.save=False;task.replace_existing=False;T.import_asset_tasks([task]);mask=unreal.load_asset(P+'/Textures/T_EBF_PathMask')
assert mask
mask.set_editor_property('srgb',False);mask.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS);mask.set_editor_property('address_x',unreal.TextureAddress.TA_CLAMP);mask.set_editor_property('address_y',unreal.TextureAddress.TA_CLAMP);assert unreal.EditorAssetLibrary.save_loaded_asset(mask,False)
def node(m,cls):return L.create_material_expression(m,cls)
def ci(name):c=unreal.CustomInput();c.set_editor_property('input_name',name);return c
def value(m,v):n=node(m,unreal.MaterialExpressionConstant);n.set_editor_property('r',v);return n
def material(name,connector=False):
 m=unreal.load_asset(P+'/Materials/'+name)
 if m:
  assert unreal.EditorAssetLibrary.get_metadata_tag(m,'EuropeanBeechOwner')=='V1';L.delete_all_material_expressions(m)
 else:m=T.create_asset(name,P+'/Materials',unreal.Material,unreal.MaterialFactoryNew());unreal.EditorAssetLibrary.set_metadata_tag(m,'EuropeanBeechOwner','V1')
 c=node(m,unreal.MaterialExpressionCustom);c.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT3);c.set_editor_property('inputs',[ci(x)for x in ['P','F','E','G','M']])
 code='''float2 uv=(P.xy-float2(-7500,3000))/12000;
float2 mask=Texture2DSample(M,MSampler,uv).rg;
float3 f=Texture2DSample(F,FSampler,P.xy/210.0).rgb;
float3 e=Texture2DSample(E,ESampler,P.xy/230.0).rgb;
float3 g=Texture2DSample(G,GSampler,P.xy/220.0).rgb;
float edge=smoothstep(3050,4100,P.y);
float macro=.96+.025*sin(P.x*.0013+sin(P.y*.0011))+.02*cos(P.y*.0021);
float3 soil=lerp(g,f,edge);soil=lerp(soil,g,mask.g*.85);
return lerp(soil,e*.91,mask.r)*macro;''' if not connector else '''return Texture2DSample(E,ESampler,P.xy/230.0).rgb*.91;'''
 c.set_editor_property('code',code)
 p=node(m,unreal.MaterialExpressionWorldPosition);assert L.connect_material_expressions(p,'',c,'P')
 for key,path in {'F':'/Game/Environment/VisualV2WorldArtV5/Textures/T_WA5_ForestFloor','E':'/Game/Environment/VisualV2HealingArtV4/Textures/T_HA4_Earth','G':'/Game/Environment/VisualV2HealingArtV4/Textures/T_HA4_Meadow','M':P+'/Textures/T_EBF_PathMask'}.items():
  t=node(m,unreal.MaterialExpressionTextureObject);t.set_editor_property('texture',unreal.load_asset(path));assert t.get_editor_property('texture');assert L.connect_material_expressions(t,'',c,key)
 assert L.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR)
 for prop,v in [(unreal.MaterialProperty.MP_ROUGHNESS,.93),(unreal.MaterialProperty.MP_SPECULAR,.1)]:assert L.connect_material_property(value(m,v),'',prop)
 if connector:
  m.set_editor_property('blend_mode',unreal.BlendMode.BLEND_MASKED);m.set_editor_property('opacity_mask_clip_value',.15)
  a=node(m,unreal.MaterialExpressionCustom);a.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT1);a.set_editor_property('inputs',[ci('P')]);a.set_editor_property('code','return 1-smoothstep(121,150,abs(P.x+3300)+5*sin(P.y*.03));');assert L.connect_material_expressions(p,'',a,'P');assert L.connect_material_property(a,'',unreal.MaterialProperty.MP_OPACITY_MASK)
 L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);return m
ground=material('M_EBF_ForestGround');trail=material('M_EBF_Connector',True)
def label(a,n):a.set_actor_label('EBF1_'+n);a.set_folder_path('VisualV2/EuropeanBeechV1');a.tags=['EuropeanBeechV1','LandscapeOnly_NoSpawn']
for name,path,pos,scale,mat,collision in [('ForestFloor','/Engine/BasicShapes/Cube',(-1500,9000,-19.8),(120,120,.4),ground,True),('AccessTrail','/Engine/BasicShapes/Plane',(-3300,2875,.5),(3,10.5,1),trail,False)]:
 a=AS.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*pos));label(a,name);a.set_actor_scale3d(unreal.Vector(*scale));c=a.static_mesh_component;c.set_static_mesh(unreal.load_asset(path));c.set_material(0,mat);c.set_collision_profile_name('BlockAll' if collision else 'NoCollision');c.set_cast_shadow(False);c.set_editor_property('affect_distance_field_lighting',False)
sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);groups=collections.defaultdict(list)
for o in plan['objects']:groups[(o['zone'],o['mesh'])].append(o)
summary=[]
for (zone,path),objects in sorted(groups.items()):
 family=objects[0]['family'];a=AS.spawn_actor_from_class(unreal.Actor,unreal.Vector());label(a,zone+'_'+path.rsplit('/',1)[1]);root=sub.k2_gather_subobject_data_for_instance(a)[0];h,reason=sub.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h));assert c,reason;c.set_static_mesh(meshes[path]);blocking=family in ['Canopy','UnderTree','Sapling','Stump','Deadwood'];c.set_collision_profile_name('BlockAll' if blocking else 'NoCollision');c.set_cast_shadow(objects[0]['shadow']);c.set_editor_property('affect_distance_field_lighting',blocking)
 c.set_cull_distances(13000,18000) if family in ['Canopy','UnderTree'] else c.set_cull_distances(6000,8500)
 for o in objects:c.add_instance(unreal.Transform(location=unreal.Vector(*o['position']),rotation=unreal.Rotator(yaw=o['yaw']),scale=unreal.Vector(*o['scale'])),True)
 assert c.get_instance_count()==len(objects);summary.append({'actor':a.get_actor_label(),'mesh':path,'family':family,'count':len(objects),'blocking':blocking,'cast_shadow':objects[0]['shadow']})
after=snapshot(old);assert before==after,'Existing actors changed! No map saved.'
assert all(p.get_path_name().startswith(P+'/')for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()),'Unexpected original dirty package; do not save'
assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2')
result={'groups':summary,'instance_count':sum(g['count']for g in summary),'new_actors':len(summary)+2,'existing_actors_unchanged':len(old),'owned_assets':[P+'/Textures/T_EBF_PathMask',P+'/Materials/M_EBF_ForestGround',P+'/Materials/M_EBF_Connector'],'bounds_cm':plan['bounds_cm']};(D/'Build.json').write_text(json.dumps(result,indent=2));unreal.log('EUROPEAN_BEECH_BUILD_SAVED '+str(result['instance_count']))
