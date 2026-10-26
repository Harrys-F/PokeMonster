"""Extend the existing real input/physics route with one connected party/battle/progression/heal/RAM-save journey."""
import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GameplayPraxisV1';request=json.loads((D/'Request.json').read_text());extra={'fixture':'Existing EvolutionReview.Party creates Glumanda15 + independent Glurak36; one XP before16. All changes RAM-only. Wild actors/HP/profiles remain unchanged.','battles':[],'defeated_sources':{},'snapshots':[],'companion_max_distance_cm':0.,'companion_samples':0,'party_swap_verified':False}

def cmd_key(k):cmd('pm.Input.Key '+k+' down');cmd('pm.Input.Key '+k+' up')
def instance_snapshot():
 inv=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterInventorySubsystem)if x.get_outer()==GI)
 return {'party':[c.export_text()for c in Enc.get_player_party()],'inventory':[x.export_text()for x in inv.get_stacks()],'completed':{str(a.encounter_id):Enc.is_encounter_completed(a.encounter_id)for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor)},'trainers':sorted(str(x)for x in Enc.get_defeated_trainer_ids()),'position':P.get_actor_location().to_tuple()}
def setup_fixture():
 cmd('pm.EvolutionReview.Party Zunderlauf 15');team=Enc.get_player_party();assert len(team)==2 and team[0].level==15
 remaining=unreal.PokeMonsterCreatureProgression.experience_to_next_level(team[0]);assert remaining>1;cmd('pm.EvolutionReview.XP '+str(remaining-1));team=Enc.get_player_party()
 extra['fire_id']=team[0].instance_id.to_string();extra['xp_before']=team[0].experience;extra['level_before']=team[0].level
 assert Enc.reorder_party(team[1].instance_id,0);extra['original_fixture_ids']=[c.instance_id.to_string()for c in Enc.get_player_party()]

def observe_world():
 for key,a in list(extra.get('_sources',{}).items()):
  rows=extra['defeated_sources'].setdefault(key,[]);now=unreal.GameplayStatics.get_time_seconds(W)
  if not rows or now-rows[-1]['time']>.2:
   rows.append({'time':now,'life':str(a.life_state),'position':a.get_actor_location().to_tuple(),'outside':a.is_outside_player_view(),'hidden':a.get_editor_property('hidden')})
   if a.life_state==unreal.PokeMonsterWildLifeState.REMOVED and(len(rows)<2 or'REMOVED'not in rows[-2]['life']):assert a.is_outside_player_view(),'Defeated source removed in view'
 if not Enc.is_encounter_active():
  visual=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==W).get_visual()
  visible=[a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterCreatureVisualActor)if'CreaturePartyCompanion'in[str(x)for x in a.tags]and not a.get_editor_property('hidden')]
  assert len(visible)<=1,'Duplicate visible companions'
  if visual and not visual.get_editor_property('hidden'):
   expected=Enc.get_player_party()[0].species.get_visuals().presentation
   if expected:assert visual.mesh.get_skeletal_mesh_asset()==expected.mesh
   extra['companion_samples']+=1;extra['companion_max_distance_cm']=max(extra['companion_max_distance_cm'],visual.get_actor_location().distance(P.get_actor_location()))

def process_actual_battle(pr,v,loc):
 if not loc.get('battle'):
  loc['battle']=True;s['battles']+=1;row={'start_position':P.get_actor_location().to_tuple(),'rounds':[],'start_party':instance_snapshot(),'goal':'Fled'if extra.get('level_after')else'Victory','classic':Enc.get_battle_widget().is_classic_presentation()};extra['battles'].append(row);assert row['classic']
 row=extra['battles'][-1]
 if v.round and (not row['rounds']or row['rounds'][-1]['round']!=v.round):
  events=[{'type':str(x.type),'xp':x.experience_added,'level_before':x.level_before,'level_after':x.level_after,'pp_before':x.pp_before,'pp_after':x.pp_after}for x in pr.get_last_result().events];row['rounds'].append({'round':v.round,'events':events})
 if v.learning_move:
  # Real B/A route: accept by selecting slot4, whose old move remains in repertoire.
  Enc.get_battle_widget().set_battle_menu(unreal.PokeMonsterBattleMenu.MOVES);cmd_key('Gamepad_DPad_Down');cmd_key(B);return
 if not v.busy and not v.finished:
  if v.must_switch:assert pr.try_select_switch(next(i for i,c in enumerate(v.player_team)if c.can_switch))
  elif row['goal']=='Fled'and v.flee_enabled:assert pr.try_select_flee()
  else:
   names=[str(x.name)for x in v.moves];i=names.index('Kratzer')if'Kratzer'in names else next(i for i,x in enumerate(v.moves)if x.enabled);assert pr.try_select_move(i)
  assert pr.resolve_selection()

def returned_from_battle(loc):
 if loc.pop('battle',False):
  end=Enc.get_last_result();row=extra['battles'][-1];row['outcome']=str(end.outcome);assert end.outcome in [unreal.PokeMonsterEncounterOutcome.VICTORY,unreal.PokeMonsterEncounterOutcome.FLED],str(end.outcome)
  row.update(outcome=str(end.outcome),returned_position=P.get_actor_location().to_tuple(),end_party=instance_snapshot());a=end.source_actor
  if end.outcome==unreal.PokeMonsterEncounterOutcome.FLED:return
  assert isinstance(a,unreal.PokeMonsterVisibleWildCreatureActor),'Connected journey did not use an existing natural wild source';key=str(a.encounter_id);extra.setdefault('_sources',{})[key]=a
  creature=next(c for c in Enc.get_player_party()if c.instance_id.to_string()==extra['fire_id']);assert creature.experience>extra['xp_before'] and creature.level>=16;extra['xp_after']=creature.experience;extra['level_after']=creature.level
  loc['victory']=True;cmd('pm.CreatureReview.CaptureLiveUI Praxis'+request['label']+'AfterVictory')

def verify_final_journey():
 assert extra['party_swap_verified'] and extra['battles'] and extra.get('level_after',0)>=16 and extra['snapshots']
 assert any(any('EXPERIENCE_GAINED'in e['type']for e in r['events'])for b in extra['battles']for r in b['rounds'])
 assert 'VICTORY'in extra['battles'][0]['outcome']and all(any(t in b['outcome']for t in ['VICTORY','FLED'])for b in extra['battles'])
 assert extra['companion_samples']>50
 for key,rows in extra['defeated_sources'].items():
  assert any('ESCAPING'in r['life']or'WAITING_FOR_EXIT'in r['life']for r in rows),('No visible recovery/escape sampled',key)
 extra.pop('_sources',None)


def steer_around_obstacle(dx,dy,distance,delta,travelled,loc,t,name):
 s['stuck']=s['stuck']+delta if travelled<.1 else 0.
 if s['stuck']>.8 and t>=loc.get('detour_until',0):
  assert not P.is_overworld_input_locked(),'Input remains locked after battle'
  attempts=loc.get('detours',0);assert attempts<6,('No walkable detour',name,P.get_actor_location());q=P.get_actor_location();near=[]
  for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
   if a==P:continue
   c,e=a.get_actor_bounds(True,False)
   if abs(c.x-q.x)<e.x+60 and abs(c.y-q.y)<e.y+60 and c.z+e.z>10 and c.z-e.z<150:
    near.append({'actor':a.get_actor_label(),'class':a.get_class().get_name(),'position':a.get_actor_location().to_tuple(),'center':c.to_tuple(),'extent':e.to_tuple()})
  extra.setdefault('obstacle_detours',[]).append({'route':name,'position':q.to_tuple(),'locked':P.is_overworld_input_locked(),'nearby_blockers':near,'method':'Actual sideways stick input; no collision changes or teleport'})
  sign=1 if attempts%2==0 else-1;length=max(distance,1);loc.update(detours=attempts+1,detour_until=t+1.05,detour_vector=(-dy/length*sign,dx/length*sign));s['stuck']=0.
 if t<loc.get('detour_until',0):dx,dy=loc['detour_vector'];distance=100
 x,y=worldinput(dx,dy);ang=round(math.atan2(x,y)/(math.pi/4))*math.pi/4;mag=max(.38,min(1,distance/90));axis(math.sin(ang)*mag,math.cos(ang)*mag);assert s['stuck']<5,('Blocked',name,P.get_actor_location())

source=(R/'Tools/VisualV2EnvironmentV3/Footrun.py').read_text();source=source.replace("R/'Saved/ProjectRefinement/EnvironmentV3/FootrunFinal'", "R/'Saved/ProjectRefinement/GameplayPraxisV1'/request['label']/'Footrun'")
source=source.replace('# Test setup only, before distance/time accounting. No subsequent test teleport.', "setup_fixture()\n# Test setup only, before distance/time accounting. No subsequent test teleport.")
source=source.replace("add('menu','MenuFocus');walk('Main1'", "add('pause','FixtureSettle',1);add('swap','SwapLeadingCompanion');add('menu','MenuFocus');add('seek','NaturalWildEncounter');walk('Main1'")
source=source.replace("walk('Main2',-760,-820)", "walk('WandererApproach',-825,-1080);add('hold','FaceWanderer',(-1,0,.12));add('interact','OriginalWanderer');add('dialog','WandererPages');walk('Main2',-760,-820)")
source=source.replace("'input':'existing pm.Input software simulation, no hardware claim'", "'input':'existing pm.Input software simulation, no hardware claim','connected_journey':{k:v for k,v in extra.items()if k!='_sources'}")
source=source.replace("if s['i']==len(route):finish();return", "if s['i']==len(route):verify_final_journey();finish();return")
start=source.index("  if Enc.is_encounter_active():\n");end=source.index("  if k=='walk':",start)
source=source[:start]+'''  observe_world()
  if Enc.is_encounter_active():
   axis(0,0);pr=Enc.get_presenter();v=pr.get_view();process_actual_battle(pr,v,loc);s['elapsed']-=delta;return
  returned_from_battle(loc)
'''+source[end:]
source=source.replace("   x,y=worldinput(dx,dy);ang=round(math.atan2(x,y)/(math.pi/4))*math.pi/4;mag=max(.38,min(1,distance/90));axis(math.sin(ang)*mag,math.cos(ang)*mag);s['stuck']=s['stuck']+delta if d<.1 else 0;assert s['stuck']<5,('Blocked',name,pos)", "   steer_around_obstacle(dx,dy,distance,delta,d,loc,t,name)")
source=source.replace("  elif k=='save':assert Save.save_current_game() and Save.load_game();assert hashlib.sha256(slot.read_bytes()).hexdigest()==sha;progress({'ram_only':True})",'''  elif k=='save':
   before=instance_snapshot();assert Save.save_current_game();inv=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterInventorySubsystem)if x.get_outer()==GI);item=unreal.load_asset('/Game/Data/Items/DA_TestHealingItem');assert inv.add_item(item,1)
   if len(Enc.get_player_party())>1:assert Enc.reorder_party(Enc.get_player_party()[1].instance_id,0)
   assert Save.load_game();after=instance_snapshot();assert before==after,(name,'RAM snapshot differs');assert hashlib.sha256(slot.read_bytes()).hexdigest()==sha;extra['snapshots'].append({'step':name,'exact_party_inventory_completion_position_roundtrip':True});progress({'ram_only':True})''')
source=source.replace("  elif k=='heal':assert all(c.current_hp==c.calculated_stats.max_hp for c in Enc.get_player_party());progress()", "  elif k=='heal':\n   assert all(c.current_hp==c.calculated_stats.max_hp and all(not x.get_editor_property('move')or x.current_pp==x.get_editor_property('move').max_pp for x in c.get_editor_property('move_slots'))for c in Enc.get_player_party());extra['healed_hp_and_pp']=True;progress()")
source=source.replace("  elif k=='menu':",'''  elif k=='seek':
   if loc.get('victory'):axis(0,0);progress({'natural_source_victory':True})
   else:
    target=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor)if str(a.encounter_id)=='Dev_VisibleWild');dx=target.get_actor_location().x-pos.x;dy=target.get_actor_location().y-pos.y;distance=max(1,math.hypot(dx,dy));x,y=worldinput(dx/distance,dy/distance);axis(x,y);assert t<45,'Could not reach existing natural wild contact'
  elif k=='swap':
   if not loc.get('opened'):cmd_key('Gamepad_FaceButton_Left'if backend else'Gamepad_FaceButton_Top');loc['opened']=True
   if t>.4 and not loc.get('selected'):cmd_key('Gamepad_DPad_Down');cmd_key(B);loc['selected']=True
   if t>.8 and not loc.get('target'):cmd_key('Gamepad_DPad_Up');cmd_key(B);loc['target']=True
   if t>1.3:
    cmd_key('Gamepad_FaceButton_Bottom'if backend else'Gamepad_FaceButton_Right');assert not PC.is_menu_open();assert Enc.get_player_party()[0].instance_id.to_string()==extra['fire_id'];extra['party_swap_verified']=True;progress()
  elif k=='menu':''')
exec(compile(source,'existing_route_with_connected_gameplay_checks','exec'),globals())
