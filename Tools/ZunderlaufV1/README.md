# Zunderlauf V1 – bestehendes Kreaturensystem

Aktives Projekt: `/Users/harry/Developer/PokeMonster`. Keine neue Map, kein neues Kampf- oder Speichersystem. Foto 1 ist gemäß Nutzerantwort maßgeblich, Foto 2 ergänzt Seiten-/Rückenform und Schwanzflamme. Die Körperhöhe ist vorläufig, nicht als kanonische Artangabe festgelegt.

## Quellen und Wiederholbarkeit

Blender 5.2.2, Hintergrundbetrieb; keine laufende Blender-Sitzung überschreiben:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 3 --python Tools/ZunderlaufV1/BuildModel.py
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 3 --python Tools/ZunderlaufV1/AnimateExport.py
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 3 --python Tools/ZunderlaufV1/BakeMaterials.py
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 3 --python Tools/ZunderlaufV1/ValidateSource.py
```

`BuildModel.py` überschreibt standardmäßig keine bestehende Quelle. `-- --revise` ist ausschließlich die bewusste Neuerzeugung dieses eigenen Modells; ersetzt dabei dessen aktuelle Arbeit. `AnimateExport.py` erneuert nur die sieben eigenen Actions in dieser Quelle, erhält Geometrie/UV/Gewichte und exportiert die Dateien unter `Exports/`. `BakeMaterials.py` ist der nachfolgende Erstbake aus den prozeduralen Quellmaterialien; nicht erneut auf bereits gebackene Materialien anwenden. Base Color enthält keine gebackene Studio-Beleuchtung. Die drei 2048²-Bilder sind gepackt.

Die Entwicklungsprüfung `ValidateSource.py` öffnet sowohl die gespeicherte Blenderdatei als auch den Walk-FBX wirklich erneut. Der aktuelle Stand enthält 96 beabsichtigte Randkanten der beiden Augenscheiben; keine wasserdichte Gesamtoberfläche behaupten. Körper, Arme, Beine und Schwanz besitzen eine zusammenhängende Haut. Das eigene Rig hat 23 Bones; Unreal übernimmt zusätzlich den FBX-Armature-Wurzelknoten.

## Unreal

`ImportAssets.py` nutzt den vorhandenen Legacy-FBX-Pfad mit anschließend wiederhergestelltem Import-Flag. Erstimport oder streng auf die eigenen Quellpfade begrenzte Wiederaufnahme. `RefreshMesh.py` ist die dokumentierte eigene Augenorientierungs-Korrektur, kein Reimport anderer Charaktere. Neue Assets unter `/Game/Characters/Creatures/Zunderlauf`, Art-/Encounter-Daten unter den vorhandenen `/Game/Data`-Verzeichnissen. Keine Physics Assets oder zusätzlichen Gameplay-Kollider.

`BindWorld.py` setzt nur am bestehenden `Slice_Wildkreatur_Optional` die Art, das eigene Encounter-Profil und die optionale kleine Umgebungsbewegung. Identität, Seed, Ausgangsposition und Kollision bleiben erhalten. Kein erneutes Binden auf einen schon umgestellten Actor.

`PokeMonsterCreaturePresentation` ist optional. Der vorhandene Encounter-Actor bleibt zuständig für Kontakt, Interaktion und Persistenz. Der bestehende BattleWidget-Phasenablauf signalisiert Attack/Hit/Faint/Happy an die Darstellung. Regeln, Zufallszahlen und Teamzustände bleiben im bisherigen BattleSession-System. Weltbegegnungen bleiben über der geladenen Karte sichtbar; Arten ohne 3D-Modell behalten ihre vorhandene 2D-UI-Darstellung. Keine neue Arena oder Kamera.

Die Hautgeschwindigkeiten sind 35 cm/s Walk und 60 cm/s Run. Der native Proxy skaliert den Zyklus anhand der tatsächlichen Bewegung. `GroundOffsetCm` gleicht den gemessenen Abstand des Meshfußes zum Modellursprung aus. Nur die Darstellung wird zum Boden projiziert; der bestehende Gameplay-Kollider wird nicht angepasst.

## Prüfungen und Kontrollmedien

- Build/Automation: `Tools/ProjectMaintenance/ProjectQA.py` bei geschlossenem Editor; eigene eindeutige Ergebnislabels verwenden.
- `ValidateWorld.py`: ursprünglicher V5-Art-Vertrag, explizite neue Wild-Bindung, geschützte Dateihashes.
- `MapChecks.py`: alle elf vorhandenen Maps, einschließlich unveränderter Ranger-V3-Prüfung; keine Speicherung.
- `RuntimeReview.py`: sieben Clips und acht Richtungen mit dem tatsächlich vom Wild-Actor erzeugten Mesh; nur PIE-Laufzeitzustand. QHD-Frames und Socketpositionen unter `Saved/ZunderlaufV1`.
- `RunGameplay.py <Label>` / `StartGameplay.py`: bestehende vollständige Enhanced-Input-Fußroute; Original-Dev-Spielstand vorab sichern und abschließend exakt wiederherstellen. `Battle...`-Labels erlauben die kurze Kampf-Wiederholungsroute.
- `ObserveGameplay.py`: separate Aufnahmebeobachtung; darf einen Gameplay-Test nicht ersetzen.
- `PrepareEvidence.py`: optionale Pillow-Nachbearbeitung echter QHD-Bilder zu beschrifteten Ausschnitten und GIF. Kein Echtzeitvideo und keine generierte Grafik. Verwendeter Pillow-Interpreter steht im Prüfbericht.

Alle Kontrollbilder, GIFs, Logs und Spielstand-Testnachweise bleiben im ignorierten `Saved/`. Nur tatsächliche Designreferenzen, Quellen, nötige Exporte, Unreal-Assets, Tests, Werkzeuge und Dokumentation werden versioniert. Technische Prüfung ist keine automatische visuelle Endfreigabe.
