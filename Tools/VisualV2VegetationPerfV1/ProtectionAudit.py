"""Verify all pre-existing project content and every map without modifying them."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2];O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18');before=json.loads((O/'BeforeFiles.json').read_text());allowed={'Source/PokeMonster/Development/PokeMonsterEnvironmentPerformanceProbeV2.cpp'};changed=[];missing=[]
for name,d in before.items():
 p=R/name
 if not p.exists():missing.append(name)
 elif hashlib.sha256(p.read_bytes()).hexdigest()!=d['sha256']:changed.append(name)
assert not missing and not(set(changed)-allowed),(missing,set(changed)-allowed)
backup='03492bd96b4dba44692f675c19d5f11abfa86b4b';git=lambda *a:subprocess.check_output(['git',*a],cwd=R,text=True).strip();assert git('rev-parse','main')==backup and git('rev-parse','refs/archive/pokemonster/full-backup-03492bd')==backup
maps=[n for n in before if n.startswith('Content/Maps/')];assert not(set(maps)&set(changed))
original_status=subprocess.check_output(['git','status','--short'],cwd='/Users/harry/Developer/PokeMonster/Game/PokeMonster',text=True).strip();assert not original_status
result={'checked':len(before),'changed_existing_files':changed,'missing_original_files':missing,'all_original_maps_byte_identical':True,'map_count':len(maps),'original_worktree_status':original_status,'backup_unchanged':backup}
(O/'ProtectionAudit.json').write_text(json.dumps(result,indent=2));print('PROTECTION_PASS',len(before),changed)
