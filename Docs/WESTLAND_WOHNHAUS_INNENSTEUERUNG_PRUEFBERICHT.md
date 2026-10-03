# Westland-Wohnhaus: Innensteuerung und Cutaway-Folgeprüfung

Stand: 03.10.2026. Fortsetzung des offenen Innenkamera-Proofs; keine Gasthausarbeit, kein Staging, Commit oder Push.

## Ergebnis in den 18 angeforderten Punkten

1. **Ausgangs-HEAD:** `9132c2d Add Westland building kit V1`. Ausgangsbaum bewusst nicht sauber: 11 geänderte und 3 neue Dateien des noch offenen Kamera-Proofs. Dieser Stand wurde erhalten und gezielt fortgesetzt.
2. **Cutaway alt → neu:** 75 → 58 explizite Actor-Referenzen. Entfernt wurden ausschließlich die 17 rechte Seiten-Referenzen unten; keine neuen Occluder hinzugefügt. Die bisher sichtbare linke Seite bleibt sichtbar. Die vollständige finale Liste steht weiter unten.
3. **Vorderwand:** Kameraseitige Front bei lokal X=-300 cm: WindowArch-Wände 036/040, Door-Wand 038, Frontbalken, Frontgiebel, vordere Pfosten/Sockel, Türrahmen/-blatt, Frontfenster und Vorbau. Dachpaneele, Traufen, First und der Dachkamin bleiben ausblendbar. Die Front passt zur raumfesten Ansicht entlang +X.
4. **Seiten/Rückwand:** Y=-300 und Y=+300 samt seitlichem Fachwerk/Sockel, hinteren Eckpfosten und linkem Fenster bleiben sichtbar. Rückwand X=+300 ebenfalls sichtbar. Die pro Gebäude konfigurierte Actor-Liste bleibt die einzige Sichtbarkeitsregel; keine automatische Seitenregel oder Raytracing-Lösung.
5. **Außensteuerung:** Unveränderte horizontale CameraComponent-Basis mit Yaw -45°. W weist entlang (+X,-Y), D entlang (+X,+Y). SpringArm 2500 cm, Pitch -55°, FOV 35°, Lag 6/maximal 180 cm bleiben erhalten.
6. **Innensteuerung:** Horizontale Projektion der konfigurierten Raumkamera, hier Yaw 0°. W=+X/in den Raum, S=-X/zum Eingang, A=-Y/Bild links, D=+Y/Bild rechts. Keine Bewegungs-Z-Komponente; feste Kamera 2000 cm, Pitch -50°, FOV 35° bleibt erhalten.
7. **Umschaltung:** Ein gemerkter zuletzt erreichter Kamera-Endpunkt genügt. Innenbasis wird erst bei CutawayAmount=1 aktiviert; Außenbasis erst bei CutawayAmount=0 nach dem vollständigen Rückschwenk. Während der Kamerafahrt bleibt die bisher erreichte Basis erhalten. Der 0,4-s-Kamera-/Materialfade bleibt unverändert. Anschließend dreht die Eingabebasis mit 250 Grad/s, also 45 Grad in 0,18 s.
8. **Gehaltenes W:** Regulärer Fußweg vom PlayerStart, passende Annäherung an die Tür, dann durchgehend Enhanced-Input-W-Vektor während Einlauf und Übergang. Keine Eingabeunterbrechung, kein StopMovement und kein Speed-Reset. Gemessene Geschwindigkeit während des Schwenks und Basis-Blends konstant 210 cm/s (numerische Rundung kleiner 0,000001 cm/s). Erst nach vollständiger Kamera-Endlage dreht die Laufrichtung weich um die notwendigen 45°.
9. **Diagonalen:** Alle vier Innenraum-Diagonalen ausgeführt und normalisiert, jeweils 210 cm/s. Gerade und diagonale Türpassagen in beide Richtungen bestanden; keine geänderte Collision oder blockierende Stelle.
10. **Blickrichtung/Animation:** W Up, D Right, S Down, A Left; WD UpRight, WA UpLeft, SA DownLeft, SD DownRight. Alle vorhandenen Walking-/Idle-Flipbooks bleiben erhalten. Facing projiziert den tatsächlichen gewünschten Weltbewegungsvektor in die gerenderte Kamerabasis; im Idle bleibt der Weltvektor erhalten. Eine reine Sprite-Z-Drehung (außen 45°, innen 90°) hält die Sprite-Fläche zur Ansicht ausgerichtet. Körperhöhe 140 cm, Skalierung, Fußpivot und Assets unverändert.
11. **Rückschwenk:** Während des Fades nach außen bleibt Yaw 0° als Steuerungsbasis. Erst vollständig draußen beginnt der kurze Rückblend auf -45°. Danach gelten ursprüngliche Kamera und Außensteuerung exakt; zusätzlicher Player-Tick wieder deaktiviert.
12. **Umkehr mitten im Übergang:** Drei schnelle Ein-/Auslaufzyklen real zu Fuß ausgeführt. Fade-Umkehr bei ungefähr 0,56–0,60; bei keinem davon wurde Interior vollständig erreicht. Steuerungsmodus blieb durchgehend außen, Yaw -45°. Zusätzlich Pause im Türrahmen, erneutes Hineingehen sowie Exit→Entry-Umkehr automatisiert geprüft. Hysterese und reversible Kameraberechnung bleiben erhalten.
13. **Interaktion:** Letzte Weltbewegungsrichtung wird für Trace und Idle-Orientierung erhalten. W innen zeigt +X, alle acht Richtungen stimmen mit den Bewegungsvektoren überein. Reichweite unverändert 150 cm. Das leere Cottage enthält kein Interaktionsobjekt; PIE prüft Orientierung und keine Phantom-Interaktion. Die vorhandenen Player-/Interaktions-Automationstests sind grün; die Interaktionsmechanik wurde nicht umgebaut.
14. **PIE:** Vollständiger Ablauf vom normalen Start ohne Spawn-Override oder Player-Teleport: draußen → gehaltenes W hinein → acht Innenrichtungen → Orientierung → gerade hinaus → diagonal hinein/hinaus → drei Teil-Umkehrungen → Pause an der Schwelle → Rückkehr zum Start. Enhanced Input lief durch den normalen CharacterMovement-Pfad. 668 aufgezeichnete Frames des finalen Durchlaufs, anschließend separater regulärer Fußweg für die Sichtprüfung. Beide Seiten und Rückwand sichtbar, Dach/Front innen verborgen, Raumfläche und Player lesbar.
15. **Build/Tests/Map Check:** Finaler macOS-Development-Editor-Build erfolgreich. Vollständiger PokeMonster-Testbestand vor und erneut nach abgeschlossenem PIE: 36/36 erfolgreich, 0 Testwarnungen, 0 fehlgeschlagen, 0 übersprungen. Darunter Player.Foundation, ScaleCalibration, BuildingInteriorCamera, Building-/HealingHouse-, Quest-, Battle-, Save- und weitere bestehende Tests. Map Check nach PIE: 0 Fehler/0 Warnungen. Material-/Modul-/Collision-Audit erneut bestanden: 148 unveränderte Cottage-Placements, freie Capsule-Routen und diagonale Tür, blockierende Front-/Rück-/Fensterwand.
16. **Dateien:** 15 offene Projektdateien insgesamt: 11 geänderte und 4 neue gegenüber HEAD. Die beiden Cutaway-Source-Dateien und der Importer sind in diesem Folgeauftrag bytegleich zum bereits offenen Stand. Tabelle unten. Keine Blender-/FBX-/Mesh-/Material-/Sprite-Datei geändert. Die 640 übrigen von 651 erfassten HEAD-Dateien bleiben bytegleich, einschließlich Dev_TestMap, Healing House V3 und Gasthaus. Keine Gameplay-Systeme migriert.
17. **git diff --check:** Erfolgreich, keine Ausgabe. Auch neue Markdown-/Test-/Tool-Dateien auf Zeilenenden und nachgestellte Leerzeichen geprüft.
18. **git status --short:** Unten vollständig; alles ungestaged. Kein Commit und kein Push.

## Messmethodik und Grenzen

Die Messhelfer liegen nur unter `/private/tmp/WestlandInteriorControls` und die Ergebnisse unter ignoriertem `Saved/WestlandInteriorControls`. Der Fußtest verwendet reproduzierbare digitale Enhanced-Input-Vektoren, nicht Actor-Transforms. Screenshot-Anfragen wurden von den kurzen Eingabephasen getrennt, nachdem sie in einem Vorlauf Messphasen verzögert hatten. Die finale Bewegung wurde ohne parallele Screenshot-Anfragen aufgezeichnet.

Der finale Durchlauf wurde an der diagonalen Einlaufpassage in derselben PIE-Sitzung fortgesetzt: Die Figur stand bereits hinter der Schwelle, die erste Testabfrage lag wegen der Tick-Reihenfolge einen Frame vor der Cutaway-Aktualisierung. Endzustände wurden korrekt nach dem 0,4-s-Fade geprüft. Das war eine Korrektur des temporären Messhelfers, keine Änderung an Schwellen-, Collision- oder Gameplaylogik.

Lokale Belege: `PIEAudit.json`, `FinalPartA_PIEFrames.jsonl` + `PIEFrames.jsonl`, zugehörige Route-Protokolle, `AutomationResults.json`, `MapConfiguration.json`, `FollowUpPreservation.json` und `InteriorFinal.png`. Logs und Screenshots werden nicht versioniert. Im derzeit leeren Wohnhaus kann keine permanente Möbel-/NPC-Interaktion getestet werden; es wurden dafür keine neuen Gameplay-Actors angelegt.

## Aus der vorherigen Liste entfernt

- `Cottage_WallSolid2m_068`
- `Cottage_HorizontalBeam2m_069`
- `Cottage_WallSolid2m_070`
- `Cottage_HorizontalBeam2m_071`
- `Cottage_WallSolid2m_072`
- `Cottage_HorizontalBeam2m_073`
- `Cottage_StonePlinth1m_074`
- `Cottage_StonePlinth1m_075`
- `Cottage_StonePlinth1m_076`
- `Cottage_StonePlinth1m_077`
- `Cottage_StonePlinth1m_078`
- `Cottage_StonePlinth1m_079`
- `Cottage_CornerPost3m_083`
- `Cottage_VerticalPost3m_090`
- `Cottage_VerticalPost3m_091`
- `Cottage_DiagonalBrace1m_094`
- `Cottage_DiagonalBrace1m_095`

## Finale explizite Ausblendliste

- `Cottage_WallWindowArch2m_036`
- `Cottage_HorizontalBeam2m_037`
- `Cottage_WallDoor2m_038`
- `Cottage_HorizontalBeam2m_039`
- `Cottage_WallWindowArch2m_040`
- `Cottage_HorizontalBeam2m_041`
- `Cottage_GableHalf3m_042`
- `Cottage_GableTrimHalf3m_043`
- `Cottage_GableHalf3m_044`
- `Cottage_GableTrimHalf3m_045`
- `Cottage_CornerPost3m_080`
- `Cottage_CornerPost3m_081`
- `Cottage_VerticalPost3m_084`
- `Cottage_VerticalPost3m_085`
- `Cottage_StonePlinth1m_096`
- `Cottage_StonePlinth1m_097`
- `Cottage_StonePlinth1m_098`
- `Cottage_StonePlinth1m_099`
- `Cottage_RoofPanel1m_106`
- `Cottage_EaveTrim1m_107`
- `Cottage_RoofPanel1m_108`
- `Cottage_EaveTrim1m_109`
- `Cottage_RoofPanel1m_110`
- `Cottage_EaveTrim1m_111`
- `Cottage_RoofPanel1m_112`
- `Cottage_EaveTrim1m_113`
- `Cottage_RoofPanel1m_114`
- `Cottage_EaveTrim1m_115`
- `Cottage_RoofPanel1m_116`
- `Cottage_EaveTrim1m_117`
- `Cottage_RoofPanelEnd30cm_118`
- `Cottage_RoofPanelEnd30cm_119`
- `Cottage_RoofPanel1m_120`
- `Cottage_EaveTrim1m_121`
- `Cottage_RoofPanel1m_122`
- `Cottage_EaveTrim1m_123`
- `Cottage_RoofPanel1m_124`
- `Cottage_EaveTrim1m_125`
- `Cottage_RoofPanel1m_126`
- `Cottage_EaveTrim1m_127`
- `Cottage_RoofPanel1m_128`
- `Cottage_EaveTrim1m_129`
- `Cottage_RoofPanel1m_130`
- `Cottage_EaveTrim1m_131`
- `Cottage_RoofPanelEnd30cm_132`
- `Cottage_RoofPanelEnd30cm_133`
- `Cottage_RidgeCap1m_134`
- `Cottage_RidgeCap1m_135`
- `Cottage_RidgeCap1m_136`
- `Cottage_RidgeCap1m_137`
- `Cottage_RidgeCap1m_138`
- `Cottage_RidgeCap1m_139`
- `Cottage_DoorFrame130x200_140`
- `Cottage_DoorLeaf130x200_141`
- `Cottage_WindowArch_142`
- `Cottage_WindowArch_143`
- `Cottage_Porch160cm_145`
- `Cottage_Chimney60cm_147`

## Sämtliche offenen Dateien

| Git | Datei | Zweck / Herkunft |
| --- | --- | --- |
| M | `Art/Architecture/Westland/Buildings/WL_Cottage_V1.json` | Explizite Dach-/Frontliste und Beschreibung der Innensteuerung |
| M | `Content/Maps/Dev_BuildingKitTestMap.umap` | Nur Cottage-Konfiguration aktualisiert |
| M | `Docs/ENTSCHEIDUNGEN.md` | Vorige Seiten-/Steuerungsentscheidung teilweise ersetzt |
| M | `Docs/TECHNIK.md` | Endpunktwechsel, Facing und Interaktion dokumentiert |
| M | `Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.cpp` | Bewegungsbasis, Endpunkt-Latch, nachgelagerter Blend, Sprite-Yaw/Facing |
| M | `Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.h` | Blueprint-lesbare Basis/Modus und kleiner Runtime-Zustand |
| M | `Source/PokeMonster/World/PokeMonsterBuildingCutaway.cpp` | Unverändert aus dem bereits offenen Innenkamera-Proof übernommen |
| M | `Source/PokeMonster/World/PokeMonsterBuildingCutaway.h` | Unverändert aus dem bereits offenen Innenkamera-Proof übernommen |
| M | `Tools/Blender/BuildWestlandBuildingKitV1.py` | Nur Autoren-Metadaten; nicht in Blender ausgeführt |
| M | `Tools/ImportWestlandBuildingKitV1.py` | Unverändert aus dem bereits offenen Innenkamera-Proof übernommen |
| M | `Tools/ValidateWestlandBuildingKitV1.py` | Zusätzliche Prüfung beider sichtbarer Seiten und Rückwand |
| ?? | `Docs/WESTLAND_WOHNHAUS_INNENKAMERA_PRUEFBERICHT.md` | Voriger Proof ausdrücklich als historischer Zwischenstand gekennzeichnet |
| ?? | `Docs/WESTLAND_WOHNHAUS_INNENSTEUERUNG_PRUEFBERICHT.md` | Dieser aktuelle Folgebericht |
| ?? | `Source/PokeMonster/Tests/PokeMonsterBuildingCameraTest.cpp` | Vorhandenen offenen Kamera-Test um Steuerung und gespeicherte Liste erweitert |
| ?? | `Tools/ConfigureCottageInteriorCamera.py` | Vorhandenes offenes Werkzeug für aktualisierte Cottage-Liste verwendet |

## Abschließender Git-Status

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
?? Docs/WESTLAND_WOHNHAUS_INNENSTEUERUNG_PRUEFBERICHT.md
?? Source/PokeMonster/Tests/PokeMonsterBuildingCameraTest.cpp
?? Tools/ConfigureCottageInteriorCamera.py
```

## Sinnvoller Git-Sicherungspunkt

Nach Harrys Sichtprüfung eignet sich der kombinierte Kamera-/Steuerungs-Proof als Sicherungspunkt. Nur diese Projektdateien stagen; Messartefakte bleiben unter Saved beziehungsweise /private/tmp. Der folgende Befehl wurde nicht ausgeführt:

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
  Docs/WESTLAND_WOHNHAUS_INNENSTEUERUNG_PRUEFBERICHT.md \
  Source/PokeMonster/Tests/PokeMonsterBuildingCameraTest.cpp \
  Tools/ConfigureCottageInteriorCamera.py
```
