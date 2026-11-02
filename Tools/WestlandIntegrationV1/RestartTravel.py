"""Fresh native process reloads only the previous owned tour slot, then travels through the real save loader."""
import unreal,json,time,traceback,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandIntegrationV1';cfg=json.loads((D/'ActiveNative.json').read_text());O=D/cfg['label'];expected=json.loads((D/'NativeTour01/Tour_review.json').read_text());assert expected['passed'];assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D/'NativeTour01')
s={'phase':'init','at':time.monotonic(),'start':time.monotonic(),'busy':False};r={'checks':[],'physical_gamepad_test':False,'original_user_saves_used':False}
def phase(n):s.update(phase=n,at=time.monotonic());(O/'Progress.json').write_text(json.dumps({'phase':n}))
def world(name):return next((w for w in unreal.ObjectIterator(unreal.World)if w.get_name()==name and unreal.GameplayStatics.get_player_pawn(w,0)),None)
def bind(w):
 global W,P,PC,E,C,S,GI,Comp
 W=w;P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
 def sub(t,o=GI):return next(x for x in unreal.ObjectIterator(t)if x.get_outer()==o)
 E=sub(unreal.PokeMonsterEncounterSubsystem);C=sub(unreal.PokeMonsterWorldClock);S=sub(unreal.PokeMonsterSaveSubsystem);Comp=sub(unreal.PokeMonsterCreatureCompanionSubsystem,W)
def check():
 assert P.is_third_person_camera()and P.third_person_distance==350 and P.third_person_pitch==-12
 values={n:unreal.SystemLibrary.get_console_variable_float_value(n)for n in ['r.ScreenPercentage','r.Lumen.HardwareRayTracing','r.Lumen.FinalGatherMethod','r.TemporalAA.Upsampling','r.Shadow.Virtual.SMRT.RayCountDirectional']};assert values=={'r.ScreenPercentage':75,'r.Lumen.HardwareRayTracing':0,'r.Lumen.FinalGatherMethod':0,'r.TemporalAA.Upsampling':1,'r.Shadow.Virtual.SMRT.RayCountDirectional':4}
 assert [x.export_text()for x in E.get_player_party()]==expected['saved_party'];assert Comp.get_visual()and not Comp.get_visual().get_editor_property('hidden');return values
def finish(error=None):
 r.update(passed=error is None,error=error,seconds=time.monotonic()-s['start']);(O/'Result.json').write_text(json.dumps(r,indent=2));unreal.unregister_slate_post_tick_callback(unreal._westland_restart);unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
def tick(dt):
 if s['busy']:return
 s['busy']=True
 try:
  assert time.monotonic()-s['start']<120,'Bounded owned restart/travel check'
  if s['phase']=='init':
   bind(world('Dev_WestlandRegion'));assert S.has_save_game();PC.toggle_main_menu();assert PC.is_menu_open();assert S.load_game();phase('initial_load')
  elif s['phase']=='initial_load':
   if time.monotonic()-s['at']<2 or S.is_load_in_progress():return
   r['graphics']=check();assert math.dist(P.get_actor_location().to_tuple(),expected['saved_position'])<.1;assert C.get_time().export_text()==expected['saved_time'];r['checks'].append('Fresh native application starts Westland by default, loads exact owned tour team/AP/time/position and companion');unreal.SystemLibrary.execute_console_command(W,'Shot filename="'+str(O/'Westland_Neustart.png')+'" -nosuffix',PC);phase('begin_travel')
  elif s['phase']=='begin_travel':
   if time.monotonic()-s['at']<1:return
   assert PC.close_menu();s['travel_time']=C.get_time().seconds_of_day;unreal.GameplayStatics.open_level(W,'/Game/Maps/Dev_TestMap_VisualV2');phase('visual_wait')
  elif s['phase']=='visual_wait':
   w=world('Dev_TestMap_VisualV2')
   if not w:return
   bind(w)
   if time.monotonic()-s['at']<3:return
   check();assert C.get_real_minutes_per_day()==120;assert C.get_time().seconds_of_day>=s['travel_time'];r['checks'].append('Actual travel to unchanged VisualV2 preserves team/buddy/world clock and current rendering');assert S.load_game();phase('region_wait')
  elif s['phase']=='region_wait':
   w=world('Dev_WestlandRegion')
   if not w:return
   bind(w)
   if S.is_load_in_progress()or time.monotonic()-s['at']<2:return
   check();assert math.dist(P.get_actor_location().to_tuple(),expected['saved_position'])<.1;assert not P.is_overworld_input_locked();r['checks'].append('Normal menu save loader changes map back to Westland, restores saved position/individuals/AP and valid unlocked Third Person/companion');unreal.SystemLibrary.execute_console_command(W,'Shot filename="'+str(O/'Westland_Nach_Kartenwechsel.png')+'" -nosuffix',PC);phase('finish')
  elif s['phase']=='finish':
   if time.monotonic()-s['at']<1:return
   assert (O/'Westland_Neustart.png').exists()and(O/'Westland_Nach_Kartenwechsel.png').exists();finish()
 except Exception:finish(traceback.format_exc())
 finally:s['busy']=False
unreal._westland_restart=unreal.register_slate_post_tick_callback(tick)
