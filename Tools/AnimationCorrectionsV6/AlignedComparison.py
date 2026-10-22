"""Controlled old/current A/B on native test specimens, same camera in each pair.
Both variants are real retained Unreal assets. PIE-only presentation swaps, no saved asset changes.
"""
import unreal,json,time,traceback,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/AnimationCorrectionsV6/AlignedAB07';D.mkdir(exist_ok=False);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w;g=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureTestGround)if x.get_outer()==w);assert g.visit(0);assert g.set_mode('idle');p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);mesh=p.get_component_by_class(unreal.PokeMonsterMeshyVisualComponent);current_clips={r:mesh.get_editor_property(r+'_animation')for r in ['idle','walk','run']};save=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(save.read_bytes()).hexdigest();actions=[];shots=[];index=0;due=0;started=time.monotonic();pairs=[]
def cmd(s):unreal.SystemLibrary.execute_console_command(w,s,pc)
def action(name,fn,delay=1.):actions.append((name,fn,delay))
def shot(name):
 assert pc.get_viewport_size()==(2560,1440);cam=pc.player_camera_manager;cmd('Shot filename='+str(D/(name+'.png')));shots.append(dict(name=name,file=name+'00000.png',camera=cam.get_camera_location().to_tuple(),rotation=cam.get_camera_rotation().to_tuple(),player=p.get_actor_location().to_tuple()))
action('qhd',lambda:cmd('pm.EnvPerf2.Viewport 2560 1440'),2);action('percentage',lambda:cmd('r.ScreenPercentage 100'))
old={'Glurak':'MotionV5/DA_Glurak_Presentation','Nebulak':'MotionV5/DA_Nebulak_Presentation','Machomei':'MeshyV1/DA_Machomei_Presentation','Myrapla':'MeshyV1/DA_Myrapla_Presentation'}
for i,n in [(10,'Glurak'),(8,'Nebulak'),(7,'Machomei'),(5,'Myrapla')]:
 v=g.specimens[i-1];current=unreal.load_asset('/Game/Characters/Creatures/'+n+'/AnimationV6/DA_'+n+'_Presentation_V6');original=unreal.load_asset('/Game/Characters/Creatures/'+n+'/'+old[n]);assert current and original
 def place(i=i,v=v):
  v.set_actor_rotation(unreal.Rotator(pitch=0,yaw=315 if i==10 else 135,roll=0),False);assert g.visit(i)
 action(n+' position',place,2);action(n+' old',lambda v=v,original=original:v.set_presentation(original),1.5);action(n+' before',lambda n=n:shot(n+'Before'),.5);action(n+' new',lambda v=v,current=current:v.set_presentation(current),1.5);action(n+' after',lambda n=n:shot(n+'After'),.5);pairs.append((n+'Before',n+'After'))
action('player position',lambda:g.visit(0),2)
def clips(old):
 for r in ['idle','walk','run']:
  a=unreal.load_asset('/Game/Characters/YoungTrainer/MotionV3/A_Player_'+r.title()+'_V3')if old else current_clips[r];mesh.set_editor_property(r+'_animation',a)
action('old player',lambda:clips(True),1.5);action('player before',lambda:shot('PlayerBefore'),.5);action('new player',lambda:clips(False),1.5);action('player after',lambda:shot('PlayerAfter'),.5);pairs.append(('PlayerBefore','PlayerAfter'))
def finish(error=None):
 clips(False);cmd('pm.EnvPerf2.Viewport 0 0');unreal.unregister_slate_post_tick_callback(unreal._v6_aligned);delattr(unreal,'_v6_aligned');comparison=[]
 for a,b in pairs:
  aa=next((s for s in shots if s['name']==a),None);bb=next((s for s in shots if s['name']==b),None)
  if aa and bb:comparison.append(dict(before=a,after=b,camera_delta_cm=sum((x-y)**2 for x,y in zip(aa['camera'],bb['camera']))**.5,rotation_delta=sum((x-y)**2 for x,y in zip(aa['rotation'],bb['rotation']))**.5))
 (D/'Result.json').write_text(json.dumps(dict(passed=error is None,error=error,shots=shots,pairs=comparison,save_unchanged=hashlib.sha256(save.read_bytes()).hexdigest()==before,scope='Controlled retained-old/current Unreal assets in same ordinary PIE on native test ground; no model spawning or authored map changes'),indent=2))
def tick(dt):
 global index,due
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);assert time.monotonic()-started<160
  if now<due:return
  if index==len(actions):finish();return
  n,fn,d=actions[index];fn();index+=1;due=now+d
 except Exception:finish(traceback.format_exc())
unreal._v6_aligned=unreal.register_slate_post_tick_callback(tick)
