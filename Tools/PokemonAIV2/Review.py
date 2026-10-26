"""Ordinary VisualV2 PIE, real native AI and game camera. Isolated save only.
Diagnostic relocations are recorded; actual input is used during the walking leg.
No creature positions, species profiles, scenery or cameras are changed.
"""
import unreal,json,time,traceback,math,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/PokemonAIV2';request=json.loads((D/'ReviewRequest.json').read_text());label=request['label'];assert label.isalnum();O=D/label;O.mkdir(exist_ok=False)
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W
P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
def sub(c):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==GI)
E=sub(unreal.PokeMonsterEncounterSubsystem);S=sub(unreal.PokeMonsterSaveSubsystem)
assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_PokemonAI'+label)
assert not E.is_encounter_active(),'Fresh ordinary PIE required before this review'
user=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(user.read_bytes()).hexdigest()
wild=list(unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor));subjects=[a for a in wild if a.overworld_movement.activities_enabled]
assert len(subjects)==8
result={'ordinary_pie':True,'diagnostic_relocations':[],'checks':[],'samples':[],'frames':[],'original_save_sha256':before,'physical_controller_test':False}
s={'phase':'autonomous','time':0.,'last':unreal.GameplayStatics.get_time_seconds(W),'sample':0.,'wall':time.monotonic(),'shot':0,'walk_start':None}
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def axis(x=0,y=0):
 yaw=math.radians(P.get_movement_basis_yaw());cmd('pm.Input.Axis Gamepad_LeftX '+str(-math.sin(yaw)*x+math.cos(yaw)*y));cmd('pm.Input.Axis Gamepad_LeftY '+str(math.cos(yaw)*x+math.sin(yaw)*y))
def place(q):
 axis()
 # A runtime diagnostic move must not land inside a roaming territorial animal.
 candidates=[q]+[(q[0]+x,q[1]+y)for x,y in [(250,0),(-250,0),(0,250),(0,-250),(350,350),(-350,-350)]]
 chosen=None
 for v in candidates:
  valid=True
  for a in wild:
   if a.life_state!=unreal.PokeMonsterWildLifeState.ACTIVE:continue
   d=math.hypot(v[0]-a.get_actor_location().x,v[1]-a.get_actor_location().y)
   b=a.overworld_movement.get_behavior_profile();contact=b.temperament in [unreal.PokeMonsterOverworldTemperament.TERRITORIAL,unreal.PokeMonsterOverworldTemperament.AGGRESSIVE]
   if d<(760 if contact else 130):valid=False;break
  if valid:chosen=v;break
 assert chosen is not None,('No safe diagnostic player point',q)
 P.set_actor_location(unreal.Vector(chosen[0],chosen[1],50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();result['diagnostic_relocations'].append({'time':unreal.GameplayStatics.get_time_seconds(W),'requested':q,'position':chosen})
def phase(n):s.update(phase=n,time=0.)
def shot(n):cmd('HighResShot 2560x1440 filename="'+str(O/(n+'.png'))+'"')
def finish(error=None):
 axis();cmd('pm.TAAReview.CaptureStop');unreal.unregister_slate_post_tick_callback(unreal._pokemon_ai_review)
 result.update(passed=error is None,error=error,seconds=unreal.GameplayStatics.get_time_seconds(W),original_save_unchanged=hashlib.sha256(user.read_bytes()).hexdigest()==before)
 assert result['original_save_unchanged'];(O/'Result.json').write_text(json.dumps(result,indent=2));unreal.log('POKEMON_AI_CONNECTED_DONE '+str(error))
place((-300,2100));cmd('pm.EnvPerf2.Viewport 2560 1440')
clip=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('PokemonAIV2'+label);assert not clip.exists()
if request.get('capture',False):cmd('pm.TAAReview.CaptureStart '+str(clip))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(W);delta=now-s['last'];s['last']=now;s['time']+=delta
  assert time.monotonic()-s['wall']<650,'Wall timeout'
  if now-s['sample']>.5:
   s['sample']=now
   rows=[]
   for a in subjects:
    m=a.overworld_movement;q=a.get_actor_location();body=a.get_component_by_class(unreal.CapsuleComponent)
    assert m.is_inside_habitat(q-unreal.Vector(0,0,body.get_scaled_capsule_half_height()))or m.escaping_defeat,(a.get_actor_label(),'Outside habitat')
    rows.append({'id':str(a.encounter_id),'species':str(a.visual_species.get_internal_id()),'state':str(m.behavior_state),'position':q.to_tuple(),'speed':m.current_speed,'decisions':m.activity_decisions,'perception_queries':m.peer_queries,'traces':m.perception_traces,'social_completed':m.social_completed,'forage_completed':m.forage_completed,'partner':m.social_partner.get_owner().get_name()if m.social_partner else None,'travelling':m.is_activity_travelling(),'distant':m.activity_distant,'plans':m.successful_plans,'blocked':m.blocked_steps,'distance':m.distance_travelled})
   result['samples'].append({'time':now,'phase':s['phase'],'player':P.get_actor_location().to_tuple(),'encounter':E.is_encounter_active(),'subjects':rows})
   (O/'Progress.json').write_text(json.dumps({'phase':s['phase'],'elapsed':s['time'],'states':[(x['species'],x['state'])for x in rows]},indent=2))
  if s['phase']=='autonomous':
   assert not E.is_encounter_active(),'Unexpected distant battle'
   if s['time']>5 and s['shot']==0:shot('01_Myrapla_OrdinaryGameCamera');s['shot']=1
   if s['time']>75:
    cmd('pm.TAAReview.CaptureStop');result['checks'].append('75 seconds autonomous native wild behavior without any forced state or spawn');place((-300,300));phase('observe');return
  elif s['phase']=='observe':
   assert not E.is_encounter_active(),'Approach without contact started battle'
   if s['time']>5 and s['shot']==1:shot('02_Bisasam_Pikachu_Group');s['shot']=2
   if s['time']>24:place((-1900,-1000));phase('shy');return
  elif s['phase']=='shy':
   assert not E.is_encounter_active(),'Shy actor auto-started battle'
   if s['time']>5 and s['shot']==2:shot('03_Nebulak_Observed');s['shot']=3
   if s['time']>15:place((700,-1300));phase('enton');return
  elif s['phase']=='enton':
   assert not E.is_encounter_active(),'Shy Enton auto-started battle'
   if s['time']>4 and s['shot']==3:shot('04_Enton_Approach');s['shot']=4
   if s['time']>14:place((-200,-100));phase('walk');s['walk_start']=P.get_actor_location().to_tuple();axis(0,1);return
  elif s['phase']=='walk':
   if s['time']>2:
    axis();assert math.dist(s['walk_start'],P.get_actor_location().to_tuple())>100,'Normal movement blocked';result['checks'].append('Real input walking leg >100 cm with ordinary camera/controller mapping');phase('savewait');return
  elif s['phase']=='savewait':
   if s['time']>1:
    assert S.save_current_game(),'Isolated save failed';s['pose']=P.get_actor_location().to_tuple();s['party']=[(x.instance_id.to_string(),str(x.species),x.level,x.current_hp)for x in E.get_player_party()];place((150,0));assert S.load_game();phase('loadwait');return
  elif s['phase']=='loadwait':
   if s['time']>2:
    assert math.dist(s['pose'],P.get_actor_location().to_tuple())<.5,'Saved location changed'
    assert s['party']==[(x.instance_id.to_string(),str(x.species),x.level,x.current_hp)for x in E.get_player_party()],'Persistent Pokemon changed'
    result['checks'].append('Isolated native disk Save/Load preserves pose, instances, levels and HP while AI resumes');phase('resume');return
  elif s['phase']=='resume':
   if s['time']>8:
    assert not P.is_overworld_input_locked();shot('05_AfterLoad_NormalOverworld');finish()
 except Exception as ex:finish(traceback.format_exc());raise
unreal._pokemon_ai_review=unreal.register_slate_post_tick_callback(tick)
