"""Retire only this task's redundant temporary imports after verified reuse, not original NPC assets."""
import unreal,json,hashlib,subprocess
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/NPCExpansion';rows=json.loads((O/'SupersededCandidates.json').read_text());paths={x['asset']for x in rows};assert len(paths)==27;assets=[]
for x in rows:
 p=x['asset'];assert any(p.startswith('/Game/Characters/NPCs/Library/'+id+'/')for id in ['WhiteHairedWarrior','DwarfWarrior','ElvenArcher']) and '/SharedSkeleton/'not in p
 assert subprocess.run(['git','ls-files','--error-unmatch','--',x['file']],cwd=R,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==1
 refs={str(v).split('.')[0]for v in unreal.EditorAssetLibrary.find_package_referencers_for_asset(p,True)};assert not refs-paths,(p,refs-paths);f=R/x['file'];x['sha256']=hashlib.sha256(f.read_bytes()).hexdigest();assets.append(unreal.load_asset(p))
assert unreal.EditorAssetLibrary.delete_loaded_assets(assets)
assert all(not unreal.EditorAssetLibrary.does_asset_exist(p) for p in paths)
(O/'RetiredOwnDuplicates.json').write_text(json.dumps({'deleted_only_new_redundant_imports':rows,'original_assets_untouched':True},indent=2))
