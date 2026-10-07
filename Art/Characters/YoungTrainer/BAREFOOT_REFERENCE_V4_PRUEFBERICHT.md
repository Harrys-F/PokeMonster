# YoungTrainer V4 – barfüßiger Referenzabgleich

Arbeitsstand vom 07.10.2026. Grundlage: `32979f3 Save YoungTrainer Blender progress through head and hair V3` sowie der tatsächlich geöffnete Blender-Arbeitsstand. Die bereits vorhandene Änderung an `Source/YoungTrainer_HeadHair_V3.blend` und die vorhandene `YoungTrainer_HeadHair_V3.blend1` wurden nicht überschrieben. Kein Commit, kein Push, kein Unreal-Import.

Verbindlich für diese Modellversion ist ausschließlich `Reference/BarefootFinal/Player_Barefoot_Turnaround.png`. Das Originalbild wurde unverändert übernommen. Die älteren Stiefelreferenzen bleiben als historische Ausgangsdaten erhalten und sind in der neuen Szene ausgeblendet.

## Sicherung und aktive Modellversion

- Sicherung des zuvor geöffneten, auch ungespeicherte Änderungen enthaltenden Arbeitsstands: `Source/Stages/08_BeforeBarefootReferenceRework_20261007.blend`.
- Neue aktive Quelle: `Source/YoungTrainer_BarefootReference_V4.blend`.
- Alte Geometrie, Formschlüssel, UVs, Materialien, Gewichte, Rig und Aktionen bleiben in ihren ausgeblendeten Quell-Collections erhalten.
- Die neue Figur liegt unter `YT4_PlayerRoot` in `YT4_Player`. Sie besteht aus statischen Arbeitskopien und neuen Formmeshes, ohne Armature-Anbindung oder neue Gewichte. Das alte Rig wurde nicht an die neuen Proportionen angepasst.

## Referenzausrichtung

`REF_PLAYER_FINAL` enthält elf gepackte, gegen Auswahl und Transformation gesperrte Referenzbilder: acht Richtungen, Portrait, Fußdetail und Spielperspektiven. Transparenz: 40 % für Richtungen, 45 % für die ergänzenden Bilder.

Die Hauptrichtungen verwenden einen gemeinsamen Maßstab von **0,00358974359 m pro Pixel**: gemeinsame Scheitellinie bei Bildzeile 87, Bodenlinie bei 477, entsprechend 390 Pixel für 1,40 m. Keine richtungsweise Streckung oder Anpassung der Referenz an das Modell. Die ergänzenden Portrait-/Detailbilder stehen separat und sind keine metrischen Messansichten.

Das Modell schaut entlang −Y. Blender **Right Orthographic** betrachtet es von +X und entspricht deshalb der nach links blickenden Profilansicht des Sheets. Die Bilder wurden nicht gespiegelt. Auch die beiden hinteren 3/4-Referenzen sind entsprechend dieser Konvention ausgerichtet.

## Durchgeführte Formkorrekturen

Mehrere Modellierungs- und Vergleichsrunden wurden anhand derselben Bodenlinie und desselben Maßstabs durchgeführt.

- **Körper:** kompaktere Höhenverteilung, schmalere Schultern, kürzerer Oberkörper und kürzere Beinproportionen. Arme und Hände tiefer und näher an die Referenzhaltung gebracht.
- **Kopf/Gesicht:** weicheres unteres Gesicht, kleines Kinn, reduzierte Nasenprojektion; größere, vertikal betonte Augen mit größerer brauner Iris, sichtbarer oberer Lidkante und kleiner freundlicher Mundlinie. Keine finalen Gesichtsdetails.
- **Haare:** altes Röhren-/Lockenmodell aus der aktiven Figur genommen. Neues zusammenhängendes Grundvolumen mit 46 überlagerten Volumenfeldern und 64 unterschiedlich großen, breiten Lockengruppen. Asymmetrische Stirnlocken, geschwungene Scheitelgruppen, Schläfenvolumen und dichterer Nacken. Wiederholte hornartige Spitzen entfernt; Augen bleiben frei.
- **Halstuch:** geschichtete, locker verlaufende Falten, mehr Stoffvolumen, überlappende Frontpartie und seitliches Ende. Seitliche Öffnungen aus einer zunächst ungeeigneten Dickenkonstruktion wurden korrigiert. Die neue Stoffform ist geschlossen.
- **Hemd/Weste:** weichere Ärmel, neue breite Rollbündchen, nach unten auslaufende offene Westenflächen. Der Saum wurde nochmals am maßgleichen Vergleich verlängert. Nicht mehr passend sitzende separate Zierstreifen sind nur aus der neuen Arbeitskopie entfernt; die Ausgangsgeometrie bleibt erhalten. Bestehende gemalte Ornamente werden weiterverwendet.
- **Hose:** breitere Knie-/Oberschenkelvolumen, versetzte breite Stofffalten und deutlicher eingezogene Bündchen; keine symmetrischen glatten Beinzylinder.
- **Hände:** neue zusammenhängende Handformen mit vier nach unten verlaufenden Fingern und einem seitlichen Daumen, statt seitlich gestapelter Fingerformen.
- **Füße:** Stiefel und Socken aus der aktiven Figur entfernt. Neue breite barfüßige Formen mit Ballen, Ferse, Fußgewölbe, schmalerem Knöchel und fünf unterscheidbaren Zehen je Fuß. Leicht unterschiedliche Außenrotation wie in der Referenz.
- **Reiseausrüstung:** Taschen näher am Körper und unterschiedlich positioniert; Gürtel geneigt, vorhandene Schnalle passend gesetzt. Rucksackvolumen weicher und tiefer, Schlafrolle niedriger und leicht durchhängend. Vorhandene Schnallen, Blattornament und Reiseaccessoire neu an ihren Trägerflächen positioniert; eine verzerrende stückweise Verschiebung des runden Accessoires wurde beseitigt.

Keine zusätzlichen Taschen oder Mikrodeko als Ersatz für fehlende Ähnlichkeit. Keine neuen finalen Texturen, UVs, Hautporen, Einzelhaare, Animationen oder Runtime-Dateien.

## Maßstab und Kontrollen

Die gespeicherte Datei wurde wieder geöffnet und ihre tatsächlich ausgewertete Geometrie vermessen:

| Größe | Ergebnis |
| --- | --- |
| Gesamthöhe | 1,39999998 m ≈ 140,00 cm |
| Niedrigste Fußsohle | Z = 0,00 m |
| Root | Weltursprung, Scale 1/1/1 |
| Gesamtbreite einschließlich Armen | ca. 56,70 cm |
| Gesamttiefe einschließlich Füßen/Rucksack | ca. 55,94 cm |
| Aktive Arbeitsmeshes | 106 |
| Basisvertices vor Vorschau-Subdivision | 280.344 |
| Zehen / Finger | jeweils fünf pro Fuß / Hand |

Front, beide Profile, Rücken und alle vier 3/4-Richtungen wurden als echte Blender-Ansichten geprüft. Zusätzlich wurden alle acht Richtungen mit einer erhöhten Blender-Prüfkamera verglichen. Diese verwendet 35° Höhenwinkel, 35° horizontalen FOV und 3,40 m Abstand für die Formkontrolle. Sie verändert keine Unreal-Kamera. Die gezeichnete Spielperspektive hat keine exakt bekannte Kamerakalibrierung; ihr Vergleich ist eine visuelle Plausibilitätskontrolle.

Die wesentlichen Merkmale sind jetzt gemeinsam lesbar: großer jugendlicher Kopf, dichte braune Haarmasse, schmale Schultern, rotes geschichtetes Halstuch, blaue offene Weste, kompakte weite Hose, nackte breite Füße und großer Reiserucksack. Der Abgleich ist keine Behauptung einer pixelgenauen oder finalen visuellen Gleichheit. Die Zeichnung enthält feinere Haarübergänge, Augen-/Wangenzeichnung, Stofffalten, Lederformen und malerische Oberflächen, die die einfache 3D-Arbeitsdarstellung noch nicht vollständig wiedergibt. Weitere Arbeit muss die Referenz weiterhin als Maßstab verwenden und darf nicht automatisch in Rigging oder Texturarbeit übergehen.

## Prüfungen

- Blenderdatei erfolgreich wieder geöffnet.
- Alle **50 vorhandenen Charakterdateien bytegleich** zur Sicherung vor V4, einschließlich der bereits geänderten V3-Datei und ihrer vorhandenen `.blend1`.
- **119 ursprüngliche Objekte** und **14 ursprüngliche Materialien** unverändert; Quellgeometrie, Formschlüssel, UVs, Gewichte, Rig/Bones/Pose und Aktionen erhalten.
- Neue Arbeitsgeometrie: keine ungültigen Koordinaten, losen Vertices, flächenlosen Faces oder nicht-manifold inneren Kanten.
- Neue Haare, Hände, Füße und Halstuch geschlossen. Beabsichtigte offene Augen-/Mundschleifen und ursprüngliche dünne Farb-/Kleidungsflächen bleiben dokumentiert.
- Tatsächliche transformierte Boden- und Scheitellinien der gesperrten Referenzen geprüft, nicht nur Metadaten.
- Vier Authoring-Skripte syntaktisch geprüft; neue JSON-Dateien geprüft.
- `git diff --check` erfolgreich. Für die bereits geänderte V3-Binärdatei benötigte Git LFS einmal Zugriff auf seinen lokalen Prüfcache; Index, History und Remote blieben unberührt.
- Keine Unreal-Dateien geändert; keine Unreal-Builds oder Gameplaytests in diesem Blender-Formpass.

Audit und native Vergleichsbilder liegen ausschließlich unter `Saved/YoungTrainerReferenceRework` und gehören nicht zum empfohlenen Staging. Die eigene letzte V4-Zwischenkopie wurde unter `Saved/YoungTrainerReferenceRework/Backups` erhalten. Die vorhandene V3-`.blend1` wurde nicht bewegt.

## Neue Projektdateien und Sicherungspunkt

Neue Dateien dieses Passes:

- `BAREFOOT_REFERENCE_V4.json`
- `BAREFOOT_REFERENCE_V4_PRUEFBERICHT.md`
- `Authoring/ReworkBarefootReference.py`
- `Authoring/RenderBarefootReference.py`
- `Authoring/CompareBarefootReference.py`
- `Authoring/ValidateBarefootReference.py`
- `Source/Stages/08_BeforeBarefootReferenceRework_20261007.blend`
- `Source/YoungTrainer_BarefootReference_V4.blend`
- `Reference/BarefootFinal/Alignment.json`
- `Reference/BarefootFinal/Player_Barefoot_Turnaround.png`
- `Reference/BarefootFinal/Front.png`
- `Reference/BarefootFinal/FrontRight.png`
- `Reference/BarefootFinal/Right.png`
- `Reference/BarefootFinal/BackRight.png`
- `Reference/BarefootFinal/Back.png`
- `Reference/BarefootFinal/BackLeft.png`
- `Reference/BarefootFinal/Left.png`
- `Reference/BarefootFinal/FrontLeft.png`
- `Reference/BarefootFinal/Portrait.png`
- `Reference/BarefootFinal/BareFeetDetail.png`
- `Reference/BarefootFinal/GameDirections.png`

Ein sinnvoller Git-Sicherungspunkt ist diese erneut geöffnete und geometrisch geprüfte Modellversion. Ausschließlich die neuen V4-Dateien lassen sich mit folgendem Befehl vormerken; er wurde nicht ausgeführt. Die bereits offenen V3-Nutzeränderungen sind bewusst nicht enthalten.

```sh
git add -- \
  Art/Characters/YoungTrainer/BAREFOOT_REFERENCE_V4.json \
  Art/Characters/YoungTrainer/BAREFOOT_REFERENCE_V4_PRUEFBERICHT.md \
  Art/Characters/YoungTrainer/Authoring/ReworkBarefootReference.py \
  Art/Characters/YoungTrainer/Authoring/RenderBarefootReference.py \
  Art/Characters/YoungTrainer/Authoring/CompareBarefootReference.py \
  Art/Characters/YoungTrainer/Authoring/ValidateBarefootReference.py \
  Art/Characters/YoungTrainer/Source/Stages/08_BeforeBarefootReferenceRework_20261007.blend \
  Art/Characters/YoungTrainer/Source/YoungTrainer_BarefootReference_V4.blend \
  Art/Characters/YoungTrainer/Reference/BarefootFinal
```
