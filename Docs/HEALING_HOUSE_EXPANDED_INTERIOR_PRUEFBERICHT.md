# Healing House – Expanded Interior Prototype: Prüfbericht

Prüfdatum: 04.10.2026. Implementierter, spielbarer Technik-Prototyp; **Harrys manuelle Sichtfreigabe steht noch aus**. Keine neue Detailgestaltung oder finale Innenraumgrafik.

## Ausgangsstand und Erhalt

1. Ausgangs-HEAD **`32bba08 Add Westland village core V1`**. Westland Village Core V1 ist damit committed.
2. `git status --short` zu Beginn: keine Ausgabe, sauber. Ausschließlich dieser Auftrag wurde umgesetzt. Kein Commit, kein Push, nichts gestaged.
3. Kleine opt-in-Erweiterung von `PokeMonsterBuildingCutaway`; kein neues Gebäudeframework. Außen- und Innenraum bleiben auf derselben Map. Der Player wird ausschließlich durch die reguläre Türübergangslogik versetzt; sämtliche PIE-Fußwege verwenden Enhanced Input ohne manuelle Test-Teleports oder Spawn-Overrides. Isolierte Automationstests dürfen ihre Testpositionen setzen.
4. Heilhaus-Hauptkörper weiterhin **9,00 × 9,30 m**, nominaler First **6,40 m** (V3-Dachgeometrie ca. 6,389 m). Freie Außentür weiterhin **1,50 × 2,15 m**. Außenarchitektur, Fenster, Dach, Vorbau, Schild, Außendressing, Eingangslaterne und deren Assetzuweisungen/Transforms bleiben gleich.

Ein Vorher-/Nachher-Audit umfasst 295 bestehende und jetzt 337 Map-Actors. Kein bestehender Actor gelöscht. 96 bestehende Actors erhalten die vorgesehene Cutaway-/Innenraumkonfiguration oder neue Innenposition/Ordner; keine Außenarchitektur verändert. 42 zusätzliche Architekturinstanzen. Alle bestehenden Mesh-, Material-, Sprite-, Blender- und FBX-Dateien bleiben bytegleich.

## Raum und Übergang

5. Neuer Raum: **12,00 m Breite Y × 10,00 m Tiefe X**, 3,00 m Wandhöhe. Nominaler Rahmen 120 m² statt 83,7 m² der Außenhülle: **+43,4 %**. Das ist ein Rahmenvergleich, keine Behauptung über netto freie Möbel-/Lauffläche. Grobe lichte Wandabstände etwa 11,80 × 9,75 m. Boden inklusive Wandauflage 12,40 × 10,40 m, Bodenoberkante Z=0.
6. Raumzentrum **(20000,0,150) cm**. Er liegt rund 200 m vom äußeren Gebäude entfernt. Der Türversatz beträgt **19950 cm / 199,50 m** entlang X. Die Außenkamera sieht den Raum nicht; die frontale Innenkamera zeigt keine Außenwelt. Keine neuen weitreichenden Schattenwerfer. Kein zweites äußeres Heilhaus.
7. Korrespondierende Türzentren: außen **(-450,0,107,5) cm**, innen **(19500,0,107,5) cm**, beide inward +X / Yaw 0°. Beide nicht kollidierenden Schwellenboxen haben Extent (20,75,107,5) cm und 4-cm-Hysterese. Passage innen ebenfalls 150 × 215 cm. Innerer Türwand-Blocker **30 cm dick**, identisch zum bestehenden äußeren Querschnitt.
8. `MapDoorwayPosition` bildet die tatsächliche Position quelltürlokal auf die Zieltür ab. X-, Seiten- und Höhenoffset bleiben erhalten. Beim Austritt dieselbe inverse Abbildung. Keine immer neu addierte Schätzung und kein fester Spieler-Spawn. Ein Capsule-Sweep verhindert Platzierung in Zielcollision. Ablehnung entfernt die Maske und wartet auf eine neue Schwellenquerung. Externes Checkpoint-/Load-Versetzen auf eine der beiden Seiten wird erkannt, ohne einen zweiten Versatz hinzuzufügen.
9. Vorhandener Dach-/Front-Cutaway: **0,4 s**, reversible Interpolation. Zusätzliche schwarze CameraManager-Maske nur im relocated Modus, Smoothstep über CutawayAmount 0,3–0,7, vollständig schwarz bei 0,5. Nominal **0,16 s Maskenfenster plus Halteframes**: mindestens ein schwarzer Frame vor dem Ortswechsel und ein vollständig schwarzer Wechsel-Frame. Die reale Dauer hängt von der Framerate ab. Der Kamera-Ortswechsel liegt vollständig unter der Blende; keine sichtbare 199,5-m-Kamerafahrt. Im PIE-Protokoll waren alle **42 Ortswechsel vor und nach dem Cut vollständig maskiert**. Langsame Editorframes können die Blende verlängern; die manuelle Prüfung sollte zusätzlich das subjektive Übergangsgefühl beurteilen.
10. Innenkamera tatsächlich in PIE verglichen: **2200, 2400 und 2600 cm**. Gewählt **2600 cm / FOV 35° / Pitch −50° / lokaler Yaw 0°**, fester Fokus Welt **(19940,0,80) cm**. 2200/2400 schneiden mehr vom Eingangs-/Vorderbereich ab. 2600 bietet Rand für Player und Tür sowie Übersicht über Empfang, Betten und Sitzbereich. Außen unverändert **2500 cm / 35° / −55° / −45°**, Lag 6/maximal 180 cm.

## Einrichtung und Gameplay

V3-Props werden als Gruppen versetzt, nicht neu modelliert oder skaliert: kleine/große Liege, Bücher-/Kräuterregal samt Inhalt, Kräutertisch samt Behandlungsmaterial, Teppich, Sitzbank/-tisch, Bücher und getrocknete Kräuter. Der bestehende Tresenmesh wird als zusätzliche visuelle Instanz wiederverwendet; der vorhandene funktionale Tresenblocker und die echte Hüterin ziehen in den Raum. Ein vorhandenes Kaminmodul markiert die Kaminzone, ohne Feuer-VFX oder neue Lichtstimmung. Die zwei bestehenden Innenlichtquellen folgen ihren Bereichen mit unveränderten Lichtwerten. Möbel und Interaktion behalten die vorhandenen Collision-/Visibility-Einstellungen.

11. Gehaltenes **W** über Eintritt, außerdem **W+D** über Eintritt und **W+A/W+D** im Innenraum geprüft. Kein Input-Reset, StopMovement oder Gameplaylock während des Ortswechsels. Geschwindigkeit maximal gemessen **210 cm/s**; Unit-Test prüft den unveränderten Geschwindigkeitsvektor direkt am Cut. Die bisherige äußere Bewegungsbasis bleibt bis zum Innen-Endpunkt, anschließend der vorhandene 250-Grad/s-Blend (45 Grad in **0,18 s**). Beim Austritt umgekehrt. Acht Richtungen, 140-cm-Figur, Sprite-/Pivot-/Collisionwerte und 150-cm-Interaktionsreichweite unverändert. Aus dieser Außenkamerabasis bedeutet W+A eine seitliche Weltrichtung; deshalb ist nicht jede Tastenkombination von derselben Startposition ein Türdurchgang.
12. Diagonaler Eintritt mit W und beide mittigen diagonalen Austrittsrichtungen **S+A / S+D** bestanden. Gerade Ein-/Austritte ebenfalls bestanden. Physische Türpfosten bleiben kollidierend; seitlich dagegenzulaufen wird nicht als gültige freie Passage behandelt.
13. Schnelle Schwellenumkehr während Teilfade (gemessener Startfortschritt ca. **0,345**) kehrt wieder zum korrekten Außenzustand zurück. Je nach bereits zurückgelegtem Fußweg kann der Mittelpunkt noch erreicht werden und eine verdeckte Hin-/Rückversetzung stattfinden. Kein hängenbleibender Fade oder falscher Kamera-/Inputendpunkt. Ein isolierter Unit-Test prüft zusätzlich die frühe Umkehr vor dem Mittelpunkt ohne Relocation.
14. **Zehn aufeinanderfolgende vollständige Ein-/Austrittsrunden bestanden**; insgesamt in derselben PIE-Sitzung **21 Eintritte / 21 Austritte**. Alle zehn Endpunkte der abschließenden Serie geprüft. Absolute Türabbildung in Automation zusätzlich 100 Roundtrips für drei Seiten-/Bodenoffsets ohne Drift über 0,001 cm. Tatsächliche Fußbewegung zwischen PIE-Ablesungen wird separat berücksichtigt, nicht fälschlich als Mappingfehler gewertet. Kein Bodenfall, kein Dauerschwarz, am Ende normale Außenkamera und Basis −45°.
15. **Hüterin / Heal / RestPoint / Checkpoint / Save in echtem PIE bestanden.** Ein regulärer bestehender Testkampf erzeugte reale Schäden: Teammitglied 1 vor Rast 0/52 HP, Mitglied 2 15/47 HP sowie verbrauchte PP. Zu Fuß zur Hüterin, korrekte Blickrichtung, reguläre E-Interaktion und bestehender mehrseitiger Dialog. Danach beide volle HP und sämtliche bekannten Moves volle PP. Dev-Save geschrieben, Checkpoint-ID `Dev_HealingHouse` und exakte neue Rastposition (20324,390742; −3,751136; 50,149998) cm in der Save-Datei geprüft. Save-/Checkpoint-Deserialisierung und Niederlagenrückkehr werden zusätzlich durch die bestehenden erweiterten Automationstests geprüft. Keine Healing-/Save-/Quest-/Battlelogik umgeschrieben. Der vorherige persönliche Dev-Save wurde nach den Tests **bytegleich wiederhergestellt**, SHA-256 `f7ef30aef1fdeb0d41d3fe8b4ddda541b0d3be1fe3640cc67c0ad7dd50125c74`.
16. **Wohnhaus-Regression bestanden**: normaler PIE-Start in `Dev_BuildingKitTestMap`, zu Fuß hinein, Raumzentrum, Tür und hinaus. Bestehendes In-place-System, 2000-cm-Innenkamera, lokale Basis 0° innen / −45° außen; Cutaway-Endpunkte 1/0. Kein räumlicher Versatz.
17. **Gasthaus-Regression bestanden**: zu Fuß vom Wohnhaus über die bestehende Verbindung zum Inn, hinein, diagonale Bewegung durch Gastraum und Rückflügel, zurück zur Tür und hinaus. Bestehendes In-place-System, 2200-cm-Innenkamera und bisherige L-Regionen unverändert. FOV, Cutaway und Steuerungsendpunkte korrekt. Die BuildingKit-Testmap wurde nicht gespeichert oder geändert.

## Gefundene Probleme und Prüfung

Ein erster Autorenschritt verwendete falsch angeordnete Python-Rotator-Argumente; benannte `pitch/yaw/roll` korrigieren Wand-/Balken-/Hüterin-Ausrichtung. Der größere Tiefengrundriss wurde nach dem Spielkamera-Vergleich in den jetzigen breiteren 12×10-m-Raum und leicht eingangsnahen Fokus überführt. Ein zunächst 20 cm dicker innerer Türblocker erlaubte Eckpositionen, die außen bei 30 cm Wanddicke kollidierten; beide Querschnitte stimmen jetzt überein. Eine abgelehnte Relocation durfte keine wiederholte Schwarzauslösung erzeugen; Ablehnungslatch und Rückkehr zum aktuellen Seiten-Endpunkt sind gezielt getestet.

Die Fußtest-Steuerung wurde nach einem zu frühen Ablesen des letzten Basis-Blends auf den tatsächlichen Endpunkt umgestellt. Eine zu randnahe Diagonalroute traf erwartungsgemäß den Pfosten; die abschließende Zehnerserie verwendet beide mittigen Diagonalquerungen. Diese Testkorrekturen lockern weder Collision noch Geschwindigkeit oder Türmaß. Frühere fehlgeschlagene Diagnoseproben bleiben in lokalen Arbeitsprotokollen nachvollziehbar.

18. **Mac Development Editor Build erfolgreich** nach den C++-Änderungen. Vollständiger Automationbestand **38/38 Success**, 0 Fehler/0 nicht ausgeführt, einschließlich Player Foundation/ScaleCalibration/BuildingInteriorCamera, HealingHouse Layout/CollisionAndCutaway/RestCheckpointSaveAndDefeat, neuem `PokeMonster.Building.RelocatedInterior.MappingAndTransition` und allen Battle-/Inventory-/Quest-/Save-/Checkpoint-Tests. Ein Testreport enthält zwei Engine-Hintergrundwarnungen zum optionalen iOS-Tool `idevice_id` (Bad CPU type), keine Testassertion oder Projektwarnung. **Map Check 0 Fehler / 0 Warnungen.** Gespeicherte Geometrie-/Material-/Missing-Asset-Prüfung bestanden; echte Capsule-Sweeps prüfen freie Innenwege, Möbelblocking, Tür und Sichttrace zur Hüterin. Neue gezielte Automation prüft Mapping, zehn Übergänge, frühen Reverse, vollständige Maske, Geschwindigkeit/Input, Checkpoint-Erkennung und blockiertes Ziel.

## Dateien und Review

19. **8 bestehende Dateien geändert, 5 neue Dateien**:

| Status | Pfad |
| --- | --- |
| Geändert | `Content/Maps/Dev_HealingHouseTestMap.umap` |
| Geändert | `Source/PokeMonster/World/PokeMonsterBuildingCutaway.h` |
| Geändert | `Source/PokeMonster/World/PokeMonsterBuildingCutaway.cpp` |
| Geändert | `Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.h` |
| Geändert | `Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.cpp` |
| Geändert | `Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp` |
| Geändert | `Docs/TECHNIK.md` |
| Geändert | `Docs/ENTSCHEIDUNGEN.md` |
| Neu | `Source/PokeMonster/Tests/PokeMonsterRelocatedInteriorTest.cpp` |
| Neu | `Tools/BuildHealingHouseExpandedInterior.py` |
| Neu | `Tools/ValidateHealingHouseExpandedInterior.py` |
| Neu | `Tools/TestHealingHouseExpandedPIE.py` |
| Neu | `Docs/HEALING_HOUSE_EXPANDED_INTERIOR_PRUEFBERICHT.md` |

Von 668 ursprünglich erfassten Projektdateien bleiben **660 bytegleich**, darunter sämtliche Kunstassets, Blenderquellen, `Dev_TestMap`, `Dev_BuildingKitTestMap`, `Dev_WestlandVillage` und alle Gameplayquellen außerhalb der gezielten Kamera-/Cutaway-Anbindung. Keine neuen Content-Assets außer der Bearbeitung der bestehenden Heilhaus-Map; neue Architektur sind Map-Instanzen vorhandener Assets. Keine AGENTS-/Build-/Input-/Konfigurationsänderung.

20. Sechs aktuelle lokale Review-Aufnahmen, **nicht versioniert**, unter:

`/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/HealingExpanded/Review/Final/`

- `01_Exterior.png`
- `02_BeforeEntry.png`
- `03_Interior.png`
- `04_Healer.png`
- `05_BedsAndSeating.png`
- `06_ExitView.png`

Weitere Vergleichsbilder für 2200/2400 cm sowie Wohnhaus/Inn bleiben im übergeordneten Reviewordner. Native PIE-Screenshots zeigen die tatsächliche Spielkamera; sie enthalten standardmäßig keine UMG-Oberfläche. Lauf-/Übergangs-/Heilbelege: `PIERoute.json`, `Frames.jsonl`, `TransitionSummary.json`, `BuildingRegression.json`, `MapAudit.json`, `ActorPreservation.json`, `Automation/index.json`, alle unter ignoriertem `Saved/HealingExpanded`. Build- und Editorlogs liegen lokal unter `/private/tmp/HealingExpanded`.

21. `git diff --check`: abschließend ohne Ausgabe erfolgreich. Neue Markdown-/Python-/C++-Dateien zusätzlich auf Syntax beziehungsweise Whitespace und letzte Newline geprüft.
22. Endgültiges `git status --short`:

```text
 M Content/Maps/Dev_HealingHouseTestMap.umap
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
 M Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.cpp
 M Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.h
 M Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp
 M Source/PokeMonster/World/PokeMonsterBuildingCutaway.cpp
 M Source/PokeMonster/World/PokeMonsterBuildingCutaway.h
?? Docs/HEALING_HOUSE_EXPANDED_INTERIOR_PRUEFBERICHT.md
?? Source/PokeMonster/Tests/PokeMonsterRelocatedInteriorTest.cpp
?? Tools/BuildHealingHouseExpandedInterior.py
?? Tools/TestHealingHouseExpandedPIE.py
?? Tools/ValidateHealingHouseExpandedInterior.py
```

Nach Harrys Sichtprüfung ist dies ein sinnvoller Git-Sicherungspunkt. Der folgende gezielte Stage-Befehl ist nur ein Vorschlag und wurde **nicht ausgeführt**:

```sh
git add -- Content/Maps/Dev_HealingHouseTestMap.umap Docs/TECHNIK.md Docs/ENTSCHEIDUNGEN.md Docs/HEALING_HOUSE_EXPANDED_INTERIOR_PRUEFBERICHT.md Source/PokeMonster/World/PokeMonsterBuildingCutaway.h Source/PokeMonster/World/PokeMonsterBuildingCutaway.cpp Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.h Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.cpp Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp Source/PokeMonster/Tests/PokeMonsterRelocatedInteriorTest.cpp Tools/BuildHealingHouseExpandedInterior.py Tools/ValidateHealingHouseExpandedInterior.py Tools/TestHealingHouseExpandedPIE.py
```

Manuelle Prüfung: `Dev_HealingHouseTestMap` mit dem aktualisierten Editor-Build öffnen, normal Play starten, W über die Türschwelle halten, Innenraum/Hüterin und Rückweg prüfen. Der Prototype ist technisch geprüft, die endgültige Beurteilung von Raumgefühl, Lesbarkeit und Übergangslänge bleibt Harry vorbehalten. Keine weitere Gestaltung oder Erweiterung vor dieser Sichtprüfung.
