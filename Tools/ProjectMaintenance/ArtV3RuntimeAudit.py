"""Read-only runtime shadow and healer-facing checks alongside the real input footrun."""
import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ArtPassV3';D=S/'Acceptance'/json.loads((S/'AcceptanceRequest.json').read_text())['label'];w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0));p=unreal.GameplayStatics.get_player_pawn(w,0);h=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor) if a.source_actor and a.source_actor.get_actor_label()=='V2_House_HouseHealer');pc=unreal.GameplayStatics.get_player_controller(w,0);cut=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterBuildingCutaway) if a.get_actor_label()=='V2_House_HouseCutaway');state={'time':0.,'interior_frames':0,'exterior_frames':0,'healer_talk_frames':0,'shots':0,'phase':None,'settle':0.,'talk_time':0.,'errors':[]}
def tick(dt):
 try:
  state['time']+=dt;inside=cut.is_viewer_in_relocated_room(p.get_actor_location());state['last_position']=p.get_actor_location().to_tuple()
  if state['phase']!=inside:state['phase']=inside;state['settle']=0.
  state['settle']+=dt
  if state['settle']>.3:
   for c in p.get_components_by_class(unreal.PrimitiveComponent):
    ch=c.get_editor_property('lighting_channels')
    if inside:assert not c.cast_shadow and (ch.channel0,ch.channel1,ch.channel2)==(False,True,False)
   if inside:state['interior_frames']+=1
   else:
    mesh=p.get_component_by_class(unreal.SkeletalMeshComponent);assert mesh.cast_shadow and mesh.get_editor_property('lighting_channels').channel0;state['exterior_frames']+=1
  if h.is_conversing():
   state['talk_time']+=dt
   if state['talk_time']>.7:
    d=p.get_actor_location()-h.get_actor_location();expected=math.degrees(math.atan2(d.y,d.x))+h.forward_yaw_offset;delta=(h.get_actor_rotation().yaw-expected+180)%360-180;assert abs(delta)<2,delta;assert h.static_visual.is_visible() and h.static_visual.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION;state['healer_talk_frames']+=1
    if state['shots']<4 and state['talk_time']>.7+state['shots']*.3:
     unreal.SystemLibrary.execute_console_command(w,'Shot showui filename="'+str(D/('SilverLady_Healing_'+str(state['shots'])+'.png'))+'"',pc);state['shots']+=1
  if (D/'FootTest.json').exists():
   assert all(state[k]>0 for k in ['interior_frames','exterior_frames','healer_talk_frames']);state['passed']=True;unreal.unregister_slate_post_tick_callback(unreal._artv3_runtime);(D/'RuntimeAudit.json').write_text(json.dumps(state,indent=2))
 except Exception:
  import traceback
  state['passed']=False;state['errors'].append(traceback.format_exc());unreal.unregister_slate_post_tick_callback(unreal._artv3_runtime);(D/'RuntimeAudit.json').write_text(json.dumps(state,indent=2));raise
unreal._artv3_runtime=unreal.register_slate_post_tick_callback(tick)
