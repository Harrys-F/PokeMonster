"""Read-only blocker evidence for the unchanged legacy full walking route."""
import unreal,json,math,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/GlumandaV11/Acceptance'/json.loads((R/'Saved/GlumandaV11/AcceptanceRequest.json').read_text())['label']
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);result={'read_only':True,'blockers':[]};seen=set();previous=None;still=0
def tick(dt):
 global previous,still
 try:
  q=p.get_actor_location();still=still+dt if previous and(q-previous).length()<.1 else 0;previous=q
  steps=json.loads((O/'FootProgress.json').read_text())if(O/'FootProgress.json').exists()else[]
  last=steps[-1]['name']if steps else''
  if still>1 and last=='NorthEast' and last not in seen:
   seen.add(last);end=unreal.Vector(-1700,1220,q.z);h=unreal.SystemLibrary.capsule_trace_single(w,q,end,28,48,unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[p],unreal.DrawDebugTrace.NONE,True)
   row={'position':q.to_tuple(),'target':end.to_tuple(),'capsule_trace':str(h),'nearby':[]}
   for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
    c,e=a.get_actor_bounds(True)
    if abs(c.x-q.x)<e.x+45 and abs(c.y-q.y)<e.y+45 and c.z+e.z>10 and c.z-e.z<150:
     row['nearby'].append({'actor':a.get_path_name(),'label':a.get_actor_label(),'class':a.get_class().get_name(),'location':a.get_actor_location().to_tuple(),'bounds':[c.to_tuple(),e.to_tuple()]})
   result['blockers'].append(row);(O/'BlockerObservation.json').write_text(json.dumps(result,indent=2))
  if(O/'FootTest.json').exists():
   unreal.unregister_slate_post_tick_callback(unreal._testground_foot_watch);result['foot_passed']=json.loads((O/'FootTest.json').read_text())['passed'];(O/'BlockerObservation.json').write_text(json.dumps(result,indent=2))
 except Exception:
  unreal.unregister_slate_post_tick_callback(unreal._testground_foot_watch);result['error']=traceback.format_exc();(O/'BlockerObservation.json').write_text(json.dumps(result,indent=2))
unreal._testground_foot_watch=unreal.register_slate_post_tick_callback(tick)
