import unreal,json
from pathlib import Path
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0)
r={'menu':PC.is_menu_open(),'unreal_pause':unreal.GameplayStatics.is_game_paused(W),'world':W.get_name(),'has_begun':W.has_begun_play()if hasattr(W,'has_begun_play')else None}
for cls,methods in [(unreal.PokeMonsterWorldClock,['is_clock_paused','get_debug_speed']),(unreal.PokeMonsterEncounterSubsystem,['is_encounter_active']),(unreal.PokeMonsterDialogueSubsystem,['is_dialogue_active']),(unreal.PokeMonsterSaveSubsystem,['is_load_in_progress','is_pie_memory_preview_active']),(unreal.PokeMonsterCheckpointSubsystem,['is_returning_from_defeat'])]:
 obj=next(x for x in unreal.ObjectIterator(cls)if x.get_outer()==GI)
 for name in methods:
  try:r[name]=str(getattr(obj,name)())
  except Exception as e:r[name]=str(e)
for name in ['EvolutionWidget','OverworldWidget','bMenuOpen']:
 try:r[name]=str(PC.get_editor_property(name))
 except Exception as e:r[name]=str(e)
(Path(unreal.Paths.project_dir())/'Saved/ProjectRefinement/DayNightV1/PauseInspection.json').write_text(json.dumps(r,indent=2))
for n in ['W','GI','PC','obj']:globals().pop(n,None)
