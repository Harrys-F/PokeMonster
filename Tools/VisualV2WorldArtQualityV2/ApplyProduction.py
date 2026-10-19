"""Commit only the reviewed eleven-actor delta to the existing central map. No new map."""
import unreal,json,sys,copy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtQualityV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not E.get_game_world();w=E.get_editor_world();assert w.get_path_name()=='/Game/Maps/Dev_TestMap_VisualV2.Dev_TestMap_VisualV2'
dirty=[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()];assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert not (S/'AfterScene.json').exists(),'Do not repeat a production save'
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
sys.path.insert(0,str(R/'Tools/VisualV2WorldArtQualityV2'));from RuntimeVariants import Variants
def canonical(s):
 s=copy.deepcopy(s)
 for a in s['actors'].values():a['components'].sort(key=lambda c:c['name'])
 return s
current=canonical(scene(w));baseline=canonical(json.loads((S/'Dev_TestMap_VisualV2_Scene.json').read_text()))
if dirty:
 assert dirty==['/Game/Maps/Dev_TestMap_VisualV2'] and (S/'ApplyFailureScene.json').exists()
 assert current==canonical(json.loads((S/'ApplyFailureScene.json').read_text())),'Do not overwrite any change since the owned guard failure'
 before=canonical(json.loads((S/'BeforeProductionScene.json').read_text()));assert before==baseline
else:
 before=current;assert before==baseline
 (S/'BeforeProductionScene.json').write_text(json.dumps(before,indent=2))
v=Variants(w);v.apply('V2');after=canonical(scene(w));assert before['world_settings']==after['world_settings'];assert before['actors'].keys()==after['actors'].keys()
groups={r['actor']:r for r,c in v.groups};ground={c.get_owner().get_name() for c,old,new in v.ground};assert len(groups)==6 and len(ground)==5
changed=[]
for name,old in before['actors'].items():
 new=after['actors'][name]
 if old==new:continue
 assert name in groups or name in ground,('Out-of-scope actor',name)
 test=copy.deepcopy(new)
 for oc,nc in zip(old['components'],test['components']):
  if oc==nc:continue
  assert oc['name']==nc['name']
  nc['materials']=oc['materials']
  if name in groups:
   assert 'instances' in oc and len(oc['instances'])==len(nc['instances'])==groups[name]['count']
   for ot,nt in zip(oc['instances'],nc['instances']):assert max(abs(a-b) for a,b in zip(ot[2],nt[2]))<3e-6 and abs(ot[0][2]-nt[0][2])<1e-6,'Instance scale/height changed beyond six-decimal Transform and single-precision HISM matrix serialization'
   nc['instances']=oc['instances'];nc['props']['static_mesh']=oc['props']['static_mesh']
 assert test==old,('Unexpected actor/component property delta',name)
 changed.append(name)
assert set(changed)==set(groups)|ground;assert len(after['actors'])==1354
assert sum(c.get_instance_count() for row,c in v.groups)==175
for row,c in v.groups:
 assert c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION and not c.cast_shadow
 assert c.instance_start_cull_distance==4500 and c.instance_end_cull_distance==6500
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages(),'No shared content save permitted'
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2')
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
(S/'AfterScene.json').write_text(json.dumps(after,indent=2))
(S/'ProductionDelta.json').write_text(json.dumps({'existing_map':'/Game/Maps/Dev_TestMap_VisualV2','new_maps':0,'added_actors':0,'changed_actor_names':sorted(changed),'actor_count':len(after['actors']),'instance_count':175,'protected_other_actors':len(after['actors'])-len(changed),'all_other_actor_and_world_properties_identical':True,'authored_instance_scales_and_heights_unchanged':True,'hism_scale_roundtrip_tolerance':3e-6,'height_roundtrip_tolerance_cm':1e-6,'original_pots_untouched':True,'adopted':'V2','baseline_commit':'371190e69776d906288e9772c7fdfcb0d635f4b1'},indent=2))
unreal.log('WAQ2_PRODUCTION_SAVED_ELEVEN_ACTORS_ONLY')
