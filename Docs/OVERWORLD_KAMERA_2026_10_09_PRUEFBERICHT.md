# Feste Overworld-Kamera – Prüfbericht vom 09.10.2026

**Aktueller Folgeauftrag:** Der Außenabstand ist wieder **2500 cm** statt 2000 cm. Alle übrigen Kamerawerte bleiben erhalten. Die folgenden ursprünglichen Messungen und Tests beziehen sich auf den früheren 2000-cm-Durchlauf; der aktuelle Prüfstand steht im Nachtrag am Ende.

## Ausgangsstand und Umfang

HEAD: `20b6daf12ec56a1b22faa1a21c0981807ca47240` – `Character: refine Young Trainer clothing and barefoot feet V1`.

Der Arbeitsbaum war bereits durch `Art/Characters/YoungTrainer/Source/YoungTrainer_ClothingFeet_V1.blend` verändert. Diese Nutzeränderung wurde nicht angefasst; ihre SHA-256 ist vor und nach der Aufgabe identisch: `782b36ba2ce3986fdc43ffa013a378cd5d56371bdd84a329eca1680c2e4310d5`.

Umgesetzt ist ausschließlich die Kameraanpassung im vorhandenen Player-System, begleitet von Regressionstests und Dokumentation. Keine Map, Blueprint-, Sprite-, Blender- oder sonstige Contentdatei wurde geändert. Keine Staging-Aktion, kein Commit, kein Push.

## Tatsächliche Architektur und Overrides

Der geöffnete Editor zeigt `Dev_TestMap`. Die Kamera besteht aus `APokeMonsterPlayerCharacter`, `CameraBoom` (SpringArm) und `FollowCamera` (CameraComponent). Der native Konstruktor war die maßgebliche Außenkonfiguration. Der lesende Unreal-Asset-Audit vor und nach dem Build findet keine Blueprint-Assets unter `/Game`, damit insbesondere keine Player-Blueprint-Overrides. `Dev_TestMap`, `Dev_HealingHouseTestMap` und `Dev_BuildingKitTestMap` verwenden `PokeMonsterGameMode` mit dem nativen `PokeMonsterPlayerCharacter`; keine dieser Maps enthält platzierte Playerinstanzen mit abweichenden Werten.

Der vorhandene `CalcCamera`-Pfad mischt bei aktivierten Gebäude-Innenkameras eine raumfeste Ansicht ein. Diese Konfigurationen und ihre Relocation-, Fade-, Cutaway- und Bewegungsbasis-Übergänge bleiben unverändert. Der neue Standard gilt für die normale Außenansicht; beispielsweise bleibt das Expanded Healing House innen bei 2600 cm, FOV 35°, Pitch −50°, lokalem Yaw 0°.

## Endgültige Außenwerte

| Parameter | Vorher | Jetzt |
| --- | --- | --- |
| SpringArm-Abstand | 2500 cm / 25 m | 2000 cm / 20 m |
| Pitch | −55° | −55° |
| Yaw | −45° | −45° |
| Roll | 0° | 0° |
| Projektion | Perspektive | Perspektive |
| Horizontaler FOV | 35° | 35° |
| TargetOffset, Welt-Z über Capsule-Zentrum | 0 cm | 35 cm |
| Absolute SpringArm-Rotation | aus | an |
| Position Camera Lag | an | an |
| Lag Speed | 6 | 12 |
| Maximaler Lag-Abstand | 180 cm | 45 cm |
| Lag Substepping / maximaler Zeitschritt | Engine-Default an / 1⁄60 s | explizit an / 1⁄60 s |
| Rotations-Lag | aus | explizit aus |
| SpringArm-Kollision | aus | aus |
| Controllerrotation / Pitch-, Yaw-, Roll-Vererbung | aus | aus |

Der Yaw −45° ist die vorherige horizontale Blickrichtung, keine zusätzliche isometrische Drehung. Absolute Rotation verhindert zusätzlich ein Mitdrehen bei einer Actorrotation. Die feste Ausrichtung bleibt beim Wechsel der acht Sprite-Blickrichtungen erhalten.

Der kürzere Arm dient dem ausdrücklich gewünschten Figurenanteil von 10–13 Prozent. Er zeigt gegenüber dem vorherigen 2500-cm-Stand weniger Welt; ein weiter entfernter Arm würde bei gleichem FOV die Figur wieder kleiner darstellen. Keine Skalierung von Figur oder Welt als Ausgleich.

Die bestehende Bewegungsumrechnung nutzt bereits Camera Forward/Right auf der horizontalen Ebene. Oben/rechts führen auf dem Bildschirm nach oben/rechts; diagonale Eingaben bleiben normalisiert. Bewegung, acht Animationsrichtungen, Fußpivot, Interaktionsreichweite und Gameplay wurden nicht verändert. Sichtbare Körperhöhe weiterhin 140 cm, Collision-Capsule weiterhin Radius 28 cm / Halbhöhe 48 cm, Geschwindigkeit weiterhin 210 cm/s.

## Messung und Tests

Der neue Foundation-Test verwendet die tatsächliche SpringArm-/CameraComponent-Kette in einer isolierten Unreal-Testwelt. Nach Einschwingen projiziert er den Fußpunkt und den 140-cm-Scheitel mit dem vorhandenen perspektivischen FOV in ein 16:9-Spielbild. Ergebnis: **11,209 Prozent Körperhöhe**, Körpermittelpunkt **Y = 0,5089** (50,89 Prozent von oben). Transparente Sprite-Ränder und Collisionhöhe zählen nicht zum Körpermaß. Andere Seitenverhältnisse ändern den Anteil bei unverändertem horizontalem FOV; dies ist keine Messung aus einem gerenderten PIE-Screenshot.

Geprüft sind alle acht Inputrichtungen, normalisierte Bewegung, unveränderter Kamerawinkel bei Blickrichtungswechsel und Actorrotation, kurzer begrenzter Lag bei 210 cm/s und Einschwingen nach dem Anhalten. Die bereits deaktivierte SpringArm-Kollision bleibt deaktiviert und kann daher keine kollisionsbedingte Armverkürzung auslösen. Das macht verdeckende Baumkronen nicht durchsichtig.

- Mac Development Editor Build erfolgreich, keine Compile Errors. Abschließender Build: `Result: Succeeded`, Exit 0.
- Vollständiger vorhandener `PokeMonster`-Automationstestbestand: **38/38 erfolgreich, 0 fehlgeschlagen, 0 mit Warnungen, 0 nicht ausgeführt**, Exit 0.
- Darunter Player Foundation, Scale Calibration, Building Interior Camera und Relocated Interior sowie bestehende Gameplay-/Save-/Questtests.
- Ein erster Lauf hatte zwei numerisch zu strenge neue Richtungsvergleiche. Nur deren Vergleichstoleranz wurde auf 0,0001 korrigiert; der abschließende vollständige Lauf ist grün.
- Frischer Unreal-Python-Commandlet-Audit nach dem Build bestätigt die endgültigen nativen Defaults und Pawn-Zuordnungen. Keine Assets gespeichert.

Lokale Rohbelege liegen im ignorierten `Saved/OverworldCamera20261009`: `BuildFinal.log`, `AutomationFinal.log`, `AutomationFinal/index.json`, `AssetAudit.json`, `AssetAuditFinal.json`, `BeforeHead.txt`, `BeforeStatus.txt` und `BeforeFiles.json`.

## Grenze der visuellen Prüfung

**Eine visuelle PIE-Prüfung ist mit den hier verfügbaren Werkzeugen nicht gelungen.** Der Editor lässt sich beobachten und zeigt die gespeicherte `Dev_TestMap`; Spielstart über Bedienung und Tastenkürzel führt jedoch nicht zu einer bestätigten PIE-Sitzung. Eine nutzbare Unreal-MCP-/Python-Remote-Verbindung ist nicht erreichbar. Die isolierten Automationstests sind deshalb ausdrücklich kein visueller Fußlauf durch die Map.

Figurenlesbarkeit, gemeinsame Sicht auf Dächer/Fassaden, Baumverdeckungen und Interaktionspunkte in der tatsächlichen gerenderten Szene bleiben offen. Auch die optische Gesamtkomposition des Heilhauses wurde nicht als bestanden bewertet. Gebäudespezifische Innenkamera-Übergänge sind automatisiert geprüft, ihre unveränderte Innenansicht wurde in dieser Aufgabe nicht visuell neu beurteilt.

Für die Sichtprüfung den Editor regulär neu starten, damit die neu gebauten Konstruktor-Defaults geladen werden, `Dev_TestMap` öffnen und PIE starten. In allen acht Richtungen laufen, am Haus und an Baumgruppen vorbeigehen und prüfen, dass kein Rotations-/Zoomsprung auftritt. Falls gewünscht die HealingHouse-Testmap anschließend separat für den Innenübergang prüfen. Es wurden keine ungesicherten Editorinhalte verworfen oder ein Editorprozess zwangsweise beendet.

## Dateien und Git-Prüfung

Acht bestehende Dateien gezielt geändert:

- `Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.cpp`
- `Source/PokeMonster/Tests/PokeMonsterPlayerFoundationTest.cpp`
- `Source/PokeMonster/Tests/PokeMonsterScaleCalibrationTest.cpp`
- `Source/PokeMonster/Tests/PokeMonsterBuildingCameraTest.cpp`
- `Source/PokeMonster/Tests/PokeMonsterRelocatedInteriorTest.cpp`
- `Docs/GRAFIKSTIL.md`
- `Docs/TECHNIK.md`
- `Docs/ENTSCHEIDUNGEN.md`

Neu: `Docs/OVERWORLD_KAMERA_2026_10_09_PRUEFBERICHT.md`.

Von 999 zu Beginn erfassten versionierten Dateien sind ausschließlich diese acht durch die Aufgabe verändert; die übrigen 991 sind bytegleich zum tatsächlichen Arbeitsstand am Anfang, einschließlich der bereits modifizierten Blenderquelle und sämtlicher Maps/Assets.

`git diff --check`: erfolgreich, keine Ausgabe. Abschließendes `git status --short`:

```text
 M Art/Characters/YoungTrainer/Source/YoungTrainer_ClothingFeet_V1.blend
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/GRAFIKSTIL.md
 M Docs/TECHNIK.md
 M Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.cpp
 M Source/PokeMonster/Tests/PokeMonsterBuildingCameraTest.cpp
 M Source/PokeMonster/Tests/PokeMonsterPlayerFoundationTest.cpp
 M Source/PokeMonster/Tests/PokeMonsterRelocatedInteriorTest.cpp
 M Source/PokeMonster/Tests/PokeMonsterScaleCalibrationTest.cpp
?? Docs/OVERWORLD_KAMERA_2026_10_09_PRUEFBERICHT.md
```

Ein sinnvoller Sicherungspunkt folgt nach der noch offenen visuellen Prüfung. Dieser gezielte Befehl würde ausschließlich die Dateien dieser Kameraaufgabe stagen und die bestehende Blenderänderung auslassen; **nicht ausgeführt**:

```sh
git add -- Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.cpp Source/PokeMonster/Tests/PokeMonsterPlayerFoundationTest.cpp Source/PokeMonster/Tests/PokeMonsterScaleCalibrationTest.cpp Source/PokeMonster/Tests/PokeMonsterBuildingCameraTest.cpp Source/PokeMonster/Tests/PokeMonsterRelocatedInteriorTest.cpp Docs/GRAFIKSTIL.md Docs/TECHNIK.md Docs/ENTSCHEIDUNGEN.md Docs/OVERWORLD_KAMERA_2026_10_09_PRUEFBERICHT.md
```

## Nachtrag: Außenabstand wieder 2500 cm

Auf Harrys Folgeauftrag vom 09.10.2026 wurde ausschließlich `CameraBoom->TargetArmLength` von 2000 auf **2500 cm** gesetzt; der Kommentar zur projizierten Körperhöhe wurde berichtigt. Pitch −55°, Yaw −45°, Roll 0°, FOV 35°, Perspektive, Fokus +35 cm, absolute Rotation, Lag 12/maximal 45 cm, Substepping und alle übrigen Einstellungen bleiben unverändert. Keine Map-/Asset-/Gameplayänderung.

Die drei bestehenden Abstandserwartungen und die Körperprojektionsprüfung wurden auf den wiederhergestellten Standard angepasst; Gebäude-Innenabstände bleiben erhalten. Die tatsächliche Component-Projektion beträgt bei 16:9 jetzt **8.983 Prozent**, Körpermittelpunkt Y = **0.5073**. Der vorherige 10–13-Prozent-Zielbereich ist durch diesen Folgeauftrag ersetzt.

Mac Development Editor Build: **erfolgreich**, keine Compile Errors, Exit 0. Anschließend vollständiger `PokeMonster`-Automationstestbestand: **38/38 erfolgreich**, 0 fehlgeschlagen, 0 mit Warnungen, Exit 0. Rohbelege im ignorierten `Saved/OverworldCamera2500/Build.log` und `Automation/index.json`. Keine neue visuelle PIE-Prüfung im Rahmen dieser Abstandsrücksetzung.

Geändert wurden derselbe PlayerCharacter, die vier oben aufgeführten Testdateien und `GRAFIKSTIL.md`, `TECHNIK.md`, `ENTSCHEIDUNGEN.md` sowie dieser Bericht. Bestehende Nutzeränderungen bleiben erhalten. `git diff --check` erfolgreich; kein Commit und kein Push. Den Editor vor der Sichtprüfung neu starten, damit die neuen Konstruktor-Defaults geladen werden. Der oben genannte gezielte Git-add-Befehl bleibt für einen späteren Sicherungspunkt gültig und wurde nicht ausgeführt.
