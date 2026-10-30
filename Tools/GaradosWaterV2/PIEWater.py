"""Real VisualV2 PIE observation; isolated save fixture, unchanged natural activity profiles."""
import unreal,json,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GaradosWaterV2';O=D/'PIE03';O.mkdir(exist_ok=False);s={'start':time.monotonic(),'phase':'init','at':0,'sample':0,'done':False};r={'checks':[],'samples':[]};W=PC=P=H=C=S=None

def cmd(x):unreal.SystemLibrary.execute_console_command(W,x,PC)
def finish(error=None):
 if s['done']:return
 s['done']=True;unreal.unregister_slate_post_tick_callback(unreal._garados_pie)
 try:cmd('pm.TAAReview.CaptureStop')
 except Exception:pass
 r.update(passed=error is None,error=error,seconds=time.monotonic()-s['start']);(O/'Result.json').write_text(json.dumps(r,indent=2,default=str))
def sample():
 rows=[]
 for a in H.population:
  if str(a.visual_species.get_internal_id())not in ['Garados','Karpador']:continue
  m=a.overworld_movement;v=next((x for x in a.get_attached_actors()if isinstance(x,unreal.PokeMonsterCreatureVisualActor)),None)
  rows.append({'species':str(a.visual_species.get_internal_id()),'position':a.get_actor_location().to_tuple(),'speed':m.current_speed,'distance':m.distance_travelled,'plans':m.successful_plans,'blocks':m.blocked_steps,'rejected':m.rejected_targets,'state':str(m.behavior_state),'activity_remaining':m.activity_remaining,'mesh':v.mesh.get_skeletal_mesh_asset().get_path_name()if v else None,'aquatic':v.aquatic_pose_alpha if v else None,'observe':v.swim_observe_alpha if v else None,'turn':v.swim_turn_input if v else None,'head':v.mesh.get_socket_location('head').to_tuple()if v else None})
 r['samples'].append({'seconds':time.monotonic()-s['at'],'water':rows,'player':P.get_actor_location().to_tuple()});(O/'Progress.json').write_text(json.dumps(r['samples'][-1],indent=2))
def tick(dt):
 global W,PC,P,H,C,S
 try:
  now=time.monotonic();assert now-s['start']<220
  if s['phase']=='init':
   W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
   if not W:return
   GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0)
   if not P:return
   def sub(t,o=GI):return next(x for x in unreal.ObjectIterator(t)if x.get_outer()==o)
   S=sub(unreal.PokeMonsterSaveSubsystem);C=sub(unreal.PokeMonsterWorldClock);H=sub(unreal.PokeMonsterHabitatSubsystem,W);assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D);assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_GaradosWaterV2');s.update(phase='preload',at=now);return
  if s['phase']=='preload':
   if now-s['at']<8:return
   assert S.load_game(),S.get_last_storage_message();s.update(phase='load',at=now);return
  if s['phase']=='load':
   if now-s['at']<4 or S.is_load_in_progress():return
   P.set_actor_location(unreal.Vector(1800,-600,50.15),False,True);cmd('pm.WorldClock set 1 12 0');cmd('pm.WorldClock resume');s.update(phase='observe',at=now);r['checks'].append('PIE loads own cloned QA fixture through normal SaveSubsystem');return
  if now-s['sample']>1:sample();s['sample']=now
  if s['phase']=='observe'and now-s['at']>=100:
   garados=[x for a in r['samples']for x in a['water']if x['species']=='Garados'];assert garados,'No natural Garados admitted with full body clearance';r['distance_cm']=max(x['distance']for x in garados);r['moving_frames']=sum(x['speed']>2 for x in garados);assert r['distance_cm']>20,'Natural movement not observed';assert all('/WaterV2/'in x['mesh']and x['aquatic']==1 for x in garados);r['checks'].append('Natural Garados uses the water rig and moves inside the unchanged pond');P.set_actor_location(unreal.Vector(720,-1090,50.15),False,True);cmd('pm.EnvPerf2.Viewport 2560 1440');s.update(phase='near',at=now);return
  if s['phase']=='near'and now-s['at']>=10:
   cmd('Shot filename='+str(O/'Pond.png'));s.update(phase='shot',at=now);return
  if s['phase']=='shot'and now-s['at']>=4:finish()
 except Exception:finish(traceback.format_exc())
unreal._garados_pie=unreal.register_slate_post_tick_callback(tick)
