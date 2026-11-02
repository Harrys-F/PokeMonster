"""Map-local grounded grass pockets and restrained forest-floor blending."""
import unreal,json,sys,random,math,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualUpgradeV1';sys.path.insert(0,str(R/'Tools'));import WestlandRegionLayout as L
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);S=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);M=unreal.MaterialEditingLibrary;assert W.get_name()=='Dev_WestlandRegion'and not E.get_game_world();assert not(D/'PolishAudit.json').exists()
tex=unreal.load_asset('/Game/Environment/WestlandVisualUpgradeV1/Textures/T_WVU_ForestCoverage');task=unreal.AssetImportTask();task.filename=str(R/'Art/World/WestlandVisualUpgradeV1/ForestCoverage.png');task.destination_path='/Game/Environment/WestlandVisualUpgradeV1/Textures';task.destination_name='T_WVU_ForestCoverage';task.automated=True;task.replace_existing=True;task.save=False;unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task]);tex.set_editor_property('srgb',False);tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS);assert unreal.EditorAssetLibrary.save_loaded_asset(tex,False)
for key in ['Grass','PathBlend']:
 m=unreal.load_asset('/Game/Environment/WestlandVisualUpgradeV1/Materials/M_WVU_'+key)
 for node in M.get_material_expressions(m):
  if isinstance(node,unreal.MaterialExpressionCustom):
   code=node.get_editor_property('code')
   if 'float3 forestEarth=d*lerp' in code:
    code=code.replace('float3 forestEarth=d*lerp(float3(.60,.65,.51),float3(.78,.72,.57),litter);','float earthLuma=dot(d,float3(.299,.587,.114));float3 forestEarth=lerp(d,earthLuma.xxx,.62)*lerp(float3(.49,.61,.45),float3(.65,.70,.52),litter);').replace('forest*.80','forest*.70');node.set_editor_property('code',code)
 M.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
actors=list(A.get_all_level_actors());assert not any(a.get_actor_label().startswith('WVU_DetailGrass')for a in actors);barriers=[a for a in actors if a.actor_has_tag('BiomePlayerWaterBarrier')];protected=[L.en(a.get_actor_location().x,a.get_actor_location().y)for a in actors if isinstance(a,(unreal.PokeMonsterNPC,unreal.PokeMonsterWorldItem,unreal.PokeMonsterRestPoint))];grid={};rng=random.Random(2111026)
paths=[]
for _,points,width in L.PATHS:
 for e,n in L.sample(points,spacing=5):grid.setdefault((int(e//10),int(n//10)),[]).append((e,n,width));paths.append((e,n,width))
def safe(e,n):
 if abs(e-L.river(n))<7.5:return False
 for x in range(int(e//10)-1,int(e//10)+2):
  for y in range(int(n//10)-1,int(n//10)+2):
   if any(math.hypot(e-u,n-v)<w*.5+.55 for u,v,w in grid.get((x,y),[])):return False
 for b in L.buildings():
  if abs(e-b['place'][0])<b['size'][1]/2+3 and abs(n-b['place'][1])<b['size'][0]/2+3:return False
 return not any(math.hypot(e-u,n-v)<3.2 for u,v in protected)
def ground(x,y,z):
 hit=unreal.SystemLibrary.line_trace_single(W,unreal.Vector(x,y,z+2500),unreal.Vector(x,y,z-4000),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,barriers,unreal.DrawDebugTrace.NONE)
 if not hit:return None
 match=re.search(r'ImpactPoint=\(X=[^,]+,Y=[^,]+,Z=([^\)]+)',hit.export_text());return float(match[1])if match else None
clusters=[]
for i,(e,n,w)in enumerate(paths):
 if i%2:continue
 for side in [-1,1]:clusters.append((e+side*(w*.5+1.4),n,1.5,18))
for i in range(450):clusters.append((rng.uniform(-380,380),rng.uniform(-280,280),rng.uniform(1.2,3),rng.randint(14,28)))
mat=unreal.load_asset('/Game/Environment/VisualV2EnvironmentV3/Materials/M_EQ3_Grass');assert mat.get_editor_property('used_with_instanced_static_meshes');groups={};rows=[]
for key in ['Short','Meadow','Woodland']:
 a=A.spawn_actor_from_class(unreal.Actor,unreal.Vector());a.set_actor_label('WVU_DetailGrass_'+key);a.set_folder_path('WestlandRegion/VisualUpgradeV1');a.tags=['WestlandVisualUpgradeV1','VisualOnly_NoCollision'];root=S.k2_gather_subobject_data_for_instance(a)[0];handle,why=S.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle));assert c,why;c.set_material(0,mat);c.set_static_mesh(unreal.load_asset('/Game/Environment/VisualV2EnvironmentV3/Meshes/SM_EQ3_Grass'+key));c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False);c.set_editor_property('affect_distance_field_lighting',False);c.set_cull_distances(5000,6500);groups[key]=c
for ce,cn,r,count in clusters:
 for i in range(count):
  e=ce+rng.gauss(0,r*.6);n=cn+rng.gauss(0,r*.6)
  if not safe(e,n):continue
  x,y,z=L.world(e,n,L.height(e,n));g=ground(x,y,z)
  if g is None:continue
  key=rng.choices(['Short','Meadow','Woodland'],[.5,.33,.17])[0];sc=rng.uniform(.9,1.45);groups[key].add_instance(unreal.Transform(location=unreal.Vector(x,y,g-.4),rotation=unreal.Rotator(yaw=rng.uniform(0,360)),scale=unreal.Vector(sc,sc,sc)),True)
for key,c in groups.items():rows.append(dict(group=key,instances=c.get_instance_count(),collision='NoCollision',shadow=False))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_WestlandRegion');(D/'PolishAudit.json').write_text(json.dumps(dict(groups=rows,coverage='soft grouped ground cover; no global settings changed'),indent=2));unreal.log('WESTLAND_VISUAL_POLISH_SAVED')
