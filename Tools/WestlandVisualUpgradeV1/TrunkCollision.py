"""Use the models' already-authored trunk-only UCX hulls; no new collision mesh or source edit."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualUpgradeV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_WestlandRegion');W=E.get_editor_world();S=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);rows=[]
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
 label=a.get_actor_label()
 if label.startswith('WVU_Trees_'):
  c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);m=c.static_mesh;simple=S.get_simple_collision_count(m);convex=S.get_convex_collision_count(m);assert simple+convex>0,(label,'No authored trunk hull; no fallback allowed');a.modify();c.set_collision_profile_name('BlockAll');c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_IGNORE);rows.append(dict(group=label,mesh=m.get_path_name(),instances=c.get_instance_count(),simple=simple,convex=convex,source='existing authored trunk-only asset collision',pawn='Block',camera='Block',visibility='Ignore'))
 elif label=='WR_TrunkCollision':
  a.modify();c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);c.set_collision_profile_name('NoCollision');assert not c.visible
assert len(rows)==7;assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_WestlandRegion');(D/'TrunkCollisionAudit.json').write_text(json.dumps(rows,indent=2));unreal.log('WESTLAND_VISUAL_AUTHORED_TRUNK_HULLS_SAVED')
