# YoungTrainer V5 – Kopf, Gesicht und Haarform

Arbeitsstand vom 07.10.2026 auf `32979f3 Save YoungTrainer Blender progress through head and hair V3`. Fortsetzung des offenen V4-Arbeitsstands, kein sauberer Ausgangsbaum: die vorhandene Änderung an V3, deren `.blend1` sowie sämtliche V4-Dateien bleiben erhalten. Kein Commit, kein Push, kein Unreal-Import.

## Umfang und Sicherung

Harry hat den vorgeschlagenen nächsten Pass ausschließlich für Kopf, Gesicht und Haare bestätigt. Körper, Kleidung, Hände, Füße und Reiseausrüstung wurden nicht weiter bearbeitet. Die 1,40-m-Gesamthöhe bleibt verbindlich.

- Vorheriger Live-Stand: `Source/YoungTrainer_BarefootReference_V4.blend`.
- Separate Sicherung vor Bearbeitung: `Source/Stages/09_BeforeHeadFormV5_20261007.blend`.
- Neue aktive Quelle: `Source/YoungTrainer_HeadForm_V5.blend`.
- V4 bleibt vollständig als ausgeblendete Quell-Collection erhalten. Neue Arbeitskopien liegen in `YT5_Player` unter `YT5_PlayerRoot`.
- Die vom eigenen V5-Speichern erzeugten Zwischenkopien werden unter ignoriertem `Saved/YoungTrainerHeadFormV5/Backups` erhalten. Die bereits vorhandene V3-`.blend1` wurde nicht bewegt oder überschrieben.

## Ausgangsprobleme und Formkorrekturen

Die native V4-Portraitansicht zeigte stark aufgesetzte, fast kreisrunde Augen mit deutlichem unteren Rand. Die Wangen-/Kinnflächen hatten unruhige Vertiefungen; Nase und Mund waren wenig klar. Die Haargruppen wirkten wie dicke einzelne Blätter mit sichtbaren Übergängen zur Grundmasse.

Dieser Pass umfasst mehrere getrennt geprüfte Iterationen:

- **Gesicht:** breitere zusammenhängende Wangenfläche, ruhigerer Kinnverlauf, kleiner Nasenvorsprung. Die vordere Fläche wurde an den vorhandenen Augen- und Mundschleifen ausgerichtet. Ein zunächst stufiger Profilverlauf wurde durch stetige kubische Profile korrigiert; Übergänge zur Seitenfläche werden weich gemischt.
- **Augen:** weniger Tiefe und Vorwölbung; breitere, flachere mandelförmige Kontur. Iris, Pupille, vorhandene Glanzflächen und Lider folgen derselben Gesichtsoberfläche. Der untere Rand tritt zurück, die obere Lidkante bleibt lesbar. Keine neuen finalen Gesichtstexturen oder zusätzlichen Wimperndetails.
- **Brauen/Mund:** vorhandene Brauen folgen der neuen Fläche. Die vorhandene Mundlinie ist etwas breiter und mit leicht angehobenen Winkeln auf der Oberfläche positioniert. Keine finale Mimik oder Gesichtsanimation.
- **Haare:** größere asymmetrische Stirn- und Schläfenschwünge, kürzere abstehende Haken, koordinierter Verlauf über Scheitel und Hinterkopf. 57 breite Formverläufe werden zusammen mit dem Grundvolumen zu einer zusammenhängenden Arbeitsgeometrie verbunden. Stabile Querschnittsorientierung verhindert unbeabsichtigte Verdrehungen der Locken. Die Haarbreite wurde im abschließenden Silhouettenvergleich um 6 % reduziert, das Nackenhaar lokal um bis zu 5,2 cm verlängert. Keine feinen Einzelhaare.
- **Geometriebereinigung:** ausschließlich winzige neu erzeugte Voxel-Fragmente und degenerierte Elemente aus der eigenen neuen Haargeometrie entfernt. Keine vorhandenen Projektobjekte gelöscht.

Die Gesamthöhe wird ausschließlich am Scheitel des neuen Haarvolumens auf 1,40 m gehalten. Keine Körper-/Actor-Skalierung, keine Verschiebung der Fußsohlen, keine Änderung einer Unreal-Einstellung.

## Referenzen und Prüfkameras

Die vorhandenen elf gepackten und gesperrten Referenzbilder in `REF_PLAYER_FINAL` bleiben unverändert. Gemeinsamer Maßstab der Hauptrichtungen: 0,00358974359 m pro Pixel, Scheitelzeile 87, Bodenzeile 477. Front-, Seiten- und Rückvergleiche verwenden denselben Weltmaßstab und dieselbe Bodenlinie. Blender Right Orthographic entspricht bei der Blickrichtung −Y der linken Profilzeichnung des Sheets.

V5 enthält fünf eigene, gesperrte Blender-Prüfkameras: Front, Right Orthographic, Back, erhöhte Game-Ansicht und Kopf-3/4. Alte Kameras bleiben unverändert. Die Formprüfung verwendet:

| Ansicht | Feste Einstellung |
| --- | --- |
| Ganze Figur orthografisch | 1,62 m Bildhöhe, Zentrum Z = 0,70 m |
| Kopf orthografisch | 0,45 m Bildhöhe, Zentrum (0 / 0,02 / 1,21 m) |
| Erhöhte Formansicht | 35° Höhenwinkel, 35° horizontaler FOV, 3,40 m Abstand |
| Acht Richtungen | dieselbe erhöhte Kamera, nur Azimut geändert |

Die Prüfkamera bleibt für alle Iterationen und für den V4-/V5-Vergleich fest. Die Zeichnung liefert keine exakten Kameraparameter; eine eindeutig gelöste Kalibrierung ist deshalb nicht behauptet. Dies ist eine angenäherte Blender-Formprüfung und verändert keine Unreal-Spielkamera.

## Sichtprüfung und verbleibende Abweichungen

Front, beide Seiten, Rücken, sämtliche 3/4-Richtungen und alle acht erhöhten Richtungen wurden an echten Blender-Renderbildern geprüft. Die Augen stehen weniger vor, das Gesicht hat ruhigere Flächen, und die dominante Stirnlocke verläuft seitlich statt senkrecht. Der Hinterkopf endet näher am Halstuch.

Die Figur entspricht dem Sheet weiterhin nicht vollständig. Besonders die Haarformen sind noch massiver und regelmäßiger als die gezeichneten Locken. Augenlider, Ohren und Gesichtsausdruck bleiben einfacher; die Zeichnung besitzt feinere Übergänge und eine bewusst malerische Formbeschreibung. Dies ist kein finales Gesicht, keine finale Frisur und keine vorweggenommene visuelle Freigabe.

Kleidung, Ärmel, Hände, Füße und Rucksack behalten die bekannten V4-Abweichungen. Sie wurden in diesem begrenzten Pass ausdrücklich nicht verändert. Weitere Arbeit muss anhand der Vergleichsbilder entschieden werden; es folgt kein automatischer Übergang zu Texturen, Rigging oder Animationen.

## Prüfung und Dateiliste

Die gespeicherte V5-Datei wurde erneut geöffnet. Der lesende Audit vergleicht die Sicherung mit V5, inklusive aller ursprünglichen Objekte, Meshkoordinaten, UVs, Gewichte, Formschlüssel, Materialien, Rig/Pose und Aktionen. Zusätzlich werden sämtliche Körper-/Kleidungs-/Ausrüstungs-Arbeitskopien mit den entsprechenden V4-Objekten verglichen. Ergebnisdetails und native Bilder liegen unter ignoriertem `Saved/YoungTrainerHeadFormV5`; die abschließenden Zahlen stehen auch in `HEAD_FORM_V5.json`.

Abschließender Audit: **PASS**. Alle **70** zu Beginn vorhandenen Charakterdateien bytegleich; **237** vorherige Blender-Objekte und **21** Materialien erhalten. Alle **20** Körper-/Kleidungs-/Ausrüstungs-Arbeitsmeshes einschließlich UVs, Gewichten und Modifikatoren gleich zu V4. V5 umfasst **42** aktive Meshes mit **595,258** Basisvertices. Gesamthöhe **1.39999998 m**, Fußsohlen **Z = 0**. Keine ungültigen Koordinaten, losen Vertices, degenerierten Flächen oder nicht-manifold inneren Kanten; neue Haare geschlossen. Bestehende offene Augen-/Mundschleifen, Farbflächen und dünne Kleidungsflächen sind beabsichtigt.

Keine Unreal-Dateien, Maps oder Assets geändert. Daher kein Unreal-Build und keine Gameplay-Automation in diesem ausschließlich auf Blender beschränkten Pass.

Neue Projektdateien dieses Passes:

- `HEAD_FORM_V5.json`
- `HEAD_FORM_V5_PRUEFBERICHT.md`
- `Authoring/RefineHeadFormV5.py`
- `Authoring/RenderHeadFormV5.py`
- `Authoring/CompareHeadFormV5.py`
- `Authoring/ValidateHeadFormV5.py`
- `Source/Stages/09_BeforeHeadFormV5_20261007.blend`
- `Source/YoungTrainer_HeadForm_V5.blend`

Vier Authoring-Skripte syntaktisch geprüft; JSON und Markdown gültig. `git diff --check` erfolgreich, ohne Ausgabe. `git status --short` enthält ausschließlich den bereits offenen Charakterstand und die acht neuen V5-Dateien; nichts gestaged. Ein sinnvoller Sicherungspunkt ist die erneut geöffnete V5-Version nach Harrys Sichtprüfung. Nur die neuen V5-Dateien können mit diesem Befehl vorgemerkt werden; er wurde nicht ausgeführt. Die bereits offenen V4-Referenzdateien sind weiterhin Grundlage der Vergleichsskripte und sollten über den separaten Sicherungsbefehl im V4-Bericht ebenfalls versioniert werden; dieser V5-Befehl verändert ihren Staging-Status nicht:

```sh
git add -- \
  Art/Characters/YoungTrainer/HEAD_FORM_V5.json \
  Art/Characters/YoungTrainer/HEAD_FORM_V5_PRUEFBERICHT.md \
  Art/Characters/YoungTrainer/Authoring/RefineHeadFormV5.py \
  Art/Characters/YoungTrainer/Authoring/RenderHeadFormV5.py \
  Art/Characters/YoungTrainer/Authoring/CompareHeadFormV5.py \
  Art/Characters/YoungTrainer/Authoring/ValidateHeadFormV5.py \
  Art/Characters/YoungTrainer/Source/Stages/09_BeforeHeadFormV5_20261007.blend \
  Art/Characters/YoungTrainer/Source/YoungTrainer_HeadForm_V5.blend
```
