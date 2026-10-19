"""Explicit archived map prerequisites and immutable regression signatures. No restore/delete API."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[2]
def policy():return json.loads((Path(__file__).with_suffix('.json')).read_text())
def require_historical_maps(script,root=ROOT,specification=None):
 spec=specification if specification is not None else policy();rel=Path(script).resolve().relative_to(Path(root).resolve()).as_posix()
 missing=[m for m in spec['tools'].get(rel,[]) if not (Path(root)/spec['retired_maps'][m]['file']).is_file()]
 if missing:
  print('HISTORICAL_MAP_REVIEW_NOT_EXECUTED: '+rel+'; missing '+', '.join(missing)+'. This is NOT a test pass. Current gameplay/build do not require these retired maps. Use the retained GPU/NPC test maps; an explicitly approved historical restore requires commit '+spec['restore_commit']+' and its LFS objects.',file=sys.stderr)
  raise SystemExit(2)
def actor_digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def npc_baseline(root=ROOT,specification=None):
 spec=specification if specification is not None else policy();item=spec['frozen_npc_baseline'];p=(Path(root)/item['file']).resolve()
 if not p.is_relative_to(Path(root).resolve()):raise ValueError('Baseline path escapes project')
 if hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Required NPC baseline is corrupt')
 v=json.loads(p.read_text());assert v['schema']==1 and v['source_commit']==spec['restore_commit']
 assert v['source_file_sha256']==spec['retired_maps']['/Game/Maps/Dev_TestMap_NPCMotionV2']['sha256']
 return v
