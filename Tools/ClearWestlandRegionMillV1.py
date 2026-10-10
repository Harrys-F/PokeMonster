"""Relocate own rock instances that obstruct the mill's forecourt/game-camera view.
Record during PIE, then replay in the editor after StopPIE. No shared mesh change.
"""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'Tools'));import WestlandRegionLayout as L
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_game_world();actors=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor) if w else unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors();assert 'Dev_WestlandRegion' in (w or E.get_editor_world()).get_name();a=next(a for a in actors if a.get_actor_label()=='WR_RockyContours');c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);f=R/'Art/World/WestlandRegion/WestlandRegion_MillClearance.json';changes=[]
if not w and f.exists():changes=json.loads(f.read_text())
else:
 for i in range(c.get_instance_count()):
  t=c.get_instance_transform(i,True);e,n=L.en(t.translation.x,t.translation.y)
  if 138<e<159 and -250<n<-232:changes.append({'instance':i,'old_m':[e,n],'new_m':[170+len(changes)*5,n]})
 f.write_text(json.dumps(changes,indent=2))
for v in changes:
 t=c.get_instance_transform(v['instance'],True);e,n=v['new_m'];t.translation=unreal.Vector(*L.world(e,n,L.height(e,n)));c.update_instance_transform(v['instance'],t,True,True,True)
if not w:unreal.EditorLoadingAndSavingUtils.save_map(E.get_editor_world(),L.MAP)
unreal.log('REGION_MILL_CLEAR '+str(len(changes)))
