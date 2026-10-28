"""Keep existing hidden prototype collision helpers aligned with their moved art.
No collision removal and no shared mesh modification. Only explicit pond-bank
relocations recorded by ApplyPond are eligible, with original-position guards.
"""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PokemonWaterTeamV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world()
assert not E.get_game_world()and W.get_name()=='Dev_TestMap_VisualV2'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert not(D/'BankCollisionAligned.json').exists()
by={a.get_actor_label():a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()};planned=[];seen=set()
for row in json.loads((D/'PondApplied.json').read_text())['changes']:
 if row['purpose']!='preserved decoration relocated onto bank':continue
 label=row['actor'];original=label.split('_P2D_',1)[1];before=unreal.Transform();before.import_text(row['before']);after=unreal.Transform();after.import_text(row['after']);delta=after.translation-before.translation
 aliases=[original]
 if original.endswith('_Trunk'):aliases=[x for x in by if x.startswith(original[:-6]+'_')]
 elif original.endswith('Trunk'):aliases=[x for x in by if x.startswith(original[:-5])]
 for name in aliases:
  if name not in by or name in seen:continue
  a=by[name];old=a.get_actor_location()
  assert (old.x-before.translation.x)**2+(old.y-before.translation.y)**2<250*250,(name,old,before.translation)
  planned.append((a,old,unreal.Vector(after.translation.x,after.translation.y,old.z)));seen.add(name)
assert planned
records=[]
for a,old,new in planned:
 records.append({'actor':a.get_actor_label(),'before':old.to_tuple(),'after':new.to_tuple(),'actor_collision_retained':a.get_actor_enable_collision()});a.set_actor_location(new,False,False)
assert all(p.get_path_name()=='/Game/Maps/Dev_TestMap_VisualV2'for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages())and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2');(D/'BankCollisionAligned.json').write_text(json.dumps(records,indent=2))
