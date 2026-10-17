"""Restore only the guarded dev slot changed by our completed foot test; retain both copies."""
from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV3';p=R/'Saved/SaveGames/PokeMonster_Dev.sav';original=O/'PokeMonster_Dev_Original.sav';foot=json.loads((O/'FootTest/FootTest.json').read_text());h=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
assert foot['passed'];before=h(p);expected=h(original)
if before!=expected:
 assert before==foot['save_after_sha256'],'Outside save change detected; do not overwrite'
 preserved=O/'PokeMonster_Dev_FootTest_Result.sav';assert not preserved.exists();shutil.copy2(p,preserved);shutil.copy2(original,p)
assert h(p)==expected
(O/'DevSaveRestored.json').write_text(json.dumps({'before_restore_sha256':before,'original_sha256':expected,'after_restore_sha256':h(p),'foot_test_result_preserved':str(O/'PokeMonster_Dev_FootTest_Result.sav')},indent=2));print('Dev save restored byte-for-byte')
