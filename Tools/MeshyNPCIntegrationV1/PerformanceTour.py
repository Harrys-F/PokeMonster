import unreal,json,time,statistics,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Art/Characters/NPCs/IntegrationV1';label=json.loads((O/'MeasureLabel.json').read_text())['label'];w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name()=='Dev_TestMap_VisualV2'
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);s=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if x.get_world()==w);a=next(x for x in unreal.ObjectIterator(unreal.InputAction) if x.get_outer()==p and x.get_name()=='MoveAction')
quality=['sg.ViewDistanceQuality','sg.AntiAliasingQuality','sg.ShadowQuality','sg.GlobalIlluminationQuality','sg.ReflectionQuality','sg.PostProcessQuality','sg.TextureQuality','sg.EffectsQuality','sg.FoliageQuality','sg.ShadingQuality','r.ScreenPercentage','r.VSync','t.MaxFPS','r.GPUCsvStatsEnabled'];old={k:unreal.SystemLibrary.get_console_variable_float_value(k) for k in quality}
for k in quality:unreal.SystemLibrary.execute_console_command(w,k+' '+str(75 if k=='r.ScreenPercentage' else 0 if k in ['r.VSync','t.MaxFPS'] else 1))
# Request fixed rendering extent; record the real viewport rather than assuming it worked.
unreal.SystemLibrary.execute_console_command(w,'r.SetRes 1280x740w',pc)
route=[('measure','Dorf',None),('walk','Main',(-760,-1000)),('walk','Forest',(-740,-700)),('measure','Wald',None),('walk','BridgeApproach',(-500,-540)),('walk','BridgeEntry',(-350,-490)),('walk','BridgeExit',(-350,-140)),('walk','Path',(-20,-40)),('measure','OffenerWeg',None)]
i=0;start=time.monotonic();stage=start;last=p.get_actor_location();distance=0;stuck=0;frames=[];csv=False;out={'label':label,'settings':'Medium,75%,VSync off,uncapped','requested_viewport':[1280,740],'mode':'embedded Editor-PIE','points':[],'no_teleports':True}
def inject(x,y):s.inject_input_vector_for_action(a,unreal.Vector(x,y,0),[],[])
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._npc_perf);del unreal._npc_perf
 try:inject(0,0)
 except Exception:pass
 for k,v in old.items():unreal.SystemLibrary.execute_console_command(w,k+' '+str(v))
 out.update(error=error,distance_m=distance/100);(O/(label+'_Performance.json')).write_text(json.dumps(out,indent=2))
def tick(dt):
 global i,stage,last,distance,stuck,frames,csv
 try:
  now=time.monotonic();elapsed=now-stage;q=p.get_actor_location();step=(q-last).length();last=q;distance+=step
  if i>=len(route):finish();return
  kind,name,target=route[i]
  if kind=='walk':
   dx=target[0]-q.x;dy=target[1]-q.y
   if math.hypot(dx,dy)<25:inject(0,0);i+=1;stage=now;stuck=0;return
   yaw=math.radians(p.get_movement_basis_yaw());sx=-math.sin(yaw)*dx+math.cos(yaw)*dy;sy=math.cos(yaw)*dx+math.sin(yaw)*dy;ang=round(math.atan2(sx,sy)/(math.pi/4))*math.pi/4;inject(math.sin(ang),math.cos(ang));stuck=stuck+dt if step<.15 else 0;assert stuck<4,(name,q)
  else:
   inject(0,0)
   if elapsed<5:return
   if not csv:
    unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(O/(label+'_'+name+'.png'))+'"',pc);unreal.SystemLibrary.execute_console_command(w,'csvprofile startfile=NPCV1_'+label+'_'+name);unreal.SystemLibrary.execute_console_command(w,'csvprofile start');csv=True
   frames.append(dt*1000)
   if elapsed<20:return
   unreal.SystemLibrary.execute_console_command(w,'csvprofile stop');out['points'].append({'name':name,'location':q.to_tuple(),'viewport':list(pc.get_viewport_size()),'fps':1000/statistics.mean(frames),'frame_median_ms':statistics.median(frames),'samples':len(frames)});(O/(label+'_Performance.json')).write_text(json.dumps(out,indent=2));i+=1;stage=now;frames=[];csv=False
 except Exception as e:finish(str(e))
unreal._npc_perf=unreal.register_slate_post_tick_callback(tick)
