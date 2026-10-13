# Kamera B und sichtlinienabhängige Kronenfreistellung

Prüfung: 13.10.2026, Unreal Engine 5.8.2, macOS/Metal. Ausgangs-HEAD `e297a827b718c0109844df06c693f17890e633d0` (`Save player Meshy animation quality V2 progress`), Branch `main`.

## Ergebnis und Umfang

Kamera B ist dauerhaft im vorhandenen nativen Player/SpringArm übernommen. Die vorbereiteten Eichen in `/Game/Maps/Dev_TestMap_VisualV2` werden entlang der tatsächlichen Kamera→Player-Sichtlinie weich freigestellt. Player in den geprüften Einzelkronen-, Wald-, Überlappungs- und Bewegungsaufnahmen sichtbar; Gebäude behalten ihre Materialien und Darstellung. Dies ist keine Sichtbarkeitsgarantie für sämtliche Baumfamilien oder Orte.

Zu Beginn bestand ausschließlich `?? Art/Characters/NPCs/` als offene Nutzerarbeit. Diese Dateien wurden vollständig erhalten. Alle vorhandenen Maps, Blenderquellen, Meshes, Animationen, Texturen und Gameplaydateien außerhalb der unten genannten Kameraanbindung bleiben bytegleich. Kein Commit, kein Push, nichts gestaged.

## Kamerawerte

| Eigenschaft | Kamera A | Übernommene Kamera B |
| --- | --- | --- |
| SpringArm-Abstand | 2500 cm | **2850 cm** |
| Pitch | −55° | **−50°** |
| Yaw / Roll | −45° / 0° | unverändert |
| FOV / Projektion | 35° / perspektivisch | unverändert |
| Positions-Lag | aktiv, Geschwindigkeit 12, maximal 45 cm | unverändert |
| Lag-Substepping | aktiv, 1/60 s | unverändert |
| Zieloffset | (0,0,35) cm | unverändert |
| Kollisions-Zoom / Rotations-Lag | deaktiviert | unverändert |

Absolute Armrotation, Controller-/Pawn-Rotationsverhalten und bestehende gebäudespezifische Innenkameras bleiben erhalten. Audit und PIE nutzen tatsächlich `PokeMonsterPlayerCharacter`; die bestehende Anbindung benötigt keine Blueprint- oder Mapänderung. Bewegung weiterhin 210 cm/s, Capsule-Radius 28 cm/Halbhöhe 48 cm. Keine Änderung an der 140-cm-Darstellung oder Animationen.

## Ursache und Anpassung der Freistellung

Der bisherige Materialkorridor berechnete den Kamerafokus aus den festen Kamera-A-Werten. Er berücksichtigte weder Kamera B noch die tatsächliche Playerposition bei Camera Lag zuverlässig. Ein größerer fester Weltkreis hätte zusätzlich unbeteiligte Vegetation entfernt.

Die neue rein visuelle `PokeMonsterCameraVisibilityComponent` übergibt tatsächliche PlayerCameraManager-Position und Playerposition plus 35 cm an `MPC_PlayerSight`. Sie registriert einmalig ausschließlich Meshes mit den beiden bestehenden Reveal-Mastermaterialien. In VisualV2: **41 Baumkomponenten, 82 Materialslots**. Gebäude und andere Materialien werden nicht registriert. Keine Actorposition, Collision oder Gameplayeigenschaft wird verändert.

Der Shader prüft pro Fragment einen endlichen perspektivischen Sichtkegel. Der Abschnitt liegt zwischen 0,06 und 0,995 der Kamera→Player-Strecke; hinter dem Player volle Deckkraft. Am Ziel beträgt der innere/äußere Radius **55/110 cm**, zur Kamera proportional schmaler. Der bisherige räumliche 70/155-cm-Korridor wurde somit nicht einfach vergrößert. Smoothstep und das vorhandene temporale Dither sorgen für weiche Ränder; Blatttextur-Alpha bleibt erhalten.

Eine konservative Bounds-Prüfung aktiviert den reversiblen **0,25-s-Fade** je Baum. Anschließend begrenzt der Shader die Öffnung auf wirklich im Sichtkegel liegende Flächen. Deshalb kann die Zahl aktivierter Bounds höher sein als die Zahl sichtbar freigestellter Kronen. Es verschwindet kein ganzer Baum. Die bestehende obere Rinden-/Astfreistellung bleibt nötig, weil Äste allein sonst die Figur verdecken; niedrige Wurzelbereiche bleiben geschützt. Farbe und Schatten verwenden dieselbe tatsächliche Kameraposition. Bei EndPlay werden Runtime-Materialzuweisungen zurückgegeben.

## Tatsächlich durchgeführte PIE-Prüfungen

Separate PIE-Starts mit kontrollierten Spawnpositionen; anschließende Bewegung über bestehendes Enhanced Input. Keine gespeicherte Mapänderung. Diese kurzen Kameratests sind kein vollständiger Gameplay-Rundweg. Pro Bewegungsserie: zur Kamera, Halt/Frontansicht, von der Kamera weg, Halt/Rückansicht, diagonal hin und zurück. Dörfliche Gebäudeansicht stationär geprüft.

| Serie | Start X/Y in cm | Prüfung / Ergebnis | Maximal aktivierte Baum-Bounds |
| --- | --- | --- | --- |
| Dorf | −3970 / 650 | Heilhaus/Fassade/Dach sichtbar; keine Gebäudematerialien registriert | 2 |
| Weg | −36 / −45 | Freier Weg/Brücke, vorwärts/rückwärts/diagonal; Figur sichtbar | 2 |
| Wald | −741 / −740 | Zuvor verdeckender Waldpunkt; Figur in allen geprüften Aufnahmen sichtbar | 6 |
| Kronen | −1900 / 530 | Große, überlappende Vordergrundkronen; kleine Sichtöffnung, Figur sichtbar | 2 |
| DichterWald | −4300 / 1550 | Waldweg und Richtungswechsel; Figur sichtbar | 1 |
| EinzelkroneFinal | −2350 / −450 | Unter einer großen Eiche; Front/Back/Diagonal sichtbar, Restkrone erhalten | 1 |

Die sechs Serien sind mit JSON-Ergebnis und Frameprotokollen belegt. Gemessene maximale Bewegungsgeschwindigkeit in den Bewegungsserien: **210 cm/s**. Abweichung der übertragenen Player-/Kameraposition vom tatsächlichen Wert jeweils unter **0,0003 cm**. Zwischenwerte der Fade-Stärke wurden während Ein-/Austritt registriert; keine beobachtete wiederholte harte Sichtbarkeitsschaltung. Auch im Einzelkronentest bleibt die letzte Blickrichtung beim Halt erhalten. Keine Vergrößerung oder Verschiebung der Welt, kein Kollisions-Zoom.

### Echte Screenshots aus Kamera B

Alle Bilder sind native Unreal-`Shot`-Aufnahmen, keine Konzeptbilder. Erste fünf Serien 1280 × 740 Pixel; abschließende Einzelkrone im eingebetteten Viewport 2331 × 1346 Pixel. Qualität und Renderkonfiguration wurden nicht verändert. Bilder und detaillierte Prüfarbeitsartefakte liegen im ignorierten `Saved/CameraB_20261013` und gehören nicht automatisch in Git.

- [Dorf / Heilhaus](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/CameraB_20261013/Dorf00000.png)
- [Freier Weg](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/CameraB_20261013/Weg00000.png)
- [Wald / überlappende Kronen](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/CameraB_20261013/Wald00000.png)
- [Kronenfreistellung unter einzelner Eiche](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/CameraB_20261013/EinzelkroneFinal00000.png)
- [Spieler vorne](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/CameraB_20261013/Weg_Player_Vorne00000.png)
- [Spieler hinten](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/CameraB_20261013/Weg_Player_Hinten00000.png)
- [Einzelkrone: zur Kamera](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/CameraB_20261013/EinzelkroneFinal_Player_Vorne00000.png)
- [Einzelkrone: von Kamera weg](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/CameraB_20261013/EinzelkroneFinal_Player_Hinten00000.png)
- [Einzelkrone: diagonal](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/CameraB_20261013/EinzelkroneFinal_Diagonal00000.png)

Eine zusätzliche erste `Einzelkrone`-Serie lag neben der vorgesehenen Eiche und dient nur als zusätzlicher Bewegungs-/Gebäudevergleich; sie ist ausdrücklich kein Nachweis für den gezielten Kronentest. Maßgeblich ist `EinzelkroneFinal` nach Prüfung der tatsächlichen Actor-Bounds.

## Build, Automation und Sicherheit

- Mac Development Editor-Build erfolgreich; finaler Build `Saved/CameraB_20261013/BuildFinal.log`, Ergebnis `Succeeded`, 5,05 s. Erster Gesamtbuild 25,28 s.
- Tatsächlich entdeckter und ausgeführter Bestand: **40/40 Success, 0 Testfehler, 0 Testwarnungen**. 39 bestehende Tests plus `PokeMonster.Camera.Visibility.FiniteSightlineAndFade`. Vier bestehende Kameratests erhalten die neuen Sollwerte; keine Tests deaktiviert.
- Neuer Test: endliche Sichtlinie, hinter dem Player/off-ray/degenerierte Strecke, zeitlicher Fade und Umkehr, Rückkehr zur Deckkraft, MPC-Parameter und Materialladen.
- Abschließender Map Check der VisualV2: **0 Fehler, 0 Warnungen**, 13.10.2026 17:46:29 UTC. Keine Dirty-Map/-Content-Pakete im abschließenden Audit.
- SHA256-Vergleich gegen 1447 vorhandene Projektdateien: ausschließlich die elf unten genannten bestehenden Dateien geändert. Alle Maps unverändert, einschließlich Original-Dev_TestMap, VisualV2, WestlandRegion und AssetLibrary. Ursprünglicher Dev-Save und offene NPC-Quelldateien bytegleich.
- `git diff --check`: erfolgreich, keine Ausgabe. HEAD und Branch unverändert.

### Verbleibende Probleme und Grenzen

1. Tiefe vorhandene Schatten machen die dunkle Kleidung weiterhin schwerer lesbar. Die Figur wird freigestellt, aber hier erfolgte keine Beleuchtungs-/Materialüberarbeitung des Players.
2. Temporales Dither kann feine Körnung/Unruhe erzeugen. Keine Ganzkronen-Pops beobachtet; dies ist keine Garantie gegen sämtliche TAA-Artefakte.
3. Abgedeckt sind die bestehenden Reveal-Eichen. Birken und andere Baumfamilien ohne diese Materialien bleiben unverändert. Keine weltweite Materialumstellung und keine universelle Occlusion-Freigabe.
4. Ein lokaler Player pro World; Split-Screen nicht vorbereitet. Nachträglich gespawnte neue Baumkomponenten werden vom einmaligen Scan nicht automatisch aufgenommen.
5. **Zwei Abstürze beim MCP-StopPIE schwebender PIE-Fenster:** `IsInGameThread()`-Assertion in `Slate/SceneViewport.cpp:196`, `FSceneViewport::Destroy`, SIGSEGV. Ursache nicht abschließend geklärt; weder ein reiner Enginefehler noch eine ausgeschlossene Beteiligung der Testanbindung ist bewiesen. Logs `EditorPIEStopCrash.log` und `EditorPIEStopCrash2.log` erhalten. Editor jeweils wiederhergestellt; drei dazwischenliegende Floating-PIE-Stopps und der abschließende eingebettete PIE-Stopp erfolgreich. Vier Sekunden Render-Nachlauf verhinderten den zweiten Absturz nicht zuverlässig. Keine verlorenen Map-/Projektänderungen; Editor am Ende offen auf VisualV2, PIE beendet.
6. Keine neue Performance-/FPS-Abnahme, keine erneute vollständige Battle-/Save-/Quest-PIE-Strecke. Bestehende Automation umfasst diese Systeme; ihre Dateien und Spielstände wurden nicht verändert. One-time-Scan und 41 Bounds-Prüfungen pro Frame begrenzen den neuen CPU-Aufwand, ersetzen aber keine Messung.

## Dateien und endgültiger Git-Status

**11 bestehende Dateien geändert:** zwei lokale Reveal-Materialassets; `PokeMonsterPlayerCharacter.cpp/.h`; vier Kamera-Sollwerttests; `TECHNIK.md`, `GRAFIKSTIL.md`, `ENTSCHEIDUNGEN.md`.

**6 neue Projektdateien:** `MPC_PlayerSight.uasset`; `PokeMonsterCameraVisibilityComponent.cpp/.h`; `PokeMonsterCameraVisibilityTest.cpp`; `ConfigurePlayerCameraBVisibility.py`; dieser Bericht. Keine Map, Player-Animation oder importiertes Originalmesh geändert.

```text
 M Content/Environment/DevTestMapVisualV2/Materials/M_V2_BarkRevealBase.uasset
 M Content/Environment/DevTestMapVisualV2/Materials/M_V2_CrownReveal.uasset
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/GRAFIKSTIL.md
 M Docs/TECHNIK.md
 M Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.cpp
 M Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.h
 M Source/PokeMonster/Tests/PokeMonsterBuildingCameraTest.cpp
 M Source/PokeMonster/Tests/PokeMonsterPlayerFoundationTest.cpp
 M Source/PokeMonster/Tests/PokeMonsterRelocatedInteriorTest.cpp
 M Source/PokeMonster/Tests/PokeMonsterScaleCalibrationTest.cpp
?? Art/Characters/NPCs/
?? Content/Environment/DevTestMapVisualV2/Materials/MPC_PlayerSight.uasset
?? Docs/KAMERA_B_SICHTFREISTELLUNG_PRUEFBERICHT.md
?? Source/PokeMonster/Camera/
?? Source/PokeMonster/Tests/PokeMonsterCameraVisibilityTest.cpp
?? Tools/ConfigurePlayerCameraBVisibility.py
```

Nach Harrys Sichtprüfung bietet dieser begrenzte Kamera-/Reveal-Stand einen sinnvollen Git-Sicherungspunkt. Vor dessen getrenntem späterem Auftrag die Änderung mit `git diff --stat` und `git status --short` prüfen; vorhandene NPC-Arbeit nicht versehentlich mit aufnehmen. In dieser Aufgabe keine Staging-, Commit- oder Push-Aktion.
