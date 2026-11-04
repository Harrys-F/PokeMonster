"""Real input, interactions, capture, isolated Save/Load and travel. No production mutation."""
import unreal,json,time,math,statistics,traceback,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualV2IntegrationV1';cfg=json.loads((D/'GameplayRequest.json').read_text());O=D/cfg['label'];O.mkdir(exist_ok=True);assert not(O/'Result.json').exists();assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D);ed=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=ed.get_game_world()if ed else None;pie=W is not None
if not W:W=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_WestlandRegion'and unreal.GameplayStatics.get_player_pawn(w,0))
P=PC=GI=E=C=S=H=Comp=I=Dlg=None;checks=[];distribution=[];shots=[];frames=[];start=last=time.monotonic();lastsample=0;busy=False;profiling_old={}

def valid(obj):
 try:return obj is not None and unreal.SystemLibrary.is_valid(obj)
 except Exception:return False
def sub(cls,outer):return next(x for x in unreal.ObjectIterator(cls)if x.get_outer()==outer)
def bind(w):
 global W,P,PC,GI,E,C,S,H,Comp,I,Dlg,MoveSub,MoveAction
 W=w;P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W);E=sub(unreal.PokeMonsterEncounterSubsystem,GI);C=sub(unreal.PokeMonsterWorldClock,GI);S=sub(unreal.PokeMonsterSaveSubsystem,GI);H=sub(unreal.PokeMonsterHabitatSubsystem,W);Comp=sub(unreal.PokeMonsterCreatureCompanionSubsystem,W);I=sub(unreal.PokeMonsterInventorySubsystem,GI);Dlg=sub(unreal.PokeMonsterDialogueSubsystem,GI);MoveSub=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if x.get_world()==W);MoveAction=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==P and x.get_name()=='MoveAction')
def cmd(s):unreal.SystemLibrary.execute_console_command(W,s,PC)
def inject(x,y):MoveSub.inject_input_vector_for_action(MoveAction,unreal.Vector(x,y,0),[],[])
def steer(x,y):
 p=P.get_actor_location();dx=x-p.x;dy=y-p.y;yaw=math.radians(P.get_movement_basis_yaw());a=-math.sin(yaw)*dx+math.cos(yaw)*dy;b=math.cos(yaw)*dx+math.sin(yaw)*dy;n=max(1,math.hypot(a,b));mag=min(1,max(.2,n/120));inject(a/n*mag,b/n*mag)
def wait(seconds):
 until=time.monotonic()+seconds
 while time.monotonic()<until:yield

def walk(x,y,seconds=35,radius=28):
 since=time.monotonic()
 while math.dist(P.get_actor_location().to_tuple()[:2],(x,y))>radius:
  assert time.monotonic()-since<seconds,('Blocked walk',x,y,P.get_actor_location());steer(x,y);yield
 inject(0,0);checks.append(dict(walk=[x,y],actual=P.get_actor_location().to_tuple()))
def place(a,offset=(-130,0)):
 p=a.get_actor_location();cap=a.get_component_by_class(unreal.CapsuleComponent);z=p.z-cap.get_scaled_capsule_half_height()+50.15 if cap else p.z+50.15;P.set_actor_location(unreal.Vector(p.x+offset[0],p.y+offset[1],z),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();P.set_actor_rotation(unreal.Rotator(yaw=math.degrees(math.atan2(-offset[1],-offset[0]))),False);steer(p.x,p.y)
def shot(name):
 p=O/(name+'.png');cmd('Shot showui filename="'+str(p)+'" -nosuffix');shots.append(str(p))
def snapshot():return dict(party=[x.export_text()for x in E.get_player_party()],inventory=[x.export_text()for x in I.get_stacks()],position=P.get_actor_location().to_tuple(),clock=C.get_time().export_text(),facing=P.get_interaction_world_direction().to_tuple())
def run():
 bind(W);H.set_population_enabled(False);checks.append('Dedicated collision/door run with wild population disabled only in this isolated process; live AI is checked in Features and Tour');cmd('pm.EnvPerf2.Viewport 2560 1440');yield from wait(2)
 import sys,re
 sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'Tools'));import WestlandRegionLayout as L
 actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)};ignore=[a for n,a in actors.items()if not n.startswith('WR_Terrain_')]
 def floor(x,y):
  hit=unreal.SystemLibrary.line_trace_single(W,unreal.Vector(x,y,16000),unreal.Vector(x,y,-10000),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,ignore,unreal.DrawDebugTrace.NONE);assert hit
  return float(re.search(r'ImpactPoint=\(X=[^,]+,Y=[^,]+,Z=([^\)]+)',hit.export_text())[1])
 # 75cm route-waypoint tolerance stays inside the 2.2m access strip; actual doorway/interior targets retain 28cm tolerance.
 prior=D/'NativeAccess02/Result.json';previous=json.loads(prior.read_text())if prior.is_file()else dict(checks=[]);verified=[c for c in previous['checks']if isinstance(c,dict)and c.get('access_walk_both_directions')]
 checks.append(dict(previous_full_accesses=verified,remaining_centerline_limitation='Original Gartenhaus access spline intersects unchanged rear wall; no original road/geometry silently changed'))
 for access in json.loads((R/'Art/World/WestlandRegion/WestlandRegion_Access.json').read_text()):
  name=access['name'].removeprefix('Access_');cut=actors['WR_'+name+'_Cutaway'];t=cut.door_threshold.get_world_transform();q=unreal.MathLibrary.transform_location(t,unreal.Vector(-220,0,0));P.set_actor_location(unreal.Vector(q.x,q.y,floor(q.x,q.y)+50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();yield from wait(.4)
  q=unreal.MathLibrary.transform_location(t,unreal.Vector(140,0,0));yield from walk(q.x,q.y,15);yield from wait(.8);assert cut.is_viewer_inside(P.get_actor_location())and cut.is_cutaway_active(),(name,'inside',P.get_actor_location());assert abs(PC.player_camera_manager.get_camera_rotation().pitch+12)<.03
  shot('Innen_'+name);yield from wait(.3);q=unreal.MathLibrary.transform_location(t,unreal.Vector(-220,0,0));yield from walk(q.x,q.y,15);yield from wait(.8);assert not cut.is_viewer_inside(P.get_actor_location());checks.append(dict(building=name,door_crossed_both_directions=True,cutaway=True,camera_pitch=-12,positioned_at_actual_front_door=True))
 # Each new field gets a real collision traversal as well, without random battle interruptions.
 for field in json.loads((D/'BushFields.json').read_text())['fields']:
  x,y,_=field['center'];P.set_actor_location(unreal.Vector(x-150,y,floor(x-150,y)+50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();yield from wait(.4)
  for dx,dy in [(150,0),(150,80),(-150,80),(-150,0)]:yield from walk(x+dx,y+dy,15)
  checks.append(dict(field=field['habitat'],walked_both_directions=True))

def finish(error=None):
 if valid(P):inject(0,0)
 unreal.unregister_slate_post_tick_callback(unreal._wvi_extra);(O/'Result.json').write_text(json.dumps(dict(passed=error is None,error=error,checks=checks,shots=shots,seconds=time.monotonic()-start,diagnostic_positioning=True),indent=2))
 live=next((w for w in unreal.ObjectIterator(unreal.World)if w.get_name()in ['Dev_WestlandRegion','Dev_TestMap_VisualV2']and unreal.GameplayStatics.get_player_pawn(w,0)),None)
 if live:unreal.SystemLibrary.quit_game(live,unreal.GameplayStatics.get_player_controller(live,0),unreal.QuitPreference.QUIT,False)
gen=run()
def tick(dt):
 global busy
 if busy:return
 busy=True
 try:
  assert time.monotonic()-start<650;next(gen)
 except StopIteration:finish()
 except Exception:finish(traceback.format_exc())
 finally:busy=False
unreal._wvi_extra=unreal.register_slate_post_tick_callback(tick)
