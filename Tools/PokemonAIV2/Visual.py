"""Real normal-camera species shots and unforced calm activity footage, plus
an explicitly labeled temporary social-profile fixture on the existing group.
No models, camera parameters, asset packages or maps are saved.
"""
import unreal,json,time,math,traceback,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/PokemonAIV2';label=json.loads((D/'ReviewRequest.json').read_text())['label'];O=D/label;O.mkdir(exist_ok=False)
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W;P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
S=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==GI);E=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==GI);assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_PokemonAI'+label)
wild=list(unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor));ids=['Bisasam','Pikachu','Zunderlauf','Myrapla','Enton','Nebulak'];subjects=[next(a for a in wild if str(a.visual_species.get_internal_id())==n)for n in ids]
user=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(user.read_bytes()).hexdigest();result={'shots':[],'samples':[],'technical_social_overrides':[],'checks':[],'ordinary_pie':True,'native_game_camera':True,'source_transforms_changed':False};s={'phase':'shots','i':0,'time':0.,'sample':0.,'last':unreal.GameplayStatics.get_time_seconds(W),'wall':time.monotonic(),'shot':False,'placed':False}
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def observer(a,d=190):
 m=a.overworld_movement;body=a.get_component_by_class(unreal.CapsuleComponent);q=a.get_actor_location()-unreal.Vector(0,0,body.get_scaled_capsule_half_height())
 for distance in [d,220,170,120]:
  for angle in range(0,360,30):
   r=math.radians(angle);v=q+unreal.Vector(math.cos(r)*distance,math.sin(r)*distance,0);g=m.project_walkable(v)
   if g:
    P.set_actor_location(unreal.Vector(g.x,g.y,g.z+50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();return
 raise RuntimeError('No clear observation pose for '+a.get_actor_label())
def shot(n):
 cmd('HighResShot 2560x1440 filename="'+str(O/(n+'.png'))+'"');result['shots'].append({'name':n,'time':unreal.GameplayStatics.get_time_seconds(W),'player':P.get_actor_location().to_tuple(),'target':subjects[min(s['i'],5)].get_actor_location().to_tuple()})
def phase(n):s.update(phase=n,time=0.,shot=False,placed=False)
def record(n):
 path=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('PokemonAIV2'+label+n);assert not path.exists();cmd('pm.TAAReview.CaptureStart '+str(path));result.setdefault('clips',[]).append(str(path.relative_to(R)))
def finish(error=None):
 cmd('pm.TAAReview.CaptureStop');unreal.unregister_slate_post_tick_callback(unreal._pokemon_ai_visual);result.update(passed=error is None,error=error,user_save_unchanged=hashlib.sha256(user.read_bytes()).hexdigest()==before);assert result['user_save_unchanged'];(O/'Result.json').write_text(json.dumps(result,indent=2));unreal.log('POKEMON_AI_VISUAL_DONE '+str(error))
cmd('pm.EnvPerf2.Viewport 2560 1440')
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(W);delta=now-s['last'];s['last']=now;s['time']+=delta;assert time.monotonic()-s['wall']<300
  assert not E.is_encounter_active(),'A diagnostic observation pose caused real contact; stop instead of altering encounter rules'
  if now-s['sample']>.5:
   s['sample']=now;result['samples'].append({'time':now,'phase':s['phase'],'actors':[{'species':str(a.visual_species.get_internal_id()),'position':a.get_actor_location().to_tuple(),'state':str(a.overworld_movement.behavior_state),'social_completed':a.overworld_movement.social_completed,'forage_completed':a.overworld_movement.forage_completed,'partner':a.overworld_movement.social_partner.get_owner().get_name()if a.overworld_movement.social_partner else None}for a in wild if a.overworld_movement.activities_enabled]});(O/'Progress.json').write_text(json.dumps({'phase':s['phase'],'i':s['i'],'elapsed':s['time']}))
  if s['phase']=='shots':
   if not s['placed']:observer(subjects[s['i']]);s['placed']=True;s['time']=0;return
   if s['time']>1 and not s['shot']:shot('%02d_%s_NormalGameCamera'%(s['i']+1,ids[s['i']]));s['shot']=True
   if s['time']>1.5:
    s['i']+=1
    if s['i']==len(subjects):s['i']=3;observer(subjects[3],190);record('MyraplaNatural');phase('calm')
    else:phase('shots')
  elif s['phase']=='calm':
   if s['time']>10 and not s['shot']:shot('07_Myrapla_NativeActivities');s['shot']=True
   if s['time']>25:
    cmd('pm.TAAReview.CaptureStop');result['checks'].append('25 seconds unforced Myrapla near-player native activity footage');phase('social_setup')
  elif s['phase']=='social_setup':
   group=[a for a in wild if str(a.visual_species.get_internal_id())=='Bisasam'];assert len(group)==3
   for a in group:
    m=a.overworld_movement;cfg=m.activities;cfg.wander_weight=.01;cfg.observe_weight=cfg.rest_weight=cfg.sleep_weight=cfg.forage_weight=0;cfg.social_weight=100
    m.set_movement_paused(True);m.set_editor_property('override_activities',True);m.set_editor_property('activity_override',cfg)
    b=m.get_behavior_profile();b.temperament=unreal.PokeMonsterOverworldTemperament.CALM;b.notice_radius=220;b.personal_space=110;b.disengage_radius=350;m.set_editor_property('override_behavior',True);m.set_editor_property('behavior_override',b)
    body=a.get_component_by_class(unreal.CapsuleComponent);m.configure(a.visual_species,body.get_scaled_capsule_half_height(),body.get_scaled_capsule_radius(),body.get_scaled_capsule_half_height(),None,3817+group.index(a)*137)
    result['technical_social_overrides'].append({'id':str(a.encounter_id),'position_unchanged':True,'profile':cfg.export_text(),'perception':b.export_text()})
   observer(group[0],200);s['group']=group;phase('social');return
  elif s['phase']=='social':
   if any(a.overworld_movement.social_partner for a in s['group'])and not s['shot']:record('SocialTechnicalFixture');shot('08_Social_TechnicalProfiles');s['shot']=True;s['social_start']=s['time']
   if any(a.overworld_movement.social_completed>0 for a in s['group']):
    result['checks'].append('Existing Bisasam group completed native paired visit with temporary social-only profiles; no new actors');phase('social_completed');return
   assert s['time']<60,'Technical social pair did not finish; retain actual result'
  elif s['phase']=='social_completed':
   if s['time']>3:shot('09_Social_ReturnToNormal');finish()
 except Exception:finish(traceback.format_exc());raise
unreal._pokemon_ai_visual=unreal.register_slate_post_tick_callback(tick)
