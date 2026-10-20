"""Approved V5: remove one stone-floor actor, restore original SilverLady material, dress existing room."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ArtPassV5';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();AS=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);AT=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;D='/Game/Environment/HealingHouse/ArtV5';assert w.get_name()=='Dev_TestMap_VisualV2' and not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not (S/'InteriorApplied.json').exists();actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};bindings=[];new=[];assets=[]
def material(name,code,inputs,rough=.88):
 assert not unreal.EditorAssetLibrary.does_asset_exist(D+'/Materials/'+name);m=AT.create_asset(name,D+'/Materials',unreal.Material,unreal.MaterialFactoryNew());m.set_editor_property('used_with_instanced_static_meshes',True);n=L.create_material_expression(m,unreal.MaterialExpressionCustom);args=[]
 for key in inputs:
  q=unreal.CustomInput();q.set_editor_property('input_name',key);args.append(q)
 n.set_editor_property('inputs',args);n.set_editor_property('code',code);n.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT3)
 for key,(cls,tex) in inputs.items():
  q=L.create_material_expression(m,cls)
  if tex:q.set_editor_property('texture',unreal.load_asset(tex));q.set_editor_property('parameter_name',key)
  assert L.connect_material_expressions(q,'',n,key)
 assert L.connect_material_property(n,'',unreal.MaterialProperty.MP_BASE_COLOR)
 for val,prop in [(rough,unreal.MaterialProperty.MP_ROUGHNESS),(.12,unreal.MaterialProperty.MP_SPECULAR)]:
  q=L.create_material_expression(m,unreal.MaterialExpressionConstant);q.set_editor_property('r',val);assert L.connect_material_property(q,'',prop)
 L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);assets.append(m.get_path_name());return m
floor=material('M_HH5_AgedOak',r'''float2 q=P.xy-float2(16400,-100);float band=floor(q.y/78);float yy=frac(q.y/78)*78;float sub=yy<14?0:(yy<35?1:(yy<53?2:3));float bottom=sub<.5?0:(sub<1.5?14:(sub<2.5?35:53));float width=sub<.5?14:(sub<1.5?21:(sub<2.5?18:25));float row=band*4+sub;float hash=frac(sin(row*17.137)*427.313);float length=145+68*hash;float shift=hash*length;float2 cell=float2((q.x+shift)/length,(yy-bottom)/width);float2 f=frac(cell);float plank=frac(sin(floor(cell.x)*31.17+row*57.3)*14573.3);float edge=min(min(f.x,1-f.x)*length,min(f.y,1-f.y)*width);float seam=smoothstep(.08,.35,edge);float3 tex=Texture2DSample(Tex,TexSampler,float2(q.y/190+row*.139,q.x/425+shift*.001)).rgb;float grain=sin(q.y*2.1+sin(q.x*.053+row)*.9);float aged=sin(q.x*.012+row*1.7)*cos(q.y*.021-q.x*.004);float endWear=exp(-pow(edge/1.8,2));float3 tone=lerp(float3(.68,.60,.48),float3(.88,.78,.63),plank);float3 c=tex*tone*(.98+.055*aged+.018*grain+.035*endWear);return c*lerp(.58,1,seam);''',{'P':(unreal.MaterialExpressionWorldPosition,None),'Tex':(unreal.MaterialExpressionTextureObjectParameter,'/Game/Environment/HealingHouse/QualityV2/Textures/T_HH_PaintedWood')},.91)
crafted=material('M_HH5_LinenJoinery',r'''float3 c=lerp(C/12.92,pow(max((C+.055)/1.055,0),2.4),step(.04045,C));float fabric=smoothstep(.15,.30,C.g)*smoothstep(.95,1.12,C.g/max(C.r,.01));float grain=sin(P.z*.62+sin(P.x*.035)*1.2);float weave=sin(P.x*3.8)*sin(P.y*3.7);return c*(1+.045*grain*(1-fabric)+.022*weave*fabric);''',{'P':(unreal.MaterialExpressionWorldPosition,None),'C':(unreal.MaterialExpressionVertexColor,None)},.9)
hearth=material('M_HH5_HearthLimestone',r'''float mask=smoothstep(.12,.30,C.g)*smoothstep(.65,.90,C.g/max(C.r,.01));float3 a=Texture2DSample(Tex,TexSampler,P.yz/95).rgb;float3 b=Texture2DSample(Tex,TexSampler,P.xz/173+float2(.31,.47)).rgb;float value=dot(lerp(a,b,.30),float3(.3,.59,.11));float3 stone=float3(.54,.505,.427)*(.45+.85*value);float grain=sin(P.z*.37+sin(P.y*.083));stone*=1+.045*grain;float3 wood=lerp(C/12.92,pow(max((C+.055)/1.055,0),2.4),step(.04045,C));return lerp(wood,stone,mask);''',{'P':(unreal.MaterialExpressionWorldPosition,None),'C':(unreal.MaterialExpressionVertexColor,None),'Tex':(unreal.MaterialExpressionTextureObjectParameter,'/Game/Environment/HealingHouse/QualityV2/Textures/T_HH_PaintedStone')},.94)
def bind(c,slot,m):
 old=c.get_material(slot);bindings.append({'actor':c.get_owner().get_name(),'component':c.get_name(),'slot':slot,'before':old.get_path_name() if old else None,'after':m.get_path_name()});c.set_material(slot,m)
removed=[]
for label,a in actors.items():
 c=a.get_component_by_class(unreal.StaticMeshComponent)
 if c and c.static_mesh and c.static_mesh.get_name()=='SM_HH4_FlagstoneApron':
  assert c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION;removed.append({'actor':a.get_name(),'label':label,'mesh':c.static_mesh.get_path_name()});assert AS.destroy_actor(a)
assert len(removed)==1
floorchanges=[]
for label,a in actors.items():
 if label.startswith('V2_House_HH_Art_Floor_'):
  c=a.static_mesh_component;assert c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION;before=c.static_mesh.get_path_name();c.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Plane'));a.set_actor_scale3d(unreal.Vector(2,2,1));bind(c,0,floor);floorchanges.append({'actor':a.get_name(),'old_mesh':before,'new_mesh':c.static_mesh.get_path_name(),'scale':[2,2,1],'height_cm':a.get_actor_location().z})
 if label.startswith('ArtV4_Hearth_'):bind(a.static_mesh_component,0,hearth)
assert len(floorchanges)==30
# Original visual material; no tint, vertex-mask recolor, face/hair or geometry edit.
h=actors['V2_House_SilverLady_HealerVisual'];original=unreal.load_asset('/Game/Characters/NPCs/SilverLady/Materials/MI_SilverLady_V1');assert original;bind(h.visual,0,original);h.refresh_presentation();assert h.visual.get_material(0)==original and h.source_actor.get_name()=='PokeMonsterRestPoint_1'
meshes={};SM=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
for row in json.loads((R/'Art/HealingHouse/ArtV5_Props.json').read_text())['assets']:
 name='SM_HH5_'+row['name'];ui=unreal.FbxImportUI();ui.import_mesh=True;ui.import_materials=False;ui.import_textures=False;ui.import_as_skeletal=False;ui.automated_import_should_detect_type=False;ui.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
 for k,v in {'combine_meshes':True,'auto_generate_collision':False,'convert_scene':True,'convert_scene_unit':True,'transform_vertex_to_absolute':True,'vertex_color_import_option':unreal.VertexColorImportOption.REPLACE,'normal_import_method':unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,'normal_generation_method':unreal.FBXNormalGenerationMethod.MIKK_T_SPACE}.items():ui.static_mesh_import_data.set_editor_property(k,v)
 assert not unreal.EditorAssetLibrary.does_asset_exist(D+'/Meshes/'+name);t=unreal.AssetImportTask();t.filename=str(R/'Art/HealingHouse/Exports'/(name+'.fbx'));t.destination_path=D+'/Meshes';t.destination_name=name;t.options=ui;t.automated=True;AT.import_asset_tasks([t]);m=unreal.load_asset(D+'/Meshes/'+name);assert m and m.get_num_triangles(0)==row['triangles'];m.set_material(0,crafted)
 if row['name']=='ReadingChair':assert SM.add_simple_collisions(m,unreal.ScriptingCollisionShapeType.BOX)>=0
 assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);assets.append(m.get_path_name());meshes[row['name']]=m
# Only the one new usable chair has collision; existing benches retain their blockers.
def prop(mesh,label,pos,yaw=0,scale=(1,1,1),collision=False):
 a=AS.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*pos),unreal.Rotator(yaw=yaw));a.set_actor_label('ArtV5_'+label);a.set_folder_path('VisualV2/HealingHouse/ArtV5');a.tags=['ArtV5','PhysicalFurniture' if collision else 'VisualOnly_NoCollision'];a.set_actor_scale3d(unreal.Vector(*scale));c=a.static_mesh_component;c.set_static_mesh(mesh);c.set_collision_profile_name('BlockAll' if collision else 'NoCollision');c.set_cast_shadow(False);c.set_lighting_channels(False,True,False);c.set_editor_property('affect_dynamic_indirect_lighting',False);c.set_editor_property('affect_distance_field_lighting',False);new.append({'actor':a.get_name(),'label':a.get_actor_label(),'mesh':mesh.get_path_name(),'position':pos,'collision':collision});return a
prop(meshes['ReadingChair'],'ReadingChair',(16805,145,0),0,collision=True)
for i,(x,y,yaw) in enumerate([(16635,125,0),(16695,125,0),(16520,155,90),(16520,215,90)]):prop(meshes['LinenCushion'],'BenchCushion_'+str(i),(x,y,49),yaw)
side=prop(unreal.load_asset('/Game/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_Table'),'TeaSideTable',(16805,265,0),0,(.45,.45,.62));
# Small side table is decorative and its footprint stays outside the main route.
for i in range(side.static_mesh_component.get_num_materials()):bind(side.static_mesh_component,i,unreal.load_asset('/Game/Environment/VisualV2HealingArtV4/Materials/M_HH_InteriorWood'))
prop(meshes['HerbalBooks'],'ReadingBooks',(16805,268,46.5),15,scale=(.80,.80,.80))
prop(meshes['HerbalBooks'],'HerbWorkBooks',(16555,855,71),-12,scale=(.8,.8,.8))
tray=unreal.load_asset('/Game/Environment/VisualV2HealingArtV4/Meshes/SM_HH_HerbalRemedyTray');prop(tray,'BedsideRemedies',(17125,805,0),0,(.85,.85,.85))
# Existing broad room-only source, no new exterior or dynamic-shadow light.
c=actors['V2_House_InteriorDiffuse'].get_component_by_class(unreal.RectLightComponent);light_before={'intensity':c.intensity,'width':c.source_width,'height':c.source_height,'temperature':c.temperature};c.set_intensity(1000);c.set_editor_property('source_width',1200);c.set_editor_property('source_height',1000);assert not c.cast_shadows and c.indirect_lighting_intensity==0
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
record={'removed_stone_actors':removed,'floor_changes':floorchanges,'material_bindings':bindings,'new_actors':new,'assets':assets,'original_silverlady_material':original.get_path_name(),'silverlady_mesh_and_animation_retained':True,'light_before':light_before,'light_after':{'intensity':1000,'width':1200,'height':1000,'temperature':c.temperature},'collision_floor_untouched':True};(S/'InteriorApplied.json').write_text(json.dumps(record,indent=2));(R/'Art/HealingHouse/ArtV5_Interior.json').write_text(json.dumps(record,indent=2));unreal.log('ART_V5_INTERIOR_SAVED')
