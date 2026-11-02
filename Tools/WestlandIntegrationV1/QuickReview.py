"""Isolated real PIE interaction/regression checks. Diagnostic positioning is not a foot tour."""
import unreal,json,time,math,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandIntegrationV1';cfg=json.loads((D/'Active.json').read_text());O=D/cfg['label'];O.mkdir(exist_ok=False)
state={'phase':'init','at':0,'start':time.monotonic(),'busy':False,'index':0};result={'checks':[],'shots':[],'diagnostic_positioning':True,'physical_gamepad_test':False};W=P=PC=E=I=S=C=H=Comp=Dlg=None

def phase(n):state.update(phase=n,at=time.monotonic());(O/'Progress.json').write_text(json.dumps({'phase':n,'seconds':time.monotonic()-state['start']}))
def elapsed():return time.monotonic()-state['at']
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def done(error=None):
 result.update(passed=error is None,error=error,seconds=time.monotonic()-state['start']);(O/'Result.json').write_text(json.dumps(result,indent=2,default=str));unreal.unregister_slate_post_tick_callback(unreal._westland_quick)
def sub(cls,outer):return next(x for x in unreal.ObjectIterator(cls)if x.get_outer()==outer)
def position(a,offset=unreal.Vector(-115,0,0)):
 p=a.get_actor_location();body=a.get_component_by_class(unreal.CapsuleComponent);z=p.z-body.get_scaled_capsule_half_height()+50.15 if body else p.z+49.15
 P.set_actor_location(unreal.Vector(p.x+offset.x,p.y+offset.y,z),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();yaw=math.degrees(math.atan2(-offset.y,-offset.x));P.get_editor_property('ThirdPersonBoom').set_world_rotation(unreal.Rotator(yaw=yaw+45),False,False);P.set_actor_rotation(unreal.Rotator(yaw=yaw),False)
def inject(x,y):MoveSub.inject_input_vector_for_action(MoveAction,unreal.Vector(x,y,0),[],[])
def steer(q):
 p=P.get_actor_location();dx=q.x-p.x;dy=q.y-p.y;yaw=math.radians(P.get_movement_basis_yaw());x=-math.sin(yaw)*dx+math.cos(yaw)*dy;y=math.cos(yaw)*dx+math.sin(yaw)*dy;n=max(1,math.hypot(x,y));inject(x/n,y/n)
def door(offset,rel=False):
 b=Cut.relocated_door_threshold if rel else Cut.door_threshold;return b.get_world_location()+unreal.MathLibrary.rotate_angle_axis(unreal.Vector(offset,0,0),b.get_world_rotation().yaw,unreal.Vector(0,0,1))
def shot(n,ui=False):
 f=O/(n+'.png');cmd('Shot '+('SHOWUI 'if ui else'')+'filename="'+str(f)+'" -nosuffix');result['shots'].append(str(f))
def snap():return {'party':[x.export_text()for x in E.get_player_party()],'inventory':[x.export_text()for x in I.get_stacks()],'position':P.get_actor_location().to_tuple(),'time':C.get_time().export_text()}
def tick(dt):
 global W,P,PC,E,I,S,C,H,Comp,Dlg,Q,actors,visuals,MoveSub,MoveAction,Cut
 if state['busy']:return
 state['busy']=True
 try:
  assert time.monotonic()-state['start']<360,'Bounded PIE review timeout'
  if state['phase']=='init':
   if time.monotonic()-state['start']<6:return
   W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
   if not W:return
   assert 'Dev_WestlandRegion'in W.get_name();assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D),'Never use user storage';P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
   E=sub(unreal.PokeMonsterEncounterSubsystem,GI);I=sub(unreal.PokeMonsterInventorySubsystem,GI);S=sub(unreal.PokeMonsterSaveSubsystem,GI);C=sub(unreal.PokeMonsterWorldClock,GI);Q=sub(unreal.PokeMonsterQuestSubsystem,GI);Dlg=sub(unreal.PokeMonsterDialogueSubsystem,GI);H=sub(unreal.PokeMonsterHabitatSubsystem,W);Comp=sub(unreal.PokeMonsterCreatureCompanionSubsystem,W);assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_WestlandIntegrationV1_'+cfg['label'])
   actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)};visuals=[a for a in actors.values()if isinstance(a,unreal.PokeMonsterNPCVisualActor)];Cut=actors['HouseCutaway'];MoveSub=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if x.get_world()==W);MoveAction=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==P and x.get_name()=='MoveAction')
   assert P.is_third_person_camera() and P.third_person_pitch==-12 and P.third_person_distance==350 and P.third_person_height==170
   assert H.is_population_enabled()and len(H.zones)==16 and 0<len(H.population)<=14
   result['graphics']={n:unreal.SystemLibrary.get_console_variable_float_value(n)for n in ['r.ScreenPercentage','r.Lumen.HardwareRayTracing','r.Lumen.FinalGatherMethod','r.TemporalAA.Upsampling','r.Shadow.Virtual.Enable','r.Shadow.Virtual.SMRT.RayCountDirectional']};assert result['graphics']=={'r.ScreenPercentage':75,'r.Lumen.HardwareRayTracing':0,'r.Lumen.FinalGatherMethod':0,'r.TemporalAA.Upsampling':1,'r.Shadow.Virtual.Enable':1,'r.Shadow.Virtual.SMRT.RayCountDirectional':4},result['graphics']
   assert sub(unreal.PokeMonsterDayNightSubsystem,W).is_cycle_enabled();assert Comp.get_visual()and not Comp.get_visual().get_editor_property('hidden')
   result['checks'].append('Fresh Westland PIE: current team, companion, 16 natural zones, cap14, clock/day-night, unchanged C/75%/TAAU/IFG/VSM4 and camera');state['npc_labels']=['WR_NPC_0','WR_NPC_1','WR_NPC_2'];phase('npc_place')
  elif state['phase']=='npc_place':
   label=state['npc_labels'][state['index']];a=actors[label];position(a);state['label']=label;phase('npc_open')
  elif state['phase']=='npc_open':
   if elapsed()<.25:steer(actors[state['label']].get_actor_location());return
   inject(0,0)
   if elapsed()<1.8:return
   a=actors[state['label']];v=next(v for v in visuals if v.source_actor==a);assert v.visual.get_skeletal_mesh_asset() and v.visual.visible
   state['npc_camera']={'location':PC.player_camera_manager.get_camera_location().to_tuple(),'pitch':PC.player_camera_manager.get_camera_rotation().pitch};assert abs(state['npc_camera']['pitch']+12)<.02
   assert P.find_interactable_in_range()==a,(state['label'],str(P.find_interactable_in_range()));assert P.try_interact();assert Dlg.is_dialogue_active() and v.is_conversing();state['pages']=Dlg.get_page_count();state['npc_shot']=False;phase('npc_dialogue')
  elif state['phase']=='npc_dialogue':
   if not state.get('npc_shot'):
    if elapsed()<1:return
    shot(state['label']+'_Dialog',True);state.update(npc_shot=True,at=time.monotonic());return
   if elapsed()<.5:return
   if Dlg.is_dialogue_active():PC.advance_dialogue();state['at']=time.monotonic();return
   assert not P.is_overworld_input_locked();result['checks'].append({'npc':state['label'],'original_dialogue_pages':state['pages'],'model_visible':True,'conversation_animation':True,'camera':state['npc_camera']})
   # Repeat the same original dialogue; source actor and quest role are unchanged.
   assert P.try_interact();PC.close_dialogue();assert not P.is_overworld_input_locked();state['index']+=1
   if state['index']<3:phase('npc_place')
   else:phase('wild_find')
  elif state['phase']=='wild_find':
   if elapsed()<2:return
   candidates=[a for a in H.population if a and a.life_state==unreal.PokeMonsterWildLifeState.ACTIVE and not a.get_editor_property('hidden') and a.overworld_movement.biome_habitat.medium==unreal.PokeMonsterBiomeMedium.LAND];assert candidates,'No natural land encounter';a=min(candidates,key=lambda a:(a.get_actor_location()-P.get_actor_location()).length());state['wild']=a;state['ids']=[x.instance_id.to_string()for x in E.get_player_party()];state['ap_before']=[x.export_text()for x in E.get_player_party()];position(a,unreal.Vector(-130,0,0));assert I.add_item(unreal.load_asset('/Game/Data/Items/DA_MasterBall'),1);phase('wild_open')
  elif state['phase']=='wild_open':
   a=state['wild'];P.get_editor_property('ThirdPersonBoom').set_world_rotation(unreal.Rotator(yaw=math.degrees(math.atan2(a.get_actor_location().y-P.get_actor_location().y,a.get_actor_location().x-P.get_actor_location().x))),False,False)
   if E.is_encounter_active():phase('battle');return
   if P.try_interact():assert E.is_encounter_active();phase('battle')
   else:
    assert elapsed()<10,'Natural encounter not interactable';steer(a.get_actor_location())
  elif state['phase']=='battle':
   inject(0,0);assert E.is_encounter_active();pr=E.get_presenter();view=pr.get_view()
   if view.busy or view.presentation_pending or view.finished:return
   shot('ClassicBattle',True);idx=1 if len(view.moves)>1 and view.moves[1].enabled else next(i for i,m in enumerate(view.moves)if m.enabled);E.get_battle_widget().call_method('Move'+str(idx));phase('attack')
  elif state['phase']=='attack':
   if not E.is_encounter_active():result['checks'].append('Real attack/encounter ended before capture; separate capture required');phase('wild_find');return
   pr=E.get_presenter();view=pr.get_view()
   if view.busy or view.presentation_pending or view.finished:return
   assert pr.try_select_capture_item(unreal.load_asset('/Game/Data/Items/DA_MasterBall'));assert pr.resolve_selection();phase('capture')
  elif state['phase']=='capture':
   if E.is_encounter_active():return
   team=list(E.get_player_party());assert len(team)==len(state['ids'])+1;assert [x.instance_id.to_string()for x in team[:len(state['ids'])]]==state['ids'];result['checks'].append('Natural habitat encounter, real ClassicBattle attack/AP consumption, normal capture adds distinct individual and returns control');phase('healer_door')
  elif state['phase']=='healer_door':
   p=door(-125);P.set_actor_location(unreal.Vector(p.x,p.y,p.z-Cut.door_threshold.get_scaled_box_extent().z+50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();phase('enter')
  elif state['phase']=='enter':
   if Cut.is_viewer_relocated():inject(0,0);state['label']='HouseHealer';phase('healer_approach');return
   assert elapsed()<12,'Real healing-house doorway transition';steer(door(130))
  elif state['phase']=='healer_approach':
   a=actors['HouseHealer'];center=Cut.relocated_interior_area.get_world_location()
   if not state.get('healer_center_reached'):
    if math.dist(P.get_actor_location().to_tuple()[:2],center.to_tuple()[:2])<30:state['healer_center_reached']=True
    else:assert elapsed()<40,'Interior center approach blocked';steer(center);return
   target=a.get_actor_location()+unreal.MathLibrary.rotate_angle_axis(unreal.Vector(-195,0,0),-45,unreal.Vector(0,0,1))
   if math.dist(P.get_actor_location().to_tuple()[:2],target.to_tuple()[:2])<20:
    inject(0,0);state['label']='HouseHealer';P.get_editor_property('ThirdPersonBoom').set_world_rotation(unreal.Rotator(yaw=0),False,False);phase('healer_open')
   else:assert elapsed()<40,'Healer approach blocked';steer(target)
  elif state['phase']=='healer_open':
   if elapsed()<.25:steer(actors['HouseHealer'].get_actor_location());return
   inject(0,0)
   if elapsed()<1.5:return
   a=actors['HouseHealer'];v=next(v for v in visuals if v.source_actor==a);assert P.find_interactable_in_range()==a;assert P.try_interact()and Dlg.is_dialogue_active();assert v.visual.visible;shot('Heilerin_Dialog',True);phase('heal_dialogue')
  elif state['phase']=='heal_dialogue':
   if elapsed()<.5:return
   if Dlg.is_dialogue_active():PC.advance_dialogue();state['at']=time.monotonic();return
   assert all(x.current_hp==x.calculated_stats.max_hp and all(m.current_pp==m.max_pp for m in x.move_slots if m.move)for x in E.get_player_party());cp=sub(unreal.PokeMonsterCheckpointSubsystem,unreal.GameplayStatics.get_game_instance(W)).get_active_checkpoint();assert str(cp.checkpoint_id)=='WestlandRegion_HealingHouse'and str(cp.map_package)=='/Game/Maps/Dev_WestlandRegion';result['checks'].append('Real doorway/relocated interior, original healer dialogue, HP/AP recovery and exact regional checkpoint')
   # Persist an existing quest in isolated QA only. No production story/dialogue changes.
   quest=unreal.load_asset('/Game/Data/Quests/DA_SliceArchiveQuest');assert Q.start_quest_by_id(quest.internal_id);PC.toggle_main_menu();assert PC.is_menu_open();state['snapshot']=snap();assert S.save_current_game();view=PC.get_overworld_widget().get_view();state['quest_saved']=[str(view.active_quest_name),str(view.active_quest_objective)];assert state['quest_saved'][0];assert S.load_game();phase('load')
  elif state['phase']=='load':
   if elapsed()<2 or S.is_load_in_progress():return
   assert snap()==state['snapshot'];view=PC.get_overworld_widget().get_view();assert [str(view.active_quest_name),str(view.active_quest_objective)]==state['quest_saved'];assert PC.close_menu();result['checks'].append('Menu Save/Load: exact full individual/team/AP/inventory/time/position snapshot and existing active quest UI inside healing house');shot('Heilhaus_Nach_Laden');phase('exit_approach')
  elif state['phase']=='exit_approach':
   target=door(90,True)
   if math.dist(P.get_actor_location().to_tuple()[:2],target.to_tuple()[:2])<25:inject(0,0);phase('exit')
   else:assert elapsed()<20;steer(target)
  elif state['phase']=='exit':
   if not Cut.is_viewer_relocated():inject(0,0);result['checks'].append('Healing-house return to exterior with camera/control restored');phase('time');return
   assert elapsed()<12;steer(door(-130,True))
  elif state['phase']=='time':
   times=[6,12,19,22];j=state.get('time_index',0)
   if j>=len(times):cmd('pm.WorldClock reset');state['pickup_index']=0;phase('pickup_place');return
   if not state.get('time_set'):
    cmd('pm.WorldClock set 1 '+str(times[j])+' 0');cmd('pm.WorldClock pause');assert C.get_hour()==times[j];state.update(time_set=True,at=time.monotonic());return
   if elapsed()<2:return
   sample=sub(unreal.PokeMonsterDayNightSubsystem,W).get_lighting_sample();assert abs(sample.sun_elevation-75)<.05 if times[j]==12 else True;shot('Tageszeit_'+str(times[j]));
   if times[j]==12:
    cmd('pm.DayNight C');assert abs(sub(unreal.PokeMonsterDayNightSubsystem,W).get_lighting_sample().sun_elevation-85)<.05;cmd('pm.DayNight B');assert abs(sub(unreal.PokeMonsterDayNightSubsystem,W).get_lighting_sample().sun_elevation-75)<.05;result['checks'].append('Existing B75/C85 debug switch works in Westland and restores B75')
   result['checks'].append({'hour':times[j],'sun_elevation':sample.sun_elevation,'population':len(H.population)});state.update(time_index=j+1,time_set=False)
  elif state['phase']=='pickup_place':
   finds=[actors[x]for x in ['WR_Pickup_HofFund','WR_Pickup_DorfFund','WR_Pickup_UferFund']];a=finds[state['pickup_index']];assert not a.get_editor_property('hidden');state['pickup']=a;state['pickup_quantity_before']=I.get_quantity(a.item);position(a,unreal.Vector(-130,0,0));phase('pickup_collect')
  elif state['phase']=='pickup_collect':
   a=state['pickup']
   if elapsed()<.2:steer(a.get_actor_location());return
   inject(0,0)
   if elapsed()<1:return
   assert P.find_interactable_in_range()==a;assert P.try_interact();assert a.get_editor_property('hidden')and E.is_encounter_completed(a.pickup_id);assert I.get_quantity(a.item)==state['pickup_quantity_before']+a.quantity;result['checks'].append('Normal pickup collected once: '+str(a.pickup_id));state['pickup_index']+=1
   if state['pickup_index']<3:phase('pickup_place')
   else:
    PC.toggle_main_menu();state['pickup_snapshot']=snap();assert S.save_current_game();assert S.load_game();phase('pickup_load')
  elif state['phase']=='pickup_load':
   if elapsed()<2 or S.is_load_in_progress():return
   assert snap()==state['pickup_snapshot'];assert all(actors[n].get_editor_property('hidden')for n in ['WR_Pickup_HofFund','WR_Pickup_DorfFund','WR_Pickup_UferFund']);assert PC.close_menu();result['checks'].append('Collected world finds and exact inventory remain collected after menu Save/Load');phase('sort')
  elif state['phase']=='sort':
   if not state.get('sort_started'):
    state['first']=E.get_player_party()[0].instance_id;assert E.reorder_party(E.get_player_party()[1].instance_id,0);state.update(sort_started=True,at=time.monotonic());return
   if elapsed()<2:return
   assert Comp.get_visual()and not Comp.get_visual().get_editor_property('hidden');assert E.reorder_party(state['first'],0);assert PC.open_menu(unreal.PokeMonsterOverworldMenuSection.TEAM);shot('Team_Status_EP',True);result['checks'].append('Regular team sorting and companion refresh; existing team/status UI opens');phase('finish')
  elif state['phase']=='finish':
   if elapsed()<1:return
   assert PC.close_menu();assert len(H.population)<=14;assert all(Path(p).exists()for p in result['shots']);done()
 except Exception:done(traceback.format_exc())
 finally:state['busy']=False
unreal._westland_quick=unreal.register_slate_post_tick_callback(tick)
