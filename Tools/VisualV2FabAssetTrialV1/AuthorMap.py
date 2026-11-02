"""Bounded six-area VisualV2 trial. All original/library assets and gameplay actors preserved."""
import unreal,json,math,random,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2FabAssetTrialV1';ROOT='/Game/Environment/VisualV2FabAssetTrialV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);W=E.get_editor_world();ML=unreal.MaterialEditingLibrary;assert W.get_name()=='Dev_TestMap_VisualV2'and not E.get_game_world();assert all(x.get_path_name()=='/Game/Maps/Dev_TestMap_VisualV2'for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages())and all(x.get_path_name().startswith(ROOT+'/')for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages());assert not(D/'Authored.json').exists();assert not any(a.actor_has_tag('VisualV2FabAssetTrialV1')for a in A.get_all_level_actors()),'Trial already authored in this map';actors={a.get_actor_label():a for a in A.get_all_level_actors()};rng=random.Random(261102);groups={};SUB=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);changes=[]
def segment(x,y,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/max(1,dx*dx+dy*dy)));return math.hypot(x-a[0]-t*dx,y-a[1]-t*dy)
paths=json.loads((R/'Tools/VisualV2FabAssetTrialV1/ExistingPaths.json').read_text());segments=[]
for ps in paths.values():segments.extend(zip(ps,ps[1:]))
protected=[a.get_actor_location()for a in actors.values()if isinstance(a,(unreal.PokeMonsterNPC,unreal.PokeMonsterRestPoint,unreal.PokeMonsterWorldItem))]
barriers=[a for a in actors.values()if a.actor_has_tag('BiomePlayerWaterBarrier')]
def safe(x,y,margin=40):
 if not(-5750<x<2600 and -3000<y<2900):return False
 if min(segment(x,y,a,b)for a,b in segments)<180+margin:return False
 if math.hypot((x-720)/1000,(y+1800)/740)<1:return False
 if min(segment(x,y,(-910,-320),(1100,-320)),segment(x,y,(720,-320),(720,-680)))<100+margin:return False
 if math.hypot((x+3100)/750,(y-500)/650)<1 or math.hypot((x+2750)/850,(y+1020)/600)<1:return False
 return not any(math.hypot(x-p.x,y-p.y)<140+margin for p in protected)
def ground(x,y):
 # Only the actual target terrain; decorative surfaces must not influence planting.
 c=actors['V2_Ground'].static_mesh_component;hit=unreal.SystemLibrary.line_trace_single(W,unreal.Vector(x,y,600),unreal.Vector(x,y,-600),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,True,barriers,unreal.DrawDebugTrace.NONE);s=hit.export_text() if hit else '';m=re.search(r'ImpactPoint=\(X=[^,]+,Y=[^,]+,Z=([^\)]+)',s);return float(m[1])if m else 0.
def group(label,path,mat=None,shadow=False,cull=5500):
 if label in groups:return groups[label]
 mesh=unreal.load_asset(path);assert mesh,path;mats=[unreal.load_asset(mat)]if mat else[x.material_interface for x in mesh.static_materials];a=A.spawn_actor_from_class(unreal.Actor,unreal.Vector());a.set_actor_label('FAT_'+label);a.set_folder_path('VisualV2/FabAssetTrialV1');a.tags=['VisualV2FabAssetTrialV1'];h,reason=SUB.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=SUB.k2_gather_subobject_data_for_instance(a)[0],new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h));assert c,reason
 for i in range(len(mesh.static_materials)):c.set_material(i,mats[min(i,len(mats)-1)])
 c.set_static_mesh(mesh);c.set_collision_profile_name('NoCollision');c.set_editor_property('generate_overlap_events',False);c.set_cast_shadow(shadow);c.set_editor_property('affect_distance_field_lighting',False);c.set_cull_distances(cull-1000,cull);groups[label]=c;return c
def put(c,x,y,height,yaw=None,z=None):
 b=c.static_mesh.get_bounding_box();s=height/max(1,b.max.z-b.min.z);zz=ground(x,y)if z is None else z;c.add_instance(unreal.Transform(location=unreal.Vector(x,y,zz-b.min.z*s-.7),rotation=unreal.Rotator(yaw=rng.uniform(0,360)if yaw is None else yaw),scale=unreal.Vector(s,s,s)),True)
# Local derivative creates a shallow bed only under the existing masked stream.
g=actors['V2_Ground'];src=unreal.load_asset('/Game/Environment/PokemonAIV3/Meshes/SM_AIV3PondGround');mesh=unreal.load_asset(ROOT+'/Meshes/SM_FAT_StreamGround')if unreal.EditorAssetLibrary.does_asset_exist(ROOT+'/Meshes/SM_FAT_StreamGround')else unreal.EditorAssetLibrary.duplicate_asset(src.get_path_name(),ROOT+'/Meshes/SM_FAT_StreamGround');assert mesh;dm,res=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(src,unreal.DynamicMesh(),unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());_,vs,gaps=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(dm,True);vs=unreal.GeometryScript_List.convert_vector_list_to_array(vs);count=0
for idx,p in enumerate(vs):
 if p.z < -100:continue
 d=min(segment(p.x,p.y,(-910,-320),(1100,-320)),segment(p.x,p.y,(720,-320),(720,-680)))
 if d<61:
  w=max(0,min(1,(61-d)/25));p.z-=34*w*w*(3-2*w);vs[idx]=p;count+=1
unreal.GeometryScript_MeshEdits.set_all_mesh_vertex_positions(dm,unreal.GeometryScript_List.convert_array_to_vector_list(vs));opt=unreal.GeometryScriptCopyMeshToAssetOptions();opt.enable_recompute_normals=True;unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(dm,mesh,opt,unreal.GeometryScriptMeshWriteLOD());mesh.get_editor_property('body_setup').set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);mesh.set_material(0,unreal.load_asset(ROOT+'/Materials/M_FAT_Ground'));assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,False);g.modify();g.static_mesh_component.set_static_mesh(mesh);g.static_mesh_component.set_material(0,unreal.load_asset(ROOT+'/Materials/M_FAT_Ground'));changes.append(dict(actor=g.get_name(),kind='local ground/material and shallow stream bed',vertices=count))
for label in ['V2_Path_Main','V2_Path_Wild','V2_Path_VillageLoop','V2_Path_NorthLoop','V2_Path_Cottage']:
 a=actors[label];a.modify();a.static_mesh_component.set_material(0,unreal.load_asset(ROOT+'/Materials/M_FAT_Path'));changes.append(dict(actor=a.get_name(),kind='local textured path material'))
# Reuse original stream shape/normal/time expressions, add physically lit volume.
m=unreal.load_asset(ROOT+'/Materials/M_FAT_Stream')if unreal.EditorAssetLibrary.does_asset_exist(ROOT+'/Materials/M_FAT_Stream')else unreal.EditorAssetLibrary.duplicate_asset('/Game/Environment/PokemonAIV3/Materials/M_AIV3RiverConnection',ROOT+'/Materials/M_FAT_Stream');assert m;m.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_SINGLE_LAYER_WATER);m.set_editor_property('blend_mode',unreal.BlendMode.BLEND_MASKED);wet=next(n for n in ML.get_material_expressions(m)if isinstance(n,unreal.MaterialExpressionCustom)and'float wet='in n.get_editor_property('code'));mask=ML.create_material_expression(m,unreal.MaterialExpressionComponentMask);mask.set_editor_property('r',False);mask.set_editor_property('g',False);mask.set_editor_property('b',False);mask.set_editor_property('a',True);assert ML.connect_material_expressions(wet,'',mask,'');assert ML.connect_material_property(mask,'',unreal.MaterialProperty.MP_OPACITY_MASK)
def scalar(v,prop):
 n=ML.create_material_expression(m,unreal.MaterialExpressionConstant);n.r=v;assert ML.connect_material_property(n,'',prop)
def vector(v):
 n=ML.create_material_expression(m,unreal.MaterialExpressionConstant3Vector);n.set_editor_property('constant',unreal.LinearColor(*v,1));return n
assert ML.connect_material_property(vector((.018,.035,.026)),'',unreal.MaterialProperty.MP_BASE_COLOR);scalar(.23,unreal.MaterialProperty.MP_OPACITY);scalar(.17,unreal.MaterialProperty.MP_ROUGHNESS);scalar(.5,unreal.MaterialProperty.MP_SPECULAR);sl=ML.create_material_expression(m,unreal.MaterialExpressionSingleLayerWaterMaterialOutput)
for pin,v in [('ScatteringCoefficients',(.0006,.0014,.001)),('AbsorptionCoefficients',(.004,.0018,.0012)),('ColorScaleBehindWater',(.95,.99,.96))]:assert ML.connect_material_expressions(vector(v),'',sl,pin)
n=ML.create_material_expression(m,unreal.MaterialExpressionConstant);n.r=.3;ML.connect_material_expressions(n,'',sl,'PhaseG');ML.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);a=actors['P2D_OrganicWater'];a.modify();a.static_mesh_component.set_material(0,m);changes.append(dict(actor=a.get_name(),kind='local masked Single Layer Water, unchanged river footprint'))
# Actual rock pack pebbles are centimetres, not giant boulders.
for i in range(360):
 x=rng.uniform(-850,1040);y=-320+rng.uniform(-48,48)
 if -500<x<-200:continue
 key=str(i%7+1);c=group('StreamPebbles_'+key,'/Game/RockEnv_Pack/Meshes/Small_Rocks/SM_Small_Rock_'+key);put(c,x,y,rng.uniform(3,8),z=-30)
for i in range(95):
 x=rng.uniform(-950,1110);y=-320+rng.choice([-1,1])*rng.uniform(78,112)
 if -550<x<-200:continue
 key=str(i%7+1);c=group('BankPebbles_'+key,'/Game/RockEnv_Pack/Meshes/Small_Rocks/SM_Small_Rock_'+key);put(c,x,y,rng.uniform(4,10),z=0)
# Irregular islands, two grass families, four colourful clumps plus real Fab poppies.
style='/Game/StyleHex_Studio/Free_Packs/FREE_Stylized_Grass_Flowers_Foliage/Meshes/'
for zone,cx,cy,rx,ry,num in [('Meadow',-4500,-2300,1000,520,1800),('Habitat',-2100,1450,440,280,420),('ForestEdge',-4800,1500,550,1000,700)]:
 for i in range(num):
  x=cx+rng.uniform(-rx,rx);y=cy+rng.uniform(-ry,ry)
  if not safe(x,y,0):continue
  # Preserve distinct free patches instead of uniform carpet coverage.
  if math.sin(x*.009+math.sin(y*.005))*math.cos(y*.008)<-.18:continue
  k=i%11
  if zone=='ForestEdge'and k<7:
   key='A'if i%2 else'B';c=group('FabFern'+key,'/Game/Fab/VisualV2TrialLocal/Plants/SM_FAT_Fern'+key);h=rng.uniform(35,80)
  elif k<6:
   key=str(i%3+1);c=group('Grass'+key,style+'SM_Fol_Grass_Clump_'+key,ROOT+'/Materials/MI_FAT_Grass');h=rng.uniform(25,48)
  elif k<9:
   key=str(i%4+1);c=group('Flowers'+key,style+'SM_Fol_Flower_Clump_'+key,ROOT+'/Materials/MI_FAT_Flowers');h=rng.uniform(28,48)
  else:
   key='A'if i%2 else'B';c=group('FabPoppy'+key,'/Game/Fab/VisualV2TrialLocal/Plants/SM_FAT_Poppy'+key);h=rng.uniform(40,68)
  put(c,x,y,h)
# Bush margins keep the existing canopies and clear the habitat's centre.
for i in range(55):
 x=-4900+rng.uniform(-500,500);y=1450+rng.uniform(-950,950)
 if safe(x,y,65):c=group('FabShrubs',style+'SM_Fol_Bush_1',ROOT+'/Materials/MI_FAT_Flowers');put(c,x,y,rng.uniform(65,105))
# Small rock outcrop outside the established path, no new impassable wall.
for i in range(22):
 x=-1100+rng.gauss(0,290);y=1250+rng.gauss(0,230)
 if not safe(x,y,70):continue
 key=str(i%3+1);c=group('Outcrop'+key,'/Game/RockEnv_Pack/Meshes/Jungle_Rocks/SM_Jungle_Rock_'+key,shadow=True,cull=8000);put(c,x,y,rng.uniform(50,120))
# Reorder the five existing isolated fences into one coherent herb garden.
fence_changes=[]
for i,(x,y,yaw)in enumerate([(-4700,-180,90),(-4700,60,90),(-4700,300,90),(-4580,-300,0),(-4580,420,0)]):
 a=actors['V2_Fence_'+str(i)];old=a.get_actor_location().to_tuple();a.modify();a.set_actor_location(unreal.Vector(x,y,0),False,False);a.set_actor_rotation(unreal.Rotator(yaw=yaw),False);fence_changes.append(dict(actor=a.get_name(),before=old,after=[x,y,0]));changes.append(dict(actor=a.get_name(),kind='coherent herb-garden fence'))
for i in range(80):
 x=rng.uniform(-4630,-4420);y=rng.uniform(-240,350);c=group('GardenFlowers',style+'SM_Fol_Flower_Clump_2',ROOT+'/Materials/MI_FAT_Flowers');put(c,x,y,rng.uniform(22,35))
# All small decorative vegetation/pebbles are explicitly non-blocking.
assert all(c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION for c in groups.values());assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages(),'Never save changed library originals';assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2')
(D/'Authored.json').write_text(json.dumps(dict(changes=changes,fences=fence_changes,groups=[dict(name=k,count=c.get_instance_count(),mesh=c.static_mesh.get_path_name(),materials=[c.get_material(i).get_path_name()for i in range(c.get_num_materials())],collision=str(c.get_collision_enabled()))for k,c in groups.items()],preserved_global_population_limit=14,gameplay_or_habitat_edits=False),indent=2))
