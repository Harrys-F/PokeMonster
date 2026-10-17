import unreal,json,time,statistics
from pathlib import Path
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();pc=unreal.GameplayStatics.get_player_controller(w,0);v=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor));P=Path(unreal.Paths.project_dir(),'Art/Characters/NPCs/IntegrationV1');old={k:unreal.SystemLibrary.get_console_variable_float_value(k) for k in ['r.ScreenPercentage','r.VSync','t.MaxFPS','sg.ViewDistanceQuality','sg.AntiAliasingQuality','sg.ShadowQuality','sg.GlobalIlluminationQuality','sg.ReflectionQuality','sg.PostProcessQuality','sg.TextureQuality','sg.EffectsQuality','sg.FoliageQuality','sg.ShadingQuality']};(P/'ScopedCostSettingsBefore.json').write_text(json.dumps(old,indent=2));phases=[False,True,False,True];i=0;stage=time.monotonic();frames=[];out=[]
for k,val in [(k,75 if k=='r.ScreenPercentage' else 0 if k in ['r.VSync','t.MaxFPS'] else 1) for k in old]:unreal.SystemLibrary.execute_console_command(w,k+' '+str(val))
v.use_visual=False;v.refresh_presentation()
def tick(dt):
 global i,stage,frames
 elapsed=time.monotonic()-stage
 if elapsed>2:frames.append(dt*1000)
 if elapsed<8:return
 out.append({'ranger_enabled':phases[i],'fps':1000/statistics.mean(frames),'median_frame_ms':statistics.median(frames),'viewport':list(pc.get_viewport_size())});i+=1;stage=time.monotonic();frames=[]
 if i>=len(phases):
  v.use_visual=True;v.refresh_presentation()
  for k,val in old.items():unreal.SystemLibrary.execute_console_command(w,k+' '+str(val))
  unreal.unregister_slate_post_tick_callback(unreal._npc_cost);del unreal._npc_cost;(P/'ScopedPresentationCost.json').write_text(json.dumps(out,indent=2));return
 v.use_visual=phases[i];v.refresh_presentation()
unreal._npc_cost=unreal.register_slate_post_tick_callback(tick)
