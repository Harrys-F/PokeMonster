"""One-frame A/B terrain-query diagnosis, with other fish collision/position restored in finally."""
import unreal,time,json,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GaradosWaterV2';q=json.loads((D/'Active.json').read_text());O=D/q['label'];s={'at':time.monotonic(),'done':False};W=PC=None

def finish(r):
 if s['done']:return
 s['done']=True;unreal.unregister_slate_post_tick_callback(unreal._garados_peer_probe);(O/'Result.json').write_text(json.dumps(r,indent=2,default=str))
 if W:unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
def tick(dt):
 global W,PC
 try:
  assert time.monotonic()-s['at']<140
  if time.monotonic()-s['at']<16:return
  worlds=[w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0)]
  if not worlds:return
  W=worlds[0];PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0);P.set_actor_location(unreal.Vector(1800,-600,50.15),False,True);H=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterHabitatSubsystem)if x.get_outer()==W);fish={str(a.visual_species.get_internal_id()):a for a in H.population if str(a.visual_species.get_internal_id())in ['Garados','Karpador']}
  if len(fish)!=2:return
  if 'fish_at'not in s:s['fish_at']=time.monotonic();return
  if time.monotonic()-s['fish_at']<4:return
  a,b=fish['Garados'],fish['Karpador'];m=a.overworld_movement;cap=a.get_component_by_class(unreal.CapsuleComponent);foot=a.get_actor_location()-unreal.Vector(0,0,cap.get_scaled_capsule_half_height());before=b.get_actor_location();coll=b.get_actor_enable_collision();rows=[]
  try:
   # The contact capsules do not overlap at 350 cm separation (205 + 40 cm).
   for x,y in [(350,0),(-350,0),(0,350),(0,-350)]:
    target=unreal.Vector(foot.x+x,foot.y+y,11.2);b.set_actor_location(target,False,True);b.set_actor_enable_collision(True);blocked=m.project_walkable(foot);b.set_actor_enable_collision(False);clear=m.project_walkable(foot);rows.append({'fish_offset':[x,y],'garados_foot':foot.to_tuple(),'with_fish_collision':str(blocked),'without_fish_collision':str(clear)})
  finally:b.set_actor_location(before,False,True);b.set_actor_enable_collision(coll)
  shore=[];p0=P.get_actor_location()
  try:
   for x,y in [(720,-1100),(1620,-1800),(720,-2500),(-180,-1800),(1300,-1200)]:
    P.set_actor_location(unreal.Vector(x,y,50.15),False,True);shore.append({'player':P.get_actor_location().to_tuple(),'distance':float((P.get_actor_location()-a.get_actor_location()).length()),'can_interact':a.can_interact(P),'input_locked':P.is_overworld_input_locked()})
  finally:P.set_actor_location(p0,False,True)
  finish({'passed':True,'checks':[],'shore':shore,'probe':rows,'restored_peer':b.get_actor_location().to_tuple(),'original_peer':before.to_tuple(),'original_peer_collision':coll})
 except Exception:finish({'passed':False,'checks':[],'error':traceback.format_exc()})
unreal._garados_peer_probe=unreal.register_slate_post_tick_callback(tick)
