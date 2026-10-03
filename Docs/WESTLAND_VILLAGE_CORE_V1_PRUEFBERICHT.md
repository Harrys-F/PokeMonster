# Westland Village Core V1 – Prüfbericht

Stand: 2026-10-03, Unreal Engine 5.8.2, macOS / MacBook Air M4 mit 16 GB RAM.

Der erste eigenständige Dorfkern ist gespeichert und vollständig über die normale Playerbewegung durchlaufen. Architektur, fünf Gebäudeeingänge, bestehende Innenkamera/-steuerung und Cutaways funktionieren. Die Gestaltung verwendet vorhandene Westland-Kit-Architektur und illustrierte Prototype2D-Vegetation. Die visuelle Freigabe bleibt Harrys Sichtprüfung vorbehalten; dies ist kein final eingerichtetes Dorf.

## 1. Ausgangs-HEAD und Erhalt des Projektstands

`3d48cea Complete Westland inn V1`; Arbeitsbaum zu Beginn sauber. Der aktuelle L-Grundriss und die Innensteuerung des Gasthauses waren bereits in HEAD gesichert. Die ältere quadratische Inn-Komposition wird nicht als Bauvorlage verwendet.

Die 659 ursprünglichen versionierten Dateien wurden vor Beginn mit SHA-256 erfasst. Nach Abschluss bleiben 657 bytegleich. Nur `Docs/TECHNIK.md` und `Docs/ENTSCHEIDUNGEN.md` sind als bestehende Dateien geändert. Insbesondere Kit-/Inn-/Healing-House-Blenderquellen, FBX-Dateien, bestehende Meshes, Materialien, Player-/Gameplay-C++ und alle alten Maps bleiben bytegleich.

## 2. Neue Map

`/Game/Maps/Dev_WestlandVillage`, gespeichert als `Content/Maps/Dev_WestlandVillage.umap`. Sie verwendet den vorhandenen Overworld-GameMode und normalen PlayerStart am Dorfrand. `Dev_TestMap`, `Dev_BuildingKitTestMap` und die Healing-House-Testmap sind unverändert.

## 3. Größe und Erkundungsdauer

Der Kern umfasst ungefähr **45 × 48 m** (X −21 bis +24 m, Y −23 bis +25 m). Ein 140 × 140-m-Geländepuffer verhindert technische Bildrandlücken; er enthält keine weiteren Dorfviertel. Der Eingangspfad reicht in diesen Puffer hinein.

Der vollständige Prüfweg einschließlich aller fünf Innenräume umfasst **327,56 m**. Gemessene reine Bewegungszeit: **165,19 s**, also ungefähr **2 min 45 s**. Mit Kamera-/Reviewpausen dauerte der Test etwa 3 min 42 s. Die geplante kurze Erkundungsdauer ist damit ohne Reviewpausen erreichbar.

## 4. Anzahl Gebäude und Gebäudestellen

**Sechs Stellen:** fünf errichtete, begehbare Gebäude und ein vorbereiteter Heilhausplatz. Hinzu kommt der öffentliche Bereich um die alte Eiche.

## 5. Gebäudetypen und Abmessungen

Die Maße beziehen sich auf das Modulraster des Hauptkörpers, ohne vorspringendes Fachwerk, Traufen oder Eingangshauben. X ist die lokale Gebäudetiefe, Y die lokale Breite.

| Gebäude | Raster / Form | Welt-Yaw | Freie Tür | Architekturinstanzen | Innenkamera |
| --- | --- | ---: | --- | ---: | ---: |
| Birkenhof | 6 × 6 m, vorhandenes Wohnhaus | −35° | 1,30 × 2,00 m | 148 | 2000 cm |
| Kräuterhaus | 4 × 6 m, kürzeres Wohnhaus | −55° | 1,30 × 2,00 m | 115 | 2000 cm |
| Langhaus | 8 × 6 m, tiefes Wohnhaus | −20° | 1,30 × 2,00 m | 180 | 2000 cm |
| Wiesenhaus | 4 × 8 m, breite kurze Variante | −65° | 1,30 × 2,00 m | 134 | 2000 cm |
| Gasthaus | bestehende L-Form: 6 × 8-m-Halle + 2 × 6-m-Rückflügel, Gesamtrahmen 8 × 8 m | −40° | 1,60 × 2,15 m | 221 | 2200 cm |

Kräuterhaus steht 20 cm erhöht. Der Heilhausplatz reserviert ungefähr 10 × 11 m bei Weltzentrum (−10, −14, 0) m. Healing House V3 wird nicht neu instanziert oder verändert.

## 6. Wiederverwendung und exakte Modulzahlen

Alle **798 Architekturinstanzen** verwenden unveränderte vorhandene Module (**100 % Wiederverwendung**). Tatsächlich eingesetzt werden 31 verschiedene Modularten. Das Assetaudit überprüfte zusätzlich die vollständige Bibliothek aus 25 ursprünglichen Kit- und acht bereits vorhandenen Inn-Erweiterungsmodulen.

Birkenhof übernimmt die gesicherte Wohnhauskomposition. Drei weitere Häuser variieren Wandfelder, Fenster, Dachspannweite, Gebäudelänge und Kaminanordnung. Das bestehende L-Gasthaus wird einschließlich Rückflügel und vorhandener Thekenreserve wiederverwendet. Die beiden Engine-Cubes der Thekenreserve zählen nicht als Kitmodule.

| Vorhandenes Modul | Instanzen im Dorf |
| --- | ---: |
| `Chimney60cm` | 5 |
| `CornerPost3m` | 22 |
| `DiagonalBrace1m` | 13 |
| `DoorFrame130x200` | 4 |
| `DoorFrame160x215` | 1 |
| `DoorLeaf130x200` | 4 |
| `DoorLeaf160x215` | 1 |
| `EaveTrim1m` | 60 |
| `Floor1m` | 202 |
| `GableHalf3m` | 14 |
| `GableHalf4m` | 8 |
| `GableTrimHalf3m` | 14 |
| `GableTrimHalf4m` | 8 |
| `HorizontalBeam2m` | 64 |
| `Porch160cm` | 5 |
| `RidgeCap1m` | 30 |
| `RoofPanel1m` | 40 |
| `RoofPanel8mSpan1m` | 20 |
| `RoofPanel8mSpanEnd30cm` | 7 |
| `RoofPanelEnd30cm` | 14 |
| `StonePlinth1m` | 118 |
| `Threshold130cm` | 4 |
| `Threshold160cm` | 1 |
| `VerticalPost3m` | 48 |
| `WallDoor160x2152m` | 1 |
| `WallDoor2m` | 4 |
| `WallSolid2m` | 32 |
| `WallWindowArch2m` | 11 |
| `WallWindowDouble2m` | 16 |
| `WindowArch` | 11 |
| `WindowDouble` | 16 |
| **Gesamt** | **798** |

Exakte Positionen, Rotationen, Cutaway-Zuordnung und Stückzahlen je Gebäude stehen im dauerhaften Bauplan `Art/World/Westland/WestlandVillage_V1.json`. Alle Architekturinstanzen behalten Scale (1,1,1); Fenster, Türen oder Dächer werden nicht gestreckt.

## 7. Neue Kitmodule und sonstige Assets

**Keine neuen Architektur-/Kitmodule, Blenderquellen oder FBX-Exporte.** Die bestehende `WestlandBuildingKit_V1.blend` wurde lesend in einem separaten Blender-Prozess geprüft, ohne Speichern. Modulgeometrien, Bounds und Materialien stimmen mit der bestehenden Definition überein.

Neu sind ausschließlich ein Gelände-StaticMesh, ein Weg-StaticMesh und ein eigenes Wegmaterial im Ordner `/Game/Environment/WestlandVillage`. Sie sind Landschafts-/Mapmittel, keine Gebäude-Sondermeshes. Native GeometryScript ist bereits vorhanden; keine neuen Plugins installiert.

## 8. Dorfgrundriss

Der westliche Eingang führt über einen gekrümmten Hauptweg in die Mitte. Wohnhäuser stehen nach Norden und Osten versetzt, das Gasthaus am östlichen Hauptweg, Wiesenhaus und künftiger Heilhausplatz an südlichen Schleifen/Abzweigen. Winkel von −20° bis −65°, unterschiedliche Grundstücksabstände und ungleich große Vorflächen vermeiden Gebäudezeilen.

Ein begehbarer Rundweg verbindet die Stellen. Engere Wohnzweige und offenere Kreuzungen wechseln sich ab; Vegetation, Felsen und niedrige Grundstückselemente führen natürlich. Es gibt keine unsichtbare äußere Dorfwand.

## 9. Öffentlicher Mittelpunkt

Eine große alte Eiche bei (−4,50, +2,60, 0) m bildet den natürlichen Mittelpunkt. Ihr vorhandener illustrierter Sprite wird mit Scale 1,35 dargestellt; umliegende Bäume variieren etwa zwischen 0,72 und 1,15. Die begehbare Aufweitung und mehrere Abzweige machen die Stelle zur Orientierung, ohne gepflasterten Stadtplatz oder neue Interaktionsfunktion.

## 10. Wegsystem

Sieben weich gekrümmte Bänder mit variierender Randlinie verbinden Hauptweg, Häuser und Heilhausreserve. Breiten sind Ausgangswerte; örtliche Aufweitungen und organische Ränder variieren diese.

| Weg | Ausgangsbreite |
| --- | ---: |
| Hauptweg | 3,40 m |
| Wohnweg | 2,50 m |
| Kräuterweg | 2,20 m |
| Ostweg | 2,50 m |
| Wiesenbogen | 2,40 m |
| Gasthausgarten | 2,10 m |
| Heilhausplatz | 2,20 m |

Catmull-Rom-Kurven, diagonale Verbindungen, weiche Alpha-Ränder und dezente Erdvariation ersetzen rechtwinklige Rasterwege. Eingangsvorflächen reichen ungefähr 3 m vor die Türen. Das Material ist unbeleuchtet und transparent; es verwendet vorhandene Welt-/UV-Daten, keine externe Textur.

## 11. Höhenunterschiede und Geometrie

Sanfte Geländeformen und weich eingeblendete Hausplateaus; maximale gemessene Gelände-Dreiecksneigung **2,223°**. Kräuterhaus liegt 20 cm höher. Die größte geprüfte Eingangsstufe beträgt 24 cm und bleibt unter der vorhandenen 45-cm-StepHeight.

Gelände: 5041 Vertices / 9800 Dreiecke, Nanite deaktiviert, beidseitige Flächen-Collision mit `Use Complex As Simple`. Wege: 8037 Vertices / 14176 Dreiecke, Map-Komponenten `NoCollision`. Ihre Höhe folgt baryzentrisch den tatsächlichen Terrain-Dreiecken plus 3 cm. Fein unterteilte Längs-/Querstreifen vermeiden durchscheinendes Gras an Kurven.

## 12. Vegetation

605 vorhandene illustrierte Sprite-Instanzen: **97 Bäume, 336 Büsche, 51 Felsen und 121 kleine Pflanzen/Gras-/Blumengruppen**. Verwendet werden `S_Oak`, `S_Bush`, `S_Rock`, `S_GrassCluster` und `S_Wildflowers` aus Prototype2D. Blumen bleiben sparsam. Gehölzgruppen, Grundstücksränder und Wegsäume sind gezielt gruppiert; keine gleichmäßige Streuung über Laufwege.

Separate kleine Stamm-Collisionkörper sind im Spiel unsichtbar; die illustrierte Darstellung bleibt erhalten. Die stabile, zurückhaltende Grundbeleuchtung und feste Belichtung sind ein Proof, keine finale Lichtstimmung.

## 13. Grundstückselemente

Unterbrochene niedrige Holzzäune, kleine Kräuterflächen und Hecken gliedern zwei Wohnbereiche. Eine kleine Holzreserve begleitet das Langhaus. Steine und Kräuter markieren den späteren Heilhausplatz. Kein vollständiges Wohnungs-/Gasthausdressing, keine NPCs oder zusätzliche Funktionen.

## 14. Begehbare Gebäude

Alle fünf Gebäude wurden vollständig betreten und wieder verlassen. Gerade und diagonale Türpassagen sind geprüft; Innenflächen lassen freie diagonale Bewegung zu. Gasthaus-Rückflügel, Verbindung zur Halle und Thekenumgang sind erreichbar. Noch keine vollständige Einrichtung; diese Prüfung bestätigt begehbare Architektur und vorhandene Gebäudetechnik.

## 15. Cutaway

Fünf separate vorhandene `PokeMonsterBuildingCutaway`-Actors. Explizite, je Gebäude passende Dach-/Frontlisten: Birkenhof 58, Kräuterhaus 48, Langhaus 68, Wiesenhaus 54, Gasthaus 82 Actors. Beide Seiten- und die unteren Rückwände bleiben sichtbar. Nur störende obere Dach-/Front-/Anschlussdetails werden ausgeblendet.

0,4-s-Fade, 4-cm-Hysterese und Auslösung an der Türschwelle bleiben bestehen. Beim Inn bleiben die vorhandenen zwei Innen-Teilregionen erhalten; die offene Ecke der L-Form löst keine Innenkamera aus. Eintritt, Rückweg und zusätzlicher diagonaler Wieder-Eintritt/-Austritt am Birkenhof bestanden. Keine neue Cutaway-Logik.

## 16. Kamera, Innensteuerung und Player

Außen unverändert: **2500 cm, FOV 35°, Yaw −45°, Pitch −55°, Lag 6 / maximal 180 cm**. Sichtbare Playerkörperhöhe 140 cm, Capsule und Sprite-Assets/Scale/Pivot bleiben unverändert. Gemessene horizontale Maximalgeschwindigkeit 210 cm/s; alle acht Walk-Flipbooks wurden im echten PIE nachgewiesen.

Innen: Wohnhäuser 2000 cm, Gasthaus 2200 cm, Pitch −50°, FOV 35°, raumfester Fokus und an der jeweiligen Gebäudeorientierung ausgerichteter Yaw. Bestehende Endpunkt-Latches erhalten die äußere Bewegungsbasis während des Eintrittsschwenks und die innere beim Rückschwenk bis zum jeweiligen Endpunkt.

Der vorhandene nachgelagerte Basis-Blend bleibt **250 Grad/s**, also 45 Grad in 0,18 s. Die gedrehten Dorfhäuser haben kleinere Winkelunterschiede zur Außenkamera und deshalb entsprechend kürzere Blendzeiten. Gemessen wurden maximal 249,999975 Grad/s. Keine neue Variante, kein Input-Reset und keine Änderung von Geschwindigkeit, Animationen oder Blickrichtungslogik.

## 17. Dach-Framing aus der tatsächlichen Spielkamera

Gedrehte Fassaden, freie Vorflächen und weniger frontale Wegannäherungen ergeben lesbare Eingänge und Gebäudeabschnitte. **Das obere Dach bleibt unmittelbar an Wohnhaus-/Gasthausfassaden und teils noch an den etwa 3-m-Vorflächen angeschnitten.** Das Layout beseitigt dieses bestehende Problem nicht vollständig. Türen, Schwellen, Wege und Player bleiben dort erkennbar.

Außenkamera/FOV wurden dafür ausdrücklich nicht geändert. Die lokale Aufnahme `05_Gasthausbereich.png` dokumentiert den verbleibenden Zuschnitt. Eine spätere gestalterische Entscheidung zur Komposition bleibt der Sichtprüfung vorbehalten; keine verdeckte Änderung der verbindlichen Kamera.

## 18. Player-Verdeckungen

Auf der vollständigen Haupt-/Wohn-/Gasthausroute wurden keine blockierten oder vollständig verdeckten wichtigen Laufstellen festgestellt. Eine zusätzliche zu Fuß erreichte Probe am östlichen Rand der alten Eiche zeigt eine **leichte Verdeckung des Fußpunkts durch den Kronenrand**, während Oberkörper und Laufrichtung gut lesbar bleiben. Probe ungefähr bei (−1,97, +2,00, +0,46) m Actorposition; Beleg `11_OakEastFlankOcclusion.png`.

Dies ist eine konkrete mögliche spätere Vegetations-Fade-Stelle. Kein Fade-System hinzugefügt. Die Bewertung betrifft den geprüften Rundweg und diese zusätzliche Probe, nicht jede denkbare Position hinter allen Bäumen.

## 19. Vollständiger PIE-Fußweg

Normaler PlayerStart bei (−2050,100,60) cm; keine Spawnüberschreibung, Pawn-Transforms oder Test-Teleports. Das Testwerkzeug steuert denselben Player über Enhanced Input mit acht normalisierten Richtungen. Es reduziert nur nahe Prüf-Wegpunkten die Eingabestärke für zuverlässiges Anhalten bei schwankender Editor-Bildrate; Gameplay-MaxWalkSpeed bleibt 210 cm/s.

Bestanden: Dorfeingang → Hauptweg → Dorfzentrum → Wohnbereich → Birkenhof hinein/acht Richtungen/gerade und diagonal hinaus/hinein → Kräuterhaus → Hauptweg → Gasthaus → Rückflügel → Thekenumgang → hinaus → Langhaus → Wiesenhaus → Heilhausplatz → zurück zum PlayerStart.

130 Prüfschritte, 15 tatsächliche Spielkamera-Reviewstopps, 327,56 m und 165,19 s Bewegungszeit. Keine Kollisions-Sackgasse, kein Absturz durch den Boden, keine unbeabsichtigte Aktivierung anderer Gebäude. Alle Kamera-/Cutaway-Endpunkte bestanden. Anschließend zusätzliche Eichen-Sichtprobe ebenfalls zu Fuß.

Während der Iteration wurden ausschließlich neue Mapmittel korrigiert: Gelände-Flächen-Collision aktiviert, hausnahe Geländeüberstände unter Böden entfernt, Wegmaterialanschlüsse und Terrain-following der Wege korrigiert. Die finalen Aufnahmen und der komplette erfolgreiche Rundlauf stammen aus dem korrigierten, gespeicherten Stand.

## 20. Technische Prüfungen

- **Map Check: 0 Fehler / 0 Warnungen** auf der finalen `Dev_WestlandVillage` nach PIE-Ende.
- Geometrie-/Material-/Missing-Asset-Audit bestanden: 33 Bibliotheksmeshes geprüft, 798 Modultransforms/Scale geprüft, 952 StaticMesh-Materialslots gültig, 40 eindeutige visuelle Assetreferenzen vorhanden, keine fehlenden Assets.
- Collision-Audit bestanden: alle fünf Türen mit 28-cm-Radius/48-cm-HalfHeight-Capsule gerade und diagonal frei; Front-/Seitenwände blockieren; Inn-Verbindung frei und Theke blockiert; 39 Terrain-Höhenprüfungen bestanden.
- Finaler PIE-/Frameaudit bestanden: acht Walk-Richtungen, fünf Innenkamera-Endpunkte, vollständige Außenrückkehr, 2439 vollständig äußere Kamerasamples korrekt.
- **Vollständige vorhandene Automation-Suite `PokeMonster`: 37/37 erfolgreich, 0 Testwarnungen, 0 Fehler, 0 nicht ausgeführte Tests.** Eigenständiger Null-RHI-Editorlauf beendet mit Exitcode 0. Darunter Player Foundation, Scale Calibration, Innenkamera/Inn/Healing House sowie bestehende Gameplay-/Save-/Quest-/Battletests.
- C++ bytegleich: **kein Build erforderlich oder durchgeführt**. Es werden keine neuen C++-Tests oder Gameplayklassen eingeführt; Mapprüfungen liegen in den drei Editor-/PIE-Werkzeugen.

## 21. Sämtliche neuen und geänderten Projektdateien

**Neun neue Dateien:**

- `Art/World/Westland/WestlandVillage_V1.json`
- `Content/Maps/Dev_WestlandVillage.umap`
- `Content/Environment/WestlandVillage/Meshes/SM_WV_Ground.uasset`
- `Content/Environment/WestlandVillage/Meshes/SM_WV_Paths.uasset`
- `Content/Environment/WestlandVillage/Materials/M_WV_Path.uasset`
- `Tools/BuildWestlandVillageV1.py`
- `Tools/TestWestlandVillageV1PIE.py`
- `Tools/ValidateWestlandVillageV1.py`
- `Docs/WESTLAND_VILLAGE_CORE_V1_PRUEFBERICHT.md`

**Zwei bestehende Dateien geändert:**

- `Docs/TECHNIK.md`
- `Docs/ENTSCHEIDUNGEN.md`

Die Werkzeuge sind dauerhafte, wiederverwendbare Autoren-/Prüfquellen: deterministischer JSON-Bauplan, auf die neue Map begrenztes Erstellen, lesender Asset-/Collisionaudit und reproduzierbarer Enhanced-Input-Fußlauf. Keine Screenshot-/Protokolldaten werden darin eingecheckt.

## 22. Lokale Reviews und Zwischenartefakte

Alle tatsächlichen PIE-Spielkamera-Aufnahmen liegen ausschließlich im bereits ignorierten Ordner:

`/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/WestlandVillage/`

Mindestens die geforderten Perspektiven sind vorhanden:

- `01_Dorfeingang.png`
- `02_Dorfzentrum.png`
- `03_Wohnbereich.png`
- `04_GeschwungenerWeg.png`
- `05_Gasthausbereich.png`

Weitere lokale Aufnahmen: fünf `*_InteriorReview.png`, `06_GasthausRueckfluegel.png`, `07_Langhaus.png`, `08_Wiesenhaus.png`, `09_Heilhausplatz.png`, `10_ReturnedToStart.png` und `11_OakEastFlankOcclusion.png` – insgesamt 16.

`PIERoute.json`, `PIEFrames.jsonl`, `FrameAudit.json`, `Validation.json`, Autorenprotokolle, Fortsetzungsmarker und ältere Iterationsprotokolle bleiben ebenfalls lokal unter `Saved/WestlandVillage`. Final erfolgreich ist `PIERoute.json`; ältere Fehlversuche sind keine finalen Testergebnisse.

Zusätzliche Baseline-/Blender-/Geometrieaudits, Editorlogs und Automationreport bleiben unter `/private/tmp/WestlandVillage`, insbesondere `Automation/index.json`. Diese Arbeitsartefakte nicht versionieren; nichts davon wurde gelöscht.

## 23. Git-/Dokumentationsprüfung und Sicherungspunkt

`git diff --check`: erfolgreich, keine Ausgabe. JSON und drei Python-Werkzeuge syntaktisch geprüft; Markdown-Codeblöcke geschlossen und keine nachgestellten Leerzeichen. Keine Änderung an HEAD, Index oder Remote; nichts gestaged.

Nach Harrys Sichtprüfung ist dieser isolierte Dorfstand ein sinnvoller Sicherungspunkt. Ausschließlich folgende versionierungswürdige Dateien aufnehmen (Befehl nur dokumentiert, nicht ausgeführt):

```sh
git add -- \
  Art/World/Westland/WestlandVillage_V1.json \
  Content/Maps/Dev_WestlandVillage.umap \
  Content/Environment/WestlandVillage/Meshes/SM_WV_Ground.uasset \
  Content/Environment/WestlandVillage/Meshes/SM_WV_Paths.uasset \
  Content/Environment/WestlandVillage/Materials/M_WV_Path.uasset \
  Tools/BuildWestlandVillageV1.py \
  Tools/TestWestlandVillageV1PIE.py \
  Tools/ValidateWestlandVillageV1.py \
  Docs/WESTLAND_VILLAGE_CORE_V1_PRUEFBERICHT.md \
  Docs/TECHNIK.md \
  Docs/ENTSCHEIDUNGEN.md
```

## 24. Abschließendes `git status --short`

```text
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
?? Art/World/
?? Content/Environment/WestlandVillage/
?? Content/Maps/Dev_WestlandVillage.umap
?? Docs/WESTLAND_VILLAGE_CORE_V1_PRUEFBERICHT.md
?? Tools/BuildWestlandVillageV1.py
?? Tools/TestWestlandVillageV1PIE.py
?? Tools/ValidateWestlandVillageV1.py
```

`--untracked-files=all` löst die beiden Verzeichniseinträge in genau den JSON-Bauplan und die drei oben genannten Content-Assets auf. Kein Commit, kein Push.

Zur Sichtprüfung im Unreal Editor `/Game/Maps/Dev_WestlandVillage` laden und Play am normalen PlayerStart starten. Nach diesem Abschluss keine weiteren Features, NPCs oder Dorfteile hinzufügen.
