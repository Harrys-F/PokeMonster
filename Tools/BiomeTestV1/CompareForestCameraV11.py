"""Real A/B game-camera photos: same player point, yaw/pitch/FOV; only the explicit local feature changes."""
import unreal,json,time,sys,traceback,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
req=json.loads((R/'Saved/BiomeTestV11/ForestCompareRequest.json').read_text());O=R/'Saved/BiomeTestV11'/req['label'];O.mkdir(exist_ok=False)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name().endswith('Dev_BiomeTestMap_V1');p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);arm=p.get_component_by_class(unreal.SpringArmComponent);cam=p.get_component_by_class(unreal.CameraComponent);vis=p.get_component_by_class(unreal.PokeMonsterCameraVisibilityComponent);zones=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterForestCameraZone);assert len(zones)==1;z=zones[0];enabled=z.get_editor_property('bEnabled');original=p.get_actor_location();slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest();assert vis.reveal_radius_scale==2.
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
cases=[(name,u,v,variant)for name,u,v in [('DensePath',3200,-1800),('CanopyEdge',2500,-1800)]for variant in ['A_OriginalSight','B_LocalCanopy']];s={'i':0,'stage':'move','last':unreal.GameplayStatics.get_time_seconds(w),'time':0.,'wall':time.monotonic(),'rows':[]}
def cmd(c):unreal.SystemLibrary.execute_console_command(w,c,pc)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._biome_forest_compare);p.set_actor_location(original,False,True);z.set_editor_property('bEnabled',enabled);settings.set_editor_property('bThrottleCPUWhenNotForeground',old);(O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'fixture':'Actual game photograph positioning of player only. Identical point/yaw/pitch/FOV; local camera distance intentionally differs. Not a footwalk.','rows':s['rows'],'save_before':before,'save_after':hashlib.sha256(slot.read_bytes()).hexdigest()},indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['time']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<180
  if s['i']>=len(cases):assert hashlib.sha256(slot.read_bytes()).hexdigest()==before;finish();return
  name,u,v,variant=cases[s['i']];active=variant.startswith('B')
  if s['stage']=='move':
   z.set_editor_property('bEnabled',active);p.set_actor_location(unreal.Vector(*L.world(u,v,L.height(u,v)+p.get_component_by_class(unreal.CapsuleComponent).get_scaled_capsule_half_height()+2)),False,True);p.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();s.update(stage='shot',time=0.);return
  if s['time']<3:return
  assert abs(arm.target_arm_length-(1700 if active else 2850))<.01;assert abs(vis.dense_canopy_amount-(1 if active else 0))<.01;assert vis.reveal_radius_scale==2.;assert cam.field_of_view==35;assert vis.get_dense_canopy_opt_in_tree_count()>15
  assert(vis.get_dense_canopy_faded_tree_count()>0)if active else(vis.get_dense_canopy_faded_tree_count()==0)
  path=O/(name+'_'+variant+'_QHD.png');cmd('HighResShot 2560x1440 filename="'+str(path)+'"');s['rows'].append({'point':name,'variant':variant,'player':p.get_actor_location().to_tuple(),'arm_cm':arm.target_arm_length,'camera':pc.player_camera_manager.get_camera_location().to_tuple(),'rotation':pc.player_camera_manager.get_camera_rotation().to_tuple(),'fov':cam.field_of_view,'sight_radius_scale':vis.reveal_radius_scale,'dense_opt_in_trees':vis.get_dense_canopy_opt_in_tree_count(),'dense_faded_trees':vis.get_dense_canopy_faded_tree_count(),'path':str(path.relative_to(R))});s.update(i=s['i']+1,stage='move',time=0.)
 except Exception:finish(traceback.format_exc())
cmd('r.ScreenPercentage 100');cmd('DisableAllScreenMessages 1');unreal._biome_forest_compare=unreal.register_slate_post_tick_callback(tick)
