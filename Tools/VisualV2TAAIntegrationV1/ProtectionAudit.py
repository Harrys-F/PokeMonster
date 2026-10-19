"""Read-only pre-existing-file SHA verification; new own outputs are inventoried separately."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2];O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18');before=json.loads((O/'BeforeFiles.json').read_text());allowed={'Content/Maps/Dev_TestMap_VisualV2.umap','Docs/TECHNIK.md','Docs/ENTSCHEIDUNGEN.md','Source/PokeMonster/Development/PokeMonsterEnvironmentPerformanceProbeV2.cpp'};changed=[];missing=[]
for name,d in before.items():
 p=R/name
 if not p.exists():missing.append(name)
 elif hashlib.sha256(p.read_bytes()).hexdigest()!=d['sha256']:changed.append(name)
assert not missing and not (set(changed)-allowed),(missing,set(changed)-allowed)
map_audit=json.loads((R/'Saved/VisualV2TAAIntegrationV1/MapChangeAudit.json').read_text());assert hashlib.sha256((R/'Content/Maps/Dev_TestMap_VisualV2.umap').read_bytes()).hexdigest()==map_audit['after_sha256']
backup='03492bd96b4dba44692f675c19d5f11abfa86b4b';git=lambda *a:subprocess.check_output(['git',*a],cwd=R,text=True).strip();assert git('rev-parse','backup/full-03492bd')==backup and git('rev-parse','refs/archive/pokemonster/full-backup-03492bd')==backup
maps=[name for name in before if name.startswith('Content/Maps/')];assert all(name=='Content/Maps/Dev_TestMap_VisualV2.umap' or name not in changed for name in maps)
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';states=[json.loads(p.read_text()) for p in (R/'Saved/VisualV2TAAIntegrationV1/Acceptance').glob('*/SaveRestored.json')];assert len(states)==3 and all(s['restored'] and not s['initial']['existed'] for s in states) and not slot.exists()
d={'checked':len(before),'changed_existing_files':changed,'missing_original_files':missing,'unexpected_changes':sorted(set(changed)-allowed),'all_other_maps_byte_identical':True,'original_map_count':len(maps),'dev_slot_original_absence_restored':True,'backup':backup,'original_worktree_status':subprocess.check_output(['git','status','--short'],cwd='/Users/harry/Developer/PokeMonster',text=True).strip()};assert not d['original_worktree_status'];(O/'ProtectionAudit.json').write_text(json.dumps(d,indent=2));print('PROTECTION_PASS',len(before),'files; only',changed)
