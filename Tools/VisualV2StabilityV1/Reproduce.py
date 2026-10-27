"""Bounded native QHD repro and ablations in real PIE, without saving scene/assets."""
import unreal,json,time,traceback,gc
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2StabilityV1';O=D/json.loads((D/'ReproduceRequest.json').read_text())['label'];O.mkdir(exist_ok=False);Ed=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=Ed.get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0)
def sub(c,outer=GI):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==outer)
C=sub(unreal.PokeMonsterWorldClock);S=sub(unreal.PokeMonsterSaveSubsystem);E=sub(unreal.PokeMonsterEncounterSubsystem);assert unreal._stability_isolated;assert not E.is_encounter_active()
V=P.get_component_by_class(unreal.PokeMonsterCameraVisibilityComponent);profiles=[(a,a.profile)for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor)]
for a,profile in profiles:a.set_editor_property('profile',None)
components=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 if isinstance(a,(unreal.PokeMonsterVisibleWildCreatureActor,unreal.PokeMonsterCreatureVisualActor)):
  for component in a.get_components_by_class(unreal.PrimitiveComponent):components.append((component,component.is_visible()))
result={'actual_pie':True,'shots':[],'wild_instances':len(profiles),'visual_instances':len(unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterCreatureVisualActor))};route=[];state={'i':0,'last':time.monotonic()}
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def place(x,y):P.set_actor_location(unreal.Vector(x,y,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
def act(n,f,wait=1.):route.append((n,f,wait))
def shot(n):
 cmd('HighResShot 2560x1440 filename="'+str(O/(n+'.png'))+'"');result['shots'].append({'name':n,'clock':C.get_time().export_text(),'player':P.get_actor_location().to_tuple(),'camera':PC.player_camera_manager.get_camera_location().to_tuple(),'rotation':PC.player_camera_manager.get_camera_rotation().to_tuple(),'fov':PC.player_camera_manager.get_fov_angle()})
def sight(enabled):
 V.set_component_tick_enabled(enabled)
 if not enabled:
  for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
   for mesh in a.get_components_by_class(unreal.MeshComponent):
    for i in range(mesh.get_num_materials()):
     material=mesh.get_material(i)
     if isinstance(material,unreal.MaterialInstanceDynamic):material.set_scalar_parameter_value('PlayerRevealStrength',0.)
cmd('pm.WorldClock pause');cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');cmd('r.SecondaryScreenPercentage.GameViewport 100');cmd('r.DynamicRes.OperationMode 0')
for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']:cmd('sg.'+n+'Quality 2')
act('Original documented group view',lambda:place(-650,1000),2)
for hour in [6,9,12,19,22,0]:
 act('Clock '+str(hour),lambda h=hour:cmd('pm.WorldClock set 1 '+str(h)+' 0'));act('Photo '+str(hour),lambda h=hour:shot('Group%02d00'%h),3)
act('Exact dusk',lambda:cmd('pm.WorldClock set 1 19 0'));act('Disable sight fade only',lambda:sight(False));act('Sight disabled photo',lambda:shot('Group1900_NoSight'),3);act('Restore sight',lambda:sight(True))
act('Hide Pokemon rendering only',lambda:[c.set_visibility(False,False)for c,v in components]);act('No Pokemon photo',lambda:shot('Group1900_NoPokemon'),3);act('Restore Pokemon',lambda:[c.set_visibility(v,False)for c,v in components])
act('Move player while camera follows',lambda:place(-450,1000),2);act('Moved group photo',lambda:shot('Moved1900'),3)
act('Under crown same baseline site',lambda:place(-1353.161706774002,-775.1272881918381),2);act('Under crown photo',lambda:shot('Crown1900'),3)
def finish(error=None):
 sight(True)
 for component,visible in components:component.set_visibility(visible,False)
 for actor,profile in profiles:actor.set_editor_property('profile',profile)
 unreal.unregister_slate_post_tick_callback(unreal._stability_reproduce);result.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(result,indent=2));route.clear()
 for n in ['W','GI','PC','P','C','S','E','V','profiles','components','component','actor','profile']:globals().pop(n,None)
 gc.collect()
def tick(dt):
 try:
  name,f,delay=route[state['i']]
  if time.monotonic()-state['last']<delay:return
  f();state.update(i=state['i']+1,last=time.monotonic());(O/'Progress.json').write_text(json.dumps({'step':state['i'],'last':name}))
  if state['i']==len(route):finish()
 except Exception:finish(traceback.format_exc())
unreal._stability_reproduce=unreal.register_slate_post_tick_callback(tick)
