"""Human-readable full results; no quality approval inferred from numerical checks."""
import json
from pathlib import Path

R = Path(__file__).resolve().parents[2]
O = R / 'Saved/VisualV2EnvironmentQualityV1'
rows = json.loads((O / 'FactorResults.json').read_text())
assert len(rows) == 144


def n(value):
    return '—' if value is None else f'{value:.2f}'


def pair(row, key):
    return n(row['control_' + key]) + ' → ' + n(row['candidate_' + key])


out = ['# Vollständige Einzelfaktor-Ergebnisse', '',
       'A = Mittel der flankierenden Kontrollmediane pro Wiederholung; B = Einzelmaßnahme. '
       'Tabellenwerte sind anschließend Mediane der drei Wiederholungen. Zeiten in ms. '
       'Delta-Spanne nennt alle drei Framezeit-Differenzen B−A als Min/Max; negativ ist schneller. '
       'P95 ist der Median der wiederholungsbezogenen P95-Werte, kein gepooltes Gesamt-P95. '
       'GPU-Pässe nicht addieren. Fehlende bzw. konstante Nullzähler erscheinen als —.', '']
for factor in ['MotionBlurOff', 'BloomOff', 'VSMRayCount2', 'LumenIntegrate2']:
    out += ['## ' + factor, '',
            '| Modus | Ausgabe / Qualität / % | Ort | FPS A → B | Frame A → B | P95 A → B | GPU A → B | ShadowProjection A → B | ShadowDepths A → B | ΔFrame Min … Max |',
            '|---|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for row in [row for row in rows if row['factor'] == factor]:
        config = f"{row['width']}×{row['height']} / {'Medium' if row['quality'] == 1 else 'High'} / {row['percentage']}"
        span = row['delta_range_ms']
        out.append('| ' + ' | '.join([row['mode'], config, row['site'], pair(row, 'fps'),
                    pair(row, 'ms'), pair(row, 'p95_ms'), pair(row, 'GPUTime'),
                    pair(row, 'GPU/ShadowProjection'), pair(row, 'GPU/ShadowDepths'),
                    n(span[0]) + ' … ' + n(span[1])]) + ' |')
    out.append('')
(O / 'VOLLSTAENDIGE_MESSWERTE.md').write_text('\n'.join(out) + '\n')
print('Formatted', len(rows), 'comparisons')
