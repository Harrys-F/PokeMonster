"""Relocate only regional rock instances obstructing the corrected bank path.
During PIE, adjust only its runtime instances and record placements in JSON.
After StopPIE, replay that JSON in the editor and save the owned map. Never move the pawn.
"""
import unreal,json,math,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'Tools'));import WestlandRegionLayout as L;import importlib;importlib.reload(L)
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);w=E.get_game_world();world=w or E.get_editor_world();assert 'Dev_WestlandRegion' in world.get_name()
actors=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor) if w else A.get_all_level_actors();a=next(a for a in actors if a.get_actor_label()=='WR_RockyContours');c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
points=L.sample(L.PATHS[5][1]);changes=[];saved=R/'Art/World/WestlandRegion/WestlandRegion_UferClearance.json'
if not w and saved.exists():
 changes=json.loads(saved.read_text())
 for item in changes:
  t=c.get_instance_transform(item['instance'],True);e,n=item['new_m'];t.translation=unreal.Vector(*L.world(e,n,L.height(e,n)));c.update_instance_transform(item['instance'],t,True,True,True)
else:
 for i in range(c.get_instance_count()):
  t=c.get_instance_transform(i,True);q=t.translation;e,n=L.en(q.x,q.y)
  if min(math.hypot(e-x,n-y) for x,y in points)<4.7:
   ee=L.river(n)+22;t.translation=unreal.Vector(*L.world(ee,n,L.height(ee,n)));c.update_instance_transform(i,t,True,True,True);changes.append({'instance':i,'old_m':[e,n],'new_m':[ee,n]})
 (R/'Saved/WestlandRegion/UferClearance.json').write_text(json.dumps(changes,indent=2));saved.write_text(json.dumps(changes,indent=2))
unreal.log('REGION_UFER_CLEAR '+str(len(changes)))
if not w:unreal.EditorLoadingAndSavingUtils.save_map(world,L.MAP)
