"""Verify unchanged baseline and originals; refresh only this QA package's hashes.

This script never stages files, changes refs or copies a save. Evidence stays Saved/.
"""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess

R = Path(__file__).resolve().parents[2]
D = R / 'Saved/ProjectRefinement/GameplayPraxisV1'
base = json.loads((D / 'Baseline.json').read_text())
manifest = 'Tools/DevelopmentEvidence/CoreFiles.json'


def sha(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=R, text=True).strip()


assert git('branch', '--show-current') == 'main'
assert git('remote', 'get-url', 'origin') == 'git@github.com:Harrys-F/PokeMonster.git'
files = {'Docs/GAMEPLAY_CONTROLLER_PRAXISTEST_V1_PRUEFBERICHT.md'}
for path in (R / 'Tools/GameplayPraxisV1').rglob('*'):
    if path.is_file() and '__pycache__' not in path.parts:
        assert path.suffix in ('.py', '.md', '.json'), ('Unexpected QA file', path)
        files.add(str(path.relative_to(R)))
assert not files.intersection(base['untracked'])
assert all((R / name).is_file() for name in files)

for name, original in base['protected'].items():
    path = R / name
    assert path.is_file(), ('Protected original missing', name)
    assert path.stat().st_size == original['bytes'], ('Protected size changed', name)
    assert sha(path) == original['sha256'], ('Protected hash changed', name)
for ref, original in base['backup_refs'].items():
    assert git('rev-parse', ref) == original, ('Backup ref changed', ref)

old = json.loads(git('show', base['head'] + ':' + manifest))
for name, original in old['files'].items():
    path = R / name
    assert path.is_file(), ('Existing core file missing', name)
    assert sha(path) == original['sha256'], ('Unexpected production change', name)

# Every untracked file must be either an original or part of this explicit package.
others = set(git('ls-files', '--others', '--exclude-standard').splitlines())
assert others - set(base['untracked']) <= files, ('Unassigned files', sorted(others - set(base['untracked']) - files))
assert set(base['untracked']) <= others, 'An originally untracked file was staged or removed'
core = json.loads((R / manifest).read_text())
assert set(core['files']) == set(old['files']) | (files & set(core['files'])), 'Unassigned core manifest entries'
for name in sorted(files):
    path = R / name
    core['files'][name] = {'bytes': path.stat().st_size, 'sha256': sha(path)}
core['files'] = dict(sorted(core['files'].items()))
core['generated_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
core['snapshot_kind'] = 'gameplay_controller_praxis_v1_verified'
(R / manifest).write_text(json.dumps(core, indent=2) + '\n')
files.add(manifest)
(D / 'PackageFiles.json').write_text(json.dumps(sorted(files), indent=2) + '\n')
result = {
    'passed': True,
    'baseline_head': base['head'],
    'prior_core_files': len(old['files']),
    'unchanged_prior_core_files': len(old['files']),
    'approved_existing_changes': [],
    'protected_files_verified': len(base['protected']),
    'protected_untracked': len(base['untracked']),
    'all_maps_and_user_save_unchanged': True,
    'backup_refs': base['backup_refs'],
    'package_files': len(files),
}
(D / 'Integrity.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
