"""Actual Enhanced Input walking through every new biome, with live creature/media telemetry.
No player teleports, no map saves, no save-byte restoration and no frame-rate benchmark.
"""
import unreal,json,sys,math,time,hashlib,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
REQUEST=json.loads((R/'Saved/BiomeTestV1/WalkRequest.json').read_text());D=R/'Saved/BiomeTestV1'/REQUEST['label'];assert D.is_dir()
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name().endswith('Dev_BiomeTestMap_V1')
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w)
cm=p.get_component_by_class(unreal.CharacterMovementComponent);cam=p.get_component_by_class(unreal.CameraComponent);arm=p.get_component_by_class(unreal.SpringArmComponent)
def sub(cls):return next(a for a in unreal.ObjectIterator(cls)if a.get_outer()==gi)
save=sub(unreal.PokeMonsterSaveSubsystem);enc=sub(unreal.PokeMonsterEncounterSubsystem);dialog=sub(unreal.PokeMonsterDialogueSubsystem)
inputsys=next(a for a in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if a.get_world()==w);move=next(a for a in unreal.ObjectIterator(unreal.InputAction)if a.get_outer()==p and a.get_name()=='MoveAction')
sprint=next(a for a in unreal.ObjectIterator(unreal.InputAction)if a.get_outer()==p and a.get_name()=='SprintHoldAction')
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)

habitats={h.habitat_name:h for h in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterBiomeHabitat)}
assert len(habitats)==9 and all(len(h.runtime_specimens)==len(h.specimens)for h in habitats.values()),[(k,len(h.runtime_specimens),len(h.specimens))for k,h in habitats.items()]
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest()
checks=[];result={'normal_PIE':True,'no_player_teleports':True,'hardware_controller_test':False,'checks':checks,'screenshots':[],'frames':[]};route=[];s={'i':0,'elapsed':0.,'last':p.get_actor_location(),'distance':0.,'stuck':0.,'t':0.,'last_world':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'frame_time':-100.,'telemetry_time':0.,'sprint':False,'max_speed':0.,'directions':set()};telemetry=[];phases=set();water_states={};previous={};max_step={};departures=[]
def cmd(c):unreal.SystemLibrary.execute_console_command(w,c,pc)
def inject(x,y):inputsys.inject_input_vector_for_action(move,unreal.Vector(x,y,0),[],[])
def action(name,fn,delay=.5):route.append(('action',name,fn,delay))
def walk(name,u,v):route.append(('walk',name,(u,v),0))
def wait(name,seconds):route.append(('wait',name,None,seconds))
def shot(name):route.append(('shot',name,None,1.0))
def check(name,fn):
 def test():assert fn(),name;checks.append(name)
 action(name,test)
def capture(name):
 path=D/(name+'.png');assert not path.exists();cmd('HighResShot 2560x1440 filename="'+str(path)+'"');result['screenshots'].append(str(path))
def record_frame(kind):
 if not REQUEST.get('capture_sequences',True):return
 folder=D/'Frames';folder.mkdir(exist_ok=True);path=folder/(kind+str(len(result['frames'])).zfill(4)+'.png')
 cmd('HighResShot 1280x720 filename="'+str(path)+'"');result['frames'].append({'path':str(path),'game_time':unreal.GameplayStatics.get_time_seconds(w),'kind':kind,'method':'Actual Unreal gameplay viewport, 1280x720, sparse timestamped sequence'})
check('Test GameMode uses current character and camera',lambda:p.get_class().get_name()=='PokeMonsterPlayerCharacter'and cam.field_of_view==35 and arm.target_arm_length==2850 and abs(arm.get_editor_property('relative_rotation').pitch+50)<.01)
check('Save Load Delete disabled only in sandbox',lambda:not save.save_current_game()and not save.load_game()and not save.delete_dev_save()and hashlib.sha256(slot.read_bytes()).hexdigest()==before)
check('No encounters dialogues or party instances',lambda:not enc.is_encounter_active()and not dialog.is_dialogue_active()and len(enc.get_player_party())==0)
# Ordinary movement and sprint are injected through the existing Enhanced Input action.
for i in range(8):
 a=i*math.pi/4;action('Direction '+str(i),lambda a=a:inject(math.sin(a),math.cos(a)),.1);wait('Hold direction '+str(i),.22);action('Release direction '+str(i),lambda:inject(0,0),.1)
action('Sprint action down',lambda:s.update(sprint=True))
walk('Flight clearing approach',-1200,1000);walk('Flight clearing',-1550,1300);shot('01_Wiese_Flugfeld');wait('Observe takeoff hover landing',60)
check('Existing Glurak takeoff hover landing all observed',lambda:{'Takeoff','Hover','Landing'}.issubset(phases))
walk('Meadow path',-2350,2300);walk('Meadow observation',-2700,2700);shot('02_Wiese_Waldrand');wait('Observe small meadow specimens',10)
walk('Back hub',0,0);walk('Water approach',1600,1600);walk('West shore',1900,2800);shot('03_Bach_Teich');wait('Observe real shore transitions',40)
check('Amphibious Schiggy has land and floating states',lambda:water_states.get('SchiggyUfer',set())=={'land','water'})
check('Only-water diagnostic remains in water',lambda:water_states.get('NurWasser_Diagnose',set())=={'water'})
walk('Bank path',1900,3650);walk('Bridge west',2850,4100);walk('Bridge middle',L.stream(0,4100),4100);shot('04_Bruecke');walk('Bridge east',3910,4100);walk('East bank',4420,3300);shot('05_Wasserbewohner');walk('Bridge return east',3910,4100);walk('Bridge return west',2850,4100);walk('North bank return',1900,3650);walk('West bank return',1900,2800);walk('Water junction return',1600,1600);walk('Hub return',0,0)
walk('Rock approach',-1100,-1100);walk('Ramp foot',-1200,-1800);walk('Ramp middle',-1700,-1800);walk('Plateau',-2800,-1800);shot('06_Felsplattform_3m');check('Actual plateau foot is approximately3m',lambda:abs(p.get_actor_location().z-p.get_component_by_class(unreal.CapsuleComponent).get_scaled_capsule_half_height()-300)<10)
wait('Observe plateau creature safe edge',8);walk('Ramp descent',-1700,-1800);walk('Ramp foot return',-1200,-1800);walk('Cave approach path',-1200,-2850);walk('Cave door',-2700,-2850);walk('Cave inside',-2700,-3650);shot('07_Hoehle_OffenerSchnitt');wait('Observe cave specimen',7);walk('Leave cave',-2700,-2850);walk('Cave path return',-1200,-2850);walk('Cave fork',-1200,-1800);walk('Rock junction',-1100,-1100);walk('Hub before forest',0,0)
walk('Dark forest path',1500,-1500);shot('08_DichterWald_Schweben');wait('Observe floating specimen',8);walk('Ruin approach',2800,-2800);walk('Ruin door',3000,-2800);walk('Ruin inside',3000,-3450);shot('09_AlteRuine');wait('Observe ruin specimen',8);walk('Ruin exit',3000,-2800);walk('Forest path return',1500,-1500);walk('Final hub',0,0)
action('Sprint action up',lambda:s.update(sprint=False));check('Eight directions and existing sprint speed',lambda:len(s['directions'])==8 and s['max_speed']>=314);check('No unexpected gameplay or save writes',lambda:not enc.is_encounter_active()and not dialog.is_dialogue_active()and hashlib.sha256(slot.read_bytes()).hexdigest()==before)
check('No specimen left habitat or crossed collision',lambda:not departures)
check('Every specimen demonstrated real locomotion',lambda:all(a.get_component_by_class(unreal.PokeMonsterCreatureRoamingComponent).distance_travelled>10 for h in habitats.values()for a in h.runtime_specimens))

# Optional additional observations use ordinary walking to a moving visual, with the same camera.
if REQUEST.get('details',False):
 route=route[:3]
 action('Sprint action down',lambda:s.update(sprint=True))
 walk('Rock approach',-1100,-1100);walk('Cave fork',-1200,-1800);walk('Cave path',-1200,-2850);walk('Cave door',-2700,-2850);walk('Cave observation room',-2700,-3950)
 def near(name):
  q=habitats[name].runtime_specimens[0].get_actor_location();a=p.get_actor_location();du,dv=L.local(a.x-q.x,a.y-q.y);length=math.hypot(du,dv)
  if length<1:du,dv,length=0,1,1
  u,v=L.local(q.x,q.y);return(u+du/length*200,v+dv/length*200)
 route.append(('walk','Near moving Glutexo',lambda:near('Hoehle'),0));wait('Observe Glutexo',1);shot('10_Glutexo_Hoehle_Spielkamera')
 walk('Cave exit',-2700,-2850);walk('Cave path return',-1200,-2850);walk('Cave fork return',-1200,-1800);walk('Rock path return',-1100,-1100);walk('Hub return',0,0)
 walk('Forest path',1500,-1500);route.append(('walk','Near floating Nebulak',lambda:near('Waldschweben'),0));wait('Observe Nebulak',1);shot('11_Nebulak_Wald_Spielkamera');walk('Forest return',1500,-1500);walk('Final hub',0,0)
 action('Sprint action up',lambda:s.update(sprint=False));check('No save writes or encounters',lambda:not enc.is_encounter_active()and hashlib.sha256(slot.read_bytes()).hexdigest()==before)

def sample():
 now=unreal.GameplayStatics.get_time_seconds(w)
 for name,h in habitats.items():
  for i,a in enumerate(h.runtime_specimens):
   m=a.get_component_by_class(unreal.PokeMonsterCreatureRoamingComponent);q=a.get_actor_location();id=name+str(i)
   # Root offsets are part of the existing presentation contract.
   zoffset=-h.specimens[i].species.get_visuals().presentation.ground_offset_cm if isinstance(a,unreal.PokeMonsterCreatureVisualActor)else 0
   foot=unreal.Vector(q.x,q.y,q.z-zoffset)
   if not h.contains_footprint(foot,0):departures.append({'name':id,'position':q.to_tuple()})
   if id in previous:max_step[id]=max(max_step.get(id,0),(q-previous[id]).length())
   previous[id]=q
   if isinstance(a,unreal.PokeMonsterCreatureVisualActor):
    if name=='BodennaherFlug':phases.add(a.get_ground_hover_state())
    alpha=a.aquatic_pose_alpha
   else:
    blockers=[b for b in unreal.GameplayStatics.get_all_actors_with_tag(w,'BiomePlayerWaterBarrier')]
    hit=unreal.SystemLibrary.line_trace_single(w,unreal.Vector(q.x,q.y,800),unreal.Vector(q.x,q.y,-1200),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,blockers+[a],unreal.DrawDebugTrace.NONE,True).to_tuple()
    assert hit[0]and hit[5].z<=h.water_surface_z-h.minimum_depth_cm and abs(q.z-(h.water_surface_z-h.water_draft_cm))<.1,'Only-water marker left physical water'
    alpha=1
   if name in ['SchiggyUfer','EntonUfer','NurWasser_Diagnose']:water_states.setdefault(name,set()).add('water'if alpha>.5 else'land')
   telemetry.append({'t':now,'habitat':name,'p':q.to_tuple(),'distance':m.distance_travelled,'plans':m.successful_plans,'blocked':m.blocked_steps,'rejected':m.rejected_targets,'aquatic_alpha':alpha,'suspended':h.suspended_count})

def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._biome_walk)
 inject(0,0);inputsys.inject_input_vector_for_action(sprint,unreal.Vector(0,0,0),[],[]);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle)
 result.update(passed=error is None,error=error,distance_m=s['distance']/100,completed=s['i'],total=len(route),glurak_phases=sorted(phases),media_states={k:sorted(v)for k,v in water_states.items()},departures=departures,max_observed_root_step_cm=max_step,sprint_max_speed=s['max_speed'],eight_directions=sorted(s['directions']),save_sha256=hashlib.sha256(slot.read_bytes()).hexdigest(),source_save_sha256=before)
 (D/'Result.json').write_text(json.dumps(result,indent=2));(D/'Telemetry.json').write_text(json.dumps(telemetry));unreal.log('BIOME_WALK_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);delta=now-s['last_world'];s['last_world']=now;s['t']+=delta;s['elapsed']+=delta
  assert time.monotonic()-s['wall']<900,'No forced close; inspect test'
  inputsys.inject_input_vector_for_action(sprint,unreal.Vector(1 if s['sprint']else 0,0,0),[],[]);s['max_speed']=max(s['max_speed'],cm.max_walk_speed)
  q=p.get_actor_location();step=(q-s['last']).length();s['last']=q;s['distance']+=step
  assert q.z>-100,'Player under water/floor';assert cam.field_of_view==35 and arm.target_arm_length==2850
  if now-s['telemetry_time']>.25:sample();s['telemetry_time']=now
  if s['i']>=len(route):finish();return
  kind,name,arg,duration=route[s['i']]
  if kind=='walk':
   u,v=L.local(q.x,q.y);target=arg()if callable(arg)else arg;du,dv=target[0]-u,target[1]-v;dist=math.hypot(du,dv)
   if dist<22:inject(0,0)
   else:
    a=round(math.atan2(du,dv)/(math.pi/4))*math.pi/4;mag=min(1,dist/85);inject(math.sin(a)*mag,math.cos(a)*mag);s['stuck']=s['stuck']+delta if step<.1 else 0;assert s['stuck']<5,('Path blocked',name,[u,v,q.z]);return
  elif kind=='wait':
   # Direction holds deliberately keep their injected vector until the release action.
   if name.startswith('Hold direction'):
    i=int(name.rsplit(' ',1)[1]);a=i*math.pi/4;inject(math.sin(a),math.cos(a));s['directions'].add(i)
   else:inject(0,0)
   if ('takeoff'in name or 'shore transitions'in name)and now-s['frame_time']>.65:
    record_frame('Flight'if'takeoff'in name else'Water');s['frame_time']=now
   if s['t']<duration:return
  elif kind=='shot':
   inject(0,0)
   if s['t']<duration:return
   capture(name)
  else:
   if s['t']<duration:return
   arg()
  s['i']+=1;s['t']=0;s['stuck']=0;(D/'Progress.json').write_text(json.dumps({'completed':s['i'],'total':len(route),'last':name,'distance_m':s['distance']/100}))
 except Exception:finish(traceback.format_exc())
unreal._biome_walk=unreal.register_slate_post_tick_callback(tick)
