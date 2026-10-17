"""Required source validation and explicit optional review archive access; stdlib only.
Never deletes, restores, rewrites manifests, or modifies source files.
"""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, os, shutil, sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def _inside(path, base):
    try: path.relative_to(base); return True
    except ValueError: return False

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(4*1024*1024),b''):
            h.update(block)
    return h.hexdigest()

def safe_name(name):
    name=str(name)
    p=PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or '\\' in name or not p.parts:
        raise ValueError('Only project-relative manifest paths are accepted: '+name)
    return p.as_posix()

def manifest():
    return json.loads((HERE/'EvidenceManifest.json').read_text())['files']

def resolve_optional(name, archive=None):
    """Return a verified optional input, or None. Unknown paths fail, not skip."""
    name=safe_name(name); item=manifest().get(name)
    if item is None:
        raise KeyError('Not a classified optional review input: '+name)
    local=ROOT/name
    candidates=[local]
    configured=archive or os.environ.get('POKEMONSTER_EVIDENCE_ARCHIVE')
    if configured:
        base=Path(configured).expanduser().resolve()
        archived=(base/item['archive_object']).resolve()
        if not _inside(archived, base):
            raise ValueError('Unsafe archive object path')
        candidates.append(archived)
    for path in candidates:
        if path.is_file():
            if path.stat().st_size!=item['bytes'] or digest(path)!=item['sha256']:
                raise ValueError('Evidence hash/size mismatch; refusing input: '+str(path))
            return path
    return None

def validate_core(root=ROOT, specification=None):
    specification=specification or json.loads((HERE/'CoreFiles.json').read_text())['files']
    missing=[];changed=[]
    for name,item in specification.items():
        name=safe_name(name);p=Path(root)/name
        if not p.is_file():missing.append(name)
        elif p.stat().st_size!=item['bytes'] or digest(p)!=item['sha256']:changed.append(name)
    return {'check':'current_required_core_snapshot_not_historical_session','checked':len(specification),'missing_required':missing,'changed_required':changed,'passed':not missing and not changed}

def review_preflight(script):
    name=Path(script).resolve().relative_to(ROOT).as_posix()
    policy=json.loads((HERE/'ReviewPolicies.json').read_text())[name]
    # Original scripts expect an original directory tree. An external object archive
    # is NOT silently materialized into the project; use a separate replay directory.
    missing=[p for p in policy['optional_inputs'] if not (ROOT/p).is_file()]
    if missing:
        print('REVIEW_NOT_EXECUTED: '+name+'; '+str(len(missing))+' optional historical inputs are absent. This is NOT a test pass.',file=sys.stderr)
        print('Game/build/current automation do not require these files. Generate fresh captures with the existing Capture/RunFinalRecording tools, or materialize verified archive inputs into a SEPARATE replay tree. See Tools/DevelopmentEvidence/README.md.',file=sys.stderr)
        if os.environ.get('POKEMONSTER_REQUIRE_EVIDENCE')=='1':
            raise SystemExit(2)
        raise SystemExit(0)

def current_guard():
    result=validate_core()
    print(json.dumps(result,indent=2))
    print('Current core snapshot only. Historical review/session guards were NOT run; POKEMONSTER_RUN_HISTORICAL_GUARD=1 explicitly selects their original, session-dependent checks.')
    raise SystemExit(0 if result['passed'] else 1)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest='command',required=True)
    commands.add_parser('validate-core');commands.add_parser('status')
    get=commands.add_parser('get');get.add_argument('path');get.add_argument('--archive')
    materialize=commands.add_parser('materialize');materialize.add_argument('prefix');materialize.add_argument('--archive',required=True);materialize.add_argument('--destination',required=True)
    args=parser.parse_args()
    if args.command=='validate-core':
        result=validate_core();print(json.dumps(result,indent=2));return 0 if result['passed'] else 1
    if args.command=='status':
        files=manifest();missing=[p for p in files if not (ROOT/p).is_file()]
        print(json.dumps({'optional_inputs':len(files),'missing_optional':len(missing),'not_a_build_or_game_failure':True,'review_replay_not_executed':True},indent=2));return 0
    if args.command=='get':
        result=resolve_optional(args.path,args.archive)
        print(json.dumps({'path':args.path,'verified_input':str(result) if result else None,'optional_unavailable':result is None}));return 0 if result else 2
    prefix=safe_name(args.prefix).rstrip('/')
    dest=Path(args.destination).expanduser().resolve()
    saved=(ROOT/'Saved').resolve()
    if _inside(dest, ROOT) and not _inside(dest, saved):
        parser.error('Archive materialization is allowed only outside the project or under ignored Saved/.')
    selected={p:x for p,x in manifest().items() if p==prefix or p.startswith(prefix+'/')}
    if not selected:parser.error('No explicit manifest input matches this prefix')
    sources={p:resolve_optional(p,args.archive) for p in selected}
    if any(p is None for p in sources.values()):raise FileNotFoundError('Archive incomplete; nothing copied')
    for name in selected:
        target=dest/name
        if target.exists() or target.is_symlink():raise FileExistsError('No overwrite permitted: '+str(target))
        ancestor=target.parent
        while ancestor!=dest:
            if ancestor.is_symlink():raise ValueError('Symlink in output path: '+str(ancestor))
            ancestor=ancestor.parent
    for name,src in sources.items():
        target=dest/name;target.parent.mkdir(parents=True,exist_ok=True)
        with src.open('rb') as source,target.open('xb') as output:shutil.copyfileobj(source,output)
        if digest(target)!=selected[name]['sha256']:raise ValueError('Copy mismatch: '+str(target))
    print(json.dumps({'materialized_optional_files':len(selected),'destination':str(dest),'source_project_unchanged':True}));return 0

if __name__=='__main__':
    raise SystemExit(main())
