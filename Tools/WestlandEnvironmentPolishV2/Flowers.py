"""Existing wildflower geometry, map-local petal tints, irregular meadow and edge clusters."""
import runpy
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/WestlandEnvironmentPolishV2/Common.py')));assert not(D/'Flowers.json').exists();rng=random.Random(2211027);mesh=unreal.load_asset('/Game/Environment/WestlandAssetLibrary/Meshes/Vegetation/SM_WLA_Wildflowers_A');colors={'Cream':(.92,.90,.70),'Yellow':(.95,.70,.12),'Blue':(.22,.32,.70),'Violet':(.52,.22,.60),'Red':(.72,.14,.10),'Pink':(.83,.37,.53)};mats={}
for name,col in colors.items():
 src=unreal.load_asset('/Game/Environment/WestlandAssetLibrary/Materials/MI_WLA_FlowerCream');q=ROOT+'/Materials/MI_WEP_Blossom_'+name;mi=unreal.EditorAssetLibrary.duplicate_asset(src.get_path_name(),q);assert mi;ML.set_material_instance_parent(mi,mat(src.parent));ML.set_material_instance_vector_parameter_value(mi,'Tint',unreal.LinearColor(*col,1));assert unreal.EditorAssetLibrary.save_loaded_asset(mi,False);mats[name]=mi
patches=[(145,11,28,1500),(-300,-210,20,600),(-220,-100,25,700),(120,30,28,1200),(180,-32,25,1300),(285,80,14,500)]
for i in range(150):
 e=rng.uniform(-370,365);n=rng.uniform(-280,280)
 if forest(e,n)<.5:patches.append((e,n,rng.uniform(3,9),rng.randint(25,90)))
for ce,cn,r,count in patches:
 preferred=rng.choice(list(colors))
 for i in range(count):
  e=ce+rng.gauss(0,r*.48);n=cn+rng.gauss(0,r*.48)
  if not safe(e,n,.35):continue
  name=preferred if rng.random()<.72 else rng.choice(list(colors));matlist=[x.material_interface for x in mesh.static_materials];matlist[1]=mats[name];matlist[2]=mats[rng.choice(['Cream','Yellow'])];c=group('Wildflowers_'+name,mesh,matlist,cull=6500);put(c,e,n,rng.uniform(32,66),rng.uniform(0,360))
for i in range(42000):
 e=rng.uniform(-400,400);n=rng.uniform(-300,300)
 if not safe(e,n,.2)or rng.random()<forest(e,n)*.55:continue
 key=rng.choices(['Short','Meadow','Woodland'],[.2,.6,.2])[0];c=group('MeadowGrass_'+key,'/Game/Environment/VisualV2EnvironmentV3/Meshes/SM_EQ3_Grass'+key,cull=6500);put(c,e,n,rng.uniform(18,44),rng.uniform(0,360))
save('Flowers.json',dict(colors=colors,mesh_source=mesh.get_path_name(),no_specific_botanical_species_claimed=True))
