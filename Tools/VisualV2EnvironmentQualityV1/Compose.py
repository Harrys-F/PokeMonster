"""Arrange genuine game-camera screenshots; preserve native pixels and source files.

Requires Pillow. Run after measurements. No generated scene content or color edits.
"""
import hashlib
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

R = Path(__file__).resolve().parents[2]
S = R / 'Saved/VisualV2EnvironmentQualityV1/Screenshots'
D = Path(sys.argv[1]) if len(sys.argv) > 1 else S.parent / 'Comparisons'
D.mkdir(parents=True, exist_ok=False)
try:
    font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 38)
    small = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 20)
except OSError:
    font = small = ImageFont.load_default()
factor_titles = {'MotionBlurOff': 'Bewegungsunschaerfe aus', 'BloomOff': 'Bloom aus',
                 'VSMRayCount2': 'VSM: zwei Schattenstrahlen', 'LumenIntegrate2': 'Lumen: Integration 2'}
manifest = []


def actual_capture(request):
    path = Path(request)
    if path.exists():
        return path
    # Unreal's Shot command appends a numeric suffix to preserve previous captures.
    matches = list(path.parent.glob(path.stem + '*.png'))
    assert len(matches) == 1, (str(path), [str(p) for p in matches])
    return matches[0]


for label, expected in [('VEQ1_Review_1280_1_75', (1280, 720)),
                        ('VEQ1_Review_2560_1_75', (2560, 1440)),
                        ('VEQ1_Review_2560_2_100', (2560, 1440))]:
    folder = S / label
    review = json.loads((folder / 'Review.json').read_text())
    assert not review['error'] and len(review['rows']) == 20
    for start in [0, 5, 10, 15]:
        a = review['rows'][start]
        original = actual_capture(a['request'])
        ia = Image.open(original).convert('RGB')
        assert ia.size == expected and tuple(a['viewport']) == expected
        for index in range(start + 1, start + 5):
            b = review['rows'][index]
            changed = actual_capture(b['request'])
            ib = Image.open(changed).convert('RGB')
            assert ib.size == ia.size and b['viewport'] == a['viewport']
            assert b['camera_rotation'] == a['camera_rotation'] and b['fov'] == a['fov'] == 35
            assert max(abs(x - y) for x, y in zip(a['camera_cm'], b['camera_cm'])) < .02
            name = label + '_' + a['site'] + '_' + b['condition']
            canvas = Image.new('RGB', (2 * ia.width, ia.height + 80), (24, 28, 27))
            canvas.paste(ia, (0, 80))
            canvas.paste(ib, (ia.width, 80))
            draw = ImageDraw.Draw(canvas)
            draw.text((24, 20), 'A: VisualV2-Kontrolle', font=font, fill='white')
            draw.text((ia.width + 24, 20), 'B: nur ' + factor_titles[b['condition']], font=font, fill='white')
            full = D / (name + '.png')
            canvas.save(full)
            thumbnail = canvas.resize((1280, round(canvas.height * 1280 / canvas.width)), Image.Resampling.LANCZOS)
            thumbnail.save(D / (name + '_Vorschau.jpg'), quality=94)
            record = {'output': str(full), 'sources': [str(original), str(changed)],
                      'sha256_sources': [hashlib.sha256(p.read_bytes()).hexdigest() for p in [original, changed]],
                      'source_extent': list(expected), 'camera_a': a['camera_cm'], 'camera_b': b['camera_cm'],
                      'condition': b['condition'], 'quality': review['quality'], 'percentage': review['percentage'],
                      'operation': 'Unscaled original RGB pixels side by side, caption outside scene. Separate JPEG thumbnail is resized.'}
            manifest.append(record)
            if label == 'VEQ1_Review_2560_2_100' and a['site'] == 'NPCWald':
                box = (1000, 600, 1800, 1400)
                ca, cb = ia.crop(box), ib.crop(box)
                detail = Image.new('RGB', (1600, 880), (24, 28, 27))
                detail.paste(ca, (0, 80))
                detail.paste(cb, (800, 80))
                draw = ImageDraw.Draw(detail)
                draw.text((20, 24), 'A: Kontrolle', font=font, fill='white')
                draw.text((820, 24), 'B: ' + factor_titles[b['condition']], font=small, fill='white')
                detail.save(D / (name + '_NPC_Detail.png'))
                manifest.append({'output': str(D / (name + '_NPC_Detail.png')), 'sources': record['sources'],
                                 'crop': list(box), 'operation': 'Unscaled native-pixel crop; captions outside scene.'})
(D / 'Comparisons.json').write_text(json.dumps(manifest, indent=2))
print('Comparison layouts:', len(manifest), '; source captures:', 60)
