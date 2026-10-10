"""Owned-region surface and landmark finishing after first real-camera foot replay.
Existing module meshes/materials are referenced read-only. No runtime changes.
"""
import unreal,runpy,sys,math,random,json
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();OUT=ROOT/'Saved/WestlandRegion';sys.dont_write_bytecode=True;sys.path.insert(0,str(ROOT/'Tools'))
import WestlandRegionLayout as L
B=runpy.run_path(str(ROOT/'Tools/BuildWestlandRegionV1.py'),run_name='region_library');A=B['A'];E=B['E'];assert not E.get_game_world();assert E.get_editor_world().get_name()=='Dev_WestlandRegion'
by={a.get_actor_label():a for a in A.get_all_level_actors()};REPAIR=(OUT/'RepairAccess.flag').exists();assert REPAIR or 'WR_ArtFinishComplete' not in by
rng=random.Random(190226);paths=[]
def update(sm,vs,tri,uv):
 buf=unreal.GeometryScriptSimpleMeshBuffers();buf.vertices=[unreal.Vector(*v) for v in vs];buf.triangles=[unreal.IntVector(t[0],t[2],t[1]) for t in tri];buf.uv0=[unreal.Vector2D(*v) for v in uv];d=unreal.DynamicMesh();unreal.GeometryScript_MeshEdits.append_buffers_to_mesh(d,buf)
 opt=unreal.GeometryScriptCopyMeshToAssetOptions();opt.enable_recompute_normals=True;_,res=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(d,sm,opt,unreal.GeometryScriptMeshWriteLOD());assert res==unreal.GeometryScriptOutcomePins.SUCCESS;unreal.EditorAssetLibrary.save_loaded_asset(sm,False)
def ribbon(name,points,width,existing=False):
 pts=L.sample(points,spacing=.5);vs=[];uv=[];tri=[]
 for i,(e,n) in enumerate(pts):
  q=pts[max(0,i-1)];r=pts[min(len(pts)-1,i+1)];dx=r[0]-q[0];dy=r[1]-q[1];length=max(.01,math.hypot(dx,dy));ww=width*(1+.04*math.sin(i*.13))
  for j in range(9):
   s=j/8*2-1;ee=e-dy/length*ww/2*s;nn=n+dx/length*ww/2*s;z=B['path_height'](ee,nn)+.10;vs.append(L.world(ee,nn,z));uv.append((i/(len(pts)-1),j/8))
   if i and j:a=(i-1)*9+j-1;b=a+9;tri.extend([(a,a+1,b+1),(a,b+1,b)])
 p=L.ASSETS+'/Meshes/SM_WR_Path_'+name
 if existing:update(unreal.load_asset(p),vs,tri,uv)
 else:
  sm=B['newmesh']('SM_WR_Path_'+name,vs,tri,uv,unreal.load_asset(L.ASSETS+'/Materials/M_WR_PathBlend'));B['mesh_actor']('Path_'+name,sm,(0,0,0),folder='Paths/Access')
 paths.append({'name':name,'points_m':points,'width_m':width})
def job():
 if not REPAIR:
  for name,p,w in L.PATHS:ribbon(name,p,w,True);yield name+' draped'
 # Exact front thresholds, not guessed axis-aligned building footprints.
 for b in L.buildings():
  cut=by['WR_'+b['id']+'_Cutaway'];q=cut.get_editor_property('door_threshold').get_world_location();e,n=L.en(q.x,q.y);yaw=math.radians(b['yaw']);fore=(e-math.cos(yaw+math.pi/4)*2.5,n-math.sin(yaw+math.pi/4)*2.5)
  # World local X points north in authoring coordinates at yaw -45.
  f=unreal.MathLibrary.rotate_angle_axis(unreal.Vector(-250,0,0),b['yaw'],unreal.Vector(0,0,1));ff=q+f;fore=L.en(ff.x,ff.y)
  near=min((pt for _,pts,w in B['PATHS'] for pt in pts),key=lambda pt:math.dist(pt,fore))
  v=unreal.Vector(*L.world(*near))-q;local=unreal.MathLibrary.rotate_angle_axis(v,-b['yaw'],unreal.Vector(0,0,1))
  points=[near]
  if local.x>-350:
   corner=q+unreal.MathLibrary.rotate_angle_axis(unreal.Vector(-400,local.y,0),b['yaw'],unreal.Vector(0,0,1));points.append(L.en(corner.x,corner.y))
   front=q+unreal.MathLibrary.rotate_angle_axis(unreal.Vector(-400,0,0),b['yaw'],unreal.Vector(0,0,1));points.append(L.en(front.x,front.y))
  points.extend([fore,(e,n)])
  ribbon('Access_'+b['id'],points,2.2,REPAIR);yield b['id']+' access'
 if REPAIR:
  (OUT/'AccessRepair.json').write_text(json.dumps(paths,indent=2));(ROOT/'Art/World/WestlandRegion/WestlandRegion_Access.json').write_text(json.dumps(paths,indent=2));return
 # A softly edged, nonrectangular village square and farm garden ground patches.
 for name,ce,cn,rx,ry in [('VillageSquare',-220,-35,17.5,15),('FarmGarden',-300,-207,5,6),('MillCropSoil',181,-229,24,18)]:
  vs=[L.world(ce,cn,B['surface'](ce,cn)+.11)];uv=[(.5,.5)];tri=[]
  for j in range(65):
   t=j*math.tau/64;r=1+.035*math.sin(t*5)+.025*math.cos(t*7);e=ce+rx*r*math.cos(t);n=cn+ry*r*math.sin(t);vs.append(L.world(e,n,B['surface'](e,n)+.11));uv.append((.5,0));
   if j:tri.append((0,j,j+1))
  sm=B['newmesh']('SM_WR_'+name,vs,tri,uv,unreal.load_asset(L.ASSETS+'/Materials/M_WR_PathBlend'));B['mesh_actor'](name,sm,(0,0,0),folder='Dressing/Ground');yield name
 stone=unreal.load_asset('/Game/Environment/HealingHouse/QualityV2/Materials/M_HH_Q2_Stone')
 for name in ['StoneBridge','RuinArch','RuinColumn','StandingStone','Crag']:
  sm=unreal.load_asset(L.ASSETS+'/Meshes/WR_'+name)
  for i in range(len(sm.get_editor_property('static_materials'))):sm.set_material(i,stone)
  unreal.EditorAssetLibrary.save_loaded_asset(sm,False);yield name+' painted stone'
 groups={name:B['instances']('Garden_'+name,unreal.load_asset('/Game/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_'+name),end=4500) for name in ['FlowerPlant','LeafPlant','BroadHerb','NarrowHerb']}
 for c in groups.values():c.set_mobility(unreal.ComponentMobility.STATIC)
 def plant(name,e,n,s=1):groups[name].add_instance(unreal.Transform(location=unreal.Vector(*L.world(e,n,B['surface'](e,n)+.12)),rotation=unreal.Rotator(yaw=rng.uniform(0,360)),scale=unreal.Vector(s,s,s)),True)
 for i in range(200):
  e=-303+(i%12)*.55;n=-211+(i//12)*.5;plant(['FlowerPlant','LeafPlant','BroadHerb','NarrowHerb'][i%4],e,n,.9)
 for b in L.buildings():
  cut=by['WR_'+b['id']+'_Cutaway'];q=cut.get_editor_property('door_threshold').get_world_location()
  for side in [-1,1]:
   for j in range(9):
    f=unreal.MathLibrary.rotate_angle_axis(unreal.Vector(-130-rng.uniform(0,100),side*(160+j*25),0),b['yaw'],unreal.Vector(0,0,1));e,n=L.en(q.x+f.x,q.y+f.y);plant('FlowerPlant' if j%2 else 'LeafPlant',e,n,.8)
  yield b['id']+' garden'
 # Keep meaningful silhouettes near the game viewport, without hiding access.
 oak=by['WR_Oak'].get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
 bush=by['WR_Bush'].get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
 trunks=by['WR_TrunkCollision'].get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
 clusters=[(-310,-232),(-303,-229),(-239,-44),(-229,-45),(-232,-9),(-216,-19),(-196,-34),(134,12),(155,19),(177,15),(190,33),(203,91),(214,169),(237,193),(214,210),(238,214),(278,78),(287,89),(-304,192),(-323,201),(-53,225),(-36,244),(134,-240),(155,-220)]
 for e,n in clusters:
  if B['distance_to_paths'](e,n)<3:continue
  z=B['surface'](e,n);s=rng.uniform(2,2.5);oak.add_instance(unreal.Transform(location=unreal.Vector(*L.world(e,n,z)),rotation=unreal.Rotator(yaw=45),scale=unreal.Vector(s,s,s)),True);trunks.add_instance(unreal.Transform(location=unreal.Vector(*L.world(e,n,z+1)),scale=unreal.Vector(.5,.5,2)),True)
  for i in range(9):
   ee=e+rng.uniform(-2.5,2.5);nn=n+rng.uniform(-2.5,2.5)
   if B['distance_to_paths'](ee,nn)<1:continue
   bush.add_instance(unreal.Transform(location=unreal.Vector(*L.world(ee,nn,B['surface'](ee,nn))),rotation=unreal.Rotator(yaw=45),scale=unreal.Vector(.8,.8,.8)),True);plant('LeafPlant',ee,nn,.9)
 yield 'near camera groves'
 # Layered flower/herb pockets at ruins and stone circle, not uniform decoration.
 for ce,cn in [L.PLACES[k] for k in ['Steinkreis','Waldruinen','Lichtung','Uferfund']]:
  for i in range(55):
   t=rng.uniform(0,math.tau);r=rng.uniform(5,10);e=ce+r*math.cos(t);n=cn+r*math.sin(t)
   if B['distance_to_paths'](e,n)>1.4:plant('FlowerPlant' if i%3==0 else 'NarrowHerb',e,n,.9)
  yield 'landmark garden'
 B['spawn'](unreal.Actor,'ArtFinishComplete',(0,0,0),folder='Metadata');(OUT/'ArtFinish.json').write_text(json.dumps({'paths':paths,'garden_instances':sum(c.get_instance_count() for c in groups.values()),'no_shared_changes':True},indent=2));yield 'done'
gen=job();busy=False
def tick(dt):
 global busy
 if busy:return
 busy=True
 try:next(gen)
 except StopIteration:unreal.unregister_slate_post_tick_callback(unreal._wr_artfinish);del unreal._wr_artfinish;unreal.EditorLoadingAndSavingUtils.save_map(E.get_editor_world(),L.MAP)
 except Exception as ex:unreal.unregister_slate_post_tick_callback(unreal._wr_artfinish);del unreal._wr_artfinish;unreal.log_error('REGION_ART_FINISH_FAILED '+repr(ex))
 busy=False
unreal._wr_artfinish=unreal.register_slate_post_tick_callback(tick)
