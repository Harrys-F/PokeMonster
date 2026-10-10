"""Real Enhanced Input foot inspection, camera/player invariants and gameplay HUD locks."""
import unreal,json,math,time
from pathlib import Path
R=Path(unreal.Paths.project_dir());O=R/'Saved/WestlandAssetLibrary';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and 'Dev_WestlandAssetLibrary' in w.get_name();p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);move=p.get_component_by_class(unreal.CharacterMovementComponent);boom=p.get_component_by_class(unreal.SpringArmComponent);camera=p.get_component_by_class(unreal.CameraComponent)
assert move.max_walk_speed==210 and boom.target_arm_length==2500 and camera.field_of_view==35
sub=next(s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if s.get_world()==w);act=next(a for a in unreal.ObjectIterator(unreal.InputAction) if a.get_outer()==p and a.get_name()=='MoveAction')
full=(R/'Art/World/WestlandAssetLibrary/Assets.json').exists();name='Full' if full else 'Hero';rt=[]
def walk(label,e,n):rt.append(('walk',label,(e,n)))
def shot(label):rt.append(('shot',label,None))
walk('Vegetation',-12,1);shot('Vegetation');walk('YoungOak',-2,18.5);shot('YoungOak');walk('OldOak',-10,21);shot('OldOak');walk('Return',-10,6);walk('Stones',-1,-2);shot('Landscape');walk('Village',10,-2);shot('Village')
if full:
 walk('VillageClear',10,-4);walk('CartApproach',19,-4);walk('Cart',19,1);shot('Cart');walk('FarmApproach',19,7);walk('Farm',15,7);shot('Farm');walk('Fruit',11,13.5);shot('FruitTree');walk('Birch',4,20);shot('Birch');walk('RuinsApproach',7,13);walk('Ruins',10,14);shot('Ruins')
else:walk('VillageClear',7,-2);walk('RuinsApproach',7,14);walk('Ruins',10,14);shot('Ruins')
walk('ReturnNorth',4,14);walk('Return',4,5);walk('ReturnSouth',6,-4);walk('OpenGround',3,-9);shot('PlayerOpenGround');walk('Start',-14,-9);rt.append(('menu','HUD_menu',None))
custom=json.loads((O/'FootViewJob.json').read_text()) if (O/'FootViewJob.json').exists() else None
if custom:
 name=custom['name'];rt=[('walk',x[0],(x[1],x[2])) for x in custom['points']]
i=0;pause=0;distance=0;last=p.get_actor_location();game=0;wall=time.monotonic();stuck=0;data={'mode':name,'checks':[],'screenshots':[],'no_test_teleports':True,'camera':[2500,-55,-45,35],'movement_cm_s':210}
def inject(x,y):sub.inject_input_vector_for_action(act,unreal.Vector(x,y,0),[],[])
def finish(error=None):
 inject(0,0);unreal.unregister_slate_post_tick_callback(unreal._wla_walk);del unreal._wla_walk;data.update({'passed':error is None,'error':error,'distance_m':distance/100,'seconds':game,'wall_seconds':time.monotonic()-wall});(O/(name+'FootTest.json')).write_text(json.dumps(data,indent=2)+'\n');unreal.log('WLA_FOOT_TEST_DONE '+str(error))
def tick(dt):
 global i,pause,distance,last,game,stuck
 try:
  game+=dt;q=p.get_actor_location();step=(q-last).length();distance+=step;last=q
  assert q.z>40,'Fell below ground';assert move.max_walk_speed==210
  if i>=len(rt):finish();return
  kind,label,target=rt[i]
  if kind=='walk':
   e=(q.x+q.y)/math.sqrt(2)/100;n=(q.x-q.y)/math.sqrt(2)/100;dx=target[0]-e;dy=target[1]-n
   if math.hypot(dx,dy)<.40:inject(0,0);data['checks'].append({'point':label,'E_N_m':[e,n],'grounded':not move.is_falling()});i+=1;stuck=0;return
   a=round(math.atan2(dy,dx)/(math.pi/4))*(math.pi/4);inject(math.cos(a),math.sin(a));stuck=stuck+dt if step<.2 else 0;assert stuck<5,('Movement blocked',label,e,n)
  elif kind=='shot':
   inject(0,0)
   if not pause:pause=game+1.7;path=O/('PIE_'+name+'_'+label+'.png');unreal.AutomationLibrary.take_high_res_screenshot(1280,720,str(path),delay=.5);data['screenshots'].append(str(path))
   if game>=pause:i+=1;pause=0
  else:
   inject(0,0);assert pc.open_menu(unreal.PokeMonsterOverworldMenuSection.INVENTORY);assert p.is_overworld_input_locked();assert pc.close_menu();assert not p.is_overworld_input_locked();data['checks'].append({'menu_locks_and_returns_control':True});i+=1
 except Exception as error:finish(str(error))
assert not hasattr(unreal,'_wla_walk');unreal._wla_walk=unreal.register_slate_post_tick_callback(tick)
