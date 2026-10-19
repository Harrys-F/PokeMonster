"""Read-only SHA-256 and ref protection audit, against the task-start snapshot outside Git."""
from pathlib import Path
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[2];O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V2_2026-10-19');before=json.loads((O/'ProtectedBefore.json').read_text());allowed={'Content/Maps/Dev_TestMap_VisualV2.umap','Docs/TECHNIK.md','Docs/ENTSCHEIDUNGEN.md'}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(4*1024*1024):h.update(b)
 return h.hexdigest()
changes=[]
for rel,row in before.items():
 p=R/rel;assert p.is_file(),('Original file missing',rel)
 h=sha(p)
 if h!=row['sha256']:changes.append(rel)
assert set(changes)<=allowed,('Unexpected original file changes',set(changes)-allowed)
assert sha(O/'Dev_TestMap_VisualV2_V1_Backup.umap')==before['Content/Maps/Dev_TestMap_VisualV2.umap']['sha256']
backup='03492bd96b4dba44692f675c19d5f11abfa86b4b'
for ref in ['backup/full-03492bd','refs/archive/pokemonster/full-backup-03492bd']:assert subprocess.check_output(['git','rev-parse',ref],cwd=R,text=True).strip()==backup
assert subprocess.run(['git','merge-base','--is-ancestor',backup,'HEAD'],cwd=R).returncode==1
result={'protected_files':len(before),'protected_bytes':sum(r['bytes'] for r in before.values()),'unchanged_original_files':len(before)-len(changes),'permitted_changed_files':changes,'no_original_file_missing':True,'full_backup_ref_and_main_unchanged':backup,'map_backup_sha256_verified':True}
(O/'ProtectionAfter.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
