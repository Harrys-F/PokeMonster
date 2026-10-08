# Young Trainer – ClothingFeet V1 Prüfbericht

Stand: 7. Oktober 2026. Ausschließlich Kleidung, Halstuch und barfüßige Fußform.

## Ausgangspunkt und Dateisicherheit

- HEAD: `58793f8b3bb563548cc6c18b6c72fa27ef4aed1d` – `Character: checkpoint Young Trainer head form V6`.
- Arbeitsbaum zu Beginn sauber. V6 bleibt verbindlicher Ausgangspunkt und wurde nicht überschrieben.
- Ausgabe: `Art/Characters/YoungTrainer/Source/YoungTrainer_ClothingFeet_V1.blend`.
- Ausschließliche Bildreferenz: `Reference/BarefootFinal/Player_Barefoot_Turnaround.png`.
- 992 vorhandene, nicht ignorierte Projektdateien wurden vor und nach der Arbeit per SHA-256 verglichen: alle bytegleich.
- Neue aktive Collection `YTCF_Player`; V6-Objekte bleiben unverändert als ausgeblendeter Vergleichsstand in der neuen Datei erhalten. Elf bereits ausgerichtete und gesperrte Bildreferenzen bleiben erhalten.
- Zwischenstände und Reviewbilder liegen ausschließlich unter dem ignorierten `Saved/YoungTrainerClothingFeetV1`. Kein Unreal-Export.

## Formänderungen

### Halstuch

Der bisherige massive, eher kantige Kragen wurde in der neuen aktiven Figur durch sechs geschlossene, geglättete Stoffformen ersetzt: drei weich verlaufende Halslagen, vorderer Stoffbogen, überlappende Falte und seitliches hängendes Ende. Höhen, Breiten und Verlauf sind asymmetrisch. Die Halslagen fallen vorne ab, statt als gleichmäßige Ringe zu verlaufen. Das seitliche Ende bleibt aus der erhöhten Perspektive sichtbar.

In der Silhouettenprüfung fiel zunächst ein Abstand am Ansatz des seitlichen Endes auf. Dessen obere Reihen wurden näher an die Halslagen geführt und der gespeicherte Stand erneut gerendert und geprüft. Bestehendes rotes Vorschau-Material wiederverwendet; keine Materialverfeinerung.

### Hemd und Ärmel

Lockerere Torsoform und rundere Schulterübergänge. Die Ärmel erhalten etwas mehr Volumen sowie breite, leichte Bündelungen vor den hochgerollten Manschetten. Redundante alte Manschettenschalen wurden ausschließlich aus der neuen Hemdkopie entfernt; die sichtbaren gerollten Ärmelabschlüsse bleiben bestehen. Der überlange mittige Hemdzipfel wurde kürzer und leicht asymmetrisch.

### Weste, Hose, Gürtel und Taschen

Die offene Weste bleibt blau und besitzt weiterhin längere untere Enden. Die überbreite, mantelartige Ausladung wurde reduziert, der untere Verlauf körpernäher und leicht unregelmäßig gestaltet. Bestehende Ornamente wurden mit der Form bewegt; keine neuen hinzugefügt.

Die Hose bleibt weit an Oberschenkeln und Knien und läuft oberhalb der nackten Knöchel enger aus. Breite schräge Falten und unterschiedliche linke/rechte Verläufe reduzieren die Spiegelgleichheit. Das Gesamtvolumen wurde nur moderat verändert.

Die vorhandenen Taschen sind kleiner, näher an Hüfte und Gürtel, unterschiedlich groß und auf verschiedenen Höhen angeordnet. Der Taillengürtel liegt etwas ruhiger und folgt weiterhin schräg der Hüfte. Keine zusätzlichen Taschen oder Beschläge.

### Barfüßige Hobbit-Füße

Die verbundenen V6-Fußvolumen mit jeweils fünf Zehen wurden erhalten und lokal verformt. Kein Neubau aus Schuhformen. Vorderfüße etwas breiter, Zehenpolster flacher und weniger kugelig, Gesamtlänge moderat kürzer; Fersen und ein leichtes mediales Gewölbe bleiben vorhanden. Die große Zehe ist breiter als die übrigen. Die Außenrotation wurde rechts von 10° auf 9°, links von −28° auf −21° beruhigt.

| Lokale Fußmaße, je Fuß | V6 | ClothingFeet V1 |
| --- | ---: | ---: |
| Länge | 28,53 cm | 26,83 cm |
| Breite | 13,46 cm | 13,88 cm |
| Zehen | 5 | 5 |
| Tiefster Sohlenpunkt | 0 cm | 0 cm |

Die Maße wurden ohne die unterschiedliche Außenrotation im lokalen Fußsystem bestimmt. Die Fußmesh-Höhe von ca. 21,7 cm enthält den nackten Knöchel/Unterschenkel und ist keine anatomische Fußhöhe. Beide Fußsohlen bleiben auf Z = 0. Keine sichtbaren Schuh-, Stiefel-, Sockengeometrien oder Schuhsohlen in der aktiven Figur.

## Messbare Kleidungssilhouette

Evaluierte Bounds enthalten vorhandene Bekleidungsornamente; sie sind keine Körpermessungen.

| Bauteil | V6 | V1 |
| --- | ---: | ---: |
| Weste, gesamte Breite | 44,72 cm | 38,13 cm |
| Weste, tiefster Punkt über Boden | 43,77 cm | 50,92 cm |
| Hemd, tiefster Punkt über Boden | 51,02 cm | 58,80 cm |
| Taschen, gesamte Breite | 44,49 cm | 40,58 cm |

Die Gesamthöhe bleibt 1,399999976 m, also 1,40 m innerhalb numerischer Genauigkeit. Kopf, Gesicht, Augen, Ohren, Ausdruck und Haare sind geometrisch exakt V6. Körper, Hände, Rucksack, Bettrolle, Ausrüstung und Anhänger einschließlich Grundposition sind ebenfalls unverändert.

## Vergleichsansichten und Ergebnis

Erzeugt und visuell geprüft: Front Orthographic, Blender Right Orthographic, beide Sheet-Seiten, Back Orthographic, beide vorderen und hinteren Dreiviertelansichten sowie erhöhte Ansichten aus acht Richtungen. Zusätzlich Nahansicht beider Füße, isolierte Fuß-Draufsicht, Kleidungsnahansicht und dunkle Silhouetten aus vier Richtungen.

Die Figur blickt nach −Y. Die rechte Sheet-Seite entspricht daher einer Kamera von −X; Blender Right Orthographic von +X zeigt die gegenüberliegende Seite. Beide Seiten werden ohne Spiegelung überprüft. Orthografische Bildvergleiche sind an Bodenlinie, Körperachse und 1,40-m-Höhe ausgerichtet.

Die erhöhte Blender-Formkamera verwendet für V6 und V1 dieselbe Distanz, FOV, Winkel und Beleuchtung. Sie ist eine Annäherung an die gezeichnete Spielperspektive, kein Unreal-PIE-Test. Kein Unreal-Import war Teil dieses Auftrags.

Die kürzeren Hemd-/Westenenden und das weichere, seitlich hängende Halstuch bringen die Kleidung näher an die Referenz. Halstuch, Ärmel, offene Weste, weite Hose und nackte Füße sind auch erhöht lesbar. Die Verbesserung ist vor allem beim Tuch und unteren Oberkörpersaum sichtbar; die Gesamtsilhouette ändert sich moderat.

Verbleibende Unterschiede:

- Ärmel und gerollte Abschlüsse sind weiterhin glatter und einfacher als die gezeichnete Stoffbündelung.
- Hose besitzt noch größere, rundere Grundmassen; die Referenz zeigt feinere und stärker unregelmäßige Falten.
- Westenenden und Tuchüberlappung bleiben konstruktiv vereinfachte Formen.
- Zehen sind klar vorhanden, aber Oberflächenanatomie und Übergänge noch weich und vereinfacht.
- Bereits bestehende Unterschiede von V6-Kopf und Rucksack zum Sheet bleiben aufgrund der eingefrorenen Vorgaben bewusst bestehen.

Es wird keine vollständige visuelle Deckung mit dem Sheet behauptet. Keine zusätzlichen Details als Ersatz für Formähnlichkeit erstellt.

## Prüfungen

- Neue Blender-Datei gespeichert und anschließend im Hintergrund sowie im geöffneten Blender erneut geöffnet. Live-Datei meldet `dirty: false`, korrekten Speicherpfad und 47 aktive Meshes.
- Originaldatenvergleich: 329 bestehende Objekte, 21 Materialdatenblöcke und ursprüngliche Animationsdaten unverändert.
- 32 kopierte Meshes exakt V6; neun vorhandene Kleidung-/Fußkopien gezielt verändert; sechs neue Halstuchformen.
- Geometrieaudit: 499.736 rohe Vertices, 502.210 Flächen. Endliche Koordinaten, keine losen Vertices, keine degenerierten Flächen oder ungültigen inneren Kanten. Bereits vorhandene offene Augen-/Mundgrenzen sind zulässig; Füße, Haarvolumen und neue Tuchformen geschlossen.
- Fünf vordere Zehenkonturen pro Fuß zusätzlich geometrisch per Strahlabtastung erkannt; nicht ausschließlich über eine Objekt-Eigenschaft geprüft.
- Ursprung und Skalierung der neuen Figur korrekt; Höhe und Bodenpunkte geprüft.
- Keine neuen Rig-/Armature-Verbindungen, Animationen oder Shape Keys. Keine Weight-Painting-Arbeit. Vorhandene Vorschau-UVs wurden bei Geometrieoperationen erhalten/interpoliert, nicht finalisiert.
- Vier neue Python-Dateien syntaktisch geprüft, JSON geprüft, Markdown/Whitespace geprüft.
- `git diff --check`: ohne Ausgabe. Neue unversionierte Textdateien zusätzlich mit `git diff --no-index --check` geprüft.
- Kein Unreal-Build nötig: bestehende Gameplay-/C++-/Asset-Dateien bytegleich. Keine Runtime- oder Animationsreife behauptet.

## Dateien und Git-Sicherungspunkt

Sieben neue Dateien, keine bestehenden geändert. Reviewbilder, Logs und Zwischenkopien sind ignorierte Arbeitsartefakte.

```text
?? Art/Characters/YoungTrainer/Authoring/CompareClothingFeetV1.py
?? Art/Characters/YoungTrainer/Authoring/RefineClothingFeetV1.py
?? Art/Characters/YoungTrainer/Authoring/RenderClothingFeetV1.py
?? Art/Characters/YoungTrainer/Authoring/ValidateClothingFeetV1.py
?? Art/Characters/YoungTrainer/CLOTHING_FEET_V1.json
?? Art/Characters/YoungTrainer/CLOTHING_FEET_V1_PRUEFBERICHT.md
?? Art/Characters/YoungTrainer/Source/YoungTrainer_ClothingFeet_V1.blend
```

Für einen späteren, bewusst gewählten Sicherungspunkt kann ausschließlich dieser neue Stand gestaged werden. Der Befehl wurde nicht ausgeführt:

```sh
git add -- \
  Art/Characters/YoungTrainer/CLOTHING_FEET_V1.json \
  Art/Characters/YoungTrainer/CLOTHING_FEET_V1_PRUEFBERICHT.md \
  Art/Characters/YoungTrainer/Source/YoungTrainer_ClothingFeet_V1.blend \
  Art/Characters/YoungTrainer/Authoring/RefineClothingFeetV1.py \
  Art/Characters/YoungTrainer/Authoring/RenderClothingFeetV1.py \
  Art/Characters/YoungTrainer/Authoring/CompareClothingFeetV1.py \
  Art/Characters/YoungTrainer/Authoring/ValidateClothingFeetV1.py
```

Kein Commit und kein Push. Arbeit endet nach diesem Formpass; keine finalen Texturen, keine UV-Finalisierung, kein Rigging, keine Animationen und kein Unreal-Import.

## Prüfsummen

- Unveränderte V6-Quelle: `003a4d58b6a96384dd61b0e3fa93ac05025b28f2aacf48203a5eb8617a67a744`.
- Gespeicherte ClothingFeet-V1-Datei: `16be34ec332c3cbf6ff4422886094c3a38efd054bbcf9fdbb03f24d1d34085b3`.
