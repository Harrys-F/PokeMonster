"""Isolated existing shadowless exterior fill-light comparison; always restores the actual starting light and player state."""
import unreal,json,traceback,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();q=json.loads((R/'Saved/CreaturePolishV4/FillRequest.json').read_text());target=float(q['intensity']);assert .65<target<=1.;D=R/'Saved/CreaturePolishV4'/q['label'];D.mkdir(exist_ok=False);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w;p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);assert not p.is_overworld_input_locked();original=p.get_actor_transform();p.set_overworld_input_locked(True);movement=p.get_component_by_class(unreal.CharacterMovementComponent);old_movement=movement.movement_mode;movement.set_movement_mode(unreal.MovementMode.MOVE_NONE);mesh=p.get_component_by_class(unreal.PokeMonsterMeshyVisualComponent);paused=mesh.pause_anims;mesh.set_editor_property('pause_anims',True);fill=p.get_component_by_class(unreal.PokeMonsterCharacterFillComponent);sky=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.DirectionalLight)if a.get_actor_label()=='VS_SoftSkyFill').get_component_by_class(unreal.DirectionalLightComponent);assert not sky.cast_shadows and abs(sky.intensity-.65)<.001;old=sky.intensity;unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Viewport 2560 1440');unreal.SystemLibrary.execute_console_command(w,'r.ScreenPercentage 100');settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
points=[('Sun',-760,-1410),('Canopy',-1320,-720),('Overlap',-1300,-850),('Meadow',-1950,1050),('River',1240,-1100),('Interior',16900,670)]
jobs=[(n,x,y,v)for n,x,y in points for v in ['Original','Fill08']];s=dict(i=0,t=0,last=unreal.GameplayStatics.get_time_seconds(w),placed=False,rows=[],wall=time.monotonic())
def finish(error=None):
 sky.set_intensity(old);movement.set_movement_mode(old_movement);mesh.set_editor_property('pause_anims',paused);p.set_actor_transform(original,False,True);p.set_overworld_input_locked(False);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);unreal.unregister_slate_post_tick_callback(unreal._polish_shadow);s.update(passed=error is None,error=error,restored_exterior_fill_intensity=sky.intensity);(D/'Result.json').write_text(json.dumps(s,indent=2));unreal.log('POLISH_SHADOW_COMPARE_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['t']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<240
  if s['i']>=len(jobs):finish();return
  n,x,y,v=jobs[s['i']]
  if not s['placed']:
   p.set_actor_location(unreal.Vector(x,y,50.15),False,True);p.set_actor_rotation(unreal.Rotator(pitch=0,yaw=135,roll=0),True);sky.set_intensity(target if v=='Fill08'else old);s['placed']=True
  if s['t']>=6:
   assert pc.get_viewport_size()==(2560,1440);unreal.SystemLibrary.execute_console_command(w,'Shot filename='+str(D/(n+'_'+v+'_QHD.png')),pc);s['rows'].append(dict(point=n,variant=v,exterior_fill_intensity=sky.intensity,player=p.get_actor_location().to_tuple(),camera=pc.player_camera_manager.get_camera_location().to_tuple(),rotation=pc.player_camera_manager.get_camera_rotation().to_tuple(),viewport=list(pc.get_viewport_size()),screen_percentage=unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage'),fill_lumens=fill.fill_lumens,shade_estimate=fill.estimated_shade));s.update(i=s['i']+1,t=0,placed=False)
 except Exception:finish(traceback.format_exc())
unreal._polish_shadow=unreal.register_slate_post_tick_callback(tick)
