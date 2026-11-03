"""Verify original working files/saves against task-start SHA256, without resetting anything."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2PokemonTestGroundHealhouseV7'
allowed={'Content/Maps/Dev_TestMap_VisualV2.umap','Config/DefaultPokeMonsterHabitats.ini','Docs/ENTSCHEIDUNGEN.md','Source/PokeMonster/Development/PokeMonsterCreatureTestGround.cpp','Source/PokeMonster/Development/PokeMonsterCreatureTestGround.h','Source/PokeMonster/Creatures/Overworld/PokeMonsterCreatureRoamingComponent.cpp','Source/PokeMonster/Creatures/Overworld/PokeMonsterCreatureRoamingComponent.h','Source/PokeMonster/Creatures/Overworld/PokeMonsterCreatureRoamingActivities.cpp','Source/PokeMonster/Habitats/PokeMonsterHabitatSubsystem.cpp','Source/PokeMonster/Habitats/PokeMonsterHabitatSubsystem.h','Source/PokeMonster/Tests/PokeMonsterCreatureTestGroundTest.cpp'}
results={}
for name in ['FileBaseline','OriginalAssetBaseline','SaveBaseline']:
 original=json.loads((D/(name+'.json')).read_text());changed=[];missing=[]
 for relative,sha in original.items():
  p=R/relative
  if not p.is_file():missing.append(relative);continue
  h=hashlib.sha256()
  with p.open('rb')as f:
   for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
  if h.hexdigest()!=sha:changed.append(relative)
 unexpected=set(changed)-allowed if name=='FileBaseline'else set(changed);assert not missing and not unexpected,dict(baseline=name,missing=missing,unexpected=sorted(unexpected));results[name]=dict(checked=len(original),changed=changed,missing=missing,unexpected=[])
refs={ref:subprocess.check_output(['git','rev-parse',ref],cwd=R,text=True).strip()for ref in ['backup/full-03492bd','refs/archive/pokemonster/full-backup-03492bd']};assert all(v=='03492bd96b4dba44692f675c19d5f11abfa86b4b'for v in refs.values());results['backup_refs']=refs
results['user_config_sha256']=hashlib.sha256((R/'Config/DefaultEngine.ini').read_bytes()).hexdigest();assert results['user_config_sha256']=='f676a51869c678a5820c869165154b6d6e05ae723c77c622d5fb510957799523'
(D/'ProtectionFinal.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
