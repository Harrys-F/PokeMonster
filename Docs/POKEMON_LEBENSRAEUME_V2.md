# Pokémon-Lebensräume V2 – Prüfbericht

Fortschreibung: Die anschließende sichtbare Erstbesiedlung, zehn Zonen, der vertiefte Wasserlebensraum und die neue Entwicklungs-Testparty sind in [VISUALV2_POKEMON_WASSER_TEAM_V1.md](VISUALV2_POKEMON_WASSER_TEAM_V1.md) dokumentiert. Die folgenden Zahlen und Einschränkungen beschreiben die ursprüngliche V2-Prüfung.

Stand: 28.10.2026. Basis `57a76037` auf `main`, UE 5.8.2, MacBook Air M4/16 GB/Metal.

## 1. Bestand und Abgrenzung

VisualV2 besitzt eine zusammenhängende Bodenfläche von etwa 90×65 m, Dorf und Heilhaus mit verlagertem Innenraum, Wiesen, Waldgruppen, Waldränder, nördliche Freiflächen, einen kleinen dekorativen Teich/Bach und niedrige Felsstufen. Die frische Laufzeitinventur `Saved/ProjectRefinement/PokemonHabitatsV2/Survey02/Survey.json` ist maßgeblich. Es werden keine Höhlen, großen Gewässer oder zusätzlichen Biome unterstellt.

Das vorhandene Modellgelände hatte eine fest gepflegte Elf-Arten-Liste und nur PIE-Zugang. Das zentrale AssetManager-Register enthält tatsächlich 21 CreatureSpecies: 18 mit gültiger spielbarer Präsentation sowie drei technische Testarten ohne entsprechendes 3D-Modell. Die Incoming-Modelle sind keine integrierten Arten und werden nicht importiert.

Die freie Welt und das Modellgelände verwenden dieselben Präsentations-/Bewegungsklassen, aber unterschiedliche Zwecke und Objekte. Modelle im Testbereich sind weder Wildencounter noch Pokémon-Instanzen und besitzen keine Fang-/Save-Identität. Die normale Welt ist keine Vollausstellung aller Arten.

## 2. Modellgelände: Bedienung und Registrierung

Unreal-Konsole in normalem VisualV2-PIE oder einem Development-Spielprozess:

```text
pm.TestGround.List
pm.TestGround.Go
pm.TestGround.Go Pikachu
pm.TestGround.Go Glumanda
pm.TestGround.Go 18
pm.TestGround.Mode idle
pm.TestGround.Mode walk
pm.TestGround.Mode run
pm.TestGround.Mode turn
pm.TestGround.Mode directions
pm.TestGround.Mode auto
pm.TestGround.React attack
pm.TestGround.React hit
pm.TestGround.React faint
pm.TestGround.React happy
pm.TestGround.Reset
pm.TestGround.Return
```

`Go` und `Go 0` besuchen den vorhandenen Mittelpunkt −7500/−4000/0 cm. Ein Artenname, interne ID oder die aktuelle Stationsnummer aus `List` besucht das betreffende Modell. Rückkehr benutzt die vorherige Spielertransformation; bei blockierter Rückkehr bleibt der Anker erhalten. Keine neue Map. Shipping und andere Maps sind ausgeschlossen.

Der bisherige Bereich wächst nach Süden: aktuell fünf Spalten, vier Reihen, 18 m Stationsabstand, Boden etwa 90×72 m. Die Nordkante bleibt bei Y=−3600 cm außerhalb des Hauptbodens (Ende Y=−3250 cm). Ein größerer Mesh-Bounds-Bedarf erhöht den Abstand automatisch. Die echte Weltgröße der Modelle und die Spielkamera werden nicht skaliert.

`auto` zeigt 5 s Idle, 12 s Walk, 12 s Run, 5 s Turn und 4 s Idle. `directions` verwendet acht kontrollierte Wegpunkte. Bewegung, Beschleunigung, Richtungswechsel und Bodenprüfung stammen aus der vorhandenen Roaming-Komponente. Laufgeschwindigkeit berücksichtigt bestehende individuelle Oberweltüberschreibungen. Run benötigt einen vorhandenen passenden Clip; fehlende Rollen werden nicht künstlich erfunden. Karpador/Garados verwenden ihre vorhandene Schwimm-Präsentation. Reaktionen verwenden die vorhandenen Clips.

Animation und Bewegung werden nur während eines expliziten Besuchs und in Spielernähe aktiviert. Keine Nahrungssuche, Flucht, Sozialkontakte oder Tagesrhythmen auf diesen Visuals. Der reguläre eigene Begleiter bleibt ein eigenständiges Gameplay-Objekt. Speichern und Laden sind während des Modellbesuchs gesperrt und nach `Return` wieder verfügbar. Das verhindert versehentlich gespeicherte Testkoordinaten; keine Änderungen am Save-Format.

### Aktueller Modellkatalog

| Station | Modell | Stabile interne ID | Referenzgröße |
|---|---|---|---|
| 1 | Bisasam | `Bisasam` | 70.0 cm |
| 2 | Glutexo | `Glutexo` | 110.0 cm |
| 3 | Glurak | `Glurak` | 170.0 cm |
| 4 | Schiggy | `Schiggy` | 50.0 cm |
| 5 | Raupy | `Raupy` | 30.0 cm |
| 6 | Smettbo | `Smettbo` | 110.0 cm |
| 7 | Hornliu | `Hornliu` | 30.0 cm |
| 8 | Bibor | `Bibor` | 100.0 cm |
| 9 | Habitak | `Habitak` | 30.0 cm |
| 10 | Pikachu | `Pikachu` | 40.0 cm |
| 11 | Myrapla | `Myrapla` | 50.0 cm |
| 12 | Enton | `Enton` | 80.0 cm |
| 13 | Machomei | `Machomei` | 160.0 cm |
| 14 | Nebulak | `Nebulak` | 130.0 cm |
| 15 | Gengar | `Gengar` | 150.0 cm |
| 16 | Karpador | `Karpador` | 90.0 cm |
| 17 | Garados | `Garados` | 650.0 cm |
| 18 | Glumanda | `Zunderlauf` | 60.0 cm |

Glumanda behält ausdrücklich die historische interne ID `Zunderlauf` und die bisherige Dex-Metadatenzahl 1002. Die Sortierung nach vorhandenen Metadaten platziert es derzeit zuletzt. Namen/IDs sind für dauerhafte Skripte geeigneter als Stationsnummern.

Neue Arten werden über den vorhandenen PrimaryAsset-Typ `CreatureSpecies` unter `/Game/Data/Creatures` registriert. `GetRegisteredPlayableSpecies()` prüft gültige Oberweltdaten und Präsentation; das Gelände erzeugt nach regulärer Registrierung und vollständigem Editor-/Spielprozess-Neustart automatisch eine Station. Keine zusätzliche Modellliste und kein manueller Umbau. Aktuell besitzen alle 18 Präsentationen sieben validierte Rollen mit passenden Skeletons; unveränderte bestehende Animationsqualität ist keine neu erstellte Animation.

## 3. Natürliche Lebensräume

`Habitats/PokeMonsterHabitatSubsystem` erzeugt in VisualV2 unsichtbare Laufzeitzonen aus `Config/DefaultPokeMonsterHabitats.ini`. Kein Speichern einer Map erforderlich. `APokeMonsterHabitatZone` verwendet den bereits vorhandenen Oberflächen-/Medienvertrag von `APokeMonsterBiomeHabitat`; die vorhandene Biom-Testmap bleibt ohne das neue Opt-in unverändert. Für spätere andere Maps können explizit konfigurierte HabitatZone-Actors verwendet werden. Dort erfolgt keine automatische VisualV2-Anlage.

| Zone | Typ | Zentrum X/Y cm | Halbausdehnung X/Y cm | Höchstzahl |
|---|---|---|---|---|
| WestVillageEdge | Village | −4400 / −600 | 650 / 650 | 1 |
| WestMeadow | Meadow | −4500 / −2050 | 1100 / 650 | 2 |
| WestForest | Forest | −4350 / 1600 | 1050 / 1050 | 2 |
| NorthGlade | Glade | −2050 / 2450 | 1000 / 400 | 1 |
| ForestEdge | Edge | −2050 / 1450 | 450 / 300 | 2 |
| EastForest | Forest | 1000 / 2000 | 1300 / 850 | 2 |
| PondShore | Shore | 1500 / −1200 | 500 / 550 | 1 |
| RockSteps | Rock | −1100 / 1100 | 450 / 400 | 1 |

Alle Zonen prüfen tatsächliche Bodenflächen; innerhalb eines Rechtecks ist nicht automatisch jeder Punkt begehbar. Gebäude/Innenräume, steile Flächen, blockierende Kollisionen und dekorative Baum-/Felskerne werden durch die bestehenden Projektions- und Wegprüfungen ausgeschlossen. Zonengrenzen berücksichtigen den Körperradius. Das natürliche Fluchtverhalten erhält diese Begrenzungen; besiegte Quellen verwenden weiterhin den bestehenden Rückzugs-/Entfernungsablauf.

### Kuratierte Artenregeln

| Art | Zulässige Typen | Gewicht | Artmaximum | Populations-Zeitpräferenz |
|---|---|---:|---:|---|
| Bisasam | Meadow, Edge, Glade | 4 | 2 | Tag |
| Pikachu | Edge, Village, Forest | 3 | 2 | Tag |
| Glumanda | Rock, Glade | 1 | 1 | Flexibel |
| Myrapla | Meadow, Edge, Forest | 3 | 2 | Nacht |
| Enton | Shore, Village | 2 | 1 | Dämmerung |
| Nebulak | Forest | 1 | 1 | Nacht |
| Schiggy | Shore | 2 | 1 | Flexibel |
| Raupy | Meadow, Forest, Edge | 3 | 2 | Tag |
| Hornliu | Forest, Edge | 2 | 2 | Tag |
| Smettbo | Meadow, Glade, Edge | 1 | 1 | Tag |
| Bibor | Forest, Edge | 0,7 | 1 | Tag |
| Habitak | Meadow, Rock, Edge | 1 | 1 | Tag |

Dies sind ausdrücklich abstimmbare Projektgewichte, keine behaupteten Original-Spawnraten. Die vorhandenen Begegnungsprofile liefern Art, Levelbereiche, Attacken, Kampfdarstellung und Fangdaten. Keine neuen Attackenwerte. Große entwickelte Formen Glutexo, Glurak, Machomei und Gengar erhalten in dieser kleinen Landschaft keinen allgemeinen Wildspawn. Karpador/Garados bleiben ohne nachgewiesenen geeigneten Schwimmraum ebenfalls ausschließlich im Modellgelände. Der Teich wird nicht durch eine erfundene Unterwasser-/Schwimmzone ersetzt. Enton/Schiggy nutzen begehbare Uferflächen und ihre vorhandene Landbewegung.

## 4. Population, KI und Speicherung

Global höchstens zehn Tiere aus höchstens sechs Arten; Zonen- und Artmaxima gelten zusätzlich. Der einzige Populationstimer läuft alle zwei Sekunden und erzeugt höchstens eine Quelle pro Durchlauf. Er verwendet das vorhandene Weltuhr-/Gameplay-Pausenverhalten. Kein Spawn bei Kampf, pausierter Uhr oder gesperrter Steuerung. Zonen weiter als 50 m werden nicht vorab vollbesiedelt.

Mindestens 11 m Abstand zum Spieler, 2,2 m zu anderen Populationsmitgliedern und dem sichtbaren Begleiter sowie konservative Bildschirm-Bounds-Prüfung mit 160 Pixel Reserve verhindern sichtbares Erscheinen. Boden-, Hindernis- und Gebäudeprüfungen kommen hinzu. Entfernen erfolgt nach mindestens 120 s Aufenthalt, über 42 m Spielerabstand und außerhalb der Spieleransicht; entfernte besiegte/gefangene Quellen folgen ebenfalls der bestehenden Lebenszykluslogik. Es gibt keine sichtbaren Tagesphasen-Despawn-Schalter. Tageszeit gewichtet die Nachbesiedlung; bereits sichtbare Pokémon behalten ihre Identität und wechseln über KI V2.2 natürlich ihre Aktivitäten.

Die bisherigen zehn frei platzierten Vorführ-Wildquellen bleiben mit ihren ursprünglichen IDs und Daten in der Map, werden bei aktiver VisualV2-Verwaltung aber zur Laufzeit suspendiert. Ihre bisherigen Gruppen werden nicht zusätzlich als zweite Population angelegt. Kein Umschreiben alter Save-IDs.

Jede neue Quelle ist ein regulärer `APokeMonsterVisibleWildCreatureActor`. Bestehende Roaming-/A*-Wegprüfung, Wahrnehmung, Flucht, Territorialreaktionen, Sozialreservierung, Factory, ClassicBattle, Fang und persistente Encounter-Abschlüsse bleiben maßgeblich. Die sechs bisherigen Aktivitäts- und Tagesrhythmusprofile bleiben erhalten. Weitere kuratierte Arten verwenden dieselben konfigurierbaren Aktivitäts-/Rhythmusstrukturen. Schwebe-/Flugdarstellung nutzt ausschließlich vorhandene Präsentationsfunktionen; kein neues Flug-Navigationssystem und keine neuen Clips.

Stabile Quellkennung: `HabitatV2_<Zone>_<Platz>_<Art>_D<Weltuhrtag>`. Bestehende Save-Daten merken besiegte/gefangene Kennungen. Derselbe Platz/Art/Tag wird nicht unmittelbar erneut ausgerollt; am nächsten Spieltag ist Nachbesiedlung möglich. Wildpositionen und Populationstimer bleiben Laufzeitdaten, wie bei den bisherigen Wildquellen. Gespeicherte individuelle Pokémon, Repertoire, AP, Team, Weltzeit, Spielerposition und Kontrollpunkt erhalten ihr bestehendes Format.

In über 35 m Entfernung werden vorhandene Actor-/Bewegungsupdates auf 0,5 s reduziert. Die bisherigen Aktivitäts-Distanzgrenzen und `OnlyTickPoseWhenRendered` bleiben bestehen. Modellvisuals werden bei normaler Welterkundung vollständig von ihren Testbewegungen getrennt. Messung der KI-Mikrosekunden ist standardmäßig deaktiviert.

Entwicklungsdiagnose:

```text
pm.Habitats status
pm.Habitats 0
pm.Habitats 1
```

`0` entfernt die verwaltete Population ausdrücklich für Diagnosevergleiche, `1` erlaubt kontrollierte Nachbesiedlung. Die alte Vorführgalerie bleibt dabei suspendiert. Während eines Kampfes ist diese Umschaltung gesperrt. Die Befehle sind nicht Teil der normalen Spielerbedienung und in Shipping nicht registriert.

## 5. Tatsächliche Prüfungen

- Abschließender Editor-Build `PokemonHabitatsV2Build09`: Exit 0. Produktive Spawnlogik zuletzt in Build08 ergänzt; Build09 ergänzt ausschließlich den Test echter Begegnungs-Rolls aller zwölf Arten.
- Letzte vollständige Automation `PokemonHabitatsV2Automation07`: **284 funktional erfolgreich, 0 fehlgeschlagen**, davon ein Test mit zwei externen iOS-Helferwarnungen. Unreal-Prozess Exit 0, **strenger QA-Wrapper Exit 1**. Dieser letzte Lauf ist damit kein vollständig warnungsfreier Wrapper-Erfolg. Die isolierte Ausführung verwendet dieselbe strenge Ergebnisprüfung wie der bestehende Wrapper, zusätzlich `-UserDir`, `-nowrite` und `-NoAssetRegistryCacheWrite` zum Schutz vorhandener Dateien; kein Warnungsfilter.
- Die Zwischenläufe Automation04 und Automation05 erreichten jeweils 284/284 ohne Testwarnungen und Wrapper-Exit 0. Frühere Läufe sowie Automation06/07 hatten ausschließlich die separat genannten iOS-Testwarnungen und Wrapper-Exit 1. Keine unveränderte Wiederholung nur zum Erzielen eines grünen Ergebnisses.
- Drei neue Habitat-Testfälle prüfen bestehende Profildaten, echte gültige Encounter-/Factory-Rolls aller zwölf konfigurierten Arten, Art-/Zonengrenzen, Zeitpräferenzen, stabile Kennungen, Mapabgrenzung und Suspendierung. Modelltests verwenden alle registrierten Präsentationen und bestehende Boden-/Wegprüfung.
- `ModelReview05`: echter Development-Spielprozess, 18/18 Modelle besucht, konkrete Walk-Bewegung 20,3–182,2 cm im jeweiligen Beobachtungsfenster, 68 Prüfeinträge, Rückkehr und anschließendes isoliertes Speichern erfolgreich. Frühere Harness-Versuche 01–04 scheiterten an Python-API-Zugriffen und sind keine bestandenen Gameplayprüfungen.
- `HabitatReview02`: 33 Prüfeinträge, acht Bereiche und verschiedene Tageszeiten. Nachprüfung aller 95 Populationsbeobachtungen in 10 Samples gegen die finale Konfiguration: Grenzen, Art-/Zonen-/Gesamtmaxima, Zuordnung und Aktivitäts-/Rhythmusbindung bestanden. Alle acht Zonen tatsächlich besiedelt, höchstens zehn Tiere aus sechs Arten gleichzeitig. Vorlauf `HabitatReview01` ist separat erhalten.
- Beobachtet: Wandern, Rest, Sleep, Idle, Observe, Forage, neugierige Annäherung und Rückzug. Ein abgeschlossener spontaner Sozialkontakt wurde im kurzen Zonenrundgang nicht erfasst; die vorhandenen Sozial-/Reservierungs-Automationstests bestanden. Keine behauptete neue Schlafanimation.
- `Functional01`: echter Development-Spielprozess, 70 Schritte/20 Ergebnisprüfungen bestanden: Modellbesuch, NPC-Dialog, Heilhaus-Ein/Austritt, Innenraum-Save/Load, Pausen, Tagesphasengrenzen/Mitternacht, natürlicher Wildkampf, Attacke, Flucht, regulärer Fang, persistentes Viererteam, Teamsortierung und Begleiterwechsel.
- Erste PIE-Läufe 01/02 erreichten Fang und Viererteam, scheiterten danach an der Begleitersichtprüfung. `CompanionProbe01` zeigte dasselbe ohne Kampf: gesunder sichtbarer Actor mit laufender Bewegung, aber vom Heilhausdach verdeckte Figur/Begleiter. Keine belegte Fang-/Speicherregression. Die betroffene ForestEdge-Zone wurde nach Norden begrenzt; Kamera und Gebäude unverändert.
- **`PIEGameplay03`: alle 70 Schritte/20 Ergebnisprüfungen bestanden**, einschließlich nach Fang gerendertem Begleiter, regulärer Teamsortierung, AP/Repertoire-/Positions-/Weltzeit-Save/Load und Innenraum. Zwei weitere PIE-Sitzungen bestanden Bewegung, Sprint, Software-Controllerbedienung, Menüfokus, Profilrückkehr und Phasenwechsel (`EditorCycles02.json`). Reguläres Beenden ohne Stillstand. Einschließlich Diagnose-/Vorlaufsitzungen insgesamt sechs kontrollierte PIE-Enden in zwei eigenen Editoren; finale drei Sitzungen erfolgreich.
- **Zwölf Map Checks**, jede vorhandene Map geprüft: jeweils 0 Fehler und 0 Map-Check-Warnungen (`MapCheckSummaries.json`). Keine Map gespeichert.
- **`WorldFootwalk01`: 319,05 m, 28 Wegpunkte in 133,08 s**, reguläre EnhancedInput-Bewegung, Gehen/Sprint und folgende Kamera. Ein Vorbereitungsteleport zum Start, **keine Teleports entlang der Route**. Dorf, Wiese, Wald, Waldrand/Lichtung, Ufer und Felsbereich durchlaufen. 114 Stichproben, maximal zehn Tiere, Begleiter in 113 gerendert. Hier keine zufällige Kampfberührung; Kampf/Fang sind im separaten Ablauf geprüft.
- **`Travel01`: bestanden**, VisualV2 → vorhandene Dev_TestMap → VisualV2, gleicher GameInstance-/Weltuhr-/Teamzustand, weiterhin Profil C/IFG/TAAU/VSM4 und regulärer Begleiter. Kein World-Cleanup-Stillstand.

### Warnungen und Einschränkungen der Logs

Externe iOS-Infrastruktur: `idevice_id` / „Bad CPU type in executable“ / „Failed to launch Tool“. In Automation07 traf dies `PokeMonster.Encounter.OverworldIntegration`; beide Meldungen sind Warnungen, kein fehlgeschlagener Projekttest. Im finalen PIE-Editorprotokoll zusätzlich 17 `LogAutomationTest: Error: Condition failed` bereits bei Frame 0; dieselbe Anzahl steht im bestehenden V5-Referenz-Editorprotokoll. Dieser bekannte Startbefund wird nicht als neue Habitat-Testfehlfunktion und nicht als iOS-Warnung umetikettiert; seine Ursache ist hier nicht geklärt.

Die vorhandene Messinstrumentierung meldet viele `FindConsoleObject`-Abfragen für TAA-Upsampling. Eine bekannte Blattmaterial-/Instancing-Meldung und die durch die bestehende Nutzerkonfiguration aktivierte rote Precomputed-Visibility-Anzeige werden nicht durch Änderung geschützter Materialien/Konfiguration verdeckt. In den finalen nativen Funktions-, Reise- und Benchmarklogs sowie im finalen PIE-Log kein Fatal Error, keine `Assertion failed`, kein GPU-Crash/Out-of-video-memory. Frühere Python-Harnessfehler bleiben als fehlgeschlagene Versuche dokumentiert.

## 6. Echte Bildnachweise

Alle nachfolgenden Dateien sind tatsächliche Unreal-Aufnahmen, keine generierten Bilder:

- `Saved/ProjectRefinement/PokemonHabitatsV2/Functional01/Model_Pikachu.png` (2560×1440).
- `Saved/ProjectRefinement/PokemonHabitatsV2/HabitatReview02/Habitat_00.png` bis `Habitat_07.png` (je 2560×1440; tatsächliche Bereiche des Rundgangs).
- `Saved/ProjectRefinement/PokemonHabitatsV2/Functional01/C_ClassicBattle.png`, `C_CompanionAfterCapture.png`, `C_SwitchedCompanion.png`, `C_Interior.png`.

Zusätzliche Nachweise: `PIEGameplay03/C_CompanionAfterCapture.png` und `CompanionProbe01/Probe7.png` (der ausgeschlossene Dachbereich).

PIE-Fensteraufnahmen können die Editorfenstergröße besitzen und werden nicht als QHD-Backbuffer-Benchmark ausgegeben. Keine neue große Video-/Rohbildfolge. Hochfrequente temporale Videoabnahme sämtlicher bestehender Animationen ist nicht Bestandteil des behaupteten Nachweises.

## 7. Performance

Reale Development-Spielprozesse, Welt/NPCs/Begleiter aktiv, keine Aufnahme. Shader-/Asset-Vorlauf, danach 25 s Warm-up und 30 s Messung je Fenster. Je drei gültige Wiederholungen pro Ort und Populationszustand, wechselnde Reihenfolge. Identische gesteuerte Routen, vergleichbare Bewegungsstrecke; kein deterministischer kompletter Welt-Replay.

18 Fenster wurden insgesamt aufgezeichnet. Sechs vollständige Fenster aus `Benchmark01` hatten ein inaktives Spielfenster und sind **methodisch ausgeschlossen**, nicht um einzelne langsame Frames gekürzt. Ihre Daten bleiben erhalten. Die vollständigen Vergleichspaare wurden einmal in `BenchmarkForest1`, `BenchmarkVillage2`, `BenchmarkForest2` wiederholt. Ergebnis: **12 gültige Vordergrundfenster, 10182 echte Frames**, in jedem Frame tatsächliche 2560×1440-Ausgabe, 1920×1080 intern, TAAU, 75 %, High, Kamerawinkel −50°/−45°, FOV 35°. Lumen-/IFG-Pfad und VSM4 bestätigt. Globale AA-CVar 4 ist dabei nicht mit der tatsächlich verwendeten View-Methode 2 gleichgesetzt.

`r.VSync=0`, `t.MaxFPS=0`, bestehendes `rhi.SyncInterval=1`. Keine Veränderung des Präsentations-/Renderingprofils. Die frühen Fenster lagen auffällig nahe 30 FPS, spätere Fenster deutlich darunter oder darüber; die Ursache des Zeit-/Präsentationsverhaltens ist hier nicht isoliert. NSProcessInfo-Thermalzustände siehe `ThermalSummary.json`; kein allein daraus bewiesener thermischer Engpass.

| Ort | Zustand | Ø FPS | FPS-Laufspanne | GPU ms | Game ms | Render ms | p95 ms* | 1-%-Low FPS* | Max Frame ms |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|
| Dorf | Population aus | 31,13 | 30,00–33,38 | 28,75 | 2,14 | 32,20 | 33,77 | 23,69 | 68,42 |
| Dorf | 8–10 Tiere | 28,30 | 24,90–30,00 | 33,25 | 3,05 | 35,54 | 40,48 | 18,93 | 196,81 |
| Wald | Population aus | 26,26 | 23,93–30,00 | 37,07 | 2,64 | 38,41 | 44,69 | 18,91 | 124,05 |
| Wald | 8–10 Tiere | 27,45 | 18,98–33,37 | 37,27 | 2,86 | 38,60 | 46,52 | 19,73 | 129,84 |

\* p95 und 1-%-Low sind Mittel der drei vollständigen Fenster; 1-%-Low = Kehrwert des Mittels der langsamsten 1 % der Frames pro Fenster. Max Frame ist das größte Einzelereignis aller drei Fenster. GPU/Game/Render stammen aus den CSV-Profiler-Zeitreihen, FPS aus echten Frameabständen, nicht aus GPU-Zeit errechnet.

**Wichtige Abgrenzung:** `pm.Habitats 0` entfernt die verwalteten Pokémon. Der Vergleich umfasst deshalb Simulation **und** ihre Modell-/Animations-/Schattenkosten. Er isoliert nicht ausschließlich KI bei identischer sichtbarer Population. Die gewöhnlichen NPCs, eigener Begleiter, Grafikprofil, Routen und Weltuhr bleiben aktiv.

Die separat instrumentierten Roaming-Ticks benötigen im Mittel insgesamt 8,07 ms pro realer Sekunde im Dorf und 6,89 ms im Wald, entsprechend etwa 0,81 %/0,69 % eines CPU-Kerns bzw. ungefähr 0,29/0,25 ms pro tatsächlich gerendertem Frame. Einzelne mittlere Komponententicks: 22,6–52,2 µs. Diese Zahlen enthalten **nicht** Actor-Grundkontakt, Skelettanimation, Renderer, Populationstimer oder QA-Python und sind keine Behauptung über die kompletten Systemkosten.

Es besteht erhebliche zeitliche GPU-Drift, auch ohne Population. Daher weder ein behaupteter Performancegewinn noch eine belastbar allein der KI zugeschriebene GPU-Differenz. **Stabile 30 FPS sind nicht nachgewiesen.** Einzelne Spitzen bis 196,81 ms mit Population und 124,05 ms ohne Population bleiben offen; ihre Ursache ist nicht isoliert. Funktional besteht kein beobachteter Dauerstau/Renderingabsturz, aber die Leistungsreserve und Framezeitstabilität sind weiterhin ein eigener Optimierungspunkt. Ein späterer genauer KI-Ablationsvergleich sollte dieselben Modelle mit pausierter Simulation beibehalten und Hardware-/Präsentationsdrift kontrollieren.

Rohdaten, ausgeschlossene Fenster, Einzelläufe und Aggregation: `Saved/ProjectRefinement/PokemonHabitatsV2/PerformanceCombined.json`, dort aufgeführte vier Prozessverzeichnisse. Alte V4/V5-FPS werden nicht als neue Ergebnisse oder direkter Vorher-Nachher-Nachweis ausgegeben. Keine Grafikqualität reduziert, keine Rendering-Standardwerte geändert.

## 8. Einschränkungen und Erweiterung

- Konfiguration und Häufigkeiten sind eine erste kuratierte VisualV2-Belegung; kein Ökosystem, Hungerinventar oder weltweites Begegnungs-Balancing.
- Die Geburt einer Art ist gewichtet, kein garantierter Showcase. Einzelne Aufenthalte können ruhige Abschnitte zeigen. Das Modellgelände ist der garantierte vollständige Katalog.
- Kein freies großräumiges Flug-/Unterwassersystem, keine zusätzlichen Gebiete, keine neue Animation.
- Weitere Weltkarten benötigen bewusst platzierte Zonen und eine Prüfung ihrer bestehenden Spawnquellen. Westland und Biom-Testmap wurden nicht umgebaut.
- Neue Modelle: bestehende PrimaryAsset-Registrierung/Präsentationsvalidierung; Neustart aktualisiert Modellgelände automatisch. Neue Wildarten: zusätzlich ausdrücklich geeignete Habitatregel und vorhandenes Encounter-Profil freigeben.
- Physische Switch-Pro-Abnahme wird nicht behauptet; Software-Eingabeprüfungen und unveränderte Belegung sind separat dokumentiert.

## 9. Projektschutz und Git

Vorherige Nutzeränderungen in `Config/DefaultEngine.ini` und 34 vorher unversionierte Dateien bleiben erhalten und werden nicht in diesen Commit aufgenommen. Originale, Modelle, Animationen, alle Maps, bestehende Saves und geschützte Dateien werden gegen die Anfangshashes geprüft. Keine neuen Maps, Worktrees, Projektkopien, Backups oder destruktiven Git-Befehle. Keine Rendering-Produktionsänderung. Die vorhandenen Vollbackup-Refs bleiben unverändert. Hashprüfung bestanden: 6353 Anfangsdateien kontrolliert, darunter 414 vorhandene `.sav` (Nutzer- und frühere QA-Dateien), alle zwölf Maps und alle 34 vorher unversionierten Dateien; keine fehlenden oder unerwartet veränderten Anfangsdateien. `Config/DefaultEngine.ini` bleibt exakt beim vorhandenen Nutzerstand. Die 19 gezielt zugehörigen Code-/Konfigurations-/Dokumentationsdateien enthalten keine neuen LFS-Medien. Verifizierte Abschluss-SHA/Remote-/LFS-Ergebnisse werden lokal unter `Saved/ProjectRefinement/PokemonHabitatsV2/GitVerification.json` abgelegt; der Implementierungscommit ist im Git-Verlauf dieses Berichts nachvollziehbar.
