"""Read real imported local bone poses for before/after source-only FBX validation."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/NPCExpansion';phase=json.loads((O/'PoseAuditRequest.json').read_text())['phase'];assert phase in ('before','after');rows={}
for a in json.loads((R/'Tools/NPCExpansion/Library.json').read_text()):
 id=a['id'];audit=json.loads((O/'AnimationViews'/id/'Audit.json').read_text())
 for c in audit['clips']:
  path='/Game/Characters/NPCs/Library/'+id+'/Animations/'+('SharedSkeleton/' if a.get('reuse_mesh') else '')+c['name'];anim=unreal.load_asset(path);options=unreal.AnimPoseEvaluationOptions();frames=[]
  for f in range(17):
   pose=unreal.AnimPoseExtensions.get_anim_pose_at_time(anim,anim.get_play_length()*f/16,options);bones={}
   for b in unreal.AnimPoseExtensions.get_bone_names(pose):
    t=unreal.AnimPoseExtensions.get_bone_pose(pose,b);bones[str(b)]={'p':t.translation.to_tuple(),'q':t.rotation.to_tuple(),'s':t.scale3d.to_tuple()}
   frames.append(bones)
  rows[path.replace('/SharedSkeleton/','/')]={'seconds':anim.get_play_length(),'poses':frames}
(O/('AnimationPoses_'+phase+'.json')).write_text(json.dumps(rows))
