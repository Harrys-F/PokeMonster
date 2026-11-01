"""Opt-in real VisualV2 pond review, unchanged camera/planner, own save storage only.
Normal-time functional run first. Optional separate fixed-step capture is clearly labelled.
"""
import unreal,json,time,math,traceback,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GaradosPolishV3';q=json.loads((D/'Active.json').read_text());O=D/q['label'];s={'start':time.monotonic(),'phase':'init','at':0,'sample_at':0,'busy':False,'done':False};r={'checks':[],'samples':[],'shots':[],'controlled_motion_review':True,'fixed_step_review':q.get('fixed_step_review',False),'physical_gamepad_test':False};W=PC=P=A=V=M=S=None;old={};shot_pipeline=q.get('recording_pipeline')=='screenshot_request';capture=(O/'Frames')if shot_pipeline else R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('GaradosPolishV3_'+q['label']);capture_tool=None;assert not capture.exists()
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def now():return unreal.GameplayStatics.get_time_seconds(W)
def stage(name):s.update(phase=name,at=now(),shot=False);(O/'Progress.json').write_text(json.dumps({'phase':name,'shots':len(r['shots']),'wall_seconds':time.monotonic()-s['start']}))
def speed(v):M.settings.set_editor_property('walk_speed_override',float(v));assert M.settings.walk_speed_override==v

def shore(x=720,y=-1090,yaw=-90):
 P.set_actor_location(unreal.Vector(x,y,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();P.get_editor_property('ThirdPersonBoom').set_world_rotation(unreal.Rotator(yaw=yaw),False,False)
def foot():return A.get_actor_location()-unreal.Vector(0,0,A.get_component_by_class(unreal.CapsuleComponent).get_scaled_capsule_half_height())
def goal():
 c=M.biome_habitat.get_actor_location();p=foot();choices=[(c.x-130,c.y),(c.x+130,c.y),(c.x,c.y-130),(c.x,c.y+130),(c.x-80,c.y+30),(c.x+80,c.y-30),(c.x-70,c.y-100),(c.x+70,c.y+100)];choices += [(c.x+x,c.y+y)for x in range(-180,181,60)for y in range(-180,181,60)if x*x+y*y<=180*180];choices.sort(key=lambda xy:-math.dist((p.x,p.y),xy))
 return any(math.dist((p.x,p.y),xy)>100 and M.request_model_preview_goal(unreal.Vector(xy[0],xy[1],p.z))for xy in choices)
def sample():
 ai=V.mesh.get_anim_instance();cam=PC.player_camera_manager;return {'game_seconds':now(),'phase':s['phase'],'position_cm':A.get_actor_location().to_tuple(),'state':str(M.behavior_state),'speed':M.current_speed,'visual_speed':V.motion_speed,'slow':ai.swim_slow_blend,'fast':ai.swim_fast_blend,'observe':V.swim_observe_alpha,'turn':V.swim_turn_input,'heading_offsets':list(V.swim_body_yaw_offsets),'head_cm':V.mesh.get_socket_location('head').to_tuple(),'mid_cm':V.mesh.get_socket_location('spine_10').to_tuple(),'tail_cm':V.mesh.get_socket_location('spine_19').to_tuple(),'camera_cm':cam.get_camera_location().to_tuple(),'camera_pitch':cam.get_camera_rotation().pitch,'camera_yaw':cam.get_camera_rotation().yaw,'arm_cm':P.get_editor_property('ThirdPersonBoom').target_arm_length}
def shot(name):
 row=sample();assert abs(row['camera_pitch']+12)<.02;assert P.is_third_person_camera();r['shots'].append({'name':name,**row});
 if not(shot_pipeline and q.get('recording')):cmd('Shot filename="'+str(O/(name+'.png'))+'" -nosuffix')
def restore_motion():
 if M and old:
  M.set_movement_paused(True);speed(old['speed']);M.controlled_model_preview=old['preview'];A.tags=old['tags'];M.set_movement_paused(False)
def finish(error=None):
 if s['done']:return
 s['done']=True
 try:
  if q.get('recording'):
   if capture_tool:capture_tool.stop()
   else:cmd('pm.TAAReview.CaptureStop')
  if not s.get('captured'):restore_motion()
  if 'original_first'in s:Enc.reorder_party(s['original_first'],0)
 except Exception:r['restore_error']=traceback.format_exc();error=error or r['restore_error']
 unreal.unregister_slate_post_tick_callback(unreal._garados_polish_review);r.update(passed=error is None,error=error,seconds=time.monotonic()-s['start'],capture=str(capture)if q.get('recording')else None);(O/'Result.json').write_text(json.dumps(r,indent=2,default=str))
 if not q.get('pie')and W:unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
def tick(dt):
 global W,PC,P,H,C,S,Enc,Inv,A,V,M,capture_tool
 if s['busy']or s['done']:return
 s['busy']=True
 try:
  assert time.monotonic()-s['start']<q.get('timeout',420),'Bounded review'
  if s['phase']=='init':
   if time.monotonic()-s['start']<12:return
   W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()if q.get('pie')else next((w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0)),None)
   if not W:return
   assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D),'Never use user save storage'
   PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
   def sub(t,o=GI):return next(x for x in unreal.ObjectIterator(t)if x.get_outer()==o)
   S=sub(unreal.PokeMonsterSaveSubsystem);Enc=sub(unreal.PokeMonsterEncounterSubsystem);Inv=sub(unreal.PokeMonsterInventorySubsystem);C=sub(unreal.PokeMonsterWorldClock);H=sub(unreal.PokeMonsterHabitatSubsystem,W)
   if q.get('pie'):assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_GaradosPolishV3')
   assert S.load_game(),S.get_last_storage_message();cmd('pm.Evolution.Auto 0');stage('load');return
  if s['phase']=='load':
   if now()-s['at']<3 or S.is_load_in_progress():return
   assert P.is_third_person_camera();cmd('pm.EnvPerf2.Viewport 2560 1440');
   if q.get('pie'):cmd('pm.WorldClock set 1 12 0');cmd('pm.WorldClock resume')

   team=list(Enc.get_player_party());s['original_first']=team[0].instance_id
   small=next((x for x in team if str(x.species.get_internal_id())=='Enton'),None)
   if small:assert Enc.reorder_party(small.instance_id,0);r['checks'].append('Only own QA party temporarily selects existing Enton buddy to keep water specimen visible')
   P.set_actor_location(unreal.Vector(1800,-600,50.15),False,True);stage('find');return
  if s['phase']=='find':
   found=[a for a in H.population if str(a.visual_species.get_internal_id())=='Garados']
   if not found:return
   A=found[0];V=next(x for x in A.get_attached_actors()if isinstance(x,unreal.PokeMonsterCreatureVisualActor));M=A.overworld_movement;assert V.using_swim_mesh;assert '/WaterV3/'in unreal.load_asset('/Game/Characters/Creatures/Garados/MeshyV1/DA_Garados_Presentation').swim_clip.get_path_name();old.update(speed=M.settings.walk_speed_override,preview=M.controlled_model_preview,tags=list(A.tags),player=P.get_actor_location().to_tuple());r['original_water_draft']=M.get_editor_property('WaterDraftOverrideCm');r['graphics']={k:unreal.SystemLibrary.get_console_variable_float_value(k)for k in ['r.ScreenPercentage','r.TemporalAA.Upsampling','r.Lumen.HardwareRayTracing','r.Lumen.FinalGatherMethod','r.Shadow.Virtual.SMRT.RayCountDirectional','r.DefaultBackBufferPixelFormat']};assert list(r['graphics'].values())[:5]==[75,1,0,0,4];M.set_movement_paused(True);M.controlled_model_preview=True;A.tags=old['tags']+['PokemonDevelopmentSpecimen'];shore();stage('warm');return
  if capture_tool:capture_tool.tick(now())
  if now()-s['sample_at']>=.10 and A:
   row=sample();r['samples'].append(row);s['sample_at']=now();assert abs(row['camera_pitch']+12)<.02;assert M.is_inside_habitat(foot());assert V.using_swim_mesh
  elapsed=now()-s['at']
  if s['phase']in ['slow','normal','fast','turn']and not M.is_model_preview_moving():goal()
  if s['phase']=='warm':
   if elapsed<8 or V.swim_observe_alpha>.01:return
   r['checks'].append('Real naturally spawned Garados, original pond/depth and unchanged ThirdPerson/profile C')
   if q.get('recording'):
    if shot_pipeline:capture_tool=runpy.run_path(str(R/'Tools/GaradosPolishV3/ReviewCapture.py'))['ScreenshotReview'](W,capture,now())
    else:cmd('pm.TAAReview.CaptureStart '+str(capture))
   stage('idle');return
  a=sample()
  if s['phase']=='idle':
   if elapsed<2:return
   shot('01_Idle');speed(35);M.set_movement_paused(False);assert goal();stage('slow');return
  if s['phase']=='slow':
   if not s['shot']and 22<a['visual_speed']<45 and a['slow']>.65:shot('02_Slow');s['shot']=True
   if elapsed>=3.2 and s['shot']:speed(70);stage('normal')
  elif s['phase']=='normal':
   if not s['shot']and 60<a['visual_speed']<85 and a['slow']<.25:shot('03_Normal');s['shot']=True
   if elapsed>=3.2 and s['shot']:speed(125);stage('fast')
  elif s['phase']=='fast':
   if not s['shot']and a['visual_speed']>110 and a['fast']>.65:shot('04_Fast');s['shot']=True
   if elapsed>=3.2 and s['shot']:speed(70);goal();stage('turn')
  elif s['phase']=='turn':
   if not s['shot']and max(abs(x)for x in a['heading_offsets'])>5:shot('05_DelayedTurn');s['shot']=True
   if elapsed>=4 and s['shot']:M.set_movement_paused(True);stage('stop')
  elif s['phase']=='stop':
   if elapsed<2:return
   shot('06_Stopped');M.controlled_model_preview=False;A.tags=old['tags'];M.set_movement_paused(False);shore();stage('raising')
  elif s['phase']=='raising':
   if not s['shot']and .3<a['observe']<.8:shot('07_Raising');s['shot']=True
   if a['observe']>.99 and s['shot']:stage('observe')
  elif s['phase']=='observe':
   if not s['shot']:shot('08_Observe');s['shot']=True
   if elapsed>=2:shore(1620,-1800,math.degrees(math.atan2(A.get_actor_location().y+1800,A.get_actor_location().x-1620)));stage('side')
  elif s['phase']=='side':
   if elapsed<2:return
   shot('09_ObserveSide');shore(720,-2500,math.degrees(math.atan2(A.get_actor_location().y+2500,A.get_actor_location().x-720)));stage('south')
  elif s['phase']=='south':
   if elapsed<2:return
   shot('10_ObserveSouth');shore();M.set_movement_paused(True);M.controlled_model_preview=True;A.tags=old['tags']+['PokemonDevelopmentSpecimen'];M.set_movement_paused(False);speed(70);goal();stage('lowering')
  elif s['phase']=='lowering':
   if not M.is_model_preview_moving():goal()
   if not s['shot']and .3<a['observe']<.75:shot('11_Lowering');s['shot']=True
   if a['observe']<.01 and s['shot']and a['visual_speed']>40:
    shot('12_ReturnToSwim');r['checks'].append('All qualified idle/35/70/125, delayed turn, stop, raise and lower phases observed with original camera')
    if q.get('recording'):
     if capture_tool:capture_tool.stop()
     else:cmd('pm.TAAReview.CaptureStop')
    restore_motion();stage('drain')
  elif s['phase']=='drain':
   if q.get('recording'):
    if not(capture/'Complete.txt').exists():return
    assert not(capture/'Error.txt').exists();metrics=json.loads((capture/'Metrics.json').read_text());assert metrics['frames']>30;r['capture_metrics']=metrics
   if elapsed<2:return
   if q.get('recording'):r['checks'].append('Genuine timestamped frames; no rendering configuration or global time dilation changed');finish();return
   assert Enc.reorder_party(s['original_first'],0);shore();PC.toggle_main_menu();assert PC.is_menu_open();s['saved_party']=[x.export_text()for x in Enc.get_player_party()];s['saved_pos']=P.get_actor_location().to_tuple();s['saved_time']=C.get_time().export_text();assert S.save_current_game(),S.get_last_storage_message();assert S.load_game(),S.get_last_storage_message();stage('save_load')
  elif s['phase']=='save_load':
   if elapsed<3 or S.is_load_in_progress():return
   assert [x.export_text()for x in Enc.get_player_party()]==s['saved_party'];assert(P.get_actor_location()-unreal.Vector(*s['saved_pos'])).length()<.1;assert C.get_time().export_text()==s['saved_time'];assert PC.close_menu();r['checks'].append('Isolated menu Save/Load preserves complete party/AP/identities, position and world time');stage('land')
  elif s['phase']=='land':
   if elapsed<2:return
   comp=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==W);buddy=comp.get_visual();assert buddy and not buddy.using_swim_mesh;assert buddy.mesh.get_skeletal_mesh_asset()==Enc.get_player_party()[0].species.get_visuals().presentation.mesh;r['checks'].append('Regular land companion stays on the original land rig after save/load');r['graphics_after']={k:unreal.SystemLibrary.get_console_variable_float_value(k)for k in r['graphics']};assert r['graphics_after']==r['graphics'];finish();return
  if s['phase']in ['slow','normal','fast','turn','raising','lowering']and elapsed>45:raise AssertionError('Actual requested pose not reached: '+s['phase'])
 except Exception:finish(traceback.format_exc())
 finally:s['busy']=False
unreal._garados_polish_review=unreal.register_slate_post_tick_callback(tick)
