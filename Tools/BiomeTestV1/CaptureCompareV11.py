"""Explicit photograph fixture in normal PIE. Teleports are for matched photos, NOT a gameplay footwalk."""
import unreal,json,time,sys,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
req=json.loads((R/'Saved/BiomeTestV11/CaptureRequest.json').read_text());O=R/'Saved/BiomeTestV11'/req['label'];O.mkdir(exist_ok=False)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name().endswith('Dev_BiomeTestMap_V1');p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0)
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
positions=[('Wiese',-2700,2700),('Wasser',1900,2800),('Felszugang',-1100,-1100),('Ruine',3000,-3400),('DichterWald',1500,-1500)]
s={'index':0,'stage':'move','time':0,'last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'rows':[]};original=p.get_actor_location()
def cmd(c):unreal.SystemLibrary.execute_console_command(w,c,pc)
cmd('r.ScreenPercentage 100');cmd('sg.ViewDistanceQuality 2');cmd('sg.PostProcessQuality 2');cmd('DisableAllScreenMessages 1')
def done(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._biome_photos_v11);p.set_actor_location(original,False,True);settings.set_editor_property('bThrottleCPUWhenNotForeground',old)
 (O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'fixture':'Explicit position-controlled photograph fixture, not a footwalk','rows':s['rows']},indent=2));unreal.log('BIOME_COMPARE_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['time']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<180
  if s['index']>=len(positions):done();return
  label,u,v=positions[s['index']]
  if s['stage']=='move':
   x,y,z=L.world(u,v);hit=unreal.SystemLibrary.line_trace_single(w,unreal.Vector(x,y,2500),unreal.Vector(x,y,-1000),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[p],unreal.DrawDebugTrace.NONE,True).to_tuple();assert hit[0],label
   p.set_actor_location(hit[5]+unreal.Vector(0,0,p.get_component_by_class(unreal.CapsuleComponent).get_scaled_capsule_half_height()+2),False,True);p.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();s.update(stage='shot',time=0);return
  if s['time']<2:return
  path=O/(label+'_QHD.png');assert not path.exists();cmd('HighResShot 2560x1440 filename="'+str(path)+'"')
  s['rows'].append({'label':label,'location':p.get_actor_location().to_tuple(),'camera_location':pc.player_camera_manager.get_camera_location().to_tuple(),'camera_rotation':pc.player_camera_manager.get_camera_rotation().to_tuple(),'size':[2560,1440],'screen_percentage':100,'path':str(path.relative_to(R))});s.update(index=s['index']+1,stage='move',time=0)
 except Exception:done(traceback.format_exc())
unreal._biome_photos_v11=unreal.register_slate_post_tick_callback(tick)
