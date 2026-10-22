"""Validate the completed matrix and summarize independent factors against bracketing controls.

Run after all GPU measurements, never concurrently with a timing session.
Missing counters remain missing; nested GPU passes are not added together.
"""
import csv
import json
import re
import statistics as st
from pathlib import Path

R = Path(__file__).resolve().parents[2]
O = R / 'Saved/VisualV2EnvironmentQualityV1'
P = R / 'Saved/EnvironmentPerfV1'
CONFIGS = [(1280, 720, 1, 75), (1280, 720, 1, 100),
           (2560, 1440, 1, 75), (2560, 1440, 1, 100),
           (2560, 1440, 2, 75), (2560, 1440, 2, 100)]
FACTORS = ['MotionBlurOff', 'BloomOff', 'VSMRayCount2', 'LumenIntegrate2']
COUNTERS = ['GPUTime', 'GameThreadTime', 'RenderThreadTime',
            'GPU/ShadowProjection', 'GPU/ShadowDepths', 'GPU/PostProcessing',
            'GPU/MotionBlur', 'GPU/LumenScreenProbeGather',
            'GPU/LumenIrradianceFieldGather', 'GPU/Basepass', 'GPU/Unaccounted']


def counter(row, name):
    value = row.get('csv', {}).get(name)
    if not value or value['all_zero']:
        return None
    # Near-zero PIE render-thread counters were not credible in earlier captures.
    if name == 'RenderThreadTime' and value['median'] < .05:
        return None
    return value['median']


def mean_valid(values):
    return st.mean(values) if values and all(v is not None for v in values) else None


def median_valid(values):
    return st.median(values) if values and all(v is not None for v in values) else None


def main():
    measurements = json.loads((O / 'Measurements.json').read_text())
    validation = []
    results = []
    individual = []
    for mode in ['PIE', 'Standalone']:
        for number, (width, height, quality, percentage) in enumerate(CONFIGS, 1):
            label = f'VEQ1_{mode}_{number}'
            assert (P / (label + '_Done.txt')).read_text() == 'Complete', label
            rows = measurements[label]
            assert len(rows) == 54, (label, len(rows))
            expected = [width, height] * 3 + [width * percentage // 100, height * percentage // 100]
            for row in rows:
                assert row['extent'] == [expected], (label, row['segment'], row['extent'])
                assert row['fractions'] == [[percentage / 100, 1.0]], (label, row['fractions'])
                assert row['samples'] >= 20, (label, row['segment'], row['samples'])
                for field, value in [('pitch', -50), ('yaw', -45), ('fov', 35)]:
                    assert all(abs(v - value) < .001 for v in row['camera'][field]), (label, field)
                assert int(row['quality']) == quality and int(row['percentage']) == percentage
                individual.append({'label': label, 'mode': mode, 'width': width, 'height': height,
                                   **{k: row[k] for k in ['segment', 'site', 'condition', 'repeat',
                                                        'samples', 'median_fps', 'median_ms', 'p95_ms']},
                                   **{k: counter(row, k) for k in COUNTERS}})
            cameras = {}
            for site in ['Dorf', 'Wald', 'Weg']:
                subset = [row for row in rows if row['site'] == site]
                assert len(subset) == 18
                for field in ['camera_x', 'camera_y', 'camera_z']:
                    values = [v for row in subset for v in row['camera'][field]]
                    assert max(values) - min(values) < .2, (label, site, field, min(values), max(values))
                cameras[site] = subset[0]['camera']
                for factor in FACTORS:
                    pairs = []
                    for repeat in ['1', '2', '3']:
                        group = [row for row in subset if row['repeat'] == repeat]
                        controls = [row for row in group if row['condition'] == 'Control']
                        candidate = [row for row in group if row['condition'] == factor]
                        assert len(controls) == 2 and len(candidate) == 1
                        controls.sort(key=lambda row: row['segment'])
                        candidate = candidate[0]
                        assert controls[0]['segment'] < candidate['segment'] < controls[1]['segment']
                        base_ms = st.mean(row['median_ms'] for row in controls)
                        pair = {'repeat': int(repeat), 'control_ms': base_ms,
                                'candidate_ms': candidate['median_ms'],
                                'delta_ms': candidate['median_ms'] - base_ms,
                                'control_p95_ms': st.mean(row['p95_ms'] for row in controls),
                                'candidate_p95_ms': candidate['p95_ms'],
                                'control_drift_ms': controls[1]['median_ms'] - controls[0]['median_ms'],
                                'control_segments': [row['segment'] for row in controls],
                                'candidate_segment': candidate['segment']}
                        for metric in COUNTERS:
                            pair['control_' + metric] = mean_valid([counter(row, metric) for row in controls])
                            pair['candidate_' + metric] = counter(candidate, metric)
                        pairs.append(pair)
                    result = {'mode': mode, 'config': number, 'width': width, 'height': height,
                              'quality': quality, 'percentage': percentage, 'site': site, 'factor': factor,
                              'runs': pairs}
                    for key in pairs[0]:
                        if key in ['repeat', 'control_segments', 'candidate_segment']:
                            continue
                        result[key] = median_valid([pair[key] for pair in pairs])
                    result['control_fps'] = 1000 / result['control_ms']
                    result['candidate_fps'] = 1000 / result['candidate_ms']
                    result['delta_range_ms'] = [min(p['delta_ms'] for p in pairs), max(p['delta_ms'] for p in pairs)]
                    results.append(result)
            validation.append({'label': label, 'segments': len(rows), 'output': [width, height],
                               'derived_internal': expected[-2:], 'verified_camera': cameras,
                               'window_extents': [row['window'] for row in rows],
                               'active_window_fraction': [row.get('active_window_fraction') for row in rows]})
    assert len(individual) == 648 and len(results) == 144
    (O / 'MatrixValidation.json').write_text(json.dumps(validation, indent=2))
    (O / 'FactorResults.json').write_text(json.dumps(results, indent=2))
    for name, rows in [('IndividualMeasurements.csv', individual), ('FactorSummary.csv', results)]:
        fields = [key for key in rows[0] if key != 'runs']
        with (O / name).open('w') as file:
            writer = csv.DictWriter(file, fields, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rows)
    print('Validated:', len(individual), 'segments;', len(results), 'independent factor comparisons')


if __name__ == '__main__':
    main()
