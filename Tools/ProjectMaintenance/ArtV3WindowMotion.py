"""Real game-camera temporal sequence. No renderer toggles or saved map changes."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ArtPassV3';j=json.loads((S/'WindowRequest.json').read_text());O=S/j['label'];O.mkdir(exist_ok=False);w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0));p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);ss=next(s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if s.get_world()==w);move=next(a for a in unreal.ObjectIterator(unreal.InputAction) if a.get_outer()==p and a.get_name()=='MoveAction')
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Viewport 1280 720');points=[('InteriorStill',16900,670,0),('InteriorWalk',16900,670,1),('ExteriorApproach',-4090,470,1),('ExteriorReverse',-3700,700,-1)];state={'i':0,'t':0.,'n':0,'placed':False,'shot':0.,'rows':[]}
def tick(dt):
 try:
  st=state;st['t']+=dt
  if st['i']>=len(points):
   ss.inject_input_vector_for_action(move,unreal.Vector(),[],[]);unreal.unregister_slate_post_tick_callback(unreal._artv3_windows)
   for row in st['rows']:
    q=Path(row['file']);found=list(O.glob(q.stem+'*.png'));assert len(found)==1;row['requested_filename']=row['file'];row['file']=str(found[0])
   (O/'Result.json').write_text(json.dumps(st['rows'],indent=2));return
  name,x,y,walking=points[st['i']]
  if not st['placed']:p.set_actor_location(unreal.Vector(x,y,48.15),False,True);p.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();st['placed']=True
  if 2<st['t']<8:ss.inject_input_vector_for_action(move,unreal.Vector(.32*walking,.45*walking,0),[],[])
  else:ss.inject_input_vector_for_action(move,unreal.Vector(),[],[])
  if st['t']>2 and st['t']-st['shot']>.30:
   f=O/(name+'_'+str(st['n']).zfill(3)+'.png');unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(f)+'"',pc);st['shot']=st['t'];st['n']+=1;st['rows'].append({'name':name,'file':str(f),'time':st['t'],'player':p.get_actor_location().to_tuple(),'camera':pc.player_camera_manager.get_camera_location().to_tuple(),'rotation':pc.player_camera_manager.get_camera_rotation().to_tuple(),'viewport':list(pc.get_viewport_size())})
  if st['t']>8:st.update(i=st['i']+1,t=0.,placed=False,shot=0.)
 except Exception:
  import traceback
  unreal.unregister_slate_post_tick_callback(unreal._artv3_windows);(O/'Failure.txt').write_text(traceback.format_exc());raise
unreal._artv3_windows=unreal.register_slate_post_tick_callback(tick)
