# Westland Region – technische Integration V1

Stand 02.11.2026, Ausgangscommit `92042df0ec85bffaea8f7e909a53fb4294060b14`. Ausschließlich bestehendes Projekt `/Users/harry/Developer/PokeMonster`. Die tatsächlich vorhandene Zielmap heißt **`/Game/Maps/Dev_WestlandRegion`**, nicht `Dev_Westland_Region`. Keine zweite Map oder Umbenennung angelegt. VisualV2 bleibt erhalten.

## Originalstand und Sicherung

Das unveränderte Original ist bereits im Ausgangscommit versioniert. Ursprüngliche Westland-LFS-Datei: SHA256 `4b05a2819f24b6cc2152158f856d4e88af99057534f18744f7f53714264e3740`, 11.869.648 Bytes. Vor Bearbeitung wurden tatsächliche Mapdatei, Git-Pointer und Commit sowie 6.067 versionierte Dateien, 351 geschützte/unversionierte Dateien und 676 bestehende Save-Dateien erfasst. Nachweis lokal `Saved/ProjectRefinement/WestlandIntegrationV1/Baseline.json`. Keine unnötige Map-/Projektkopie oder neuer Backup-Ref; bestehendes Vollbackup und Buchenwald-Rücknahme bleiben erhalten.

## Differenzübersicht vor/nach Integration

Vorher: 3.087 gespeicherte Actors in Westland. Die Übersicht betrifft die gespeicherte Szene; transiente Wild-Pokémon, Begleiter, UI und Himmel werden separat zur Laufzeit erzeugt.

| System/Inhalt | VisualV2-Referenz | Westland vorher | Übernahme |
|---|---|---|---|
| Player, Enhanced Input, Third Person V3, Sprint | Aktueller gemeinsamer C++-Player/Controller | Gleicher GameMode; neue Kamera bereits automatisch wirksam | Keine Kopie und keine Kamera-/Eingabeänderung |
| Team, Inventar, Kampf/Fang, EP, Attacken/AP, Entwicklung, Save/Load | GameInstance-/gemeinsame Dienste | Dienste schon vorhanden, frische Development-Sitzung aber noch mit altem technischen Testteam | Leeres Development-Team verwendet denselben aktuellen bestehenden VisualV2-Teamaufbau; geladene Teams werden nicht ersetzt |
| NPC-Dialogquellen | Zwei Dialog-NPCs, Heiler und gesonderte Trainer-/Testrollen | Drei Regionsdialog-NPCs und ein Heilpunkt, nur Sprite-/Prototypdarstellungen | Genau vier Präsentationsactors an dieselben Quellen; keine zusätzlichen Dialog-/Heilinstanzen |
| Innenräume | Zwei Cutaway-Controller | Zwölf vorhandene Gebäude-/Innenraumcontroller | Alle zwölf erhalten, keine Möbel-/Gebäude-/Raumkopie |
| Wild-Pokémon | Natürliche kuratierte Population, Galerie-/Testquellen ruhend | Drei alte `DA_DevWild`-Quellen, keine HabitatZones | Originalquellen/Kennungen erhalten und bei natürlicher Population deaktiviert; 13 Land- und drei Wasserzonen |
| KI/Tagesrhythmen | Bestehende Roaming-/Aktivitäts-/Partner-/Rhythmuslogik | Kein aktueller natürlicher Zonenbetrieb | Dieselben Komponenten und Regeln, über die bestehenden Zonen aktiviert |
| Namensanzeige | Bestehende optionale Bildschirm-Namensebene | Explizite Mapgrenze schloss Westland aus | Exakt Westland zusätzlich freigeschaltet; Einstellung/UI unverändert |
| Weltuhr | Eine zentrale Uhr, 120 Echtminuten/Tag | Gemeinsame Uhr schon vorhanden | Unverändert, keine zweite Uhr |
| Tageszyklus | Bestehendes Sun-/Fill-/Sky-Subsystem | Ein altes Sonnenlicht, SkyLight, statischer Tageszustand | Vorhandene Sonne getaggt, genau ein fehlendes schattenloses Fülllicht ergänzt; derselbe Controller |
| Profil C | Software-Lumen/IFG, High, 75 %, TAAU, vier VSM-Strahlen | Globaler Profildienst vorhanden; TAA-Blendable und Vier-Strahlen-Mapgrenze fehlten | Dieselben Werte und native AA-Wahl übernommen, keine neue Renderingverwaltung/Optimierung |
| Gegenstandsfunde | Zwölf technische VisualV2-Funde | Keine WorldItem-Actors | Drei gewöhnliche vorhandene Items mit eigenständigen Westland-Kennungen |
| Quest-/Fortschrittsdienste | Bestehende gemeinsame Dienste und Mini-Slice-Inhalte | Dienste verfügbar, drei eigene Wegbeschreibungsdialoge, keine eigene Regionsquestkette | Dienste beibehalten/geprüft; keine fremde Testquest oder Liora als neue Westland-Geschichte platziert |
| Modell-/NPC-Testflächen | Gesonderte Entwicklungsbereiche | Keine solche Galerie in der Region | Nicht übertragen |

Vollständige ursprüngliche Actor-/Klasseninventare und ausgewählte Komponenten unter `Dev_TestMap_VisualV2_Before.json`, `Dev_WestlandRegion_Before.json`, `DetailsBefore.json`. Landschafts-/Dekorationsvergleich: **3.030 ursprüngliche Actors** einschließlich aller Instanztransformationen, Meshes, Materialien, Geometriezuordnungen und Transformationen exakt gleich (`EnvironmentBefore.json`/`EnvironmentAfter.json`). Vorhandene Wege, Terrain, Häuser, Brücken, Wasser und Kulissen bleiben erhalten.

## Notwendige technische Anschlüsse

`APokeMonsterGameMode::IsIntegratedRegion` begrenzt die Übernahme exakt auf VisualV2 und die tatsächliche Westland-Map einschließlich PIE-Präfixen. Keine Freischaltung von Biom-Testmap, WestlandVillage, Assetbibliothek oder beliebigen ähnlich benannten Maps. Bestehende globale Dienste bleiben zuständig.

Die 80 Terrain-Instanzen und der bereits kollidierende ausgelagerte Heilhausboden ignorierten im alten Art-Proof `Visibility`. Der aktuelle gemeinsame Pokémon-Bodenplaner konnte dort keinen gültigen Boden finden. Ausschließlich ihre komponenteneigene Antwort auf diesen Abfragekanal wird auf Block geändert. Pawn-Kollision, Topologie, Meshes und Laufwege bleiben erhalten. Vorhandene Flussbarrieren erhalten den bereits vorhandenen `BiomePlayerWaterBarrier`-Tag; die bestehende Habitat-BeginPlay-Logik übernimmt sie für Fische. Spielerbarrieren bleiben aktiv.

Die vorhandene Spawn-Abtastung berücksichtigt nun die tatsächliche Zonenrotation. Das ist für den diagonalen Westland-Fluss nötig; die ungedrehten VisualV2-Zonen behalten dieselbe Abtastung. Kein neuer KI-/Navigationscontroller.

Tageslicht: vorhandenes `SoftDaylight` bleibt die Sonne, bekommt die eindeutige `PokeMonsterSun`-Bindung und die etablierte weiche Sonnenquelle; `WR_SoftSkyFill` ergänzt die fehlende schattenlose gerichtete Aufhellung. Forward-Shading-Priorität unterscheidet Sonne und Fill eindeutig, damit Wasser/Transparenz keine mehrdeutige Hauptlichtwahl melden. Das vorhandene SkyLight und die regionalen Belichtungs-/Tonemappingwerte bleiben erhalten. Das bestehende Tageszyklus-Subsystem liest dieselbe Weltuhr; 75° bleibt Mittag, 85° Debugoption. Keine zweite Zeit-/Beleuchtungsarchitektur.

Profilwerte bleiben unverändert: QHD2560×1440, High, 75 % Screen Percentage, TAAU, Software-Lumen/IFG, VSM vier Strahlen. Der bestehende native AA-Blendable wird einmal dem vorhandenen regionalen Außen-Postprocess zugeordnet; alle übrigen Postprocess-Felder bleiben gleich. Nur die bisherige Mapgrenze des bestehenden Vier-Strahlen-Scopes wird erweitert. Kein Lumen-/Schatten-/Materialexperiment und keine Performanceoptimierung. `pm.Graphics C`, `100`, `HardwareSPG` bleiben erhalten.

## NPC-Zuordnung

| Bestehende Quelle/Rolle | Vorhandenes Bibliotheksprofil | Sichtbare Referenzhöhe | Integration |
|---|---|---:|---|
| `WR_NPC_0` – Wanderer | Ranger | 1,80 m | Menschlicher Reisender, bestehendes Idle/Talk/Greet und Bibliotheksrig |
| `WR_NPC_1` – Dorfbewohner | HobbitBase | 1,40 m | Vorhandene Hobbitquelle, Größenbereich1,20–1,45m |
| `WR_NPC_2` – Archivarin | SilverLady | 1,90 m | Vorhandenes weibliches Fantasy-Modell in elfischer Modellgröße; keine männliche Ersatzfigur |
| `HouseHealer` – Hüterin der Ruhestätte | SilverLady | 1,90 m | Vorhandene Heilerinnenpräsentation, bestehender Heil-/Checkpoint-Actor |

Modelle/Materialien/Animationen und Originaldateien unverändert. Die beiden Frauen verwenden dieselbe vorhandene Bibliothekspräsentation; das ist bewusst Asset-Wiederverwendung, keine neue endgültige Volks-/Storyzuordnung. Für größere optische Individualität fehlen weitere geeignete weibliche Hobbit-/Archivarin-/Heilerinnenmodelle. Es wird kein fehlendes Modell durch einen neu erzeugten oder stilfremden Ersatz kaschiert.

XY-Standorte, Dialog-Assets, Texte, DisplayNames, Services und Checkpoint-ID erhalten. Die Kapselhöhen folgen den dargestellten Körperhöhen, die Fußpunkte dem vorhandenen Boden; nur die benötigte vertikale Platzierung wird angepasst. Präsentation hat keine zweite Kollision. Die Heilerin verwendet den tatsächlichen vorhandenen Westland-Innenlichtkanal0; die VisualV2-spezifische schattenlose Kanal1-Annahme wird nicht blind übernommen.

Die Quellen bleiben standortgebunden. Vorhandene Stand-/Gesprächs-/Begrüßungsdarstellung geprüft; keine neue produktive NPC-Wander-KI eingeführt. SilverLady bleibt mit ihrem bestehenden eingeschränkten Rig bewusst stationär, ohne behauptetes Gehen/Laufen. Keine Reparatur/Neugestaltung bestehender Rigs in diesem Integrationsauftrag.

## Lebensräume und Pokémon

Quellenkonfiguration: `Tools/WestlandIntegrationV1/Layout.json`; die daraus gespeicherten HabitatZone-Actors benutzen unverändert `Config/DefaultPokeMonsterHabitats.ini`. Keine zweite Artenliste, keine neuen Spezies oder erfundenen Attacken-/Entwicklungsdaten. Globale Grenzen bleiben **14 aktive Wild-Pokémon**, höchstens sechs gleichzeitige Arten, bestehende Mindestabstände, Residence-/Sicht-/Distanz-/Tagesregeln.

Landzonen: Hofwiese, Dorfrand, Obstgarten, Nordwiese, Heilhauslichtung, Steinkreis, Wildwiesen, Waldrand, Waldruinen, Waldlichtung, Südwald, Mühlenwiese und Flussufer. Typen Meadow/Village/Glade/Rock/Edge/Forest/Shore wählen die vorhandenen passenden Regeln: unter anderem Bisasam, Pikachu, Myrapla, Glumanda, Enton, Nebulak sowie die vorhandenen Insekten-/Flugarten. Nicht alle Arten gleichzeitig und keine Sammlung aller verfügbaren Modelle.

Drei begrenzte Flussabschnitte nutzen den existierenden Wasserstand; gemessene Bett-Tiefe jeweils etwa **80 cm**. Die vorhandene Karpador-Regel verlangt43 cm Tiefgang und passt grundsätzlich. Die konservativen Breiten-/Tiefen-/Boden-/Kontaktabfragen bleiben aktiv. Die einzelnen geraden Abschnitte sind keine vollständige Simulation des ganzen gewundenen Flusses.

**Kein wilder Garados in diesem Fluss:** unveränderte V4-Sicherheitsanforderung400 cm horizontaler Radius und180 cm Tiefe. Die gespeicherten Abschnitte sind dafür zu schmal und zu flach. Kein Teich erfunden, Terrain vertieft oder Modell verkleinert. Garados' V4-Assets und die aktuellen Pikachu-/Raichu-/übrigen Präsentationen bleiben globale verfügbare Speziesdarstellungen für geeignete Kontexte. Ein seriöser Garados-Wassertest in Westland ist mit der vorhandenen Geometrie nicht möglich; der bestandene VisualV2-V4-Nachweis bleibt erhalten.

## Gegenstände, Start und Mapwechsel

Drei nicht blockierende bestehende WorldItems: Hof-Fund zwei Pokébälle, Dorf-Fund ein bestehender Trank (`DA_TestHealingItem` ist dessen historischer Dateiname), Ufer-Fund ein Superball. Eigene stabile IDs `Pickup.Westland.IntegrationV1.<Fund>`; bestehende Inventar-/Weltflag-/Save-Transaktion, keine zweite Sammlungsspeicherung.

`EditorStartupMap` und `GameDefaultMap` zeigen jetzt auf **die bestehende** `Dev_WestlandRegion`. Kein vorhandenes separates Startmenü wurde ersetzt. VisualV2 kann weiterhin als vorhandene Map im Editor geöffnet werden. Engine-Konsole `open Dev_WestlandRegion` bleibt der normale vorhandene Mapwechsel, keine zusätzliche Gameplay-Verwaltung.

Alte Nutzerspielstände werden nicht umgeschrieben: normales Laden führt weiterhin zu ihrer gespeicherten Map/Position, gegebenenfalls VisualV2. Der neue Startwert bedeutet keine automatische Übertragung alter Positionskoordinaten nach Westland. Bei normalem Mapwechsel bleiben GameInstance-Team/Inventar/Fortschritt erhalten. Eine frische leere Development-Sitzung nutzt das bisherige aktuelle VisualV2-Team; das ist keine neue endgültige Starter-/Balancingentscheidung oder geprüfte Shipping-Startkampagne.

## Prüfungen

- **Build01:** Exit6, eigene Include-Reihenfolge und Test-TObjectPtr-Aufruf korrigiert. **Build02:** Exit0,8,09s; **BuildFinal:** Exit0,8,51s nach den letzten Quellkommentaren. Bestehende installierte Engine5.8.4/CL58902052; keine Engineinstallation/-änderung. Spätere reine Kommentare/QA- und Datenkontrollen sind getrennt vermerkt.
- **Automation01:**323/323 erfolgreich, Engine0/strenger Wrapper0,45,61s. **AutomationFinal:**323/323 erfolgreich,0 Warnungstests/Fehler/Skips, Engine0 und **strenger QA-Wrapper Exit0**,32,89s. Baseline321 plus zwei neue echte Regionstests für gespeicherte Bindungen, Terrainabfrage, eindeutige Zonen/Quellen, Kartenabgrenzung und vorhandene gültige Entwicklungs-Startparty. Keine Testschwellen heruntergesetzt.
- **Zwölf Map Checks:** jeweils0 Fehler/0 Warnungen, nach finalen Mapkorrekturen; `MapCheckParsed.json` und begrenzte `WESTLAND_INTEGRATION_V1_MAPCHECK_BEGIN/END`-Abschnitte im Editor02-Log. Keine geprüfte Referenzmap gespeichert.
- **PIE07:** vollständiger isolierter Westland-Lauf bestanden,50,77s. Vier bestehende NPC-Interaktionen inklusive Wiederholung/Originaldialogen, echte natürliche Wildbegegnung mit regulärer ClassicBattle-Attacke und Fang, Heilhaus hinein/heraus durch die vorhandene Tür, Heilung, Menü-Save/Load im Innenraum, individueller Team-/AP-/Inventar-/Positions-/Zeitvergleich, bestehende aktive Questanzeige nach Laden, Teamsortierung/Begleiter,06/12/19/22-Uhr-Lichtproben. Ausschließlich eigener expliziter PIE-Testslot. Gezielte Standortwechsel in diesem kurzen Lauf sind **kein Fußrundgang**.

- **PIE08 final:** bestanden,58,64s. Wiederholt die vollständige Interaktions-/Kampf-/Fang-/Heil-/Save-Prüfung; zusätzlich exakte regionale Checkpoint-ID/Map, B75/C85-Debugumschaltung mit Rückkehr zu B75 sowie alle drei regulären Fundtransaktionen. Nach Save/Load bleiben alle Funde eingesammelt und das Inventar exakt erhalten. Laufzeitwerte75%/Software-Lumen/IFG/TAAU/VSM4 nachgewiesen.
- **Natürlicher Wasserbetrieb:**35,62s bestanden,35 Karpador-Proben innerhalb gültiger Flusszonen, gemessene Geschwindigkeit0–26,25cm/s. Keine Spawn-/KI-/Animations-Overrides. Idle, Rest und Wander beobachtet; kein pauschaler Sichtnachweis sämtlicher Schlaf-/Sozial-/Nahrungssuchzustände aus diesem kurzen Lauf. Höchstens drei aktive Tiere in diesem Beobachtungsausschnitt; die globale Grenze14 bleibt separat geprüft.
- **Entwicklung/EP:**58,59s bestanden,18 inhaltliche Prüfungen. Bestehende Entwicklungs-Testparty ausschließlich im eigenen isolierten Slot, normale Level-/UI-/Save-Logik. Angebote korrekt ab16/36, Abbruch ohne Datenverlust, kein sofortiges Doppelangebot; späterer Levelaufstieg17/37 bietet erneut an und entwickelt vollständig bis zur farbigen Enthüllung zu Glutexo/Glurak. Individuelle Identität, Erfahrung, Attackenrepertoire, verbrauchte AP, Status und konsistente KP bleiben erhalten. Separat vorhandene Glurak-Reserve unverändert; Begleiter wechselt korrekt. Eigene entwickelte Individuen nach Save/Load exakt wiederhergestellt.
- **Separater vollständiger Fußrundgang NativeTour01:**bestanden,3.381,65m normale Enhanced-Input-Bewegung in1.209,32s Wandzeit. Kein Testteleport und kein Geschwindigkeits-Override; Sprint per Software-Shift, maximal315cm/s. Dorf, Wiesen, Flussufer, Stein-/Holzbrücke, Mühle, Spielerhof, Gasthausfront, Heilhausinnenraum, Steinkreis, Waldruinen und Regionsausgang angelaufen. Genau zwei große Positionsversätze durch die bestehenden Heilhaus-Ein-/Ausgänge. Originaldialog, Menü und eigener regulärer Save enthalten. Prozess normal mit0 beendet.
- **Frischer Neustart NativeRestart01:**bestanden,13,42s Prüflauf. Ohne Mapargument startet die konfigurierte Westland-Map; eigener echter Rundgang-Save stellt Position/Blickrichtung, vollständige Individuen/AP, Weltzeit und Begleiter wieder her. Echter OpenLevel-Wechsel nach VisualV2 und normales Laden zurück nach Westland erhalten Rendering, Team und Uhr. Kein Nutzersave verwendet/kopiert. Prozess normal mit0 beendet.
- **NativeViews01:**acht ruhige echte QHD-Ansichten der drei Außen-NPCs, Spielerhaus, Gasthaus, Heilhaus, Steinkreis und Waldruinen,24,38s bestanden. Nur diagnostische Standortwahl; kein zusätzlicher Fußlauf. Unveränderte Kamera, Prozessexit0.

Aus33604 Frameproben des NativeTour01 ergeben sich27,79FPS im Mittel,36,63ms Median und50,12ms Frame-p95. Der Lauf enthält13 Screenshot-Aufnahmen, Menüs und Innenraumübergänge und ist **kein isolierter GPU-Benchmark**. Keine separate GPU-/Game-/Render-Thread-Messreihe vorgenommen, keine stabilen30FPS behauptet. Keine Performance- oder Grafikqualitätsänderung durchgeführt.

 Frühere nicht vollständig bestandene QA-Aufbauten werden nicht als Gesamterfolg gezählt: erste Ausrichtung nach Test-Teleport war nicht die normale Interaktionsrichtung, eine nicht vorhandene Python-Vektormethode, ein bereits besiegter Zielactor, der direkte Weg durch den Tresen sowie geschützte Quest-Reflexionsfelder. Korrigiert wurden die Prüfhelfer, nicht Reichweite, Kollision, Gegner-/Fangregel oder Datenzugriffsschutz. Der freie vorhandene Weg und die bestehende öffentliche Questanzeige werden verwendet.

## Nachweise und Grenzen

Alle großen Kontrollmedien bleiben lokal unter `Saved/ProjectRefinement/WestlandIntegrationV1/`. `Before/` zeigt die ursprünglichen NPC-Sprites. `PIE08/` enthält die finalen tatsächlichen NPC-/Kampf-/Heilhaus-/Team- und Tageszeitaufnahmen. `Shot SHOWUI` im eingebetteten Editor erfasst das ganze2940×1696-Editorfenster; diese Bilder werden **nicht** als reine2560×1440-Gameframes ausgegeben. Die gewöhnlichen Spielviewport-Shots sind QHD; `NativeTour01/` enthält13 echte2560×1440-Spielbilder und `NativeViews01/` acht zusätzliche2560×1440-Ansichten. Der Dateipräfix `PIE_` einiger Rundgangsbilder ist ein historischer Werkzeugname; diese Bilder stammen tatsächlich aus dem separaten Development-Spielprozess. `NativeRestart01/` enthält die Neustart-/Mapwechselbilder.

Ausgewählte tatsächliche Aufnahmen (lokal, keine Git-Medien):

| Motiv | Datei unter `Saved/ProjectRefinement/WestlandIntegrationV1/` |
|---|---|
| Wanderer vorher / nachher | `Before/` / `NativeViews01/WR_NPC_0.png` |
| Hobbit-Dorfbewohner | `NativeViews01/WR_NPC_1.png` |
| Archivarin am Steinkreis | `NativeViews01/WR_NPC_2.png` |
| Heilhaus außen / innen | `NativeViews01/HouseCutaway.png` / `NativeTour01/PIE_66_Heilhaus_Innen.png` |
| Heilerin und Originaldialog | `PIE08/Heilerin_Dialog.png` (Editorfenster-SHOWUI) |
| Dorf/Gasthaus | `NativeViews01/WR_Gasthaus_Cutaway.png` |
| Spielerhof | `NativeViews01/WR_Spielerhaus_Cutaway.png` |
| Waldruinen | `NativeViews01/Waldruinen.png` |
| Natürlicher Karpador | `HabitatObservation01/Flussufer.png` |
| Vollständige Entwicklungen | `PIE_Progression01/Westland_Glutexo_Enthuellung.png`, `Westland_Glurak_Enthuellung.png` |
| Neustart/Maprückkehr | `NativeRestart01/Westland_Neustart.png`, `Westland_Nach_Kartenwechsel.png` |

Keine Videoaufnahme oder künstlich erzeugten Nachweise; verlangte Screenshots sind echte Unreal-Aufnahmen. Sichtprüfung zeigt weiterhin die ursprünglichen Vegetationskarten-/Kulissenkanten und teilweise alten Höhendarstellungen. Sie wurden nicht als Integrationsneuerung kaschiert oder eigenmächtig umgebaut.

Offene Spielinhalte: eigene Westland-Questkette, endgültige Starter-/Release-Startlogik und die spätere Zielregion am Regionsausgang sind nicht vorhanden und wurden nicht durch VisualV2-Testinhalte ersetzt. Gemeinsame Quest-/Save-/Mapwechseltechnik ist davon getrennt. Vorhandene illustrierte Vegetationskarten und ältere Gebäudekulissen behalten ihre Third-Person-/Rückseiten-/Nahsichtgrenzen; keine Landschaftsneugestaltung. Zwei NPCs teilen ein Modell, stationäre Robenfiguren erhalten keine erfundenen Laufanimationen. Keine endgültige künstlerische Freigabe behauptet. Physischer Controllerlauf nur bei tatsächlich angeschlossener/geprüfter Hardware; hier werden Softwareeingaben ausdrücklich getrennt ausgewiesen.

**Logbilanz:**AutomationFinal/Editor03 enthalten jeweils17 bestehende Startup-`Condition failed`-Zeilen; der Editor meldet außerdem die vorhandene `LeafOak`-Materialnutzung. Die nativen Tour-/Neustartprozesse enthalten jeweils58 Python-Fehlerzeilen aus sieben Engine-Plugin-Startup-Tracebacks (`Toolsets`/`ToolsetRegistry`, fehlende Game-Python-Typen `ToolsetDefinition`, `AgentSkill`, `PythonTestRunner`). Diese Zeilen stammen nicht aus den bestandenen Westland-Prüfskripten. Die Herkunft wurde anhand der vollständigen Tracebacks geprüft; Engine/Plugins werden nicht geändert. Keine Fatal-/Crash-Zeile und keine `idevice_id: Bad CPU type`-Meldung in den ausgewerteten finalen Logs. Das ist keine Behauptung, der externe iOS-Helfer sei generell repariert. Der lokale vorhandene `r.PrecomputedVisibilityWarning=True`-Wert wird nicht zur Schönung von Bildern/Logs geändert. Ein Map-Check-Ergebnis und ein strenger Automation-Exit0 bedeuten keine globale Warnungsfreiheit sämtlicher Engine-Logs.

## Projektschutz und Git

Abschließender Hashvergleich (`ProtectionCheck_Final.json`):alle351 geschützten/unversionierten Dateien und676 zuvor vorhandenen Save-Dateien unverändert und vollständig. Alle6.067 ursprünglichen versionierten Pfade noch vorhanden; ausschließlich die15 erwarteten bestehenden Auftragsdateien einschließlich der bereits lokal geänderten Engine-Konfiguration weichen ab. VisualV2, andere Maps, Modelle/Animationen einschließlich GaradosV4 und lokale Fab-Originale unverändert. Alle3.030 ursprünglichen Umgebungsactors exakt gleich; finale gespeicherte Map3.111Actors statt3.087, alle ursprünglichen Actor-Namen vorhanden. Genau24 neueActors:vier Präsentationen,16Zonen,drei Funde,ein Fill.

Die beiden Vollbackup-Refs zeigen unverändert auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`; das ursprüngliche Westland-LFS-Objekt ist zusätzlich per SHA256 im bestehenden lokalen LFS-Speicher nachgewiesen. Keine neue Archivkopie erzeugt. Die vier schon vor Auftragsbeginn vorhandenen lokalen Konfigurationszeilen bleiben unverändert und werden nicht mitgestaged; nur die beiden autorisierten Startmap-Zeilen werden aus dieser Datei versioniert.

Git-Sicherung:gezielter eigener Integrationscommit auf `main`, normaler `git push origin main`; Commit-ID und tatsächlich abgeschlossene Remote-/LFS-Verifikation werden im Abschlusschat und lokal `Saved/ProjectRefinement/WestlandIntegrationV1/GitVerification.json` festgehalten. Der Commit ist über `git log -1 -- Docs/WESTLAND_REGION_INTEGRATION_V1.md` eindeutig abrufbar. Keine vorweggenommene Push-Erfolgsbehauptung im Prüfbericht. Nur eigene notwendige Map-/Quell-/Werkzeug-/Dokumentationsänderungen werden gezielt versioniert. Bestehende lokale Konfigurationszeilen und unversionierte Nutzerdateien bleiben außerhalb des Commits. Keine Kontrollmedien, Fab-/Quixel-Originale oder Spielstände hochladen; kein Force-Push, History-Rewrite oder LFS-Prune.

Nach technischer Prüfung und Sicherung keine weitere Bearbeitung bis zu Harrys eigenem Westland-Spieltest.
