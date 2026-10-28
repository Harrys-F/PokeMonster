# VisualV2 – Wild-Pokémon, Wasserlebensraum und Testteam

Stand: 28.10.2026. Ausgangspunkt `4cf2a6f3` auf `main`, UE 5.8.2, macOS/Metal. Dieser Bericht ergänzt und ersetzt die bisherige Einschränkung des kleinen dekorativen Teichs aus `POKEMON_LEBENSRAEUME_V2.md`.

## 1. Bestandsaufnahme und Umsetzung

Die bisherigen acht Lebensräume, zwölf kuratierten Land-/Uferarten, zehn Individuen und maximal sechs gleichzeitigen Arten bleiben Grundlage. Der Modellkatalog enthält weiterhin 18 spielbereit registrierte 3D-Arten; die drei technischen Testarten und unregistrierte Incoming-Dateien gehören nicht dazu.

Der echte Starttest `Initial02` zeigte nach einer Minute zehn Wildexemplare, sämtlich außerhalb des Startbildes. Zufällige Zonenreihenfolge, große Sichtprüfgrenzen und das Artenbudget verhinderten eine zuverlässige Abdeckung nahegelegener Gebiete. Der ursprüngliche Teich war eine kleine dekorative Wasserfläche über alten durchgehenden Prototypböden; ein Boden bei Z = 0 wurde als tatsächlicher Blocker nachgewiesen. Die leere Standardparty wurde bisher mit zwei technischen `TestWater`-Instanzen initialisiert.

Verwendet werden weiterhin `PokeMonsterHabitatSubsystem`, dessen zentrale Konfiguration, `PokeMonsterVisibleWildCreatureActor`, die vorhandenen Encounter-Profile, die Pokémon-Factory, `PokeMonsterCreatureRoamingComponent`, KI V2.2, Weltuhr, Save V2 und das bestehende Modellgelände. Keine zweite KI, Artenregistrierung, Kampf-, Speicher- oder Schwimmarchitektur.

### Besiedlung

- Begrenzte Erstbesiedlung nach Actor-BeginPlay und vor dem ersten Spielframe. Große Modelle können dadurch erstmals erscheinen, ohne während des Spiels sichtbar hineinzuspringen.
- Spätere Neubesiedlung weiterhin höchstens ein Exemplar pro Zwei-Sekunden-Aktualisierung, mit Kamera-, Mindestabstands-, Boden-, Hindernis- und Gebäudeprüfung.
- Nahe leere Zonen und zunächst fehlende Gebietstypen erhalten Vorrang. Konfigurierbare Abdeckungsprioritäten: Dorf 60, Wald 45, Wiese 30. Wasserplätze werden vor Verbrauch des Artenbudgets berücksichtigt.
- **Höchstens zehn Wildindividuen aus sechs Arten**, zusätzlich Art- und Zonengrenzen. Ungültige Flächen erzwingen keinen Spawn.
- Bestehende Tagesrhythmen und zeitabhängige Gewichtungen bleiben aktiv. Keine neuen Spawnarten oder geänderten Fang-/Kampfwerte.
- Bestehende Vorführ-Wildactors bleiben ruhend mit ihren bisherigen IDs erhalten. Modellbesuche deaktivieren die natürliche Population nicht.

## 2. Lebensräume und Arten

Acht vorhandene Zonen bleiben erhalten: WestVillageEdge, WestMeadow, WestForest, NorthGlade, ForestEdge, EastForest, PondShore, RockSteps. Hinzu kommen:

| Zone | Mittelpunkt in cm | Halbausdehnung | Zweck |
|---|---|---|---|
| SouthMeadow | −1100 / −2300 / 0 | 750 / 450 / 300 | Wiese nahe dem normalen Startgebiet |
| PondWater | 720 / −1000 / 0 | 860 / 610 / 600 | Elliptisch begrenztes Wasser, maximal zwei Individuen |

| Art / vorhandene ID | Geeignete Zonenarten | Artmaximum |
|---|---|---:|
| Bisasam | Wiese, Waldrand, Lichtung | 2 |
| Pikachu | Dorfumgebung, Waldrand, Wald | 2 |
| Glumanda / Zunderlauf | Felsstufen, Lichtung | 1 |
| Myrapla | Wiese, Waldrand, Wald | 2 |
| Enton | Ufer, Dorfumgebung | 1 |
| Nebulak | Wald | 1 |
| Schiggy | Ufer | 1 |
| Raupy | Wiese, Wald, Waldrand | 2 |
| Hornliu | Wald, Waldrand | 2 |
| Smettbo | Wiese, Lichtung, Waldrand | 1 |
| Bibor | Wald, Waldrand | 1 |
| Habitak | Wiese, Felsstufen, Waldrand | 1 |
| Karpador | Wasser | 1 |
| Garados | Wasser | 1 |

Diese 14 Kandidaten sind eine kuratierte Auswahl aus dem bestehenden Register. Nicht alle erscheinen gleichzeitig. Gewichte und Abdeckungsprioritäten sind Projekt-Spielkonfiguration, keine behaupteten Original-Spawnraten. Individuelle Gegner, Level, Attacken und Fangdaten kommen aus den vorhandenen Encounter-Profilen.

## 3. Teich und Schwimmen

Der vorhandene Teich wurde nach Süden erweitert: sichtbare Fläche ungefähr **18 × 13 Meter**, Mittelpunkt 720/−1000 cm, Wasseroberfläche Z = 4,2 cm. Das tatsächliche Becken erreicht Z = −420 cm, entsprechend maximal 424,2 cm Tiefe. Die tiefe Innenfläche bietet auch dem vorhandenen Garados mit 650 cm Körperlänge Bewegungsraum. Körperlänge ist nicht mit Modellhöhe gleichgesetzt.

Der ursprüngliche Bodenumriss von ungefähr 90 × 65 Metern bleibt erhalten. Nur der VisualV2-Bodenactor verwendet ein neu abgeleitetes, geschlossenes Beckenmesh. Die originalen Engine-/Projektmeshes wurden nicht bearbeitet. Der unsichtbare Prototypboden `SM_DevFloor` bei Z = 0 wurde als tatsächlicher Blocker nachgewiesen und seine Kollision deaktiviert. Die überlagernde alte Hintergrundfläche bei Z = −22 wurde ebenfalls kollisionsfrei gesetzt; sie wird nicht als separat nachgewiesene Fehlerursache ausgegeben. Bodenmessungen treffen jetzt das reale Becken, außerhalb weiterhin Z = 0.

Die vorhandenen Wassermaterialien werden in zwei map-eigenen Kopien verwendet: erweiterte Teichmaske und bestehender Bach ohne dessen alte kleine Teichmaske. Der Bach und die Brücke bleiben bestehen. Die neue lokale Bachkopie wird innerhalb der Teichellipse maskiert, sodass beide Wasserflächen dort nicht mehr übereinanderliegen. `PondOverlap01` belegte die Ursache der goldenen Innenkanten durch einen temporären Sichtbarkeitsvergleich. Ein vorheriger Bodenfarbversuch und das temporäre Abschalten der Reflexionen halfen nicht; der Bodenversuch einschließlich ausschließlich seiner neuen, referenzfreien Materialkopie wurde vollständig verworfen (`BedExperimentReverted.json`). Originalbake, Originalmaterial, Normalen, Rauheit, Reflexionsverfahren und Renderingprofile bleiben erhalten. `PondViews03` dokumentiert den fertigen Anschluss. Beim wiederverwendeten Teichactor mussten sowohl Actor- als auch Komponenten-Sichtbarkeit aktiviert werden.

32 gezielte Actoranpassungen und 622 Vegetations-/Dekorationsinstanzen wurden im ersten Authoring-Schritt dokumentiert. Die Instanzen wurden auf das neue Ufer versetzt, nicht gelöscht. Anschließend wurden 35 zugehörige alte Baum-/Felskollisionshilfen an die sichtbaren Ufermodelle angepasst. Reale Abfragen hatten zuvor unter anderem `PondRock_01/02/03`, `Tree_11_Trunk` und `VS_Tree07Trunk` als Hindernisse für Garados nachgewiesen. Kollisionsformen, Originalmeshes und vorhandene Wege bleiben erhalten.

### Gemeinsame Medienverarbeitung

| Wasserart | Profillevel | Eintauchtiefe | Tatsächlicher Körperradius | Navigationsfuß Z |
|---|---:|---:|---:|---:|
| Karpador | 15 | 43 cm | 50 cm | −38,8 cm |
| Garados | 30 | 180 cm | 205 cm | −175,8 cm |

Die Größen-/Tiefenwerte verwenden die bestehende Wasser-Pipeline. Eine optionale Eintauchtiefe pro Bewegungskomponente erlaubt unterschiedlich große Pokémon im selben Wasserlebensraum. Rechteckige Bestandszonen behalten ihre bisherigen Standardwerte; nur PondWater verwendet die elliptische Grenze.

Zwölf konfigurierte Wegpunkt-Anker der vorhandenen Verarbeitung werden vom bestehenden variierenden Planer verwendet. Engere bzw. zu flache Ziele werden anhand der individuellen Körpergröße abgewiesen. Die reine Wasserpopulation betreibt keine landgebundene Nahrungssuche. Ruhe, Beobachten und die vorhandenen Reaktionen bleiben verfügbar. Geh-/Schwimmgeschwindigkeit, Beschleunigung und Drehung kommen aus den bestehenden Präsentations-/Artprofilen.

Der Wildactor verwendet die projizierte Wasserhöhe und den vorhandenen Schwimmlayer. Er wird nicht mehr durch seine zusätzliche visuelle Bodenabfrage auf den Teichgrund gesetzt. Der Kollisionsmittelpunkt kann bei einem teilweise eintauchenden Modell oberhalb der Wasseroberfläche liegen; entscheidend sind Eintauchtiefe, Modellpose und begrenzter Navigationsfuß. Das bedeutet keinen vollständig in der Luft schwebenden Spawn.

Die vorhandene Spieler-Wasserbarriere bleibt aktiv. Wasser-Pokémon ignorieren ausschließlich die markierten Spielerbarrieren in ihrer Bewegungs-/Sichtprüfung, bleiben aber durch Becken, Körperfreiraum, Tiefe und Lebensraumgrenze eingeschränkt. Kein Spieler-Schwimm- oder Unterwassersystem wurde eingeführt.

### Begegnungen vom Ufer

Die reale Diagnose `InteractionProbe02` belegte eine widersprüchliche doppelte Sichtprüfung: Der Wildactor erlaubte die Ansprache, während die generische Spielerauswahl dieselbe Spieler-Wasserbarriere als Hindernis wertete. Beide Prüfungen ignorieren jetzt dieselben ausdrücklich markierten Spielerbarrieren. Andere Wände, Felsen, Boden und echte Hindernisse bleiben wirksam. Die Auswahl berücksichtigt außerdem den tatsächlichen Körperradius von Wasser-Pokémon; Landquellen und NPCs behalten die bisherige Reichweite.

Reine Wasserquellen nutzen die bestehende manuelle Herausforderung (`Challenge`) vom Ufer, einschließlich Garados. Sein territoriales Temperament bleibt erhalten; es wird kein für den nicht schwimmenden Spieler unerreichbarer Kontakt im Wasser erzwungen. Originalprofile und Landbegegnungen werden nicht umgeschrieben. Dies ist eine explizite Projektentscheidung in `ENTSCHEIDUNGEN.md`.

## 4. Modellgelände

Unveränderte Befehle in VisualV2-PIE und Development-Spielprozess:

```text
pm.TestGround.List
pm.TestGround.Go Pikachu
pm.TestGround.Return
```

Alle 18 registrierten Modelle bleiben verfügbar: Bisasam, Glutexo, Glurak, Schiggy, Raupy, Smettbo, Hornliu, Bibor, Habitak, Pikachu, Myrapla, Enton, Machomei, Nebulak, Gengar, Karpador, Garados und Glumanda (bestehende ID Zunderlauf). Registrierung, Modellbewegungen und Rückkehr verwenden den vorhandenen Testbereich. Seine visuellen Exemplare zählen nicht zur Wildpopulation. Speichern während eines expliziten Modellbesuchs bleibt gesperrt.

Lediglich zwei interne lokale C++-Namen wurden eindeutig benannt, um durch die neue Unity-Zusammenstellung sichtbar gewordene Namenskollisionen zu beheben. Öffentliche Befehle und Verhalten wurden dadurch nicht verändert.

## 5. Standard-Testparty und Speicherkompatibilität

Nur eine **noch leere Entwicklungs-Testparty auf VisualV2** wird initialisiert:

1. Glumanda / bestehende ID Zunderlauf, Level 15.
2. Garados, Level 30 aus dem vorhandenen Wildprofil.
3. Pikachu, Level 11 aus dem vorhandenen Wildprofil.
4. bis 6. leer; keine ungültigen Platzhalterinstanzen.

Die bestehende Factory erzeugt Identität, Erfahrung und Werte. Glumandas vorhandene Lernliste wird ausdrücklich zugewiesen; Garados und Pikachu werden über die vorhandenen Profile einschließlich ihrer Attackenzuweisung erzeugt. Die Zusammenstellung wird nur vollständig übernommen, wenn alle drei Instanzen gültig sind.

`EnsureDevPlayerParty` kehrt bei einer bereits vorhandenen Party unverändert zurück. Geladene Teams werden weder ersetzt noch gelevelt oder geheilt. Es gibt keine automatische Umschreibung bestehender Dateien, kein neues Speicherformat und keine Änderung an AP-, Repertoire-, Entwicklungs-, Kontrollpunkt- oder Ohnmachtsregeln. Synthetische Battle-Testfixtures anderer Maps bleiben erhalten. Das neue Vorgabeteam gilt nicht automatisch für eine bereits geladene alte Party.

## 6. Technische Prüfungen

- Editor-Build `VisualV2WaterTeamV1Build13`: Exit 0.
- Vollständige relevante Automation `VisualV2WaterTeamV1Automation03`: **285 funktional erfolgreich, 0 fehlgeschlagen, 0 ausgelassen**. 284 ohne Testwarnung, ein Test mit zwei externen iOS-Helferwarnungen. Unreal-Exit 0, **strenger QA-Wrapper Exit 1**. Kein vollständig bestandener strenger Wrapper.
- Der ergänzte Test prüft die drei echten Teamarten, Level, vorhandene Lernattacken und freie Teamplätze. Habitatprüfungen umfassen die 14 echten Encounter-Rolls, zehn Zonen, Landhöhen, elliptische Körpergrenzen und stabile Identitäten.
- Alle zwölf vorhandenen Maps werden ohne Neuanlage geprüft. Abschließende Ergebnisse: zwölf explizite `MAP CHECK`-Durchläufe im abschließenden Editor08, jeweils **0 Fehler, 0 Warnungen**, bestätigt in `MapCheckSummaries.json`; keine andere Map gespeichert.
- Abschließende PIE-Prüfung: `PIEFunctional03` auf dem letzten C++-Build: **76 Ablaufsschritte und 22 Assertions bestanden**, 225.5 Sekunden. Darunter natürliche Wasserbewegung, Dorf/Wiese/Wald, alle 18 Modellregistrierungen, echte Modellreise und Rückkehr, NPC-Dialog, Innenraumdarstellung, Kamera-/Positions-/Checkpoint-/Weltzeit-/Teamdaten nach Save/Load, Phasenwechsel/Mitternacht, reguläre Attacke/Flucht/Fang, Teamsortierung und Begleiter. Zusätzlich zwei frische Zyklen `FinalCycles06`: Acht-Wege-Gehen/Sprint, Menüs, Controller-Softwareeingaben, Profilwechsel HardwareSPG/100/C und gültige soziale Reservierungen nach Phasenwechsel; sauberes PIE-Ende und reguläres Editorende. Der abschließende reine Materialanschluss wurde separat mit Ufer-PIE und Map Checks nachgeprüft; keine spätere C++-Änderung.
- Abschließender separater Gameplay-Test: `Functional05`: 76 Ablaufsschritte, 22 Assertions, 225,2 Sekunden; bestanden, echter Prozess-Exit 0. Initialisierung, Anfangsbesiedlung von Dorf/Wiese/Wald/Wasser, Modellgelände/Rückkehr, Dialog, Heilhaus, alle Tagesphasen, reguläre Attacke/Flucht, Pikachu-Fang, Teamtausch/Begleiter und Save/Load. Dieser Lauf ging der letzten gezielten Ufer-Auswahlkorrektur voraus; deren separater aktueller Nachtest ist unten dokumentiert.
- Zusammenhängender Fußlauf einschließlich Brücke: `WorldFootwalk01`: 32 Wegpunkte, 352,77 m in 151,97 Sekunden, bestanden; eine explizite Startvorbereitung, keine Teleports entlang der Strecke, vorhandene Brücke überquert. 132 Telemetriestichproben, Population 7–8 und höchstens sechs Arten, Begleiter in 131/132 Stichproben gerendert. Tag-/Nachtwechsel und eine normale Begegnungsunterbrechung mit Rückkehr.
- Mapwechsel mit älterer isolierter Party: `TravelLegacy01`: bestanden, echter Prozess-Exit 0. VisualV2 → vorhandene Dev_TestMap → VisualV2 mit älterem isoliertem Team Schiggy 13/Pikachu 11/Glumanda 5. Instanz-IDs, KP/AP, Team, Begleiter, Weltzeit und Renderingprofil erhalten; die neue Testvorgabe ersetzt dieses geladene Team nicht.

Isolierte `-UserDir`-Verzeichnisse und explizite PIE-Testslots schützen die vorhandenen Dateien. Der Hashabgleich erfasst **6.363 vorhandene Dateien, darunter 432 Spielstände und 34 geschützte unversionierte Dateien**. Zwischenprüfung: keine geschützte Änderung, keine fehlende Datei, Nutzeränderung an DefaultEngine.ini und beide Vollbackup-Verweise unverändert. Abschließender Abgleich: bestanden, keine fehlende oder geschützte Änderung; `Protection.json`.

### Bereinigte Befunde und getrennte Warnungen

Nicht erfolgreiche Zwischenläufe sind erhalten. Sie deckten die alte Materialmaske/Sichtbarkeit, unsichtbare Boden- und Uferkollisionen sowie die zunächst fehlende explizite Attackenzuweisung für den neuen Glumanda-Starter auf. Diese Fälle wurden korrigiert und in den nachfolgenden erfolgreichen Läufen überprüft. `WaterGameplay01` scheiterte an der doppelten Sichtprüfung; Diagnose02 wies die Spielerbarriere nach, `WaterGameplay02` prüfte die Korrektur erfolgreich. Zusätzlich wurden Python-Diagnoseabfragen und ausschließlich für PIE freigegebene Uhr-Testbefehle im separaten Prozess korrigiert; daraus wurde keine Produktionsänderung an der Weltuhr abgeleitet.

Die zwei Warnungen im letzten Lauf Automation03 trafen `PokeMonster.Creatures.DayRhythms.ReservationsSurviveTimeChangeAndReleaseInvalidPausedPeer`: externer Engine-Helfer `idevice_id`, „Bad CPU type in executable“ und „Failed to launch Tool“. Sie sind keine fehlgeschlagenen Projekttests. Bereits im Referenzbericht dokumentierte Startmeldungen `LogAutomationTest: Error: Condition failed` werden separat gezählt und nicht zu iOS-Warnungen umetikettiert. Die finalen Editor06/07/08-Protokolle enthalten jeweils dieselben 17 Frame-0-Startmeldungen; ihre Ursache bleibt ungeklärt. Native Spielprozesse enthalten 58 Python-Fehlerzeilen aus den experimentellen Engine-Toolsets (`AgentSkill`, `ToolsetDefinition`, `PythonTestRunner`); exakt derselbe Befund steht im alten `PokemonHabitatsV2/Functional01/Engine.log`. Beide Befunde bleiben ausdrücklich sichtbare externe bzw. ungeklärte Startprobleme. Kein neuer Fatalfehler, keine Assertion, kein GPU-Crash und kein fehlgeschlagenes Materialkompilat in den geprüften Abschlussläufen. Einzelne Epic-Telemetrie-/Netzwerkwarnungen sind keine funktionalen Testfehler. `LogReview.json` enthält die Zählung.

Die rote Precomputed-Visibility-Anzeige aus der bestehenden Nutzerkonfiguration und die bekannte Messinstrumentierungswarnung zu vielen `FindConsoleObject`-Abfragen werden nicht durch Änderungen geschützter Einstellungen verdeckt.


### Aktueller Wasser-Nachtest

`WaterGameplay02`, aktueller Build13: **bestanden, Prozess-Exit 0, 112,5 Sekunden**. Normale Bewegung hält den Spieler bei X ≈ −188,1 cm vor dem Teich auf. Reguläre Ansprache startet Karpador-ClassicBattle; zwei normale Kratzer, ein normaler Fangversuch, echte Übernahme auf Platz 4. Keine Manipulation von Fangwahrscheinlichkeit, KP, AP oder Ballvorrat. Vollständige Instanzdaten einschließlich verbrauchter AP bestehen danach den Save/Load-Rundlauf im isolierten Testslot. Garados erreicht sieben Bewegungspläne und 30,25 m Schwimmstrecke; alle sekündlichen Wasserstichproben prüfen Eintauchtiefe und elliptische Körpergrenze.

Die Ufer-Fangprüfung verwendet ausdrücklich eine **technische, isolierte Interaktionsvorbereitung**: Nur der vorhandene Karpador-Wildactor wird auf einen vom gemeinsamen Planer geprüften Uferpunkt gesetzt und für die Ansprache angehalten. Dies beweist die reguläre Interaktion, Kampf- und Fangverarbeitung; es wird nicht als zufällig natürlich erreichter Uferkontakt ausgegeben. Natürliche Bewegung beider Wasserarten wurde separat in Functional05 und PIEFunctional02 beobachtet; im kurzen Vorlauf des Fangtests bewegte sich Karpador noch nicht. Garados bleibt während dieses Tests in seiner normalen Simulation.

`WaterInteractionPIE03` auf der endgültigen Map: **bestanden**, 8,80 Sekunden. Reguläre Karpador- und Garados-Uferherausforderung aus etwa 148 bzw. 303 cm Mittelpunktabstand, beide ClassicBattles mit normaler Flucht und korrekter Rückkehr/Clock-Freigabe. Explizite technische Uferfixtures, keine veränderte Fang-/Kampf-/Kollisionsregel. `WaterInteractionPIE01` wurde zuvor korrekt abgewiesen: Die erste Karpador-Fixture belegte noch Garados’ Zielpunkt. Nach Verlegung auf einen anderen vom bestehenden Planer freigegebenen Punkt besteht derselbe Test ohne Lockerung der Freiraumprüfung.

## 7. Performance und Bildnachweise

Unveränderte Grafikbasis: QHD-Ausgabe 2560 × 1440, Profil C, High, 75 % Screen Percentage, TAAU, Software-Lumen + IFG, VSM4. Keine Videoaufnahme bei den Messungen. Kurzer Funktionalitäts-/Kostenvergleich in drei frisch gestarteten Development-Spielprozessen, ohne Video oder Screenshots während der Messfenster: je Standort ein 15-Sekunden-Fenster mit und eines ohne verwaltete Wildpopulation, vorher 12 Sekunden Warm-up plus Prozess-/Shader-Vorlauf. Dorf und Wald mit Enhanced-Input-Bewegung, Teich stationär; Weltuhr, Sonne, NPCs und Begleiter aktiv. Reihenfolge Dorf an/aus, Wald aus/an, Teich an/aus. **6 gültige Fenster, 3.297 Frames**, jedes auf Vordergrundfokus, Ausgabe 2560 × 1440, tatsächliche interne 1920 × 1080, effektives AA-Verfahren 2/TAAU, Upsampling 1, High 2, normale Kamera −50°/−45°/35° geprüft. Keine ausgeschlossenen oder selektiv entfernten Frames.

| Standort / Population | FPS Ø | GPU ms Ø | Game ms Ø | Render ms Ø | Frame-p95 ms | 1-%-Low FPS | Max. Frame ms | Population |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Dorf / aus | 37,10 | 26,13 | 2,17 | 26,95 | 29,08 | 31,78 | 33,11 | 0–0 |
| Dorf / an | 37,01 | 26,18 | 2,42 | 26,95 | 29,29 | 26,51 | 68,19 | 8–8 |
| Wald / aus | 32,71 | 30,30 | 2,42 | 30,48 | 33,67 | 22,14 | 75,36 | 0–0 |
| Wald / an | 29,74 | 33,38 | 2,49 | 33,60 | 41,63 | 14,39 | 83,51 | 7–10 |
| Teich / aus | 39,00 | 24,90 | 1,55 | 25,64 | 29,35 | 30,12 | 41,41 | 0–0 |
| Teich / an | 44,30 | 21,73 | 1,85 | 22,49 | 24,48 | 30,53 | 74,08 | 8–8 |

Der an/aus-Vergleich ist **kein isolierter KI-Benchmark**: Er verändert auch Geometrie, Animation, Sichtbarkeit und Schatten der Pokémon. Im Dorf beträgt die Differenz der GPU-Mittelwerte nur +0,05 ms, im Wald +3,08 ms. Am Teich ist die Reihenfolge sogar umgekehrt (an 21,73 / aus 24,90 ms), weshalb daraus keine negative Populationslast oder verlässliche Ersparnis abgeleitet wird. Der vorherige kurze Teichcheck hatte 36,48 / 37,39 FPS ergeben; die Unterschiede zeigen die Grenzen dieser kurzen Einzelmessungen. Ein Rendering-Optimierungsgewinn wird daraus nicht behauptet.

Gemessene akkumulierte Arbeit aller natürlichen Bewegungskomponenten: 4,32 / 6,45 / 7,42 ms pro realer Sekunde an Dorf/Wald/Teich; keine pauschale Gleichsetzung mit der gesamten CPU- oder Spawn-Arbeit.
Die Fenster sind ein kurzer Kostencheck, keine belastbare mehrfache Performance-Freigabe. Insbesondere im Wald **keine stabilen 30 FPS**, p95 41,63 ms und seltene Spitzen bis 83,51 ms. Auch ein Dorfmittel von 37 FPS beweist keine langfristig stabile Ausgabe. Historische Beleuchtungsmessungen mit anderen Populationen, längeren Abläufen und anderem Zustand sind kein kausaler Vorher-/Nachher-Vergleich dieser Umsetzung. Keine Rendering- oder Grafikqualitätsänderung wurde dafür übernommen.

Rohdaten: `BenchmarkVillage`, `BenchmarkForest`, `BenchmarkPond03` unter dem auftragseigenen Saved-Verzeichnis; Auswertung `PerformanceCombined.json` mit validierten Einzelbildern, GPU-Pässen, KI-Stichproben und Profilwerten..

Echte Unreal-Aufnahmen liegen ausschließlich unter `Saved/ProjectRefinement/VisualV2PokemonWaterTeamV1/`. Native Spielaufnahmen sind QHD; eingebettete PIE-Aufnahmen enthalten auch die Editoroberfläche und werden nicht als QHD-Spielviewport ausgegeben. Keine generierten Nachweisbilder und keine umfangreichen Bildfolgen.

| Nachweis | Datei unter dem Saved-Auftragsverzeichnis |
|---|---|
| Natürliches Dorf-Pikachu | `WildViews01/Village.png` |
| Natürliches Wiesen-Bisasam, Glumanda-Begleiter und normales Testteam | `WildViews01/Meadow.png` |
| Natürliches Wald-Pikachu | `WildViews01/Forest.png` |
| Teich, natürlicher Garados und Karpador, normale Kamera | `PondViews03/PondView0.png`, `PondViews03/PondView1.png` |
| Regulärer Karpador-Kampf vom Ufer | `WaterGameplay02/WaterClassicBattle.png` |
| Beide Uferkämpfe in PIE, technische Vorbereitung gekennzeichnet | `WaterInteractionPIE03/Karpador.png`, `WaterInteractionPIE03/Garados.png` |
| Kontrollierter Pikachu-Modellbesuch | `Functional05/Model_Pikachu.png` |
| Innenraum, Landkampf, Begleiter nach Fang und Teamsortierung | `Functional05/C_Interior.png`, `C_ClassicBattle.png`, `C_CompanionAfterCapture.png`, `C_SwitchedCompanion.png` |
| Zusammenhängender Fußlauf, Brücke und Tageszeiten | `WorldFootwalk01/Walk_2.png`, `Walk_6.png`, `Walk_10.png`, `Walk_14.png`, `Walk_18.png`, `Walk_23.png` |

Die Habitatbilder verwenden wirkliche verwaltete Wildactors mit aktiver KI, keine Modellgelände-Exemplare. Teleports dienen dort ausschließlich der Fotopositionierung; der Fußlauf ist separat ohne Streckenteleports protokolliert. Die frühere goldene Überlagerung ist in `PondViews01`, die Ausschlussdiagnosen in `PondReflection01` und `PondOverlap01` erhalten. Diese Diagnosebilder sind kein Endstand.

## 8. Grenzen und Abschluss

Die Beckenform bleibt eine gezielt begrenzte stilisierte Teichgestaltung; die elliptische Kontur und der geradlinige vorhandene Bacheinlauf sind aus der Spielkamera erkennbar. Das ist keine vollständige landschaftliche Neugestaltung. Kein Unterwasserspiel, keine Spieler-Schwimmfunktion, keine neuen Modelle/Animationen oder Arten. Individuelle Wildpositionen werden wie bisher nicht als neue Persistenzstruktur gespeichert; Fang-/Siegkennungen und Pokémon-Instanzen nutzen das vorhandene System. Das Modellgelände ist eine kontrollierte Vorführung und keine natürliche Population.

Andere Maps, originale Modell-/Blenderquellen, Renderingprofile, Weltuhr, Kampfregeln und Nutzerspielstände werden nicht umgestellt. Die aktuelle DefaultEngine.ini bleibt ausdrücklich eine vorhandene, nicht mitzucommittende Nutzeränderung.

Änderungssatz: eigene Habitat-/Wasseranbindung, vorhandene VisualV2, abgeleitete Beckenquellen und Assets, begrenzte Authoring-Werkzeuge, Assertions und dieser Bericht. Nutzeränderung `Config/DefaultEngine.ini` und die 34 fremden unversionierten Dateien bleiben ausgeschlossen. Ausgangscommit und live abgefragtes `origin/main` vor Abschluss: `4cf2a6f393ded35c1b2f2ac03b78d8584d818ff0`. Der geprüfte Commit und die anschließende Remote-/LFS-Verifikation werden in der Abschlussmeldung sowie `Saved/ProjectRefinement/VisualV2PokemonWaterTeamV1/GitFinal.json` festgehalten; kein zusätzlicher Dokumentationscommit nur zum Eintragen der eigenen Commit-ID.
