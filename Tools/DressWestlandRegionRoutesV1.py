"""Second owned art pass after real-camera route review. No gameplay rewriting."""
import unreal,runpy,sys,math,random,json
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();OUT=ROOT/'Saved/WestlandRegion';sys.dont_write_bytecode=True;sys.path.insert(0,str(ROOT/'Tools'))
import WestlandRegionLayout as L
B=runpy.run_path(str(ROOT/'Tools/BuildWestlandRegionV1.py'),run_name='region_library');A=B['A'];E=B['E'];assert not E.get_game_world();assert E.get_editor_world().get_name()=='Dev_WestlandRegion'
by={a.get_actor_label():a for a in A.get_all_level_actors()};assert 'WR_RouteDressingComplete' not in by,'Already applied'
groups={name:by['WR_'+name].get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent) for name in ['Oak','Bush','GrassSmall','GrassMedium','GrassLarge','MeadowHerbs','PebbleSmall']}
for a in A.get_all_level_actors():
 for c in a.get_components_by_class(unreal.HierarchicalInstancedStaticMeshComponent):c.set_mobility(unreal.ComponentMobility.STATIC)
rng=random.Random(490226);counts={}
def put(name,e,n,s=1,yaw=45):
 groups[name].add_instance(unreal.Transform(location=unreal.Vector(*L.world(e,n,B['surface'](e,n)+.02)),rotation=unreal.Rotator(yaw=yaw),scale=unreal.Vector(s,s,s)),True);counts[name]=counts.get(name,0)+1
def job():
 for label,points,width in L.PATHS:
  pts=L.sample(points)
  for i in range(2,len(pts)-2,2):
   e,n=pts[i];x=pts[i+1][0]-pts[i-1][0];y=pts[i+1][1]-pts[i-1][1];length=max(.01,math.hypot(x,y))
   for side in [-1,1]:
    if rng.random()<.18:continue
    off=width/2+rng.uniform(.5,1.5)
    for j in range(rng.randint(2,4)):
     ee=e-y/length*off*side+rng.uniform(-.4,.4);nn=n+x/length*off*side+rng.uniform(-.4,.4)
     if abs(ee-L.river(nn))<6 or any(abs(ee-b['place'][0])<b['size'][1]/2+1 and abs(nn-b['place'][1])<b['size'][0]/2+1 for b in L.buildings()):continue
     put(rng.choice(['GrassMedium','GrassLarge','MeadowHerbs']),ee,nn,rng.uniform(.85,1.2),rng.uniform(0,360))
    if i%18==0:put('Bush',e-y/length*(width/2+2.1)*side,n+x/length*(width/2+2.1)*side,rng.uniform(.65,1.0))
   if i%100==0:yield label+' edges '+str(i)
 # Landmarks are framed, rather than surrounded by a uniformly empty safety disk.
 for key,trees in {'Waldruinen':[(216,202),(215,209),(220,216),(232,215),(235,207),(236,198)],'Steinkreis':[(-56,231),(-55,241),(-37,245),(-34,229)],'Heilhaus':[(-323,195),(-323,207),(-298,210)],'Hof':[(-304,-229),(-294,-227)]}.items():
  for e,n in trees:
   if B['distance_to_paths'](e,n)<3:continue
   put('Oak',e,n,rng.uniform(2.2,2.8),45+rng.uniform(-5,5));put('Bush',e-1,n-.5,1.15)
  yield key+' framing'
 # Painted stone finish is overridden only on new regional objects.
 stone=unreal.load_asset('/Game/Environment/HealingHouse/QualityV2/Materials/M_HH_Q2_Stone');assert stone
 for a in A.get_all_level_actors():
  if a.get_actor_label().startswith(('WR_Ruin','WR_StandingStone','WR_WellStone','WR_PassStone')) and isinstance(a,unreal.StaticMeshActor):a.static_mesh_component.set_material(0,stone)
 # Small wall-foot plants and garden beds make individual fronts legible.
 for b in L.buildings():
  theta=math.radians(b['yaw']);ce,cn=b['place'];yaw=b['yaw']
  for side in [-1,1]:
   local=unreal.MathLibrary.rotate_angle_axis(unreal.Vector(-b['size'][0]*50-60,side*b['size'][1]*40,0),yaw,unreal.Vector(0,0,1));origin=unreal.Vector(*L.world(ce,cn,b['z']));q=origin+local;e,n=L.en(q.x,q.y)
   put('Bush',e,n,1.1)
   for j in range(8):put('MeadowHerbs',e+rng.uniform(-1.2,1.2),n+rng.uniform(-.6,.6),rng.uniform(.8,1.1),rng.uniform(0,360))
  yield b['id']+' front planting'
 B['spawn'](unreal.Actor,'RouteDressingComplete',(0,0,0),folder='Metadata');(OUT/'RouteDressing.json').write_text(json.dumps(counts,indent=2));yield 'route art done'
gen=job();busy=False
def tick(dt):
 global busy
 if busy:return
 busy=True
 try:next(gen)
 except StopIteration:unreal.unregister_slate_post_tick_callback(unreal._wr_routes);del unreal._wr_routes;unreal.EditorLoadingAndSavingUtils.save_map(E.get_editor_world(),L.MAP)
 except Exception as ex:unreal.unregister_slate_post_tick_callback(unreal._wr_routes);del unreal._wr_routes;unreal.log_error('REGION_ROUTE_ART_FAILED '+repr(ex))
 busy=False
unreal._wr_routes=unreal.register_slate_post_tick_callback(tick)
