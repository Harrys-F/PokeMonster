"""Bounded, visual-only Healing House pass. Original assets, collision and all lighting remain unchanged.
One-shot authoring tool. Refuses existing output assets; no deletion/rebuild fallback.
"""
import unreal,json,math,random,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtQualityV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2' and not E.get_game_world();assert all(p.get_path_name()=='/Game/Maps/Dev_TestMap_VisualV2' for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages());assert all(p.get_path_name().startswith('/Game/Environment/VisualV2WorldArtV1/') for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages())
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
before=json.loads((S/'Dev_TestMap_VisualV2_Scene.json').read_text());actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)}
assert not (S/'ArtChanges.json').exists(),'Already completed: never stack the pass twice'
D='/Game/Environment/VisualV2WorldArtV1/Materials';T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;changes=[];newm=[]
area='smoothstep(-4620,-4510,p.x)*(1-smoothstep(-3670,-3560,p.x))*smoothstep(-720,-610,p.y)*(1-smoothstep(1080,1190,p.y))'
soil='''
float art='''+area+''';
float soil=.5+.25*sin(p.x*.013+sin(p.y*.009))+.16*cos(p.y*.021-p.x*.006);
d=lerp(d,lerp(d,dot(d,float3(.299,.587,.114)).xxx,.13)*lerp(float3(.89,.93,.87),float3(1.06,1.015,.95),saturate(soil)),art);
'''
for label,src,name in [('V2_Ground','/Game/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_Grass','M_WAQ1_HealingMeadow'),('PATH','/Game/Environment/DevTestMapVisualV2/Materials/M_V2_PathBlend','M_WAQ1_HealingPath'),('V2_House_Forecourt','/Game/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_ForecourtBlend','M_WAQ1_HealingForecourt')]:
 m=unreal.load_asset(D+'/'+name) if unreal.EditorAssetLibrary.does_asset_exist(D+'/'+name) else unreal.EditorAssetLibrary.duplicate_asset(src,D+'/'+name);assert m
 nodes=[x for x in unreal.ObjectIterator(unreal.MaterialExpression) if x.get_outer()==m];color=next(x for x in nodes if isinstance(x,unreal.MaterialExpressionCustom) and x.get_editor_property("output_type")==unreal.CustomMaterialOutputType.CMOT_FLOAT3);code=color.get_editor_property("code")
 needle='if(Mode<.5)return g;';assert needle in code
 code=code if 'float meadow=' in code else code.replace(needle,'float meadow='+area+';float patch=sin(p.x*.009+cos(p.y*.008))*cos(p.y*.011-p.x*.003);g*=lerp(float3(1,1,1),float3(.96,1.015,.94)*(1+.07*patch),meadow);'+needle)
 needle='if(Mode<1.5)return d;';assert needle in code;code=code if 'float soil=' in code else code.replace(needle,soil+needle);color.set_editor_property("code",code)
 if label=='PATH':
  mask=next(x for x in nodes if isinstance(x,unreal.MaterialExpressionCustom) and x.get_editor_property('desc')=='VisualV2 path edge opacity');old=mask.get_editor_property("code");old=old[old.index('float irregular='):] if old.startswith('float2 p=P.xy;') else old;mask.set_editor_property("code",'float2 p=P.xy;float art='+area+';'+old.replace('float edge=abs(UV.y*2-1)+irregular;','irregular+=art*(sin(P.y*.031+cos(P.x*.024))*.065+sin(P.x*.095+P.y*.072)*.025);float edge=abs(UV.y*2-1)+irregular;'))
 if label=='V2_House_Forecourt':
  for x in nodes:
   if isinstance(x,unreal.MaterialExpressionVectorParameter):
    if str(x.get_editor_property("parameter_name"))=='CourtCenter_cm':x.set_editor_property("default_value",unreal.LinearColor(-3910,500,0,0))
    if str(x.get_editor_property("parameter_name"))=='CourtHalfSize_cm':x.set_editor_property("default_value",unreal.LinearColor(390,360,0,0))
 L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);newm.append(m.get_path_name())
 targets=[actors[n] for n in ['V2_Path_VillageLoop','V2_Path_NorthLoop']] if label=='PATH' else [actors[label]]
 for a in targets:
  c=a.static_mesh_component;changes.append({'label':a.get_actor_label(),'old':before['actors'][a.get_name()]['components'][0]['materials'][0],'new':m.get_path_name()});c.set_material(0,m)
# Cohesive small planting pockets rather than a uniform sprinkle. Keep the established 2.7 m path clear.
rng=random.Random(191026);A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);groups=[]
centres=[(-4400,-400),(-3915,-300),(-4370,0),(-3880,85),(-4415,280),(-4330,790),(-4210,1010),(-3910,830),(-3735,955),(-3720,140)]
def distseg(x,y,a,b):
 dx=b[0]-a[0];dy=b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)));return math.hypot(x-a[0]-t*dx,y-a[1]-t*dy)
route=[(-4150,-720),(-4100,450),(-3600,500)];north=[(-4100,450),(-4300,1190)]
def safe(x,y,radius):
 if not(-4510<x<-3630 and -610<y<1080):return False
 if x>-3800 and 300<y<720:return False # generous door/porch exclusion
 return min(distseg(x,y,a,b) for a,b in list(zip(route,route[1:]))+list(zip(north,north[1:])))>155+radius
G='/Game/Environment/Westland/NaturalGroundV1/Meshes/SM_WL_NG_';W='/Game/Environment/WestlandAssetLibrary/Meshes/Vegetation/SM_WLA_'
for key,path,count,scale,rad,source in [('GrassSmall',G+'GrassSmall',54,1.0,18,None),('GrassMedium',G+'GrassMedium',36,.95,30,None),('MeadowHerbs',G+'MeadowHerbs',28,1.0,25,None),('Flowers',W+'Wildflowers_A',18,.64,26,'V2_Instanced_Flowers'),('Fern',W+'Fern_A',12,.48,38,'V2_Instanced_Fern'),('Pebbles',G+'PebbleCluster',27,.7,12,None)]:
 mesh=unreal.load_asset(path);assert mesh;actor=actors.get('WAQ1_'+key) or A.spawn_actor_from_class(unreal.Actor,unreal.Vector());actor.set_actor_label('WAQ1_'+key);actor.set_folder_path('VisualV2/WorldArtV1/HealingHouse');actor.tags=['WorldArtQualityV1','VisualOnly_NoCollision'];existing=actor.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);root=sub.k2_gather_subobject_data_for_instance(actor)[0];handle,reason=(None,None) if existing else sub.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True));c=existing or unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle));assert c,reason;initial_count=c.get_instance_count();assert initial_count in (0,count);c.set_static_mesh(mesh);c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False);c.set_cull_distances(4500,6500);c.set_editor_property('affect_distance_field_lighting',False);c.set_editor_property('affect_dynamic_indirect_lighting',False)
 if source:
  original=actors[source].get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);assert original
  for i in range(c.get_num_materials()):c.set_material(i,original.get_material(i))
 for i in range(c.get_num_materials()):
  mat=c.get_material(i)
  while isinstance(mat,unreal.MaterialInstance):mat=mat.parent
  if not mat.used_with_instanced_static_meshes:
   original_mat=c.get_material(i);parent_path=D+'/'+mat.get_name()+'_Instanced';parent=unreal.load_asset(parent_path) if unreal.EditorAssetLibrary.does_asset_exist(parent_path) else unreal.EditorAssetLibrary.duplicate_asset(mat.get_path_name(),parent_path);parent.set_editor_property('used_with_instanced_static_meshes',True);L.recompile_material(parent);assert unreal.EditorAssetLibrary.save_loaded_asset(parent,False)
   instance_path=D+'/'+original_mat.get_name()+'_Instanced';mi=unreal.load_asset(instance_path) if unreal.EditorAssetLibrary.does_asset_exist(instance_path) else unreal.EditorAssetLibrary.duplicate_asset(original_mat.get_path_name(),instance_path);L.set_material_instance_parent(mi,parent);assert unreal.EditorAssetLibrary.save_loaded_asset(mi,False);c.set_material(i,mi)
   for n in [parent.get_path_name(),mi.get_path_name()]:
    if n not in newm:newm.append(n)
 placed=[]
 for _ in range(10000):
  if len(placed)>=count:break
  cx,cy=rng.choice(centres);x=rng.gauss(cx,62 if key!='Pebbles' else 100);y=rng.gauss(cy,75)
  if not safe(x,y,rad):continue
  if any(math.hypot(x-p[0],y-p[1])<rad*.75 for p in placed):continue
  sc=scale*rng.uniform(.72,1.18);z=.4 if key!='Pebbles' else -.3;transform=unreal.Transform(location=unreal.Vector(x,y,z),rotation=unreal.Rotator(pitch=rng.uniform(-4,4) if key=='Pebbles' else 0,yaw=rng.uniform(0,360)),scale=unreal.Vector(sc*rng.uniform(.9,1.1),sc,sc*(.50 if key=='Pebbles' else rng.uniform(.88,1.1))));c.add_instance(transform,True) if initial_count==0 else None;placed.append([x,y,sc])
 assert len(placed)==count,key;groups.append({'label':actor.get_actor_label(),'mesh':path,'instances':placed,'collision':str(c.get_collision_enabled()),'cast_shadow':False,'materials':[c.get_material(i).get_path_name() for i in range(c.get_num_materials())]})
after=scene(w);changed={k for k in before['actors'] if before['actors'][k]!=after['actors'].get(k)};expected={actors[n].get_name() for n in ['V2_Ground','V2_House_Forecourt','V2_Path_VillageLoop','V2_Path_NorthLoop']};assert changed==expected,(changed,expected)
# Deep compare each original actor: only the explicitly listed material slots may differ.
import copy
for k in changed:
 b=copy.deepcopy(before['actors'][k]);a=copy.deepcopy(after['actors'][k]);
 for row in [a,b]:
  for comp in row['components']:
   if 'materials' in comp:comp['materials']=[]
 assert a==b,k
assert before['world_settings']==after['world_settings'];assert len(after['actors'])-len(before['actors'])==6
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2')
(S/'ArtChanges.json').write_text(json.dumps({'bounded_region_cm':[-4620,-3560,-720,1190],'material_changes':changes,'new_materials':newm,'groups':groups,'existing_actors_changed_only_material_slots':sorted(changed),'new_actor_count':6,'new_instance_count':sum(len(g['instances']) for g in groups)},indent=2));(S/'AfterScene.json').write_text(json.dumps(after,indent=2));unreal.log('WORLD_ART_HEALING_HOUSE_SAVED')
