"""Only the temporary duplicate assets created by this task, never existing NPC assets."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/NPCExpansion';protected=json.loads((O/'Baseline.json').read_text())['protected'];candidates=set()
for id in ['WhiteHairedWarrior','DwarfWarrior','ElvenArcher']:
 for p in unreal.EditorAssetLibrary.list_assets('/Game/Characters/NPCs/Library/'+id,True,False):
  p=p.split('.')[0]
  if '/SharedSkeleton/' not in p:candidates.add(p)
assert len(candidates)==27,len(candidates);rows=[]
for p in sorted(candidates):
 file='Content/'+p.removeprefix('/Game/')+'.uasset';assert file not in protected;refs=[str(x).split('.')[0]for x in unreal.EditorAssetLibrary.find_package_referencers_for_asset(p,True)];external=[x for x in refs if x not in candidates];assert not external,(p,external);rows.append({'asset':p,'file':file,'referencers':refs,'external_referencers':external})
(O/'SupersededCandidates.json').write_text(json.dumps(rows,indent=2));unreal.log('NPC_OWN_UNUSED_CANDIDATES '+str(len(rows)))
