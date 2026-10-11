# V3 – Blattgruppen-Atlas

- Datei: `Textures/T_WLA_FoliageGroups_V3.png`, RGBA, 1254 × 1254 px.
- Erzeugt am 11. Oktober 2026 mit dem integrierten ImageGen-Werkzeug; keine externen Downloads.
- Vier gemalte Blattgruppen in einem Atlas; keine einzelne Großblatt-Textur.
- Alpha bleibt erhalten. Unreal normalisiert beim Texture-Build auf 2048 × 2048, erzeugt Mips und erhält die Alpha-Abdeckung bei 0,45. Die Quelldatei wird dabei nicht verändert.
- Vorhandene Rinde `T_WLA_Bark.png` und bestehende Materialinstanz `MI_WLA_Bark` werden unverändert wiederverwendet.

## Generierungsprompt

```text
Use case: stylized-concept. Asset type: one reusable 2x2 RGBA foliage-cluster atlas for curved leaf cards in a modern hand-painted fantasy 2.5D game. Square composition on a genuinely TRANSPARENT background. Four separate irregular dense clusters, one in each quadrant, each completely contained with generous transparent gutters and margin; no text, no frame, no labels, no trees, no trunk, no ground. Each cluster is a spray of roughly 25-45 SMALL overlapping lobed oak leaves; little twig hints only, no individually huge leaves. Distinct silhouettes: broad fan upper-left, longer diagonal spray upper-right, compact scalloped cluster lower-left, loosely arcing spray lower-right. Dense leaf coverage in their centers, delicate serrated/lobed organic edges and small natural holes only near edges. Beautiful high-resolution hand-painted fantasy RPG illustration, brush-made soft gradients and precise readable small leaf forms, harmonious muted moss/olive/sage greens, warm yellow-green highlights and deep blue-green recesses, subtle vein marks, a little asymmetry and varied leaf orientations. Soft diffuse light, no glossy highlights, no baked hard directional shadow, no black outline, no photographic surface, no pixel art, no geometric spheres, no thick bush ball. Each cluster should look like a small realistic branch spray of many oak leaves seen from a slightly elevated 3/4 view; these atlas clusters will overlap on curved 3D cards to form a broad dense ancient oak canopy and wild shrubs. Actual transparency outside the leaves; no checkerboard painted into the image. This is a production texture atlas, not a presentation sheet.
```
