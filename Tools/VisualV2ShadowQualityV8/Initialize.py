"""Generate local safety inputs from the current project; never requires archived review media."""
from pathlib import Path
import subprocess,json,hashlib,shutil
from ProcessGuard import editor_pids
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2ShadowQualityV8';O=Path('/Users/harry/Documents/Codex/PokeMonster_ShadowQuality_V8_2026-10-19');assert not editor_pids()
for p in [S,O]:p.mkdir(parents=True,exist_ok=True)
state={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'status':subprocess.check_output(['git','status','--short'],cwd=R,text=True),'maps':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'Content/Maps').glob('*.umap')}}
f=O/'InitialState.json';backup=O/'VisualV2_Original.umap'
if f.exists():
 old=json.loads(f.read_text());assert old['maps']==state['maps'],'Map changed since prior session; keep existing evidence and start a deliberately named new session'
else:f.write_text(json.dumps(state,indent=2))
sha=state['maps']['Content/Maps/Dev_TestMap_VisualV2.umap']
if backup.exists():assert hashlib.sha256(backup.read_bytes()).hexdigest()==sha
else:shutil.copy2(R/'Content/Maps/Dev_TestMap_VisualV2.umap',backup)
assert subprocess.check_output(['git','rev-parse','main'],cwd=R,text=True).strip()=='03492bd96b4dba44692f675c19d5f11abfa86b4b'
print('Original safety baseline available; no project asset changed')
