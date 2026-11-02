"""Dense layered forest using exclusively existing mesh variants and original trunk hulls."""
import runpy,sys
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/WestlandEnvironmentPolishV2/Common.py')));assert not(D/'Densify.json').exists();rng=random.Random(2211026);treepoints=[]
for a in actors.values():
 if not a.get_actor_label().startswith('WVU_Trees_'):continue
 c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
 for i in range(c.get_instance_count()):p=c.get_instance_transform(i,True).translation;treepoints.append(L.en(p.x,p.y))
grid={}
for e,n in treepoints:grid.setdefault((int(e//4),int(n//4)),[]).append((e,n))
existing={a.get_actor_label()[10:]:a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)for a in actors.values()if a.get_actor_label().startswith('WVU_Trees_')};treeadded=[]
for attempt in range(16000):
 e=rng.uniform(-405,385);n=rng.uniform(-280,300);f=forest(e,n)
 if rng.random()>f or not safe(e,n,2.3):continue
 if any(math.hypot(e-u,n-v)<rng.uniform(2.8,4.4)for gx in range(int(e//4)-1,int(e//4)+2)for gy in range(int(n//4)-1,int(n//4)+2)for u,v in grid.get((gx,gy),[])):continue
 key=rng.choices(['OakAncient_V3','OakYoung_A','OakYoung_B','Birch_A','Birch_B'],[.38,.23,.20,.1,.09])[0];src=existing[key];c=group('Canopy_'+key,src.static_mesh,[src.get_material(i)for i in range(src.get_num_materials())],True,True,18000);h=rng.uniform(750,1350)if f>.6 else rng.uniform(400,850);put(c,e,n,h,rng.uniform(0,360));grid.setdefault((int(e//4),int(n//4)),[]).append((e,n));treeadded.append([e,n,h,key])
 if len(treeadded)>=1600:break
for i in range(12000):
 e=rng.uniform(-405,395);n=rng.uniform(-295,300);f=forest(e,n)
 if rng.random()>f*.92+.06 or not safe(e,n,.9):continue
 if i%3==0:
  key=rng.choice(['OakYoung_A','Birch_A']);src=existing[key];c=group('Sapling_'+key,src.static_mesh,[src.get_material(j)for j in range(src.get_num_materials())],True,True,10500);put(c,e,n,rng.uniform(190,400),rng.uniform(0,360))
 else:
  key='A'if i%2 else'B';c=group('Underwood_'+key,'/Game/Environment/WestlandAssetLibrary/QualityV3/Meshes/Vegetation/SM_WLA_WildBush_V3_'+key,shadow=False,cull=8000);put(c,e,n,rng.uniform(65,170),rng.uniform(0,360))
for i in range(16000):
 e=rng.uniform(-405,395);n=rng.uniform(-295,300);f=forest(e,n)
 if rng.random()>f or not safe(e,n,.35):continue
 if i%3==0:
  key='A'if i%2 else'B';c=group('Ferns_'+key,'/Game/Environment/WestlandAssetLibrary/Meshes/Vegetation/SM_WLA_Fern_'+key,cull=5000);put(c,e,n,rng.uniform(45,85),rng.uniform(0,360))
 else:
  key='Meadow'if i%2 else'Woodland';c=group('ForestGrass_'+key,'/Game/Environment/VisualV2EnvironmentV3/Meshes/SM_EQ3_Grass'+key,cull=6000);put(c,e,n,rng.uniform(22,48),rng.uniform(0,360))
save('Densify.json',dict(added_canopy=len(treeadded),original_tree_count=1710,canopy_positions=treeadded,forest_area='eastern woodland and existing west woodland margin; paths/pads/clearings excluded'))
