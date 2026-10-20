"""Corrections from real QHD draft: strengthen soil patches, break shrub ribbon, darken deadwood, ground table props."""
import unreal,json,random,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ArtPassV5';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();L=unreal.MaterialEditingLibrary;assert not E.get_game_world() and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not (S/'ReviewFinished.json').exists();actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};graphs=[]
for key in ['Ground','NorthPath','MainPath']:
 m=unreal.load_asset('/Game/Environment/HealingHouse/ArtV5/Materials/M_HH5_Landscape'+key)
 for n in L.get_material_expressions(m):
  if not isinstance(n,unreal.MaterialExpressionCustom):continue
  code=n.get_editor_property('code')
  if '// V5:'not in code:continue
  before=code;code=code.replace('float3(.24,.195,.135)','float3(.17,.135,.09)').replace('smoothstep(.26,.76,soilPatch)','smoothstep(.20,.80,soilPatch)').replace('v5SoilColor,.67)*(1+.085*(grainPatch-.5))','v5SoilColor,.55)*(0.82+.32*soilPatch+.14*(grainPatch-.5))').replace('smoothstep(.40,.70,v5.n(p/108','smoothstep(.32,.65,v5.n(p/108').replace('smoothstep(.085,.19,length(local','smoothstep(.11,.25,length(local');assert code!=before;n.set_editor_property('code',code);graphs.append({'material':m.get_path_name(),'expression':n.get_name(),'before':before,'after':code})
 L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
# Opaque, textured bark for the new V4 branch instances only; no original tree material changed.
p='/Game/Environment/HealingHouse/ArtV5/Materials/M_HH5_Deadwood';assert not unreal.EditorAssetLibrary.does_asset_exist(p);mat=unreal.EditorAssetLibrary.duplicate_asset('/Game/Environment/VisualV2HealingArtV4/Materials/M_HH_HandcraftedSurface',p)
for n in L.get_material_expressions(mat):
 if isinstance(n,unreal.MaterialExpressionCustom):n.set_editor_property('code','float lum=dot(C,float3(.3,.59,.11));float grain=sin(UV.y*49+sin(UV.x*16))*cos(UV.x*21);return float3(.085,.067,.043)*(.55+lum*1.6)*(1+.08*grain);')
L.recompile_material(mat);assert unreal.EditorAssetLibrary.save_loaded_asset(mat,False);bindings=[]
a=actors['ArtV4_Edge_Branches'];c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);bindings.append({'actor':a.get_name(),'component':c.get_name(),'slot':0,'before':c.get_material(0).get_path_name(),'after':mat.get_path_name()});c.set_material(0,mat)
# Use existing instances, moving some into deeper background instead of adding a continuous border.
rng=random.Random(52126);groups=[]
for name in ['ArtV4_Edge_Shrubs','ArtV4_Edge_RoadPebbles']:
 a=actors[name];c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);rows=[];count=c.get_instance_count()
 for i in range(count):
  t=c.get_instance_transform(i,True);before={'position':t.translation.to_tuple(),'scale':t.scale3d.to_tuple()}
  if 'Shrubs'in name:
   if i%3==0:t.translation.y+=rng.uniform(110,190)
   # smaller clumps and room between silhouettes, never more massive shrubs
   t.scale3d=t.scale3d*(.76 if i%3==1 else .95)
  elif i<96:
   px,py=rng.choice([(-3745,1924),(-3510,2000),(-3160,2076),(-2850,2112)])
   t.translation=unreal.Vector(rng.gauss(px,48),rng.gauss(py,32),.35);sc=rng.uniform(.38,.65);t.scale3d=unreal.Vector(sc,sc,sc*rng.uniform(.18,.28))
  else:continue
  c.update_instance_transform(i,t,True,True,True);rows.append({'index':i,'before':before,'after':{'position':t.translation.to_tuple(),'scale':t.scale3d.to_tuple()}})
 assert count==c.get_instance_count();groups.append({'actor':a.get_name(),'label':name,'count':count,'changed_instances':rows})
a=actors['ArtV5_BedsideRemedies'];before=a.get_actor_location().to_tuple();a.set_actor_location(unreal.Vector(16570,932,76),False,True)
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');j={'material_bindings':bindings,'group_adjustments':groups,'table_prop_move':{'actor':a.get_name(),'before':before,'after':a.get_actor_location().to_tuple()},'reason':'Actual QHD review; initial sandy draft was too pale and uniform; herbs were at floor level; branch tones too orange.'};(R/'Art/HealingHouse/ArtV5_ReviewFinish.json').write_text(json.dumps(j,indent=2));(R/'Art/World/VisualV2WorldArtV7/ArtV5_ReviewedPathGraphs.json').write_text(json.dumps(graphs,indent=2));(S/'ReviewFinished.json').write_text(json.dumps(j,indent=2));unreal.log('ART_V5_REVIEW_FINISHED')
