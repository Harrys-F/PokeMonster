"""Denser, irregular fern/litter pockets after direct Third-Person review."""
import runpy
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/WestlandEnvironmentPolishV2/Common.py')));assert not(D/'ForestFloor.json').exists();rng=random.Random(2211030);refs={r['label']:r for r in json.loads((D/'Inventory.json').read_text())['Dev_TestMap_VisualV2']};centers=[]
for a in actors.values():
 if not a.get_actor_label().startswith(('WVU_Trees_','WEP_Canopy_')):continue
 c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
 for i in range(c.get_instance_count()):
  p=c.get_instance_transform(i,True).translation;e,n=L.en(p.x,p.y)
  if forest(e,n)>.3 and rng.random()<.65:centers.append((e,n))
for ce,cn in centers:
 for i in range(8):
  e=ce+rng.gauss(0,2.0);n=cn+rng.gauss(0,2.0)
  if not safe(e,n,.3):continue
  if i<5:
   key='A'if i%2 else'B';c=group('FloorFerns_'+key,'/Game/Environment/WestlandAssetLibrary/Meshes/Vegetation/SM_WLA_Fern_'+key,cull=4800);put(c,e,n,rng.uniform(38,75),rng.uniform(0,360))
  elif i==5:
   ref=refs['EQ3_Moss'];c=group('FloorMoss',ref['mesh'],ref['materials'],cull=5500);put(c,e,n,rng.uniform(8,22),rng.uniform(0,360))
  else:
   c=group('FloorGrass','/Game/Environment/VisualV2EnvironmentV3/Meshes/SM_EQ3_GrassWoodland',cull=6000);put(c,e,n,rng.uniform(24,42),rng.uniform(0,360))
save('ForestFloor.json',dict(review='Third-Person floor gaps receive local fern/moss pockets; no density reduction'))
