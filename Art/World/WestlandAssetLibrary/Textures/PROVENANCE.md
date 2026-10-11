# Gemalte Materialquellen

Neue Bilder wurden mit dem eingebauten Imagegen-Werkzeug am 10.10.2026 erzeugt.
Es wurden keine Marketplace-, Foto- oder ROM-Texturen heruntergeladen.

- `T_WLA_PaintedAtlas_Source.png`: ursprüngliche, unveränderte 2×2-Quelle: Eichenrinde, Birkenrinde, Blattflächen, Stroh. Tatsächliche Ausgabe 1254×1254 Pixel.
- `T_WLA_Bark.png`, `T_WLA_Birch.png`, `T_WLA_Leaf.png`, `T_WLA_Straw.png`: technische, unveränderte Ausschnitte der vier Quadranten, je 627×627 Pixel. Keine nachträgliche Bemalung oder erfundene Auflösung.
- `T_WLA_LeafSummer.png`: separate korrigierte Sommergrün-Quelle. Die erste gelbliche Blatttextur bleibt als Ausgangsstand erhalten und wird von den fertigen Blattmaterialien nicht verwendet.

Prompts: flache orthografische, handgemalte Fantasy-Diffusetexturen; organische Rindenrillen, horizontale Birkennarben, zurückhaltendes Blattgrün mit weichen Blattmassen und Blattadern, trockene Strohfasern. Keine Schrift, Materialkugeln, Perspektive, Fototexturen oder Pixel-Art. Die Sommerkorrektur verlangt ausdrücklich Jade-/Moos-/Salbeigrün statt Herbstgelb und zusammenhängende malerische Blattgruppen.

Vorhandene, unverändert referenzierte Projektquellen: `Art/HealingHouse/Textures/QualityV2/T_HH_PaintedWood.png` und `T_HH_PaintedStone.png`.
UV0 ist eine wiederholbare Material-/Trim-Projektion mit bewusst überlagerten Blatt-UVs; kein eindeutiger Lightmap-Atlas. Unreal generiert separat UV1. Blattflächen sind echte gebogene Geometrie und verwenden keine Alpha-Masken.

## Art Quality V2 – Blattfamilien

Am 10.10.2026 mit dem eingebauten Imagegen-Werkzeug erzeugt:

- `T_WLA_LeafAtlas_V2_Source.png`: unveränderte 1254×1254-Pixel-Quelle mit vier Blattoberflächen.
- `T_WLA_LeafOak_V2.png`, `T_WLA_LeafBirch_V2.png`, `T_WLA_LeafOrchard_V2.png`, `T_WLA_LeafFern_V2.png`: jeweils unveränderte technische Quadrantenausschnitte, 627×627 Pixel. Kein künstliches Upscaling.

Promptinhalt: flache handgemalte Fantasy-Blattoberflächen in vier Materialfeldern für Eiche, Birke, Obstbaum und Farn; zentrale Blattadern und feine Nebenadern, zurückhaltendes Moos-/Oliv-/Salbeigrün, weiche Pigmentverläufe, sichtbare Pinselstruktur. Keine Fototextur, Schrift, Materialkugel, perspektivische Darstellung oder fertig gemalten Kronencluster. Die Blattform und Kontur entstehen aus der Geometrie; keine Alpha-Masken.

Vier neue Materialinstanzen verwenden den vorhandenen opaken, zweiseitigen Blattmaster. Die bisherigen Rinden-, Holz- und Steinquellen bleiben unverändert. Gepackte Bilder in der V2-Blenderquelle wurden beim Wiederöffnen geprüft.
