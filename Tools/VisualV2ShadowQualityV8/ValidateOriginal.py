import unreal,json,sys,copy,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir());S=R/'Saved/VisualV2ShadowQualityV8';O=Path('/Users/harry/Documents/Codex/PokeMonster_ShadowQuality_V8_2026-10-19');E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
a=scene(E.get_editor_world());b=json.loads((S/'BeforeScene.json').read_text())
for v in [a,b]:
 for actor in v['actors'].values():actor['components'].sort(key=lambda x:x['name'])
assert a==b,'Unexpected persistent editor-scene change';initial=json.loads((O/'InitialState.json').read_text())
for rel,sha in initial['maps'].items():assert hashlib.sha256((R/rel).read_bytes()).hexdigest()==sha,rel
assert {str(p.relative_to(R)) for p in (R/'Content/Maps').glob('*.umap')}==set(initial['maps'])
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(S/'OriginalRestored.json').write_text(json.dumps({'full_editor_scene_equal':True,'all_17_map_sha256_unchanged':True,'no_map_created':True,'actor_count':len(a['actors']),'dirty_maps':[],'dirty_content':[]},indent=2));unreal.log('SV8_ORIGINAL_EXACTLY_PRESERVED')
