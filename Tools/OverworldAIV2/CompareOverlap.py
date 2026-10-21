"""Transient A/B diagnostic in the existing PIE; restores all touched values."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/OverworldAIV2/LightingOverlap';D.mkdir(exist_ok=True)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);m=p.get_component_by_class(unreal.PokeMonsterMeshyVisualComponent);mov=p.get_component_by_class(unreal.CharacterMovementComponent)
oldloc=p.get_actor_location();oldrot=p.get_actor_rotation();oldchannels=m.get_editor_property('lighting_channels');oldpause=m.pause_anims
sky=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.SkyLight));sk=sky.get_component_by_class(unreal.SkyLightComponent);oldsky=sk.intensity
oldmode=unreal.SystemLibrary.get_console_variable_int_value('pm.PlayerFill.Mode');fill=p.get_component_by_class(unreal.PokeMonsterCharacterFillComponent);unreal.SystemLibrary.execute_console_command(w,'pm.PlayerFill.Mode 0')
for cmd in ['pm.EnvPerf2.Viewport 2560 1440','r.ScreenPercentage 100','r.SecondaryScreenPercentage.GameViewport 100']:unreal.SystemLibrary.execute_console_command(w,cmd)
m.set_editor_property('pause_anims',True)
points=[('DeepOverlap',-1300,-850),('CanopyOpening',-1910,530)]
jobs=[(n,x,y,v)for n,x,y in points for v in ['Original','Automatic']];state={'i':0,'t':0,'placed':False,'shot':False,'rows':[]}
def restore():
 sk.set_intensity(oldsky);m.set_lighting_channels(oldchannels.channel0,oldchannels.channel1,oldchannels.channel2);m.set_editor_property('pause_anims',oldpause);unreal.SystemLibrary.execute_console_command(w,'pm.PlayerFill.Mode '+str(oldmode));p.set_actor_location(oldloc,False,True);p.set_actor_rotation(oldrot,True)
def tick(dt):
 try:
  state['t']+=dt
  if state['i']>=len(jobs):
   restore();unreal.unregister_slate_post_tick_callback(unreal._ai_lighting);(D/'Result.json').write_text(json.dumps(state['rows'],indent=2));return
  n,x,y,v=jobs[state['i']]
  if not state['placed']:
   p.set_actor_location(unreal.Vector(x,y,50.15),False,True);mov.stop_movement_immediately();p.set_actor_rotation(unreal.Rotator(0,0,0),True);sk.set_intensity(oldsky*(1.15 if v=='A_Sky15'else 1));unreal.SystemLibrary.execute_console_command(w,'pm.PlayerFill.Mode '+('1'if v=='Automatic'else'0'));state['placed']=True
  loc=p.get_actor_location();cam=pc.player_camera_manager.get_camera_location();toward=cam-loc;toward.z=0;toward=unreal.MathLibrary.normal(toward);pass
  if state['t']>5 and not state['shot']:
   unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(D/(n+'_'+v+'.png'))+'"',pc);state['shot']=True;state['rows'].append({'point':n,'variant':v,'player':loc.to_tuple(),'camera':cam.to_tuple(),'viewport':list(pc.get_viewport_size()),'sky':sk.intensity,'fill':fill.fill_lumens,'shade_estimate':fill.estimated_shade,'channels':str(m.get_editor_property('lighting_channels'))})
  if state['t']>7:state.update(i=state['i']+1,t=0,placed=False,shot=False)
 except Exception as e:
  restore();unreal.unregister_slate_post_tick_callback(unreal._ai_lighting);(D/'Error.txt').write_text(str(e));raise
unreal._ai_lighting=unreal.register_slate_post_tick_callback(tick)
