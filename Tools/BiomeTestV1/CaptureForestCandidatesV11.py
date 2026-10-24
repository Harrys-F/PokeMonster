"""Matched actual QHD camera-only candidates, not a gameplay walk. Restores the original arm and player."""
import unreal,json,time,sys,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
req=json.loads((R/'Saved/BiomeTestV11/ForestCandidatesRequest.json').read_text());O=R/'Saved/BiomeTestV11'/req['label'];O.mkdir(exist_ok=False)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name().endswith('Dev_BiomeTestMap_V1');p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);arm=p.get_component_by_class(unreal.SpringArmComponent);original_arm=arm.target_arm_length;original=p.get_actor_location();assert original_arm==2850
zones=list(unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterForestCameraZone))if hasattr(unreal,'PokeMonsterForestCameraZone')else[];zone_states=[z.get_editor_property('bEnabled')for z in zones]
for z in zones:z.set_editor_property('bEnabled',False)
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
positions=[('DensePath',3200,-1800),('CanopyEdge',2500,-1800)];variants=[('A_OriginalSight',2850),('B_Closer1700',1700),('C_Closer1200',1200)];cases=[(pos,variant)for pos in positions for variant in variants];s={'i':0,'stage':'move','last':unreal.GameplayStatics.get_time_seconds(w),'time':0.,'wall':time.monotonic(),'rows':[]}
def cmd(c):unreal.SystemLibrary.execute_console_command(w,c,pc)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._biome_forest_candidates);arm.target_arm_length=original_arm;p.set_actor_location(original,False,True);settings.set_editor_property('bThrottleCPUWhenNotForeground',old)
 for z,enabled in zip(zones,zone_states):z.set_editor_property('bEnabled',enabled)
 (O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'fixture':'Matched real game photographs, player-only positioning and transient arm-distance variants; no tree/material/light edits, not a footwalk','rows':s['rows']},indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['time']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<180
  if s['i']>=len(cases):finish();return
  (name,u,v),(variant,distance)=cases[s['i']]
  if s['stage']=='move':
   p.set_actor_location(unreal.Vector(*L.world(u,v,L.height(u,v)+p.get_component_by_class(unreal.CapsuleComponent).get_scaled_capsule_half_height()+2)),False,True);p.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();arm.target_arm_length=distance;s.update(stage='shot',time=0.);return
  if s['time']<2:return
  path=O/(name+'_'+variant+'_QHD.png');cmd('HighResShot 2560x1440 filename="'+str(path)+'"');s['rows'].append({'name':name,'variant':variant,'player':p.get_actor_location().to_tuple(),'arm_cm':arm.target_arm_length,'camera':pc.player_camera_manager.get_camera_location().to_tuple(),'rotation':pc.player_camera_manager.get_camera_rotation().to_tuple(),'path':str(path.relative_to(R))});s.update(i=s['i']+1,stage='move',time=0.)
 except Exception:finish(traceback.format_exc())
cmd('r.ScreenPercentage 100');cmd('DisableAllScreenMessages 1');unreal._biome_forest_candidates=unreal.register_slate_post_tick_callback(tick)
