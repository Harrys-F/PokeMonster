"""Short animation contact probe without screenshot I/O or a performance benchmark."""
import unreal,json,math,statistics
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ZunderlaufV1/ContactsProbeForeground';O.mkdir(exist_ok=False);w=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0));wild=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor));wild.set_actor_tick_enabled(False);a=next(x for x in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterCreatureVisualActor));original=a.get_actor_transform();center=unreal.Vector(-810,-1520,1.28567);phases=list(range(0,360,45));s={'i':0,'t':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'rows':[],'placed':False}
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._zunderlauf_contacts);a.set_actor_transform(original,False,True);result={}
 for yaw in phases:
  rows=[r for r in s['rows']if r['yaw']==yaw];distances=[]
  for key in ['left','right']:
   if not rows:continue
   bottom=min(r[key][2]for r in rows)
   for prev,now in zip(rows,rows[1:]):
    if prev['t']<.7 or now['time']-prev['time']>.15 or any(abs(r[key][2]-bottom)>.03 for r in [prev,now]):continue
    distances.append(math.dist(prev[key][:2],now[key][:2]))
  result[str(yaw)]={'stance_pairs':len(distances),'median_slip_cm':statistics.median(distances)if distances else None,'max_slip_cm':max(distances)if distances else None}
 (O/'Result.json').write_text(json.dumps({'runtime_blend_checks_passed':error is None,'stance_metric_status':'available'if all(x['stance_pairs']>0 for x in result.values())else'inconclusive','error':error,'measurement':'World-space ankle motion in consecutive flat stance samples after .7s, <=.15s spacing, no screenshot I/O; not a full shoe/terrain or pixel-lock guarantee','directions':result,'rows':s['rows']},indent=2))
def tick(editor_dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);dt=now-s['last'];s['last']=now
  if dt<=0:return
  if s['i']==len(phases):finish();return
  yaw=phases[s['i']];s['t']+=dt
  if not s['placed']:a.set_actor_location(center,False,True);a.set_actor_rotation(unreal.Rotator(yaw=yaw),True);s['placed']=True
  v=unreal.Vector(math.cos(math.radians(yaw)),math.sin(math.radians(yaw)),0);a.set_actor_location(a.get_actor_location()+v*35*dt,False,True)
  if s['t']>.7:assert a.mesh.get_anim_instance().walk_blend>.9 and a.mesh.get_anim_instance().reaction_blend<.01
  s['rows'].append({'yaw':yaw,'t':s['t'],'time':now,'position':a.get_actor_location().to_tuple(),'speed':a.motion_speed,'left':a.mesh.get_socket_location('foot_L').to_tuple(),'right':a.mesh.get_socket_location('foot_R').to_tuple()})
  if s['t']>=3.:s.update(i=s['i']+1,t=0.,placed=False)
 except Exception:
  import traceback
  finish(traceback.format_exc());raise
unreal._zunderlauf_contacts=unreal.register_slate_post_tick_callback(tick)
