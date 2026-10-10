"""Additive staged region authoring. Saves only own map/assets. No design-doc changes.
Run in full UE through the existing Python console. Phase from Saved/WestlandRegion/Job.json.
Building kit and illustrated assets are read-only. Owned map starts as a copy of HealingHouse,
retaining its complete working relocated interior, rest/checkpoint/save and cutaway references.
"""
import unreal,math,json,random,sys,time,runpy
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();sys.dont_write_bytecode=True;sys.path.insert(0,str(ROOT/'Tools'))
import WestlandRegionLayout as L
import importlib;importlib.reload(L)
OUT=ROOT/'Saved/WestlandRegion';DEST=L.ASSETS;TAG=L.TAG
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
CACHE={};BUILDINGS=L.buildings();PATHS=[(n,L.sample(p),w) for n,p,w in L.PATHS]
def load(p):
 if p not in CACHE:CACHE[p]=unreal.load_asset(p);assert CACHE[p],p
 return CACHE[p]
def spawn(cls,label,p,yaw=0,folder='Terrain'):
 a=A.spawn_actor_from_class(cls,(p if isinstance(p,unreal.Vector) else unreal.Vector(*p)),unreal.Rotator(yaw=yaw));assert a,label
 a.set_actor_location(p if isinstance(p,unreal.Vector) else unreal.Vector(*p),False,False);a.set_actor_label('WR_'+label);a.set_folder_path('WestlandRegion/'+folder);a.tags=[TAG];return a
def mesh_actor(label,mesh,p,yaw=0,collision=False,scale=None,mat=None,folder='Terrain'):
 a=spawn(unreal.StaticMeshActor,label,p,yaw,folder);c=a.static_mesh_component;c.set_static_mesh(mesh);c.set_cast_shadow(False);c.set_collision_profile_name('BlockAll' if collision else 'NoCollision');c.set_editor_property('generate_overlap_events',False)
 if collision:c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_IGNORE)
 if scale:a.set_actor_scale3d(unreal.Vector(*scale))
 if mat:c.set_material(0,mat)
 return a

def newmesh(name,vs,tri,uv,mat,collision=False):
 path=DEST+'/Meshes/'+name;assert not unreal.EditorAssetLibrary.does_asset_exist(path),path+' already exists; use saved map, never overwrite shared assets'
 buf=unreal.GeometryScriptSimpleMeshBuffers();buf.vertices=[unreal.Vector(*v) for v in vs];buf.triangles=[unreal.IntVector(t[0],t[2],t[1]) for t in tri];buf.uv0=[unreal.Vector2D(*v) for v in uv]
 dm=unreal.DynamicMesh();unreal.GeometryScript_MeshEdits.append_buffers_to_mesh(dm,buf);unreal.GeometryScript_Normals.recompute_normals(dm,unreal.GeometryScriptCalculateNormalsOptions())
 opt=unreal.GeometryScriptCreateNewStaticMeshAssetOptions();opt.enable_collision=collision;opt.collision_mode=unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE;opt.enable_nanite=False;opt.enable_recompute_normals=True
 sm,res=unreal.GeometryScript_NewAssetUtils.create_new_static_mesh_asset_from_mesh(dm,path,opt);assert sm,(path,res);sm.set_material(0,mat)
 if collision:
  sm.get_editor_property('body_setup').set_editor_property('double_sided_geometry',True);unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).enable_section_collision(sm,True,0,0)
 assert unreal.EditorAssetLibrary.save_loaded_asset(sm,False);return sm

def material(name,color):
 p=DEST+'/Materials/M_WR_'+name
 if unreal.EditorAssetLibrary.does_asset_exist(p):return load(p)
 m=unreal.AssetToolsHelpers.get_asset_tools().create_asset('M_WR_'+name,DEST+'/Materials',unreal.Material,unreal.MaterialFactoryNew());lib=unreal.MaterialEditingLibrary
 node=lib.create_material_expression(m,unreal.MaterialExpressionConstant3Vector,-300,0);node.constant=unreal.LinearColor(*color,1);lib.connect_material_property(node,'',unreal.MaterialProperty.MP_BASE_COLOR)
 rough=lib.create_material_expression(m,unreal.MaterialExpressionConstant,-300,150);rough.r=.85;lib.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS);lib.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m,False);return m

def path_height(e,n):
 if abs(n+50)<3 and abs(e-L.river(-50))<15:return .05
 if abs(n+235)<2 and abs(e-L.river(-235))<8:return -.08
 return surface(e,n)+.035

def surface(e,n):
 # Match native terrain triangulation at a global 2 m grid; no floating paths.
 e0=math.floor((e+500)/2)*2-500;n0=math.floor((n+400)/2)*2-400
 u=(e-e0)/2;v=(n-n0)/2;a=L.height(e0,n0);b=L.height(e0+2,n0);c=L.height(e0+2,n0+2);d=L.height(e0,n0+2)
 return a+(b-a)*u+(c-b)*v if v<=u else a+(c-d)*u+(d-a)*v

def distance_to_paths(e,n):return min(math.hypot(e-p[0],n-p[1])-w/2 for _,pts,w in PATHS for p in pts[::2])
def free(e,n,pad=0):
 if distance_to_paths(e,n)<pad:return False
 if abs(e-L.river(n))<7+pad:return False
 for b in BUILDINGS:
  if abs(e-b['place'][0])<b['size'][1]/2+3+pad and abs(n-b['place'][1])<b['size'][0]/2+3+pad:return False
 for key,(x,y) in L.PLACES.items():
  if key in ('Heilhaus','Steinkreis','Waldruinen','Ausgang') and math.hypot(e-x,n-y)<16+pad:return False
 return True

def base():
 assert not E.get_game_world(),'Stop PIE'
 if unreal.EditorAssetLibrary.does_asset_exist(L.MAP):
  assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level(L.MAP);
  if any(a.get_actor_label()=='WR_RegionPlayerStart' for a in A.get_all_level_actors()):
   assert any(a.actor_has_tag(TAG) for a in A.get_all_level_actors()),'Map exists but not ours';yield 'existing region loaded';return
 else:
  assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level('/Game/Maps/Dev_HealingHouseTestMap')
  assert unreal.EditorLoadingAndSavingUtils.save_map(E.get_editor_world(),L.MAP)
 actors=list(A.get_all_level_actors());offset=unreal.Vector(*L.world(-310,205,10));r=unreal.Rotator(yaw=-45);inside=unreal.Vector(*L.world(1000,-1000,10));cut=None
 for i,a in enumerate(actors):
  if isinstance(a,unreal.WorldSettings):continue
  p=a.get_actor_location();is_inside=p.x>15000
  q=unreal.MathLibrary.rotate_angle_axis(p, -45, unreal.Vector(0,0,1))
  if is_inside:q=unreal.MathLibrary.rotate_angle_axis(p-unreal.Vector(20000,0,0),-45,unreal.Vector(0,0,1))+inside
  else:q=q+offset
  a.set_actor_location(q,False,False);a.set_actor_rotation(unreal.Rotator(pitch=a.get_actor_rotation().pitch,yaw=a.get_actor_rotation().yaw-45,roll=a.get_actor_rotation().roll),False)
  a.set_folder_path('WestlandRegion/HealingHouse/'+str(a.get_folder_path()));a.tags=list(a.tags)+[TAG,'WR_HealingHouseCopied']
  if a.get_class().get_name()=='PokeMonsterBuildingCutaway':cut=a
  if i%30==0:yield 'Healing House preserved '+str(i)
 assert cut
 area=cut.get_editor_property('relocated_interior_area');area.set_world_location(inside+unreal.Vector(0,0,150),False,False)
 # The relative threshold and camera target remain exactly those of the original room.
 oldstarts=[a for a in actors if isinstance(a,unreal.PlayerStart)]
 for a in oldstarts:
  a.set_actor_location(unreal.Vector(*L.world(-300,-220,.5)),False,False);a.set_actor_label('WR_RegionPlayerStart');a.set_folder_path('WestlandRegion/Start')
 if not oldstarts:spawn(unreal.PlayerStart,'RegionPlayerStart',L.world(-300,-220,.5),folder='Start')
 E.get_editor_world().get_world_settings().set_editor_property('default_game_mode',unreal.PokeMonsterGameMode.static_class())
 (OUT/'HealingCopy.json').write_text(json.dumps({'actors':len(actors),'house_world_cm':[offset.x,offset.y,offset.z],'interior_world_cm':[inside.x,inside.y,inside.z],'source_map':'Dev_HealingHouseTestMap'},default=str,indent=2))
 yield 'region base ready'

def terrain():
 # Own copies preserve shared painted-ground shader assets.
 for n in ['Grass','Earth','PathBlend']:
  target=DEST+'/Materials/M_WR_'+n
  if not unreal.EditorAssetLibrary.does_asset_exist(target):assert unreal.EditorAssetLibrary.duplicate_asset('/Game/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_'+n,target)
 grass=load(DEST+'/Materials/M_WR_Grass');earth=load(DEST+'/Materials/M_WR_PathBlend')
 # 100 m outer backdrop on all four sides; 80 individually editable mesh tiles.
 for tx in range(10):
  for ty in range(8):
   name='SM_WR_Terrain_%02d_%02d'%(tx,ty);p=DEST+'/Meshes/'+name
   if unreal.EditorAssetLibrary.does_asset_exist(p):continue
   e0=-500+tx*100;n0=-400+ty*100;vs=[];uv=[];tri=[]
   for i in range(51):
    for j in range(51):e=e0+i*2;n=n0+j*2;vs.append(L.world(e,n,L.height(e,n)));uv.append((e/2,n/2))
   for i in range(50):
    for j in range(50):a=i*51+j;b=a+51;c=b+1;d=a+1;tri.extend([(a,d,c),(a,c,b)])
   sm=newmesh(name,vs,tri,uv,grass,True);mesh_actor('Terrain_%02d_%02d'%(tx,ty),sm,(0,0,0),collision=True);yield name
 for index,(name,pts,width) in enumerate(PATHS):
  if unreal.EditorAssetLibrary.does_asset_exist(DEST+'/Meshes/SM_WR_Path_'+name):continue
  vs=[];uv=[];tri=[]
  for i,p in enumerate(pts):
   q=pts[max(0,i-1)];r=pts[min(len(pts)-1,i+1)];dx=r[0]-q[0];dy=r[1]-q[1];length=max(.01,math.hypot(dx,dy));w=width*(1+.045*math.sin(i*.2))
   for j in range(5):
    s=j/4*2-1;e=p[0]-dy/length*w/2*s;n=p[1]+dx/length*w/2*s;vs.append(L.world(e,n,path_height(e,n)));uv.append((i/(len(pts)-1),j/4))
    if i and j:a=(i-1)*5+j-1;b=a+5;tri.extend([(a,a+1,b+1),(a,b+1,b)])
  sm=newmesh('SM_WR_Path_'+name,vs,tri,uv,earth);mesh_actor('Path_'+name,sm,(0,0,0),folder='Paths');yield name
 # Water surface follows a monotonic level; the steep reach at N165..185 is a true drop.
 watermat=material('River',(.035,.20,.23));vs=[];uv=[];tri=[]
 for i in range(421):
  n=-420+i*2;e=L.river(n);w=7+.9*math.sin(n/19)
  for j in range(5):vs.append(L.world(e+(j/4*2-1)*w/2,n,L.water(n)));uv.append((j/4,n/8))
  if i:
   for j in range(4):a=(i-1)*5+j;b=a+5;tri.extend([(a,b,b+1),(a,b+1,a+1)])
 sm=newmesh('SM_WR_River',vs,tri,uv,watermat);mesh_actor('WindingRiver',sm,(0,0,0),folder='River');yield 'river'
 # Collision volume coincides with visible water, with openings under each bridge.
 cube=load('/Engine/BasicShapes/Cube')
 for n in range(-300,301,5):
  if abs(n+50)<3 or abs(n+235)<2:continue
  a=mesh_actor('RiverBarrier_'+str(n),cube,L.world(L.river(n),n,L.water(n)+1),-45,True,scale=(5.5,7,2),folder='River/Collision');a.set_actor_hidden_in_game(True)
 yield 'water boundaries'

def buildings():
 # Pure authoring functions from the original Kit proof; no shared map build invoked.
 module=runpy.run_path(str(ROOT/'Tools/BuildWestlandVillageV1.py'),run_name='kit_library');home=module['home']
 kit=json.loads((ROOT/'Art/Architecture/Westland/WestlandBuildingKit_V1.json').read_text())['modules']+json.loads((ROOT/'Art/Architecture/Westland/WestlandBuildingKit_InnExtensions_V1.json').read_text())['modules'];desc={m['name']:m for m in kit}
 for b in BUILDINGS:
  if any(a.get_actor_label()=='WR_'+b['id']+'_Cutaway' for a in A.get_all_level_actors()):continue
  if b['kind']=='inn':
   inn=json.loads((ROOT/'Art/Architecture/Westland/Buildings/WL_Inn_V1.json').read_text());placements=inn['placements'];body=[8,8];door=[-300,-100,107.5];focus=[100,0,150];regions=[{'center':[-100,0,0],'extent':[310,410,200]},{'center':[300,100,0],'extent':[110,310,200]}];width=1.6;doorheight=2.15
  else:
   placements,door,ridge=home(b['size'][0],b['size'][1],1 if b['size'][1]>=6 else 0,'Arch',1)
   body=b['size'];focus=[0,0,150];regions=[];width=1.3;doorheight=2.
  origin=unreal.Vector(*L.world(*b['place'],b['z']));yaw=b['yaw']
  def wp(p):return origin+unreal.MathLibrary.rotate_angle_axis(unreal.Vector(*p),yaw,unreal.Vector(0,0,1))
  occ=[]
  for i,p in enumerate(placements):
   d=desc[p['module']];a=mesh_actor(b['id']+'_'+str(i),load('/Game/Environment/Architecture/Westland/Meshes/'+d['category']+'/'+d['mesh']),wp([v*100 for v in p['position_m']]),yaw+p['yaw'],bool(d['collision_boxes']),folder='Buildings/'+b['id'])
   if p['cutaway']:occ.append(a)
   if i%25==0:yield b['id']+' '+str(i)
  c=spawn(unreal.PokeMonsterBuildingCutaway,b['id']+'_Cutaway',wp(focus),yaw,'Buildings/'+b['id'])
  for prop,value in {'use_interior_camera':True,'interior_camera_distance':2200. if b['kind']=='inn' else 2000.,'interior_camera_pitch':-50.,'interior_camera_yaw_offset':0.,'interior_camera_target':unreal.Vector(0,0,-70),'occluding_actors':occ,'fade_duration':.4}.items():c.set_editor_property(prop,value)
  c.get_editor_property('interior_area').set_box_extent(unreal.Vector(body[0]*50+10,body[1]*50+10,200));th=c.get_editor_property('door_threshold');th.set_relative_location(unreal.Vector(*(door[i]-focus[i] for i in range(3))),False,False);th.set_box_extent(unreal.Vector(20,width*50,doorheight*50))
  if regions:
   rr=[]
   for item in regions:r=unreal.PokeMonsterBuildingInteriorRegion();r.center=unreal.Vector(*item['center']);r.extent=unreal.Vector(*item['extent']);rr.append(r)
   c.set_editor_property('interior_regions',rr)
  yield b['id']+' done'

def import_props():
 for f in sorted((ROOT/'Art/World/WestlandRegion/Exports').glob('*.fbx')):
  if unreal.EditorAssetLibrary.does_asset_exist(DEST+'/Meshes/'+f.stem):continue
  task=unreal.AssetImportTask();task.filename=str(f);task.destination_path=DEST+'/Meshes';task.destination_name=f.stem;task.automated=True;task.save=True;task.replace_existing=False
  ui=unreal.FbxImportUI();ui.import_mesh=True;ui.import_materials=False;ui.import_textures=False;ui.import_as_skeletal=False;ui.static_mesh_import_data.set_editor_property('combine_meshes',True);ui.static_mesh_import_data.set_editor_property('auto_generate_collision',False);task.options=ui
  unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task]);yield f.name
 stone=load('/Game/Environment/Architecture/Westland/Materials/M_WL_Stone');wood=load('/Game/Environment/Architecture/Westland/Materials/M_WL_Wood')
 for n in ['StoneBridge','WoodBridge','Waterwheel','RuinArch','RuinColumn','StandingStone','Crag']:
  sm=load(DEST+'/Meshes/WR_'+n)
  for i in range(len(sm.get_editor_property('static_materials'))):sm.set_material(i,wood if n in ('WoodBridge','Waterwheel') else stone)
  unreal.EditorAssetLibrary.save_loaded_asset(sm,False)
 for label,n,e,north,z,yaw in [('Steinbruecke','StoneBridge',L.river(-50),-50,0,45),('Holzbruecke','WoodBridge',L.river(-235),-235,-.2,45),('Muehlenrad','Waterwheel',138,-230,-4,45)]:
  mesh_actor(label,load(DEST+'/Meshes/WR_'+n),L.world(e,north,z),yaw,folder='Landmarks')
  if 'bruecke' in label:
   length,width=(28,4) if n=='StoneBridge' else (16,2.5)
   mesh_actor(label+'_Deck',load('/Engine/BasicShapes/Cube'),L.world(e,north,z-.16),45,True,scale=(length,width,.25),mat=wood if n=='WoodBridge' else stone,folder='Landmarks/Collision')
   for side in (-1,1):
    a=mesh_actor(label+'_Rail_'+str(side),load('/Engine/BasicShapes/Cube'),L.world(e,north+side*(width/2+.08),z+.5),45,True,scale=(length,.15,1.),folder='Landmarks/Collision');a.set_actor_hidden_in_game(True)
 for i in range(8):
  t=i*math.tau/8;e=-45+7*math.cos(t);n=235+7*math.sin(t);mesh_actor('StandingStone_'+str(i),load(DEST+'/Meshes/WR_StandingStone'),L.world(e,n,18),-45+i*9,folder='Landmarks/Steinkreis')
 for i,(e,n) in enumerate([(219,212),(230,210),(234,200)]):mesh_actor('RuinArch_'+str(i),load(DEST+'/Meshes/WR_RuinArch'),L.world(e,n,12),-45+i*32,folder='Landmarks/Ruins')
 for i in range(8):mesh_actor('RuinColumn_'+str(i),load(DEST+'/Meshes/WR_RuinColumn'),L.world(216+(i%4)*6,195+(i//4)*20,12),-45,folder='Landmarks/Ruins')
 yield 'bridges and ruins'

def instances(label,sm,collision=False,end=6500):
 a=spawn(unreal.Actor,label,(0,0,0),folder='Vegetation');sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);root=sub.k2_gather_subobject_data_for_instance(a)[0]
 p=unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True);h,reason=sub.add_new_subobject(p)
 c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h));assert c,reason;c.set_static_mesh(sm);c.set_collision_profile_name('BlockAll' if collision else 'NoCollision');c.set_editor_property('cast_shadow',False);c.set_editor_property('instance_start_cull_distance',int(end*.85));c.set_editor_property('instance_end_cull_distance',end)
 if collision:c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_IGNORE)
 return c

def card(name,path):
 asset=DEST+'/Meshes/SM_WR_Card_'+name
 if unreal.EditorAssetLibrary.does_asset_exist(asset):return load(asset)
 s=load(path);tex=s.get_editor_property('source_texture');dim=s.get_editor_property('source_dimension');offset=s.get_editor_property('source_uv');pivot=s.get_editor_property('custom_pivot_point');ppu=s.get_editor_property('pixels_per_unreal_unit')
 x0=-pivot.x/ppu;x1=(dim.x-pivot.x)/ppu;z0=(pivot.y-dim.y)/ppu;z1=pivot.y/ppu
 m=unreal.AssetToolsHelpers.get_asset_tools().create_asset('M_WR_Card_'+name,DEST+'/Materials',unreal.Material,unreal.MaterialFactoryNew());m.set_editor_property('blend_mode',unreal.BlendMode.BLEND_MASKED);m.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_UNLIT);m.set_editor_property('two_sided',True)
 lib=unreal.MaterialEditingLibrary;t=lib.create_material_expression(m,unreal.MaterialExpressionTextureSample);t.texture=tex;t.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_COLOR);lib.connect_material_property(t,'RGB',unreal.MaterialProperty.MP_EMISSIVE_COLOR);lib.connect_material_property(t,'A',unreal.MaterialProperty.MP_OPACITY_MASK);lib.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m,False)
 tw=tex.blueprint_get_size_x();th=tex.blueprint_get_size_y();u0=offset.x/tw;u1=(offset.x+dim.x)/tw;v0=offset.y/th;v1=(offset.y+dim.y)/th
 return newmesh('SM_WR_Card_'+name,[(x0,0,z0),(x1,0,z0),(x1,0,z1),(x0,0,z1)],[(0,1,2),(0,2,3)],[(u0,v1),(u1,v1),(u1,v0),(u0,v0)],m)

def dress():
 rng=random.Random(5100926);counts={};parts={}
 for n in ['Oak','Bush','Rock']:
  parts[n]=instances(n,card(n,'/Game/Environment/Prototype2D/Sprites/S_'+n),end=10000 if n=='Oak' else 6000);yield 'card '+n
 for n in ['GrassSmall','GrassMedium','GrassLarge','MeadowHerbs','PebbleSmall','PebbleCluster']:
  parts[n]=instances(n,load('/Game/Environment/Westland/NaturalGroundV1/Meshes/SM_WL_NG_'+n),end=4300)
 parts['Trunks']=instances('TrunkCollision',load('/Engine/BasicShapes/Cylinder'),True,10000)
 wood=load('/Game/Environment/Architecture/Westland/Materials/M_WL_Wood');stone=load('/Game/Environment/Architecture/Westland/Materials/M_WL_Stone')
 parts['Crags']=instances('RockyContours',load(DEST+'/Meshes/WR_Crag'),end=11000)
 def put(k,e,n,s=1,yaw=45,z=None,scale=None):
  parts[k].add_instance(unreal.Transform(location=unreal.Vector(*L.world(e,n,surface(e,n)+.015 if z is None else z)),rotation=unreal.Rotator(yaw=yaw),scale=unreal.Vector(*(scale or (s,s,s)))),True);counts[k]=counts.get(k,0)+1
 # Groves cluster along contours; clearings, roads and building approaches remain open.
 for i in range(6400):
  e=rng.uniform(-485,485);n=rng.uniform(-385,385)
  density=.17
  if n>140 and e>110:density=.83
  elif abs(e)>355 or abs(n)>280:density=.76
  elif e<-80:density=.28
  else:density=.12
  density*=.55+.45*math.sin(e/17)*math.sin(n/23)
  if rng.random()>density or not free(e,n,4):continue
  old=n>155 and e>190;height=rng.uniform(15,20) if old and rng.random()<.3 else rng.uniform(6,11)
  scale=height/3.06;put('Oak',e,n,scale,yaw=45+rng.uniform(-7,7));put('Trunks',e,n,z=surface(e,n)+1,scale=(.5,.5,2))
  for j in range(rng.randint(2,5)):
   ee=e+rng.uniform(-3,3);nn=n+rng.uniform(-3,3)
   if free(ee,nn,.5):put('Bush',ee,nn,rng.uniform(.8,1.5))
  if i%80==0:yield 'groves '+str(i)
 # Dense, nonuniform ground coverage plus deliberate roadside clusters.
 for i in range(23000):
  e=rng.uniform(-399,399);n=rng.uniform(-299,299)
  if not free(e,n,.15):continue
  if math.sin(e/11)+math.cos(n/16)<-.8:continue
  k=rng.choices(['GrassSmall','GrassMedium','GrassLarge','MeadowHerbs','PebbleSmall'],[4,4,1,2,1])[0];put(k,e,n,rng.uniform(.8,1.2),rng.uniform(0,360))
  if i%1000==0:yield 'meadow '+str(i)
 for _,pts,w in PATHS:
  for i,(e,n) in enumerate(pts[::3]):
   for side in (-1,1):
    ee=e+side*(w/2+rng.uniform(.4,2.3));nn=n+rng.uniform(-1,1)
    if free(ee,nn,.1):put(rng.choice(['GrassMedium','GrassLarge','MeadowHerbs']),ee,nn,rng.uniform(.8,1.1),rng.uniform(0,360))
   if i%60==0:yield 'path edges '+str(i)
 # Painted rock accents along real banks and higher terraces, never across routes.
 for i in range(450):
  n=rng.uniform(-298,298);e=L.river(n)+rng.choice([-1,1])*rng.uniform(7,15)
  if distance_to_paths(e,n)>3:put('Crags',e,n,rng.uniform(.65,1.1),rng.uniform(0,360));put('Bush',e+1,n+1,1.2)
 for key in ['Heilhaus','Steinkreis','Waldruinen']:
  ce,cn=L.PLACES[key]
  for i in range(35):
   t=rng.uniform(0,math.tau);r=rng.uniform(18,38);e=ce+math.cos(t)*r;n=cn+math.sin(t)*r
   if distance_to_paths(e,n)>4 and free(e,n,1):put('Crags',e,n,rng.uniform(.6,.95),rng.uniform(0,360))
 yield 'rock contours'
 # Well, market shelter, benches and two agricultural areas use existing reusable meshes.
 cube=load('/Engine/BasicShapes/Cube');cyl=load('/Engine/BasicShapes/Cylinder')
 def box(name,e,n,z,s,mat=wood,collision=False,yaw=-45):return mesh_actor(name,cube,L.world(e,n,z),yaw,collision,scale=s,mat=mat,folder='Dressing')
 for i in range(12):
  t=i*math.tau/12;box('WellStone_'+str(i),-218+1.2*math.cos(t),-31+1.2*math.sin(t),.48,(.6,.35,.9),stone,True,yaw=45-math.degrees(t))
 for side in [-1,1]:box('WellPost_'+str(side),-218+side*1.45,-31,1.35,(.18,.18,2.7))
 box('WellLintel',-218,-31,2.6,(.25,3.25,.25));box('WellWater',-218,-31,.3,(1.8,1.8,.08),material('WellWater',(.04,.15,.18)))
 for i,(e,n) in enumerate([(-224,-21),(-235,-35),(-202,-24)]):
  box('Bench_'+str(i),e,n,.45,(.55,2.2,.18),collision=True)
  for side in [-1,1]:box('BenchLeg_'+str(i)+'_'+str(side),e,n+side*.8,.2,(.4,.18,.4))
 for i,e in enumerate([-235,-230]):
  n=-20;box('MarketCounter_'+str(i),e,n,.82,(1.2,2.5,.3),collision=True)
  for de in [-.8,.8]:
   for dn in [-1.5,1.5]:box('MarketPost_'+str(i)+'_'+str(de)+str(dn),e+de,n+dn,1.25,(.13,.13,2.5))
  box('MarketCanopy_'+str(i),e,n,2.6,(2.2,3.5,.12),material('Canvas',(.55,.47,.28)))
 # Fences enclose gardens with intentional wide entrances.
 for prefix,ce,cn,hx,hy in [('Farm',-300,-220,35,28),('Field',180,-230,30,22)]:
  for side in [-1,1]:
   for j in range(int(hy*2/3)):
    e=ce+side*hx;n=cn-hy+j*3
    box(prefix+'FencePost_'+str(side)+'_'+str(j),e,n,surface(e,n)+.6,(.16,.16,1.2))
    box(prefix+'FenceRail_'+str(side)+'_'+str(j),e,n+1.5,surface(e,n)+.75,(3,.1,.12))
  for j in range(int(hx*2/3)):
   e=ce-hx+j*3
   for side in [-1,1]:
    n=cn+side*hy
    if distance_to_paths(e,n)<5:continue
    box(prefix+'FenceEnd_'+str(side)+'_'+str(j),e,n,surface(e,n)+.6,(.16,.16,1.2));box(prefix+'FenceEndRail_'+str(side)+'_'+str(j),e+1.5,n,surface(e,n)+.75,(.1,3,.12))
  yield prefix+' fenced'
 for row in range(15):
  for j in range(28):
   e=160+row*2.1;n=-247+j*1.3
   if distance_to_paths(e,n)>3:put('MeadowHerbs',e,n,1.7)
 # Orchard groups read differently through rhythm and fruit-colored accents.
 for i,(e,n) in enumerate([(-326,-205),(-320,-202),(-325,-196),(-315,-195),(-320,-189),(-310,-187)]):put('Oak',e,n,2);put('Bush',e-1,n-1,1)
 for key in ['Lichtung','Aussicht','Uferfund']:
  e,n=L.PLACES[key];box('RestBench_'+key,e-3,n+2,surface(e-3,n+2)+.42,(.6,2,.18),collision=True)
  for i in range(8):put('MeadowHerbs',e+rng.uniform(-5,5),n+rng.uniform(-5,5),1.1)
 # A recognizable pass, with no implicit travel system added.
 for side in [-1,1]:mesh_actor('PassStone_'+str(side),load(DEST+'/Meshes/WR_StandingStone'),L.world(383+side*4,170,4),45,folder='Landmarks/Exit')
 box('PassLintel',383,170,7.1,(.5,9,.35));(OUT/'DressingCounts.json').write_text(json.dumps(counts,indent=2));yield 'dressing ready'

def lighting():
 for a in A.get_all_level_actors():
  if isinstance(a,unreal.DirectionalLight):a.light_component.set_mobility(unreal.ComponentMobility.MOVABLE);a.light_component.set_intensity(2.2);a.light_component.set_editor_property('cast_shadows',False)
  if isinstance(a,unreal.SkyLight):
   a.light_component.set_mobility(unreal.ComponentMobility.MOVABLE);a.light_component.set_editor_property('source_type',unreal.SkyLightSourceType.SLS_SPECIFIED_CUBEMAP);a.light_component.set_editor_property('cubemap',load('/Engine/EngineResources/DefaultTextureCube'));a.light_component.set_intensity(.7)
 pp=spawn(unreal.PostProcessVolume,'OutdoorExposure',(0,0,0),folder='Lighting');pp.set_editor_property('unbound',True);pp.set_editor_property('priority',-100)
 s=pp.get_editor_property('settings')
 for k,v in {'override_auto_exposure_method':True,'auto_exposure_method':unreal.AutoExposureMethod.AEM_MANUAL,'override_auto_exposure_apply_physical_camera_exposure':True,'auto_exposure_apply_physical_camera_exposure':False,'override_auto_exposure_bias':True,'auto_exposure_bias':0.}.items():s.set_editor_property(k,v)
 pp.set_editor_property('settings',s);yield 'stable painted outdoor light'

def systems():
 # Existing data and subsystems; unique source IDs avoid altering Slice progression.
 for i,(e,n) in enumerate([(155,10),(190,-68),(268,90)]):
  a=next((a for a in A.get_all_level_actors() if a.get_actor_label()=='WR_Wild_'+str(i)),None) or spawn(unreal.PokeMonsterVisibleWildCreatureActor,'Wild_'+str(i),L.world(e,n,surface(e,n)+.6),folder='Encounters');a.set_editor_property('encounter_id','WestlandRegion_Wild_'+str(i));a.set_editor_property('seed',3817+i)
  s=a.get_editor_property('sprite');s.set_sprite(load('/Game/Creatures/Prototype2D/Sprites/S_Waldling'));s.set_relative_rotation(unreal.Rotator(yaw=45),False,False)
  for t in a.get_components_by_class(unreal.TextRenderComponent):t.set_hidden_in_game(True);t.set_visibility(False)
  yield 'wild '+str(i)
 for i,(e,n,dialogue,name,sprite) in enumerate([(-299,-216,'DA_DevWandererDialogue','Wanderer','Wanderer'),(-222,-29,'DA_DevWandererDialogue','Dorfbewohner','Wanderer'),(-48,231,'DA_DevArchivistDialogue','Archivarin','Archivarin')]):
  a=next((a for a in A.get_all_level_actors() if a.get_actor_label()=='WR_NPC_'+str(i)),None) or spawn(unreal.PokeMonsterNPC,'NPC_'+str(i),L.world(e,n,surface(e,n)+.6),folder='NPC');a.set_editor_property('dialogue',load('/Game/Data/Dialogues/'+dialogue));a.set_editor_property('display_name',name);a.sprite.set_sprite(load('/Game/Characters/Prototype2D/Sprites/S_'+sprite));a.sprite.set_relative_rotation(unreal.Rotator(yaw=45),False,False)
  for t in a.get_components_by_class(unreal.TextRenderComponent):t.set_hidden_in_game(True);t.set_visibility(False)
  yield 'NPC '+name
 yield 'existing encounters and conversations integrated'

PHASES={'base':base,'terrain':terrain,'buildings':buildings,'props':import_props,'dress':dress,'systems':systems,'lighting':lighting}
def start(phase):
 assert not E.get_game_world(),'Stop PIE before authoring';gen=PHASES[phase]();beg=time.monotonic();state={'phase':phase,'done':False,'steps':0,'error':None};(OUT/'Progress.json').write_text(json.dumps(state))
 state['busy']=False
 def tick(dt):
  if state['busy']:return
  state['busy']=True
  try:
   state['last']=next(gen);state['steps']+=1;state['elapsed']=time.monotonic()-beg
  except StopIteration:
   unreal.unregister_slate_post_tick_callback(unreal._wr_job);del unreal._wr_job;assert unreal.EditorLoadingAndSavingUtils.save_map(E.get_editor_world(),L.MAP);state['done']=True;unreal.log('REGION_PHASE_DONE '+phase)
  except Exception as ex:
   unreal.unregister_slate_post_tick_callback(unreal._wr_job);del unreal._wr_job;state['error']=repr(ex);unreal.log_error('REGION_PHASE_FAILED '+phase+' '+repr(ex))
  state['busy']=False
  (OUT/'Progress.json').write_text(json.dumps(state,indent=2))
 if hasattr(unreal,'_wr_job'):raise RuntimeError('An authoring phase is still running')
 unreal._wr_job=unreal.register_slate_post_tick_callback(tick)
if __name__=='<run_path>':start(json.loads((OUT/'Job.json').read_text())['phase'])
