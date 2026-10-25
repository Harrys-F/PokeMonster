"""Read-only NPC source inventory; hashes protect originals, saves and pre-existing untracked files."""
from pathlib import Path
import hashlib,json,struct,subprocess
R=Path(__file__).resolve().parents[2];O=R/'Saved/ProjectRefinement/NPCExpansion'
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def glb(p):
 with p.open('rb') as f:
  magic,version,total=struct.unpack('<4sII',f.read(12));n,kind=struct.unpack('<II',f.read(8));j=json.loads(f.read(n))
 primitives=[v for m in j.get('meshes',[]) for v in m['primitives']]
 return dict(version=version,bytes=p.stat().st_size,sha256=digest(p),meshes=len(j.get('meshes',[])),materials=len(j.get('materials',[])),images=len(j.get('images',[])),skins=len(j.get('skins',[])),animations=len(j.get('animations',[])),vertices=sum(j['accessors'][v['attributes']['POSITION']]['count'] for v in primitives),triangles=sum(j['accessors'][v['indices']]['count']//3 for v in primitives),bounds=[{'min':j['accessors'][v['attributes']['POSITION']].get('min'),'max':j['accessors'][v['attributes']['POSITION']].get('max')} for v in primitives])
paths=sorted(p for p in (R/'Art/Characters/NPCs').rglob('*') if p.is_file() and 'Incoming' in p.parts)
models={str(p.relative_to(R)):glb(p) for p in paths if p.suffix.lower()=='.glb'}
untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=R).decode().split('\0');untracked=[x for x in untracked if x and not x.startswith('Tools/NPCExpansion/')]
protected={str(p.relative_to(R)):digest(p) for p in paths}
for rel in untracked:
 p=R/rel
 if p.is_file():protected[rel]=digest(p)
for p in (R/'Saved/SaveGames').rglob('*'):
 if p.is_file():protected[str(p.relative_to(R))]=digest(p)
for p in (R/'Content/Maps').glob('*.umap'):protected[str(p.relative_to(R))]=digest(p)
base=O/'Baseline.json'
if not base.exists():base.write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'protected':protected,'untracked':untracked},indent=2))
(O/'Incoming.json').write_text(json.dumps(models,indent=2))
print(json.dumps({'models':models,'protected_count':len(protected),'untracked':len(untracked)},indent=2))
