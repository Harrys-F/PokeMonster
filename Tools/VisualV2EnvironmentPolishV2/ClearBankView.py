"""Local bank-height correction from actual Third-Person review; no asset changes."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2EnvironmentPolishV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();W=E.get_editor_world();A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);rows=[]
for a in A.get_all_level_actors():
 p=a.get_actor_location();label=a.get_actor_label()
 if not(label.startswith('V2_Bush_P2D_')and -1200<p.x<1300 and -800<p.y<0):continue
 c=a.get_component_by_class(unreal.StaticMeshComponent);m=c.static_mesh;b=m.get_bounding_box();old=a.get_actor_scale3d();height=(b.max.z-b.min.z)*old.z;factor=min(1,58/max(1,height))
 if factor<1:a.modify();a.set_actor_scale3d(old*factor);rows.append(dict(name=a.get_name(),label=label,old_height=height,new_height=height*factor,scale_factor=factor,original_mesh_retained=True))
assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2');(D/'BankViewCorrection.json').write_text(json.dumps(rows,indent=2))
