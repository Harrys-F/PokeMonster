"""PIE-only preview of the six existing regions, reusing NPCGround's RAM save guard.
Console: py exec(open(r"/Users/harry/Developer/PokeMonster/Tools/VisualV2FabAssetTrialV1/Visit.py").read(), {"AREA":"Blumenwiese"})
Use AREA="Zurueck" before ending the preview. No production console/C++ changes.
"""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();ed=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=ed.get_game_world()if ed else None;assert W and 'Dev_TestMap_VisualV2'in W.get_name(),'Only an ordinary VisualV2 PIE session';P=unreal.GameplayStatics.get_player_pawn(W,0);assert P.is_third_person_camera(),'Use pm.Camera ThirdPerson first';G=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterNPCTestGround)if x.get_outer()==W);area=globals().get('AREA','Blumenwiese')
if area=='Zurueck':
 assert G.return_to_world(),'No active preview, or current gameplay prevents return'
 if hasattr(unreal,'_fat_preview_boom_rotation'):P.third_person_boom.set_world_rotation(unreal._fat_preview_boom_rotation,False,False);del unreal._fat_preview_boom_rotation
else:
 sites={x[0]:x[1:]for x in json.loads((R/'Tools/VisualV2FabAssetTrialV1/Sites.json').read_text())};sites.update(Kraeutergarten=[-4900,-400,55],Bachbett=[-100,-500,90],Felsgruppe=[-1700,1200,35]);assert area in sites,sorted(sites);old=P.third_person_boom.get_world_rotation();assert G.visit(0),'Preview requires a safe, unlocked gameplay state'
 if not hasattr(unreal,'_fat_preview_boom_rotation'):unreal._fat_preview_boom_rotation=old
 x,y,yaw=sites[area];P.set_actor_location(unreal.Vector(x,y,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();P.third_person_boom.set_world_rotation(unreal.Rotator(yaw=yaw),False,False)
unreal.log('Fab-Testbereich: '+area+'; Vorschau nutzt den vorhandenen RAM-Speicherschutz.')
