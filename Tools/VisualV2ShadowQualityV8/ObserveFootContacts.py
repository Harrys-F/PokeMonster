import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir());S=R/'Saved/VisualV2ShadowQualityV8';j=json.loads((S/'AcceptanceRequest.json').read_text());D=S/'Acceptance'/j['label'];w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);state={'time':0,'last':0,'rows':[],'shots':0}
def tick(dt):
 state['time']+=dt
 if not hasattr(unreal,'_sv8_mid'):return
 q=p.get_actor_location();c=unreal._sv8_mid.get_vector_parameter_value('Contact0');delta=math.hypot(c.r-q.x,c.g-q.y)
 if state['time']-state['last']>5 and p.get_velocity().length()>80 and state['shots']<24:
  state['last']=state['time'];state['shots']+=1;file=D/('ContactMotion_'+str(state['shots']).zfill(2)+'.png');unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(file)+'"',pc);state['rows'].append({'time':state['time'],'player':q.to_tuple(),'contact_xy':[c.r,c.g],'lag_cm':delta,'speed':p.get_velocity().length(),'file':str(file),'viewport':list(pc.get_viewport_size())});(D/'ContactMotion.json').write_text(json.dumps(state['rows'],indent=2))
unreal._sv8_motion=unreal.register_slate_post_tick_callback(tick)
