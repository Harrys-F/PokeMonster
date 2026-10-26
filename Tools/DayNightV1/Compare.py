"""Actual PIE QHD light comparison. Original, B75, C85; no noon-60 variant.
Existing test-ground specimens are temporary color/scale references, not new wild encounters.
The player's existing adaptive fill and idle pose are frozen per comparison pair only.
"""
import unreal,json,time,traceback,gc
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/DayNightV1';q=json.loads((D/'ReviewRequest.json').read_text());O=D/q['label'];O.mkdir(exist_ok=False)
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0)
def sub(c,outer):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==outer)
Cycle=sub(unreal.PokeMonsterDayNightSubsystem,W);Clock=sub(unreal.PokeMonsterWorldClock,GI);Save=sub(unreal.PokeMonsterSaveSubsystem,GI);Ground=sub(unreal.PokeMonsterCreatureTestGround,W)
assert Cycle.is_cycle_enabled()and Cycle.is_sky_ready();assert Save.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_DayNight'+q['label'])
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
cmd('pm.WorldClock pause');cmd('pm.WorldClock set 1 12 0');cmd('pm.EnvPerf2.Viewport 2560 1440')
for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']:cmd('sg.'+n+'Quality 2')
for n,v in [('r.ScreenPercentage',100),('r.SecondaryScreenPercentage.GameViewport',100),('r.DynamicRes.OperationMode',0)]:cmd(n+' '+str(v))
actors={a.get_name():a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)};Sun=actors['DirectionalLight_1'].get_component_by_class(unreal.DirectionalLightComponent);Fill=actors['DirectionalLight_0'].get_component_by_class(unreal.DirectionalLightComponent);SkyLight=actors['SkyLight_1'].get_component_by_class(unreal.SkyLightComponent)
fill_components=[c for c in P.get_components_by_class(unreal.ActorComponent)if'CharacterFillComponent'in c.get_class().get_name()];fill_ticks=[c.is_component_tick_enabled()for c in fill_components]
skels=P.get_components_by_class(unreal.SkeletalMeshComponent);pause_states=[c.get_editor_property('pause_anims')for c in skels]
specs=list(Ground.specimens[:3]);transforms=[a.get_actor_transform()for a in specs]
for m in Ground.movements[:3]:m.set_movement_paused(True)
route=[];state={};result={'actual_pie':True,'existing_specimens_temporarily_repositioned':True,'new_models':0,'player_fill_frozen_per_pair':True,'rows':[],'checks':[]};s={'i':0,'last':time.monotonic(),'start':time.monotonic()}
def act(n,f,d=.5):route.append((n,f,d))
def place(pos):
 for c,t in zip(fill_components,fill_ticks):c.set_component_tick_enabled(t)
 for c,v in zip(skels,pause_states):c.set_editor_property('pause_anims',v)
 P.set_actor_location(unreal.Vector(*pos),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
 for i,a in enumerate(specs):a.set_actor_location(unreal.Vector(pos[0]+100+i*140,pos[1]+170+i*45,0),False,True)
def freeze():
 for c in fill_components:c.set_component_tick_enabled(False)
 for c in skels:c.set_editor_property('pause_anims',True)
def record(view,variant):
 folder=O/variant;folder.mkdir(exist_ok=True);cmd('HighResShot 2560x1440 filename="'+str(folder/(view+'.png'))+'"')
 src=[]
 for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
  for c in a.get_components_by_class(unreal.LightComponentBase):
   row={'name':c.get_path_name(),'intensity':c.intensity,'color':c.light_color.export_text(),'actor_rotation':a.get_actor_rotation().to_tuple()}
   if isinstance(c,unreal.LightComponent):row.update(temperature=c.temperature,use_temperature=c.use_temperature,shadow=c.cast_shadows,channels=c.lighting_channels.export_text())
   src.append(row)
 result['rows'].append({'view':view,'variant':variant,'clock':Clock.get_time().export_text(),'phase':str(Clock.get_phase()),'sample':Cycle.get_lighting_sample().export_text(),'player':P.get_actor_location().to_tuple(),'camera':PC.player_camera_manager.get_camera_location().to_tuple(),'rotation':PC.player_camera_manager.get_camera_rotation().to_tuple(),'fov':PC.player_camera_manager.get_fov_angle(),'lights':src,'exposure':actors['PostProcessVolume_0'].settings.export_text()if'PostProcessVolume_0'in actors else None,'sky_intensity':SkyLight.intensity,'sky_color':SkyLight.light_color.export_text()})
points=json.loads((D/'Before/Result.json').read_text())['rows']
for row in points:
 n=row['view'];pos=row['player'];act('Original light at '+n,lambda:Cycle.set_cycle_enabled(False));act('Position '+n,lambda v=pos:place(v),.1);act('Freeze only adaptive fill and idle after settle',freeze,3)
 act('Original '+n,lambda n=n:record(n,'Original'),.4)
 act('B75 '+n,lambda:(Cycle.set_noon_variant(unreal.PokeMonsterNoonSun.B75),Cycle.set_cycle_enabled(True)))
 act('B75 capture '+n,lambda n=n:record(n,'B75'),3)
 act('C85 '+n,lambda:Cycle.set_noon_variant(unreal.PokeMonsterNoonSun.C85));act('C85 capture '+n,lambda n=n:record(n,'C85'),3)
# Unfrozen gameplay lighting across the actual requested clock times; same camera.
act('Provisional B75 only',lambda:Cycle.set_noon_variant(unreal.PokeMonsterNoonSun.B75));act('Stable open-field time-series camera',lambda:place(points[0]['player']))
for h,m in [(4,30),(6,0),(9,0),(12,0),(16,0),(19,0),(22,0),(0,0)]:
 act('Set actual clock '+str(h)+':'+str(m),lambda h=h,m=m:cmd('pm.WorldClock set 2 '+str(h)+' '+str(m)))
 act('Capture time '+str(h)+':'+str(m),lambda h=h,m=m:record('Time%02d%02d'%(h,m),'Cycle'),3)
# Readability at the fixed canopy and NPC in normal (adaptive) night lighting.
for n,pos in [('NightCanopy',points[1]['player']),('NightNPC',[-850,-1100,50.15])]:
 act('Night readable position '+n,lambda pos=pos:place(pos));act('Night time '+n,lambda:cmd('pm.WorldClock set 2 22 0'));act('Night actual game view '+n,lambda n=n:record(n,'Cycle'),3)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._daynight_compare)
 for c,t in zip(fill_components,fill_ticks):c.set_component_tick_enabled(t)
 for c,v in zip(skels,pause_states):c.set_editor_property('pause_anims',v)
 for a,t in zip(specs,transforms):a.set_actor_transform(t,False,True)
 for m in Ground.movements[:3]:m.set_movement_paused(False)
 result.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(result,indent=2));route.clear()
 for n in ['W','GI','P','PC','Cycle','Clock','Save','Ground','Sun','Fill','SkyLight','actors','skels','fill_components','specs']:globals().pop(n,None)
def tick(dt):
 try:
  now=time.monotonic();assert now-s['start']<400,'Comparison timeout';n,f,d=route[s['i']]
  if now-s['last']<d:return
  f();s['i']+=1;s['last']=time.monotonic();(O/'Progress.json').write_text(json.dumps({'step':s['i'],'last':n}))
  if s['i']==len(route):finish()
 except Exception:finish(traceback.format_exc())
unreal._daynight_compare=unreal.register_slate_post_tick_callback(tick)
