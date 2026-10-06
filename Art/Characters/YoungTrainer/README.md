# Young Trainer – Blender Reference V1

Datum: 2026-10-06. Ausgangs-HEAD: `eafab5b Complete healing house art quality V3`.
Der Arbeitsbaum war zu Beginn sauber. Ausschließlich neue Charakter-Quelldateien;
keine Änderung an Unreal, Maps, Gameplay, bestehender Spielfigur oder Projektdokumentation.

Die verbindliche Vorlage liegt unverändert unter `Reference/Character_Turnaround.png`.
Dies ist eine vollständig modellierte erste Blenderfassung mit UVs, Materialien
und einem einfachen gewichteten FK-Skelett. Die gezeichnete Hauptreferenz bleibt
das Qualitätsziel: Gesicht, Locken, Stofffalten und gemalte Oberflächen sind in
dieser Fassung sichtbar vereinfacht. Die Datei ist keine bereits in Unreal
validierte oder fertig animierte Produktionsfigur.

## Öffnen und Aufbau

`Source/YoungTrainer_Reference_V1.blend` in Blender öffnen. Die aktive Szene heißt
`YoungTrainer_Reference_V1`; die ursprüngliche Szene `Scene` bleibt separat erhalten.
`Cube`, `Camera` und `Light` wurden nicht verändert. Der Vergleich gegen den ersten
Kontrollpunkt hat Geometrie, lokale Transformationen und Kamera-/Lichtparameter bestätigt.

`YT_CharacterRoot` enthält `YT_Rig` und die Charaktermeshes.
Die Sammlung `YT_ReviewOnly` enthält ausschließlich Kameras und Studiolichter.
Beim späteren Export darf diese Sammlung ebenso wie die ursprüngliche Szene nicht
mit exportiert werden. In dieser Aufgabe wurde kein Export angelegt.

| Kennwert | Geprüfter Wert |
| --- | --- |
| Höhe, Sohlen bis oberste Haarform | 1,400 m / 140,0 cm |
| Bounds, neutrale A-Pose | X −0,399…+0,399 m; Y −0,170…+0,357 m; Z 0…1,400 m |
| Vertices | 28.499 |
| Triangulierter Umfang | 56.066 Dreiecke |
| Quads | 25.954 |
| Logische Meshkomponenten | 20 |
| Knochen | 32, davon Root ohne direkte Deformation |
| Höchste Anzahl Gewichte pro Vertex | 3; normalisiert |
| Mesh-/Rig-/Root-Skalierung | (1, 1, 1), keine negative Skalierung |
| Rotation und Ursprung | Meshes/Rig/Root ohne Objektrotation; gemeinsamer Bodenursprung (0, 0, 0) |
| Koordinaten | Meter, +Z oben, −Y vorwärts; +X anatomisch links |
| Skinning | Linear, ohne Blender-spezifisches Preserve Volume |
| Texturen | zwei gepackte PNGs, je 2048 × 1024 |

20 Meshes: `YT_Head`, `YT_Body`, `YT_Shirt`, `YT_Pants`, `YT_Socks`, `YT_Boots`,
`YT_Hands`, `YT_Eyes`, `YT_Face`, `YT_Hair`, `YT_Vest`, `YT_Scarf`, `YT_Belt`,
`YT_Harness`, `YT_Pouches`, `YT_Wristbands`, `YT_Pendant`, `YT_Backpack`,
`YT_Bedroll`, `YT_Equipment`.

Die Kleidungs- und Ausrüstungsschichten bleiben logisch getrennt. Haarlocken,
Nähte und Verzierungen sind mehrere geschlossene Geometrieinseln innerhalb ihrer
Komponente. Die Topologieprüfung bestätigt geschlossene Komponenten ohne lose
Vertices, Nullflächen, offene oder nicht-mannigfaltige Kanten. Das bedeutet keine
verschweißte Gesamtfigur und ersetzt keine Animationsprüfung sämtlicher Posen.

## Materialien und UVs

Ein gemeinsames Material `YT_IllustratedAtlas` verwendet:

- `Textures/YT_PaintedBaseColor.png`: sRGB, warme Palette mit selbst erzeugten
  weichen Farb- und Pinselvariationen. Keine Fremdtexturen oder Bildgenerierung.
- `Textures/YT_ORM.png`: Non-Color; R = 1 (kein gebackenes AO), G = Roughness,
  B = Metallic. Matte Stoff-/Lederflächen; gedämpfter Messington.

Beide Bilder sind gepackt und zusätzlich extern vorhanden; Bildpfade sind relativ
zur Blenderquelle. Die UVs teilen absichtlich Palettekacheln. Es gibt keine einzigartige
Ganzkörper-Bake-/Lightmap-UV und keinen Normalmap-Bake. Die Oberflächen sind einfache
illustrierte Farbfelder, kein individuell von Hand gemaltes finales Texturset.
Die 20 Meshes teilen einen Materialdatensatz; das garantiert nicht einen Drawcall.

## Rig und Prüfungen

Neutrale A-Pose mit freigestellten Armen, vereinfachten Fingern und getrenntem
Rucksack. Skelett: Root, Becken, Wirbelsäule, Brust, Hals, Kopf; pro Seite
Schlüsselbein, Oberarm, Unterarm, Hand, vier Finger, Daumen, Oberschenkel,
Unterschenkel, Fuß und Zehe. Kein IK, keine Animation-Actions, keine Gesichtsmimik.

Der Test wurde nach erneutem Öffnen der gespeicherten Quelle ausgeführt:

- Höhe, Transformationen, UVs, Materialslots und sämtliche Gewichte geprüft.
- Vier temporäre FK-Prüfposen: Rest, Schritt, Interaktion, stärkerer Laufimpuls.
- Hände/Rucksack und sichtbare Haut/Rucksack: jeweils keine überschneidenden
  Oberflächen in diesen vier Posen. Dies ist kein Beweis für beliebige Lauf-,
  Kampf- oder Reitanimationen; innere Kleidungslagen werden nicht als Fehler gewertet.
- Native Blender-Renderbilder: acht Richtungen frontal, acht erhöhte Richtungen,
  Portrait, zwei Kamerabilder mit 25 m Abstand / 35° FOV / 55° Elevation und zwei
  Deformationsbilder. Alle geprüft; die Figur bleibt als kleine Figur durch
  Halstuch, Weste, Stiefel und Rucksack unterscheidbar.
- Die Kameratests sind Blender-Vorschauen, kein PIE-Test. Unreal blieb unangetastet.
- Reopen erfolgreich; beide Texturen gepackt; neutrale Ausgangspose wiederhergestellt.

Die technische Prüfung steht in `Saved/YoungTrainerV1/Audit.json`, die ursprüngliche
Szene in `Saved/YoungTrainerV1/Preservation.json`. Native Bilder/Kameraangaben liegen
unter `Saved/YoungTrainerV1/Review`. Logs und automatisch erzeugte `.blend1`-Backups
bleiben unter `Saved/YoungTrainerV1`; sie gehören nicht zu den Charakterquellen.

## Referenzvergleich und Grenzen

Großer Kopf, warme braune Augen, rote Halstuchform, cremefarbene Rollärmel,
goldverzierte blaue Weste, weite Olivhose, helle Socken, große braune Stiefel,
Gürtel/Taschen, runder Anhänger und der Rucksack mit Schlafrolle sind umgesetzt.
Vorder-, Seiten-, Rücken- und erhöhte Ansichten wurden gemeinsam berücksichtigt.
Der Haarpass ersetzt zunächst regelmäßige ovale Locken durch größere unregelmäßige
geschwungene Haarformen. Augenüberdeckung und spitz zulaufende Irisformen wurden
nach dem Portraitvergleich korrigiert.

Die Formensprache ist dennoch einfacher und runder als die Vorlage; der Rucksack
ist konstruktiver/rechteckiger, die Kleidungsoberflächen und Haarkonturen weniger
malerisch. Insbesondere Gesicht und Locken brauchen für eine finale, sehr nahe
Referenzumsetzung weitere künstlerische Arbeit. Für ausdrucksstarke Mimik wäre
zusätzliche Facial-Retopologie mit echten Augen-/Mund-Deformationsschleifen und
Blendshapes nötig; derzeit sind Augen, Lider und Mund auf den Kopf gewichtet.

Vor einer Produktionseinbindung müssen Lauf/Run und die weiteren geforderten
Animationen tatsächlich erstellt und geprüft werden. LODs, Engine-Import,
Retargeting, Collision/Physics und M4-Laufzeitperformance wurden nicht getestet.
Für einen späteren Unreal-Export müssen Meter → Zentimeter und −Y → gewünschte
Engine-Vorwärtsachse kontrolliert umgesetzt werden. Es wurde keine bestehende
Playergröße, Geschwindigkeit, Kamera oder Darstellung ersetzt.

## Kontrollpunkte und reproduzierbare Quellen

| Datei in `Source/Stages` | Zweck |
| --- | --- |
| `01_Blockout.blend` | Grundkörper und Proportionshülle |
| `02_FaceHair.blend` | erster Kopf-/Haarpass |
| `03_Modelled.blend` | Kleidung und vollständige Ausrüstung |
| `04_ReferenceRefined.blend` | erster Mehransichten-Korrekturpass |
| `05_LikenessPolish.blend` | korrigierte Haare/Augen/Gesicht vor UVs und Rig |

`Authoring` enthält die Blender-Python-Schritte und die Palette. Die Modellierung
beginnt mit `BuildYoungTrainer.py` in einer neuen/geeigneten Blenderdatei, danach
folgen `DetailYoungTrainer.py`, `RefineYoungTrainer.py`, `PolishYoungTrainer.py`
und `PrepareYoungTrainer.py`. Die mittleren Schritte erwarten die vorherigen
eigenen Kontrollpunkte; nicht blind auf der fertigen, bereits geriggten Quelle
erneut ausführen. `PrepareYoungTrainer.py` prüft seinen Ausgangskontrollpunkt.
Validierung und Review sind separate Skripte. Die Skripte enthalten für diese
lokale Arbeit den Projektpfad; vor einer Wiederholung an anderem Ort anpassen.

`MANIFEST.json` enthält Prüfdaten, Komponenten und SHA-256-Werte der Quellen.
Kein bestehender Git-Inhalt wurde verändert. Kein Commit, kein Push.

Ein sinnvoller Sicherungspunkt ist diese gesichtete Blenderfassung; ausschließlich
die neuen Charakterquellen ließen sich bei Bedarf mit folgendem Befehl stagen:

```sh
git add -- Art/Characters/YoungTrainer
```

Dieser Befehl wurde nicht ausgeführt. Reviewbilder und Backups unter `Saved` werden
dabei nicht eingeschlossen.
