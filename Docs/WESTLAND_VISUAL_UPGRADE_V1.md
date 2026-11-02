# Westland Visual Upgrade V1

Stand: 02.11.2026. Ausgangscommit `37489167f6a327dcae9d7e3c2a8a0dc37463b014`, Branch `main`. Bearbeitete vorhandene Map: `/Game/Maps/Dev_WestlandRegion`. Referenz: `/Game/Maps/Dev_TestMap_VisualV2`.

## Ergebnis und Abgrenzung

**1.710 alte Baum-Sheets wurden vollständig durch sieben vorhandene 3D-Baumvarianten ersetzt.** Zusätzlich sind 6.668 Busch-Sheets durch zwei vorhandene 3D-Buschvarianten ersetzt. Alte Sheet-Gruppen bleiben als leere Actor-Identitäten erhalten; keine übereinanderliegenden alten Baum-/Buschflächen mehr. Die vorhandenen Standorte sind übernommen, Materialien, Bodenvegetation und Wasser map-spezifisch verbessert.

Keine neuen Modelle, Maps, Worktrees oder Projektkopien. Das zurückgenommene Buchenwaldexperiment bleibt zurückgenommen; keine Fab-/Quixel-Originale verwendet oder verändert. Gebäude, Wege, Terrain-/Flussmeshgeometrie, vier NPC-Funktionen, 16 Lebensräume, drei Funde, Pokémon-Modelle/-Animationen einschließlich Garados V4 sowie Grafikprofil und Kamera bleiben erhalten. Die einzige allgemeine C++-Ergänzung ist der ausdrücklich beauftragte transiente Spieler-Testgeschwindigkeitsfaktor.

Verwendete bereits installierte Engine: **5.8.4, CL58902052**, Mac Development/Metal, Apple M4/16 GB. Keine Engineinstallation oder -änderung; die ältere allgemeine AGENTS-Angabe5.8.2 wurde nicht durch einen Enginewechsel umgesetzt.

## Bestandsaufnahme gegenüber VisualV2

Editor-Inventare beider tatsächlichen Maps liegen unter `Saved/ProjectRefinement/WestlandVisualUpgradeV1/`. In Westland standen Baum-/Busch-Sheets, Grassheets und ein schlichtes ursprüngliches Flussmaterial. VisualV2 verwendet inzwischen vorhandene plastische Grasmeshes, 3D-Vegetation, zusätzliche Bodenpflanzen und differenzierte Wasseroberflächen.

Übernommen werden die tatsächlich vorhandenen Projektassets, keine angenommenen Assetnamen. VisualV2s aktuell gebundener Bach verwendet noch `M_SoftWater`; der aktuelle Teich verwendet das beleuchtete `M_AIV3PondWater`. Für Westlands Fluss wurde dessen geeignete Lit-/Translucency-/Normal-/SSR-Struktur abgeleitet und von der fest codierten VisualV2-Teichform befreit. Es wurde weder ein neuer Teich noch ein zweiter Fluss erzeugt.

## Bäume, Sträucher und Kollision

| Vorhandenes Mesh | Anzahl in Westland |
|---|---:|
| `QualityV3/Meshes/Trees/SM_WLA_OakAncient_V3` | 860 |
| `Meshes/Trees/SM_WLA_OakYoung_A` | 209 |
| `Meshes/Trees/SM_WLA_OakYoung_B` | 204 |
| `Meshes/Trees/SM_WLA_Birch_A` | 212 |
| `Meshes/Trees/SM_WLA_Birch_B` | 208 |
| `Meshes/Trees/SM_WLA_FruitTree_A` | 7 |
| `Meshes/Trees/SM_WLA_FruitTree_B` | 10 |

Alle Pfade sind relativ zu `/Game/Environment/WestlandAssetLibrary/`. Genau1.710 ursprüngliche Baum-XY-Standorte, deterministische Varianten, variierte Rotation/Proportionen, ungefähr 6–20 m Gesamthöhe; Obstbäume auf 6,5 m begrenzt. Tatsächliche Geländeabfrage statt allein analytischer Höhenfunktion; Stammfuß 0,8 cm eingebettet. Keine Bearbeitung der Meshes, UVs, Originalquellen oder bestehenden Bibliotheksmaterialien.

Zwei vorhandene Bibliotheks-Buschmeshes: Bush_A 4.445 / Bush_B 2.223, etwa 0,5–1,35 m hoch; ebenfalls tatsächlicher Boden, keine blockierenden Busch-/Blätterkollisionen.

Die sieben Baum-HISM-Gruppen verwenden die **bereits importierten einfachen Stamm-UCX-Hüllen** ihrer jeweiligen Modelle, je eine konvexe Hülle. Pawn und Camera blockieren; Visibility ignoriert diese Hüllen, damit der bestehende Pokémon-Bodenplaner weiterhin das Terrain abfragt. Keine komplexe Kronen-/Dreieckskollision, kein neuer Collision-Mesh, keine Änderung am BodySetup der Originalassets. Die vorherigen schmalen `WR_TrunkCollision`-Zylinder bleiben verborgen und sind als doppelte Hindernisse deaktiviert. Ihre alten Platzierungsdaten sind erhalten; 17 zuvor unbedeckte Baumstellen wurden während der Zwischenstufe ergänzt, inzwischen ebenfalls inert. Maßgeblich sind die tatsächlichen Komponenten-Antworten, nicht rein beschreibende Authoring-Tags.

Native Nachweise: einfache Capsule-Sweeps gegen alle sieben Baumvarianten treffen deren Stammhüllen. Beim echten Faktor 3-Anlauf stoppt die Spielfigur ohne Kapselüberlappung. Die vorhandene Kamerakollision verkürzt den Arm am Stamm auf 270,73 cm und stellt anschließend 350 cm wieder her. Das ist eine Stichprobe plus längerer regionaler Fußlauf, keine exhaustive Prüfung jedes einzelnen Baums.

## Gras, Waldboden und Ufer

- Bestehende 18.167 Grasinstanzen verwenden nun die vorhandenen `SM_EQ3_GrassShort`, `SM_EQ3_GrassMeadow`, `SM_EQ3_GrassWoodland` und `M_EQ3_Grass` aus VisualV2EnvironmentV3 statt einfacher alter Grasdarstellungen. Keine zusätzlichen Grasschatten oder Kollisionen.
- 21.613 zusätzliche, unregelmäßig gruppierte Boden-Grasinstanzen:10.831Short,7.049Meadow,3.733Woodland. Tatsächliche Bodenprojektion; Abstände zu Wegen, Gebäuden, Interaktionspunkten und Fluss. HISM und begrenzte Sichtentfernung50–65m statt einzelner Tick-Actors.
- Vorhandene 6.394 Wiesenkräuter bleiben erhalten. Ergänzt:189 Farne, 187 Wurzelgruppen, 189 Moosgruppen und 154 Ufer-Schilfgruppen aus vorhandenem Assetbestand. Bodenpflanzen kollisionsfrei, ohne zusätzliche feine Schatten.
- Map-eigene `M_WVU_Grass`/`M_WVU_PathBlend` behalten ursprüngliche gemalte Gras-/Erdtexturen und die regionale Wegmaske. Eine technische, weich geglättete Waldabdeckungsmaske aus den bestehenden Baumstandorten mischt zurückhaltenden, entsättigten Waldboden ein; Ufernähe erhält feuchtere Erde. Keine neuen Terrainformen oder geänderten Wegverläufe.
- Die 503 vorhandenen felsigen Konturgruppen behalten XY-Standorte, Mesh und Kollision. Die visuelle Z-Einbettung wurde über fünf Gelände-Stützproben angepasst, damit Gruppen an steileren Ufern weniger schweben. Die alten kantigen Felsformen bleiben sichtbar.

Neue Assets ausschließlich unter `/Game/Environment/WestlandVisualUpgradeV1`: drei Oberflächenmaterialien, eine technische 1024×820-Abdeckungstextur und elf notwendige lokale Instancing-Material-/MIC-Ableitungen. Technische Importquelle: `Art/World/WestlandVisualUpgradeV1/ForestCoverage.png`. Keine neue fotorealistische Texturserie oder Änderung gemeinsamer Originalmaterialien. Lokale Ableitungen setzen die benötigte InstancedStaticMesh-Nutzung, statt die Originalmaterialien anderer Maps umzuschreiben.

## Flusswasser

`M_WVU_River` ersetzt ausschließlich die vorhandene Materialbindung an `WR_WindingRiver`. `SM_WR_River`, Transformation, Wasserhöhe, Verlauf, Bettgeometrie, bestehende Brücken, Flussbarrieren und drei Wasserlebensräume bleiben erhalten.

Die Oberfläche ist nun beleuchtet/transluzent mit zurückhaltendem blaugrünem Tiefenverlauf, sichtbarem Untergrund im flachen Rand, animierter Längsströmung, zwei dezenten Normalwellen, wenigen Glanzlichtern und angepasster Rauheit 0,28 / Specular 0,32. Screen-Space-Reflexionsfähigkeit der vorhandenen Teicharchitektur bleibt erhalten; keine neue Planar-Reflection oder globale Reflexionsumstellung. Optische Alpha-Werte ungefähr 0,38 am Rand bis 0,82 in der Mitte, zusätzlicher 50 cm-SceneDepth/PixelDepth-Uferfade. Keine Wasserverformung, neue Physik oder künstliche Vergrößerung des Flusses.

Die Grundfarbe und Normalen sind auf die tatsächlichen Fluss-UVs und regionale Fließrichtung angepasst. Nasse Ufererde, vorhandene Steine und zusätzliche Schilfgruppen vermitteln den Übergang. Transparenz lässt stellenweise vorhandene ufernahe Pflanzen durchscheinen; weder ein vollständiges Unterwassersystem noch eine Überarbeitung des gesamten Flussbetts ist enthalten.

Der bestehende flache Fluss bleibt für wilden Garados zu schmal und mit ungefähr 80 cm zu flach. Keine Garados-Platzierung, Modellverkleinerung oder Änderung seiner V4-Daten. Natürlicher Karpador-Betrieb und die Spielerbarriere wurden im echten separaten Prozess geprüft.

## Testgeschwindigkeit benutzen

Im normalen PIE oder Development-Spiel mit aktiver Spielfigur die Konsole öffnen:

```text
pm.Speed Status
pm.Speed 3
pm.Speed 2
pm.Speed 1
```

| Faktor | Gehen | Sprint |
|---|---:|---:|
|1|210cm/s|315cm/s|
|2|420cm/s|630cm/s|
|3|630cm/s|945cm/s|

`PokeMonsterPlayerTestSpeed.cpp` ergänzt die bestehende Playerbewegung. Der Quotient neuer/alter Faktor skaliert die vorhandenen Bewegungsgrenzen und deren bestehende Sprint-Walk-Basis genau einmal. `RefreshSprint` bleibt für Sprint zuständig; kein zweiter Sprintzustand. Wiederholung desselben Faktors vervielfacht nichts. Auch eine abweichend konfigurierte normale Geschwindigkeit wird beim Zurücksetzen exakt wiederhergestellt. Ungültige/NaN-Werte werden abgewiesen.

Nur der aktuelle Player wird verändert. Keine Zeitdilatation, keine NPC-/Pokémon-/Kampf-/Kamera-Beschleunigung, keine SaveGame-Felder. Faktor ist kein UPROPERTY-/persistentes Feld. Neuer Pawn bzw. vollständiger Neustart beginnt bei1; Laden in denselben laufenden Pawn darf den aktuellen Sitzungsfaktor behalten. `pm.Speed 1` stellt ihn jederzeit zurück. Konsole und Änderung sind in Shipping deaktiviert; eine eigene Shipping-Paketierung war nicht Teil dieser Editor-Prüfung.

WASD/Shift und vorhandene linke Stickaktion/L3 bleiben unverändert. Im nativen Test wurden alle zwölf Kombinationen aus Software-WASD/Stickaktion, Faktoren1/2/3 und Gehen/Sprinten mit tatsächlicher Kapselgeschwindigkeit nachgewiesen. **Kein echter angeschlossener Controller wurde als getestet ausgegeben.**

## Technische Prüfungen

Alle Nachweise unter `Saved/ProjectRefinement/WestlandVisualUpgradeV1/`, große Medien ausschließlich lokal.

| Prüfung | Tatsächliches Ergebnis |
|---|---|
|Editor-Build `BuildFinalCollision`|Exit0,9,81s nach finalem Kollisions-/Teststand|
|Vollständige Automation `AutomationFinal`|**325/325**,0 Warnungstests,0 Fehler,0 Skips;58,24s|
|Strenger QA-Wrapper|Engine0, **Wrapper Exit0**; bestehender Automation-/Report-Vertrag mit isoliertem UserDir, keine abgesenkten Schwellen|
|Zwölf vorhandene Map Checks|jeweils0 Fehler/0 Warnungen; `MapCheckParsed.json`|
|`PIERegressionFinal`|Bestanden,58,70s: ursprüngliche vier NPC-Interaktionen, echte Wildbegegnung/Attacke/AP/Fang, Heilung/Checkpoint, Innenraum, Menü-Save/Load, drei Funde, Team/Begleiter/EP, Tageszeiten|
|`NativeSpeed03`|Bestanden,44,10s; zwölf gemessene Geschwindigkeitsfälle, Stamm-/Kamerakollision, normaler Weltuhrfortschritt|
|`NativeTour02`|Bestanden, **1.388,01m** echte Enhanced-Input-Bewegung in213,53s Wandzeit; keine Teleports, Faktor 3/Software-Shift; ursprünglicher Dialog und Menü-Save enthalten|
|`NativeRestart02`|Bestanden,13,05s; neuer Prozess startet Westland, lädt eigenen Tour-Save exakt, echter Wechsel nach VisualV2 und normales Laden zurück nach Westland|
|`NativeWater03`|Bestanden,80,37s; sieben native Stammhüllensweeps, Flussbarriere bei Faktor 3,74 natürliche Karpador-Proben,0–26,25cm/s,Idle/Rest/Wander; höchstens6aktive Tiere|
|Acht QHD-Bildpaare|16echte2560×1440-Dateien geprüft, `MediaAudit.json`|

Baseline 323 plus zwei neue Automationstests: `PokeMonster.Player.TransientTestSpeed` und `PokeMonster.WestlandVisualUpgrade.SavedSheetReplacementAndCollision`. Sie prüfen unter anderem ungültige Faktoren, Sprintwechsel, fremde Pawns, neue Pawns, abweichende Grundgeschwindigkeit, gespeicherte3D-Ersetzungen, vorhandene Stammhüllen und unveränderte Flussmeshbindung. Keine Produktions-Kampf-/Save-/KI-Regeln zur Testvereinfachung geändert.

PIE-Regression verwendet gezielte diagnostische Standortwahl und ist **kein** Fußrundgang. Der getrennte native Tour02-Lauf ist dagegen ein zusammenhängender echter Fußlauf: Hof/Originaldialog/Menü, Dorf, Wiese, Waldruinen, Waldpfad, Wiese, Ufer. Maximal gemessene Geschwindigkeit945cm/s. Für den abschließenden regulären Menü-Save wird vorher Faktor 1 gesetzt. NativeRestart02 benutzt ausschließlich diesen eigenen Save, keinen kopierten Nutzerspielstand.

Verglichen werden beim Laden vollständige individuelle Pokémon-Daten einschließlich AP, Team, Inventar, Position/Blickrichtung, Weltzeit, Begleiter und bestehende Questanzeige. Im Heilhaus werden tatsächlicher Eingang/Ausgang, Heilung und regionaler Checkpoint geprüft. Alle drei Funde bleiben nach erneutem Laden eingesammelt. Der natürliche Kampf führt eine reguläre Attacke und einen Fang aus, aktualisiert das Team und gibt die Steuerung zurück.

Aktuelle Runtime-Proben:75%ScreenPercentage, Software-Lumen(`r.Lumen.HardwareRayTracing=0`), IFG(`r.Lumen.FinalGatherMethod=0`), TAAU1,VSM1,vier Richtungsstrahlen. Mittag75°, Debug85°und Rückkehr75° geprüft,06/12/19/22-Uhr-Proben. Uhr weiterhin120Echtminuten/Tag: im Geschwindigkeitslauf44,2273Spielweltsekunden zu530,7273Ingame-Sekunden, Faktor 12; kein `pm.Speed`-Einfluss. Kamera weiterhin−12°,350cm freier Abstand, tatsächliche freie Höhe ungefähr1,72m; Kollision darf Abstand vorübergehend verkürzen.

### Nicht als Erfolg gezählte Zwischenläufe und Warnungen

Der erste Build scheiterte an einer von mir verwendeten nicht verfügbaren NaN-Testfunktion; auf `std::numeric_limits` korrigiert und neu gebaut. Zwischenzeitliche Python-Authoring-Probleme mit geschützten Eigenschaften/nicht vorhandenen Hilfs-APIs sowie ein doppelter unverbundener Wasser-UV-Eingang wurden vor Abschluss korrigiert. Keine Standardmaterial-Fallbacks in den frischen finalen nativen Prüfläufen.

`NativeSpeed02` scheiterte an einer noch auf die alten25cm-Zylinder abgestimmten Prüfannahme. Der neue korrekte Test misst tatsächliche Kapselüberlappung statt eines falschen pauschalen Stammradius; `NativeSpeed03` besteht. `NativeWater02` sah in 40 s keinen Karpador und gilt ausdrücklich nicht als vollständig bestanden. Im verlängerten `NativeWater03` war die Kamera zunächst vom Wasser abgewandt, damit die unveränderte Offscreen-Spawnregel nicht durch die Beobachtung blockiert wird; anschließend wird der natürlich erschienene Fisch betrachtet.74 Proben, gültiger Lebensraum, keine KI-/Spawn-Overrides. Das belegt den finalen Wasserbetrieb, nicht rückwirkend einen vollständig bestandenen Water02 oder die alleinige Ursache seiner fehlenden Sichtung.

Der strenge Wrapper bewertet den bestehenden vollständigen Projekt-Testreport; er ersetzt keine Zusage, dass jede Rohlogzeile warnungsfrei ist. Vor der eigentlichen Automation meldet die installierte Engine 17-mal `LogAutomationTest: Error: Condition failed`; diese Meldungen sind keinem der 325 ausgeführten Tests zugeordnet (der Report enthält 0 Fehler). Ihre interne Ursache wurde in diesem visuellen Auftrag nicht behoben. Native `-game`-Starts der installierten Engine melden außerdem bestehende experimentelle Toolset-Python-Initialisierungsfehler zu `ToolsetDefinition`, `AgentSkill`, `PythonTestRunner` und Editor-Widgetregistrierung. Eigene Testskripte liefern trotzdem bestandene Ergebnisse und die Prozesse beenden regulär mit0. Keine Engine-/Plugin-Umschreibung, kein Verschweigen dieser Infrastrukturmeldungen.

Editor02 enthält beim Laden älterer Bibliotheksinhalte eine ursprüngliche `MI_WLA_LeafOak`-Instancing-Warnung sowie Audio-/Layout-/Scalability-/HTTP-Shutdown-Meldungen. Westlands neue Gruppen binden lokale kompatible Ableitungen; frische finale native Läufe enthalten keinen Material-Compile-/Default-Material-Fallback und keinen Fatal-/Assertion-Abbruch. Die extern bekannte iOS-Helfermeldung `idevice_id: Bad CPU type in executable` trat in den ausgewerteten finalen Logs nicht auf; sie wurde durch diesen Auftrag nicht repariert. Die Logs sind insgesamt nicht pauschal als warnungsfrei deklariert.

## Echte Vorher-/Nachher-Bilder

Gleiche sieben festgelegte Spielerpositionen und Blickrichtungen, 12:00 Uhr angehalten, unverändertes Profil C/High, 2560×1440 Ausgabe. Der numerische Kameraabgleich bestätigt sechs spielseitige Paare bis auf Gleitkommarundung exakt, einschließlich FOV, Rotation, Auflösung und Screen Percentage. Beim Motiv Flussufer verkürzt die neue echte Stammkollision den Arm: Kameraort um 54,65 cm versetzt bei identischer Figurposition und Blickrichtung. Dieses Paar ist deshalb ein vergleichbares Motiv, aber kein exakt identischer Kamerastand; keine Kollision wurde für das Bild ausgeschaltet. Kamera-Grundhöhe/-neigung/-abstand bleiben unverändert. Einzelwerte: `PairedCameraAudit.json`. Die achte Gesamtansicht ist eine tatsächliche Editor-Übersicht mit identischem Bildausschnitt vor/nachher, keine normale Third-Person-Ansicht. Bewegliche Pokémon, Flammen und Wasser sind nicht pixelidentisch eingefroren. Kamera-/Viewportdaten in den jeweiligen `Result.json`.

| Motiv | Vorher | Final nachher |
|---|---|---|
|Hobbit-Dorf|`BeforeFinal/Dorf.png`|`AfterFinalCollision/Dorf.png`|
|Waldrand|`BeforeFinal/Waldrand.png`|`AfterFinalCollision/Waldrand.png`|
|Dichter Wald|`BeforeFinal/DichterWald.png`|`AfterFinalCollision/DichterWald.png`|
|Waldweg|`BeforeFinal/Waldweg.png`|`AfterFinalCollision/Waldweg.png`|
|Flussoberfläche|`BeforeFinal/Flussoberflaeche.png`|`AfterFinalCollision/Flussoberflaeche.png`|
|Flussufer|`BeforeFinal/Flussufer.png`|`AfterFinalCollision/Flussufer.png`|
|Third Person mit Vegetation|`BeforeFinal/ThirdPersonVegetation.png`|`AfterFinalCollision/ThirdPersonVegetation.png`|
|Gesamtregion|`BeforeFinal/Gesamtansicht.png`|`AfterFinalCollision/Gesamtansicht.png`|

Alle Pfade in der Tabelle relativ zu `/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/WestlandVisualUpgradeV1/`. Zusätzliche echte Bilder aus PIERegressionFinal, NativeTour02, NativeRestart02 und NativeWater03 liegen im selben Nachweisordner. Keine künstlich generierten Vergleichsbilder, keine neue umfangreiche Rohbildfolge oder Videoaufnahme.

## Messgrenzen und verbleibende optische Einschränkungen

NativeTour02: 8.485 Frameintervallproben, 39,74 FPS im Mittel,24,70 ms Median, 26,97 ms Frame-p95. Enthält Software-Input, drei Screenshots und Menüabschnitte; Messung über Laufzeit-Callbacks, **kein kontrollierter GPU-Benchmark**. Der frühere längere Westland-Rundgang mit 27,79 FPS hatte andere Strecke/Dauer/Ansichten und darf nicht als gepaarter Vorherwert für eine behauptete Optimierung dienen. Keine gesonderte GPU-/Game-/Render-Thread-Reihe, kein allgemeiner stabiler 30 FPS-Nachweis und keine Performanceoptimierung durchgeführt.

Die alten einfachen Geländekulissen und kantigen Felsformen bleiben sichtbar. Bestehende Standortmuster, scharfe Hangformen und lokale Überschneidungen größerer Kronen sind durch reinen Assetaustausch nicht vollständig neu gestaltet. Einzelne durchscheinende Uferpflanzen und sichtbare Übergänge an vereinfachter Bettgeometrie bleiben mögliche optische Nacharbeit. Die Wasserfläche ist keine physikalische Flusssimulation; SSR ist blickabhängig. Kleinvegetation ist bewusst nicht blockierend und besitzt begrenzte Sichtweite. Keine neue Waldkamera, kein globales Material-/Licht-/Renderingprofil und keine vollständige temporale GI-Bildfreigabe.

Physischer Controller, Shipping-Paket und jeder einzelne Baum-/Ufermeter wurden nicht vollständig geprüft. Bestehende Garados-Land-/Kampf-/V4-Animationen wurden nicht verändert; ihre separaten historischen Nachweise bleiben gültig, es gab hier keinen neuen Garados-im-Fluss-Test.

## Projektschutz und Git-Sicherung

Ausgangsinventar `Baseline.json`:6.082 versionierte Dateien, 351 geschützte/unversionierte Dateien und 686 bereits vorhandene Save-Dateien. Hashvergleich `ProtectionFinal.json`: nur erwartete eigene Map-/Playerheader-/Entscheidungsdokument-Änderungen vor Abschlussdokumentation;351/351 geschützte und 686/686 bestehende Saves bytegleich. Die bereits beim Start lokal geänderte `Config/DefaultEngine.ini` ist gegen diesen lokalen Ausgangszustand bytegleich und wird nicht mitcommittet. VisualV2, Biom-Testmap, alle Originalmeshes/-animationen/-Blenderquellen, Fab-Inhalte und sonstige Maps unverändert. Nach Abschlussdokumentation folgt der abschließende begrenzte Hash-/Stage-Abgleich.

Die Original-Westlanddatei bleibt im Ausgangscommit und als nachgewiesenes lokales LFS-Objekt mit SHA256 `5544fee52cac11bda0d7d884347362bdc79303697d0de588024f4dcd4708a386`, 11.914.831 Bytes erhalten. Keine neue unnötige Sicherungskopie. Bestehende Vollbackup-Refs bleiben `03492bd96b4dba44692f675c19d5f11abfa86b4b`; kein Prune oder Umschreiben.

Geplant ist ausschließlich die Sicherung der geprüften Westland-Map, neuen lokalen Oberflächen/Importmaske, Spieler-Testgeschwindigkeit mit zwei Tests sowie der eigenen Autoren-/Prüfwerkzeuge und Dokumentation. Keine Saved-Kontrollmedien, bestehenden fremden unversionierten Dateien, lokalen Fab-Originale oder Nutzerkonfigurationen. Konkreter Abschlusscommit und bestätigter Remote-/LFS-Status werden nach regulärem Push im Abschlusschat genannt und unter `Saved/ProjectRefinement/WestlandVisualUpgradeV1/` verifiziert. Keine Budget-/Abrechnungseinstellung wird verändert. Nach der Sicherung keine weitere gestalterische Bearbeitung vor Harrys eigenem Test.
