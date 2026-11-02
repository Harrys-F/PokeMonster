"""One guarded, map-only replacement of legacy sheets with existing project meshes."""
import unreal,json,random,sys,math,re,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualUpgradeV1';ROOT='/Game/Environment/WestlandVisualUpgradeV1';sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'Tools'));import WestlandRegionLayout as Layout
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);SUB=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);L=unreal.MaterialEditingLibrary
assert W.get_name()=='Dev_WestlandRegion'and not E.get_game_world();assert (D/'SurfaceAudit.json').exists();assert not(D/'VegetationAudit.json').exists();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
actors={a.get_actor_label():a for a in A.get_all_level_actors()};assert not any(x.startswith('WVU_')for x in actors)
original=json.loads((D/'Dev_WestlandRegion_Before.json').read_text())['actors'];rng=random.Random(211026);audit={'trees':[],'bushes':[],'groups':[],'material_derivations':[],'grounded_rocks':[]};cache={};groups={}
barriers=[a for a in actors.values()if a.actor_has_tag('BiomePlayerWaterBarrier')];ignore=barriers+list(unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterNPC))+list(unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterRestPoint))
def floor(x,y,z):
 h=unreal.SystemLibrary.line_trace_single(W,unreal.Vector(x,y,z+6000),unreal.Vector(x,y,z-10000),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,ignore,unreal.DrawDebugTrace.NONE)
 assert h,(x,y,'No existing floor');m=re.search(r'ImpactPoint=\(X=[^,]+,Y=[^,]+,Z=([^\)]+)',h.export_text());assert m,h;return float(m[1])
def hism_material(m):
 path=m.get_path_name()
 if path in cache:return cache[path]
 out=m
 if isinstance(m,unreal.Material):
  if not m.get_editor_property('used_with_instanced_static_meshes'):
   name='M_WVU_Inst_'+m.get_name();out=unreal.EditorAssetLibrary.duplicate_asset(path,ROOT+'/Materials/'+name);assert out;out.set_editor_property('used_with_instanced_static_meshes',True);L.recompile_material(out);assert unreal.EditorAssetLibrary.save_loaded_asset(out,False)
 elif isinstance(m,unreal.MaterialInstanceConstant):
  parent=hism_material(m.get_editor_property('parent'))
  if parent!=m.parent:
   name='MI_WVU_Inst_'+m.get_name();out=unreal.EditorAssetLibrary.duplicate_asset(path,ROOT+'/Materials/'+name);assert out;L.set_material_instance_parent(out,parent);assert unreal.EditorAssetLibrary.save_loaded_asset(out,False)
 if out!=m:audit['material_derivations'].append(dict(source=path,result=out.get_path_name(),reason='map-local instancing usage; original shader preserved'))
 cache[path]=out;return out

def group(label,mesh,materials=None,shadow=False,end=15000):
 if label in groups:return groups[label]
 mesh=unreal.load_asset(mesh)if isinstance(mesh,str)else mesh;assert mesh
 mats=materials or [x.material_interface for x in mesh.static_materials];mats=[hism_material(unreal.load_asset(x)if isinstance(x,str)else x)for x in mats]
 a=A.spawn_actor_from_class(unreal.Actor,unreal.Vector());a.set_actor_label('WVU_'+label);a.tags=['WestlandVisualUpgradeV1','VisualOnly_NoCollision'];a.set_folder_path('WestlandRegion/VisualUpgradeV1');root=SUB.k2_gather_subobject_data_for_instance(a)[0];h,reason=SUB.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h));assert c,reason
 # Bind supported local overrides before mesh registration can request shared usage flags.
 for i,m in enumerate(mats):c.set_material(i,m)
 c.set_static_mesh(mesh);c.set_collision_profile_name('NoCollision');c.set_editor_property('generate_overlap_events',False);c.set_cast_shadow(shadow);c.set_cull_distances(int(end*.82),end);c.set_editor_property('affect_distance_field_lighting',shadow);c.set_editor_property('affect_dynamic_indirect_lighting',shadow)
 groups[label]=c;audit['groups'].append(dict(actor=a.get_name(),label=a.get_actor_label(),mesh=mesh.get_path_name(),materials=[m.get_path_name()for m in mats],shadow=shadow,collision='NoCollision',end_cull_cm=end));return c

def put(c,x,y,z,s,yaw):
 c.add_instance(unreal.Transform(location=unreal.Vector(x,y,z),rotation=unreal.Rotator(yaw=yaw),scale=unreal.Vector(*s)),True)

def original_instances(label):
 a=actors[label];c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);return a,c,[c.get_instance_transform(i,True)for i in range(c.get_instance_count())]

base='/Game/Environment/WestlandAssetLibrary/Meshes/Trees/';paths={x:base+'SM_WLA_'+x for x in ['OakYoung_A','OakYoung_B','Birch_A','Birch_B','FruitTree_A','FruitTree_B']};paths['OakAncient_V3']='/Game/Environment/WestlandAssetLibrary/QualityV3/Meshes/Trees/SM_WLA_OakAncient_V3'
# Existing VisualV2 crown/bark material family on the same mature oak geometry.
reference=json.loads((D/'Inventory.json').read_text());oakref=next(c for c in reference['Dev_TestMap_VisualV2']if c['label']=='V2_ForestOak_0')
a,old,trees=original_instances('WR_Oak');assert len(trees)==1710
trunka,trunk,oldtrunks=original_instances('WR_TrunkCollision');trunkpoints={(round(t.translation.x,1),round(t.translation.y,1))for t in oldtrunks};added=0
for i,t in enumerate(trees):
 p=t.translation;ground=floor(p.x,p.y,p.z);e,n=Layout.en(p.x,p.y);height=306.108459*t.scale3d.z
 if -305<e<-160 and -230<n<75 and rng.random()<.28:key=rng.choice(['FruitTree_A','FruitTree_B']);height=min(height,650)
 elif height>1200 or rng.random()<.50:key='OakAncient_V3'
 else:key=rng.choice(['OakYoung_A','OakYoung_B','Birch_A','Birch_B'])
 c=group('Trees_'+key,paths[key],oakref['materials']if key=='OakAncient_V3'else None,True,18000);box=c.static_mesh.get_bounding_box();scale=height/(box.max.z-box.min.z);s=(scale*rng.uniform(.91,1.06),scale*rng.uniform(.91,1.06),scale);yaw=rng.uniform(0,360);z=ground-box.min.z*scale-.8;put(c,p.x,p.y,z,s,yaw)
 audit['trees'].append(dict(source=i,group=key,x=p.x,y=p.y,ground_z=ground,z=z,height_cm=height,scale=s,yaw=yaw))
 if(round(p.x,1),round(p.y,1))not in trunkpoints:put(trunk,p.x,p.y,ground+100,(.5,.5,2),0);added+=1
# Remove sheet geometry, keep original actor identity and its known references.
a.modify();old.clear_instances();trunka.modify();trunk.set_visibility(False,True);trunk.set_editor_property('hidden_in_game',True);audit['trunk_colliders_added']=added;audit['existing_trunk_colliders_retained']=len(oldtrunks);audit['trunk_debug_geometry_hidden']=True

a,old,bushes=original_instances('WR_Bush');assert len(bushes)==6668
for i,t in enumerate(bushes):
 p=t.translation;ground=floor(p.x,p.y,p.z);key='A'if i%3 else'B';c=group('Bush_'+key,'/Game/Environment/WestlandAssetLibrary/Meshes/Vegetation/SM_WLA_Bush_'+key,shadow=False,end=8500);b=c.static_mesh.get_bounding_box();height=max(50,min(135,97.224884*t.scale3d.z));sc=height/(b.max.z-b.min.z);s=(sc*rng.uniform(.65,.90),sc*rng.uniform(.65,.90),sc);put(c,p.x,p.y,ground-b.min.z*sc-2,s,rng.uniform(0,360));audit['bushes'].append(dict(source=i,ground_z=ground,height_cm=height))
a.modify();old.clear_instances()
# Swap only pre-existing rough grass clusters to the proven opaque VisualV2 blades.
for label,key in [('WR_GrassSmall','Short'),('WR_GrassMedium','Meadow'),('WR_GrassLarge','Woodland')]:
 a,c,ts=original_instances(label);a.modify();m=hism_material(unreal.load_asset('/Game/Environment/VisualV2EnvironmentV3/Materials/M_EQ3_Grass'));c.set_editor_property('override_materials',[m]);c.set_static_mesh(unreal.load_asset('/Game/Environment/VisualV2EnvironmentV3/Meshes/SM_EQ3_Grass'+key));c.set_cast_shadow(False);audit['groups'].append(dict(label=label,reused_instances=len(ts),mesh=c.static_mesh.get_path_name(),materials=[m.get_path_name()]))
# Correct the visibly floating visual rock pivots without changing XY, collision or terrain.
a,c,ts=original_instances('WR_RockyContours');a.modify();b=c.static_mesh.get_bounding_box()
for i,t in enumerate(ts):
 p=t.translation;g=floor(p.x,p.y,p.z);newz=g-b.min.z*t.scale3d.z-(b.max.z-b.min.z)*t.scale3d.z*.12;t.translation=unreal.Vector(p.x,p.y,newz);c.update_instance_transform(i,t,True,False,True);audit['grounded_rocks'].append(dict(instance=i,before_z=p.z,after_z=newz,ground_z=g,xy_unchanged=True))
c.mark_render_state_dirty()if hasattr(c,'mark_render_state_dirty')else None
# Small existing roots/fern/moss pockets and reeds. Not a continuous row or a new biome.
refs={x['label']:x for x in reference['Dev_TestMap_VisualV2']};paths_points=[(e,n,w)for _,points,w in Layout.PATHS for e,n in Layout.sample(points,spacing=4)];grid={}
for e,n,w in paths_points:grid.setdefault((int(e//10),int(n//10)),[]).append((e,n,w))
def clear(e,n,margin=.7):
 if abs(e-Layout.river(n))<4.5:return False
 for gx in range(int(e//10)-1,int(e//10)+2):
  for gy in range(int(n//10)-1,int(n//10)+2):
   if any(math.hypot(e-x,n-y)<w*.5+margin for x,y,w in grid.get((gx,gy),[])):return False
 return not any(math.hypot(e-x,n-y)<14 for x,y in Layout.PLACES.values())
for i,row in enumerate(audit['trees']):
 if i%3:continue
 e,n=Layout.en(row['x'],row['y']);e+=rng.uniform(-2.6,2.6);n+=rng.uniform(-2.6,2.6)
 if not clear(e,n):continue
 kind=['Ferns','Roots','Moss'][i//3%3];ref=refs['EQ3_'+kind];c=group('Forest_'+kind,ref['mesh'],ref['materials'],False,6500);x,y,_=Layout.world(e,n);g=floor(x,y,row['ground_z']);sc=rng.uniform(.46,.8);b=c.static_mesh.get_bounding_box();put(c,x,y,g-b.min.z*sc-1,(sc,sc,sc),rng.uniform(0,360))
for j in range(170):
 n=-295+j*3.45;e=Layout.river(n)+rng.choice([-1,1])*rng.uniform(4.4,6.3)
 if not clear(e,n,.35):continue
 x,y,_=Layout.world(e,n);g=floor(x,y,Layout.water(n)*100);c=group('Shore_Reeds','/Game/Environment/VisualV2WorldArtV5/Meshes/SM_WA5_ReedTuft',shadow=False,end=7500);sc=rng.uniform(.60,1.05);b=c.static_mesh.get_bounding_box();put(c,x,y,g-b.min.z*sc-2,(sc,sc,sc),rng.uniform(0,360))
for row in audit['groups']:
 if row['label'].startswith('WVU_'):row['instances']=groups[row['label'][4:]].get_instance_count()
assert sum(c.get_instance_count()for k,c in groups.items()if k.startswith('Trees_'))==1710
assert old.get_instance_count()==0
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages(),'Shared asset auto-edit detected; do not save shared originals'
assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_WestlandRegion');(D/'VegetationAudit.json').write_text(json.dumps(audit,indent=2));unreal.log('WESTLAND_VISUAL_VEGETATION_SAVED trees1710 bushes6668')
