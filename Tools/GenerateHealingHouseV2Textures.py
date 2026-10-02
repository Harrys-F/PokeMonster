"""Create reproducible, painted-style architectural textures without downloads.

Run with the bundled Python/Pillow runtime. Sources remain outside Content;
Unreal imports the seven images into the existing HealingHouse hierarchy.
"""
from pathlib import Path
import math
import random
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'Art/HealingHouse/Textures/V2'
DEST.mkdir(parents=True, exist_ok=True)
PALETTE = {'Plaster': (216, 198, 158), 'Wood': (143, 96, 52),
           'Timber': (82, 53, 33), 'Stone': (150, 150, 130),
           'Roof': (175, 86, 53), 'Metal': (68, 78, 70),
           'Glass': (231, 179, 78)}

for index, (name, base) in enumerate(PALETTE.items()):
    path = DEST / ('T_HH_V2_' + name + '.png')
    if path.exists():
        raise RuntimeError('Preserve existing texture: ' + str(path))
    size = 1024 if name == 'Roof' else 512
    rng = random.Random(20261002 + index)
    field = Image.new('RGB', (32, 32))
    field.putdata([tuple(max(0, min(255, c + rng.randrange(-11, 12))) for c in base)
                   for _ in range(32 * 32)])
    im = field.resize((size, size), Image.Resampling.BICUBIC)
    draw = ImageDraw.Draw(im)
    if name == 'Roof':
        # Eight offset courses of broad rounded shingles; soft highlights read
        # at the production camera, unlike subpixel individual roof geometry.
        cell, course = size // 8, size // 8
        for row in range(-1, 9):
            for col in range(-1, 9):
                x = col * cell + (cell // 2 if row % 2 else 0)
                y = row * course
                shift = rng.randint(-12, 12)
                color = tuple(c + shift for c in base)
                draw.rounded_rectangle((x + 3, y + 2, x + cell - 3, y + course - 1),
                                       radius=14, fill=color, outline=(110, 61, 43), width=5)
                draw.line((x + 14, y + 12, x + cell - 15, y + 12),
                          fill=(203 + shift, 121 + shift, 75 + shift), width=7)
                draw.line((x + 16, y + course - 12, x + cell - 16, y + course - 12),
                          fill=(145 + shift, 73 + shift, 48 + shift), width=5)
                for vein in (36, 75, 103):
                    draw.line([(x + vein + int(math.sin(j / 20) * 3), y + j)
                               for j in range(25, course - 20, 5)],
                              fill=(164 + shift, 81 + shift, 51 + shift), width=2)
    elif name in ('Wood', 'Timber'):
        plank = size // 4
        for i in range(4):
            offset = rng.randint(-9, 9)
            draw.rectangle((i * plank + 2, 0, (i + 1) * plank - 2, size),
                           fill=tuple(c + offset for c in base))
            draw.line((i * plank + 3, 0, i * plank + 3, size),
                      fill=tuple(max(0, c - 25) for c in base), width=4)
            for k in range(10):
                x = i * plank + rng.randrange(10, plank - 10)
                draw.line([(x + int(5 * math.sin(j / 65 + k)), j)
                           for j in range(0, size + 8, 8)],
                          fill=tuple(max(0, c + rng.choice((-13, 8))) for c in base), width=2)
            if name == 'Wood':
                cx, cy = i * plank + 65, 150 + i * 72
                for radius in (7, 14, 23):
                    draw.ellipse((cx - radius / 2, cy - radius * 2,
                                  cx + radius / 2, cy + radius * 2),
                                 outline=tuple(c - 20 for c in base), width=2)
    elif name == 'Stone':
        # Broad tonal islands rather than photographic/gritty microdetail.
        for _ in range(45):
            x, y = rng.randrange(size), rng.randrange(size)
            w, h = rng.randrange(30, 110), rng.randrange(20, 75)
            shift = rng.randint(-14, 14)
            draw.ellipse((x, y, x + w, y + h), fill=tuple(c + shift for c in base))
        im = im.filter(ImageFilter.GaussianBlur(9))
    elif name == 'Glass':
        for y in range(size):
            highlight = int(21 * (1 - y / size))
            draw.line((0, y, size, y), fill=tuple(min(255, c + highlight) for c in base))
        for x in range(-size, size, 130):
            draw.line((x, 0, x + size, size), fill=(243, 204, 116), width=7)
    elif name == 'Plaster':
        im = im.filter(ImageFilter.GaussianBlur(5))
    im = im.filter(ImageFilter.GaussianBlur(.65))
    im.save(path, optimize=True)
    print(path.relative_to(ROOT))
