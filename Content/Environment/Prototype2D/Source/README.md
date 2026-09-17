# Prototype2D – eigene visuelle Platzhalter

Generiert am 17.09.2026 mit dem eingebauten Imagegen-Werkzeug; keine Downloads oder Marketplace-Inhalte. Original-PNGs mit Alpha bleiben unverändert in Source. Die vier Texturen werden von allen Sprite-Instanzen gemeinsam genutzt. Importlimit 1024; die 1254-Pixel-Quellen ergeben bei dieser Mip-Einstellung effektiv 627 Pixel. Quellregion und Pivot beziehen sich stets auf die Originalauflösung.

## Assets

- Textures/T_Oak, T_Bush, T_Rock, T_Hut
- Sprites/S_Oak, S_Bush, S_Rock, S_Hut
- Materials/M_PaintedGround, M_SoftPath, M_SoftWater, M_SoftPond, M_ContactWash

Sprites: MaskedUnlitSpriteMaterial aus Paper2D, keine Kollision oder geworfenen Schatten. Feste Ausrichtung: Pitch 0, Yaw 45, Roll -55. Maßstab und leichte Farbdämpfung liegen auf den Map-Instanzen. Bei später geändertem Kamerawinkel die Ausrichtung erneut prüfen.

Outliner: Prototype2D/Boden, Wege, Wasser, Vegetation, Gebaeude, Vordergrund, Felsen, Collision, Archived3D. Archived3D enthält die erhaltenen bisherigen Actors; unsichtbare Meshes behalten ihre ursprünglichen Kollisionen. Brücke und begehbare Höhenstufen bleiben einfache Geometrie. Neue Oberflächen und Kontaktflächen sind rein visuell.

## Generierungsprompts

### Oak

Single transparent painted oak sprite. Elevated 55 degree view. Organic rounded moss/olive/sage foliage, short visible branching trunk, soft gradients, clean silhouette, no ground, no shadow, no text or pixel art.

### Bush

Use case: stylized-concept. Single transparent game sprite for modern painted 2D/2.5D fantasy top-down RPG: one low broad leafy woodland shrub, small rounded organic clumps, moss sage olive foliage, occasional delicate leaf highlights. Clean sophisticated hand-painted illustration, soft blended gradients, naturally muted colors, subtle shaded underside. Elevated 55-degree view, three-quarter view if building. Complete silhouette centered with 5 percent clear margins, ground contact at bottom center. True transparent alpha background, no ground or cast shadow. No text, no pixel art, no 3D rendering. 1024x1024.

### Rock

Use case: stylized-concept. Single transparent game sprite for modern painted 2D/2.5D fantasy top-down RPG: one broad weathered grey slate boulder with rounded natural edges, moss patches and subtle fine stone detail, no angular low-poly facets. Clean sophisticated hand-painted illustration, soft blended gradients, naturally muted colors, subtle shaded underside. Elevated 55-degree view, three-quarter view if building. Complete silhouette centered with 5 percent clear margins, ground contact at bottom center. True transparent alpha background, no ground or cast shadow. No text, no pixel art, no 3D rendering. 1024x1024.

### Hut

Use case: stylized-concept. Single transparent game sprite for modern painted 2D/2.5D fantasy top-down RPG: one entire small medieval fantasy cottage, warm cream plaster and aged oak timber frame, muted blue slate gabled roof, small chimney, wooden front door and two windows, charming modest proportions, no surroundings. Clean sophisticated hand-painted illustration, soft blended gradients, naturally muted colors, subtle shaded underside. Elevated 55-degree view, three-quarter view if building. Complete silhouette centered with 5 percent clear margins, ground contact at bottom center. True transparent alpha background, no ground or cast shadow. No text, no pixel art, no 3D rendering. 1024x1024.

