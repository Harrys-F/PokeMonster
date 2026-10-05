"""One-time visual quality pass, furniture clearance fixes and reusable ground.
No gameplay/camera/cutaway configuration changes. Original asset files preserved.
"""
import unreal,json,math,random
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();H='/Game/Environment/HealingHouse/QualityV2';W='/Game/Environment/Westland/NaturalGroundV1';OUT=ROOT/'Saved/HealingQualityV2';OUT.mkdir(parents=True,exist_ok=True)
e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();world=e.get_editor_world();assert world.get_name()=='Dev_HealingHouseTestMap'
actorlib=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);allactors=actorlib.get_all_level_actors();by={a.get_actor_label():a for a in allactors};assert 'HH_Q2_GrassInstances' not in by,'Already applied; do not rebuild the map'
cut=by['HouseCutaway'];occ=list(cut.get_editor_property('occluding_actors'));healer=by['HouseHealer'].get_actor_transform();lib=unreal.MaterialEditingLibrary
def wire(source,output,destination,input_name):
 assert lib.connect_material_expressions(source,output,destination,input_name),(source.get_name(),destination.get_name(),input_name)

assert all(unreal.load_asset(H+'/Meshes/SM_HH_Q2_'+n) for n in ['FloorTile2m','CounterStepped','Fireplace','Bench','StoneWainscot2m','Pillow','Coverlet']), 'Complete import before dressing'
materials={k:unreal.load_asset(H+'/Materials/M_HH_Q2_'+k) for k in ['Wood','WoodLight','WoodDark','Timber','Stone','Plaster','Sage','Linen']};assert all(materials.values())
# Art-only material overrides on retained interior actors; no front-fade replacement.
for a in allactors:
 if isinstance(a,unreal.StaticMeshActor) and 19400<a.get_actor_location().x<20700 and a not in occ:
  c=a.static_mesh_component
  for i,m in enumerate(c.get_materials()):
   key=m.get_name().split('_')[-1] if m else ''
   if key in materials:c.set_material(i,materials[key])
  name=c.static_mesh.get_name().removeprefix('SM_HH_Art_') if c.static_mesh else ''
  if name in ['FloorTile2m','CounterStepped','Fireplace','Bench','StoneWainscot2m','Pillow']:
   collision=c.get_collision_enabled();profile=c.get_collision_profile_name();c.set_static_mesh(unreal.load_asset(H+'/Meshes/SM_HH_Q2_'+name));c.set_collision_profile_name(profile);c.set_collision_enabled(collision)
  if a.get_actor_label().startswith('HH_Art_Floor_'):
   c.set_material(0,materials[['Wood','WoodLight','WoodDark'][sum(map(ord,a.get_actor_label()))%3]])
# Move furniture and all attached stock together, preserving functional actors.
shift={}
def move_group(names,delta):
 for a in allactors:
  if any(a.get_actor_label()==n or (n.endswith('*') and a.get_actor_label().startswith(n[:-1])) for n in names):
   old=a.get_actor_location();a.add_actor_world_offset(unreal.Vector(*delta),False,False);shift[a.get_actor_label()]={'old_cm':[old.x,old.y,old.z],'new_cm':[a.get_actor_location().x,a.get_actor_location().y,a.get_actor_location().z]}
move_group(['HH_V3_HerbShelf','HH_V3_ShelfVial*','HH_V3_ShelfHerb*','HH_Art_HerbShelfStock*'],[-105,55,0])
move_group(['HH_Art_RearApothecary_0','HH_Art_RearStock_0*'],[-60,60,0])
move_group(['HH_Art_RearApothecary_1','HH_Art_RearStock_1*'],[-60,-125,0])
def spawn(label,mesh,position,yaw=0,scale=(1,1,1)):
 a=actorlib.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*position),unreal.Rotator(yaw=yaw));a.set_actor_label('HH_Q2_'+label);a.set_folder_path('HealingHouse/QualityV2');a.tags=['HealingHouse_QualityV2'];a.set_actor_scale3d(unreal.Vector(*scale));c=a.static_mesh_component;c.set_static_mesh(mesh);c.set_collision_profile_name('NoCollision');c.set_editor_property('cast_shadow',False);return a
cover=unreal.load_asset(H+'/Meshes/SM_HH_Q2_Coverlet')
spawn('CoverletSmall',cover,(19955,415,64),scale=(.92,.95,1));spawn('CoverletLarge',cover,(20165,415,64),scale=(1.25,1.25,1))
# Softer contact definition, kept strictly inside the existing local volume.
pp=by['HH_Art_InteriorLighting'];s=pp.get_editor_property('settings')
for k,v in {'auto_exposure_bias':-.55,'ambient_occlusion_intensity':.80,'ambient_occlusion_radius':60}.items():s.set_editor_property(k,v)
pp.set_editor_property('settings',s)
for name,intensity in [('Fire',11),('Waiting',3),('Reception',4),('Treatment',3)]:
 c=by['HH_Art_Light_'+name].point_light_component;c.set_editor_property('intensity',intensity);c.set_editor_property('source_radius',65)
# Retain collision ground unchanged, replace only its visual material.
grass=unreal.load_asset(W+'/Materials/M_WL_NG_Grass');earth=unreal.load_asset(W+'/Materials/M_WL_NG_Earth');by['Ground'].static_mesh_component.set_material(0,grass)
# Old geometric path stays as a hidden, non-colliding fallback actor.
a=by['ApproachPath'];a.static_mesh_component.set_visibility(False);a.set_actor_hidden_in_game(True)
# Opaque painted ground/earth blend, avoiding translucent edge/ordering costs.
tools=unreal.AssetToolsHelpers.get_asset_tools();path=W+'/Materials/M_WL_NG_PathBlend';m=unreal.load_asset(path) or tools.create_asset('M_WL_NG_PathBlend',W+'/Materials',unreal.Material,unreal.MaterialFactoryNew());lib.delete_all_material_expressions(m)
pos=lib.create_material_expression(m,unreal.MaterialExpressionWorldPosition,-1000,0);uv=lib.create_material_expression(m,unreal.MaterialExpressionTextureCoordinate,-1000,700);samples=[]
for n,scale,y in [('Grass',1/190,200),('Earth',1/220,450)]:
 mask=lib.create_material_expression(m,unreal.MaterialExpressionComponentMask,-840,y);mask.set_editor_property('r',True);mask.set_editor_property('g',True);wire(pos,'',mask,'');mul=lib.create_material_expression(m,unreal.MaterialExpressionMultiply,-690,y);mul.set_editor_property('const_b',scale);wire(mask,'',mul,'A');t=lib.create_material_expression(m,unreal.MaterialExpressionTextureSample,-550,y);t.texture=unreal.load_asset(W+'/Textures/T_WL_Painted'+n);t.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_COLOR);wire(mul,'',t,'UVs');samples.append(t)
f=lib.create_material_expression(m,unreal.MaterialExpressionCustom,-200,100);f.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT3)
inputs=[]
for n in ['G','D','P','UV']:
 i=unreal.CustomInput();i.set_editor_property('input_name',n);inputs.append(i)
f.set_editor_property('inputs',inputs);f.set_editor_property('code','float irregular=sin(P.x*.027+sin(P.y*.04))*.035+sin(P.x*.073)*.018;float edge=abs(UV.y*2-1)+irregular;float a=1-smoothstep(.65,.99,edge);float ends=smoothstep(0,.035,UV.x)*(1-smoothstep(.965,1,UV.x));float wear=1-.08*(1-saturate(edge));return lerp(lerp(G,dot(G,float3(.299,.587,.114)),.25)*float3(.66,.72,.62),D*float3(.86,.80,.73)*wear,a*ends);')
for source,pin,name in [(samples[0],'RGB','G'),(samples[1],'RGB','D'),(pos,'','P'),(uv,'','UV')]:wire(source,pin,f,name)
lib.connect_material_property(f,'',unreal.MaterialProperty.MP_BASE_COLOR);r=lib.create_material_expression(m,unreal.MaterialExpressionConstant,0,300);r.r=.88;lib.connect_material_property(r,'',unreal.MaterialProperty.MP_ROUGHNESS);lib.recompile_material(m);unreal.EditorAssetLibrary.save_asset(path,False)
# Dense enough contour sampling for organic width, flat existing walk plane.
pts=[]
for i in range(73):
 t=i/72;x=-1920+1430*t;y=35*math.sin(t*math.pi*3)*(1-t);width=230*(1+.13*math.sin(t*11)+.07*math.cos(t*23));pts.append((x,y,width))
vs=[];uvs=[];tris=[]
for i,(x,y,width) in enumerate(pts):
 for j in range(9):
  v=j/8;vs.append(unreal.Vector(x,y+(v*2-1)*width/2,1.4));uvs.append(unreal.Vector2D(i/72,v))
  if i and j:
   a=(i-1)*9+j-1;b=i*9+j-1;tris.extend([unreal.IntVector(a,b+1,b),unreal.IntVector(a,a+1,b+1)])
buf=unreal.GeometryScriptSimpleMeshBuffers();buf.vertices=vs;buf.triangles=tris;buf.uv0=uvs;dm=unreal.DynamicMesh();unreal.GeometryScript_MeshEdits.append_buffers_to_mesh(dm,buf);unreal.GeometryScript_Normals.recompute_normals(dm,unreal.GeometryScriptCalculateNormalsOptions());opt=unreal.GeometryScriptCreateNewStaticMeshAssetOptions();opt.enable_collision=False;opt.enable_nanite=False;opt.enable_recompute_normals=True
sm,result=unreal.GeometryScript_NewAssetUtils.create_new_static_mesh_asset_from_mesh(dm,W+'/Meshes/SM_WL_NG_HealingApproach',opt);assert sm;sm.set_material(0,m);unreal.EditorAssetLibrary.save_loaded_asset(sm,False);spawn('OrganicApproach',sm,(0,0,0))
# Native component serialization via SubobjectDataSubsystem, no new gameplay class.
a=actorlib.spawn_actor_from_class(unreal.Actor,unreal.Vector(0,0,0));a.set_actor_label('HH_Q2_GrassInstances');a.set_folder_path('HealingHouse/QualityV2/Ground');a.tags=['HealingHouse_QualityV2'];sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);root=sub.k2_gather_subobject_data_for_instance(a)[0];components={}
for name in ['GrassSmall','GrassMedium','GrassLarge','MeadowHerbs','PebbleSmall','PebbleCluster']:
 params=unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True);handle,reason=sub.add_new_subobject(params);c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle));assert isinstance(c,unreal.HierarchicalInstancedStaticMeshComponent),(name,str(reason));c.set_static_mesh(unreal.load_asset(W+'/Meshes/SM_WL_NG_'+name));c.set_collision_profile_name('NoCollision');c.set_editor_property('cast_shadow',False);c.set_editor_property('instance_start_cull_distance',3200);c.set_editor_property('instance_end_cull_distance',4300);c.set_editor_property('component_tags',['WestlandNaturalGround',name]);components[name]=c
rng=random.Random(10526);placements=[]
def place(name,x,y,z=1):
 scale=rng.uniform(.72,1.18);tr=unreal.Transform(location=unreal.Vector(x,y,z),rotation=unreal.Rotator(yaw=rng.uniform(0,360)),scale=unreal.Vector(scale,scale,scale*rng.uniform(.8,1.12)));components[name].add_instance(tr,True);placements.append({'prop':name,'position_cm':[x,y,z],'scale':scale})
# Cluster distribution along path edges, frontage plants and low traffic banks.
for i,(x,y,width) in enumerate(pts[3:-5:2]):
 for side in [-1,1]:
  for j in range(rng.randint(2,4)):
   xx=x+rng.uniform(-38,38);yy=y+side*(width/2+rng.uniform(14,105));name=rng.choices(['GrassSmall','GrassMedium','GrassLarge'],[5,4,1])[0];place(name,xx,yy)
  if i%4==0:place('MeadowHerbs',x+rng.uniform(-35,35),y+side*(width/2+90))
  if i%5==0:place('PebbleSmall',x+rng.uniform(-25,25),y+side*(width/2-10))
for cx,cy in [(-1120,-425),(-705,-430),(-915,445),(-550,620),(-400,550),(-310,-650),(-80,610),(220,535)]:
 for j in range(12):
  x=cx+rng.uniform(-95,95);y=cy+rng.uniform(-60,60)
  if abs(x)<490 and abs(y)<515:continue
  place(rng.choice(['GrassSmall','GrassMedium','MeadowHerbs']),x,y)
 place('PebbleCluster',cx+rng.uniform(-40,40),cy+rng.uniform(-30,30))
assert list(cut.get_editor_property('occluding_actors'))==occ and by['HouseHealer'].get_actor_transform()==healer
assert cut.get_editor_property('interior_camera_distance')==2600 and cut.get_editor_property('interior_camera_pitch')==-50
unreal.EditorLoadingAndSavingUtils.save_map(world,'/Game/Maps/Dev_HealingHouseTestMap')
(OUT/'Placement.json').write_text(json.dumps({'furniture_moves':shift,'ground_instances':placements,'hism_counts':{n:c.get_instance_count() for n,c in components.items()},'path_triangles':len(tris),'camera_cutaway_gameplay_unchanged':True},indent=2))
source=ROOT/'Art/Environment/Westland/NaturalGroundV1';(source/'HealingApproachLayout.json').write_text(json.dumps({'schema':'Westland.NaturalGround.v1','units':'cm','seed':10526,'path':pts,'instances':placements,'culling_cm':[3200,4300],'collision':'none; retained original Ground authoritative'},indent=2))
unreal.log('ART_QUALITY_V2_DRESSED')
