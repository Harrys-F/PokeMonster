# VisualV2 Fab Asset Trial V1 – Prüfbericht

## Ergebnis und Umfang

Technischer Asset-/Gestaltungstest auf der vorhandenen `/Game/Maps/Dev_TestMap_VisualV2`.
Ausgangspunkt `1c548922939588d59999b0d1e4fe6a7ad4408b64`, Branch `main`.
Sechs begehbare Themenbereiche sind vorbereitet. **Die gestalterische Freigabe erfolgt
anschließend durch Harry. Keine Übertragung nach Westland.** Die zurückgenommene
European-Beech-Waldsektion wird nicht wiederhergestellt.

12 ursprüngliche Umwelt-Actors erhalten neue lokale Bindungen bzw. Zaunpositionen.
30 neue HISM-Gruppen enthalten 2.249 Instanzen, hinzu kommen drei vorhandene Dorfprops.
Alle übrigen ursprünglichen Actor-Signaturen und WorldSettings stimmen mit der
Bestandsaufnahme überein. Keine neue Map, Pokémon-Art, KI-, Kamera-, Inventar-,
Speicher-, Kampf- oder Renderingprofil-Architektur.

## Tatsächlich untersuchte Quellen

Projektpakete und `/Users/Shared/UnrealEngine/Launcher/VaultCache/FabLibrary` wurden
inventarisiert. Importierte Originalpakete bleiben unverändert und lokal.

| Paket | Tatsächlicher Bestand | Technik / Quellenauflösung | Verwendung / Bewertung |
|---|---|---|---|
| StyleHex_Studio | 29 Static Meshes; Gras, vier Blumenclumps, Pflanzen, drei Büsche | Meshes meist 59–596 Dreiecke an LOD0, vorhandene LODs; Pflanzenatlanten 2K, kleinere Utility-Texturen 128–1024px; Masked, Two-Sided, Instancing vorhanden | Drei Gras-, vier Blumen- und eine Buschvariante verwendet. Besonders geeignet für die farbige Fantasy-Wiese. Lokale Instanzen begrenzen Helligkeit/Wind und dämpfen Buschgrün. Masked Overdraw bleibt ein Kostenpunkt. |
| Jayant_Chakradhari_Assets/Free_Grass | Drei Texturgräser, je ein einzelnes Quad mit zwei Dreiecken | 2K-Texturen, ursprünglich 200cm hohe Karten, einseitiger Masked-Parent | Untersucht, nicht eingebaut: aus frei drehbarer Third Person zu deutlich richtungsabhängig; kein Ersatz für plastische Büschel. |
| Pack_Bonus | 15 Materialgruppen, 75 Texturen | 70 Texturen 2K, fünf 4K; Gras, Stein, Holz, Wände, Fliesen | Grass_2-Farbe und -Normal im eigenen Boden verwendet. Andere Oberflächen sind Vergleichsoptionen, keine Gebäudefassaden pauschal ersetzt. |
| RockEnv_Pack | 141 Static Meshes, fünf Instanzen, zwei Master; 14 zusätzliche TGA-Dateien | Üblicherweise vier LODs; kleine Steine 444–1.340 Dreiecke, ca. 11–35cm breit; überwiegend 1K-Texturen, dazu 512px/2K | Sieben kleine Steinvarianten für Bachbett/Ufer. Runde SimpleRocks mit kompatibler RockEnv-Oberfläche. Die zuerst getesteten kantigen Jungle-Rock-Gruppen wurden ersetzt; Eis-/Mesa-/Höhlenmodule passen nicht in diese Vergleichsbereiche. |
| SimpleRocks | 40 Felsvarianten | Sechs LODs, oft ca. 1K–4K Dreiecke an LOD0; elf 4K- und vier 32px-Utility-Texturen; untersuchte Felsen ohne einfache/konvexe Hülle | Drei rundere Silhouetten als lokale Ableitungen mit je einer 26-DOP-Hülle. Originalmesh und Originalmaterial unverändert. Keine Nanite-Aktivierung erzwungen. |
| Megaplant_Library | 725 Assets: 244 statische Teile, 203 Skeletal Meshes, 203 Skelette, dazu PVE/Growth-Daten, 36 Texturen, 18 MIs | Meist 4K, teilweise 2K und 4K×8K; etliche Teile Nanite/Voxel-konfiguriert | Nicht als funktionsfähige Gesamtbäume übernommen: vollständige Pflanzen überwiegend Skeletal/PVE; fehlende Parents unter `/ProceduralVegetationEditor/SampleAssets/Materials/MasterMaterials/…`. Inventarlauf meldet zudem nicht aktivierte Voxel-Funktionen. Keine Default-Material-Ersatzbäume in die Map gestellt. |
| Bereits vorhandenes Fab/EuropeanBeech | 34 statische Meshes, Material-/Texturbibliothek | Nur Bestand geprüft | Originale bleiben lokal; keine Wiederherstellung des verworfenen Waldtests und keine neue Beech-Platzierung. |

Die frühe `Blueprint_GetSizeX`-Abfrage traf während asynchroner Kompilierung auf den
32px-Engine-Platzhalter. Diese Werte sind **keine Quellenauflösungen**. Maßgeblich
sind die später ausgelesenen `Dimensions`-Metadaten und die Importquellen; siehe
`NativeGameplay06_Metadata.json`. Tatsächliche 32px-Utility-Texturen bleiben davon
zu unterscheiden.

Im Vault liegen zusätzlich Grass-/Uncut-/Ribbon-Grass, Field Poppy, Lady/Beech Fern,
Forest Floor, Mossy Forest Floor, Forest Path, Rocky Forest Path, Grass And Rubble,
Nordic Forest Ground, Mossy Rocks, Rock Cliff und Cracked Wooden Planks vor.
Die kleinen Megaplants-Vaultdateien sind nicht mit vollständig importierten
spielbereiten Pflanzen gleichzusetzen. Nicht jeder Cacheeintrag ist ein fertiges
Unreal-Paket. Es wurden keine weiteren Downloads gestartet.

Gezielt lokal importiert: Forest Floor, Forest Path und Grass And Rubble mit
jeweils vorhandenen 2K-B/N/ORM-Texturen sowie Field Poppy A/B und Lady Fern A/B mit
2K-Farb-/Normal-/Opazitätsatlas. Gewählte Original-LOD1-Geometrie: Mohn 246/948,
Farne 1.129/195 Dreiecke. Maßstab und Silhouette werden gleichmäßig skaliert,
Original-FBX/GLTF/Texturen im Cache nicht verändert. Diese Imports und die drei
Fab-Fels-Kollisionsableitungen bleiben im lokalen `Fab/VisualV2TrialLocal`.

## Gestaltung der sechs Bereiche

| Bereich | Tatsächliche Änderung | Schnelle Sichtposition in cm / Yaw |
|---|---|---|
| Blumenwiese | Unregelmäßige Gras-/Blumeninseln, echte Mohnvarianten, verschiedene Höhen und freie Zwischenräume; Gras meist 25–48cm, Mohn 40–68cm | −4800, −2100 / 15° |
| Waldrand | Lady-Fern-Varianten, kleine Fab-Sträucher, bestehende Eichen und Untervegetation; keine neuen kompletten PVE-Bäume | −4750, 1050 / 45° |
| Bach/Ufer | Vorhandener Flussumriss; lokale Geländekopie mit flach auslaufendem, bis 34cm abgesenktem Bett, kiesige Färbung, 311 Bett- und 81 Ufersteine; ursprüngliche Reeds/Moos/Gräser bleiben | −750, −650 / 30°; Detail −100, −500 / 90° |
| Fels-/Geländebereich | 17 gerundete Felsen abseits des ursprünglichen Waldwegs, ca. 55–105cm hoch, lokale konvexe Kollisionen; ursprüngliche begehbare Höhenstufen bleiben | Detail −1700, 1200 / 35° |
| Dorf/Kräutergarten | Fünf vorher isolierte Zaunsegmente zu einer nachvollziehbaren Gartenbegrenzung umgeordnet, 80 niedrige Blumenclumps; vorhandenes Fass, Kiste und Bank sinnvoll zugeordnet | Detail −4900, −400 / 55° |
| Pokémon-Lebensraum | Vegetationsrahmung des vorhandenen ForestEdge-/Wiesenübergangs, Sichtschneisen und bestehende natürliche Population | −2350, 1300 / 35° |

**Boden:** eigenes `M_FAT_Ground` mischt die geprüfte alte Farbgrundlage mit
Fab-Gras, Waldboden, steinigem/feuchtem Ufer und Felsbereichen über weiche
ortsabhängige Masken. Feine Normalen, Makrovariation und ca. 2,3m Texturskalierung;
keine zusätzlichen selbstleuchtenden Böden. Wege erhalten ein eigenes gedämpftes
Texturmaterial bei ca. 1,9m Skalierung. Forest Path wirkte im ersten Versuch zu
stark wie Holzmulch; die endgültige Mischung ist zurückhaltender. Keine Änderung
an gemeinsam verwendeten Elternmaterialien.

**Wasser:** `M_FAT_Stream` ist eine eigene Ableitung des vorhandenen Projektwassers,
kein erfundenes neu gefundenes Fab-Wasserpaket. Masked Single Layer Water erhält
Flussmaske und zeitabhängige Normalen; Opacity 0,23, Roughness 0,17 und zurückhaltende
Streuung/Absorption erzeugen sehr klares, leicht gefärbtes Wasser. Echte Metal-Pässe
`SingleLayerWaterDepthPrepass` und `SingleLayerWater` sind gemessen. Kleine Steine
sind 3–10cm hoch. Der Teich, seine Tiefe, Wasserhöhe, Lebensräume, Barrieren und
der trockene Abstand zum Bach bleiben erhalten. Brücken und Garados V4 unverändert.

**Korrekturen aus echten Tests:** Der erste Array-Bearbeitungsschritt hatte die
Kopie einzelner Unreal-Vektoren statt der Mesh-Liste verändert. Die endgültige
Meshkopie wurde mit expliziten neuen Positionen aufgebaut und zurückgelesen;
tatsächlicher Bettvertex liegt unter −30cm. Die zuerst verwendeten kantigen
Felsen wurden nach Bildprüfung ersetzt. Der Fußlauf belegte eine Blockade durch
die neuen Felsgruppen; Overlap-Proben identifizierten genau diese HISM-Gruppen.
Nach Versetzen und erneuter Kollisionsprüfung ist der Weg frei. Vegetation und
Kiesel bleiben ohne Pawn-Kollision, die gerundeten Felsen besitzen ihre eigenen
lokalen Hüllen. Kein pauschales Abschalten aller Kollisionen.

## Pokémon und Gameplay

Globales Limit weiterhin 14, maximal sechs aktive Arten; zehn bestehende
VisualV2-Zonen und alle ursprünglichen Regeln/Profile unverändert. Keine zweite
KI, keine neuen Modelle und kein erzwungener Garados im kleinen Bach. Die
PIE-Beobachtung erfasst Population in allen zehn Zonen; maximal 14 gleichzeitig.
Beobachtet wurden Bisasam, Pikachu, Raupy, Enton, Karpador und Glumanda
(interner historischer Schlüssel `Zunderlauf`). Nicht alle registrierten Arten
werden als tatsächlich beobachtet ausgegeben.

Im aktiven Lauf treten Wander, Rest, Idle, Forage, Curious/Approach, Social,
Observe und Battle auf. Die bessere Rahmung macht vorhandene Pokémon erkennbarer;
es gibt keine zusätzliche künstliche Show-Population. Zeitabhängige Profile,
Begegnung, Fang und Begleiter verwenden dieselben Dienste wie zuvor.

## Reproduzierbare Performance

Tatsächliche Hardware: MacBook Air `Mac16,12`, Apple M4 mit zehn GPU-Kernen,
16GB RAM, arm64, macOS 27.2. Installierte Engine 5.8.4, CL58902052; nicht neu
installiert oder geändert. Displaydaten stehen in `Hardware.json`.

Getrennte Development-Spielprozesse über die vorhandene UnrealEditor-Binärdatei
mit `-game`, expliziter VisualV2 und jeweils frischem UserDir; kein packaged
Shipping-Test. Geräteprofil laut Log `MacEditor`. QHD-Viewport und PNG-Abmessungen
2560×1440 geprüft, High-Gruppen jeweils 2, Screen Percentage 75, Software-Lumen/IFG,
VSM4 unverändert. 1920×1080 ist die rechnerische interne Zielauflösung; der interne
ViewRect wurde in diesem Assetauftrag nicht separat erneut vermessen.

Der globale CVar `r.AntiAliasingMethod=4` ist hier nicht der endgültige View-Pfad:
der erhaltene map-eigene `PokeMonsterTemporalAABlendable` wählt TAA/Temporal Upscale.
Positive `GPU/TAA`- und `GPU/LumenIrradianceFieldGather`-Pässe bestätigen die
verwendeten Verfahren. Keine heimliche Umstellung auf TSR oder andere Qualität.

Primäre Reihen: `NativeBefore06` und `NativeFinal06`. Das Vorher stellt ausschließlich
in der wegwerfbaren Laufzeit die erfassten ursprünglichen Material-/Meshbindungen
und Zaunpositionen wieder her und blendet eigene Gruppen aus; keine Map wird
zurückgespeichert. Zusätzliche echte Vorher-Aufnahmen stammen aus der noch
unbearbeiteten Map unter `Before/`.

Drei Messfenster je sechs Hauptpositionen, jeweils 4s Beruhigung und 6s Messung,
VSync/FPS-Limit temporär aus; keine Videoaufnahme. Stills erst nach CSV-Stopp.
Beide Hauptreihen stehen nachweislich auf Tag 1, 12:00 und Sonne75°.
Der vorhandene Menü-Pausenmechanismus hält die Zeit: **statischer Vergleich,
kein Nachweis regulärer bewegter 30-FPS-Spielperformance.** `Shot` enthält kein Menü.
Zeitfixture ausschließlich in frisch erstellten isolierten V11-Testslots: ein
streng geprüfter, eindeutig getaggter acht Byte großer SecondsOfDay-Wert wird
geändert und vom vorhandenen normalen Save/Load-Dienst geladen. Kein Zugriff auf
Nutzerstände, keine neue Uhr und keine dauerhafte Zeitregeländerung.

Frühere native Reihen mit ignorierten PIE-only-Zeitbefehlen bzw. unbrauchbaren
Fixturezugriffen sind nicht die Endmessung. Unreal schreibt eine zusätzliche
CSV-Kopfzeile/Metadaten ans Ende; die endgültige Auswertung verwendet die finale
Kopfzeile und liest ausschließlich Datenzeilen, keine Metadaten als Frames.
Alle neun Bildpaare besitzen verifizierte QHD-Abmessungen, gleiche Kameras und
Spielerpositionen innerhalb 0,1cm/Grad; Kreaturen-/Idle-Phasen sind nicht identisch.

### Hauptvergleich: Mittel der drei Läufe

| Messpunkt | FPS vorher | FPS nachher | GPU vorher ms | GPU nachher ms | Frame-p95 nachher ms |
|---|---:|---:|---:|---:|---:|
| Blumenwiese | 36.08 | 29.24 | 26.81 | 33.13 | 36.39 |
| Waldrand | 39.03 | 33.36 | 24.75 | 29.05 | 31.85 |
| Flussufer | 34.43 | 31.77 | 28.00 | 30.48 | 32.95 |
| Felsen | 45.35 | 38.27 | 21.15 | 25.19 | 27.50 |
| Dorf | 33.23 | 30.73 | 29.34 | 31.61 | 34.08 |
| Lebensraum | 42.30 | 37.40 | 22.83 | 25.76 | 28.11 |

Frame-p95 ist hier das Mittel der drei Fenster-p95, kein gepooltes p95. Der
Messpunkt „Felsen“ liegt bei den alten Höhenstufen; die eigentliche neue
Felsgruppe hat zusätzlich eine eigene Detailaufnahme/ein einzelnes Messfenster.
Die vollständigen Einzelwerte, Spannweiten, Kameras und Populationszahlen stehen
in `Analysis.json`. Keine GPU-Passbereiche ungeprüft zusammenrechnen.

| Messpunkt | Basepass vorher/nachher ms | ShadowDepths vorher/nachher ms | Game Thread nachher ms | Render Thread nachher ms | IFG nachher ms |
|---|---:|---:|---:|---:|---:|
| Blumenwiese | 7.44 / 7.76 | 1.36 / 1.62 | 1.66 | 34.19 | 4.09 |
| Waldrand | 6.44 / 6.51 | 1.59 / 1.86 | 1.84 | 30.01 | 3.10 |
| Flussufer | 6.15 / 5.02 | 1.48 / 1.77 | 1.67 | 31.48 | 4.20 |
| Felsen | 3.15 / 3.49 | 1.53 / 1.73 | 2.18 | 26.11 | 3.26 |
| Dorf | 8.84 / 8.59 | 1.68 / 1.90 | 1.60 | 32.54 | 3.09 |
| Lebensraum | 4.86 / 4.09 | 1.84 / 2.17 | 2.17 | 26.74 | 3.24 |

Render-Thread-Counter enthält Synchronisation/Warteanteile und ist keine isolierte
CPU-Arbeitszeit. ShadowDepths ist nicht die vollständige VSM-Gesamtsumme. Einzelne
Licht-/Materialgruppen wurden in diesem Assettest nicht isoliert als exakte
Kostentreiber vermessen. Die dichtere Gestaltung kostet im Gesamt-GPU-Vergleich
zusätzliche Zeit; ein alleiniger Basepass-Wert erklärt das nicht vollständig.

**Keine durchgehend stabilen 30 FPS:** Blumenwiese im Mittel unter30; auch Dorf
hat p95 oberhalb33,3ms. Keine globale Qualitätsabsenkung als Gegenmaßnahme.
Die Gestaltung bleibt eine bewusst beurteilbare Qualitäts-/Kostenvariante.

Separater aktiver Funktionslauf `NativeGameplay08`: 111.4s, beobachtetes Gesamtmittel 33.01 FPS und p95 39.22ms. Enthält Aufnahmen, UI, Kampf, Laden und Mapwechsel; ausdrücklich kein aufnahmefreier Bewegungsbenchmark.

## Tatsächlich durchgeführte QA

| Prüfung | Ergebnis / Nachweis |
|---|---|
| Editor-Build | Exit0, 18,13s; `Build/Result.json` |
| Vollständige bestehende Automation | 325/325, 0 failed, 0 succeededWithWarnings, 0 notRun/inProcess; `FullAutomation/Report/index.json` |
| Strenger vorhandener QA-Vertrag | Engine0 / Wrapper0; derselbe Berichtvertrag über isolierten Runner, nicht ein nachträglich erfundener Erfolg |
| Zwölf bestehende Projekt-Map-Checks | Je0 Fehler/0 Warnungen zwischen den expliziten Prüfmarkern; keine importierten Demo-Maps als zusätzliche neue Projektmaps gespeichert |
| PIE | `PIE_Gameplay05`, erfolgreich; echter zusammenhängender Eingabe-/Physiklauf über Wiese, Dorf, Wald, Habitatgrenzen und Brücke |
| Separater Spielprozess | `NativeGameplay08`, erfolgreich, inklusive tatsächlichem Mapwechsel und Rückladen nach VisualV2 |
| Kampf/Fang | Natürliches Habitat-Pokémon, reguläre ClassicBattle-Attacke/AP-Verwendung, normale MasterBall-Transaktion aus nur im Test hinzugefügtem Gegenstand, eindeutige zusätzliche Teaminstanz |
| NPC/Innenraum | Bestehender Wandererdialog, wirklicher Türdurchgang in den verschobenen Heilhausinnenraum und zurück; Übergang vollständig abgewartet |
| Save/Load | Isolierter Menü-Roundtrip erhält vollständiges Team/AP, Inventar, Position und Weltzeit; späterer echter Kartenwechsel und Rückkehr über normalen Loader |
| Team/Begleiter | Reguläres Team, Sortierung, vorhandene Teamoberfläche, aktiver Begleiter vor/nach Laden/Reise |
| Weltzeit/Licht | 06/12/19/22 geprüft, Mittag75°, Tageslänge120 unverändert |
| Schnelle Besuche | `VisitReview/Result.json`: sechs Bereiche und Rückkehr, ursprünglicher Teamzustand/Anker wiederhergestellt |
| Controller | Vorhandene Enhanced-Input-Bewegung/Sprintaktion geprüft; kein physischer Controller-Test behauptet |

Die finalen nativen Läufe laden/kompilieren keine fehlerhaften Trial-Materialien
und melden keine fehlenden Trial-Assets, Fatal Errors oder Assertions.
**Rohlogs sind dennoch nicht fehler-/warnungsfrei:** Im NullRHI-Start stehen17
`LogAutomationTest: Error: Condition failed` vor der eigentlichen Projekt-Testserie;
die exportierten 325 Projekttests sind erfolgreich. Der `-game`-Start mit dieser
Engine-Binärdatei meldet bestehende experimentelle Engine-Toolset-Pythonfehler
(fehlende Editor-Typen wie ToolsetDefinition/AgentSkill/PythonTestRunner).
Diese werden getrennt von funktionalen Projektfehlern ausgewiesen, nicht behoben
oder als verschwunden bezeichnet. Bekannter `idevice_id: Bad CPU`-Text wurde in
diesen finalen Läufen nicht beobachtet; keine Reparatur des iOS-Helfers behauptet.

Zwischenstände enthalten absichtlich aufbewahrte Fehlversuche: Python-API-Namen,
noch unvollständige Materialgraphen, nicht verwendbare Megaplant-Abhängigkeiten,
den belegten blockierten Felsweg und Korrekturen im Testharness. Der zusätzliche
Positionslogger von NativeGameplay06 griff während Mapabbau kurz auf den alten
Player zu; die finale Wiederholung08 prüft Referenzen vor dem Protokollieren und fängt bereits entleerte Python-Wrapper ab. Die Wiederholung07 musste wegen der fehlerhaften Diagnose-Schleife regulär per SIGTERM beendet werden; kein Force Quit und keine Nutzersitzung betroffen.
Diese Zwischenläufe werden nicht als saubere Endabnahme ausgegeben.

## Echte Bilder und schneller Besuch

Kontrollierte vollständige QHD-Bildpaare:
`Saved/ProjectRefinement/VisualV2FabAssetTrialV1/NativeBefore06/<Szene>.png`
und `NativeFinal06/<Szene>.png`.

Szenen: `Blumenwiese`, `Waldrand`, `Flussufer`, `Felsen`, `Dorf`, `Lebensraum`,
zusätzlich `Kraeutergarten`, `Bachbett`, `Felsgruppe`.
Die Übersicht `Ergebnisuebersicht.png` enthält nur verkleinerte echte Endaufnahmen
und Beschriftungen; keine generierten oder retuschierten Spielbilder.
PIE-/Gameplaybelege liegen zusätzlich in `PIE_Gameplay05/` und `NativeGameplay08/`.
Kontrollmedien bleiben lokal unter Saved und werden nicht öffentlich gepusht.

In gewöhnlichem VisualV2-PIE mit Third Person:

```text
py exec(open(r"/Users/harry/Developer/PokeMonster/Tools/VisualV2FabAssetTrialV1/Visit.py").read(), {"AREA":"Blumenwiese"})
```

Weitere AREA-Werte: `Waldrand`, `Flussufer`, `Felsgruppe`, `Kraeutergarten`,
`Lebensraum`; Rückkehr mit `Zurueck`. Das Werkzeug verwendet den bestehenden
NPCGround-RAM-Speicherschutz und Rückkehranker, einschließlich ursprünglichem
Kamera-Yaw. Kein neuer C++-Konsolenbefehl und kein unabhängiges Speichersystem.
Alternativ alle Bereiche über die erhaltenen Wege selbst erlaufen.

## Grenzen und nächste gestalterische Entscheidung

Besonders geeignet: StyleHex-Blumen/Gras, echte Mohn-/Farnvarianten, maßstäbliche
RockEnv-Kiesel und ausgewählte SimpleRocks-Silhouetten. Weniger geeignet: riesige
Eis-/Mesa-/Höhlenmodule in der kleinen Wiese, einseitige Einzelkarten als alleinige
Grasdarstellung und derzeit unvollständig aufgelöste PVE-Gesamtpflanzen.

Noch fehlend bzw. nicht freigegeben: vollständige kompatible Megaplant-Eltern-
materialien/Vegetationspipeline; ein tatsächlich neues Fab-Flusssystem und neue
Hobbit-Dorfprop-Pakete sind im untersuchten Projektbestand nicht nachgewiesen.
Daher vorhandene Projektwasser-/Dorfobjekte verwendet, keine falsche Herkunft
behauptet. Alte rechteckige begehbare Test-Höhenstufen bleiben sichtbar; dies ist
kein vollständiger organischer Landschaftsumbau. Manche Uferansichten bleiben
durch die bestehende dichte Vegetation verdeckt. Buschfarben/Blütenfülle und das
sehr klare Bachwasser benötigen Harrys gestalterische Beurteilung. Die echte
Performancekostenabwägung bleibt offen; keine pauschale Übernahme nach Westland.

## Projektschutz und Git

Vorhandene Nutzeränderung in `Config/DefaultEngine.ini` erhalten und nicht gestaged.
6255 vorhandene versionierte Dateien, 1488 vorhandene lokale Referenz-/Nutzerdateien
und 699 vorhandene Save-Dateien wurden vorab erfasst. Die abschließende Hashprüfung
steht in `ProtectionFinal.json`; zulässig abweichend sind ausschließlich die
beauftragte VisualV2, die engen Fab-Ignore-Regeln und dieser Auftragsvermerk in den
Entscheidungen. Westland, Biom-Testmap, Originalmodelle/-animationen, Rendering-
quellen, alle bisherigen Saves und Backup-Verweise bleiben erhalten.

Öffentlich versioniert werden nur eigene Werkzeuge, Dokumentation, die Zielmap und
neun eigene Material-/Terrainassets. Sieben enge Content-Ignore-Regeln schützen
lokale Fab-Pakete und lokale Import-/Kollisionsableitungen. **Ein frischer Checkout
benötigt die separat lizenzierten lokalen Fab-Imports; diese Quellen sind bewusst
nicht im öffentlichen Repository.** Keine Lizenzoriginale oder Kontrollmedien
pauschal gestaged. Kein Worktree, keine Projektkopie, kein destruktiver Git-Befehl.

Der Bericht gehört zum gezielten Abschlusscommit. Dessen Hash und tatsächliche
Remote-/LFS-Prüfung werden in `Saved/ProjectRefinement/VisualV2FabAssetTrialV1/GitFinal.json`
protokolliert; `git log -1 --format=%H -- Docs/VISUALV2_FAB_ASSET_TRIAL_V1.md` identifiziert
den versionierten Bericht. Nach Sicherung keine weitere Landschaftsbearbeitung.
