# Dev_TestMap Visual V2 – Prüfbericht

Datum: 12.10.2026. Umsetzung und tatsächliche Editor-/PIE-Prüfung; visuelle Nutzerfreigabe ausstehend.

## Ergebnis und Speicherort

Separate, gespeicherte Arbeitskarte **`/Game/Maps/Dev_TestMap_VisualV2.Dev_TestMap_VisualV2`**, Datei `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Content/Maps/Dev_TestMap_VisualV2.umap`. Das Original `/Game/Maps/Dev_TestMap` sowie Westland-Region, Asset-Bibliothekskarte und sämtliche anderen Ausgangskarten bleiben unverändert. Keine Änderung der Projekt-Startmap. Zum Testen diese Arbeitskarte im Editor öffnen und Play starten.

Der vollständige finale Fußlauf bestand (260.23 m, 175.25 s Spielzeit). 39/39 bestehende PokeMonster-Automationstests erfolgreich, keine Testfehler. Zwei Warnungen betreffen das externe iOS-Gerätewerkzeug `idevice_id` (Bad CPU type); keine Änderungen an diesem SDK vorgenommen. Map Check: siehe abschließenden Prüfblock. C++ unverändert; kein neuer Build erforderlich oder durchgeführt. Die neue Szene ist funktional geprüft, erreicht aber noch nicht in allen Bereichen die Qualität der handgemalten Referenz.

## 1. Ausgangsstand, Bestandsaufnahme und Sicherung

HEAD `98b1bdc4a680e1dcbdfce041c65ec4f521116182` (`Improve Meshy player animations V2 and save current project progress`), Branch `main`, anfänglich sauberer Arbeitsbaum. Es gab keine zu integrierenden uncommitted/untracked Projektänderungen. AGENTS, Grafikstil, Technik, Entscheidungen sowie Meshy-V2-, Westland-V3- und Heilhaus-/Innenraum-Prüfberichte wurden gelesen. Frühere Chatangaben wurden nicht als Freigabe übernommen.

Die tatsächlich vorhandene Meshy-V2-Integration verwendet `/Game/Characters/YoungTrainer/MeshyV2/Meshes/SK_Player_Meshy_V2`: bestehende AnimInstance, Idle/Walk, acht Modelldrehungen, Zubehörfedern. Technischer Stand vorhanden und erfolgreich benutzt; eine finale visuelle Animation-/Artfreigabe wird nicht daraus abgeleitet. Paper2D bleibt als unveränderter Code-/Asset-Fallback erhalten; ein zusätzlicher manueller Fallback-PIE-Test war nicht Teil dieses Rundlaufs.

Westland V3 enthält tatsächlich die alte Eiche und zwei Wildstrauchvarianten. Weitere Objekttypen stammen aus der bestehenden Bibliothek bzw. dem Kit, nicht aus erfundenen V3-Versionen. Die Quellen und importierten Originalassets wurden nicht verändert. Kein Blender-Neubau oder Export war nötig.

Originalkarte: exakte Datei `Content/Maps/Dev_TestMap.umap`, 624 Actors. Vorhanden waren 339 StaticMeshActors, 272 PaperSpriteActors, zwei DirectionalLights, SkyLight, PlayerStart sowie Dialog-NPCs, Trainer, sichtbare Wildbegegnung, separate Encounter-/Interaktionsmarker, Zone, RestPoint und Archivziel. Vorhandene Kollisionsflächen, Wasserblocker und Brücke wurden berücksichtigt. Keine neue Navigation-/KI-Architektur.

Der ursprüngliche ca. 40 × 40-m-Kern enthielt den Ablauf Ruhepunkt → Wanderer → optionale Wildkreatur → Liora → Archivstein. Die alte Darstellung mischte gezeichnete flache Sprites, primitive Geometrie und eine ältere Bodengestaltung; Gebäude/Innenraum und aktuelle Bibliotheksvegetation fehlten als zusammenhängender Rundweg. Vorher-Performance wurde später nochmals auf der unveränderten Originalkarte unter identischen Messbedingungen erhoben.

Sicherung: exakte Kartenkopie und Original-Dev-Save unter `Saved/DevTestMapVisualV2/Before/`, SHA-256-Baseline für 129 Schutzdateien unter `Baseline.json`. Die Arbeitskarte entstand über `EditorLoadingAndSavingUtils.save_map` (Editor Save As) und anschließendes Laden, keine rohe Kopie einer unbekannten Namensvariante. Die Schlussprüfung bestätigt identische Hashes aller 129 Schutzdateien, einschließlich der sieben Ausgangskarten, C++/Konfiguration und des wiederhergestellten Dev-Spielstands. Git zeigt keine Änderung vorhandener Asset-/Blenderdateien.

## 2. Szenenaufbau und optische Änderungen

Der funktionierende Kern blieb an seinen ursprünglichen Actor-Positionen. Neue Bodenunterlage: **90 × 65 m**, eigentliche Außeninszenierung ungefähr 70 × 50 m. Die vorgeschlagenen 150 × 120 m wurden bewusst nicht ausgeschöpft: vorhandene Testpunkte hätten sonst unnötig auseinandergezogen werden müssen. Der Expanded Interior liegt weiterhin räumlich separat und ist kein zusätzlicher Außenbereich.

| Bereich | Umgesetzt |
|---|---|
| Dorf | Bestehender Start/NPC-Bereich, Dorf-Rundweg, wiederverwendetes Quality-V3-Heilhaus, modulare Wohnhausfassade, Bank, Karre, Fass/Kiste, Wegweiser/Zäune und bestehende Laternen am Heilhaus |
| Wald | V3-Eichen und Wildstrauchvarianten, zusätzliche Birken, Felsen und gruppierter Unterwuchs; offene Bewegungsstreifen und optionaler Wildzweig |
| Bach/Brücke | Bestehende begehbare Brücke und Wasserkollision erhalten; Holzmaterialien, Ufervegetation/Felsen und neue Weganschlüsse |
| Ruinenlichtung | Vorhandener Archivstein als spielbares Ziel, zusätzliche Säulen-/Runen-/Mauerteile als Rahmen; Passage und Liora bleiben erreichbar |

Fünf native geschwungene Wegbänder: Main 2112, Wild 384, VillageLoop 1152, NorthLoop 1728, Cottage 576 Dreiecke, zusammen **5952**. Normalen-/Tangentenbasis berechnet, keine Collision, kein Schattenwurf. Breite 270 cm, Wildzweig 140 cm. Mehrere Maßstäbe/gedrehte Abtastungen bestehender gemalter Gras-/Erdtexturen reduzieren auffälliges Tiling. Keine neuen Texturimporte.

Die erste Wegversion hatte falsche Dreiecksorientierung; dies wurde in der Geometrie korrigiert. Anschließend gefundene kantige Grasflecken an Kreuzungen kamen von coplanaren, opaken Wegbändern mit Grasrand. Die finale eigene Masked-/Dither-Kante lässt angrenzende Wege durch und staffelt die Visualhöhen um je 0,15 cm. Die Lauf-/Bodenkollision bleibt unverändert. Kein Warnungsunterdrücken.

Sieben statische Unterwuchs-HISM-Gruppen mit **459 Instanzen**: Gras 175, Farne 46, Blumen 63, Kräuter 55, Kiesel 62, WildBush A 30/B 28. Gruppen an Rändern statt Raster; Weg-/NPC-/Gebäudeflächen werden bei der Verteilung freigehalten. NoCollision, kein Schattenwurf, Culling 4500–6500 cm; kleine Pflanzen ohne Distance-Field-/dynamischen Indirect-Lighting-Beitrag. Größere Bäume behalten passende Stammkollision und Schatten. Vorhandene LODs werden weiterverwendet.

Wohnhaus: 148 vorhandene Kit-Module in 29 HISM-Gruppen, 6 × 6-m-Grundkörper, bei (−2750, −1020) cm. Es wurde aus dem zunächst blockierten Bereich der separaten Testmarker versetzt. Materialfamilien für Instancing wurden als sieben lokale Kopien angelegt, gemeinsame Kit-Materialien nicht gespeichert. Generischer Cutaway mit 0,4 s und 17 Gruppenreferenzen. Dieses Wohnhaus ist architektonischer Blockout; sein Innenraum wurde nicht separat im finalen Fußlauf betreten.

Heilhaus: 534 Actors aus der tatsächlichen vorhandenen Heilhaus-Testkarte über die Editor-API dupliziert; lokale Actor-Referenzen remappt. Offset (−3100,+500,0) cm. Das Quelllevel wurde danach entfernt, nicht gespeichert und ist keine Laufzeit-Streaming-Abhängigkeit. Cutaway referenziert 117 kopierte Occluder; 12 × 10-m-Innenraum, 0,4-s-Fade und bestehende Relocation erhalten. Heilerin verwendet den eindeutigen Checkpoint `VisualV2_HealingHouse`.

Bestehende NPC-/Heilerin-Spritegrafiken erhalten nur lokale Visualskalierung und Fußpunktkorrektur. Wanderer 0,34 → 0,604614; Archivarin 0,34 → 0,511785; Liora 0,42 → 0,521978; Heilerin 0,46875 → 0,861953. Die sichtbare Außen-Spriteebene ist 95 cm hoch; dies ist keine Änderung an Player-/NPC-Kollision oder Dialoglogik. Die Heilerin repräsentiert ca. 160 cm. Transparente PNG-Ränder wurden berücksichtigt. Sichtbare Entwicklerlabels in dieser Kopie mit HiddenInGame verborgen.

Beleuchtung ausschließlich maplokal: Hauptlicht 7,5 lux, dezentes Fülllicht 0,5, SkyLight 1,25, eigener Außen-Exposure-Bias +0,3. Die zuerst zu dunkle Fassung wurde anhand echter Spielbilder korrigiert. Keine globalen Render-Konfigurationsänderungen. Bestehende Innenbeleuchtung weiterverwendet.

## 3. Player und Sichtbarkeit hinter Kronen

Unverändert: sichtbarer Playerkörper 140 cm, Capsule Radius 28 cm/Halbhöhe 48 cm, 210 cm/s, Außenkamera 2500 cm, Pitch −55°, Yaw −45°, FOV 35°, Lag 12/max.45. Bestehende Eingaben, Bewegungsbasis, Animationen, Begegnungs-/Kampf-/Quest-/Save-Regeln unverändert. Innenkamera übernimmt weiterhin ausschließlich der bestehende Heilhausübergang (2600 cm/−50°/lokal0°).

Eigene Blatt- und Rindenmaterialvarianten öffnen räumlich einen weichen geditherten Korridor zwischen fester Außenkamera und Fokus. Die Blatt-only-Fassung ließ dicke Äste vor dem Player stehen; die finale Rindenvariante berücksichtigt daher obere Stamm-/Astflächen, schützt aber die Wurzelbasis. Echte On/Off-Bilder am selben zu Fuß erreichten Punkt zeigen den Unterschied. Keine neuen Tick-Actors, keine globalen Baum-Materialänderungen.

Grenzen: kamerabezogene räumliche Freistellung, **kein zeitgesteuerter Ganzbaum-Fade**, nur auf den neuen V3-Eichen. Birken/andere Baumfamilien nicht pauschal abgedeckt. Der sichtbar dithernde Kronenausschnitt ist funktional, aber kein finaler Art-Effekt.

## 4. Tatsächlicher Gameplay-Fußtest

Finaler Durchlauf: **260.23 m**, 175.25 s Spielzeit/179.81 s reale Zeit. Höchste aufgezeichnete Bewegungsgeschwindigkeit 210.000002 cm/s. Das Skript injiziert echte Enhanced-Input-Bewegungswerte; es setzt keine Test-Actorpositionen. Die bestehende Tür-Relocation ist normales Gameplay und wurde nicht als gelaufene Strecke gezählt. Interaktionen benutzen die echte Reichweiten-/Blickrichtungsprüfung. UI-Aktionen laufen über vorhandene Controller/Presenter, ohne erzwungenes Überspringen der Präsentationssequenz.

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Start, Overworld-Menü | Erzeugt, öffnet/schließt, sperrt Bewegung und gibt sie frei |
| Wanderer | Echte Interaktion und mehrseitiger Dialog; Eingabesperre und Freigabe |
| Optionaler Wildzweig | Zu Fuß erreicht, Wildkampf begonnen, vorhandene Fangaktion erfolgreich: Captured, Team 2 → 3 |
| Liora | Zu Fuß erreicht, echte Runden/Präsentation bis Victory; `Slice_Liora` als besiegt geprüft |
| Bach/Brücke | Hin- und Rückweg über vorhandene Brückenkollision, Höhenwechsel ca.24 cm, keine Route blockiert |
| Save/Load vor Archiv | Echter Save; besiegte Trainer zur Laufzeit kontrolliert gelöscht; echtes Load stellt Liora und exakt dieselben HP/PP wieder her |
| Archivstein | Interaktion/Abschlussdialog, gespeichertes `Slice_ArchiveSeal` nachgewiesen |
| Rückweg zum Wanderer | Geänderter tatsächlicher Widgettext: „Der Archivstein leuchtet wieder. Du hast den Weg gefunden; die Archivarin wird sich freuen.“ |
| Dorf → Heilhaus | Komplett zu Fuß; gerader Tür-Eintritt mit bestehendem Expanded-Interior-Übergang |
| Innenraum/Heilerin | Laufwege am Tresen; Heal stellt alle HP und bekannten PP voll her, Save vorhanden, Checkpoint `VisualV2_HealingHouse` im Save nachgewiesen |
| Cutaway | Dach/Vorderwand nach Übergang verborgen, außerhalb wiederhergestellt; gerade sowie diagonal hinein/hinaus bestanden |
| Waldrundweg/Kronen | Vollständig zurück zum Start; Scoped-Reveal mit/ohne Material direkt verglichen und wiederhergestellt |
| Acht Richtungen/Stop | Alle acht Sektoren über Enhanced Input bewegt, Bildfolge aufgenommen; keine Kameradrehung/Zoomänderung durch diesen Pass |

Der Test veränderte ausschließlich seine PIE-Runtimezustände und den dafür vorher gesicherten Dev-Slot. Anschließend wurde der ursprüngliche Nutzer-Spielstand **bytegleich zurückkopiert**. Kein Nutzerfortschritt aus Tests bleibt als vermeintlicher Spielstand bestehen. Bestehende Weltflag-/Inventar-/Checkpoint-Serialisierung ist zusätzlich durch die Automationstests abgedeckt; nicht jeder Zustand wurde separat manuell verändert und verglichen.

Nicht als manuell geprüft ausgegeben: jede physische Tastenzuordnung/Mausbedienung, Niederlage/Blackout, TeamFull/fehlgeschlagener Fang, jeder separate Encounter-Zonentest, Cottage-Innenraum, sämtliche Außenkartenränder und alle möglichen Hinderniskombinationen. Keine neue Gameplaymechanik und keine neue Animation.

## 5. Automation, Map Check und Stabilität

Filter `StartsWith:PokeMonster`, aktueller tatsächlicher Umfang 39. Der finale Ergebnissatz enthält 39 Success, 0 Fehler, 2 Warnungen beim Versuch, das externe iOS-Gerätewerkzeug `idevice_id` auszuführen (Bad CPU type). Der macOS-Map-/Gameplay-Stand verursacht keine neue SDK-Installation; diese Warnungen bleiben protokolliert. Testnamen stehen im Anhang unten und in `Saved/DevTestMapVisualV2/AutomationFinalResults.json`. Vorhandene Tests wurden nicht auf eine gewünschte Anzahl umgeschrieben. Ein zusätzlicher Lauf in der lang laufenden Review-Sitzung endete mit 38/39: ValidationAndReplay löste beim CollectGarbage ein Ensure wegen eines noch initialisierten LandscapeSubsystem der zuvor geladenen Heilhaus-Testkarte aus. Dieser Fehlersatz ist in AutomationGCFailure.json erhalten. Für die Schlussabnahme wurde der Editor nach Sicherungs-/Dirty-Prüfung frisch auf der gespeicherten Arbeitskarte gestartet und der gesamte Bestand erneut ausgeführt; keine Ensure-Warnung wurde unterdrückt und kein Test verändert. C++ unverändert; kein Build neu gestartet.

Map Check der gespeicherten Arbeitskarte: **0 Fehler / 0 Warnungen**, abschließend nach Testlauf und Rückgabe temporärer Zustände geprüft. Eigener Audit prüft Actorpositionen, gültige Occluderreferenzen, HISM-Collision/Culling und die Schutzdatei-Hashes. Material-Usage-Warnungen der neuen instanzierten Wohnhausgruppe wurden durch eigene instancing-fähige Materialkopien behoben. Gemeinsame Kit-Materialien blieben auf Datenträger unverändert.

Während einer frühen Prüfskript-Fassung konnte ein Materialreload einen weiteren Slate-Callback verschachteln, sodass eine Leveloperation vor Abschluss des vorigen Jobs lief. Dies verursachte einen Editorabsturz. Die eigene Jobqueue wurde mit Busy-/Reentrancy-Sperre und synchroner Ack-Prüfung korrigiert, der Editor neu gestartet, die gespeicherte Kopie erneut geöffnet und sämtliche finalen Fuß-/Automation-/Map-Prüfungen wiederholt. Schutzdateien blieben unverändert. Das ist kein ungeprüft als Engine-Fehler deklarierter Absturz.

## 6. Performance unter vergleichbaren Bedingungen

MacBook Air M4/16 GB, macOS Metal SM6. In-Process-PIE im Floating-Fenster; 1280 × 740 Gameplayviewport, alle zehn Scalability-Gruppen Medium (1), 75 % Renderauflösung (nominal 960 × 555), VSync aus, kein FPS-Limit. Gleicher Meshy-V2-Player, identische Kamera. Je Punkt 5 s Warmup + 20 s CSV-Aufnahme, keine Teleports. Kein garantierter thermisch konstanter Zustand. Die letzten Messungen stammen **nach** der Wegkantenkorrektur.

| Standort | Original FPS | VisualV2 FPS | Original Game/GPU ms | VisualV2 Game/GPU ms | VisualV2 P95 Frame ms |
|---|---:|---:|---:|---:|---:|
| Dorf | 49.75 | 35.94 | 7.86/15.15 | 8.41/23.02 | 32.33 |
| Wald | 49.37 | 33.84 | 7.93/15.12 | 9.96/23.60 | 34.20 |
| OffenerWeg | 54.88 | 37.84 | 7.35/13.77 | 8.14/21.64 | 31.14 |
| HeilhausVillage | — | 36.23 | — | 8.91/21.92 | 32.07 |
| DichterWald | — | 39.27 | — | 7.82/20.80 | 29.85 |

Dorf/Wald/OffenerWeg sind dieselben Standorte der Originalkarte; tatsächliche Wald-/Weg-Endpunkte unterscheiden sich nur um wenige cm durch Fußsteuerung. HeilhausVillage und dichter Nordwald sind neue Bereiche ohne gleichwertige Originalszene. Ihre Werte sind keine Vorher-/Nachher-Differenz.

| Finale Messung | Playerposition cm (X,Y,Z) | Samples | Frame mean ms | Basepass / ShadowDepth / ShadowProjection ms | LumenSceneUpdate / SlateUI / Unaccounted ms |
|---|---|---:|---:|---:|---:|
| Dorf | (-760.00, -1410.00, 50.15) | 720 | 27.82 | 1.65/1.51/0.78 | 2.79/4.22/5.07 |
| Wald | (-746.71, -718.67, 50.15) | 676 | 29.56 | 1.70/1.42/0.76 | 2.90/4.14/5.71 |
| OffenerWeg | (-38.07, -48.01, 50.15) | 758 | 26.42 | 1.41/1.48/0.65 | 2.73/4.09/4.90 |
| HeilhausVillage | (-4106.15, 431.11, 50.15) | 726 | 27.60 | 1.69/1.65/0.63 | 2.65/3.91/5.61 |
| DichterWald | (-4293.95, 1531.43, 50.15) | 786 | 25.46 | 1.33/1.77/0.65 | 2.47/4.25/4.51 |

CSV Game-/GPU-Zeiten sind Mittelwerte gültiger Framereihen; CSV-Footer/Metadaten wurden ausgeschlossen. Frame-FPS werden aus den während der eigentlichen Aufnahme aufgezeichneten Tick-Abständen berechnet. Einzelne GPU-Passes sind keine addierbare Vollkostenrechnung. `Unaccounted` bleibt unzugeordnet und wird nicht fälschlich als Vegetationskosten ausgegeben.

Die Szene ist gegenüber dem Original messbar teurer. GPU-Zeit liegt über Game-Thread-Zeit; Blatt-Overdraw, Schatten und Lumen-Beiträge sind relevante Kosten. Vor der Schlussoptimierung ergab ein temporärer Nordwald-A/B-Test: alles sichtbar 30,16 FPS, Vegetation unsichtbar 36,43 FPS, Schatten aus 38,44 FPS. Das sind diagnostische Gesamtunterschiede mit Wechselwirkungen, keine isolierte Kostenangabe pro Blatt. Schatten-/Sichtbarkeitsänderungen wurden zurückgegeben; finale Qualität nicht pauschal reduziert.

Optimiert wurden statische HISM-Mobilität, vorhandene LODs/Culling, kein Schattenwurf der kleinen Pflanzen/Wegbänder sowie deren Distance-Field-/Indirect-Beitrag. Die frühere bestätigte Fassung vor der letzten Wegkorrektur lag im selben Ablauf bei 35,99/38,26/39,35 FPS; thermische/Editor-Unterschiede und die Materialänderung verhindern eine saubere isolierte Kausalzuordnung. Keine 60-FPS- oder konstante Standalone-Garantie.

Draw-Call- und Render-Thread-CSV-Counter sind hier auf Metal nicht zuverlässig: RHI/DrawCalls liefern 0, RenderThreadTime praktisch 0. Dies bedeutet nicht null Renderingaufwand; keine erfundenen Draw-Call-Zahlen. Echte separate Standalone-Prozessmessung wurde nicht durchgeführt. Das verfügbare MCP-StartPIE-Werkzeug stuft NewProcess ausdrücklich auf In-Process-PIE zurück; der Fenstertitel „Standalone 0“ bezeichnet den Netzwerkmodus, nicht einen eigenständigen Prozess.

Rohdaten: `Saved/Profiling/CSV/VisualV2_BeforeFinal_*.csv`, `VisualV2_AfterRelease_*.csv`; Messprotokolle `BeforeFinal_Performance.json`, `AfterRelease_Performance.json`, `CSV_ReleaseSummary.json`. Temporäre Mess-CVars wurden auf den Ausgangszustand zurückgegeben, keine Projekt-Renderdatei geändert.

## 7. Echte Bildnachweise

Alle Bilder sind native Unreal-Aufnahmen. Keine synthetischen Konzeptbilder, keine Render-Komposition aus Blender. Screenshots/CSVs/Prüf-JSONs liegen absichtlich als lokale Arbeitsartefakte unter Saved und gehören nicht in Git. Die folgende Auswahl verwendet den finalen Materialstand; Vorher/Nachher-Paar in derselben 1280×740/Medium75-Spielkamera. Die Detailbilder sind vom Engine-HighResShot erzeugte Ausschnitte einer 2560×1480-Aufnahme, kein Kameraumbau. Der letzte Fußlauf/dessen UI-Screenshots entstand nach Rückgabe der ursprünglichen Editor-Qualität; diese Bilder sind keine Performancevergleichsgrundlage.

- [Vorher, alter Startbereich](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/BeforeFinal_Dorf00000.png)
- [Nachher, gleicher Startbereich](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/AfterRelease_Dorf00000.png)
- [Dorf/Heilhaus mit UI](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/After_Heilhaus00005.png)
- [Wald](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/AfterRelease_Wald00000.png)
- [Bach/Brücke](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/After_BachBruecke00005.png)
- [Ruinen/Archivziel](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/After_Ruinen00005.png)
- [Dichter Nordwald](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/AfterRelease_DichterWald00000.png)
- [Heilhaus-Innenraum](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/After_Innenraum00005.png)
- [Kronenfreistellung aktiv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/After_CrownReveal_On00002.png)
- [Identischer Standpunkt, Originalmaterial zur Diagnose](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/After_CrownReveal_Off00002.png)
- [Player-Nahaufnahme](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/Detail_Player.png)
- [Wegkante-Nahaufnahme](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/Detail_PathEdge.png)
- [Vegetation-Nahaufnahme](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/Detail_Vegetation.png)

Acht-Richtungen-Bildfolge (native Screenshots, keine kontinuierliche Videoaufnahme):

- [Richtung 0](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/Direction_000002.png)
- [Richtung 1](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/Direction_100002.png)
- [Richtung 2](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/Direction_200002.png)
- [Richtung 3](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/Direction_300002.png)
- [Richtung 4](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/Direction_400002.png)
- [Richtung 5](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/Direction_500002.png)
- [Richtung 6](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/Direction_600002.png)
- [Richtung 7](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/DevTestMapVisualV2/Direction_700002.png)

Keine durchgehende Gameplay-Videoaufnahme erstellt. Die Route ist über FootFrames.jsonl und die acht Bildsequenzaufnahmen nachvollziehbar, aber ersetzt keine spätere menschliche Sichtung mehrerer Laufzyklen.

## 8. Selbstkritische visuelle Bewertung und offene Grenzen

- Größter Fortschritt: zusammenhängende warme Landschaft statt heterogener flacher Testmarker, deutlich bessere V3-Vegetation, organische Laufwege, tatsächliches Heilhaus/Innenraum und mehr lesbare Raumtiefe. Zentrale Weg-Artefakte und Astverdeckung wurden nach Bildprüfung korrigiert.
- Die Brücke ist weiterhin der alte einfache Geometrieblockout. Der Bach ist zu geradlinig und seine Wasseroberfläche einfacher als die Referenz. Kein hochwertiges neues Brücken-/Wassermesh als fertig ausgegeben.
- NPCs/Heilerin sind vergrößerte vorhandene 2D-Billboards, stilistisch noch nicht vollständig auf den Meshy-Player abgestimmt. Player und kleine Wildkreatur besitzen die vorhandenen Art-/Animationsgrenzen.
- Blattkartenwiederholung, relativ harte Schatten und die deutliche Kronenfreistellung bleiben sichtbar. Die Dichte ist gruppiert, aber noch nicht überall auf Referenzniveau. Vereinzelte Wegverzweigungs-/Übergangskonturen benötigen weitere Artprüfung.
- Der neue Dorfbereich ist ein kleiner begehbarer Referenzabschnitt, kein fertig gebautes Westland-Dorf. Keine neue Innenraumfunktion für die Cottage zugesichert.
- Neue Bodendetails haben keine Laufkollision; alte grobe Testkollisionen bleiben teilweise hinter den neuen sichtbaren Props. Der geprüfte Rundweg ist frei, nicht jede Off-Path-Kombination erschöpfend geprüft.
- Gebäude, Player, Pflanzen und Boden sind technisch integriert, die hochwertige handgemalte Referenz wird noch nicht vollständig erreicht. Finale Artfreigabe und weitere Performanceoptimierung bleiben offen.

## 9. Dateien, Dokumentation und Git

Neue Content-Assets: eine Karte, fünf Wegmeshes und elf lokale Materialien/-Instanzen. Keine neuen Blueprint-/Gameplayklassen, keine Texturimporte, keine Blenderänderungen. Neue Editor-/Prüfwerkzeuge sind auf die neue Kartenkennung/Namespace beschränkt; Dress-/Polish-Skripte sind Einmal-Bauschritte und nicht als beliebig wiederholbare Migration gedacht. Vor einer Wiederholung des Fußtests muss der Dev-Slot separat gesichert werden: Das Testskript verwendet den echten Slot; die Sicherung und bytegleiche Rückgabe wurden in diesem Arbeitsdurchgang außerhalb des Skripts durchgeführt. Die für die Einmal-Bauschritte benötigten Review-/Baseline-Daten liegen lokal unter Saved.

Geändert wurden ausschließlich die folgenden bestehenden Dokumente; sie beschreiben tatsächlich bestätigte technische Entscheidungen, keine zusätzliche globale Stilfreigabe:

- `Docs/ENTSCHEIDUNGEN.md`
- `Docs/TECHNIK.md`

Neue Dateien (28):

- `Content/Environment/DevTestMapVisualV2/Materials/MI_V2_BarkReveal.uasset`
- `Content/Environment/DevTestMapVisualV2/Materials/M_V2_BarkRevealBase.uasset`
- `Content/Environment/DevTestMapVisualV2/Materials/M_V2_CrownReveal.uasset`
- `Content/Environment/DevTestMapVisualV2/Materials/M_V2_PathBlend.uasset`
- `Content/Environment/DevTestMapVisualV2/Materials/M_V2_WL_Glass_Instanced.uasset`
- `Content/Environment/DevTestMapVisualV2/Materials/M_V2_WL_Metal_Instanced.uasset`
- `Content/Environment/DevTestMapVisualV2/Materials/M_V2_WL_Plaster_Instanced.uasset`
- `Content/Environment/DevTestMapVisualV2/Materials/M_V2_WL_Roof_Instanced.uasset`
- `Content/Environment/DevTestMapVisualV2/Materials/M_V2_WL_Stone_Instanced.uasset`
- `Content/Environment/DevTestMapVisualV2/Materials/M_V2_WL_Timber_Instanced.uasset`
- `Content/Environment/DevTestMapVisualV2/Materials/M_V2_WL_Wood_Instanced.uasset`
- `Content/Environment/DevTestMapVisualV2/Meshes/SM_V2_Path_Cottage.uasset`
- `Content/Environment/DevTestMapVisualV2/Meshes/SM_V2_Path_Main.uasset`
- `Content/Environment/DevTestMapVisualV2/Meshes/SM_V2_Path_NorthLoop.uasset`
- `Content/Environment/DevTestMapVisualV2/Meshes/SM_V2_Path_VillageLoop.uasset`
- `Content/Environment/DevTestMapVisualV2/Meshes/SM_V2_Path_Wild.uasset`
- `Content/Maps/Dev_TestMap_VisualV2.umap`
- `Docs/DEV_TESTMAP_VISUAL_V2_PRUEFBERICHT.md`
- `Tools/FinalizeDevTestMapVisualV2.py`
- `Tools/MeasureDevTestMapVisualV2.py`
- `Tools/ModernizeDevTestMapVisualV2.py`
- `Tools/OptimizeDevTestMapVisualV2.py`
- `Tools/PolishDevTestMapVisualV2.py`
- `Tools/RefineDevTestMapVisualV2PathEdges.py`
- `Tools/RefineDevTestMapVisualV2Reveal.py`
- `Tools/ScopeDevTestMapVisualV2Materials.py`
- `Tools/TestDevTestMapVisualV2PIE.py`
- `Tools/ValidateDevTestMapVisualV2.py`

Temporäre Sicherungen, Jobqueue, Reviewbilder, Logs und Messdateien bleiben unter Saved; nichts davon gestaged. Keine Dateien gelöscht, kein Reset/Clean/Restore, kein Commit und kein Push.

### Finale Checks

Map Check der gespeicherten `/Game/Maps/Dev_TestMap_VisualV2`: 0 Fehler / 0 Warnungen. Audit: 1344 Actors, zehn unveränderte ursprüngliche Gameplay-/Startpositionen, 117 Heilhaus- und 17 Cottage-Occluderreferenzen gültig; alle 129 Schutzdateien einschließlich ursprünglichem Dev-Save bytegleich. Keine schmutzigen Content-Pakete oder Benutzerkarten. `git diff --check`: ohne Ausgabe erfolgreich; neue Markdown-/Pythontexte zusätzlich auf Syntax, Dateipfade und Whitespace geprüft. Nichts gestaged, kein Commit/Push.

### Git-Status

```text
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
?? Content/Environment/DevTestMapVisualV2/Materials/MI_V2_BarkReveal.uasset
?? Content/Environment/DevTestMapVisualV2/Materials/M_V2_BarkRevealBase.uasset
?? Content/Environment/DevTestMapVisualV2/Materials/M_V2_CrownReveal.uasset
?? Content/Environment/DevTestMapVisualV2/Materials/M_V2_PathBlend.uasset
?? Content/Environment/DevTestMapVisualV2/Materials/M_V2_WL_Glass_Instanced.uasset
?? Content/Environment/DevTestMapVisualV2/Materials/M_V2_WL_Metal_Instanced.uasset
?? Content/Environment/DevTestMapVisualV2/Materials/M_V2_WL_Plaster_Instanced.uasset
?? Content/Environment/DevTestMapVisualV2/Materials/M_V2_WL_Roof_Instanced.uasset
?? Content/Environment/DevTestMapVisualV2/Materials/M_V2_WL_Stone_Instanced.uasset
?? Content/Environment/DevTestMapVisualV2/Materials/M_V2_WL_Timber_Instanced.uasset
?? Content/Environment/DevTestMapVisualV2/Materials/M_V2_WL_Wood_Instanced.uasset
?? Content/Environment/DevTestMapVisualV2/Meshes/SM_V2_Path_Cottage.uasset
?? Content/Environment/DevTestMapVisualV2/Meshes/SM_V2_Path_Main.uasset
?? Content/Environment/DevTestMapVisualV2/Meshes/SM_V2_Path_NorthLoop.uasset
?? Content/Environment/DevTestMapVisualV2/Meshes/SM_V2_Path_VillageLoop.uasset
?? Content/Environment/DevTestMapVisualV2/Meshes/SM_V2_Path_Wild.uasset
?? Content/Maps/Dev_TestMap_VisualV2.umap
?? Docs/DEV_TESTMAP_VISUAL_V2_PRUEFBERICHT.md
?? Tools/FinalizeDevTestMapVisualV2.py
?? Tools/MeasureDevTestMapVisualV2.py
?? Tools/ModernizeDevTestMapVisualV2.py
?? Tools/OptimizeDevTestMapVisualV2.py
?? Tools/PolishDevTestMapVisualV2.py
?? Tools/RefineDevTestMapVisualV2PathEdges.py
?? Tools/RefineDevTestMapVisualV2Reveal.py
?? Tools/ScopeDevTestMapVisualV2Materials.py
?? Tools/TestDevTestMapVisualV2PIE.py
?? Tools/ValidateDevTestMapVisualV2.py
```

### Tatsächlich ausgeführte Automationstests

- `PokeMonster.Battle.Presentation.EventSequence`: Success
- `PokeMonster.Battle.Session.HitsAndTypes`: Success
- `PokeMonster.Battle.Session.KOAndFinish`: Success
- `PokeMonster.Battle.Session.OrderAndPP`: Success
- `PokeMonster.Battle.Session.ValidationAndReplay`: Success
- `PokeMonster.Battle.Team.SwitchAndKO`: Success
- `PokeMonster.Battle.UI.BindingAndInputLock`: Success
- `PokeMonster.Battle.UI.MissedStatusLog`: Success
- `PokeMonster.Battle.UI.UnavailableMoves`: Success
- `PokeMonster.Battle.Damage`: Success
- `PokeMonster.Battle.HitCheck`: Success
- `PokeMonster.Battle.TypeChart`: Success
- `PokeMonster.Building.Inn.CameraAndFootprint`: Success
- `PokeMonster.Building.RelocatedInterior.MappingAndTransition`: Success
- `PokeMonster.Capture.WildBattleAndTeamTransfer`: Success
- `PokeMonster.Creatures.DataSystem`: Success
- `PokeMonster.Creatures.EvolutionEligibility`: Success
- `PokeMonster.Creatures.GrowthCurves`: Success
- `PokeMonster.Creatures.Progression`: Success
- `PokeMonster.Dialogue.PagesAndState`: Success
- `PokeMonster.Encounter.OverworldIntegration`: Success
- `PokeMonster.Encounter.TrainerProfileAndDefeatState`: Success
- `PokeMonster.Encounter.WildProfileAndSources`: Success
- `PokeMonster.Items.InventoryAndUsage`: Success
- `PokeMonster.Moves.DataAssetsAndSlots`: Success
- `PokeMonster.Overworld.Checkpoint.DefeatAndSave`: Success
- `PokeMonster.Overworld.HealingHouse.CollisionAndCutaway`: Success
- `PokeMonster.Overworld.HealingHouse.Layout`: Success
- `PokeMonster.Overworld.HealingHouse.RestCheckpointSaveAndDefeat`: Success
- `PokeMonster.Overworld.MiniSlice.ProgressAndSave`: Success
- `PokeMonster.Overworld.RestPoint.HealAndSave`: Success
- `PokeMonster.Overworld.UI.Foundation`: Success
- `PokeMonster.Player.BuildingInteriorCamera`: Success
- `PokeMonster.Player.Foundation`: Success
- `PokeMonster.Player.MeshyPresentation`: Success
- `PokeMonster.Player.ScaleCalibration`: Success
- `PokeMonster.Quest.MiniSlice.FlowAndSave`: Success
- `PokeMonster.Save.RejectInvalidData`: Success
- `PokeMonster.Save.SnapshotAndDisk`: Success
