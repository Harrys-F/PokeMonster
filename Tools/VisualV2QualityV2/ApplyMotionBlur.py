"""One-time guarded integration. Changes only three MotionBlur fields in VisualV2."""
import unreal,json,runpy,copy,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2QualityV2';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert R==Path('/Users/harry/Developer/PokeMonster')
assert not e.get_game_world();w=e.get_editor_world();assert w.get_path_name()=='/Game/Maps/Dev_TestMap_VisualV2.Dev_TestMap_VisualV2'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert not (O/'BeforeScene.json').exists(), 'Do not apply twice; inspect previous result'
backup=json.loads(Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17/MapBackup.json').read_text());assert hashlib.sha256((R/'Content/Maps/Dev_TestMap_VisualV2.umap').read_bytes()).hexdigest()==backup['sha256']
scene=runpy.run_path(str(R/'Tools/VisualV2QualityV2/AuditScene.py'))['scene'];before=scene(w);(O/'BeforeScene.json').write_text(json.dumps(before,indent=2));expected=copy.deepcopy(before)
volumes=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PostProcessVolume);bylabel={a.get_actor_label():a for a in volumes};assert len(volumes)==2
outside=bylabel['V2_OutdoorExposure'];inside=bylabel['V2_House_HH_Art_InteriorLighting'];outside_name=outside.get_name();inside_name=inside.get_name();assert outside.unbound and not inside.unbound and outside.priority<inside.priority
for a,value in [(outside,0.0),(inside,0.5)]:
 s=a.settings;assert not s.override_motion_blur_amount and s.motion_blur_amount==0.5
 old=expected['actors'][a.get_name()]['pp'];replacement=old.replace('bOverride_MotionBlurAmount=False','bOverride_MotionBlurAmount=True')
 if a==outside:replacement=replacement.replace('MotionBlurAmount=0.500000','MotionBlurAmount=0.000000')
 expected['actors'][a.get_name()]['pp']=replacement
 a.modify();s.set_editor_property('override_motion_blur_amount',True);s.set_editor_property('motion_blur_amount',value);a.set_editor_property('settings',s)
assert scene(w)==expected,'Unexpected change; do not save'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert [x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()]==['/Game/Maps/Dev_TestMap_VisualV2']
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2')
assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2');after=scene(e.get_editor_world());assert after==expected,'Reopened map differs'
(O/'AfterScene.json').write_text(json.dumps(after,indent=2));(O/'MapChangeAudit.json').write_text(json.dumps({'actors':len(before['actors']),'changes':[{'actor':outside_name,'field':'override_motion_blur_amount','before':False,'after':True},{'actor':outside_name,'field':'motion_blur_amount','before':0.5,'after':0},{'actor':inside_name,'field':'override_motion_blur_amount','before':False,'after':True}],'all_other_scene_and_complete_postprocess_settings_equal':True,'saved_and_reopened':True,'original_backup_sha256':backup['sha256']},indent=2))
unreal.SystemLibrary.execute_console_command(e.get_editor_world(),'MAP CHECK');unreal.log('VEQ2_MOTION_BLUR_ONLY_SAVED')
