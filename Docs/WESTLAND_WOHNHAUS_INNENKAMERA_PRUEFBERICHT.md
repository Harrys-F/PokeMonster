# Westland-Wohnhaus: Cutaway-Korrektur und Innenkamera-Proof

**Historischer erster Proof.** Die rechte Seiten-Cutaway-Zuordnung und die dauerhaft äußere Bewegungsbasis wurden durch den Folgeauftrag ersetzt. Aktueller Stand: `WESTLAND_WOHNHAUS_INNENSTEUERUNG_PRUEFBERICHT.md`. Die folgenden Messungen beschreiben den damaligen Zwischenstand.

Stand: 03.10.2026. Ausschließlich bestehendes Cottage in Dev_BuildingKitTestMap, keine neue Architektur oder Gasthausarbeit. Kein Staging, Commit oder Push.

## Ausgangsstand und Seitenwand

1. Ausgangs-HEAD: `9132c2d Add Westland building kit V1`; `git status --short` zu Beginn ohne Ausgabe. 651 Ausgangsdateien wurden per SHA-256 erfasst. Der aktuelle HEAD enthält bereits das Gasthaus aus dem früheren Auftrag; es wird nicht weitergebaut oder auf die Innenkamera umgestellt.
2. Bisher ausgeblendete linke Seite: Y=-300 cm, insbesondere `Cottage_WallSolid2m_056`, `Cottage_WallWindowDouble2m_058`, `Cottage_WallSolid2m_060`. Fenster `Cottage_WindowDouble_144`, zugehörige Seitenbalken, Streben, Sockel und der hintere linke Eckpfosten gehörten ebenfalls zum Cutaway.
3. Neue rechte Seite: Y=+300 cm, insbesondere `Cottage_WallSolid2m_068`, `Cottage_WallSolid2m_070`, `Cottage_WallSolid2m_072`. Zugehörige Seitenbalken, Streben, Sockel und hinterer rechter Eckpfosten werden mit ausgeblendet. Die vorderen Eckpfosten bleiben Teil der bereits ausgeblendeten Front. Vollständiger Zuordnungstausch: 18 alte Referenzen entfernt, 17 hinzugefügt; das zusätzliche alte Seitenfenster bleibt nun sichtbar. Keine Geometrie/Actors gelöscht, verschoben oder skaliert, keine Collision geändert.
4. Cutaway-Ergebnis: Außen Dach/Front/beide Seiten sichtbar; innen Dach/Front/rechte Seitenwand verborgen, linke Seitenwand samt Fenster und Rückwand sichtbar. Die vorhandenen maskierten Materialien, CPD Index 0, Collision, Schwellenbox 40×130×200 cm und 4-cm-Hysterese bleiben erhalten.

## Kamera und Übergang

5. Overworld: SpringArm **2500 cm**, FOV **35°**, Rotation **(-55°,-45°,0°)**, Camera Lag aktiv, Geschwindigkeit 6, maximal 180 cm. Player 140 cm, Capsule 28/48 cm, Bewegung 210 cm/s, Flipbooks und Sprite-Skalierung unverändert.
6. Innenraum: feste Ansicht zur gebäudelokalen Türschwellen-+X-Achse, Yaw-Offset 0°, Pitch -50°, Abstand **2000 cm**, FOV weiterhin 35°. Zielpunkt relativ zur InteriorArea (0,0,-70) cm, bei der vorhandenen Rootposition Ziel in Welt (0,0,80) cm. Finale Kamera etwa **(-1285,58,0,1612,09) cm**.
7. Tatsächliche Orientierungsänderung: Yaw **-45° → 0°**, Pitch **-55° → -50°**, Roll an beiden Endpunkten 0°. Quaternion-Slerp verwendet den kurzen Drehweg; keine seitliche Schrägstellung im fertigen Innenzustand.
8. Innenabstand: 1600 cm zunächst in PIE geprüft; Eingang/Raumfläche waren zu groß im Ausschnitt. 2000 cm sind als Wohnhaus-Proof gewählt. Die Bodenfläche und Türschwelle werden damit vollständig lesbar. Die Oberkante des hohen Rückgiebels darf im Ausschnitt angeschnitten bleiben; es wird keine vollständige Außenkomposition aus dem Innenkamera-Proof abgeleitet.
9. Dauer: vollständiger Eintritt und Austritt jeweils **0,4 s**. Bei Umkehr läuft der vorhandene Teilfortschritt zurück, daher ist die verbleibende Dauer entsprechend kürzer.
10. Synchronisation: Der bestehende `CutawayAmount` ist die einzige Fortschrittsquelle. Materialfade verwendet ihn direkt, Kamera einen Smoothstep desselben Werts. Dach/Wand und Kamera starten und enden gemeinsam. Keine zusätzliche Transition, Timer oder zweite Zustandsmaschine im Produktionscode. Der aktivierte Cottage-Cutaway tickt pro Frame; deaktivierte bestehende Gebäude behalten ihren bisherigen Tick.
11. Betreten: Vor der Schwelle bleibt die Außenansicht erhalten. Nach Überschreiten des bestehenden Hysteresebands beginnt gleichzeitig der Fade und die Interpolation der gerenderten Camera-POV zum festen Raumziel.
12. Verlassen: Auf demselben Schwellenmechanismus blendet die Architektur wieder ein und die POV kehrt zur unveränderten laufenden SpringArm-Kamera zurück. Danach liefert `CalcCamera` wieder exakt die normale Berechnung; keine Parameter werden zurückgeraten oder überschrieben.
13. Umdrehen: Wiederholte normale Ein-/Austritte, kurze Tastimpulse, Pause im Hystereseband und diagonale Durchgänge bestanden. Zusätzlich wurden drei echte Umkehrungen während laufender Fades über die vorhandene Enhanced-Input-MoveAction/CharacterMovement-Physik gefahren, ohne Positionssetzen: bei 0,4172 / 0,6111 / 0,5104 Ausblendanteil. Kein Fortschrittsreset, Doppelübergang oder falscher Endzustand. Die zusätzliche zeitgenaue Eingabesimulation ergänzt den vollständigen WASD-Fußweg; sie ist kein Produktionsfeature und bleibt unter Saved/tmp.
14. Diagonale Bewegung: Beide Raumseiten, diagonale Raumwege sowie diagonaler Ein-/Austritt normal erreicht. Der Render-Schwenk verändert die ursprüngliche CameraComponent nicht. Deshalb bleibt die Weltbewegungs-/Interaktionsbasis während und nach dem Übergang -45°; keine unerwartete Richtungsumkehr beim Tastendruck. In der Frontalansicht werden diese unveränderten Weltrichtungen entsprechend diagonal auf dem Bildschirm dargestellt. Es wurde bewusst keine neue Innenraum-Eingabezuordnung eingeführt.
15. Wirkung: Ruhige feste Raumansicht, keine seitliche Kameraverfolgung im Innenraum, Bodenfläche und Eingang gut lesbar; Player in Raummitte und auf beiden Seiten sichtbar. Die bestehende aufrechte Sprite-Fläche bleibt unverändert und wird aus der neuen Richtung stärker perspektivisch verkürzt. Keine Anpassung der Charaktergrafik, keine Einrichtung, keine neue Beleuchtung. Dieser Proof benötigt Harrys spätere Sichtbewertung, bevor er auf weitere Gebäude übertragen wird.

## Prüfungen und Grenzen

16. Vollständiger finaler PIE-Fußweg: normaler PlayerStart → Fassade → vor Schwelle → gerade hinein → Raummitte → linke/rechte Raumseite → diagonale Innenbewegung → gerade hinaus → diagonal hinein/hinaus → drei erneute Ein-/Austritte → kurze Türimpulse → im Türrahmen stehen → hinaus → Rückkehr zum Start. Ohne Teleports/Spawn-Overrides. Screenshots und Live-Messwerte unter `Saved/WestlandInteriorCamera`. Innen bleibt die Kameraposition trotz vieler verschiedener Playerpositionen identisch; rechte Wand verborgen, linke sichtbar. FOV 35° und SpringArm 2500 cm durchgängig bestätigt. Zusätzlicher zeitgenauer Umkehrtest wie oben bestanden.
17. Mac Development Build erfolgreich. Neuer Automationstest `PokeMonster.Player.BuildingInteriorCamera` prüft Opt-in, gemeinsame Fortschrittsquelle, Zwischenansicht, Pause/Umkehr, exakte Außenrückkehr, feste Innenansicht, gebäudelokale Orientierung, FOV/Lag/Sprite-/Interaktionsbasis und sicheren Verlust des Providers. Der erste Testaufbau hatte keine aktivierte Kamera; der isolierte Test wurde mit aktivierter CameraComponent und eigenem WorldContext korrigiert. Bestehender Wohnhaus-Collision-/Material-/Laufweg-Audit mit neuer Konfigurationsprüfung bestanden. Abschließender gesamter Automationstestbestand im frischen separaten Null-RHI-Prozess: **36/36 erfolgreich**, 0 fehlgeschlagen, 0 mit Warnungen, 0 nicht ausgeführt, Exit-Code 0. Darin neuer Kamera-Proof, Player Foundation/ScaleCalibration und sämtliche bisherigen HealingHouse-/Battle-/Encounter-/Save-/Questtests. Map Check nach PIE: 0 Fehler, 0 Warnungen.

Ein vorbereitender Fußlauf wurde durch einen noch wartenden Editor-Automationstest beendet. Nach dessen Abschluss wurde der gesamte Fußweg vom normalen Start erneut bestanden. Der finale komplette Automationstestlauf erfolgt getrennt vom PIE. Lokale Python-Messhelfer mussten an die tatsächlich verfügbaren Unreal-Bindungen angepasst werden; sie verändern keine Projektlogik und werden nicht versioniert.

Healing House V3, Dev_TestMap, originale Blenderquelle, Meshes, Materialien, Dach-/Wandgeometrie, Kollisionsdaten und Gasthaus-Konfiguration bleiben erhalten. Die neue Kameraoption ist standardmäßig false und nur im Wohnhaus aktiviert. Keine Save-/Healing-/Checkpoint-/Quest-/Battleänderung.

18. Vollständige Dateiliste und Git-Status folgen unten. Autorenwerkzeuge ändern ausschließlich Cutaway-/Kamera-Metadaten, damit ein späterer Cottage-Neuaufbau die Korrektur nicht überschreibt. Kein Blender-Neuaufbau oder Mesh-Reimport wurde ausgeführt.
19. `git diff --check`: abschließend Exit-Code 0, keine Ausgabe; zusätzliche Text-/JSON-/Python-Prüfungen bestanden.
20. `git status --short`: folgt unten. Kein Staging, Commit oder Push.

## Vollständige Dateiliste

11 bestehende Dateien geändert:

- `Art/Architecture/Westland/Buildings/WL_Cottage_V1.json`
- `Content/Maps/Dev_BuildingKitTestMap.umap`
- `Docs/ENTSCHEIDUNGEN.md`
- `Docs/TECHNIK.md`
- `Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.cpp`
- `Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.h`
- `Source/PokeMonster/World/PokeMonsterBuildingCutaway.cpp`
- `Source/PokeMonster/World/PokeMonsterBuildingCutaway.h`
- `Tools/Blender/BuildWestlandBuildingKitV1.py`
- `Tools/ImportWestlandBuildingKitV1.py`
- `Tools/ValidateWestlandBuildingKitV1.py`

3 neue Dateien:

- `Docs/WESTLAND_WOHNHAUS_INNENKAMERA_PRUEFBERICHT.md`
- `Source/PokeMonster/Tests/PokeMonsterBuildingCameraTest.cpp`
- `Tools/ConfigureCottageInteriorCamera.py`

Die übrigen **640 von 651** Ausgangsdateien sind SHA-256-bytegleich. Insbesondere sämtliche Heilhaus-/Kit-/Gasthausquellen, Meshes und Materialien, Dev_TestMap, HealingHouse-Testmap und die Gameplaydateien außerhalb der ausdrücklich erweiterten Kamera-/Cutaway-Klassen. Der Cottage-Bauplan behält alle Modulreferenzen, Instanzzahlen, Positionen, Rotationen und Skalierungen.

## Git-Status

```text
 M Art/Architecture/Westland/Buildings/WL_Cottage_V1.json
 M Content/Maps/Dev_BuildingKitTestMap.umap
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
 M Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.cpp
 M Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.h
 M Source/PokeMonster/World/PokeMonsterBuildingCutaway.cpp
 M Source/PokeMonster/World/PokeMonsterBuildingCutaway.h
 M Tools/Blender/BuildWestlandBuildingKitV1.py
 M Tools/ImportWestlandBuildingKitV1.py
 M Tools/ValidateWestlandBuildingKitV1.py
?? Docs/WESTLAND_WOHNHAUS_INNENKAMERA_PRUEFBERICHT.md
?? Source/PokeMonster/Tests/PokeMonsterBuildingCameraTest.cpp
?? Tools/ConfigureCottageInteriorCamera.py
```

Nach eigener Sichtprüfung ist dies ein sinnvoller Git-Sicherungspunkt. Folgender gezielter Befehl würde ausschließlich die 14 Projektdateien stagen; er wurde nicht ausgeführt:

```sh
git add -- \
  Art/Architecture/Westland/Buildings/WL_Cottage_V1.json \
  Content/Maps/Dev_BuildingKitTestMap.umap \
  Docs/ENTSCHEIDUNGEN.md \
  Docs/TECHNIK.md \
  Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.cpp \
  Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.h \
  Source/PokeMonster/World/PokeMonsterBuildingCutaway.cpp \
  Source/PokeMonster/World/PokeMonsterBuildingCutaway.h \
  Tools/Blender/BuildWestlandBuildingKitV1.py \
  Tools/ImportWestlandBuildingKitV1.py \
  Tools/ValidateWestlandBuildingKitV1.py \
  Docs/WESTLAND_WOHNHAUS_INNENKAMERA_PRUEFBERICHT.md \
  Source/PokeMonster/Tests/PokeMonsterBuildingCameraTest.cpp \
  Tools/ConfigureCottageInteriorCamera.py
```

Screenshots, Messdaten, Automationsergebnisse und temporäre Eingabehelfer unter Saved/tmp gehören nicht in Git. Kein Staging, Commit oder Push.
