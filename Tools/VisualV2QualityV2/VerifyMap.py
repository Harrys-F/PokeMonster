"""Independently verify the persisted map against its complete pre-change signature."""
import unreal,json,runpy,copy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2QualityV2';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not e.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2')
before=json.loads((O/'BeforeScene.json').read_text());expected=copy.deepcopy(before);changes=[]
for name,a in expected['actors'].items():
 if a['label'] in ['V2_OutdoorExposure','V2_House_HH_Art_InteriorLighting']:
  a['pp']=a['pp'].replace('bOverride_MotionBlurAmount=False','bOverride_MotionBlurAmount=True');changes.append({'actor':name,'field':'override_motion_blur_amount','before':False,'after':True})
  if a['label']=='V2_OutdoorExposure':a['pp']=a['pp'].replace('MotionBlurAmount=0.500000','MotionBlurAmount=0.000000');changes.append({'actor':name,'field':'motion_blur_amount','before':0.5,'after':0})
scene=runpy.run_path(str(R/'Tools/VisualV2QualityV2/AuditScene.py'))['scene'];after=scene(e.get_editor_world());assert after==expected, 'Persisted map has unexpected changes'
(O/'MapChangeAudit.json').write_text(json.dumps({'actors':len(before['actors']),'changes':changes,'all_other_scene_and_complete_postprocess_settings_equal':True,'saved_and_reopened':True,'independent_verification':True,'dirty_maps':[],'dirty_content':[]},indent=2));unreal.SystemLibrary.execute_console_command(e.get_editor_world(),'MAP CHECK');unreal.log('VEQ2_MAPCHECK_VERIFIED')
# Read-only lighting inventory for the final GPU recommendations.
lights=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(e.get_editor_world(),unreal.Light):
 for c in a.get_components_by_class(unreal.LightComponent):
  row={'actor':a.get_actor_label(),'component':c.get_class().get_name(),'properties':{}}
  for n in ['mobility','intensity','cast_shadows','cast_dynamic_shadows','cast_static_shadows','affect_translucent_lighting','cast_volumetric_shadow','contact_shadow_length','use_ray_traced_distance_field_shadows']:
   try:row['properties'][n]=str(c.get_editor_property(n))
   except Exception:pass
  lights.append(row)
(O/'LightingInventory.json').write_text(json.dumps(lights,indent=2))
