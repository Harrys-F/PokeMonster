import unreal,json,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV3';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not e.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
initial=json.loads((O/'InitialEditor.json').read_text());path=e.get_editor_world().get_path_name().split('.')[0]
assert unreal.EditorLoadingAndSavingUtils.load_map(path)
exec((R/'Tools/EnvironmentPerfV3/AuditInitial.py').read_text().replace("InitialEditor.json","ReopenedEditor.json"))
reopened=json.loads((O/'ReopenedEditor.json').read_text());aa={a['label']:a for a in initial['actors']};bb={a['label']:a for a in reopened['actors']};diff={k:{'live':aa.get(k),'disk':bb.get(k)} for k in set(aa)|set(bb) if aa.get(k)!=bb.get(k)}
(O/'EditorDiskComparison.json').write_text(json.dumps({'original_world':initial['world'],'reloaded_world':reopened['world'],'live_dirty_packages':initial['dirty_maps']+initial['dirty_content'],'differences':diff,'no_save_or_discard':True},indent=2))
norm=lambda x: re.sub(r'0x[0-9a-fA-F]+','0xPTR',json.dumps(x,sort_keys=True))
real={k:v for k,v in diff.items() if norm(v['live'])!=norm(v['disk'])}
(O/'EditorDiskComparison.json').write_text(json.dumps({'original_world':initial['world'],'reloaded_world':reopened['world'],'live_dirty_packages':initial['dirty_maps']+initial['dirty_content'],'differences_ignoring_transient_python_struct_addresses':real,'transient_address_only_differences':len(diff)-len(real),'no_save_or_discard':True},indent=2))
assert not real,list(real)
source='/Game/Maps/Dev_TestMap_EnvironmentPerfV2';target='/Game/Maps/Dev_TestMap_EnvironmentPerfV3'
assert not unreal.EditorAssetLibrary.does_asset_exist(target),'Preserve existing V3'
assert unreal.EditorLoadingAndSavingUtils.load_map(source);w=e.get_editor_world()
assert unreal.EditorLoadingAndSavingUtils.save_map(w,target);assert unreal.EditorLoadingAndSavingUtils.load_map(target)
(O/'MapCopy.json').write_text(json.dumps({'source':source,'target':target,'method':'save_map to new package; load new package; source never saved'},indent=2))
