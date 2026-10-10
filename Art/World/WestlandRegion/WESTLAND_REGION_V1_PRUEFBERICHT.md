# Westland Region V1 – Arbeits- und Prüfbericht

Stand: 9. Oktober 2026. Ausgangs-HEAD: `4e98b22ef0e64609fec2185668f85960ecb896dc`.

## Ergebnis und Grenzen

Separate Regionsmap `/Game/Maps/Dev_WestlandRegion`, mit zusammenhängendem Wegenetz, acht Hauptorten, zwei Rundwegen, drei versteckten Orten, vorhandenen Dialogen, Wildkämpfen und dem bestehenden Heilhaus samt verlagertem Innenraum. Dies ist eine erste spielbare Regionsversion. Die Illustration ist die räumliche und gestalterische Referenz; ihre finale Zeichnungsqualität und Dekorationsdichte werden noch nicht erreicht. Neue Brücken, Mühlenrad, Ruinen und Steine sind einfache wiederverwendbare Modelle. Wasserufer, Beleuchtung und weitläufige Wiesen benötigen weitere visuelle Verfeinerung. Einige Wegübergänge an Vorplätzen zeigen noch geometrische Kanten; das ist verbleibende visuelle Arbeit, kein behaupteter finaler Referenz-Look. Die gemessene Editorleistung erfüllt noch kein 60-FPS-Ziel.

Die bestehenden Design-Dokumente wurden entsprechend dem Auftrag **nicht geändert**. Dieser Bericht dokumentiert den tatsächlich erstellten, noch zu beurteilenden Stand und trifft keine neue verbindliche Designentscheidung.

## Schutz des Ausgangsstands

Bereits zu Beginn offen: `PokeMonster.uproject` und `Config/DefaultEditorPerProjectUserSettings.ini`. Beide gehören zu den vorherigen Nutzeränderungen. Keine Änderung daran durch die Regionsarbeit. Keine Änderung an Source/C++, Player-, Sprite-, Input-, Kamera-, Quest-, Battle-, Capture-, Inventar-, Save- oder Checkpoint-Implementierungen. Bestehende Maps einschließlich Testdorf bleiben erhalten. Geteilte Assets werden nur referenziert; eigene Varianten liegen unter `/Game/Environment/WestlandRegion`.

## Maßstab und Aufbau

- Kernregion: **800 × 600 m = 0,48 km²**.
- Außenkulisse: zusätzliche **100 m pro Seite**, Gesamtterrain **1000 × 800 m**. An den fernsten Rändern natürliche steile Geländekulisse; keine unsichtbare rechteckige Grenzwand.
- Bildkoordinaten E/N in Metern: E zeigt auf dem Bildschirm nach rechts, N nach oben. Unreal: `X=(E+N)*sqrt(0.5)*100`, `Y=(E-N)*sqrt(0.5)*100`. Figur und Gebäude wurden nicht global vergrößert.
- Dorfkern: 0 m; Heilhausterrasse: +10 m; Steinkreis: +18 m; Ruinen: +12 m. Fluss überwiegend −4 bis −8 m im südlichen Bereich; Nordlauf höher. Echter **3,5-m-Wasserfall** bei N=174,5 m mit entsprechend gestuftem Flussbett.
- Gelände: **80 getrennte 100-m-Meshkacheln**, Raster 2 m, je 5.000 Dreiecke, insgesamt **400.000 Dreiecke**, native komplexe Bodenkollision. GeometryScript wurde wegen der zuverlässig verfügbaren Editor-Werkzeuge verwendet; keine World-Partition-/Streaming-Umstellung.
- Hauptweg 3,6 m; Heilhauszugang 3,4 m; Nordrunde 2,4 m; Mühlenrunde 2,5 m; Wald- und Uferpfad je 2,1 m. Geometrie direkt auf Geländedreiecke zugeschnitten; sichtbare Oberfläche 1,2 cm über Boden. Gemeinsame Weltkoordinaten-Maske vermeidet Grasnähte an Wegkreuzungen.

| Bereich | Lage E/N in m | Inhalt |
|---|---:|---|
| Spielerhof | −300 / −220 | Wohnhaus, Schuppen, umzäunter Garten, Obstbäume, Wanderer |
| Dorf | −220 / −35 | acht Kit-Gebäude einschließlich Gasthaus, Brunnen, Markt, Sitzplätze und Gärten |
| Heilhaus | −310 / +205 | vorhandenes Außenhaus, Terrasse und native Innenraumverlagerung |
| Steinkreis | −45 / +235 | acht stehende Steine, Plateau, Blumen und Archivarin |
| Wildwiesen | +150 / +5 | offene Wiesen, drei sichtbare vorhandene Test-Wildkreaturen, Nebenwege |
| Waldruinen | +225 / +205 | Ruinenbögen, Säulen, dichterer Wald und Lichtung |
| Mühle/Felder | +145 / −230 | begehbares Kit-Haus, Mühlenrad, Getreide/Nutzgarten, Holzbrücke |
| Regionsausgang | +380 / +170 | Tor-/Pfadmarkierung; noch keine folgende Region/Levelreise |

Versteckte Orte: Aussicht bei −155/+265, Waldlichtung bei +280/+80, Uferfund bei ca. +79,31/−145. Der Uferfund ist ein vorbereiteter Erkundungsort, kein neu erfundenes Item-/Quest-System.

## Gebäude und Abweichungen

Elf neu zusammengesetzte Kit-Gebäude plus kopiertes Heilhaus. Wohnhäuser 4×6 bis 8×8 m; Dorf bleibt kompakt, größere Flächen dienen der Natur. Das vorhandene Gasthaus wird mit seiner **8×8-m-Halle** wiederverwendet, anstatt es auf den flexiblen 14×11-m-Richtwert aufzublähen. Mühle 8×6 m. Einfache begehbare Innenflächen; keine neue vollständige Einrichtung aller Häuser.

Heilhaus tatsächlich gemessen: Sockelumhüllung **9,418 × 9,210 m**, nicht als exakte Wandkörper-Abmessung misszuverstehen. Dach einschließlich Eingangsvorbau **10,734 × 10,214 m**, höchster Dachpunkt **6,397 m über Terrasse**. Bestehender getrennter Innenraum **12×10 m** erhalten. Türen: Standard-Kithaus ca. 1,30×2,00 m, Gasthaus 1,60×2,15 m, Heilhaus 1,50×2,15 m.

Steinbrücke: Deck 28×4 m. Holzbrücke: Deck 16×2,5 m. Kollisionsdeck und Geländer passen zu den sichtbaren Modellen. Beide Uferanschlüsse der Holzbrücke liegen auf sicherer Laufhöhe; die Flussrinne unter der Brücke bleibt erhalten.

## Wiederverwendung, Darstellung und Spielsysteme

Westland Building Kit, Gasthaus-Erweiterungen, Healing House Quality V3, Natural Ground V1 und illustrierte Prototype2D-Vegetation wiederverwendet. Eigene Materialien und Meshkopien verhindern Änderungen an gemeinsam verwendeten Assets. Vier Freilandpflanzenvarianten entfernen nur die keramischen Töpfe vorhandener Pflanzen; keine fremden Assets gelöscht.

Wiederholte Vegetation als HISM: **37.186 Instanzen**, dekoratives Gras ohne Kollision, eigene Baumstamm-Kollisionen. Sichtweiten ungefähr Bäume 100 m, Büsche 60 m, Gras 43 m. Große Waldbaumvarianten innerhalb des vorgesehenen Maßstabs. Kleingärten, Blüten-/Kräutergruppen, Steine, Zäune und Vorplätze ergänzen die Grundvegetation. Neue Blenderquelle enthält sieben getrennte wiederverwendbare Props: Steinbrücke, Holzbrücke, Mühlenrad, Ruinenbogen, Ruinensäule, stehender Stein und Fels.

Drei neutrale eigene Dialogdatenobjekte mit Weg-/Ortsinformationen; keine neue Questkette. Drei sichtbare Wildactors verwenden bestehendes Profil/Test-Spezies und feste Seeds. Heilung/PP, Checkpoint und Save über bestehende Heilerin. Regionsspezifische IDs vermeiden eine versehentliche Kopplung an den alten Mini-Slice. Der Ausgang bleibt vorbereitet, es existiert keine nächste Region.

Außenkamera **2500 cm / Pitch −55° / Yaw −45° / FOV 35°**, Bewegung **210 cm/s**, sichtbare Playergröße **1,40 m** unverändert. PlayerStart-Ausrichtung der neuen Map auf Yaw 0 korrigiert: Die beim Kopieren des Heilhauses mitgedrehte Spawn-Ausrichtung hatte die vorhandene Sprite-Ebene kantenförmig zur Kamera gestellt. Keine Änderung an Player-/Sprite-Assets. Bestehende gebäudespezifische Innenkameras/Cutaway-Verlagerung bleiben erhalten.

## Tatsächliche Fußtests und gefundene Korrekturen

Tests steuern den realen Pawn über Enhanced Input in acht Sektoren. Kein Test-Teleport, keine Geschwindigkeits-/Kameraüberschreibung und keine verkürzte BattleSession. Die native Heilhaus-Innenraumverlagerung ist reguläres Gameplay; ihre Ortsänderung wird getrennt von der gelaufenen Distanz erfasst.

- Hauptroute Hof → Dorf → Steinbrücke → Wildwiesen → Ruinen → Ausgang vollständig gelaufen: **1.040,795 m**, **9:02 Minuten Spielzeit**, inklusive Prüf-/Fotopausen. Geplante Mittellinie **1.026,487 m**, rechnerisch **8:09 Minuten** bei 2,1 m/s. Geschwindigkeit wurde nicht für die gewünschte Laufzeit erhöht.
- Westlauf: Wanderer mehrseitig, Eingabesicherung, Team-/Inventarmenü, Dorf/Gasthaus, Heilhaus betreten, Heilerin, vollständige HP/PP-Heilung, Save, Checkpoint, hinaus, Nordrunde/Aussicht/Steinkreis, Wildkampf. Wildkampf regulär gewonnen, zwei Runden, Menü während Battle gesperrt und danach wieder nutzbar.
- Ostlauf: Ruinen, Ausgang, Waldschleife und versteckte Lichtung tatsächlich erreicht. Zu dicht platzierte Uferfelsen und ein zunächst falsch gelegener Uferfund wurden korrigiert. 15 regionale Felsinstanzen versetzt, keine geteilten Felsassets verändert.
- Mühlenroute: anfänglich führte die Route gegen die hintere Hauswand; anschließend um die freie Gebäudeseite geführt. Ein weiterer Test zeigte einen zu tiefen Brückenanschluss; beide Landungen und die Kurve am rechten Ufer wurden gezielt korrigiert.
- Abschließender Südlauf bestanden: **945,576 m**, **8:08 Minuten Spielzeit**, Holzbrücke dreimal in beiden Richtungen, Mühlenumgang, Uferpfad und Wildwiesen. Maximale gemessene Geschwindigkeit **210 cm/s**, keine Sturz-/Blockierfehler.

Bei der zusätzlichen Mühlen-Fotoannäherung überschwang die geglättete Testroute in die Böschung. Die tatsächliche freie Vorplatzroute wurde anschließend geradlinig zu Fuß geprüft. Drei große regionale Vordergrundfelsen verdeckten dort den Player und wurden nachweislich versetzt; die Ansicht wurde erneut zu Fuß angelaufen.

Bei unveränderter Außenkamera werden größere Dächer unmittelbar vor den Fassaden teilweise angeschnitten. Die Übersichtskarte ist deshalb separat verfügbar; die Spielkameraaufnahmen zeigen den tatsächlichen Ausschnitt, keine eigens verschönerte Reviewkamera.

Die fehlgeschlagenen Zwischenläufe bleiben in den lokalen Prüfartefakten erhalten; sie werden nicht als bestandene Prüfungen gezählt.

## Abschließende Prüfungen

- Abschließender zusammenhängender Review-Fußlauf bestanden: **3201.158 m**, **27.18 Minuten Spielzeit**, inklusive wiederholter Mühlensichtprüfung, Hof, Dorf, Heilhaus innen/außen, Nordrunde/Steinkreis, Steinbrücke, Ruinen und Ausgang. Keine Test-Teleports; reguläre Heilhausverlagerung separat erfasst. Während dieses bestandenen Laufs maximale Laufgeschwindigkeit **210.000 cm/s**.
- Save/Load-Rundtest im laufenden Regions-PIE: Team/HP/XP/Level/PP, Inventar und vorhandene Trainer-IDs gespeichert; HP/PP durch regulären nativen Testkampf verändert, Inventar- und Trainerlisten kontrolliert geleert; durch bestehendes SaveSubsystem wiederhergestellt. Playerposition blieb unverändert, Eingabe frei. Originale Dev-Save-Datei anschließend bytegleich zurückgelegt.
- Map Check: **0 Fehler / 0 Warnungen**.
- Vollständiger vorhandener PokeMonster-Automationbestand: **38/38 erfolgreich**, keine Fehler/Warnungen im letzten Lauf. Erster Lauf ebenfalls 38/38; ein Zwischenlauf 37/38 wegen einer geloggten Engine-Ensure-Meldung zur Initialisierung eines temporären Tickable-World-Subsystems. Nach nativer Garbage Collection erneut 38/38. Keine Änderung am Battle-Test oder an Gameplay-C++. Details unter `Saved/WestlandRegion/AutomationResults.json`, Zwischenlauf unter `AutomationRun_Second.json`.
- Regionsaudit: zwölf Türen gerade/diagonal mit positiven Wandkontrollen; 1.583 Bodenstichproben; Materialien vorhanden; 80 Terrainkollisionen und 128 eigene gespeicherte Assets geprüft.
- Map nach Wechsel auf Dev_TestMap erneut von Disk geöffnet; eigene Maskentextur und gemeinsame gemalte Quellen wieder auflösbar.
- Alle **1001** anfangs erfassten Dateien bytegleich. Python-Syntax aller neuen Autoren-/Prüfwerkzeuge geprüft. C++ unverändert: kein neuer Build erforderlich.
- `git diff --check`: erfolgreich, keine Ausgabe.

### Leistung

MacBook Air M4 / 16 GB, Unreal 5.8.2, Editor-PIE im Viewport **2331×1346**, Medium (`sg.*=1`), 75 % Renderauflösung, Hintergrund-Drosselung für den Test aus, Zielobergrenze 60 FPS. Tatsächliche Slate-Frameintervalle einschließlich Editor, kein GPU-only- oder Paket-Benchmark.

Früher Hauptlauf bei 100 % Renderauflösung: **22,86 FPS**, Median 43,60 ms, p95 51,87 ms. Korrigierter Südlauf bei 75 %: **25,96 FPS**, Median 36,95 ms, p95 48,13 ms. Abschließender 30-Sekunden-Standtest am Ausgang ohne Fußlauf-/Dateischreibsteuerung: **26.33 FPS**, Median **35.97 ms**, p95 **51.26 ms**, 791 Stichproben. Diese Zahlen belegen noch keine stabile 60-FPS-Fassung; weitere Performancearbeit bleibt erforderlich.

## Speicherung und lokale Nachweise

- Unreal: `Content/Maps/Dev_WestlandRegion.umap` und `Content/Environment/WestlandRegion/`.
- Blender: `Art/World/WestlandRegion/WestlandRegion_PropsV1.blend`, gespeichert und erneut geöffnet; sieben Props vor FBX-Export geprüft.
- Exporte: `Art/World/WestlandRegion/Exports/WR_*.fbx`.
- Layout: `Art/World/WestlandRegion/WestlandRegion_V1.json`; Zugänge und korrigierte Felsplatzierungen in separaten JSON-Dateien.
- Übersicht: `Art/World/WestlandRegion/WestlandRegion_V1_Uebersicht.png`, aus tatsächlichen Layoutkoordinaten erzeugt, ausdrücklich kein Game-Render.
- HighRes-Spielkameraaufnahmen enthalten die tatsächlich gerenderte Szene, aber enginebedingt keine UMG-HUD-Ebene; die HUD-/Menüfunktion wurde separat im laufenden PIE und durch Automation geprüft.

Lokale Prüfdaten, vollständige Fußlaufprotokolle und Spielkamera-Screenshots: `Saved/WestlandRegion/` (ignoriert, nicht als Projektassets versionieren).

Kein Commit, kein Push, kein Staging. Erst nach visueller Beurteilung einen gezielten Git-Sicherungspunkt setzen; fremde offene Änderungen separat behandeln.

## Vollständige neue Projektdateien

173 neue Dateien dieses Auftrags. Vorhandene Nutzeränderungen sind gesondert im Git-Status sichtbar. Lokale Logs/Screenshots/Prüfartefakte unter Saved sind nicht Teil dieser Liste.

```text
Art/World/WestlandRegion/Exports/WR_Crag.fbx
Art/World/WestlandRegion/Exports/WR_RuinArch.fbx
Art/World/WestlandRegion/Exports/WR_RuinColumn.fbx
Art/World/WestlandRegion/Exports/WR_StandingStone.fbx
Art/World/WestlandRegion/Exports/WR_StoneBridge.fbx
Art/World/WestlandRegion/Exports/WR_Waterwheel.fbx
Art/World/WestlandRegion/Exports/WR_WoodBridge.fbx
Art/World/WestlandRegion/RegionReference.png
Art/World/WestlandRegion/Source/LayoutBeforeBridge.py
Art/World/WestlandRegion/Source/LayoutBeforeMill.py
Art/World/WestlandRegion/Textures/T_WR_PathCoverage.png
Art/World/WestlandRegion/WESTLAND_REGION_V1_PRUEFBERICHT.md
Art/World/WestlandRegion/WestlandRegion_Access.json
Art/World/WestlandRegion/WestlandRegion_MillClearance.json
Art/World/WestlandRegion/WestlandRegion_PropsV1.blend
Art/World/WestlandRegion/WestlandRegion_UferClearance.json
Art/World/WestlandRegion/WestlandRegion_V1.json
Art/World/WestlandRegion/WestlandRegion_V1_Uebersicht.png
Content/Environment/WestlandRegion/Data/DA_WR_Dialogue_0.uasset
Content/Environment/WestlandRegion/Data/DA_WR_Dialogue_1.uasset
Content/Environment/WestlandRegion/Data/DA_WR_Dialogue_2.uasset
Content/Environment/WestlandRegion/Materials/M_WR_Canvas.uasset
Content/Environment/WestlandRegion/Materials/M_WR_Card_Bush.uasset
Content/Environment/WestlandRegion/Materials/M_WR_Card_Oak.uasset
Content/Environment/WestlandRegion/Materials/M_WR_Card_Rock.uasset
Content/Environment/WestlandRegion/Materials/M_WR_Earth.uasset
Content/Environment/WestlandRegion/Materials/M_WR_Grass.uasset
Content/Environment/WestlandRegion/Materials/M_WR_PathBlend.uasset
Content/Environment/WestlandRegion/Materials/M_WR_River.uasset
Content/Environment/WestlandRegion/Materials/M_WR_WellWater.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Card_Bush.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Card_Oak.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Card_Rock.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_FarmGarden.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Ground_BroadHerb.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Ground_FlowerPlant.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Ground_LeafPlant.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Ground_NarrowHerb.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_MillCropSoil.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Path_Access_Birkenhaus.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Path_Access_Brunnenhaus.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Path_Access_Gartenhaus.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Path_Access_Gasthaus.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Path_Access_Kraeuterhof.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Path_Access_Nordhaus.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Path_Access_Obstschuppen.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Path_Access_Spielerhaus.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Path_Access_Wassermuehle.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Path_Access_Werkstatt.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Path_Access_Westhof.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Path_Hauptroute.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Path_Heilhauszugang.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Path_Muehlenrunde.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Path_Nordrunde.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Path_Uferpfad.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Path_Waldpfad.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_River.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_00_00.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_00_01.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_00_02.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_00_03.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_00_04.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_00_05.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_00_06.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_00_07.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_01_00.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_01_01.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_01_02.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_01_03.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_01_04.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_01_05.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_01_06.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_01_07.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_02_00.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_02_01.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_02_02.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_02_03.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_02_04.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_02_05.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_02_06.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_02_07.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_03_00.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_03_01.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_03_02.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_03_03.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_03_04.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_03_05.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_03_06.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_03_07.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_04_00.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_04_01.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_04_02.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_04_03.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_04_04.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_04_05.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_04_06.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_04_07.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_05_00.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_05_01.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_05_02.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_05_03.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_05_04.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_05_05.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_05_06.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_05_07.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_06_00.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_06_01.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_06_02.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_06_03.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_06_04.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_06_05.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_06_06.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_06_07.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_07_00.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_07_01.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_07_02.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_07_03.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_07_04.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_07_05.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_07_06.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_07_07.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_08_00.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_08_01.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_08_02.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_08_03.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_08_04.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_08_05.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_08_06.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_08_07.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_09_00.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_09_01.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_09_02.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_09_03.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_09_04.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_09_05.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_09_06.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_Terrain_09_07.uasset
Content/Environment/WestlandRegion/Meshes/SM_WR_VillageSquare.uasset
Content/Environment/WestlandRegion/Meshes/WR_Crag.uasset
Content/Environment/WestlandRegion/Meshes/WR_RuinArch.uasset
Content/Environment/WestlandRegion/Meshes/WR_RuinColumn.uasset
Content/Environment/WestlandRegion/Meshes/WR_StandingStone.uasset
Content/Environment/WestlandRegion/Meshes/WR_StoneBridge.uasset
Content/Environment/WestlandRegion/Meshes/WR_Waterwheel.uasset
Content/Environment/WestlandRegion/Meshes/WR_WoodBridge.uasset
Content/Environment/WestlandRegion/Textures/T_WR_PathCoverage.uasset
Content/Maps/Dev_WestlandRegion.umap
Tools/Blender/BuildWestlandRegionPropsV1.py
Tools/Blender/ExportWestlandRegionPropsV1.py
Tools/BoundWestlandRegionV1.py
Tools/BuildWestlandRegionPathMaskV1.py
Tools/BuildWestlandRegionV1.py
Tools/ClearWestlandRegionMillV1.py
Tools/ClearWestlandRegionUferV1.py
Tools/CompactWestlandRegionPlantMaterialsV1.py
Tools/ConfigureWestlandRegionSystemsV1.py
Tools/ConformWestlandRegionPathsV1.py
Tools/DressWestlandRegionRoutesV1.py
Tools/FinalizeWestlandRegionV1.py
Tools/FinishWestlandRegionV1.py
Tools/ImportWestlandRegionPathMaskV1.py
Tools/MeasureWestlandRegionV1PIE.py
Tools/PolishWestlandRegionV1.py
Tools/RefineWestlandRegionV1.py
Tools/RepairWestlandRegionBridgeV1.py
Tools/ReviewWestlandRegionV1.py
Tools/SaveAndAuditWestlandRegionV1.py
Tools/TestWestlandRegionSaveV1PIE.py
Tools/TestWestlandRegionTourV1PIE.py
Tools/TestWestlandRegionV1PIE.py
Tools/ValidateWestlandRegionV1.py
Tools/WestlandRegionLayout.py
Tools/WestlandRegionPathMesh.py
```

## Abschließender Git-Status

```text
 M PokeMonster.uproject
?? Art/World/WestlandRegion/
?? Config/DefaultEditorPerProjectUserSettings.ini
?? Content/Environment/WestlandRegion/
?? Content/Maps/Dev_WestlandRegion.umap
?? Tools/Blender/BuildWestlandRegionPropsV1.py
?? Tools/Blender/ExportWestlandRegionPropsV1.py
?? Tools/BoundWestlandRegionV1.py
?? Tools/BuildWestlandRegionPathMaskV1.py
?? Tools/BuildWestlandRegionV1.py
?? Tools/ClearWestlandRegionMillV1.py
?? Tools/ClearWestlandRegionUferV1.py
?? Tools/CompactWestlandRegionPlantMaterialsV1.py
?? Tools/ConfigureWestlandRegionSystemsV1.py
?? Tools/ConformWestlandRegionPathsV1.py
?? Tools/DressWestlandRegionRoutesV1.py
?? Tools/FinalizeWestlandRegionV1.py
?? Tools/FinishWestlandRegionV1.py
?? Tools/ImportWestlandRegionPathMaskV1.py
?? Tools/MeasureWestlandRegionV1PIE.py
?? Tools/PolishWestlandRegionV1.py
?? Tools/RefineWestlandRegionV1.py
?? Tools/RepairWestlandRegionBridgeV1.py
?? Tools/ReviewWestlandRegionV1.py
?? Tools/SaveAndAuditWestlandRegionV1.py
?? Tools/TestWestlandRegionSaveV1PIE.py
?? Tools/TestWestlandRegionTourV1PIE.py
?? Tools/TestWestlandRegionV1PIE.py
?? Tools/ValidateWestlandRegionV1.py
?? Tools/WestlandRegionLayout.py
?? Tools/WestlandRegionPathMesh.py
```

## Optionaler Sicherungspunkt nach visueller Beurteilung

Nicht ausgeführt. Ausschließlich Regionsdateien; fremde Änderungen bleiben außen vor.

```sh
git add -- \
  Art/World/WestlandRegion \
  Content/Environment/WestlandRegion \
  Content/Maps/Dev_WestlandRegion.umap \
  Tools/Blender/BuildWestlandRegionPropsV1.py \
  Tools/Blender/ExportWestlandRegionPropsV1.py \
  Tools/BoundWestlandRegionV1.py \
  Tools/BuildWestlandRegionPathMaskV1.py \
  Tools/BuildWestlandRegionV1.py \
  Tools/ClearWestlandRegionMillV1.py \
  Tools/ClearWestlandRegionUferV1.py \
  Tools/CompactWestlandRegionPlantMaterialsV1.py \
  Tools/ConfigureWestlandRegionSystemsV1.py \
  Tools/ConformWestlandRegionPathsV1.py \
  Tools/DressWestlandRegionRoutesV1.py \
  Tools/FinalizeWestlandRegionV1.py \
  Tools/FinishWestlandRegionV1.py \
  Tools/ImportWestlandRegionPathMaskV1.py \
  Tools/MeasureWestlandRegionV1PIE.py \
  Tools/PolishWestlandRegionV1.py \
  Tools/RefineWestlandRegionV1.py \
  Tools/RepairWestlandRegionBridgeV1.py \
  Tools/ReviewWestlandRegionV1.py \
  Tools/SaveAndAuditWestlandRegionV1.py \
  Tools/TestWestlandRegionSaveV1PIE.py \
  Tools/TestWestlandRegionTourV1PIE.py \
  Tools/TestWestlandRegionV1PIE.py \
  Tools/ValidateWestlandRegionV1.py \
  Tools/WestlandRegionLayout.py \
  Tools/WestlandRegionPathMesh.py
```
