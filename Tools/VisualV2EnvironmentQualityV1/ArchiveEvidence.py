"""Preserve completed evidence outside the repository, without removing Saved originals.

Run only after timing, gameplay and automation. Pass a new external destination.
"""
import hashlib
import json
import shutil
import sys
import zipfile
from pathlib import Path

R = Path(__file__).resolve().parents[2]
S = R / 'Saved/VisualV2EnvironmentQualityV1'
P = R / 'Saved/EnvironmentPerfV1'
D = Path(sys.argv[1]).resolve()
assert not D.is_relative_to(R), 'Optional evidence belongs outside the slim repository'
assert len(json.loads((S / 'MatrixValidation.json').read_text())) == 12
assert json.loads((S / 'FootTest/FootTest.json').read_text())['passed']
assert json.loads((S / 'SaveRestored.json').read_text())['restored']
D.mkdir(parents=True, exist_ok=False)
manifest = []


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as file:
        for chunk in iter(lambda: file.read(4 * 1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def copied(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    assert not target.exists()
    shutil.copy2(source, target)
    digest = sha256(source)
    assert sha256(target) == digest
    manifest.append({'source': str(source), 'copy': str(target), 'bytes': source.stat().st_size,
                     'sha256': digest, 'source_removed': False})


for source in sorted((S / 'Screenshots').rglob('*')):
    if source.is_file():
        copied(source, D / 'Screenshots' / source.relative_to(S / 'Screenshots'))
for source in sorted((S / 'FootTest').glob('*.png')):
    copied(source, D / 'FootScreenshots' / source.name)
for name in ['Measurements.json', 'MatrixValidation.json', 'FactorResults.json',
             'FactorSummary.csv', 'IndividualMeasurements.csv', 'VOLLSTAENDIGE_MESSWERTE.md',
             'GPUCounterAvailability.json', 'MapCopyAudit.json',
             'FootGraphics.json', 'FootCvarsRestored.json', 'SaveRestored.json', 'Thermal.jsonl']:
    copied(S / name, D / 'Data' / name)
copied(S / 'FootTest/FootTest.json', D / 'Data/FootTest.json')
copied(S / 'FootTest/FootProgress.json', D / 'Data/FootProgress.json')

raw = list(P.glob('VEQ1_*_Frames.csv')) + list(P.glob('VEQ1_*_Segments.csv'))
raw += list(P.glob('VEQ1_*_Settings.txt')) + list(P.glob('VEQ1_*_Done.txt'))
raw += list(S.glob('VEQ1_*_RuntimeCvars.json'))
raw += list((R / 'Saved/Profiling/CSV').glob('ENV1_VEQ1_*.csv'))
raw += [S / 'FootTest/FootFrames.jsonl']
raw += list((R / 'Tools/VisualV2EnvironmentQualityV1/Plans').glob('*.tsv'))
with zipfile.ZipFile(D / 'RawMeasurements.zip', 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=3) as archive:
    for source in sorted(set(raw)):
        archive.write(source, str(source.relative_to(R)))
(D / 'EvidenceManifest.json').write_text(json.dumps({'copies': manifest,
    'raw_archive_entries': len(set(raw)), 'source_files_removed': False}, indent=2))
print('Preserved:', len(manifest), 'files;', len(set(raw)), 'raw archive entries')
