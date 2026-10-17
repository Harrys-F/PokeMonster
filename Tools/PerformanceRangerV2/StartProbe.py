import unreal,json,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();P=R/'Art/Characters/NPCs/Ranger/Review/V2';req=json.loads((P/'Request.json').read_text());w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
r=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor));r.visual.set_skeletal_mesh_asset(unreal.load_asset('/Game/Characters/NPCs/Ranger/Meshes/SK_Ranger_NPC_V1'));r.visual.set_forced_lod(0)
plan=R/'Tools/PerformanceRangerV2/Plans'/(req['plan']+'.tsv');assert plan.is_file();unreal.SystemLibrary.execute_console_command(w,'pm.Perf.Run '+str(plan))
if req.get('shot'):
 start=time.monotonic()
 def capture(dt):
  if time.monotonic()-start<2:return
  unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(P/(req['plan']+'_ResolutionProof.png'))+'"');unreal.unregister_slate_post_tick_callback(unreal._rv2_shot);del unreal._rv2_shot
 unreal._rv2_shot=unreal.register_slate_post_tick_callback(capture)
