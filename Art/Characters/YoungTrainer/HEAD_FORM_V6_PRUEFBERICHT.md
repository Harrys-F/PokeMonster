# Young Trainer – Head Form V6: Prüfbericht

Datum: 7. Oktober 2026. Ausgangs-HEAD: `32979f347bd3a7705c43b602dadd2408d3bda08a` (`Save YoungTrainer Blender progress through head and hair V3`).

V6 ist ein lokaler Formpass auf dem gespeicherten V5-Stand. Keine grundlegende Neumodellierung, kein Folgepass. V5, V4, V3 und alle bereits vorhandenen Projektdateien bleiben erhalten. Der Arbeitsbaum war zu Beginn bereits offen; die V3-Änderung und die V4-/V5-Dateien gehören nicht zu dieser Aufgabe.

## Quelle, Ziel und Sicherung

- Verbindliche Quelle: `Art/Characters/YoungTrainer/Source/YoungTrainer_HeadForm_V5.blend`.
- Neue Quelle: `Art/Characters/YoungTrainer/Source/YoungTrainer_HeadForm_V6.blend`.
- Vollständiger Speicherpfad: `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer/Source/YoungTrainer_HeadForm_V6.blend`.
- V6-SHA256: `003a4d58b6a96384dd61b0e3fa93ac05025b28f2aacf48203a5eb8617a67a744`.
- Blender 5.2.2 LTS. V6 im Hintergrund und anschließend im geöffneten Blender erfolgreich erneut geladen; sauberer Speicherzustand, aktive Sammlung `YT6_Player`, aktives Objekt `YT6_Head`.
- Unveränderte V5-Geometrie bleibt zusätzlich als ausgeblendete Sammlung in V6 erhalten. Nur neue V6-Meshdaten wurden bearbeitet. Gemeinsame Vorschau-Materialien wurden nicht verändert.
- Ein eigener Zwischenstand der Ohrkontrolle liegt ausschließlich im ignorierten `Saved/YoungTrainerHeadFormV6/FirstLocalReview.blend1`. Die bereits vorhandene V3-Backup-Datei wurde nicht angefasst.
- 11 unverändert gepackte, gesperrte Referenzbilder aus `Reference/BarefootFinal` bleiben vorhanden. Verbindlich ist die barfüßige Referenzfigur, nicht das ältere Stiefel-Sheet.

## Haarvolumen

| Messgröße | V5 | V6 | Unterschied |
| --- | ---: | ---: | ---: |
| Geschlossenes Meshvolumen | 0,016959 m³ | 0,014774 m³ | −12,88 % |
| Maximale Breite | 36,60 cm | 33,90 cm | −2,70 cm / −7,38 % |
| Maximale Tiefe | 40,51 cm | 38,41 cm | −2,10 cm / −5,18 % |
| Vertikale Haarausdehnung | 35,49 cm | 35,49 cm | unverändert |
| Gesamthöhe der Figur | 140,00 cm | 140,00 cm | unverändert |

Das Volumen wurde mit `bmesh.calc_volume` am geschlossenen Haarmesh gemessen; es ist keine Schätzung aus der Bounding Box. Die Breite und Tiefe sind maximale geometrische Grenzen, keine anatomischen Kopfmaße.

Lokale, kontinuierliche Verformung an den Schläfen und seitlichen Haarpartien, am Hinterkopf sowie an der oberen seitlichen/hinteren Masse. Keine globale Skalierung. Seitliche Extrempunkte wandern links ca. 1,30 cm und rechts ca. 1,40 cm nach innen; der hinterste Punkt wandert 2,10 cm nach vorne. Maximale kombinierte lokale Verschiebung: 2,82 cm.

Alle Haar-Z-Koordinaten bleiben identisch. 29.047 zentrale Stirnlocken-Vertices bleiben exakt unverändert; die höchste Spitze bei Z = 1,40 m ebenfalls. Bestehende Spitzen, Asymmetrie und große Lockenverläufe bleiben erhalten. Es wurden weder Haarsträhnen ergänzt noch die Topologie neu aufgebaut. 293.548 von 359.332 Haar-Vertices haben veränderte Koordinaten.

## Augen, Lider und Ausdruck

- Obere Augenöffnung lokal um maximal 3,7 mm abgesenkt; Breite unverändert. Augenweiß-Höhe rechts: 6,03 → 5,66 cm. Die unterstützenden orbitalen Loops folgen dieser Form.
- Bestehende obere Lidkante im Querschnitt verstärkt (Faktor 1,38 vor Projektion auf die Gesichtsfläche); die unteren Lidkonturen reduziert (Faktor 0,62). Äußere Augenwinkel nur lokal um etwa 1,2 mm verlängert und 0,6 mm abgesenkt. Kein kompletter kreisförmiger dunkler Rand.
- Iris samt Pupille und Glanzpunkten lediglich fein abgestimmt: +1,5 % Breite, −1 % Höhe und 2,5 mm höher. Iris rechts: 4,61 × 4,97 → 4,68 × 4,93 cm. Der große warme Blick bleibt erhalten. Das Weiß oberhalb der Iris ist deutlich geringer; die obere Kontur liegt näher an der Iris, ohne die Augen neu zu bauen.
- Brauen etwa 1,5 mm tiefer, Bogenvertikale um 12 % abgeflacht; bestehendes Dunkelbraun bleibt erhalten.
- Mundbreite um 3 % reduziert; Mundwinkel um maximal etwa 0,65 mm angehoben. Kleiner freundlicher neutraler Ausdruck, kein breites Dauerlächeln.
- Bestehende Nase, Kinn, Stirn und breite Wangenform bleiben erhalten. Am Kopf sind ausschließlich bestehende Augen- und Mund-Supportloops verändert.

## Ohren

Nur die beiden bereits getrennten Ohrkomponenten innerhalb des Body-Meshes wurden verändert: Vertices 302–745. Sämtliche Hals-/Arm-Vertices 0–301 bleiben exakt identisch.

Kleine lokale Verkleinerung, weicherer unterer Abschluss (bis 3 mm angehoben), einfache breite Ohrmulde an Vorder- und Außenfläche. Keine neuen Knorpel-, Falten- oder Schmuckdetails. Ohrposition grundsätzlich erhalten, obere Bereiche weiterhin teilweise vom Haar verdeckt.

Rechtes Ohr, rohe geometrische Breite × Tiefe × Höhe: 4,73 × 2,29 × 4,78 cm → 4,13 × 2,27 × 4,24 cm. Die zusätzliche Außenmulde macht die Breitenreduktion etwas größer als den grundlegenden Faktor 0,92. Die Ohren bleiben vereinfacht und sind kein finales Anatomiemodell.

## Ansichten und visuelle Bewertung

Alle V5/V6-Vergleiche verwenden dieselben nativen Kameraeinstellungen, Auflösungen und Review-Lichter. Die orthografischen Vollansichten sind auf Fußboden und 1,40-m-Höhe registriert. Die Illustrationsausschnitte sind unverändert; kein gezeichnetes Gesicht wurde ins Modellbild montiert.

| Ansicht | Ergebnis |
| --- | --- |
| Front | Schläfen kompakter, Augen ruhiger und weniger offen, Stirnlocken erhalten. |
| Rechte Seite | Hinterkopf weniger ausladend; kleine Nase und kompakter Kinnverlauf erhalten; Ohrabschluss weicher. |
| Rücken | Weniger seitliche/hintere Masse; bestehende asymmetrische Locken und Spitzen erhalten. |
| 3/4 vorne, beide Seiten | Ruhigere Augen und kompaktere seitliche Frisur; keine grundlegende neue Gesichtsform. |
| 3/4 hinten, beide Seiten | Haarabschluss und Rucksack bleiben gut getrennt; Rucksack identisch. |
| Erhöht vorne | Augen erkennbar, Gesicht und Haare bleiben getrennt. Lokale Verbesserung moderat sichtbar. |
| Erhöht seitlich | Hinterkopf kompakter, unveränderte Körper-/Ausrüstungssilhouette. |
| Erhöht hinten | Kompaktere Kontur, unveränderte Rucksackform. |

Die Seitenbenennung folgt dem Sheet: rechts wird von −X gesehen. Blender Right Orthographic (+X) entspricht der linken Sheet-Ansicht; beide wurden zusätzlich kontrolliert. Keine gespiegelte Referenz wurde verwendet.

Die erhöhte Blender-Formkamera nutzt FOV 35°, 35° Elevation und 3,4 m Abstand mit vollständiger Figur im Bild. Sie ist eine Annäherung an die Perspektivenreihe des Sheets und ausdrücklich kein Unreal-PIE-Test bzw. keine identische Laufzeitkamera. Die tatsächliche Unreal-Kamera wurde nicht geöffnet oder verändert.

### Verbleibende Unterschiede

V6 ist eine moderate Annäherung, keine volle Übereinstimmung mit dem Sheet. Haarbündel bleiben gröber, größer und streifenartiger als die feineren illustrativen Locken; hintere Spitzen wirken stellenweise länger. Die Augen, Nase, Wangen und Ohren bleiben konstruktiv einfacher als das Portrait. Der Unterschied zwischen untexturiertem 3D-Vorschauvolumen und gezeichneten Licht-/Konturlinien ist weiterhin sichtbar. Körper-/Kleidungsabweichungen aus früheren Ständen wurden in diesem ausdrücklich begrenzten Pass nicht korrigiert.

Aus der erhöhten Formkamera liegt die Kopfkontur etwas näher an der Referenz, ohne Lesbarkeit einzubüßen. Lid- und Ohrdetails sind dort schwächer sichtbar als in der Nahaufnahme; die Silhouette hat Vorrang. Kein weiterer Detailpass wurde begonnen.

## Prüfungen

- Geometrieaudit: PASS, 42 aktive Meshes, 595.258 rohe Vertices / 597.348 Faces. Topologie unverändert.
- Endliche Koordinaten, keine losen Vertices, keine degenerierten Faces, keine ungültigen nicht-manifold Innenkanten. Haarmesh weiterhin geschlossen. Bestehende gewollte Augen-/Mundflächenränder sind erhalten und werden nicht als Fehler behandelt.
- 19 vollständige Körper-/Kleidungs-/Ausrüstungsmeshes exakt identisch. Am 20. nicht zum Kopf gehörenden Mesh (`Body`) ausschließlich beide Ohren angepasst; Hals und Arme exakt erhalten.
- An allen kopierten Meshes: UVs, Gewichte, Gruppen, Materialzuweisungen, Modifier und lokale Transformationen identisch zu V5.
- 285 bereits vorhandene Blender-Objekte, 21 Materialien und vorhandene Actions/Rig unverändert. Sichtbarkeit der V5-Archivsammlung ist die beabsichtigte Ausnahme.
- 11 gesperrte gepackte Referenzen unverändert.
- Fußsohlen Z = 0, Gesamthöhe 1,399999976 m; Root am Ursprung, Scale 1.
- Integrität aller 986 vor Beginn vorhandenen nicht ignorierten Projektdateien: SHA256 identisch. V5 und andere `.blend`-Dateien nicht überschrieben.
- V6 erfolgreich erneut geöffnet, sauberer Speicherzustand.
- Neue Python-Skripte syntaktisch geprüft; JSON gültig; Markdown-Struktur und Whitespace geprüft.
- `git diff --check`: Exit 0, keine Ausgabe. Alle sechs neuen unversionierten Textdateien zusätzlich mit `git diff --no-index --check /dev/null` geprüft, ohne Whitespace-Meldungen. Exit 1 bezeichnet hier den vorhandenen Unterschied zur leeren Datei.
- Kein Unreal-Build, keine Gameplay-Automationstests: keine Unreal-/C++-/Gameplay-Datei verändert und kein Import erstellt.
- Keine finalen Materialien/Texturen/UVs, kein Rigging und keine Animation. Vorhandene Vorschau-Materialien unverändert wiederverwendet.
- Kein Staging, Commit oder Push.

## Neue Dateien dieser Aufgabe

1. `Art/Characters/YoungTrainer/Source/YoungTrainer_HeadForm_V6.blend`
2. `Art/Characters/YoungTrainer/HEAD_FORM_V6.json`
3. `Art/Characters/YoungTrainer/HEAD_FORM_V6_PRUEFBERICHT.md`
4. `Art/Characters/YoungTrainer/Authoring/RefineHeadFormV6.py`
5. `Art/Characters/YoungTrainer/Authoring/RenderHeadFormV6.py`
6. `Art/Characters/YoungTrainer/Authoring/CompareHeadFormV6.py`
7. `Art/Characters/YoungTrainer/Authoring/ValidateHeadFormV6.py`

Keine bestehende Projektdatei in dieser Aufgabe verändert. Neue Prüfprotokolle, eigene Zwischenbackup-Datei und Reviewbilder liegen ausschließlich im ignorierten `Saved/YoungTrainerHeadFormV6`.

## Reviewbilder

Vollständige Pfade:

- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/YoungTrainerHeadFormV6/Review/HeadBeforeAfter.jpg` – Referenz, V5, V6.
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/YoungTrainerHeadFormV6/Review/HeadFrontBeforeAfter.jpg`.
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/YoungTrainerHeadFormV6/Review/HeadRightBeforeAfter.jpg`.
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/YoungTrainerHeadFormV6/Review/HeadBackBeforeAfter.jpg`.
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/YoungTrainerHeadFormV6/Review/ReferenceFrontSideBack.jpg`.
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/YoungTrainerHeadFormV6/Review/V5_V6_EightViews.jpg`.
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/YoungTrainerHeadFormV6/Review/GameBeforeAfter.jpg`.
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/YoungTrainerHeadFormV6/Review/Silhouettes.jpg`.
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/YoungTrainerHeadFormV6/Audit.json` – Maschinenlesbare Geometrie-/Integritätsprüfung.
- `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/YoungTrainerHeadFormV6/ComponentMetrics.json` – Vergleichsmaße.

## Empfohlener Git-Sicherungspunkt

Erst nach Harrys visueller Prüfung. Ausschließlich V6-Dateien auswählen; die bereits offenen V3/V4/V5-Änderungen separat beurteilen. Dieser Befehl wurde nicht ausgeführt:

```sh
git add -- \
  Art/Characters/YoungTrainer/Source/YoungTrainer_HeadForm_V6.blend \
  Art/Characters/YoungTrainer/HEAD_FORM_V6.json \
  Art/Characters/YoungTrainer/HEAD_FORM_V6_PRUEFBERICHT.md \
  Art/Characters/YoungTrainer/Authoring/RefineHeadFormV6.py \
  Art/Characters/YoungTrainer/Authoring/RenderHeadFormV6.py \
  Art/Characters/YoungTrainer/Authoring/CompareHeadFormV6.py \
  Art/Characters/YoungTrainer/Authoring/ValidateHeadFormV6.py
```

## Abschließender Git-Status

Enthält auch sämtliche bereits vor Aufgabenbeginn offenen Dateien. Keine davon wurde durch V6 überschrieben:

```text
 M Art/Characters/YoungTrainer/Source/YoungTrainer_HeadHair_V3.blend
?? Art/Characters/YoungTrainer/Authoring/CompareBarefootReference.py
?? Art/Characters/YoungTrainer/Authoring/CompareHeadFormV5.py
?? Art/Characters/YoungTrainer/Authoring/CompareHeadFormV6.py
?? Art/Characters/YoungTrainer/Authoring/RefineHeadFormV5.py
?? Art/Characters/YoungTrainer/Authoring/RefineHeadFormV6.py
?? Art/Characters/YoungTrainer/Authoring/RenderBarefootReference.py
?? Art/Characters/YoungTrainer/Authoring/RenderHeadFormV5.py
?? Art/Characters/YoungTrainer/Authoring/RenderHeadFormV6.py
?? Art/Characters/YoungTrainer/Authoring/ReworkBarefootReference.py
?? Art/Characters/YoungTrainer/Authoring/ValidateBarefootReference.py
?? Art/Characters/YoungTrainer/Authoring/ValidateHeadFormV5.py
?? Art/Characters/YoungTrainer/Authoring/ValidateHeadFormV6.py
?? Art/Characters/YoungTrainer/BAREFOOT_REFERENCE_V4.json
?? Art/Characters/YoungTrainer/BAREFOOT_REFERENCE_V4_PRUEFBERICHT.md
?? Art/Characters/YoungTrainer/HEAD_FORM_V5.json
?? Art/Characters/YoungTrainer/HEAD_FORM_V5_PRUEFBERICHT.md
?? Art/Characters/YoungTrainer/HEAD_FORM_V6.json
?? Art/Characters/YoungTrainer/HEAD_FORM_V6_PRUEFBERICHT.md
?? Art/Characters/YoungTrainer/Reference/BarefootFinal/
?? Art/Characters/YoungTrainer/Source/Stages/08_BeforeBarefootReferenceRework_20261007.blend
?? Art/Characters/YoungTrainer/Source/Stages/09_BeforeHeadFormV5_20261007.blend
?? Art/Characters/YoungTrainer/Source/YoungTrainer_BarefootReference_V4.blend
?? Art/Characters/YoungTrainer/Source/YoungTrainer_HeadForm_V5.blend
?? Art/Characters/YoungTrainer/Source/YoungTrainer_HeadForm_V6.blend
?? Art/Characters/YoungTrainer/Source/YoungTrainer_HeadHair_V3.blend1
```
