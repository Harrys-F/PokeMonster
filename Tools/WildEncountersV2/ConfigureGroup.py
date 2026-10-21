"""Save only a verified GroupSize change, after full serialized open/disk map comparison.
The diagnostic disk export must come from ExportDiskMapState.py in a separate commandlet.
Unknown map differences stop this tool. No Save All, reload, discard or restore.
"""
import unreal,json,hashlib,re,difflib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/WildEncountersV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert all(p.get_path_name()=='/Game/Maps/Dev_TestMap_VisualV2'for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages());w=E.get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2'
initial=json.loads((O/'Initial.json').read_text());mapfile=R/'Content/Maps/Dev_TestMap_VisualV2.umap';assert hashlib.sha256(mapfile.read_bytes()).hexdigest()==initial['maps'][str(mapfile.relative_to(R))]
a=next(x for x in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor)if str(x.encounter_id)=='Dev_Bisasam_Wild_01');assert a.group_size==3
current=O/'OpenVerified.t3d';assert not current.exists();t=unreal.AssetExportTask();t.object=w;t.filename=str(current);t.exporter=unreal.LevelExporterT3D();t.automated=True;t.selected=False;t.prompt=False;t.replace_identical=False;assert unreal.Exporter.run_asset_export_task(t),t.errors
old=(O/'DiskBefore.t3d').read_text(encoding='utf-16');new=current.read_text(encoding='utf-16')
def normalize(text,remove_group):
 def actor(match):
  block=match.group(0);header=block.splitlines()[0]
  # Engine-created transient debugging actors differ between graphical editor and NullRHI.
  # Engine sources: GameplayDebuggerPlayerManager.h UCLASS(Transient);
  # ChaosDebugDrawComponent.cpp Params.ObjectFlags |= RF_Transient.
  if 'Class=/Script/GameplayDebugger.GameplayDebuggerPlayerManager Name=GameplayDebuggerPlayerManager_0 'in header:return ''
  if 'Class=/Script/Engine.Actor Name=ChaosDebugDrawActor 'in header:
   assert 'ChaosDebugDrawComponent'in block and 'bListedInSceneOutliner=False'in block;return ''
  if 'Class=/Script/Water.BuoyancyManager Name=BuoyancyManager_0 'in header:block=block.replace('         ActorLabel="BuoyancyManager0"\n','')
  if remove_group and "PersistentLevel.PokeMonsterVisibleWildCreatureActor_6'"in header:
   assert 'EncounterId="Dev_Bisasam_Wild_01"'in block and block.count('         GroupSize=3\n')==1;block=block.replace('         GroupSize=3\n','')
  return block
 return re.sub(r'(?ms)^      Begin Actor .*?^      End Actor\n',actor,text)
diff=list(difflib.unified_diff(normalize(old,False).splitlines(),normalize(new,True).splitlines()))
proof={'serialized_nontransient_properties_equal_except_exact_bisasam_group_size':not diff,'differences':diff,'source_sha256_unchanged':True,'intended_actor':a.get_path_name(),'group_size_before':1,'group_size_after':3,'comparison':'Complete T3D serialization, excluding two proven transient engine debug actors and one generated engine-manager label'};(O/'GroupSavePreflight.json').write_text(json.dumps(proof,indent=2));assert not diff,diff[:30]
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();proof['map_saved']=True;(O/'GroupConfiguration.json').write_text(json.dumps(proof,indent=2));unreal.log('VERIFIED_SINGLE_GROUP_PROPERTY_SAVED')
