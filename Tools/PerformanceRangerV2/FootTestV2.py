"""Complete walking/interaction route in the VisualV2 copy. No test teleports.
Controlled runtime Save/Load test uses the real dev slot; back it up before running.
"""

# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import unreal,json,math,time,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Art/Characters/NPCs/Ranger/Review/V2/FootTest';O.mkdir(exist_ok=True);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name()=='Dev_TestMap_RangerPerfV2'
assert hashlib.sha256((R/'Saved/SaveGames/PokeMonster_Dev.sav').read_bytes()).hexdigest()==json.loads((R/'Art/Characters/NPCs/Ranger/Review/V2/DevSaveBackup.json').read_text())['sha256'],'Dev save changed since backup; do not overwrite user progress'
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);cm=p.get_component_by_class(unreal.CharacterMovementComponent);arm=p.get_component_by_class(unreal.SpringArmComponent);cam=p.get_component_by_class(unreal.CameraComponent);cut=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterBuildingCutaway) if 'V2_House' in a.get_actor_label())
gi=unreal.GameplayStatics.get_game_instance(w)
def subsystem(cls):return next(s for s in unreal.ObjectIterator(cls) if s.get_outer()==gi)
enc=subsystem(unreal.PokeMonsterEncounterSubsystem);dialog=subsystem(unreal.PokeMonsterDialogueSubsystem);save=subsystem(unreal.PokeMonsterSaveSubsystem);inv=subsystem(unreal.PokeMonsterInventorySubsystem)
s=next(s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if s.get_world()==w);move=next(a for a in unreal.ObjectIterator(unreal.InputAction) if a.get_outer()==p and a.get_name()=='MoveAction')
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
visual=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor));assert visual.visual.get_skeletal_mesh_asset().get_name()=='SK_Ranger_NPC_V2_Clean';sprite=visual.source_actor.get_component_by_class(unreal.PaperSpriteComponent);assert not sprite.is_visible();visual.set_editor_property('bUseVisual',False);visual.refresh_presentation();assert sprite.is_visible() and not visual.visual.is_visible();visual.set_editor_property('bUseVisual',True);visual.refresh_presentation();assert not sprite.is_visible() and visual.visual.is_visible()
route=[]
def add(kind,name,arg=None):route.append((kind,name,arg))
def walk(name,x,y):add('walk',name,(x,y))
def face(name,x,y):add('face',name,(x,y))
def shot(name):add('shot',name)
add('menu','Menu');shot('Dorf');walk('WandererApproach',-835,-1080);face('WandererFacing',-1,0);add('interact','Wanderer');add('dialog','QuestDialogue')
walk('WildBranchEntry',-850,-1380);walk('WildApproach',-950,-1450);face('WildFacing',-1,0);add('interact','Wild');add('battle','WildCapture');shot('WildBranch');walk('BackMain',-760,-1160);walk('TrainerApproachA',-760,-820);walk('TrainerApproach',-670,-600);face('TrainerFacing',-1,0);add('interact','Liora');add('dialog','TrainerDialogue');add('battle','TrainerBattle');add('verifytrainer','TrainerVictory');shot('Wald')
walk('BridgeApproach',-500,-540);walk('BridgeEntry',-350,-490);walk('BridgeMid',-350,-320);shot('BachBruecke');walk('BridgeExit',-350,-130);walk('OpenWay',-20,-40);shot('OffenerWeg');walk('Pass1',220,160);walk('Pass2',410,280);walk('ArchiveApproach',700,590);walk('Archive',745,680);face('ArchiveFacing',1,0);add('save','SaveLoad');shot('Ruinen');add('interact','ArchiveStone');add('dialog','ArchiveActivation');add('verifygoal','ArchiveComplete')
walk('ArchiveReturn',700,590);walk('PassReturn2',410,280);walk('PassReturn1',220,160);walk('BridgeNorthReturn',-350,-130);walk('BridgeSouthReturn',-350,-490);walk('ReturnForest',-740,-720);walk('ReturnNPC',-835,-1080);face('ReturnNPCFacing',-1,0);add('interact','WandererCompleted');add('dialog','CompletedDialogue')
walk('BackStart',-760,-1410);walk('VillageFork',-1150,-1920);walk('VillagePath',-2100,-2060);walk('VillageSouth',-3350,-1700);walk('VillageWest',-4150,-700);walk('HealerForecourt',-4100,450);shot('Heilhaus');walk('HouseDoor',-3610,500);face('DoorStraight',1,0);add('hold','DoorEntry',(1,0,.85));add('pause','InteriorReady',.8);shot('Innenraum');add('verifyinside','CutawayInside')
walk('InteriorAisle',16900,670);walk('HealerSideAisle',17230,650);walk('HealerApproach',17230,555);face('HealerFacing',0,-1);add('interact','Healer');add('dialog','Healing');add('verifyheal','HealingSaveCheckpoint')
walk('HealerReturn',17230,650);walk('InteriorFront',16900,670);walk('InsideDoor',16460,500);add('hold','DoorExit',(-1,0,.85));add('pause','OutsideReady',.8);add('verifyoutside','CutawayOutside');walk('DiagonalDoorApproach',-3610,560);add('hold','DiagonalEntry',(1,-1,.65));add('pause','DiagonalReady',.8);add('verifyinside','DiagonalInside');walk('DiagonalInsideDoor',16460,540);add('hold','DiagonalExit',(-1,-1,.85));add('pause','DiagonalOutsideReady',.8);add('verifyoutside','DiagonalOutside')
walk('NorthFork',-4100,450);walk('NorthForest',-4300,1550);shot('DichterWald');walk('NorthRidge',-3300,2050);walk('NorthEast',-2150,2000);walk('ForestEast',-1700,1220);walk('ForestMiddle',-1550,650);walk('CrownApproach',-1900,530);shot('CrownReveal_On');add('crownoff','CrownRevealDiagnosticOff');shot('CrownReveal_Off');add('crownrestore','CrownRevealRestored');walk('ForestMiddleReturn',-1550,650);walk('ForestSouth',-1580,-100);walk('ForestReturn',-1560,-860);walk('VillageReturn',-1520,-1830);walk('StartReturn1',-1150,-1920);walk('StartReturn',-760,-1410);add('directions','AllEight');add('menu','MenuAfterTour');shot('Final')
crown_swaps={}
i=0;seconds=0.;stage=0.;last=p.get_actor_location();dist=0.;stuck=0.;local={};out={'npc_sprite_fallback_checked':True,'ranger_mesh':'SK_Ranger_NPC_V2','steps':[],'no_test_teleports':True,'max_speed_cm_s':0,'original_maps_unchanged':True};wall=time.monotonic();log=(O/'FootFrames.jsonl').open('w')
def inject(x,y):s.inject_input_vector_for_action(move,unreal.Vector(x,y,0),[],[])
def worldinput(dx,dy):
 yaw=math.radians(p.get_movement_basis_yaw());return -math.sin(yaw)*dx+math.cos(yaw)*dy,math.cos(yaw)*dx+math.sin(yaw)*dy
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._visualv2_foot);del unreal._visualv2_foot
 try:inject(0,0)
 except Exception:pass
 for c,ms in crown_swaps.items():
  for j,m in enumerate(ms):c.set_material(j,m)
 log.close();out.update(passed=error is None,error=error,distance_m=dist/100,game_seconds=seconds,wall_seconds=time.monotonic()-wall);(O/'FootTest.json').write_text(json.dumps(out,indent=2));unreal.log('VISUAL_V2_FOOT_DONE '+str(error))
def progress(extra=None):
 global i,stage,stuck,local
 q=p.get_actor_location();out['steps'].append({'name':route[i][1],'position_cm':q.to_tuple(),'relocated':cut.is_viewer_relocated(),'input_locked':p.is_overworld_input_locked(),'time':seconds,**(extra or {})});(O/'FootProgress.json').write_text(json.dumps(out['steps'],indent=2));i+=1;stage=seconds;stuck=0;local={}
def tick(dt):
 global i,seconds,last,dist,stuck
 try:
  seconds+=dt;q=p.get_actor_location();step=(q-last).length()
  if step<1000:dist+=step
  last=q;speed=math.hypot(p.get_velocity().x,p.get_velocity().y);out['max_speed_cm_s']=max(speed,out['max_speed_cm_s']);assert cm.max_walk_speed==210 and cam.field_of_view==35;assert q.z>-20,'Below ground';assert not cm.is_falling(),'Unexpected fall'
  if i>=len(route):finish();return
  kind,name,arg=route[i];elapsed=seconds-stage;log.write(json.dumps({'time':seconds,'step':name,'position':q.to_tuple(),'speed':speed,'cutaway':cut.get_cutaway_amount(),'relocated':cut.is_viewer_relocated()})+'\n')
  if kind=='walk':
   dx=arg[0]-q.x;dy=arg[1]-q.y;distance=math.hypot(dx,dy)
   if distance<18:inject(0,0);progress();return
   sx,sy=worldinput(dx,dy);ang=round(math.atan2(sx,sy)/(math.pi/4))*math.pi/4;mag=min(1,distance/100);inject(math.sin(ang)*mag,math.cos(ang)*mag);stuck=stuck+dt if step<.1 else 0;assert stuck<4,('Blocked',name,q)
  elif kind=='face' or kind=='hold':
   duration=.12 if kind=='face' else arg[2]
   if elapsed>=duration:inject(0,0);progress();return
   x,y=worldinput(arg[0],arg[1]);inject(x*(.2 if kind=='face' else 1),y*(.2 if kind=='face' else 1))
  elif kind=='pause':
   inject(0,0)
   if elapsed>=arg:progress()
  elif kind=='shot':
   inject(0,0)
   if elapsed>1 and not local.get('shot'):unreal.SystemLibrary.execute_console_command(w,'Shot showui filename="'+str(O/('After_'+name+'.png'))+'"',pc);local['shot']=True
   if elapsed>1.6:progress()
  elif kind=='interact':
   inject(0,0)
   if not local.get('sent') and elapsed>.3:
    local['sent']=True;assert p.try_interact(),('Interaction failed',name,q)
   if dialog.is_dialogue_active() or enc.is_encounter_active():progress({'dialog_active':dialog.is_dialogue_active(),'battle_active':enc.is_encounter_active()})
   elif elapsed>2:raise RuntimeError('Interaction produced no dialogue/battle '+name)
  elif kind=='dialog':
   inject(0,0)
   if not dialog.is_dialogue_active():progress();return
   assert p.is_overworld_input_locked();assert not pc.open_menu(unreal.PokeMonsterOverworldMenuSection.INVENTORY),'Menu opened during dialogue'
   if name=='QuestDialogue' and elapsed>.35:
    visual_actor=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor))
    assert visual_actor.is_conversing(), 'Ranger did not receive dialogue-source signal'
    anim=visual_actor.get_editor_property('visual').get_anim_instance()
    assert anim and anim.get_editor_property('conversation_alpha')>.5, 'Conversation blend not active'
    if not local.get('ranger_shot'):
     unreal.SystemLibrary.execute_console_command(w,'Shot showui filename="'+str(O/'Ranger_Conversation.png')+'"',pc);local['ranger_shot']=True
   if name in ['QuestDialogue','CompletedDialogue'] and elapsed-local.get('last_ranger_capture',0)>.3:
    count=local.get('ranger_capture_count',0);unreal.SystemLibrary.execute_console_command(w,'Shot showui filename="'+str(O/('TalkSequence_'+name+'_'+str(count).zfill(2)+'.png'))+'"',pc);local['last_ranger_capture']=elapsed;local['ranger_capture_count']=count+1
   if elapsed-local.get('lastpage',0)>1.0:dialog.advance_dialogue();local['lastpage']=elapsed
  elif kind=='battle':
   inject(0,0)
   if not enc.is_encounter_active():progress({'result':str(enc.get_last_result().outcome),'party_count':len(enc.get_player_party())});return
   assert p.is_overworld_input_locked();assert not pc.open_menu(unreal.PokeMonsterOverworldMenuSection.INVENTORY)
   pr=enc.get_presenter();view=pr.get_view()
   if not view.busy and not view.finished:
    if view.must_switch:assert pr.try_select_switch(next(j for j,m in enumerate(view.player_team) if m.can_switch))
    elif name=='WildCapture' and view.capture_enabled and local.get('attempts',0)<12:assert pr.try_select_capture();local['attempts']=local.get('attempts',0)+1
    else:assert pr.try_select_move(0)
    assert pr.resolve_selection()
   assert elapsed<160,'Battle timeout'
  elif kind=='verifytrainer':assert enc.is_trainer_defeated('Slice_Liora');progress({'trainer_defeated':True})
  elif kind=='save':
   before=[(m.current_hp,[s.current_pp for s in m.get_editor_property('move_slots')]) for m in enc.get_player_party()];assert save.save_current_game();enc.restore_defeated_trainer_ids([]);assert not enc.is_trainer_defeated('Slice_Liora');assert save.load_game();assert enc.is_trainer_defeated('Slice_Liora');after=[(m.current_hp,[s.current_pp for s in m.get_editor_property('move_slots')]) for m in enc.get_player_party()];assert before==after;progress({'save_load':True,'hp_pp_preserved':True})
  elif kind=='verifygoal':assert save.save_current_game();assert b'Slice_ArchiveSeal' in (R/'Saved/SaveGames/PokeMonster_Dev.sav').read_bytes();progress({'archive_flag':True})
  elif kind=='verifyinside':assert cut.is_viewer_relocated() and cut.get_cutaway_amount()>.999 and p.is_using_interior_movement_basis();progress({'relocation':True,'roof_front_hidden':all(a.get_editor_property('hidden') for a in cut.get_editor_property('occluding_actors'))})
  elif kind=='verifyoutside':assert not cut.is_viewer_relocated() and cut.get_cutaway_amount()<.001 and not p.is_using_interior_movement_basis();progress({'outside_restored':True})
  elif kind=='verifyheal':
   party=enc.get_player_party();assert party and all(m.current_hp==m.calculated_stats.max_hp for m in party);assert all(s.current_pp==s.max_pp for m in party for s in m.get_editor_property('move_slots') if s.get_editor_property('move'));assert save.has_save_game();assert b'VisualV2_HealingHouse' in (R/'Saved/SaveGames/PokeMonster_Dev.sav').read_bytes();progress({'hp_pp_full':True,'checkpoint_saved':True})
  elif kind=='crownoff':
   for tree in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor):
    if tree.get_actor_label().startswith(('V2_Tree_','V2_ForestOak_')):
     c=tree.static_mesh_component;crown_swaps[c]=(c.get_material(0),c.get_material(1));c.set_material(0,unreal.load_asset('/Game/Environment/WestlandAssetLibrary/Materials/MI_WLA_Bark'));c.set_material(1,unreal.load_asset('/Game/Environment/WestlandAssetLibrary/QualityV3/Materials/MI_WLA_FoliageGroups_V3'))
   progress({'temporary_original_material_comparison':True})
  elif kind=='crownrestore':
   for c,ms in crown_swaps.items():
    for j,m in enumerate(ms):c.set_material(j,m)
   crown_swaps.clear();progress({'scoped_crown_material_restored':True})
  elif kind=='menu':assert pc.open_menu(unreal.PokeMonsterOverworldMenuSection.INVENTORY);assert p.is_overworld_input_locked();assert pc.close_menu();assert not p.is_overworld_input_locked();progress({'menu_lock_release':True})
  elif kind=='directions':
   sector=min(7,int(elapsed/.5));ang=sector*math.pi/4;inject(math.sin(ang),math.cos(ang))
   if sector!=local.get('sector'):
    unreal.SystemLibrary.execute_console_command(w,'Shot showui filename="'+str(O/('Direction_'+str(sector)+'.png'))+'"',pc);local['sector']=sector
   if elapsed>4.0:inject(0,0);progress({'eight_directions':True})
 except Exception as e:finish(str(e))
assert not hasattr(unreal,'_visualv2_foot');unreal._visualv2_foot=unreal.register_slate_post_tick_callback(tick)
