"""Controlled real-game-camera lighting study, temporary PIE only; no map/material writes."""
import unreal,json,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/LightingV31';request=json.loads((D/'Request.json').read_text());O=D/request['label'];O.mkdir(exist_ok=False);E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_game_world();assert W;P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);G=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterNPCTestGround)if x.get_outer()==W);assert G.visit(0)
actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)};sky=actors['SkyLight_Dev'].get_component_by_class(unreal.SkyLightComponent);sun=actors['DirectionalLight_Dev'].get_component_by_class(unreal.DirectionalLightComponent);fill=actors['VS_SoftSkyFill'].get_component_by_class(unreal.DirectionalLightComponent);pp=actors['V2_OutdoorExposure'];original={'source_type':sky.source_type,'cubemap':sky.cubemap,'intensity':sky.intensity,'lower_hemisphere_is_black':sky.lower_hemisphere_is_black,'lower_hemisphere_color':sky.lower_hemisphere_color};original_pp=pp.settings;fill_actor=actors['VS_SoftSkyFill'];original_fill_rotation=fill_actor.get_actor_rotation();original_fill_intensity=fill.intensity;cube=unreal.load_asset('/Engine/MapTemplates/Sky/DaylightAmbientCubemap');assert isinstance(cube,unreal.TextureCube)
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False);cv=['r.ScreenPercentage','r.SecondaryScreenPercentage.GameViewport','r.DynamicRes.OperationMode'];old_cv={k:unreal.SystemLibrary.get_console_variable_float_value(k)for k in cv}
def cmd(s):unreal.SystemLibrary.execute_console_command(W,s,PC)
cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');cmd('r.SecondaryScreenPercentage.GameViewport 100');cmd('r.DynamicRes.OperationMode 0')
frozen=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 if 'VisibleWildCreatureActor'in a.get_class().get_name():frozen.append((a,a.is_actor_tick_enabled(),a.get_actor_enable_collision()));a.set_actor_tick_enabled(False);a.set_actor_enable_collision(False)
points=[('SonnigeWiese',-2100,-1760),('Baumkrone',-1320,-720),('Kronenrand',-1500,500),('DichterWald',-1300,-850),('Waldweg',-3300,2050),('Gebaeude',-4100,450),('Felsen',450,470),('NPC',-850,-1100),('PokemonUfer',1120,-1170),('Innenraum',16900,670)]
if request.get('views'):points=[p for p in points if p[0]in request['views']]
s={'variant':0,'view':0,'t':0.,'initial':True,'placed':False,'shot':False,'rows':[]};start=time.monotonic()
changed=False
def apply(v):
 global changed
 unreal.log('LIGHT31_VARIANT '+str(v))
 if not v and not changed:return
 if v.get('id')=='A'and not changed:return
 if changed:
  sky.set_editor_property('source_type',original['source_type']);sky.set_cubemap(original['cubemap']);sky.set_intensity(original['intensity']);pp.set_editor_property('settings',original_pp);fill_actor.set_actor_rotation(original_fill_rotation,False);fill.set_intensity(original_fill_intensity)
 if not v:return
 if v.get('daylight_cube'):sky.set_editor_property('source_type',unreal.SkyLightSourceType.SLS_SPECIFIED_CUBEMAP);sky.set_cubemap(cube)
 if 'intensity'in v:sky.set_intensity(v['intensity'])
 if 'fill_yaw'in v:fill_actor.set_actor_rotation(unreal.Rotator(pitch=original_fill_rotation.pitch,yaw=v['fill_yaw'],roll=original_fill_rotation.roll),False)
 if 'fill'in v:fill.set_intensity(v['fill'])
 if 'ao'in v:
  st=pp.settings;st.set_editor_property('ambient_occlusion_intensity',v['ao']);pp.set_editor_property('settings',st)
 changed=True
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._light31_study)
 apply({})
 for a,t,c in frozen:a.set_actor_tick_enabled(t);a.set_actor_enable_collision(c)
 for k,v in old_cv.items():cmd(k+' '+str(v))
 cmd('pm.EnvPerf2.Viewport 0 0');settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);restored=G.return_to_world();(O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'variants':request['variants'],'rows':s['rows'],'restored_preview':restored,'qhd_quality':{k:unreal.SystemLibrary.get_console_variable_int_value(k)for k in ['sg.ShadowQuality','sg.GlobalIlluminationQuality','sg.FoliageQuality','sg.ShadingQuality','sg.PostProcessQuality']},'source_cube':cube.get_path_name(),'diagnostic_positioning_not_footrun':True},indent=2));unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
def tick(dt):
 try:
  assert time.monotonic()-start<720
  if s['variant']>=len(request['variants']):finish();return
  v=request['variants'][s['variant']]
  if s['initial']:
   apply(v);s.update(t=-5.,initial=False)
  s['t']+=dt;name,x,y=points[s['view']]
  if not s['placed']:P.set_actor_location(unreal.Vector(x,y,48.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();s['placed']=True
  if s['t']>4 and not s['shot']:
   out=O/v['id'];out.mkdir(exist_ok=True);cmd('HighResShot 2560x1440 filename="'+str(out/(name+'.png'))+'"');s['shot']=True;s['rows'].append({'variant':v['id'],'view':name,'player':P.get_actor_location().to_tuple(),'camera':PC.player_camera_manager.get_camera_location().to_tuple(),'rotation':PC.player_camera_manager.get_camera_rotation().to_tuple(),'fov':PC.player_camera_manager.get_fov_angle(),'viewport':PC.get_viewport_size(),'sky_intensity':sky.intensity,'sky_source':str(sky.source_type),'sky_cube':sky.cubemap.get_path_name()if sky.cubemap else None,'sun_intensity':sun.intensity,'fill_intensity':fill.intensity,'fill_rotation':fill_actor.get_actor_rotation().to_tuple(),'pp':pp.settings.export_text()});(O/'Progress.json').write_text(json.dumps({'variant':v['id'],'view':name}))
  if s['t']>5.6 and s['shot']:
   s.update(view=s['view']+1,t=0.,placed=False,shot=False)
   if s['view']==len(points):s.update(variant=s['variant']+1,view=0,initial=True)
 except Exception:finish(traceback.format_exc())
unreal._light31_study=unreal.register_slate_post_tick_callback(tick)
