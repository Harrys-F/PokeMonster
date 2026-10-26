"""Reuse existing CSV/GPU profiler, QHD High, three repeats per fixed site."""
import unreal,json,gc
from pathlib import Path
gc.collect();R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/DayNightV1';q=json.loads((D/'PerformanceRequest.json').read_text());W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();PC=unreal.GameplayStatics.get_player_controller(W,0)
# VGB1_ prefix selects stock scalability, not the old performance candidate.
label='VGB1_DayNight_'+q['label'];plan=D/(label+'.tsv');assert not plan.exists();rows=[label+'\tPIE\t3\t5']
for rep in [1,2,3]:
 for site in ['Dorf','Wald']:rows.append(site+'\tControl\t'+str(rep)+'\t2560\t1440\t2\t100')
plan.write_text('\n'.join(rows)+'\n');unreal.SystemLibrary.execute_console_command(W,'pm.EnvPerf2.Run '+str(plan),PC)
