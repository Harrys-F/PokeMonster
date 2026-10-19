"""Compare original map/source/config bytes and protected backup refs. No mutations."""
from pathlib import Path
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[2];O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V1_2026-10-19');before=json.loads((O/'ProtectedBefore.json').read_text());changed=[];missing=[]
for name,sha in before.items():
 p=R/name
 if not p.is_file():missing.append(name)
 elif hashlib.sha256(p.read_bytes()).hexdigest()!=sha:changed.append(name)
assert not missing and changed==['Content/Maps/Dev_TestMap_VisualV2.umap'],(missing,changed)
g=lambda *args:subprocess.check_output(['git',*args],cwd=R,text=True).strip();backup='03492bd96b4dba44692f675c19d5f11abfa86b4b';assert g('rev-parse','main')==g('rev-parse','refs/archive/pokemonster/full-backup-03492bd')==backup
original=subprocess.check_output(['git','status','--short'],cwd='/Users/harry/Developer/PokeMonster',text=True);assert not original,original
save=json.loads((R/'Saved/VisualV2WorldArtQualityV1/Acceptance/ArtFinalFoot/SaveRestored.json').read_text());assert save['restored'] and not save['initial']['existed'] and not (R/'Saved/SaveGames/PokeMonster_Dev.sav').exists()
out={'checked_files':len(before),'changed_existing':changed,'all_other_maps_and_source_and_config_unchanged':True,'missing':missing,'original_worktree_status':original,'backup':backup,'dev_save_original_absence_restored':True};(O/'ProtectionAudit.json').write_text(json.dumps(out,indent=2));print(out)
