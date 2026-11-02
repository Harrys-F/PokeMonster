"""Replace old crags with existing authored boulder hulls; existing pebbles dress the actual bed."""
import runpy
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/WestlandEnvironmentPolishV2/Common.py')));assert not(D/'RocksBed.json').exists();rng=random.Random(2211028);old=actors['WR_RockyContours'].get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);ts=[old.get_instance_transform(i,True)for i in range(old.get_instance_count())];assert len(ts)==503;replaced=0
for i,t in enumerate(ts):
 p=t.translation;e,n=L.en(p.x,p.y)
 for j in range(3):
  key='A'if(i+j)%2 else'B';mesh='/Game/Environment/WestlandAssetLibrary/Meshes/Landscape/SM_WLA_Boulder_'+key;c=group('Boulders_'+key,mesh,collision=True,shadow=True,cull=16000);u=e+(rng.uniform(-1.3,1.3)if j else 0);v=n+(rng.uniform(-1.1,1.1)if j else 0);h=min(430,max(95,300*t.scale3d.z*(.8 if j else 1.1)));x,y,z=L.world(u,v,L.height(u,v));g=ground(x,y,z);box=c.static_mesh.get_bounding_box();s=h/(box.max.z-box.min.z);s3=(s*rng.uniform(1.0,1.45),s*rng.uniform(.8,1.2),s);c.add_instance(unreal.Transform(location=unreal.Vector(x,y,g-h*.22),rotation=unreal.Rotator(pitch=rng.uniform(-11,11),yaw=rng.uniform(0,360),roll=rng.uniform(-9,9)),scale=unreal.Vector(*s3)),True)
 replaced+=1
actors['WR_RockyContours'].modify();old.clear_instances();old.set_collision_profile_name('NoCollision')
# Existing tiny pebble meshes, not newly generated stone models. Keep bridges and fish silhouettes clear.
for i in range(4200):
 n=rng.uniform(-305,305)
 if abs(n+50)<16 or abs(n+235)<14 or 150<n<200:continue
 e=L.river(n)+rng.uniform(-3.3,3.3);key='PebbleSmall'if i%3 else'PebbleCluster';c=group('Bed_'+key,'/Game/Environment/Westland/NaturalGroundV1/Meshes/SM_WL_NG_'+key,cull=6000);put(c,e,n,rng.uniform(5,13),rng.uniform(0,360))
# Patchy banks, not a continuous hedge that conceals the stream.
for i in range(1500):
 n=rng.uniform(-295,295);e=L.river(n)+rng.choice([-1,1])*rng.uniform(4.4,6.8)
 if path_distance(e,n)<.9 or any(math.hypot(e-u,n-v)<5 for u,v in protected):continue
 key='Reeds'if i%3==0 else'MeadowGrass';mesh='/Game/Environment/VisualV2WorldArtV5/Meshes/SM_WA5_ReedTuft'if key=='Reeds'else'/Game/Environment/VisualV2EnvironmentV3/Meshes/SM_EQ3_GrassMeadow';c=group('Banks_'+key,mesh,cull=7000);put(c,e,n,rng.uniform(30,65)if key=='Reeds'else rng.uniform(20,42),rng.uniform(0,360))
save('RocksBed.json',dict(old_crag_clusters_replaced=replaced,existing_boulder_variants=2,no_bed_collision=True,fish_zones_and_barriers_unchanged=True))
