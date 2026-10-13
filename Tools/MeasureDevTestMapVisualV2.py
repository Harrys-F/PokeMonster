import unreal,json,math,time,statistics
from pathlib import Path
O=Path(unreal.Paths.project_dir()).resolve()/'Saved/DevTestMapVisualV2';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w.get_name() in ('Dev_TestMap','Dev_TestMap_VisualV2')
version='BeforeFinal' if w.get_name()=='Dev_TestMap' else globals().get('CAPTURE_LABEL','AfterFinal')
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);cm=p.get_component_by_class(unreal.CharacterMovementComponent);arm=p.get_component_by_class(unreal.SpringArmComponent);cam=p.get_component_by_class(unreal.CameraComponent);visual=p.get_editor_property('meshy_visual');assert visual.get_skeletal_mesh_asset().get_name()=='SK_Player_Meshy_V2'
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
quality=['sg.ViewDistanceQuality','sg.AntiAliasingQuality','sg.ShadowQuality','sg.GlobalIlluminationQuality','sg.ReflectionQuality','sg.PostProcessQuality','sg.TextureQuality','sg.EffectsQuality','sg.FoliageQuality','sg.ShadingQuality','r.ScreenPercentage','r.VSync','t.MaxFPS','r.GPUCsvStatsEnabled'];vals={k:unreal.SystemLibrary.get_console_variable_float_value(k) for k in quality};(O/(version+'_Quality.json')).write_text(json.dumps(vals,indent=2))
for k in quality:
 val=75 if k=='r.ScreenPercentage' else 0 if k in ('r.VSync','t.MaxFPS') else 1
 unreal.SystemLibrary.execute_console_command(w,k+' '+str(val))
s=next(s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if s.get_world()==w);a=next(a for a in unreal.ObjectIterator(unreal.InputAction) if a.get_outer()==p and a.get_name()=='MoveAction')
route=[('measure','Dorf',None),('walk','MainPath',(-760,-1000)),('walk','ForestApproach',(-740,-700)),('measure','Wald',None),('walk','BridgeApproach',(-500,-540)),('walk','BridgeEntry',(-350,-490)),('walk','BridgeExit',(-350,-140)),('walk','OpenWay',(-20,-40)),('measure','OffenerWeg',None)]
if version!='BeforeFinal':
 route.extend([('walk','ReturnBridgeNorth',(-350,-140)),('walk','ReturnBridgeSouth',(-350,-490)),('walk','ReturnMain',(-760,-1000)),('walk','ReturnStart',(-760,-1410)),('walk','VillageFork',(-1150,-1920)),('walk','VillageSouth',(-3350,-1700)),('walk','VillageWest',(-4150,-700)),('walk','HouseForecourt',(-4100,450)),('measure','HeilhausVillage',None),('walk','NorthForest',(-4300,1550)),('measure','DichterWald',None)])
i=0;started=time.monotonic();stage=started;last=p.get_actor_location();dist=0;stuck=0;frames=[];out={'checks':[],'measurements':[],'no_teleports':True,'map':w.get_path_name(),'mode':'InEditorFloating PIE (in-process)','warmup_s':5,'capture_s':20};capture=False;csv=False
def inject(x,y):s.inject_input_vector_for_action(a,unreal.Vector(x,y,0),[],[])
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._visualv2_perf);del unreal._visualv2_perf
 try:inject(0,0)
 except Exception:pass
 out.update(error=error,distance_m=dist/100);(O/(version+'_Performance.json')).write_text(json.dumps(out,indent=2))
def tick(dt):
 global i,stage,last,dist,stuck,frames,capture,csv
 try:
  q=p.get_actor_location();step=(q-last).length();last=q;dist+=step;now=time.monotonic();elapsed=now-stage
  if i>=len(route):finish();return
  kind,name,target=route[i]
  if kind=='walk':
   dx=target[0]-q.x;dy=target[1]-q.y
   if math.hypot(dx,dy)<25:inject(0,0);out['checks'].append({'name':name,'position':q.to_tuple()});i+=1;stage=now;stuck=0;return
   yaw=math.radians(p.get_movement_basis_yaw());sx=-math.sin(yaw)*dx+math.cos(yaw)*dy;sy=math.cos(yaw)*dx+math.sin(yaw)*dy;ang=round(math.atan2(sx,sy)/(math.pi/4))*math.pi/4;inject(math.sin(ang),math.cos(ang));stuck=stuck+dt if step<.15 else 0;assert stuck<4,(name,q)
  else:
   inject(0,0)
   if elapsed<2:return
   if not capture:
    unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(O/(version+'_'+name+'.png'))+'"',pc);capture=True
   if elapsed<5:return
   if not csv:unreal.SystemLibrary.execute_console_command(w,'csvprofile startfile=VisualV2_'+version+'_'+name);unreal.SystemLibrary.execute_console_command(w,'csvprofile start');csv=True
   frames.append(dt*1000)
   if elapsed<25:return
   unreal.SystemLibrary.execute_console_command(w,'csvprofile stop');out['measurements'].append({'name':name,'position':q.to_tuple(),'viewport':list(pc.get_viewport_size()),'fps':1000/statistics.mean(frames),'median_ms':statistics.median(frames),'p95_ms':sorted(frames)[int(.95*len(frames))],'samples':len(frames),'quality':'Medium/75%,VSync off,uncapped','player_mesh':visual.get_skeletal_mesh_asset().get_path_name(),'camera':[arm.target_arm_length,arm.get_world_rotation().pitch,arm.get_world_rotation().yaw,cam.field_of_view]});(O/(version+'_Performance.json')).write_text(json.dumps(out,indent=2));frames=[];i+=1;stage=now;capture=False;csv=False
 except Exception as e:finish(str(e))
unreal._visualv2_perf=unreal.register_slate_post_tick_callback(tick)
