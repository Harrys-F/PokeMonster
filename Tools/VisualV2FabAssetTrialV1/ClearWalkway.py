"""Move the proven three blocking trial rock groups away from the original forest route."""
import unreal,json,random,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2FabAssetTrialV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert not E.get_game_world();A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);SM=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);rng=random.Random(261105);rows=[]
for a in A.get_all_level_actors():
 if not a.get_actor_label().startswith('FAT_Outcrop'):continue
 a.modify();c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);m=c.static_mesh;assert m.get_path_name().startswith('/Game/Fab/VisualV2TrialLocal/Rocks/');SM.remove_collisions(m);SM.add_simple_collisions(m,unreal.ScriptCollisionShapeType.NDOP26);assert SM.get_convex_collision_count(m)==1;assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
 for i in range(c.get_instance_count()):
  t=c.get_instance_transform(i,True);old=t.translation;new=unreal.Vector(rng.uniform(-1220,-840),rng.uniform(1480,1820),old.z);t.translation=new;assert c.update_instance_transform(i,t,True,True,True);rows.append(dict(actor=a.get_actor_label(),index=i,before=old.to_tuple(),after=new.to_tuple()))
for x,y in [(-1886,1518),(-1860,1470),(-1800,1400)]:
 parts=unreal.SystemLibrary.sphere_overlap_components(W,unreal.Vector(x,y,50),65,[unreal.ObjectTypeQuery.ECC_WORLD_STATIC],unreal.PrimitiveComponent,[]);assert not any(c.get_owner().get_actor_label().startswith('FAT_Outcrop')for c in(parts or[])),(x,y)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2');(D/'WalkwayCleared.json').write_text(json.dumps(rows,indent=2))
