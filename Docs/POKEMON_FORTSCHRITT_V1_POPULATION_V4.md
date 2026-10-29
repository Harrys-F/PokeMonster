# Pokémon-Fortschritt V1 und VisualV2-Population V4

Abschlussprüfung vom 29.10.2026, Ausgangscommit `b0ffa238`. Die nachfolgend bezeichneten Abschlussläufe sind bestanden: Editor-Build, 292 Automationstests, zwölf Map Checks, PIE und separater Development-Spielprozess. Strenger QA-Wrapper: Exit 0. Das Populationsmaximum beträgt 14; stabile 30 FPS bleiben ausdrücklich unbewiesen. Der Abschlusscommit wird über die Git-Historie und die Abschlussmeldung identifiziert.

## Vorhandene Architektur und gezielte Ergänzungen

Es existieren bereits `CreatureSpeciesData`, `CreatureInstance`, `CreatureProgression`, `BattleSession`, `BattlePresenter`/`BattleWidget`, `EncounterSubsystem`, das persönliche Repertoire, der Meisterdienst und Save-Schema 10. Diese Systeme werden erhalten. Keine zweite Fortschritts-, Kampf-, Speicher-, Namens- oder KI-Verwaltung.

| Bereich | Bereits vorhanden / erhalten | Ergänzung dieses Auftrags |
|---|---|---|
| EP | Artbezogener Ertrag, Gegnerlevel, lebende Kampfteilnehmer, Trainerfaktor | Meldung nennt den tatsächlichen Empfänger, auch ausgewechselte Teilnehmer |
| Level | Kumulative EP, mehrere Aufstiege, Deckel 100, negative/inkonsistente Eingaben atomar abweisen | Gezielte Prüfung des vorhandenen echten Testteams |
| Werte | Sechs Werte aus Artbasis und Level | Keine stillschweigende neue IV-/EV- oder Werte-Migration |
| Lernen | Bestehende LevelUpMoves, freie Slots, vier aktive Slots, Ersatz/Ablehnen, persistente Angebote | Vorhandene Abläufe zusätzlich im Gameplay prüfen |
| Repertoire | Tatsächlich erlernte Attacken behalten; AP pro Individuum/Attacke | Keine freie Neuordnung außerhalb des Meisters |
| Entwicklung | Vollständige Glumanda–Glutexo–Glurak-Sequenz V2.1, Abbruch, Modellprüfung | Optionale Tageszeitfenster im vorhandenen Bedingungsprüfer |
| Population | Tatsächlich zehn Zonen / 14 kuratierte Kandidaten / 18 unabhängige Modelle | VisualV2-Zielmaximum 14; sechs gleichzeitige Arten bleiben erhalten |
| Namen | Bounds-Anker, vorhandene Arten-/Wild-/Modellquellen | Gemeinsames UI-Overlay in vorhandener Oberwelt-UI, einschließlich aktivem Begleiter |

## EP, Kurven und Werte

Die vorhandene Kampftransaktion vergibt ganzzahlig `Art-Ertrag × Gegnerlevel / 7 / Anzahl lebender Teilnehmer`; danach gilt bei Trainerkämpfen der vorhandene Faktor `3/2` mit den bestehenden Integer-Rundungen. Unbeteiligte oder kampfunfähige Mitglieder bekommen keine EP. Fang/Flucht wird nicht zu einem K.O.-Sieg umdefiniert. Empfänger werden für die Anzeige anhand der individuellen Ereignis-ID ermittelt.

Fast, MediumFast, MediumSlow und Slow sowie die bereits technisch vorhandenen zusätzlichen Kurven Erratic/Fluctuating bleiben unterstützt. Kumulative Levelgrenzen sind die einzige Berechnungsgrundlage der bestehenden EP-Balken. Level 1 startet bei null, Level 100 endet an seiner Kurvengrenze; übergroße Vergaben werden überlaufsicher begrenzt. Die historischen Glumanda-Daten, ihre Wachstumskurve und bestehende individuelle Überschreibungen bleiben aus Save-Kompatibilität erhalten. Keine erfundenen Originaldaten oder verdeckte Balancingänderung.

Die ausdrücklich bestehende vereinfachte Individualberechnung bleibt: KP = `floor(2 × BasisKP × Level / 100) + Level + 10`; übrige Werte = `floor(2 × Basiswert × Level / 100) + 5`. Separate IVs/EVs/Wesen sind bisher nicht implementiert. Fehlende KP bleiben beim Aufstieg erhalten, K.O. bleibt K.O.; es gibt keine automatische Vollheilung. Kampfmodifikatoren bleiben Sache der vorhandenen BattleSession.

## Lernen, Attackenverwaltung und Speichern

Die vorhandenen geprüften Lernlisten und Attackenassets bleiben unverändert. Freie Slots werden nach bestehender V1-Regel unmittelbar gefüllt. Volle Sets erzeugen sortierte, deduplizierte Entscheidungen; Annahme ersetzt genau einen Slot, Ablehnen nur das aktuelle Angebot. Ersetzte Attacken bleiben im persönlichen Repertoire, offene/abgelehnte Angebote werden nicht als erlernt erfunden. Neuordnung bleibt ortsgebunden beim Meister, das normale Pokémon-Menü reine Ansicht. AP anderer Attacken bleiben erhalten; Wiederaktivieren übernimmt verbrauchte AP aus dem Repertoire.

Save-Version 10 wird nicht geändert. Identität, Gesamt-EP, Level, Status, aktive Slots, Repertoire/AP, offene Angebote, Entwicklungsmetadaten, Team, Inventar, Position, Innenraum, Kontrollpunkt und Weltzeit verwenden weiter den bestehenden Transport. Tests verwenden eigene UserDir-Spielstände beziehungsweise isolierte PIE-Slots. Originalspielstände werden per SHA-256 geprüft.

## Entwicklungsvorbereitung und bestehende Sequenz

Die bereits funktionierenden Entwicklungen 16 → Glutexo und 36 → Glurak bleiben spielbar. Der Auftrag setzt diese nicht auf einen früheren vorbereiteten Stand zurück. Angebote werden nach Kampf-/Lernabschluss behandelt, fehlende Modelle blockieren sicher. Die Instanz bleibt erhalten, K.O./AP werden nicht geheilt, Zwischenformen nicht übersprungen.

Die vorhandenen Bedingungen Level, Item, Freundschaft, Ort und besondere Handlung erhalten optional `RequiredStartMinute`/`RequiredEndMinute`: halboffene Minutenfenster, auch über Mitternacht. Beide −1 deaktivieren die neue Zusatzbedingung. Bei benötigtem, aber unbekanntem Zeitpunkt oder ungültigem Fenster wird abgewiesen. Das bestehende EncounterSubsystem liefert Minuten aus der zentralen Weltuhr. Save-Metadaten prüfen ein grundsätzlich mögliches Angebot; tatsächliches Anbieten/Bestätigen prüft die aktuelle Zeit. Keine bestehende Art erhält eine Zeitbedingung. Die Beispiel-Nachtzeiten im Test sind ausschließlich technische Fixtures, keine neue artspezifische Regel. Ehemalige Tauschentwicklungen erhalten keine erfundenen Mindestlevel, Items, Orte oder Prüfungen.

## Population und Verteilung

Es werden vorhandene Konfigurationszonen verwendet, ohne Map-Neuspeicherung. Globales VisualV2-Limit 14; sechs Arten. WestMeadow, WestForest und EastForest erhalten lokal höchstens drei Individuen. Artweit: Bisasam/Pikachu vier, Myrapla/Raupy/Hornliu drei, Glumanda/Enton zwei. Vier Exemplare einer Art müssen über mehrere Zonen verteilt sein. Die übrigen Regeln, Wasserreservierungen, Temperamente, Tagesrhythmen und Kampf-/Fangdaten bleiben erhalten.

Ein bloßes globales Limit 14 reichte bei der ursprünglichen Auswahl von zwei Einzelarten nicht: Der erste echte Lauf belegte weiter nur zehn Plätze. Die angepassten artweiten Maxima beseitigen diese nachgewiesene Budgetlücke. Das Limit erzwingt weiterhin keine ungeeigneten Spawns; Art-, Zonen-, Abstands-, Hindernis-, Kamera- und Tageszeitregeln gelten gemeinsam. Tatsächliche beobachtete Zahlen folgen unten.

Karpador und Garados nutzen ausschließlich das bestehende Wasserhabitat. Teichabmessungen, Tiefe, 4,06-m-Trennstreifen zum Bach, Mediengrenzen, Uferinteraktionen und Schwimmclips bleiben unverändert. Alle 18 Modelltest-Registrierungen sind unabhängig von der Wildpopulation. `pm.TestGround.List`, `pm.TestGround.Go Pikachu`, `pm.TestGround.Return` bleiben erhalten.

## Dauerhafte Namen im Kamerabild

`pm.WildNames 1` ist Standard; `pm.WildNames 0` blendet sämtliche Pokémon-Namen einschließlich Modellschildern und aktivem Begleiter aus. Ein reiner Interaktionspfeil darf bestehen bleiben. `pm.WildNames.Distance` bleibt nur als wirkungslose Kompatibilitätsvariable; kein Entfernungslimit.

Die vorhandene Oberwelt-UI projiziert den tatsächlichen Mesh-Bounds-Anker über der Welt. Keine Sichtlinie, Tiefenprüfung oder Sichtbarkeitsgrenze durch Vegetation, Gebäude oder Abstand. Ein Pokémon muss tatsächlich aktiv und mit seinem Körper im Kamerabild sein; noch nicht gespawnte, entfernte oder kampfseitig unterdrückte Exemplare liefern keinen Namen. Große sichtbare Körper behalten am Bildrand einen geklemmten Namen, auch wenn der Kopfanker außerhalb liegt. Bestehende 3D-Schilder werden unterdrückt, sodass kein zweiter Text gezeichnet wird. Modell- und Wild-/Begleiternamen teilen denselben UI-Zeichenweg und die vorhandene Schriftgestaltung.

Ein kleiner wiederverwendeter Textblock-Pool vermeidet laufende Widget-Erzeugung. Namen folgen pro UI-Frame ihrer Quelle; die Anordnung verschiebt nahe Beschriftungen vertikal, statt Namen wegzufiltern. Bei extrem kleinen/überfüllten Viewports ist perfekte Kollisionsfreiheit nicht garantiert; kein Name wird deshalb absichtlich verworfen. Menüs und Kampfpräsentation verdecken die Weltbeschriftungen regulär.

## Performance – tatsächliche Messwerte

Separater Development-Spielprozess (`UnrealEditor -game`), keine Videoaufnahme. 2560 × 1440 Ausgabe, **pro Frame nachgewiesen 1920 × 1080 intern**, High/75 %/TAAU, Software-Lumen/IFG, vier VSM-Strahlen, 75° Mittag. VSync/FPS-Limit aus; acht Sekunden Aufwärmen, jeweils drei 15-Sekunden-Messfenster pro Zustand, wechselnde Reihenfolge. Weltuhr, Beleuchtung, NPCs, Pokémon-KI und regulärer Begleiter bleiben aktiv. Insgesamt **30 gültige Fenster / 17.597 Frames**; sämtliche Frames auf aktive Fensterlage, Grafikwerte und normale Kamera geprüft. Thermal-/Stromprotokolle liegen neben den Rohdaten.

### Kontrollierter 10-/12-/14-Vergleich

Technischer Dichteaufbau im vorhandenen WestMeadow, jeweils genau hälftig Bisasam/Raupy mit tatsächlichen Actors, Modellen, KI und Bewegungsplaner. Nur für diese Messung gelten höhere lokale Art-/Zonenkapazitäten im Arbeitsspeicher; keine neuen Arten oder gespeicherten Konfigurationen. Spawnvorbereitung und Positionsanordnung liegen außerhalb der Messfenster. Die regulären Lebensraumregeln werden nicht als solche dargestellt. Ein vorheriger Versuch `Density01` erreichte bei einer erneuten 14er-Vorbereitung nur 13 Plätze und wurde abgebrochen; seine Daten dienen nicht dem Abschlussvergleich. Der korrigierte Aufbau lässt Kamera-Lag und Kollisionsfreigabe normale Frames verarbeiten, statt 50 Neubesiedlungen im selben Frame zu erzwingen. `Density02` besteht vollständig, einschließlich Rücksetzung der temporären Konfiguration.

| Wildzahl | Namen | FPS Ø | GPU ms | Game ms | Render ms | Frame-p95 ms | 1-%-Low FPS |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | aus | 46.56 | 20.44 | 2.27 | 21.55 | 23.57 | 36.21 |
| 10 | ein | 42.31 | 22.48 | 2.51 | 23.62 | 26.55 | 33.78 |
| 12 | aus | 42.43 | 22.41 | 2.41 | 23.55 | 25.86 | 29.91 |
| 12 | ein | 45.97 | 20.72 | 2.61 | 21.85 | 24.14 | 36.95 |
| 14 | aus | 44.65 | 21.41 | 2.37 | 22.49 | 25.82 | 36.06 |
| 14 | ein | 42.78 | 22.30 | 2.67 | 23.38 | 26.60 | 35.35 |

Alle angegebenen Wildzahlen waren innerhalb jedes zugehörigen Messfensters exakt belegt. Sichtbare bzw. kürzlich gerenderte Modelle variieren durch reale Bewegung und den Kamerarand (bei 14: 12–14). Mit Namen wurden bis zu 14 gleichzeitige Beschriftungen gemessen, einschließlich des Begleiters, falls im Bild. Ausgeschaltet bleiben null Namen; ein einzelner reiner Fokus-Pfeil ist möglich. Diese Werte sind kein Beweis, dass alle 14 Modelle ständig gleichzeitig im Kamerabild waren.

Der Game Thread kostet mit Namen in diesen Paaren zusätzlich etwa **0,20–0,30 ms**. Die GPU-Differenzen ändern ihr Vorzeichen; wegen Bewegung, sichtbarer Modellzahl und Messschwankungen wird kein verlässlicher isolierter GPU-Preis der Namen behauptet. Der 14er-Zustand zeigt keine erhebliche Verschlechterung gegenüber zehn bzw. zwölf. Daher bleibt das ausdrücklich gewünschte globale Maximum **14** erhalten, bei kleinen lokalen Zonen und sechs Arten.

| Wildzahl, Namen ein | Gesamte KI-Komponenten ms pro Echtsekunde | Davon Planung ms pro Echtsekunde | Planaufrufe pro Sekunde |
|---:|---:|---:|---:|
| 10 | 8.163 | 0.540 | 1.51 |
| 12 | 11.876 | 0.475 | 1.74 |
| 14 | 11.646 | 0.438 | 2.02 |

Die neue Planungszeit ist ein standardmäßig abgeschalteter Unterzähler der bereits vorhandenen opt-in KI-Zeitmessung, einschließlich gescheiterter lokaler Oberflächen-/Pfadversuche. Die Planung ist hier **Teil** der KI-Zeit und wird nicht hinzuaddiert. Normalbetrieb aktiviert keinen dauerhaften Profiler. Actor-/Animations-/UI-Arbeit außerhalb der Roaming-Komponente ist zusätzlich in den allgemeinen Threadzeiten enthalten.

### Bewegtes reguläres Gameplay

Gleiche vorhandene Dorf-/Waldrouten, normale Kamera, etwa 33,3 Meter tatsächlicher Fußweg je Fenster, keine Streckenteleports während der Messung. Die Null-Wild-Kontrolle schaltet nur die vorhandene Population aus; NPCs, Team, Begleiter, Weltuhr und Beleuchtung bleiben aktiv.

| Ort | Natürliche Wildpopulation | FPS Ø | GPU ms | Game ms | Render ms | Frame-p95 ms | 1-%-Low FPS |
|---|---|---:|---:|---:|---:|---:|---:|
| Wald | 0 | 31.04 | 31.34 | 2.36 | 32.20 | 36.27 | 24.33 |
| Wald | 4–12 | 30.90 | 31.46 | 2.63 | 32.34 | 38.65 | 17.28 |
| Dorf | 0 | 32.72 | 29.64 | 2.28 | 30.56 | 33.36 | 27.18 |
| Dorf | 5–13 | 31.74 | 30.61 | 2.76 | 31.47 | 39.53 | 19.96 |

**Stabile 30 FPS sind weiterhin nicht nachgewiesen.** Die Mittelwerte der lebenden Welt erreichen 31,74 FPS im Dorf und 30,90 FPS im Wald, ihre p95 liegt aber über 33,3 ms. Einzelne Frames erreichen 99,57 bzw. 102,31 ms. Die alten Referenzen 31,37/26,15 FPS sind keine neue identische Vorhermessung; daraus wird kein bewiesener Performancegewinn abgeleitet. Es wurde keine Grafikqualität reduziert.

Im Dorf erreicht die gemessene Game-Thread-Spitze 98,26 ms, die GPU 52,18 ms; im Wald sind es 10,09 bzw. 50,48 ms. Ohne korrelierten CPU-/GPU-Trace ist damit keine eindeutige Ursache jedes Frameausreißers belegt. Weitere gezielte Spitzenanalyse bleibt offen; die lokale Planung ist in diesen Messfenstern kein großer Dauerverbraucher.

Frame-p95 und 1-%-Low in den Tabellen sind Mittelwerte der drei Fensterstatistiken, keine nachträglich behauptete globale Quantile. Einzelstatistiken, Maxima und 1-%-Low-Definition (Kehrwert der mittleren langsamsten ein Prozent der Frames) stehen in `Performance.json`, unveränderte Roh-CSV unter den jeweiligen UserDir-Ausgaben. Weniger sichtbare Modelle, andere Arten und andere Gelände dürfen nicht mit dem kontrollierten Dichteaufbau gleichgesetzt werden.

## Tatsächlich geladene Fortschrittsdaten

Die Bestandsaufnahme im separaten Spielprozess erfasst alle 18 registrierten Arten und **154 bereits gebundene Level-Lerneinträge**. Keine neue Attacke, Levelanforderung oder Artzuordnung wurde erfunden. Vollständige exportierte Basiswerte, Lern- und Entwicklungslisten stehen in `Saved/ProjectRefinement/ProgressionPopulationV4/NativeFunctional01/Result.json`.

| Art | Vorhandene Kurve | EP-Ertrag | Lerneinträge |
|---|---|---:|---:|
| Bisasam | MEDIUM_SLOW | 64 | 11 |
| Glutexo | MEDIUM_SLOW | 142 | 11 |
| Glurak | MEDIUM_SLOW | 209 | 13 |
| Schiggy | MEDIUM_SLOW | 66 | 11 |
| Raupy | MEDIUM_FAST | 53 | 2 |
| Smettbo | MEDIUM_FAST | 160 | 10 |
| Hornliu | MEDIUM_FAST | 52 | 2 |
| Bibor | MEDIUM_FAST | 159 | 8 |
| Habitak | MEDIUM_FAST | 58 | 8 |
| Pikachu | MEDIUM_FAST | 82 | 11 |
| Myrapla | MEDIUM_SLOW | 78 | 8 |
| Enton | MEDIUM_FAST | 80 | 8 |
| Machomei | MEDIUM_SLOW | 193 | 11 |
| Nebulak | MEDIUM_SLOW | 95 | 9 |
| Gengar | MEDIUM_SLOW | 190 | 10 |
| Karpador | SLOW | 20 | 3 |
| Garados | SLOW | 214 | 8 |
| Glumanda | MEDIUM_FAST | 65 | 10 |

Fast ist technisch unterstützt und automatisiert geprüft, aber keiner dieser 18 Arten zugeordnet. Glumanda bleibt ausdrücklich bei der historischen MediumFast-Konfiguration und seinen bestehenden Basiswerten (46/58/42/60/45/56); keine stillschweigende Datenmigration. Weiterentwickelte bestehende Individuen behalten ihre gespeicherte Kurvenüberschreibung.


## Tatsächlich beobachtete Verteilung und KI

Der reguläre Anfangszustand in `NativeFunctional01` und `PIEFunctional01` enthält zwölf Individuen aus sechs Arten in allen zehn vorhandenen Zonen. Die Tabelle beschreibt diesen echten Lauf, keine garantierte dauerhafte Belegung:

| Vorhandene Zone | Lokales Maximum | Beobachtet im Anfangszustand |
|---|---:|---|
| WestVillageEdge | 1 | Pikachu |
| WestMeadow | 3 | Bisasam |
| WestForest | 3 | Pikachu |
| NorthGlade | 1 | Bisasam |
| ForestEdge | 2 | Bisasam, Pikachu |
| EastForest | 3 | Pikachu |
| PondShore | 1 | Enton |
| RockSteps | 1 | Glumanda |
| SouthMeadow | 2 | Bisasam |
| PondWater | 2 | Karpador, Garados |

Die interne historische Glumanda-ID `Zunderlauf` bleibt zur Save-/Assetkompatibilität erhalten; der Spieler sieht Glumanda. Der zusammenhängende Fußlauf erreicht natürlich bis zu zwölf Individuen, die bewegten Benchmarkfenster bis zu 13 im Dorf. Vierzehn ist eine Obergrenze, kein erzwungener Mindestbestand. Tageszeit, Artenauswahl und sichere Spawnplätze können Plätze frei lassen. Die 14er-Auslastung wurde zusätzlich gezielt im bezeichneten Dichtetest nachgewiesen.

Bestehende KI-V3-Spielerwahrnehmung, Reaktionen, Tagesrhythmen, gegenseitige Sozialreservierungen, Distanzreduktion und begrenzte Bewegungsplanung bleiben bestehen. Der Fußlauf umfasst 32 Wegpunkte und 368,30 Meter ohne Routenteleport. Protokolliert werden unter anderem Wandern, Ruhen, Schlafen und Nahrungssuche; gültige gegenseitige Reservierungen werden geprüft. Es wird keine neue Social- oder Navigationsarchitektur eingeführt. Wasserbewegung wird gesondert beobachtet: Garados legt im Wasserlauf 38,99 Meter mit sieben Bewegungsplanungen zurück. Ein aus einem isolierten Fixture an den erreichbaren Uferbereich gesetztes Karpador verwendet anschließend die normalen Interaktions-, ClassicBattle-, Fang- und Teamfunktionen; der Test umgeht nicht deren Zulässigkeitsprüfung. Diese Vorbereitung wird nicht als zufällige natürliche Begegnung ausgegeben.

## Technische und spielbare Abschlussprüfungen

Alle Nachweise liegen unter `Saved/ProjectRefinement/ProgressionPopulationV4/`, sofern nicht anders angegeben. Tests verwenden eigene Testspielstände, keinen produktiven Nutzerslot.

| Prüfung | Tatsächlich ausgeführt | Ergebnis / Nachweis |
|---|---|---|
| Editor-Build | Finale geänderte C++-Quellen, UE 5.8.2 / Mac | Exit 0, 13,66 s; `../ProgressionPopulationV4Build06/Result.json` |
| Strenge Automation | Gesamter vorhandener PokeMonster-Umfang einschließlich drei neuer Tests | **292 bestanden, 0 mit Warnungen, 0 fehlgeschlagen, 0 offen; Wrapper Exit 0**; `StrictQASummary.json`, `../ProgressionPopulationV4Automation02/Result.json` |
| Neue Automation | ScreenNameLayout, RealTeamProgressionAndRewards, OptionalEvolutionTimeWindow | 18 gleichzeitige Layoutnamen, Randanker, 14/6-Konfiguration; drei echte Teamarten mit Schwellen/KP/AP/Leveldeckel; aktive und ausgewechselte EP-Empfänger; exakte und um Mitternacht laufende Zeitfenster, fehlende/ungültige Zeit |
| Map Checks | Alle zwölf vorhandenen Projektmaps | Jeweils 0 Fehler / 0 Warnungen; `MapCheckResults.json` und Editor-Engine.log |
| Separates Gameplay | 76 Prüfschritte / 22 Assertions | Bestanden; `NativeFunctional01/Result.json` |
| PIE-Gameplay | Derselbe Ablauf mit 76 Prüfschritten / 22 Assertions | Bestanden; `PIEFunctional01/Result.json` |
| Fortschritt im Kampf | Je sechs Fälle im separaten Prozess und PIE | ClassicBattle und WorldBattle, freier Lernslot, Ersetzen, Ablehnen, Glumanda 15→16 mit Entwicklungsangebot und Abbruch, Save/Load nach jedem Fall; `Progression02/Result.json`, `PIEProgression01/Result.json` |
| Team und Begleiter | Reguläres Dreierteam, Fang erweitert Team, Slottausch über bestehendes Teammenü | Identitäten, KP/AP/Repertoire und aktiver Begleiter korrekt; in den beiden vollständigen Gameplayabläufen |
| Innenraum und Save/Load | Betreten, eigener Slot, Position/Blickrichtung, Kamera, Weltzeit, Team und Kontrollpunkt | Bestanden, Rückweg und Außenkamera wiederhergestellt |
| Wasser | Sieben Fälle einschließlich Uferkollision, regulärem Karpador-Kampf/Fang, Teamplatz 4, Save/Load | Bestanden; `WaterGameplay01/Result.json` |
| Welt-Fußlauf | 32 Wegpunkte, 368,30 m tatsächliche Bewegung, kein Routenteleport | Bestanden; `WorldFootwalk01/Result.json` |
| Mapwechsel | VisualV2 → vorhandene Dev_TestMap → VisualV2 | Team/IDs/KP/AP, Weltuhr, Software-Lumen/IFG, TAAU/75 %, Begleiter erhalten; `Travel01/Result.json` |
| Tageszeiten | Morgen, Tag, Dämmerung, Nacht, Mitternacht/Tageszähler | Bestehende Uhr-/Lichtreaktionen, Dialog-/Kampf-/Menüpause korrekt, KI-Reservierungen gültig |
| Controller-Software | Acht Richtungen, Sprint an/aus, Schnell-/Hauptmenü, B/A, X, Steuerkreuz, L/R und Plus gemäß vorhandener Belegung | Bestanden; `PIECycles01/movement/Result.json`; keine erneute physische Controllerabnahme behauptet |
| Rendering-Profilwechsel | HardwareSPG, 100, C und neue PIE-Welten | Referenz wiederherstellbar, C am Ende Software-Lumen/IFG / TAAU / 75 %; `EditorRestored.json` |
| PIE-Stabilität | Vier Start-/Stopp-Zyklen, darunter vollständiges Gameplay, Fortschritt, Eingaben und Tagesphasen | Bestanden, Editor regulär geschlossen, keine ungespeicherten Maps/Assets; `EditorQAFinal.json` |
| Namen | Dorf, Wiese, Wald, beide Fische, verdeckender Fels, Bildrand, größere Entfernung, Ein/Aus und Modelltest | Bestanden; `Names11/Result.json`; echte blockierende Sichtlinie zum Garados und dennoch sichtbares UI-Schild |
| Modelltestgelände | Alle 18 zentral registrierten Arten, kontrollierte Bewegung/Drehen/Reset und Rückkehr | Bestanden; während des Besuchs bleibt die vorhandene Speichersperre aktiv |
| Performance | 30 Messfenster / 17.597 Frames ohne Video | Auswertung und Grenzen oben; `Performance.json` |

### Wiederholte beziehungsweise zunächst fehlgeschlagene Prüfungen

Fehlgeschlagene Vorversuche sind erhalten und werden nicht als bestandene Abschlussläufe gezählt. Der erste Build deckte einen Unity-Build-Namenskonflikt des lokalen Temperament-Alias `T` auf; der lokale Bezeichner wurde ohne Verhaltensänderung umbenannt. Der finale Build 06 und die nachfolgenden Tests bestehen.

Frühe Namensprüfungen scheiterten an Python-Bindings, falschen Enum-Namen, Testkamera-/Kollisionsaufbau oder einer fehlerhaften Aufräumfunktion. Der eigene Prozess 95204 wurde nach Identitätsprüfung regulär über die macOS-Anwendungsbeendigung geschlossen, ohne Force Quit. Das ist kein nachgewiesener Engine-Absturz. `Names10` bestand die logischen Checks, hatte jedoch bei drei verzögert erzeugten Screenshots bereits den nächsten Testzustand; diese Bilder dienen nicht als Abschlussnachweis. `Names11` wartet nach der Aufnahme, bevor der Zustand weitergeschaltet wird, und liefert die bezeichneten korrekten Bilder.

`Progression01` erreichte die sechs Lern-/Kampffälle, scheiterte anschließend an einem nicht exportierten Python-Aufräumaufruf. `Progression02` und die PIE-Wiederholung verwenden die unterstützten Wege, bestätigen den Abbruchdialog und bestehen einschließlich unverändertem Eingabespielstand. `Density01` wurde vor dem nicht vollständig vorbereiteten 14er-Fenster abgebrochen; ausschließlich `Density02` wird für den Dichtevergleich verwendet.

### Warnungen und Loggrenzen

Der strenge Automation-Wrapper endet tatsächlich mit Exit 0. Dies bedeutet nicht, dass sämtliche separaten Engine-Startlogs warnungsfrei sind. In zehn erfolgreichen Gameplay-/Editorlogs gibt es keinen erfassten Fatal-/Assert-/Critical-Abbruch. Neun separate Spielstarts melden jedoch den bekannten experimentellen ToolsetRegistry-/`PythonTestRunner`-Importfehler; außerdem treten einzelne Startwarnungen zu CharacterMovement-Iterationsgrenzen und zur EnvPerf-Konsolenvariablensuche auf. Die Warnungen sind in `LogReview.json` getrennt gezählt; es wurde kein fremdes Engine-Plugin umgebaut.

Die externe iOS-Helfermeldung `idevice_id: Bad CPU type in executable` tritt in diesen zehn geprüften Abschlusslogs nicht auf. Daraus wird keine generelle Engine- oder Rosetta-Reparatur abgeleitet. Es erfolgte keine Installation oder Änderung dieses Helfers.

## Echte Unreal-QHD-Aufnahmen

Alle folgenden Bilder stammen aus Unreal und sind per PNG-Header als 2560 × 1440 bestätigt (`QHDProof.json`). Aufnahmen sind von den Benchmarkfenstern getrennt. Medien bleiben lokal unter Saved und werden nicht in Git hochgeladen.

| Inhalt | Aufnahme relativ zum Nachweisordner |
|---|---|
| Dorf / Wiese / Wald mit Namens-Overlay | `Names11/Village.png`, `Names11/Meadow.png`, `Names11/Forest.png` |
| Karpador und Garados | `Names11/Karpador.png`, `Names11/Garados.png` |
| Echte Verdeckung durch Kollisionsgeometrie, Name bleibt sichtbar | `Names11/OccludedOverlay.png` |
| Namensquelle in 29,21 m Abstand | `Names11/LongDistanceTechnicalZoom.png` — ausdrücklich technischer temporärer Kamera-Zoom, danach zurückgesetzt |
| Einheitliche Modelltest-Beschriftung | `Names11/TestGroundOverlay.png` |
| Levelaufstieg 6→7 / Glumanda 15→16 | `Progression02/Level_0.png`, `Progression02/Level_5.png` |
| Lernentscheidung bei vier Slots | `Progression02/Learning_1.png` |
| ClassicBattle / Innenraum | `NativeFunctional01/C_ClassicBattle.png`, `NativeFunctional01/C_Interior.png` |
| Technischer 14er-Dichteaufbau | `Density02/N14_Names1_R1_AfterBenchmark.png` |

Direkt öffnen: [Wald mit Namensanzeige](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ProgressionPopulationV4/Names11/Forest.png), [verdecktes Pokémon mit sichtbarem Namen](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ProgressionPopulationV4/Names11/OccludedOverlay.png), [Glumanda 15→16](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ProgressionPopulationV4/Progression02/Level_5.png), [Modelltestgelände](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ProgressionPopulationV4/Names11/TestGroundOverlay.png). Die Verdeckungsgeometrie und der technische Zoom sind ausschließlich ungespeicherte Laufzeitfixtures, keine Änderung der Map.

## Projektschutz, Änderungsumfang und Git

SHA-256-Kontrolle gegen den vor Beginn erfassten Zustand: **6.406 ursprüngliche Dateien geprüft, darunter 504 vorhandene Spielstände und 34 geschützte unversionierte Dateien; keine unerwartete Änderung**. Sämtliche Maps, Originalassets, Modelle, Animationen, Blenderquellen und geschützten Nutzerdateien bleiben unverändert. Die schon vorher vorhandene lokale Änderung an `Config/DefaultEngine.ini` wird unverändert erhalten und nicht gestaged. Backup-Verweise `backup/full-03492bd` und `refs/archive/pokemonster/full-backup-03492bd` bleiben auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`.

Nur die 22 eigenen geprüften Textdateien aus `CommitFiles.json` werden versioniert: vorhandene Fortschritts-/Präsentations-/Habitatquellen, der kleine gemeinsame Layouthelfer, drei Automationstests, Habitatkonfiguration und Dokumentation. Keine binären Assets oder neuen LFS-Objekte sind Teil dieses Auftrags. Rohmessungen, Medien und isolierte QA-Dateien verbleiben unter Saved. Nach regulärem Commit/Push werden lokales main, origin/main und der tatsächliche Remote-HEAD verglichen; das Ergebnis und der Commit stehen in der Abschlussmeldung.

## Verbleibende Einschränkungen

- Stabile 30 FPS sind nicht nachgewiesen; insbesondere Frame-p95 und einzelne CPU-/GPU-Spitzen bleiben offen. Der Dichtetest ist keine Garantie für jede Artkombination oder jeden zukünftigen Kartenausbau.
- Die neue Grenze 14 garantiert keine dauerhafte natürliche Vollbelegung. Die bestehenden Habitat-/Arten-/Sicherheitsregeln haben Vorrang.
- Extrem kleine oder überfüllte Viewports können Namensüberschneidungen erzeugen. Kein zulässiger Name wird zur Entzerrung absichtlich ausgeblendet; Menüs/Kampf verdecken das Welt-Overlay regulär.
- Nicht vorhandene IV-/EV-/Wesenwerte, fehlende zukünftige Entwicklungsmodelle und besondere Tausch-Ersatzprüfungen werden nicht erfunden. Zeitfenster sind vorbereitet, aber keiner bestehenden Art neu zugewiesen.
- Der Software-Controllercheck ersetzt keine neue Prüfung mit einem physisch angeschlossenen Controller. Die bestehende belegte Grundbelegung bleibt unverändert.
- Die allgemeine vollständige temporale IFG-Bildfreigabe aus dem Renderingauftrag wird durch diesen Fortschritts-/Populationstest nicht nachträglich behauptet.
