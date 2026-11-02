"""Restore recorded original bindings/positions in disposable runtime only, never save."""
import unreal,json,runpy,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2FabAssetTrialV1';label=json.loads((D/'Request.json').read_text())['label'];W=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0));actors={a.get_name():a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)};before=json.loads((D/'SceneBefore.json').read_text())['actors'];changed=json.loads((D/'Authored.json').read_text())['changes'];rows=[]
for a in actors.values():
 if a.actor_has_tag('VisualV2FabAssetTrialV1'):a.set_actor_hidden_in_game(True);a.set_actor_enable_collision(False)
for row in changed:
 a=actors[row['actor']];b=before[row['actor']];p,q,s=b['transform'];a.set_actor_location(unreal.Vector(*p),False,True);a.set_actor_rotation(unreal.Rotator(yaw=math.degrees(2*math.atan2(q[2],q[3]))),False);a.set_actor_scale3d(unreal.Vector(*s))
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  old=next(x for x in b['components']if x['name']==c.get_name());source=old['props'].get('static_mesh')
  if source:c.set_static_mesh(unreal.load_asset(source))
  for i,m in enumerate(old['materials']):c.set_material(i,unreal.load_asset(m)if m else None)
 rows.append(a.get_name())
(D/(label+'_Reconstruction.json')).write_text(json.dumps(dict(changed_actor_names=rows,recorded_original_scene='SceneBefore.json',runtime_only=True,no_disk_asset_or_map_saves=True),indent=2));runpy.run_path(str(R/'Tools/VisualV2FabAssetTrialV1/CaptureBenchmark.py'),run_name='__main__')
