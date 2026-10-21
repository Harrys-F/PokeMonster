# Wilde Pokémon und Begegnungen V2 – Prüfbericht

Stand: 21.10.2026. Projekt ausschließlich `/Users/harry/Developer/PokeMonster`, Branch `main`. Ausgangs-HEAD `305976e4a54134d12ca34ad3b62ec1f9db6abdcd`, direkt mit `origin/main` abgeglichen. AGENTS und relevante Projekt-/KI-Dokumentation gelesen. Keine zusätzliche Map, Projektkopie, Worktree oder neue Kreatur.

## Ergebnis

Die korrigierte Nutzerregel ist im vorhandenen Wild-Actor, Verhaltensprofil, Interactable-Vertrag, Enhanced Input und EncounterSubsystem umgesetzt. ClassicBattle-Kamera, Kampfoberfläche und Kampflogik bleiben unverändert. WorldBattle erhält keine normale KO-Flucht. Technische Abnahme bestanden; physischer Switch-Pro-Test bleibt offen.

| Verhalten | Automatik bei Berührung | Herausforderung |
|---|---|---|
| Territorial / Aggressiv | ausschließlich tatsächlicher Player-Kapselkontakt | standardmäßig kein Ersatz für Kontakt |
| Ruhig / Neugierig | nein | vorhandene gemeinsame Interaktionsaktion |
| Scheu | nein, weicht weiterhin aus | bei gültiger Reichweite und Ausrichtung |
| Begleiter | nie | kein Begegnungsziel |

`Behavior.Initiation` bietet ByTemperament, Contact, Challenge und Disabled. Artspezifische Vorgabe und vorhandener Begegnungs-Override bleiben getrennt konfigurierbar. Aggressive ist am Enum angehängt, bestehende Werte bleiben erhalten. Der alte `EncounterRadius` ist kein Distanztrigger mehr. Sichtkontakt und Warnzeit lösen keine Kämpfe aus. Die bisherige Nahbereichsregel ist in den Entscheidungen als ersetzt markiert.

## Änderungen

- Kontakt: tatsächliche vertikale Kapselgeometrie beider Figuren, höchstens 2 cm Bewegungstoleranz. Die bisherige größere Sensorsphäre reicht nicht zur Auslösung. Kontakt wird auch beim laufenden Player geprüft. Laufender Kampf, Eingabesperre, Niederlagenrückkehr und Cooldown sperren Auslösungen. Territorial erfordert zusätzlich weiterhin Verlassen des Reaktionsbereichs; nach Ende ist Kontakttrennung nötig.
- Interaktion: derselbe bestehende Vertrag und dieselbe Aktion. Auswahl nach Entfernung/Blickrichtung, gültiger Reichweite/Höhe und freier Sichtlinie. HUD mit Artname; kleiner, nicht schattenwerfender Zielpfeil über dem ausgewählten Wild-Pokémon. Keine feste neue Controller-Taste: optionale Gamepad-Zuordnung derselben Aktion; E/Enter bleiben erhalten. Softwarezuordnung und tatsächliche Enhanced-Input-Auslösung geprüft.
- Sieg: bestehende Faint-/Kampfpräsentation und XP-Abrechnung, kurze vorhandene Hit-Reaktion in der Oberwelt (0,9 s), dann eigener Fluchtzustand derselben Bewegungskomponente. **Kein neuer Aufstehclip:** der vorhandene Hit→Idle-/Run-Übergang wird verwendet. Keine Änderung an Originalanimationen, Meshes oder Größen.
- Wegsuche: bestehende A*-, Boden-, Wasser-, Gebäude- und Kollisionsprüfung; nur KO-Flucht darf das normale Habitat verlassen. Begrenzte Etappen und höchstens 60 m Abstand vom Habitatursprung. Kollisionslose Baumstämme und größere Felsen erhalten konservative lokale Hinderniskerne, keine neue Welt-/Spielerkollision.
- Entfernung: vollständige projizierte Visual-Boundingbox außerhalb des echten Player-Viewports plus 96 Pixel Rand, mindestens 0,4 s stabil und mindestens 1,5 s Flucht. Kronenverdeckung allein reicht nicht. Abgeschlossene Source-Actors bleiben für Save-Restore unsichtbar, ohne Kollision/Actor-/Mesh-Tick erhalten. Kein unmittelbares Wiederauffüllen.
- Unerreichbarer Weg: sichtbar und nicht interaktiv warten, alle 1,5 s erneut planen; kein sichtbarer Teleport und kein Timeout-Ausblenden. Der geschlossene Hindernisring ist als echte Kollisionswelt in Automation geprüft.
- Fang: vorhandener Team-/Reserveübergang und sofortige Entfernung ohne Flucht. Spielerflucht: Habitat bleibt mit Wiederholungssperre erhalten. Spielerniederlage: bestehende Heilpunktrückkehr und Autosave. Keine neue Saveversion oder Spezies-ID.
- Snapshot-Rückkehr: Nach-Sieg-Laden lässt den Actor abgeschlossen. Ausdrückliches Laden eines Vor-Sieg-Snapshots reaktiviert ihn am ursprünglichen Map-Spawn und initialisiert das Habitat neu. Diese explizite Wiederherstellung ist von normaler teleportfreier Flucht getrennt.

Kernbereiche: `PokeMonsterCreatureBehavior`, `PokeMonsterCreatureRoamingComponent`, `PokeMonsterVisibleWildCreatureActor`, bestehende Player-Interaktion/HUD sowie mitgeführter PresentationMode im vorhandenen Encounter-EndData. Prüfwerkzeuge und Einstellungen: `Tools/WildEncountersV2/README.md`.

## Kleine Gruppe und Map-Schutz

Nur am vorhandenen Actor `Dev_Bisasam_Wild_01` in VisualV2 wurde GroupSize von 1 auf 3 gesetzt. Mitglieder heißen `Dev_Bisasam_Wild_01_Group_1/2`; eigene Seeds, getrennte Ziele/Pausen und Idle-Phasen. Kein gemeinsamer Kampf. Laufkadenz bleibt geschwindigkeitsabhängig. Alle ursprünglichen drei Habitat-/Spezies-IDs und Größen 60/50/70 cm bleiben erhalten. Zur Laufzeit sind damit fünf Wildakteure und höchstens ein Begleiter möglich.

Die Map speichert keine zusätzlichen permanenten Gruppen-Actors. Die Mitglieder entstehen nur aus dieser ausdrücklichen Konfiguration; kein unbegrenzter Respawner. Im Gruppen-Nachweis wurde ein dokumentierter ruhiger Laufzeit-Override geprüft; das bestehende neugierige Bisasam-Artprofil wurde nicht umgeschrieben.

Ein anfänglicher Vergleich scheiterte an Python-Speicheradressen von Transform-Repräsentationen. Automatische Sicherheitsprüfung blockierte daraufhin das Speichern einer bereits schmutzigen Map. **Kein Save All oder Verwerfen:** vollständiger T3D-Abgleich des offenen Zustands mit der getrennt gelesenen gespeicherten Map. Einzige Projektänderung war GroupSize=3 am genannten Actor. Unterschiede zweier nach Enginequellen transienter Debugakteure und eines erzeugten Engine-Manager-Labels wurden explizit getrennt. Erst nach erneutem vollständigem Gleichheitsnachweis wurde genau diese Map gespeichert. Belege: `Saved/WildEncountersV2/GroupSavePreflight.json`, `GroupConfiguration.json` und T3D-Dateien.

## Reale PIE-Ergebnisse

| Prüfung | Ergebnis / lokaler Nachweis |
|---|---|
| Territorial: Warnung/Nähe ohne Kontakt | kein Kampf; tatsächlicher Kontakt startet genau einen (`FinalGlum01`) |
| Aggressiv: Kontakt | genau ein Kampf; Quelle für die isolierte Kontaktprüfung zunächst pausiert (`FinalAggressive01`) |
| Ruhig: Berührung / Interaktion | Berührung startet nichts; gemeinsame Aktion startet den Kampf (`FinalCalm01`) |
| Neugierig / Scheu | Kontakt startet nichts; gerichtete Herausforderung funktioniert (`FinalBisasam01`, `FinalSchiggy01`) |
| Mehrere gültige Ziele | zwei unterschiedliche Gruppenmitglieder nach Blickrichtung ausgewählt; nur das zweite kämpft (`GroupFinal01`) |
| Begleiter / Rückkehr | höchstens einer, kollisionslos; während Classic verborgen/pausiert, anschließend zurück; alle drei Arten und Sprint-Nachholen (`WildEncountersV2Movement02`) |
| Fang | Quellactor entfernt, kein Fluchtzustand (`FinalCapture01`); Teamwechsel, Inventar, Heilung und Save/Load separat (`WildEncountersV2Capture02`) |
| Spielerflucht | Wild bleibt aktiv, keine sofortige Wiederholung; drei Profile getrennt geprüft |
| WorldBattle-Sieg | sichtbarer Source-Actor, Mode bleibt WorldBattle, keine Classic-Flucht (`WorldOutcome01`) |
| Beide Kampfansichten | vier reale Classic-/World-Fälle mit Schiggy/Bisasam, Attacken und Rückkehr (`WildEncountersV2Modes02`) |
| Niederlagen-Autosave | echte Niederlage → Rückkehr/Heilung → Autosave → Reload, Team identisch (`WildEncountersV2Defeat02`) |
| Vor-/Nach-KO-Snapshot | kein Respawn nach KO-Laden; Vor-KO-Laden restauriert Spawn/Party und Bewegung (`Persistence01`) |

### Sichtbare KO-Flucht

| Art | Zeit nach Rückkehr* | Strecke aus Ortsstichproben | Kein erneuter Kampf | Erst außerhalb deaktiviert | Nachweis |
|---|---:|---:|---|---|---|
| Glumanda | 24.1 s | ca. 10.19 m | ja | ja | `FinalGlum01` |
| Schiggy | 24.8 s | ca. 10.42 m | ja | ja | `FinalSchiggy01` |
| Bisasam | 17.2 s | ca. 8.43 m | ja | ja | `FinalBisasam01` |

*Zeitangaben aus den aufgezeichneten Läufen einschließlich Screenshot-Overhead und Drehungen, **kein FPS-/Leistungsvergleich**. Ortsstichproben sind eine Näherung der tatsächlichen Weglänge. Erholung, Animation und Kapsel-/Bodenkontakt wurden aus der Spielkamera geprüft. Vegetation kann Teile der Flucht natürlich verdecken; der Actor wird deshalb nicht vorzeitig entfernt. Der zusätzliche westliche Anlauf `VisibleEscapeWest01` zeigt Glumanda klar auf dem offenen bestehenden Weg und anschließend außerhalb des Bilds.

### Gefundene und korrigierte Blockierung

Die zusätzliche 65-s-Bewegungsabnahme fand eine echte Planungs-/Bewegungsabweichung: Eine kurze diagonale Kreuzung einer erweiterten Felsecke lag zwischen 25-cm-Bodenproben. Der große geplante Weg wurde akzeptiert, der tatsächliche kleine Schritt wiederholt abgewiesen. Kontinuierliche Segment-/Kernbox-Prüfung zusätzlich zur Bodenabtastung und gezielter Regressionstest korrigieren dies.

Beim selben Zeitfenster: vorher 20.8 cm Gesamtbewegung / 43 blockierte Schritte; danach 300.0 cm / 0 blockierte Schritte. Der anschließend vollständig bestandene Begleitertest erreichte weiterhin die unveränderte Spielersprintgeschwindigkeit 315 cm/s. Das ist ein Funktionsvergleich, kein Renderingbenchmark.

Im Snapshot-Nachweis stiegen die Spieler-XP über die bestehende BattleSession von 1261 auf 1353. Nach explizitem Vor-KO-Laden wurden die ursprünglichen Instanz-IDs, HP und XP restauriert; die reaktivierte Wildfigur lief erneut 35.8 cm innerhalb ihres Habitats.

## Build, Automation und vollständiger Fußlauf

- Mac Development Editor, erzwungener Unity-Build ohne adaptive Ausschlüsse: bestanden (`WildEncountersV2PersistenceBuild01`).
- Vollständige Projekt-Automation: **87/87**, keine Testwarnungen/-fehler, keine ausgelassenen Tests (`WildEncountersV2PersistenceAutomation01`). Darunter Kontaktgeometrie, fünf Temperamente/Override, Richtungszielwahl, optionale gemeinsame Controller-Zuordnung, kontinuierliche Hindernisprüfung und eingeschlossene Flucht.
- Letzter kompletter echter PIE-Fußlauf: **103 Schritte, 287.20 m**. Wanderer/Quest, Liora, Wildkampf/Fang, Archiv, Brücke, Betreten/Verlassen, Heilhaus/Heilen, Save/Load, acht Richtungen und Sprint bestanden. Keine Testteleports; vorhandene reguläre Innenraumverlagerung bleibt bestehen (`WildEncountersV2FullFinal01`).
- Der volle Fußlauf verwendet die vorhandene technische Testparty; daher dort kein 3D-Begleiter aus Slot 1. **Keine falsche Begleiter-Innenraumabnahme:** Begleiter wurden separat mit den drei tatsächlichen Starterarten geprüft. Der read-only Fullroute-Observer meldete keine Probleme.
- Originaler Dev-Slot nach allen schreibenden Tests SHA-geprüft restauriert: `d9bf0677d2f06bb96bfe20f0eec7a9b369ba010117de0d49f13b9d027f8dbf6b`.

### Alle vorhandenen Map Checks

| Asset | Fehler | Warnungen |
|---|---:|---:|
| `/Game/Maps/Dev_BattleTestMap` | 0 | 0 |
| `/Game/Maps/Dev_BuildingKitTestMap` | 0 | 0 |
| `/Game/Maps/Dev_HealingHouseTestMap` | 0 | 0 |
| `/Game/Maps/Dev_TestMap` | 0 | 0 |
| `/Game/Maps/Dev_TestMap_NPCMotionV3` | 0 | 0 |
| `/Game/Maps/Dev_TestMap_VisualV2` | 0 | 0 |
| `/Game/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1` | 0 | 0 |
| `/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1` | 0 | 0 |
| `/Game/Maps/Dev_WestlandAssetLibrary` | 0 | 0 |
| `/Game/Maps/Dev_WestlandRegion` | 0 | 0 |
| `/Game/Maps/Dev_WestlandVillage` | 0 | 0 |

Tatsächlich vorhanden sind elf Maps, einschließlich der geschützten unversionierten EnvironmentQuality-Testmap. Keine neue Map. Zehn andere Mapdateien byte-/SHA-identisch erhalten. `Saved/WildEncountersV2/MapChecks.json` enthält die aus den echten deutschen/englischen Engine-Ausgaben gelesenen Ergebnisse.

## Echte Bildnachweise

Native Spielkamera-PNGs: **2560 × 1440**, 100 % Screen Percentage angefordert, keine Kameraänderung. ClassicBattle-Slate-Aufnahmen sind tatsächlich **2331 × 1311** und ausdrücklich keine QHD-UI-Nachweise; das vorhandene Classic-RenderTarget bleibt 2560 × 1080. Keine Konzeptbilder, keine retuschierten Spielweltpixel.

- `Saved/WildEncountersV2/Kontakt_Storyboard.png`: Nähe, echtes Hinlaufen, vorhandene Kampfansicht, Rückkehr/Flucht.
- `Saved/WildEncountersV2/Flucht_Storyboard.png`: zeitlich geordnete Originalbilder der sichtbaren Flucht.
- `Saved/WildEncountersV2/VisibleEscapeWest01/`: vollständige QHD-Bildfolge; Zeiten/Zustände in Result.json.
- `Saved/WildEncountersV2/FinalSchiggy01/`, `FinalBisasam01/`: weitere native Folgen, teilweise natürliche Kronenverdeckung.
- `Saved/WildEncountersV2/GroupFinal01/`: Gruppenbewegung und zwei Zielrichtungen.
- `Saved/WildEncountersV2/Persistence01/`: Vor-KO und restaurierter Snapshot.
- Herkunft, Größen und SHA der Storyboard-Originale: `Saved/WildEncountersV2/MediaProvenance.json`.

Storyboards enthalten nur proportional verkleinerte ganze Originalframes plus getrennte Beschriftung. Rohbilder bleiben erhalten. Sämtliche Kontrollmedien, T3D-Diagnosen, Test-Spielstände und Logs bleiben lokal unter ignoriertem Saved und werden nicht auf GitHub hochgeladen.

## Fehlversuche und Einschränkungen

| Befund | Behandlung |
|---|---|
| Compiler: zunächst falscher Camera-Includepfad, später doppelte UFUNCTION-Annotation | korrigiert; letzte Unity-Builds vollständig bestanden |
| Frühe Prüftreiber: nicht exponierte Python-Zugriffe / ein Syntaxfehler | korrigiert, frische Nachweisnamen; keine Erfolge aus abgebrochenen Läufen übernommen |
| Gruppeneinstellung: fehlerhafter Transform-Vergleich / Dirty-Map-Schutz | kein pauschales Speichern; vollständiger serialisierter Abgleich vor gezieltem Save |
| Erstes Gruppen-Zielfixture stand auf blockiertem Boden | gültigen Punkt über tatsächliche Bodenprüfung gewählt; finaler Gruppenlauf bestanden |
| Erster Bewegungslauf blieb nach etwa 20 cm hängen | echte kontinuierliche Hindernisprüfung ergänzt; gleicher Ablauf und volle Route erneut bestanden |
| Voll-KP-Fangversuch endete nach 22 Runden mit Spielerniederlage | kein bestandener Fangnachweis. Kontrollierte vorhandene 1-KP-/Seed-51-Fixture und separate Team-/Fangtests verwendet; Fangquoten nicht als gebalanced erklärt |
| Frühe Automation: 85 saubere Tests + ein bestandener Test mit zwei Engine-iOS-Helferwarnungen | dokumentiert; letzte vollständige Läufe 87/87 ohne Testwarnungen |
| Engine meldet wiederholt `idevice_id` „Bad CPU type“ sowie bekannte Start-/Plattformvalidierungen | unverändert dokumentiert; keine neuen Gameplay-/Buildfehler daraus abgeleitet |
| Materialwarnung `MI_WLA_LeafOak` ohne InstancedStaticMeshes-Nutzungsflag | bestehender separater Grafikbefund, nicht durch Materialänderung unterdrückt; außerhalb dieses Auftrags |
| Getrennter lesender Export-Commandlet meldete HTTP-Port 8000 belegt | kein Build-/Map-Check-Erfolg daraus behauptet; Exportdatei und vollständiger Vergleich separat geprüft |

Konservative Stamm-/Felskörper ersetzen keine Dreiecksnavigation für alle Dekorationen. Bewegliche neue Hindernisse erhalten weiter die reale Kollisionsprüfung; die dekorativen Kerne werden beim Configure erfasst. Schwimmen, Fliegen und neue Körperformen sind nicht neu implementiert. Bei versperrtem Weg kann Warten sichtbar bleiben; verfolgt der Spieler die Flucht dauerhaft, ist keine feste Despawnzeit garantiert. Der sichere geschlossene-Ring-Ablauf ist automatisiert, keine behauptete reale PIE-Ringaufnahme.

Die Fluchtabnahme gilt für die drei gültig konfigurierten 3D-Starter. Reine historische Sprite-Platzhalter ohne gültige Präsentation und Wanderkonfiguration sind nicht als vollständig animierte Fluchtgegner abgenommen; sie verbleiben gegebenenfalls sicher nicht interaktiv im Wartestatus.

Physischer Switch-Pro-Controller-Test **offen**. Keine FPS-Benchmarks oder neuen Performancebehauptungen. Keine neuen Modelle, keine Animationserstellung und keine Landschafts-/Heilhaus-/Licht-/Sichtkreisänderungen. Die technische Arbeit ist abgeschlossen; eine visuelle Nutzerabnahme der bestehenden Darstellung und der Interaktionsmarkierung bleibt sinnvoll.

## Git-/Originalschutz und Sicherung

58 vorbestehende unversionierte Dateien anhand ihrer SHA-256 unverändert erhalten, darunter die sieben neuen Incoming-Originalmodelle. Kein Add dieser Dateien. Alle Original-Blender-/Unreal-Quellen und übrigen Maps bleiben erhalten. Vollbackup `03492bd96b4dba44692f675c19d5f11abfa86b4b` unter beiden bestehenden lokalen Ref-Namen unverändert und nicht in main-Historie aufgenommen. Ein einziger vorhandener Worktree; keine Kopien, kein Reset/Clean/Prune/Force-Push.

Die tatsächliche VisualV2-Datei hat 4,154,391 Bytes. Sie ist die einzige neue LFS-Fassung dieses Pakets. Vor Commit werden die vollständige Indexliste, Core-Prüfsummen, canonical LFS-Pointer, lokales Objekt, Größen und Diff-Check geprüft. Nur benötigte Quellen, Werkzeuge und Dokumentation werden aufgenommen.

**GitHub-Sicherung verifiziert:**

- Implementierung, geprüfte Mapkonfiguration, Tests, Werkzeuge und Bericht: Commit `ed0eb6a9592a69d610a2557ab531f153ee9211aa` (`feat: add behavior-based wild encounters and visible defeat escapes`), regulär nach `origin/main` gepusht. Direkter `git ls-remote` und lokales `origin/main` stimmen überein.
- Tatsächlicher Index: exakt **48** freigegebene Pfade, **4.089** erforderliche Dateien gegen den Index-Prüfsummenstand validiert. Keine vorbestehende unversionierte Datei aufgenommen. `git diff --cached --check` bestanden.
- Normale Git-Daten: konservative unkomprimierte Obergrenze **1.318.401 Bytes**, deutlich unter der Projektgrenze von 1 GiB je Push. Keine übergroße normale Git-Datei.
- LFS separat: genau **1 Objekt, 4.154.391 Bytes** (VisualV2). OID `e5077409ff4ac69f12a9ce9b154419af916a2df3ac97714dcc38159cb0790d56`. Lokales Objekt und canonical Indexpointer geprüft; Upload erfolgreich; anschließend tatsächlicher Download von GitHub mit identischer Größe und SHA-256. Receipt: `Saved/WildEncountersV2/RemoteLFS_Implementation.json`.
- Nach dem Implementierungspush waren Index und getrackter Arbeitsbaum sauber; alle **58** geschützten unversionierten Dateien unverändert erhalten. Kein Force-Push, Kauf, Budgetwechsel oder LFS-Prune.
- Dieser abschließende Sicherungsnachtrag betrifft ausschließlich den Bericht und dessen Eintrag im Core-Prüfsummenmanifest. Sein separater Dokumentationscommit ist über die Git-Historie und den Abschluss im Chat nachvollziehbar; keine erneute Gameplayänderung.
