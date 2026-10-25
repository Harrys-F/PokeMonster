"""Full-scene equality except the two explicitly selected fill-light instance settings."""
import unreal,json,sys,copy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/LightingV31';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert not E.get_game_world();sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
before=json.loads((D/'BeforeScene.json').read_text());after=scene(W);cfg=json.loads((R/'Tools/VisualV2LightingV31/Settings.json').read_text());a=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)if a.get_actor_label()==cfg['actor_label']);light=a.get_component_by_class(unreal.DirectionalLightComponent);assert abs(light.intensity-cfg['after']['intensity'])<1e-6 and abs(a.get_actor_rotation().yaw-cfg['after']['yaw'])<.001 and abs(a.get_actor_rotation().pitch-cfg['after']['pitch'])<.001;assert not light.cast_shadows;assert abs(a.get_actor_rotation().roll-cfg['after']['roll'])<.001
norm=copy.deepcopy(after);row=norm['actors'][a.get_name()];old=before['actors'][a.get_name()];assert row['transform'][0]==old['transform'][0]and row['transform'][2]==old['transform'][2];row['transform'][1]=old['transform'][1]
for c in row['components']:
 prev=next(v for v in old['components']if v['name']==c['name']);assert c['transform'][0]==prev['transform'][0]and c['transform'][2]==prev['transform'][2];assert max(abs(x-y)for x,y in zip(c['transform'][1],after['actors'][a.get_name()]['transform'][1]))<1e-8 or max(abs(x+y)for x,y in zip(c['transform'][1],after['actors'][a.get_name()]['transform'][1]))<1e-8;c['transform'][1]=prev['transform'][1]
 if 'intensity'in c['props']:
  assert c['class']=='/Script/Engine.DirectionalLightComponent'and abs(float(c['props']['intensity'])-cfg['after']['intensity'])<1e-6;c['props']['intensity']=prev['props']['intensity']
assert norm==before,'Unexpected scene change beyond fill direction/intensity'
# Re-audit original sunlight, sky, light channels, temperature, AO and exposure, not just image brightness.
initial=json.loads((D/'Inspection.json').read_text())
for old in initial['lights']:
 actor=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)if a.get_name()==old['actor']);c=next(c for c in actor.get_components_by_class(unreal.LightComponentBase)if c.get_class().get_name()==old['class'])
 for p,value in old['props'].items():
  if actor==a and p=='intensity':continue
  v=c.get_editor_property(p);now=v.get_path_name()if isinstance(v,unreal.Object)else v.export_text()if hasattr(v,'export_text')else str(v)
  if old['label']==cfg['actor_label']and p=='intensity':assert abs(float(now)-cfg['after']['intensity'])<1e-6
  else:assert now==value,(old['label'],p,value,now)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();(D/'AfterScene.json').write_text(json.dumps(after,indent=2));(D/'Validation.json').write_text(json.dumps({'passed':True,'original_actors':len(before['actors']),'actors_added_removed':0,'allowed_actor':a.get_name(),'only_fill_yaw_and_intensity':True,'sun_sky_ao_exposure_pp_materials_instances_collisions_gameplay_unchanged':True},indent=2));unreal.log('LIGHT31_SCOPE_PASS')
