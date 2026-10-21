"""Explicit PIE-only ten-species showroom; no persistent map, save, party or habitat writes.
Write Saved/CreaturePolishV4/ShowcaseRequest.json {label, seconds, focus, yaw} then ArtControl script.
Uses actual movement and the native animation instance, never SingleNode skinning.
"""
import unreal,json,time,math,hashlib,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/CreaturePolishV4';q=json.loads((O/'ShowcaseRequest.json').read_text());label=q['label'];assert label.isalnum();D=O/label;D.mkdir(exist_ok=False)
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_game_world();assert w and 'Dev_TestMap_VisualV2' in w.get_name();p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w);enc=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi);assert not enc.is_encounter_active() and not p.is_overworld_input_locked();assert not hasattr(unreal,'_polish_showcase');comp=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==w)
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';save=hashlib.sha256(slot.read_bytes()).hexdigest();original=p.get_actor_transform();p.set_overworld_input_locked(True);center=unreal.Vector(-5200,-2300,0);right=unreal.Vector(.70710678,.70710678,0);forward=unreal.Vector(.70710678,-.70710678,0)
actors=[];bases=[];profiles={};names=['Zunderlauf','Schiggy','Bisasam','Pikachu','Myrapla','Enton','Gengar','Nebulak','Machomei','Glurak'];focus=q.get('focus');rows=[]
floor=unreal.PokeMonsterCreaturePolishLibrary.spawn_review_actor(w,True,center+unreal.Vector(0,0,-10));floor.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE);floor.static_mesh_component.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'));floor.set_actor_scale3d(unreal.Vector(46,46,.2));floor.static_mesh_component.set_material(0,unreal.load_asset('/Game/Environment/HealingHouse/ArtV5/Materials/M_HH5_LandscapeGround'));floor.set_actor_enable_collision(False);actors.append(floor)
for i,name in enumerate(names):
 s=unreal.load_asset('/Game/Data/Creatures/DA_'+name);profiles[name]=unreal.load_asset(q['profiles'][name]) if name in q.get('profiles',{}) else s.visuals.presentation;base=center+right*((i%4-1.5)*400)+forward*((i//4-1)*440)
 v=unreal.PokeMonsterCreaturePolishLibrary.spawn_review_actor(w,False,base);assert v.set_species(s);
 if name in q.get('profiles',{}):assert v.set_presentation(unreal.load_asset(q['profiles'][name]))
 v.idle_phase_offset=i*.173;v.set_actor_rotation(unreal.Rotator(pitch=0,yaw=float(q.get('yaw',135)),roll=0),True);base.z-=profiles[name].ground_offset_cm;v.set_actor_location(base,False,True);actors.append(v);bases.append((name,v,base));rows.append(dict(species=name,profile=profiles[name].get_path_name(),height=profiles[name].reference_size_cm,position=base.to_tuple(),rotation=v.get_actor_rotation().to_tuple(),walk=profiles[name].walk_speed,run=profiles[name].run_speed))
target=next((b for n,v,b in bases if n==focus),center);p.set_actor_location(target+unreal.Vector(0,0,70),False,True);p.set_actor_hidden_in_game(True)
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
def cmd(t):unreal.SystemLibrary.execute_console_command(w,t,pc)
cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');state=dict(last=unreal.GameplayStatics.get_time_seconds(w),t=0.,wall=time.monotonic(),shots=[],profiles=rows,fixture='Explicit native-animation visual showroom, not natural gameplay evidence. No assets/maps/saves/party changed.',world=w.get_path_name())
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._polish_showcase);delattr(unreal,'_polish_showcase');
 for a in actors:
  if unreal.SystemLibrary.is_valid(a):a.destroy_actor()
 p.set_actor_transform(original,False,True);p.set_actor_hidden_in_game(False);p.set_overworld_input_locked(False);settings.set_editor_property('bThrottleCPUWhenNotForeground',old)
 state.update(passed=error is None,error=error,save_unchanged=hashlib.sha256(slot.read_bytes()).hexdigest()==save);(D/'Result.json').write_text(json.dumps(state,indent=2));unreal.log('POLISH_SHOWCASE_DONE '+label+' '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);delta=now-state['last'];state['last']=now;state['t']+=delta;t=state['t'];assert time.monotonic()-state['wall']<240
  if comp.get_visual():comp.get_visual().set_actor_hidden_in_game(True)
  # Idle 10 s; eight straight directions with measured native walk/run and smooth stop intervals.
  if q.get('mode')=='reactions' and t>=10:
   index=min(3,int((t-10)//3));roles=['ATTACK','HIT','FAINT','HAPPY']
   if state.get('reaction_index')!=index:
    for name,v,base in bases:assert v.set_presentation(profiles[name]);assert v.play_reaction(getattr(unreal.PokeMonsterCreatureClip,roles[index]))
    state['reaction_index']=index
  elif q.get('mode')!='reactions' and t>=10:
   block=int((t-10)//5);part=(t-10)%5;angle=block%8*math.pi/4;run=block>=8
   for name,v,base in bases:
    speed=profiles[name].run_speed if run else profiles[name].walk_speed
    if part<3:
     v.set_actor_rotation(unreal.Rotator(pitch=0,yaw=math.degrees(angle),roll=0),True);v.add_actor_world_offset(unreal.Vector(math.cos(angle),math.sin(angle),0)*speed*delta,False,True)
    elif part<3+delta:v.play_reaction(unreal.PokeMonsterCreatureClip.ATTACK)
    elif part>4.8:v.set_actor_location(base,False,True) # Explicit between-take reset, never presented as normal locomotion.
  for stamp in q.get('stamps',[4,7,10,12,17,22,27,32,37,42,47,52,57,62,67,72,77,82,87]):
   if t>=stamp and stamp not in state['shots']:
    assert pc.get_viewport_size()==(2560,1440);cmd('Shot filename='+str(D/('Frame'+str(stamp)+'_QHD.png')));state['shots'].append(stamp);state.setdefault('capture_times',[]).append(dict(requested=stamp,actual=t));break
  if t>q.get('seconds',92):finish()
 except Exception:finish(traceback.format_exc())
unreal._polish_showcase=unreal.register_slate_post_tick_callback(tick)
