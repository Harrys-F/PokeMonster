from pathlib import Path
import json,hashlib,copy,subprocess
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2WorldArtV7';O=Path('/Users/harry/Documents/Codex/PokeMonster_WorldArt_V7_2026-10-19')
def canon(v):
 v=copy.deepcopy(v)
 for a in v['actors'].values():a['components'].sort(key=lambda c:c['name'])
 return v
before=canon(json.loads((S/'BeforeScene.json').read_text()));after=canon(json.loads((S/'AfterScene.json').read_text()));d=json.loads((S/'Delta.json').read_text());binding_names={r['name'] for r in d['material_bindings']}
assert before['world_settings']==after['world_settings']
for name,old in before['actors'].items():
 actual=copy.deepcopy(after['actors'][name])
 if name in binding_names:
  for x,y in zip(old['components'],actual['components']):y['materials']=x['materials']
 assert actual==old,('Unexpected existing actor edit',name)
assert set(after['actors'])-set(before['actors'])=={g['name'] for g in d['new_groups']}
initial=json.loads((O/'InitialState.json').read_text());unchanged=[]
for rel,sha in initial['map_sha256'].items():
 if rel=='Content/Maps/Dev_TestMap_VisualV2.umap':continue
 assert hashlib.sha256((R/rel).read_bytes()).hexdigest()==sha,rel;unchanged.append(rel)
assert set(p.name for p in (R/'Content/Maps').glob('*.umap'))=={Path(k).name for k in initial['map_sha256']},'Map added or removed'
assert (S/'ProtectedLightingAfter.json').read_bytes()==(S/'ProtectedLightingBefore.json').read_bytes()
for ref in ['main','refs/archive/pokemonster/full-backup-03492bd']:
 assert subprocess.check_output(['git','rev-parse',ref],cwd=R,text=True).strip()=='03492bd96b4dba44692f675c19d5f11abfa86b4b'
assert subprocess.run(['git','merge-base','--is-ancestor','03492bd','HEAD'],cwd=R).returncode==1
result={'existing_actors_preserved':len(before['actors']),'only_existing_changes':'six ground/path material bindings','new_hism_groups':d['new_actors'],'new_decorative_instances':d['new_instances'],'other_maps_unchanged':unchanged,'no_map_added_or_removed':True,'protected_lighting_exact':True,'backup_refs_unchanged_and_not_ancestor':True};(S/'FinalScopeAudit.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
