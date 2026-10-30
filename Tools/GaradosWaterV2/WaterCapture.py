"""Controlled animation inspection on the real pond specimen through the existing preview planner.
No asset/save writes. Original camera projection, speed settings, tags and natural control restored.
"""
import unreal,json,time,traceback,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GaradosWaterV2';q=json.loads((D/'Active.json').read_text());O=D/q['label'];s={'start':time.monotonic(),'phase':'init','at':0,'sample':0,'done':False};r={'checks':[],'shots':[],'samples':[],'controlled_animation_review':True};W=PC=P=H=C=S=A=V=M=Boom=None;old={};capture=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('GaradosWaterV2_'+q['label']);assert not capture.exists()
assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(O/'UserData')
def cmd(x):unreal.SystemLibrary.execute_console_command(W,x,PC)
def settings_speed(speed):
 st=M.settings;st.set_editor_property('walk_speed_override',float(speed));assert abs(M.settings.walk_speed_override-speed)<.01,'Transient speed did not update'
def foot():return A.get_actor_location()-unreal.Vector(0,0,A.get_component_by_class(unreal.CapsuleComponent).get_scaled_capsule_half_height())
def plan():
 z=M.biome_habitat.get_actor_location();p=foot();choices=[(z.x-130,z.y),(z.x+130,z.y),(z.x-80,z.y+30),(z.x+80,z.y-30)];choices.sort(key=lambda t:-math.hypot(t[0]-p.x,t[1]-p.y))
 for x,y in choices:
  if math.hypot(x-p.x,y-p.y)>100 and M.request_model_preview_goal(unreal.Vector(x,y,p.z)):return True
 return False

def row():
 ai=V.mesh.get_anim_instance();return {'time':time.monotonic()-s['start'],'phase':s['phase'],'actor':A.get_actor_location().to_tuple(),'state':str(M.behavior_state),'speed':M.current_speed,'visual_speed':V.motion_speed,'slow':ai.swim_slow_blend,'fast':ai.swim_fast_blend,'turn':V.swim_turn_input,'observe':V.swim_observe_alpha,'head':V.mesh.get_socket_location('head').to_tuple(),'mid':V.mesh.get_socket_location('spine_10').to_tuple(),'tail':V.mesh.get_socket_location('spine_19').to_tuple(),'surface':M.biome_habitat.water_surface_z,'mesh':V.mesh.get_skeletal_mesh_asset().get_path_name()}
def shot(name):
 r['shots'].append({'name':name,**row()});cmd('Shot filename="'+str(O/(name+'.png'))+'" -nosuffix')
def next_phase(phase):s.update(phase=phase,at=time.monotonic(),shot=False);(O/'Progress.json').write_text(json.dumps({'phase':phase,'shots':len(r['shots'])}))
def finish(error=None):
 if s['done']:return
 s['done']=True
 try:
  cmd('pm.TAAReview.CaptureStop')
  if M:
   M.set_movement_paused(True);settings_speed(old['speed']);M.controlled_model_preview=old['preview'];A.tags=old['tags'];P.set_actor_location(unreal.Vector(*old['player']),False,True);M.set_movement_paused(False)
  if W and 'time_dilation'in old:unreal.GameplayStatics.set_global_time_dilation(W,old['time_dilation'])
  if Boom:Boom.target_offset=unreal.Vector(*old['offset']);Boom.enable_camera_lag=old['lag']
 except Exception:r['restore_error']=traceback.format_exc();error=error or r['restore_error']
 unreal.unregister_slate_post_tick_callback(unreal._garados_capture);r.update(passed=error is None,error=error,capture=str(capture),seconds=time.monotonic()-s['start']);(O/'Result.json').write_text(json.dumps(r,indent=2,default=str));unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
def tick(dt):
 global W,PC,P,H,C,S,A,V,M,Boom
 try:
  now=time.monotonic();assert now-s['start']<300,'Bounded review'
  if s['phase']=='init':
   if now-s['start']<12:return
   ws=[w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0)]
   if not ws:return
   W=ws[0];PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
   def sub(t,o=GI):return next(x for x in unreal.ObjectIterator(t)if x.get_outer()==o)
   S=sub(unreal.PokeMonsterSaveSubsystem);C=sub(unreal.PokeMonsterWorldClock);H=sub(unreal.PokeMonsterHabitatSubsystem,W);assert S.load_game();cmd('pm.EnvPerf2.Viewport '+str(q.get('video_width',2560))+' '+str(q.get('video_height',1440)));next_phase('load');return
  if s['phase']=='load':
   if now-s['at']<4 or S.is_load_in_progress():return
   P.set_actor_location(unreal.Vector(1800,-600,50.15),False,True);next_phase('find');return
  if s['phase']=='find':
   found=[a for a in H.population if str(a.visual_species.get_internal_id())=='Garados']
   if not found:return
   A=found[0];V=next(a for a in A.get_attached_actors()if isinstance(a,unreal.PokeMonsterCreatureVisualActor));M=A.overworld_movement;Boom=P.get_component_by_class(unreal.SpringArmComponent);old['time_dilation']=unreal.GameplayStatics.get_global_time_dilation(W);unreal.GameplayStatics.set_global_time_dilation(W,float(q.get('simulation_dilation',1.)));r['simulation_dilation']=float(q.get('simulation_dilation',1.));old.update(speed=float(M.settings.walk_speed_override),preview=M.controlled_model_preview,tags=list(A.tags),offset=Boom.target_offset.to_tuple(),lag=Boom.enable_camera_lag,player=P.get_actor_location().to_tuple());M.set_movement_paused(True);M.controlled_model_preview=True;A.tags=old['tags']+['PokemonDevelopmentSpecimen'];settings_speed(35);A.set_actor_rotation(unreal.Rotator(yaw=180),False);Boom.enable_camera_lag=False;Boom.target_offset=unreal.Vector(*old['offset'])+A.get_actor_location()-P.get_actor_location();M.set_movement_paused(False);assert plan(),'No full-body-safe controlled lane';r['camera_projection']={'arm_length':Boom.target_arm_length,'rotation':str(Boom.get_editor_property('relative_rotation')),'fov':P.get_component_by_class(unreal.CameraComponent).field_of_view,'only_target_offset_changed':True};r['bones']=[str(n)for n in V.mesh.get_all_socket_names()];r['checks'].append('Real registered Garados in original pond, normal camera projection and unchanged world scale');next_phase('warm');return
  if now-s['sample']>.10:r['samples'].append(row());s['sample']=now
  if s['phase']in ['warm','slow','normal','fast','turn']and not M.is_model_preview_moving():plan()
  if s['phase']=='warm':
   if now-s['at']<7 or V.swim_observe_alpha>.02:return
   cmd('pm.TAAReview.CaptureStart '+str(capture)+' slate 30');next_phase('slow');return
  a=row();elapsed=now-s['at']
  if s['phase']=='slow':
   if not s['shot']and 22<a['visual_speed']<45 and a['slow']>.65:shot('01_Slow');s['shot']=True
   if elapsed>=4 and s['shot']:settings_speed(70);next_phase('normal')
  elif s['phase']=='normal':
   if not s['shot']and 60<a['visual_speed']<85 and a['slow']<.25:shot('02_Normal');s['shot']=True
   if elapsed>=4 and s['shot']:settings_speed(125);next_phase('fast')
  elif s['phase']=='fast':
   if not s['shot']and a['visual_speed']>110 and a['fast']>.65:shot('03_Fast');s['shot']=True
   if elapsed>=4 and s['shot']:settings_speed(70);plan();next_phase('turn')
  elif s['phase']=='turn':
   if not s['shot']and abs(a['turn'])>.45:shot('04_Turn');s['shot']=True
   if elapsed>=3 and s['shot']:
    M.set_movement_paused(True);M.controlled_model_preview=False;P.set_actor_location(unreal.Vector(720,-1090,50.15),False,True);Boom.target_offset=unreal.Vector(*old['offset'])+A.get_actor_location()-P.get_actor_location();M.set_movement_paused(False);next_phase('raising')
  elif s['phase']=='raising':
   if not s['shot']and .30<a['observe']<.80:shot('05_Raising');s['shot']=True
   if a['observe']>=.99 and s['shot']:next_phase('observe')
  elif s['phase']=='observe':
   if not s['shot']:shot('06_Observe');s['shot']=True
   if elapsed>=3:
    M.set_movement_paused(True);M.controlled_model_preview=True;P.set_actor_location(unreal.Vector(*old['player']),False,True);Boom.target_offset=unreal.Vector(*old['offset'])+A.get_actor_location()-P.get_actor_location();M.set_movement_paused(False);assert plan();next_phase('lowering')
  elif s['phase']=='lowering':
   if not s['shot']and .30<a['observe']<.75:shot('07_Lowering');s['shot']=True
   if a['observe']<.01 and s['shot']:cmd('pm.TAAReview.CaptureStop');next_phase('drain')
  elif s['phase']=='drain':
   if(capture/'Complete.txt').exists():
    assert len(r['shots'])==7
    assert not(capture/'Error.txt').exists(),(capture/'Error.txt').read_text()
    metrics=json.loads((capture/'Metrics.json').read_text());assert metrics['frames']>30,'No genuine video frames';r['capture_metrics']=metrics;r['checks'].append('All seven actual blended animation phases captured; original source controller and camera restored');finish();return
  if s['phase']in ['slow','normal','fast','turn','raising','lowering']and elapsed>40:raise AssertionError('Requested actual movement phase not observed: '+s['phase'])
 except Exception:finish(traceback.format_exc())
unreal._garados_capture=unreal.register_slate_post_tick_callback(tick)
