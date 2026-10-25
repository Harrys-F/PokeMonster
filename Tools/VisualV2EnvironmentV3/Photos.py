"""Real fixed gameplay-camera photos. Diagnostic positioning, explicitly not a footrun."""
import unreal,json,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/EnvironmentV3';req=json.loads((D/'PhotoRequest.json').read_text());O=D/req['label'];O.mkdir(exist_ok=False)
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_game_world();assert W;P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0)
G=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterNPCTestGround)if x.get_outer()==W);assert G.visit(0),'RAM preview guard required'
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
cv=['r.ScreenPercentage','r.SecondaryScreenPercentage.GameViewport','r.DynamicRes.OperationMode'];old={k:unreal.SystemLibrary.get_console_variable_float_value(k)for k in cv}
def cmd(s):unreal.SystemLibrary.execute_console_command(W,s,PC)
cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');cmd('r.SecondaryScreenPercentage.GameViewport 100');cmd('r.DynamicRes.OperationMode 0')
# Only this disposable PIE photo world: prevent encounters during positioned stills.
frozen=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 if any(k in a.get_class().get_name() for k in ['WildEncounter','VisibleWildCreatureActor']):
  frozen.append((a,a.is_actor_tick_enabled(),a.get_actor_enable_collision()));a.set_actor_tick_enabled(False);a.set_actor_enable_collision(False)
restore_bindings=[];restore_hidden=[];restore_lights=[]
if req.get('baseline_environment'):
 scope=json.loads((R/'Art/World/VisualV2EnvironmentV3/Scope.json').read_text());live={a.get_name():a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)}
 for b in scope['bindings']:
  if b['actor']not in live or b['actor']in{g['actor']for g in scope['groups']}:continue
  a=live[b['actor']];c=next(c for c in a.get_components_by_class(unreal.StaticMeshComponent)if c.get_name()==b['component']);restore_bindings.append((c,b['slot'],c.get_material(b['slot'])));c.set_material(b['slot'],unreal.load_asset(b['before']))
 for g in scope['groups']:
  a=live[g['actor']];restore_hidden.append((a,a.get_editor_property('hidden')));a.set_actor_hidden_in_game(True)
 for b in scope['light_changes']:
  c=live[b['actor']].get_component_by_class(unreal.DirectionalLightComponent);restore_lights.append((c,c.intensity));c.set_intensity(b['before'])
if req.get('temporary_fill') is not None:
 a=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)if a.get_actor_label()=='VS_SoftSkyFill');c=a.get_component_by_class(unreal.DirectionalLightComponent);restore_lights.append((c,c.intensity));c.set_intensity(float(req['temporary_fill']))
points=[('Wiese',-2100,-1760),('Wald',-3300,2050),('Ostwald',1450,840),('WegeFelsen',450,470),('Heilhaus',-4100,450),('Fassade',-3850,450),('BachBruecke',-350,-130),('Uferabzweig',500,-1000),('Sonne',-2300,-900),('Schatten',-3070,1790),('InnenraumKontrolle',16900,670),('PokemonWiese',-1300,-1620),('PokemonWald',-1500,500),('PokemonUfer',1120,-1170)]
if req.get('views'):points=[x for x in points if x[0]in req['views']]
s={'i':0,'t':0,'placed':False,'shot':False,'rows':[]};start=time.monotonic()
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._env3_photos)
 for a,t,c in frozen:a.set_actor_tick_enabled(t);a.set_actor_enable_collision(c)
 for c,i,m in restore_bindings:c.set_material(i,m)
 for a,h in restore_hidden:a.set_actor_hidden_in_game(h)
 for c,v in restore_lights:c.set_intensity(v)
 for k,v in old.items():cmd(k+' '+str(v))
 cmd('pm.EnvPerf2.Viewport 0 0');settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle)
 restored=G.return_to_world();(O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'rows':s['rows'],'original_cvars':old,'quality_cvars':{k:unreal.SystemLibrary.get_console_variable_int_value(k)for k in ['sg.ViewDistanceQuality','sg.AntiAliasingQuality','sg.ShadowQuality','sg.PostProcessQuality','sg.TextureQuality','sg.EffectsQuality','sg.FoliageQuality','sg.ShadingQuality']},'restored_preview':restored,'photo_positioning_not_footrun':True,'baseline_environment_reconstructed_in_temporary_pie':bool(req.get('baseline_environment'))},indent=2));E2=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem);E2.editor_request_end_play()
def tick(dt):
 try:
  assert time.monotonic()-start<240
  if s['i']>=len(points):finish();return
  s['t']+=dt;n,x,y=points[s['i']]
  if not s['placed']:
   P.set_actor_location(unreal.Vector(x,y,48.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();s['placed']=True
  if s['t']>4 and not s['shot']:
   cmd('HighResShot 2560x1440 filename="'+str(O/(n+'.png'))+'"');s['shot']=True;s['rows'].append({'name':n,'player':P.get_actor_location().to_tuple(),'camera':PC.player_camera_manager.get_camera_location().to_tuple(),'rotation':PC.player_camera_manager.get_camera_rotation().to_tuple(),'fov':PC.player_camera_manager.get_fov_angle(),'viewport':PC.get_viewport_size(),'cvars':{k:unreal.SystemLibrary.get_console_variable_float_value(k)for k in cv}})
  if s['t']>5.8 and list(O.glob(n+'*.png')):s.update(i=s['i']+1,t=0,placed=False,shot=False)
 except Exception:finish(traceback.format_exc())
unreal._env3_photos=unreal.register_slate_post_tick_callback(tick)
