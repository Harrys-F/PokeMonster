"""Fix only our new map: private instanced materials; native individual tree reveal; reload original auto-usage edits."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);ES=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);w=E.get_editor_world();D='/Game/Environment/BiomeTestV1/Materials';L=unreal.MaterialEditingLibrary
assert not E.get_game_world()and w.get_name()=='Dev_BiomeTestMap_V1'
dirty=list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages());assert all('/BiomeTestV1/'not in p.get_path_name()for p in dirty)
clones={}
def private(m):
 if not m:return None
 path=m.get_path_name()
 if path.startswith(D):return m
 if path in clones:return clones[path]
 name=m.get_name()+'_Biome';dst=D+'/'+name
 assert not unreal.EditorAssetLibrary.does_asset_exist(dst),dst
 n=unreal.EditorAssetLibrary.duplicate_asset(path,dst);assert n;clones[path]=n
 if isinstance(n,unreal.Material):
  n.set_editor_property('used_with_instanced_static_meshes',True);L.recompile_material(n)
 elif isinstance(n,unreal.MaterialInstanceConstant):
  parent=m.get_editor_property('parent');L.set_material_instance_parent(n,private(parent));L.update_material_instance(n)
 assert unreal.EditorAssetLibrary.save_loaded_asset(n,False);return n
converted=0;hism_count=0
for a in list(ES.get_all_level_actors()):
 for c in a.get_components_by_class(unreal.HierarchicalInstancedStaticMeshComponent):
  if not c.static_mesh:continue
  tree=c.static_mesh.get_name()in['SM_WLA_OakAncient_V3','SM_WLA_Birch_A']
  if tree:
   assert a.actor_has_tag('BiomeTestV1')
   for i in range(c.get_instance_count()):
    t=c.get_instance_transform(i,True);n=ES.spawn_actor_from_class(unreal.StaticMeshActor,t.translation,t.rotation.rotator());n.set_actor_label('Biome_RevealTree_'+str(converted));n.set_folder_path('BiomeV1/Trees');n.tags=['BiomeTestV1'];n.set_actor_scale3d(t.scale3d);x=n.static_mesh_component;x.set_static_mesh(c.static_mesh);x.set_collision_profile_name('NoCollision')
    for j in range(c.get_num_materials()):x.set_material(j,c.get_material(j))
    x.set_cast_shadow(True);converted+=1
   assert ES.destroy_actor(a)
  else:
   for j in range(c.get_num_materials()):c.set_material(j,private(c.get_material(j)))
   hism_count+=1
# Ensure Unreal Array edits are explicitly assigned back to the actor property.
for a in ES.get_all_level_actors():
 label=a.get_actor_label();tags=list(a.tags)
 if label.startswith('Biome_WaterBarrier_'):tags.append('BiomePlayerWaterBarrier')
 if any(label.startswith(p)for p in ['Biome_Trunk_','Biome_CaveWallCollision','Biome_RuinWallCollision','Biome_BridgeRail','Biome_MapLimit']):tags.append('CreatureNoWalk')
 a.tags=list(dict.fromkeys(tags))
# These were clean before our map build; only automatic usage edits arose in this session.
if dirty:
 ok,error=unreal.EditorLoadingAndSavingUtils.reload_packages(dirty,unreal.ReloadPackagesInteractionMode.ASSUME_POSITIVE);assert ok,str(error)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages(),[p.get_path_name()for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_BiomeTestMap_V1')
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
r={'trees_with_original_reveal':converted,'private_hism_groups':hism_count,'private_materials':{k:v.get_path_name()for k,v in clones.items()},'reloaded_original_packages_without_save':[p.get_path_name()for p in dirty]}
(R/'Saved/BiomeTestV1/MaterialIsolation.json').write_text(json.dumps(r,indent=2));unreal.log('BIOME_PRIVATE_MATERIALS_READY '+str(r))
