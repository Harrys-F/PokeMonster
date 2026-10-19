"""Read-only map/import audit and guarded embedded-PIE queue after project relocation."""
import unreal,json,time,traceback,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();assert R==Path('/Users/harry/Developer/PokeMonster')
O=R/'Saved/ProjectMigration';O.mkdir(exist_ok=True)
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
def dirty():
 return {'maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'content':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
assert not E.get_game_world() and not any(dirty().values()),dirty()
maps=[]
for name in ['Dev_WestlandRegion','Dev_TestMap_NPCMotionV3','Dev_TestMap_VisualV2']:
 assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/'+name)
 w=E.get_editor_world();assert w.get_name()==name
 unreal.log('PROJECT_MIGRATION_MAPCHECK_BEGIN '+name)
 unreal.SystemLibrary.execute_console_command(w,'MAP CHECK')
 unreal.log('PROJECT_MIGRATION_MAPCHECK_END '+name)
 maps.append({'map':w.get_path_name(),'actors':len(unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)),'dirty':dirty()})
 assert not any(dirty().values()),dirty()
(O/'Maps.json').write_text(json.dumps(maps,indent=2))
reg=unreal.AssetRegistryHelpers.get_asset_registry();reg.wait_for_completion()
imports=[];missing=[];fixes=[];classes={'Texture2D','StaticMesh','SkeletalMesh','AnimSequence'}
oldroots=['/Users/harry/Developer/PokeMonster/Game/PokeMonster','/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree']
for data in reg.get_assets_by_path('/Game',recursive=True):
 if str(data.asset_class_path.asset_name) not in classes:continue
 a=data.get_asset();assert a is not None,str(data.package_name)
 imp=a.get_editor_property('asset_import_data')
 if not imp:continue
 for i,source in enumerate(imp.extract_filenames()):
  if not source:continue
  p=Path(source);row={'asset':a.get_path_name(),'index':i,'source':source,'exists':p.is_file()};imports.append(row)
  if not row['exists']:
   candidate=None
   for old in oldroots:
    try:rel=p.relative_to(old)
    except ValueError:continue
    new=R/rel
    if new.is_file():candidate=str(new);break
   if candidate:fixes.append({**row,'candidate':candidate})
   else:missing.append(row)
(O/'Imports.json').write_text(json.dumps({'sources':imports,'relocation_fixes_needed':fixes,'other_missing':missing,'method':'Fresh live AssetImportData.extract_filenames; no reimport or asset save.'},indent=2))
assert not any(dirty().values()),dirty()
last=0;busy=False
def poll(dt):
 global last,busy
 f=O/'EditorJob.json'
 if busy or not f.exists():return
 j=json.loads(f.read_text())
 if j['id']==last:return
 last=j['id'];busy=True;close=False
 try:
  action=j['action']
  if action=='start_pie':
   assert not E.get_game_world() and not any(dirty().values())
   unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_begin_play()
  elif action=='start_route':
   request=json.loads((O/'AcceptanceRequest.json').read_text());dest=O/'Acceptance'/request['label']
   w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0))
   p=unreal.GameplayStatics.get_player_pawn(w,0);arm=p.get_component_by_class(unreal.SpringArmComponent);cam=p.get_component_by_class(unreal.CameraComponent)
   assert arm.target_arm_length==2850 and cam.field_of_view==35
   v=next(v for v in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PostProcessVolume) if v.get_actor_label()=='V2_OutdoorExposure')
   blends=v.settings.weighted_blendables.array;assert len(blends)==1 and isinstance(blends[0].object,unreal.PokeMonsterTemporalAABlendable)
   unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Viewport 1280 720')
   (dest/'Graphics.json').write_text(json.dumps({'camera_distance_cm':arm.target_arm_length,'camera_fov':cam.field_of_view,'taa_blendable':blends[0].object.get_path_name(),'project':str(R)}))
   source=(R/'Tools/VisualV2QualityV2/FootTest.py').read_text().replace('Saved/VisualV2QualityV2','Saved/ProjectMigration')
   exec(compile(source,'existing_full_gameplay_route','exec'),{'__name__':'__main__'})
  elif action=='stop_pie':unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
  elif action=='state':
   (O/'EditorState.json').write_text(json.dumps({'project':str(R),'world':E.get_editor_world().get_path_name(),'playing':bool(E.get_game_world()),'dirty':dirty()},indent=2))
  elif action=='close':
   assert not E.get_game_world() and not any(dirty().values()),dirty();close=True
  else:raise ValueError('Unknown maintenance action '+action)
  ack={'id':last,'ok':True}
 except Exception:ack={'id':last,'ok':False,'error':traceback.format_exc()};unreal.log_error(ack['error'])
 finally:busy=False
 (O/'EditorAck.json').write_text(json.dumps(ack,indent=2))
 if close:unreal.SystemLibrary.quit_editor()
unreal._project_migration_queue=unreal.register_slate_post_tick_callback(poll)
(O/'EditorReady.json').write_text(json.dumps({'project':str(R),'ready':True,'maps':len(maps),'imports':len(imports),'missing_sources':len(missing),'path_fixes_needed':len(fixes)},indent=2))
unreal.log('PROJECT_MIGRATION_READY')
