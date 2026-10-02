# Scale Calibration – Player und Heilhaus

Stand: 2026-10-02. Ausgangs-HEAD `3673e53 Add Blender healing house prototype`. `git status --short` war vor Beginn leer. Nur Maßstab/Darstellung kalibriert; keine Heilhaus-Detailarbeit, kein Commit, kein Push.

## Messverfahren und Ausgangsstand

Unreal-CDO, tatsächliche Flipbook-/Sprite-Zuordnungen, Quell-PNG-Alpha, Engine-Render-Bounds und Live-PIE wurden getrennt vermessen. Blender-Szene nur gelesen: metrisch, `scale_length=1`, Architektur-Objekte Scale 1. Der bestehende `HH_ScaleReference_140cm` ist 0,45 × 0,30 × 1,40 m. Importierte Unreal-Meshes haben ebenfalls Scale 1 und passende Zentimeterabmessungen. Kein Blender/FBX-Einheitenfehler.

| Größe | Ausgang | Kalibriert |
| --- | --- | --- |
| Capsule-Radius | 28 cm / 0,28 m | unverändert |
| Capsule-Halbhöhe | 48 cm / 0,48 m | unverändert |
| Capsule-Gesamthöhe | 96 cm / 0,96 m | unverändert |
| Capsule-Durchmesser | 56 cm / 0,56 m | unverändert |
| Actor-Scale | (1; 1; 1) | unverändert |
| Sprite-CDO-Scale | (1; 1; 1) | unverändert; tatsächliche Darstellung wird in BeginPlay gesetzt |
| Sprite-Runtime-Scale | (0,36; 0,36; 0,36) | (0,66; 0,66; 1,086758) |
| Sprite-Rotation Pitch/Yaw/Roll | (0°; 45°; -55°) | (0°; 45°; 0°), aufrechte Fläche |
| Sprite-Relative-Location | (0; 0; 0) cm | (0; 0; -48) cm / (0; 0; -0,48) m |
| Pivot | BottomCenter (128; 512) px | Custom (128; 488) px, sichtbare Sohle |
| Pixels Per Unreal Unit | 3,4 px/cm | 3,4 × Alpha-Körperhöhe / 438, je Pose |
| Kameraarm | 1400 cm / 14 m | unverändert |
| Kamera Pitch/Yaw, FOV | -55° / -45°, 35° | unverändert |
| Camera Lag | 6, max. 180 cm / 1,80 m | unverändert |
| Bewegung | 210 cm/s / 2,10 m/s | unverändert |

## Warum etwa 54 cm gemeldet wurden

Die Leinwand hat 256 × 512 Pixel. `512 / 3,4 × 0,36 = 54,2118 cm = 0,542118 m` ist ihre volle Höhe in der Sprite-Ebene. Die tatsächliche sichtbare Figur umfasst jedoch nur 429–438 Pixel: **45,4235–46,3765 cm / 0,454235–0,463765 m**. 24 transparente Pixel liegen unter den Sohlen; über dem Scheitel liegen 50–59 Pixel. Alpha-Schwellen 1/8/16/64 ergeben dieselben Außenbounds; Schwelle 128 verändert sie nur um wenige Pixel. Grundlage ist Alpha > 16.

Die frühere Roll-Neigung -55° reduzierte die geometrische Welt-Z-Körperhöhe zusätzlich auf etwa **26,05–26,60 cm / 0,2605–0,2660 m**. Außerdem hing die Grafik am Capsule-Zentrum: In PIE lag die sichtbare Sohle ungefähr 51,46 cm über dem Boden. Der Fehler bestand somit aus zu kleiner visueller Scale, falschem Boden-Pivot/Offset und einer für reale 3D-Architektur ungeeigneten gekippten Körperfläche. Collision und importierte Architektur waren nicht falsch skaliert.

Die Korrektur wurde nicht aus `140 / 54` abgeleitet. Zunächst wurde die Alpha-Körperhöhe je Pose normiert. Eine Zwischenprüfung mit weiterhin geneigter Fläche und angepasster Bildschirmgröße zeigte am 92-cm-Tresen falsche Kopfverdeckung: Bildschirmgröße allein repariert keine Welt-Z-Tiefe. Deshalb steht jetzt ausschließlich die Sprite-Fläche aufrecht. Getrennte Breite/Höhe bewahrt ihre schmale Bildschirm-Silhouette unter derselben Kamera.

`ScaleZ = 140 × 3,4 / 438 = 1,086757991`. Für jede Pose gilt `AlphaHeight / PPU × ScaleZ = 140 cm = 1,40 m`. X/Y-Scale 0,66 ergibt sichtbare Breiten von 33,78–45,98 cm / 0,3378–0,4598 m. Die Breite darf sich mit Pose/Blickrichtung natürlich ändern; die Höhe und der Fußpunkt bleiben gleich.

## Alle verwendeten Frames

19 verschiedene Sprites werden in 8 Idle-Flipbooks (je 1 Frame) und 8 Walk-Flipbooks (je 2 Frames, 8 FPS) verwendet. PNGs, Textures und Flipbooks sind unverändert. Die nachfolgenden Körpermaße schließen transparente Ränder aus. Höhe neu ist zugleich Sprite-Ebenenhöhe und Welt-Z-Höhe.

| Sprite (Präfix `S_Player_`) | Alpha B × H px | PPU px/cm | Körper alt B × H cm (m) | Körper neu B × H cm (m) |
| --- | --- | --- | --- | --- |
| Idle_Down | 230 × 438 | 3.400000 | 24.35 × 46.38 (0.2435 × 0.4638) | 44.65 × 140,00 (0.4465 × 1,4000) |
| Idle_DownRight | 206 × 438 | 3.400000 | 21.81 × 46.38 (0.2181 × 0.4638) | 39.99 × 140,00 (0.3999 × 1,4000) |
| Idle_Up | 232 × 429 | 3.330137 | 24.56 × 45.42 (0.2456 × 0.4542) | 45.98 × 140,00 (0.4598 × 1,4000) |
| Walk_DownLeft_01 | 202 × 438 | 3.400000 | 21.39 × 46.38 (0.2139 × 0.4638) | 39.21 × 140,00 (0.3921 × 1,4000) |
| Walk_DownLeft_02 | 194 × 433 | 3.361187 | 20.54 × 45.85 (0.2054 × 0.4585) | 38.09 × 140,00 (0.3809 × 1,4000) |
| Walk_DownRight_01 | 193 × 433 | 3.361187 | 20.44 × 45.85 (0.2044 × 0.4585) | 37.90 × 140,00 (0.3790 × 1,4000) |
| Walk_DownRight_02 | 203 × 438 | 3.400000 | 21.49 × 46.38 (0.2149 × 0.4638) | 39.41 × 140,00 (0.3941 × 1,4000) |
| Walk_Down_01 | 199 × 438 | 3.400000 | 21.07 × 46.38 (0.2107 × 0.4638) | 38.63 × 140,00 (0.3863 × 1,4000) |
| Walk_Down_02 | 188 × 434 | 3.368950 | 19.91 × 45.95 (0.1991 × 0.4595) | 36.83 × 140,00 (0.3683 × 1,4000) |
| Walk_Left_01 | 215 × 438 | 3.400000 | 22.76 × 46.38 (0.2276 × 0.4638) | 41.74 × 140,00 (0.4174 × 1,4000) |
| Walk_Left_02 | 202 × 437 | 3.392237 | 21.39 × 46.27 (0.2139 × 0.4627) | 39.30 × 140,00 (0.3930 × 1,4000) |
| Walk_Right_01 | 219 × 437 | 3.392237 | 23.19 × 46.27 (0.2319 × 0.4627) | 42.61 × 140,00 (0.4261 × 1,4000) |
| Walk_Right_02 | 201 × 438 | 3.400000 | 21.28 × 46.38 (0.2128 × 0.4638) | 39.02 × 140,00 (0.3902 × 1,4000) |
| Walk_UpLeft_01 | 174 × 438 | 3.400000 | 18.42 × 46.38 (0.1842 × 0.4638) | 33.78 × 140,00 (0.3378 × 1,4000) |
| Walk_UpLeft_02 | 200 × 437 | 3.392237 | 21.18 × 46.27 (0.2118 × 0.4627) | 38.91 × 140,00 (0.3891 × 1,4000) |
| Walk_UpRight_01 | 192 × 438 | 3.400000 | 20.33 × 46.38 (0.2033 × 0.4638) | 37.27 × 140,00 (0.3727 × 1,4000) |
| Walk_UpRight_02 | 198 × 438 | 3.400000 | 20.96 × 46.38 (0.2096 × 0.4638) | 38.44 × 140,00 (0.3844 × 1,4000) |
| Walk_Up_01 | 186 × 437 | 3.392237 | 19.69 × 46.27 (0.1969 × 0.4627) | 36.19 × 140,00 (0.3619 × 1,4000) |
| Walk_Up_02 | 185 × 438 | 3.400000 | 19.59 × 46.38 (0.1959 × 0.4638) | 35.91 × 140,00 (0.3591 × 1,4000) |

## Sprite-/Flipbook-Bounds und Richtungswechsel

Die volle Leinwand war vor der Korrektur 27,1059 × 54,2118 cm / 0,271059 × 0,542118 m. Danach beträgt sie je nach posebezogener PPU 49,69–50,74 cm Breite / 0,4969–0,5074 m und 163,65–167,09 cm Höhe / 1,6365–1,6709 m. Sie ist ausdrücklich nicht der Körper.

Die gemessenen tight Render-Bounds stehen vollständig in `../Art/ScaleCalibration/Measurements/FrameBounds.csv`. Alle neuen lokalen Render-Höhen betragen 128,8235 cm / 1,288235 m vor Component-Scale; Z-Minimum 0 liegt an der Sohle. Die lokale Render-Tiefe beträgt 1 cm / 0,01 m, visuell skaliert 0,66 cm / 0,0066 m. Die Welt-Z-Höhe nach ScaleZ ist stets 140 cm. Yaw 45° verteilt die horizontale Breite auf Welt-X/Y; die angegebene Breite ist entlang der Sprite-Rechtsachse, nicht die diagonale AABB-Breite.

Flipbook-Union-Bounds lassen sich aus den gemessenen Sprite-Bounds der vorhandenen Frames bilden:

| Zustand/Richtung | Frames | Union-Breite cm (m), Höhe immer 140 cm / 1,40 m |
| --- | --- | --- |
| idle / up | 1 | 45.98 (0.4598) |
| idle / up_right | 1 | 37.27 (0.3727) |
| idle / right | 1 | 42.61 (0.4261) |
| idle / down_right | 1 | 39.99 (0.3999) |
| idle / down | 1 | 44.65 (0.4465) |
| idle / down_left | 1 | 39.21 (0.3921) |
| idle / left | 1 | 41.74 (0.4174) |
| idle / up_left | 1 | 33.78 (0.3378) |
| walking / up | 2 | 36.19 (0.3619) |
| walking / up_right | 2 | 38.44 (0.3844) |
| walking / right | 2 | 42.61 (0.4261) |
| walking / down_right | 2 | 39.41 (0.3941) |
| walking / down | 2 | 38.63 (0.3863) |
| walking / down_left | 2 | 39.21 (0.3921) |
| walking / left | 2 | 41.74 (0.4174) |
| walking / up_left | 2 | 38.91 (0.3891) |

Alle 24 Frame-Verwendungen der 16 Flipbooks wurden zugeordnet und ihre 19 eindeutigen Alpha-Körper vermessen. PPU und Pivot sind für jeden einzelnen Sprite automatisiert geprüft. Gleiche Sohlenlinie und normierte Höhe verhindern Maßstabs- und vertikale Pivot-Sprünge. Natürliche Form-/Breitenänderungen durch die gezeichnete Laufpose bleiben erhalten. Richtungszuordnung, Animationstempo und 8-Wege-Eingabelogik wurden nicht geändert; native Bewegung und Idle/Walk-Wechsel wurden in PIE beobachtet. Kein neuer simultaner Tastentest aller acht Eingabevektoren; die bestehenden Foundation-Tests sichern diese Logik ab.

## Größenvergleich zur Architektur

Kurzlebige Debug-Referenzen im echten PIE: Grün 140 cm / 1,40 m, Cyan 180 cm / 1,80 m, Gelb 210 cm / 2,10 m; jeweils 24 cm breit. Keine gespeicherten Actors und keine Map-Änderung. Gleiche Bodenhöhe, versetzt entlang Kamera-Rechtsachse. Der präzise Vergleich wird zusätzlich am identischen Fußpunkt projiziert, sodass die Perspektive unterschiedlicher Standorte das Ergebnis nicht verfälscht.

Finaler Live-PIE-Messpunkt: Fuß (-1000; 0; 2) cm, Actor-Scale 1, Sprite-Fuß deckungsgleich mit Capsule-Unterkante. Körper und aufrechte 140-cm-Referenz jeweils **223,750183 Bildschirm-Pixel**, Verhältnis **1,000000**, PASS. Etwa 2 cm Bodenabstand sind normale Capsule-Floor-Clearance, keine transparente Sockelfläche.

| Architektur | Gemessen | Verhältnis / Beurteilung |
| --- | --- | --- |
| Haupteingang | 240 × 230 cm / 2,40 × 2,30 m, B × H | Kopffreiheit Hobbit 90 cm, Mensch 50 cm, großer Elf 20 cm; großzügiger gemeinsamer Eingang, keine Riesentür |
| Tresen | 94 × 350 × 92 cm / 0,94 × 3,50 × 0,92 m | 65,7 % der Hobbit-Höhe; hoch, aber erreichbar und plausibel als Versorgungstresen |
| Fensterrahmen Front | Unterkante 102, Oberkante 233 cm / 1,02–2,33 m | Hobbit-Scheitel oberhalb Brüstung, Menschen/Elfen ebenfalls passend; kein Türmaßstab |
| Frontglas | 120–215 cm / 1,20–2,15 m | für Hobbit relativ hohe Fenster, plausibel; keine Änderung |
| Wand-/Innenraumhöhe | 260 cm / 2,60 m | oberhalb Scheitel 120/80/50 cm für 140/180/210-cm-Figuren |
| Dach | 255–640 cm / 2,55–6,40 m | deutlich hoher Fantasy-Dachraum; vom begehbaren Erdgeschoss getrennt |
| Baukörper | 1030 × 930 cm / 10,30 × 9,30 m | großzügiges Gemeinschaftsheilhaus, keine kleine Privatstube |
| Gesamt mit Anbau/Dach | etwa 1220 × 990 cm / 12,20 × 9,90 m; Kamin 702 cm / 7,02 m | große Silhouette bleibt V1-Architektur; kein Einheitenfehler |

## PIE-Beurteilung

Zu Fuß vom äußeren Startpunkt zum Eingang, durch die Tür, in den Innenraum und bis an die bestehende Tresen-Collision; anschließend zurück und erneut durch den Eingang. Keine Positions-Teleports. Die finale aufrechte Darstellung wurde vorab live geprüft und nach erfolgreichem Player-Build erneut mit Referenzen gestartet und bis an den Tresen zu Fuß geprüft. Dokumentierte Ansichten:

- `../Art/ScaleCalibration/Review/01_References.png`: finaler Player neben allen drei Größenreferenzen.
- `../Art/ScaleCalibration/Review/02_Approach.png`: Player vor dem Haus, Öffnung/Fenster als Größenvergleich.
- `../Art/ScaleCalibration/Review/04_EntranceCutaway.png`: Durchgang mit regulär aktiviertem Cutaway.
- `../Art/ScaleCalibration/Review/05_Interior.png`: freie Bewegung im Innenraum.
- `../Art/ScaleCalibration/Review/06_Counter.png`: Player direkt am Tresen, Kopf sichtbar, keine falsche Verdeckung mehr.

Eingang: Figur passt problemlos; die Öffnung wirkt breit, aber als gemeinsamer Eingang glaubwürdig. Der vorhandene Cutaway beginnt bereits vor der Tür und blendet dabei die vorderen Fassadenmodule aus; im eigentlichen Durchgang ist daher nicht ständig ein vollständiger Türrahmen sichtbar. Dafür wurde keine Cutaway-Änderung vorgenommen.

Tresen: Aufrechte Geometrie behebt die in der Zwischenprüfung gefundene Verdeckung des Kopfes. Die Figur ist gut lesbar und bleibt vor der bestehenden Kollision. Innenraum: großzügig, jedoch mit 2,60-m-Wandhöhe kein Riesenmaßstab. Dach und Gebäude bleiben große architektonische Formen. Die Hüterinnen-Grafik wurde nicht kalibriert; daraus wird keine präzise menschliche Referenzhöhe abgeleitet.

Kamera blieb vollständig unverändert. Keine Änderungen an Collision, Geschwindigkeit, Input, Lag, Interaktion, Healing, Checkpoint, Save, Cutaway, Quest, Battle oder Dev_TestMap. Auch Dev_HealingHouseTestMap sowie Blender-/FBX-/Haus-Mesh-Dateien blieben unverändert.

## Build und Tests

Mac Development Editor Build: Succeeded; abschließender Build des ausschließlich auf die Heilhaus-Testmap begrenzten Test-Helfers 25,49 Sekunden, ein paralleler Compile-Prozess. Gesamter PokeMonster-Automationbestand: **35 Success, 0 Warnings, 0 Failed, 0 NotRun**, einschließlich `PokeMonster.Player.Foundation`, `PokeMonster.Player.ScaleCalibration` und allen drei `PokeMonster.Overworld.HealingHouse.*`-Tests. Finaler zusätzlicher Editor-Scale-Test: 1/1 Success; anschließender Live-PIE-Probe PASS. Nachweise in `../Art/ScaleCalibration/Measurements/AutomationSummary.json` und `LiveProjection.txt`.

## Geänderte Dateien und Git-Prüfung

Geändert: die 19 unten aufgeführten bestehenden Sprite-Assets (PPU/Pivot), die drei visuellen BeginPlay-Einstellungen im Player-C++, dessen Source-README und die genannten Dokumente. Neu: ein gezielter Automationstest sowie Messdaten und fünf PIE-Aufnahmen. Keine Maps oder Heilhaus-Assets geändert.

`git diff --check`: erfolgreich, keine Ausgabe. Vollständiger Datei-Bestand (`git status --short --untracked-files=all`):

```text
 M Content/Characters/Prototype2D/Source/HobbitPlayer/README.md
 M Content/Characters/Prototype2D/Sprites/HobbitPlayer/S_Player_Idle_Down.uasset
 M Content/Characters/Prototype2D/Sprites/HobbitPlayer/S_Player_Idle_DownRight.uasset
 M Content/Characters/Prototype2D/Sprites/HobbitPlayer/S_Player_Idle_Up.uasset
 M Content/Characters/Prototype2D/Sprites/HobbitPlayer/S_Player_Walk_DownLeft_01.uasset
 M Content/Characters/Prototype2D/Sprites/HobbitPlayer/S_Player_Walk_DownLeft_02.uasset
 M Content/Characters/Prototype2D/Sprites/HobbitPlayer/S_Player_Walk_DownRight_01.uasset
 M Content/Characters/Prototype2D/Sprites/HobbitPlayer/S_Player_Walk_DownRight_02.uasset
 M Content/Characters/Prototype2D/Sprites/HobbitPlayer/S_Player_Walk_Down_01.uasset
 M Content/Characters/Prototype2D/Sprites/HobbitPlayer/S_Player_Walk_Down_02.uasset
 M Content/Characters/Prototype2D/Sprites/HobbitPlayer/S_Player_Walk_Left_01.uasset
 M Content/Characters/Prototype2D/Sprites/HobbitPlayer/S_Player_Walk_Left_02.uasset
 M Content/Characters/Prototype2D/Sprites/HobbitPlayer/S_Player_Walk_Right_01.uasset
 M Content/Characters/Prototype2D/Sprites/HobbitPlayer/S_Player_Walk_Right_02.uasset
 M Content/Characters/Prototype2D/Sprites/HobbitPlayer/S_Player_Walk_UpLeft_01.uasset
 M Content/Characters/Prototype2D/Sprites/HobbitPlayer/S_Player_Walk_UpLeft_02.uasset
 M Content/Characters/Prototype2D/Sprites/HobbitPlayer/S_Player_Walk_UpRight_01.uasset
 M Content/Characters/Prototype2D/Sprites/HobbitPlayer/S_Player_Walk_UpRight_02.uasset
 M Content/Characters/Prototype2D/Sprites/HobbitPlayer/S_Player_Walk_Up_01.uasset
 M Content/Characters/Prototype2D/Sprites/HobbitPlayer/S_Player_Walk_Up_02.uasset
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/HEILHAUS_V1_PRUEFBERICHT.md
 M Docs/TECHNIK.md
 M Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.cpp
?? Art/ScaleCalibration/Measurements/AlphaBounds.json
?? Art/ScaleCalibration/Measurements/AutomationSummary.json
?? Art/ScaleCalibration/Measurements/FrameBounds.csv
?? Art/ScaleCalibration/Measurements/LiveProjection.txt
?? Art/ScaleCalibration/Measurements/UnrealBefore.json
?? Art/ScaleCalibration/Review/01_References.png
?? Art/ScaleCalibration/Review/02_Approach.png
?? Art/ScaleCalibration/Review/04_EntranceCutaway.png
?? Art/ScaleCalibration/Review/05_Interior.png
?? Art/ScaleCalibration/Review/06_Counter.png
?? Docs/SCALE_CALIBRATION.md
?? Source/PokeMonster/Tests/PokeMonsterScaleCalibrationTest.cpp
```

Die Änderungen sind ein sinnvoller späterer Sicherungspunkt nach visueller Abnahme. Zunächst mit `git diff --stat` und `git diff --check` prüfen; in dieser Aufgabe wurde weder committed noch gepusht.
