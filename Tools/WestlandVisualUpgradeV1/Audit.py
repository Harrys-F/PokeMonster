"""Final saved-scene audit; compares original gameplay actors exactly and visual edits narrowly."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualUpgradeV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();W=E.get_editor_world();assert W.get_name()=='Dev_WestlandRegion';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
before=json.loads((D/'Dev_WestlandRegion_Before.json').read_text());after=scene(W);(D/'SceneAfter.json').write_text(json.dumps(after,indent=2));old=before['actors'];new=after['actors'];assert set(old)<=set(new);allowed={x['actor']for x in json.loads((D/'SurfaceAudit.json').read_text())['bindings']};allowed.update(k for k,v in old.items()if v['label']in ['WR_Oak','WR_Bush','WR_GrassSmall','WR_GrassMedium','WR_GrassLarge','WR_TrunkCollision','WR_RockyContours']);changed=[];same=0
for k,a in old.items():
 b=new[k]
 if a==b:same+=1;continue
 assert k in allowed,(k,a['label'],'Unexpected original actor change');assert a['transform']==b['transform'],(k,'Original actor transform changed');changed.append(a['label'])
for k,a in old.items():
 if a['class'].split('.')[-1]in ['PokeMonsterNPC','PokeMonsterNPCVisualActor','PokeMonsterRestPoint','PokeMonsterHabitatZone','PokeMonsterWorldItem','PokeMonsterBuildingCutaway','PlayerStart','DirectionalLight','SkyLight','PostProcessVolume']:
  assert a==new[k],(a['label'],'Protected gameplay/light actor changed')
assert before['world_settings']==after['world_settings'];result=dict(passed=True,original_actors=len(old),final_actors=len(new),original_actors_exactly_unchanged=same,intentional_original_visual_actor_edits=changed,new_group_actors=[v['label']for k,v in new.items()if k not in old],dirty_maps=[],dirty_assets=[]);(D/'SceneAudit.json').write_text(json.dumps(result,indent=2));unreal.log('WESTLAND_VISUAL_SCENE_AUDIT_PASS')
