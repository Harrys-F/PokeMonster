"""Actual bounded flight above a colliding rock, interrupted by existing battle and RAM save protection."""
import unreal,json,sys,time,math,traceback,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
label=json.loads((R/'Saved/BiomeTestV11/FlightPauseRequest.json').read_text())['label'];O=R/'Saved/BiomeTestV11'/label;O.mkdir(exist_ok=False)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w;p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);mode=unreal.GameplayStatics.get_game_mode(w);assert not mode.is_isolated_gameplay_review();gi=unreal.GameplayStatics.get_game_instance(w);e=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi);h=next(x for x in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterBiomeHabitat)if x.habitat_name=='HabitakFlug');a=h.runtime_specimens[0];rock=next(x for x in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor)if x.get_actor_label()=='Biome_HabitakLowRock_V11');rc,re=rock.get_actor_bounds(False);original=p.get_actor_location();slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest()
# Reproducible technical flight corridor in PIE only. The original live creature is never teleported.
original_points=list(h.travel_points);centre=h.get_actor_location();cu,cv=L.local(centre.x,centre.y)
h.travel_points=[unreal.Vector(u-cu,-(v-cv),0)for u,v in [(-2050,2200),(-1400,2400)]]
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
s={'phase':'wait','last':unreal.GameplayStatics.get_time_seconds(w),'time':0.,'wall':time.monotonic(),'samples':[],'pause_frames':0,'max_pause_motion_cm':0.,'max_pause_lift_delta_cm':0.}
def cmd(c):unreal.SystemLibrary.execute_console_command(w,c,pc)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._biome_flight_pause_v11);settings.set_editor_property('bThrottleCPUWhenNotForeground',old);h.travel_points=original_points
 if not error:assert not e.is_encounter_active();assert mode.end_isolated_gameplay_review();p.set_actor_location(original,False,True)
 (O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'fixture':'Existing source Habitak flies via two controlled PIE-only safe corridor anchors over the actual colliding rock; original anchors restored, no creature teleport or pose override. Player observation positioning and RAM battle party are explicit technical fixtures','pause_frames':s['pause_frames'],'max_pause_motion_cm':s['max_pause_motion_cm'],'max_pause_lift_delta_cm':s['max_pause_lift_delta_cm'],'samples':s['samples'],'save_before':before,'save_after':hashlib.sha256(slot.read_bytes()).hexdigest(),'RAM_preview_active_on_failure':mode.is_isolated_gameplay_review()},indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['time']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<240;q=a.get_actor_location();height=a.get_ground_hover_height();state=a.get_ground_hover_state()
  if s['phase']=='wait':
   p.set_actor_location(unreal.Vector(*L.world(-1700,1850,L.height(-1700,1850)+p.get_component_by_class(unreal.CapsuleComponent).get_scaled_capsule_half_height()+2)),False,True)
   if state=='Hover'and abs(q.x-rc.x)<re.x and abs(q.y-rc.y)<re.y:
    assert q.z+height>rc.z+re.z+15;assert mode.begin_isolated_gameplay_review();cmd('pm.StarterReview.Party Habitak Zunderlauf');cmd('pm.StarterReview.Start classic Habitak Zunderlauf');assert e.is_encounter_active();s.update(phase='battle',time=0.,position=q,lift=height);s['samples'].append({'phase':'before_battle','world':q.to_tuple(),'lift':height});return
  elif s['phase']=='battle':
   s['pause_frames']+=1;s['max_pause_motion_cm']=max(s['max_pause_motion_cm'],(q-s['position']).length());s['max_pause_lift_delta_cm']=max(s['max_pause_lift_delta_cm'],abs(height-s['lift']));assert (q-s['position']).length()<.1 and abs(height-s['lift'])<.1;assert q.z+height>rc.z+re.z+15
   if s['time']>2:
    cmd('pm.CreatureReview.CaptureLiveUI BiomeV11_'+label+'_BattlePause');s.update(phase='flee',time=0.)
  elif s['phase']=='flee':
   if not e.is_encounter_active():s.update(phase='resume',time=0.);return
   v=e.get_presenter().get_view()
   if not v.busy and not v.finished:assert e.get_presenter().try_select_flee();assert e.get_presenter().resolve_selection()
  elif s['phase']=='resume':
   if state=='Grounded'and(q-s['position']).length()>40:
    s['samples'].append({'phase':'resumed_and_landed','world':q.to_tuple(),'lift':height});assert s['pause_frames']>10;assert hashlib.sha256(slot.read_bytes()).hexdigest()==before;finish()
 except Exception:finish(traceback.format_exc())
unreal._biome_flight_pause_v11=unreal.register_slate_post_tick_callback(tick)
