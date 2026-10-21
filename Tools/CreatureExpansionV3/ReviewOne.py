"""Actual native animation, companion movement and both ClassicBattle perspectives; explicit runtime fixture."""
import unreal,time,json,math,hashlib,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();req=json.loads((R/'Saved/CreatureExpansionV3/ReviewRequest.json').read_text());name=req['species'];profile=unreal.load_asset('/Game/Characters/Creatures/'+name+'/MeshyV1/DA_'+name+'_Presentation');label=req['label'];O=R/'Saved/CreatureExpansionV3'/label;w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w;p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w);e=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi);comp=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==w);inp=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if x.get_world()==w);move=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==p and x.get_name()=='MoveAction');sprint=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==p and x.get_name()=='SprintHoldAction');slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False);s=dict(phase='world',time=0.,last=unreal.GameplayStatics.get_time_seconds(w),wall=time.monotonic(),rows=[],case=0,fixture='Explicit existing party/battle review; wild profiles and zone triggers suspended only in this PIE instance. Not natural habitat encounter QA. World captures use unchanged game camera.');wild=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor)
for a in wild:
 a.get_component_by_class(unreal.PokeMonsterCreatureRoamingComponent).set_movement_paused(True);a.set_editor_property('profile',None) # Explicit isolated presentation fixture only; full gameplay tests retain profiles.
for zone in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterWildEncounterZone):zone.set_actor_enable_collision(False) # Isolated presentation fixture, not encounter QA.
def cmd(t):unreal.SystemLibrary.execute_console_command(w,t,pc)
def inject(dx=0,dy=0,run=False):
 yaw=math.radians(p.get_movement_basis_yaw());sx=-math.sin(yaw)*dx+math.cos(yaw)*dy;sy=math.cos(yaw)*dx+math.sin(yaw)*dy;inp.inject_input_vector_for_action(move,unreal.Vector(sx,sy,0),[],[]);inp.inject_input_vector_for_action(sprint,unreal.Vector(1 if run else 0,0,0),[],[])
def phase(v):s.update(phase=v,time=0.)
def finish(error=None):
 inject();unreal.unregister_slate_post_tick_callback(unreal._expansion_review);settings.set_editor_property('bThrottleCPUWhenNotForeground',old);s.update(passed=error is None,error=error,save_after_sha256=hashlib.sha256(slot.read_bytes()).hexdigest());(O/'Result.json').write_text(json.dumps(s,indent=2,default=lambda x:sorted(x)if isinstance(x,set)else str(x)));unreal.log('CREATURE_REVIEW_DONE '+name+' '+str(error))
cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');cmd('pm.StarterReview.Party '+name+' Zunderlauf');s['shots']=set()
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['time']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<210
  t=s['time']
  if s['phase']=='world':
   assert not e.is_encounter_active(),'Unexpected encounter in isolated presentation fixture';inject(0 if t<5 or t>=13 else -1 if t<9 else 1,0,run=t>=9)
   if t>3:
    v=comp.get_visual();assert v and v.mesh.get_skeletal_mesh_asset()==profile.mesh;assert not profile.get_validation_errors();assert v.get_actor_scale3d().distance(unreal.Vector(1,1,1))<.001
    for stamp in [4,8,12,16]:
     if t>=stamp and stamp not in s['shots']:
      assert pc.get_viewport_size()==(2560,1440);cmd('Shot filename='+str(O/(name+'_World_'+str(stamp)+'_QHD.png')));s['shots'].add(stamp);s['rows'].append(dict(stage='world',time=t,viewport=list(pc.get_viewport_size()),speed_cm_s=v.motion_speed,position=v.get_actor_location().to_tuple(),camera=pc.player_camera_manager.get_camera_location().to_tuple(),profile=profile.get_path_name()))
   if t>18:inject();phase('start')
  elif s['phase']=='start'and t>1:
   assert not e.is_encounter_active();a,b=(name,'Zunderlauf')if s['case']==0 else('Zunderlauf',name);cmd('pm.StarterReview.Start classic '+a+' '+b);assert e.is_encounter_active();phase('battle')
  elif s['phase']=='battle'and t>4:
   scene=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterClassicBattleScene)[0];assert scene.player_visual and scene.opponent_visual;assert scene.target.size_x==2560 and scene.target.size_y==1080;unreal.RenderingLibrary.export_render_target(w,scene.target,str(O),name+'_Battle_'+str(s['case'])+'.png');cmd('pm.CreatureReview.CaptureLiveUI Expansion_'+label+'_'+str(s['case']));s['rows'].append(dict(stage='classic',own=name if s['case']==0 else 'Zunderlauf',opponent='Zunderlauf'if s['case']==0 else name,target=[2560,1080],framing_distance_cm=scene.framing_distance,ui_capture='Saved/GlumandaV11/LiveUI/Expansion_'+label+'_'+str(s['case'])));s['reaction_index']=0;scene.player_visual.play_reaction(unreal.PokeMonsterCreatureClip.ATTACK);phase('reactions')
  elif s['phase']=='reactions'and t>1.35:
   scene=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterClassicBattleScene)[0];roles=['ATTACK','HIT','HAPPY','FAINT'];role=roles[s['reaction_index']];unreal.RenderingLibrary.export_render_target(w,scene.target,str(O),name+'_NativeReaction_'+str(s['case'])+'_'+role+'.png');s['reaction_index']+=1
   if s['reaction_index']<len(roles):scene.player_visual.play_reaction(getattr(unreal.PokeMonsterCreatureClip,roles[s['reaction_index']]));s['time']=0
   else:
    # Public visual reset; no species, session, asset or gameplay state changed.
    own_profile=profile if s['case']==0 else unreal.load_asset('/Game/Characters/Creatures/Zunderlauf/PolishV2/DA_Zunderlauf_Presentation');assert scene.player_visual.set_presentation(own_profile);v=e.get_presenter().get_view();index=next(i for i,m in enumerate(v.moves)if m.enabled);assert e.get_presenter().try_select_move(index);assert e.get_presenter().resolve_selection();phase('action')
  elif s['phase']=='action':
   if not e.is_encounter_active():phase('end');return
   if t>1 and not s.get('action_shot'):
    scene=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterClassicBattleScene)[0];unreal.RenderingLibrary.export_render_target(w,scene.target,str(O),name+'_Action_'+str(s['case'])+'.png');s['action_shot']=True
   v=e.get_presenter().get_view()
   if not v.busy and not v.finished:phase('flee')
  elif s['phase']=='flee':
   if not e.is_encounter_active():phase('end');return
   v=e.get_presenter().get_view()
   if t>1 and not v.busy and not v.finished:assert e.get_presenter().try_select_flee();assert e.get_presenter().resolve_selection();s['time']=0
  elif s['phase']=='end'and t>2 and not p.is_overworld_input_locked():
   s['case']+=1;s['action_shot']=False
   if s['case']>=2:finish();return
   phase('start')
 except Exception:finish(traceback.format_exc())
unreal._expansion_review=unreal.register_slate_post_tick_callback(tick)
