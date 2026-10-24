"""Actual live map photographs. Only the player is repositioned for photos; NOT a footwalk or staged creature motion."""
import unreal,json,sys,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
label=json.loads((R/'Saved/BiomeTestV11/MeadowPhotoRequest.json').read_text())['label'];assert label.isalnum();O=R/'Saved/BiomeTestV11'/label;O.mkdir(exist_ok=False)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name().endswith('Dev_BiomeTestMap_V1');p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);mode=unreal.GameplayStatics.get_game_mode(w);assert not mode.is_isolated_gameplay_review()
hs={h.habitat_name:h for h in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterBiomeHabitat)};mapping={'Raupy':'RaupyWiese','Hornliu':'HornliuWiese','Smettbo':'SmettboFlug','Bibor':'BiborFlug','Habitak':'HabitakFlug'};names=list(mapping);vs={n:hs[k].runtime_specimens[0]for n,k in mapping.items()};original=p.get_actor_location();rotation=p.get_actor_rotation();s={'i':0,'phase':'move','last':unreal.GameplayStatics.get_time_seconds(w),'time':0.,'wall':time.monotonic(),'rows':[],'record_requested':False};record=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('BiomeV11_'+label);assert not record.exists()
def cmd(c):unreal.SystemLibrary.execute_console_command(w,c,pc)
def place(q):
 u,v=L.local(q.x,q.y);p.set_actor_location(unreal.Vector(*L.world(u,v,L.height(u,v)+p.get_component_by_class(unreal.CapsuleComponent).get_scaled_capsule_half_height()+2)),False,True);p.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._biome_meadow_photos_v11)
 if s['record_requested']and record.exists()and not(record/'Complete.txt').exists():cmd('pm.TAAReview.CaptureStop')
 p.set_actor_location(original,False,True);p.set_actor_rotation(rotation,True);(O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'fixture':'Player-only photo positioning in actual live map, no creature poses/locations/scales changed. Not a footwalk.','photos':s['rows'],'recording':str(record.relative_to(R))},indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['time']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<180
  if s['i']<len(names):
   n=names[s['i']];a=vs[n]
   if s['phase']=='move':place(a.get_actor_location()+unreal.Vector(*L.world(-160,0)));s.update(phase='photo',time=0.);return
   if s['time']<2:return
   path=O/(n+'_GameCamera_QHD.png');cmd('HighResShot 2560x1440 filename="'+str(path)+'"');s['rows'].append({'species':n,'path':str(path.relative_to(R)),'player':p.get_actor_location().to_tuple(),'creature':a.get_actor_location().to_tuple(),'camera':pc.player_camera_manager.get_camera_location().to_tuple(),'reference_size_cm':hs[mapping[n]].specimens[0].species.get_visuals().presentation.reference_size_cm});s.update(i=s['i']+1,phase='move',time=0.);return
  if s['phase']=='move':
   place((vs['Smettbo'].get_actor_location()+vs['Bibor'].get_actor_location())*.5);s.update(phase='settle',time=0.);return
  if s['phase']=='settle'and s['time']>2:
   cmd('pm.TAAReview.CaptureStart "'+str(record)+'"');s.update(phase='record',time=0.,record_requested=True);return
  if s['phase']=='record'and s['time']>8:
   assert record.exists();cmd('pm.TAAReview.CaptureStop');s.update(phase='stop',time=0.);return
  if s['phase']=='stop'and(record/'Complete.txt').exists():assert int((record/'Complete.txt').read_text())>20;finish()
 except Exception:finish(traceback.format_exc())
cmd('pm.EnvPerf2.Viewport 1280 720');cmd('r.ScreenPercentage 100');cmd('DisableAllScreenMessages 1');unreal._biome_meadow_photos_v11=unreal.register_slate_post_tick_callback(tick)
