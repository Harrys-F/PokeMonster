# Dauerhaftes Pokémon-Testgelände V1 – Prüfbericht

Datum: 22.10.2026. Projekt ausschließlich `/Users/harry/Developer/PokeMonster`.
Ausgangspunkt: sauberes `main`, HEAD und direkt abgefragtes `origin/main`
`7f60c707f2b3806b933a66a8323d7fff506e4c44`. Unreal Engine 5.8.2 auf macOS.

## Ergebnis und Zugang

Das Gelände ist jetzt **bei jedem gewöhnlichen PIE-Start der bestehenden
`/Game/Maps/Dev_TestMap_VisualV2` automatisch verfügbar**. Es braucht weder
`Showcase.py` noch einen Automationstest oder einen besonderen Startparameter.
Die native Entwicklungsfunktion ist dauerhaft versioniert; ihre Actors entstehen
bewusst nur während PIE. Die gespeicherte Map muss dafür nicht überschrieben werden.

1. VisualV2 öffnen und normal **Play / Spielen** starten.
2. Einen gegebenenfalls bereits laufenden regulären Wildkampf, Dialog oder ein
   Menü normal beenden. Im Innenraum zuerst wieder hinausgehen.
3. In der Unreal-Konsole `pm.TestGround.Go` eingeben. Alternativ Shift+F1,
   Output-Log-Eingabe auf **Cmd** stellen, Befehl ausführen, zurück in den
   Spielviewport klicken. **Nicht** als Python-Code eingeben.
4. Mit der vorhandenen Steuerung erkunden; `pm.TestGround.Go 1` bis
   `pm.TestGround.Go 10` bringen die Figur zum jeweiligen aktuellen Exemplar.
5. Mit `pm.TestGround.Return` zur ursprünglichen Position zurückkehren.

Keine neue Taste oder Controllerbelegung. Folge-Teleports überschreiben den
ursprünglichen Rückkehranker nicht. Kampf, gesperrte Eingabe, Innenraum und
Niederlagenrückkehr sperren den Teleport. Blockierte Rückkehrziele erhalten den
Anker, statt die Spielfigur ungeprüft in eine Kollision zu setzen.

**Koordinaten:** Mitte X −7500 / Y −4000 / Boden Z 0 cm. Bodenfläche 56 × 36 m,
X −10300…−4700, Y −5800…−2200; niedrige kollidierbare Randeinfassung. Die
Bestandsprüfung fand keine Überlappung platzierter bestehender Actors mit der
geplanten Fläche. Das historische Showcase bei −5200/−2300 lag zu nah an Bäumen,
Zäunen und Hausdekoration und wurde nicht ungeprüft als begehbarer Bereich übernommen.

## Ursache des bisherigen Problems

`Tools/CreaturePolishV4/Showcase.py` erzeugte Boden und zehn VisualActors
explizit über `SpawnReviewActor`, versetzte und sperrte die Spielfigur und
entfernte die Actors nach der Aufnahme wieder. Im gewöhnlichen Spiel wurde
nichts erzeugt. Das war bereits im V4-Bericht und der Werkzeuganleitung als
kontrollierte, transiente Vorführung beschrieben.

Neu: `Development/PokeMonsterCreatureTestGround` als automatisch gestartetes
PIE-WorldSubsystem, exakt auf VisualV2 begrenzt. Kein zweites Wildhabitat-,
Animations-, Interaktions- oder Kampfsystem. Die historische Vorführung bleibt
als separates Aufnahmeinstrument erhalten.

## Zehn vorhandene Arten und Testbereiche

| Nr. | Art | Bereichsmitte X / Y (cm) | Originalgröße |
|---|---|---|---|
| 1 | Glumanda, bestehende ID Zunderlauf | −9500 / −4700 | 0,60 m |
| 2 | Schiggy | −8500 / −4700 | 0,50 m |
| 3 | Bisasam | −7500 / −4700 | 0,70 m |
| 4 | Pikachu | −6500 / −4700 | 0,40 m |
| 5 | Myrapla | −5500 / −4700 | 0,50 m |
| 6 | Enton | −9500 / −3300 | 0,80 m |
| 7 | Machomei | −8500 / −3300 | 1,60 m |
| 8 | Nebulak | −7500 / −3300 | 1,30 m |
| 9 | Gengar | −6500 / −3300 | 1,50 m |
| 10 | Glurak | −5500 / −3300 | 1,70 m |

Pro Exemplar 4,30 m Wanderradius; benachbarte Bereichsmitten mindestens 10 m
auseinander. Unterschiedliche Seeds, Pausen und Animationsphasen. Keine künstliche
Vergrößerung, keine neuen Modelle oder Änderungen an Präsentationsassets.
Die vorhandene Wanderkomponente prüft Boden und Bewegungssegmente. Die Visuals
selbst blockieren die Spielfigur nicht.

`pm.TestGround.Mode auto` zeigt zeitversetzt vorhandene Idle-/Walk-/Run-Rollen.
`idle`, `walk` und `run` wählen diese Rollen gezielt, mit weiterhin zulässigen
Pausen und langsamen Drehungen. `pm.TestGround.React attack|hit|faint|happy`
verwendet die vier bestehenden Reaktionen ohne Kampflogik oder Schaden.
Gluraks vorhandene MotionV5-Abheben-/Hover-/Landenfolge läuft im Auto-/Walkbetrieb;
Nebulaks vorhandene Gashülle und beide Schwanzflammen bleiben erhalten.
Die Bewegung pausiert weiter als 35 m von der Spielfigur entfernt.

## Schutz der regulären Welt und Spielstände

- Sichtbare `TEST 01`…`TEST 10`-Beschriftung und Actor-Tag `PokemonDevelopmentSpecimen`.
- Ausschließlich vorhandene `APokeMonsterCreatureVisualActor`, keine
  `APokeMonsterVisibleWildCreatureActor`, keine Interactable-Schnittstelle,
  Begegnungs-ID oder Kreatureninstanz für das Speichern.
- Keine Fangbarkeit, XP-Vergabe, Inventar- oder Teamänderung durch Testreaktionen.
- Die Bewegungs-Overrides betreffen nur die jeweiligen Laufzeitkomponenten.
  Spezies- und Präsentationsdaten werden nicht verändert.
- Keine neuen Maps, Worktrees, Projektkopien, Landschafts-, Heilhaus-, Kamera-,
  Licht-, Schatten-, TAA- oder Gameplayänderungen.
- Andere Maps, Standalone und ausgelieferte Spiele enthalten dieses PIE-Gelände nicht.
- Vollbackup `03492bd96b4dba44692f675c19d5f11abfa86b4b` bleibt unter beiden
  bestehenden lokalen Backup-/Archiv-Refs erhalten und wird nicht gepusht.

## Tatsächliche PIE-Nachweise und QHD-Aufnahmen

**Zwei unabhängige gewöhnliche PIE-Starts**, jeweils mit zehn bereits vorhandenen
nativen Testexemplaren, bevor das rein lesende `Observe.py` lief. Kein
Showcase-/Spawnfixture war für den Zugang beteiligt. Der zweite Start nach
Editorneustart wurde ohne aktiven Kampf und mit sauberen Paketen dokumentiert.
Der erste Lauf prüfte zusätzlich die Teleportsperre im zufällig bereits gestarteten
normalen Wildkampf; reguläre Flucht beendete diesen Kampf.

Die vorhandene Spielfigur wurde auf der tatsächlich kollidierbaren Fläche über
normale Enhanced-Input-Ereignisse bewegt. Alle zehn Stationen, Idle/Run,
Reaktionen und Rückkehr wurden im echten PIE bedient und beobachtet. Die
Eingabeereignisse wurden technisch simuliert; dies ist **kein physischer
Switch-Pro-Controller-Test und kein vom Nutzer persönlich durchgeführter Lauf**.
Die Verfügbarkeit beim normalen Play ist unabhängig von diesen Prüfscripten.

`Acceptance03`: elf Prüfbedingungen bestanden, 15 echte Screenshots mit geprüftem
**2560 × 1440 Framebuffer**, unveränderte echte Spielkamera. Alle zehn Tiere
legten reale Strecken innerhalb ihrer eigenen Grenzen zurück. Glurak zeigte
Grounded, Takeoff, Hover und Landing, maximale gemessene visuelle Hoverhöhe
etwa 94 cm. Keine FPS-Benchmarks oder künstliche Kameraverkleinerung.

Die weit auseinander stehenden Bereiche passen nicht alle gleichzeitig in die
normale Kamera. Daher zehn Stationsaufnahmen statt eines behaupteten gemeinsamen
Zehn-Pokémon-Kamerabildes. Die erste Glurak-Aufnahme in `Acceptance02` war nach
Wanderbewegung teilweise abgeschnitten. Der Stationszugang wurde auf die aktuelle
Tierposition verbessert; die finale Aufnahme zeigt das ganze Exemplar.

Alle nachfolgenden Bilder stammen unbearbeitet aus Unreal und bleiben lokal;
sie werden nicht auf GitHub hochgeladen:

| Art | Echte QHD-Spielkameraaufnahme |
|---|---|
| Glumanda | [Station 1](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/TestGroundV1/Acceptance03/Station0100000.png) |
| Schiggy | [Station 2](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/TestGroundV1/Acceptance03/Station0200000.png) |
| Bisasam | [Station 3](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/TestGroundV1/Acceptance03/Station0300000.png) |
| Pikachu | [Station 4](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/TestGroundV1/Acceptance03/Station0400000.png) |
| Myrapla | [Station 5](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/TestGroundV1/Acceptance03/Station0500000.png) |
| Enton | [Station 6](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/TestGroundV1/Acceptance03/Station0600000.png) |
| Machomei | [Station 7](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/TestGroundV1/Acceptance03/Station0700000.png) |
| Nebulak | [Station 8](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/TestGroundV1/Acceptance03/Station0800000.png) |
| Gengar | [Station 9](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/TestGroundV1/Acceptance03/Station0900000.png) |
| Glurak | [Station 10](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/TestGroundV1/Acceptance03/Station1000000.png) |

![Glurak im normalen PIE-Testgelände](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/TestGroundV1/Acceptance03/Station1000000.png)

## Technische Tests

- Vollständiger Mac Development Editor-Build `TestGroundBuild05`: erfolgreich.
- Projekt-Automation `TestGroundAutomation04`: **98/98 erfolgreich**, null
  Testwarnungen, Fehler oder nicht ausgeführte Tests. Zwei neue Regressionstests
  prüfen normale PIE-Zulässigkeit, Map-Abgrenzung, zehn echte Präsentationen,
  sieben Rollen, Boden/Wege und fehlende Wild-/Interaktionsidentität.
- Elf bestehende Maps: **je null Map-Check-Fehler und Warnungen**; abschließend
  VisualV2 geladen, keine Pakete gespeichert.
- `Acceptance03`: Zugang, echter Input-Lauf, zehn begrenzte Bewegungsbereiche,
  Idle, Rückkehr, unveränderte Team-IDs/HP/XP, identische Wildpopulation, kein
  Kampf/Fang durch Testtiere und identische Save-Datei bestanden.

- Vollständiger echter PIE-Fußlauf `PermanentGroundFinalFoot02`: **103 Schritte,
  305,56 m**, alle acht Richtungen und Sprint mit tatsächlich gemessenen
  **315 cm/s**; keine Testteleports. Wanderer/Dialog/Quest, Liora/Trainerkampf,
  Wildfang/Teamwechsel, Brücke/Wald, Heilhaus gerade und diagonal, Heilung,
  Checkpoint und Save/Load bestanden. ClassicBattle-Beobachter bestätigt
  unveränderte Kameraposition und Rückkehr; Originalspielstand danach exakt
  restauriert. Die Route verwendet simulierte Enhanced-Input-Eingaben.
- Der erste Fußlauf stoppte nach 211,25 m bei ForestEast als „Blocked“. Der
  tatsächliche Spielnachweis zeigt dort **einen dritten regulären Wildkampf
  gegen Glurak**, keinen Fehler des Testgeländes und keine belegte Baumkollision.
  Die ältere Route behandelte zusätzliche Wildkämpfe außerhalb ihrer vorgesehenen
  zwei Kämpfe nicht. Ein ausschließlich für den Prüftreiber registrierter Helfer
  benutzt die vorhandene erlaubte Fluchtfunktion, ohne erzwungenes Kampfende.
  Im erfolgreichen zweiten Lauf trat tatsächlich ein zusätzlicher Gengar-
  ClassicBattle auf: Flucht erlaubt, Ausgang FLED, Route danach fortgesetzt.
  Keine Habitat-, Kollisions-, Kampfregel- oder Wegpunktänderung. Der erste
  Fehllauf und beide Save-Restaurierungen bleiben vollständig nachvollziehbar.
- Der alte reale Spielstand enthält zwei technische Test-Water-Einträge ohne
  3D-Begleiter. Null Begleiterbeobachtungen dieser Fußroute sind **kein**
  positiver 3D-Begleiternachweis. Diese Lücke wurde separat geschlossen:
  `CompanionProbe.json`, explizit ungespeicherte Drei-Starter-Party-Fixture,
  bestätigt **genau einen 3D-Begleiter zusätzlich zu zehn Testexemplaren**,
  unveränderte Party-IDs bei Test-Ohnmacht, kein Kampf durch Testreaktionen
  sowie Rückkehr und Wiederaufnahme des Begleiters. Abstand zunächst 162,90 cm.
  Danach PIE regulär beendet; Save-Datei unverändert.


Originaler Dev-Spielstand vor/nach den reinen Geländeläufen:
`eeab48f3c5652ef6d24b7f386ee7c26973336c929edf39aa7f6593d407a913df`.
Kontrollmedien, Logs und Testspielstände unter `Saved` sind keine Git-Inhalte.

## Einschränkungen und frühere Prüffehler

Die Fläche ist ein freies funktionales Entwicklungsareal, kein neuer
Landschafts-Art-Pass. Vorhandene Animations-/Modellmängel werden durch diesen
Auftrag nicht neu modelliert oder als behoben ausgegeben. Große Flügel können
zeitweise einen Teil der TEST-Beschriftung überdecken. Standalone/Shipping
werden absichtlich nicht um eine Testwelt ergänzt. Der physische Controller-Test
bleibt beim Nutzer.

Die ersten eigenen Prüfversuche sind erhalten: ein korrigierter C++-
TObjectPtr-Iterationsfehler; ein anfangs falscher temporärer Automation-Paketname;
ein fehlerhaft doppelt aufgerufener Subsystem-Lebenszyklus im Test mit Absturz des
separaten unbeaufsichtigten Testprozesses; anschließend falsche Teardown-Reihenfolge
mit Warnungen. Diese **Testaufbaufehler wurden korrigiert**, nicht unterdrückt.
Der finale vollständige Lauf ist ohne Testwarnungen erfolgreich. Frühe lesende
Python-Abfragen verwendeten eine nicht öffentlich reflektierte Visual-Property;
die Prüfung liest jetzt den bestehenden öffentlichen Spezies-Vertrag.

Bekannte externe Engine-Ausgaben (`idevice_id`, Bad CPU type/86, frühe Engine-
Condition-Meldungen, Python-Namenskollision und MCP-Hinweise) werden getrennt von
Projektassertions bewertet; sie wurden nicht durch globale Konfigurationsänderungen
verborgen. Es wird keine physische Hardware- oder allgemeine Animationsabnahme behauptet.

## Dateien und Versionsverwaltung

Neu: native Testgelände-Klasse `.h/.cpp`, zwei Tests in
`Tests/PokeMonsterCreatureTestGroundTest.cpp`, Werkzeuge und Anleitung unter
`Tools/CreatureTestGroundV1`, dieser Bericht. Aktualisiert: technische Anleitung,
Entscheidungshistorie, historischer Showcase-Hinweis sowie die strenge
`Tools/DevelopmentEvidence/CoreFiles.json`-Prüfsummenliste.

Keine Binärassets oder Maps geändert: **null neue LFS-Payloads**. Vor Staging werden
sämtliche eigenen Änderungen und der Index geprüft; nur benötigte Quellen,
Prüfwerkzeuge und Dokumentation werden aufgenommen. Backup-Refs werden nicht
übertragen. Commit-Hash und Remote-/LFS-Verifikation werden nach dem regulären
Push im Abschluss genannt; lokale Quittung unter
`Saved/ProjectRefinement/TestGroundV1/GitVerification.json`.


Vor Upload am 22.10.2026 anhand offizieller GitHub-Dokumentation geprüft:
[reguläre Einzeldateien bis 100 MiB](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github),
[LFS-Einzeldateigrenze im Free-Tarif 2 GB](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage).
Dieses Paket enthält ausschließlich kleine Textdateien und keine neuen
LFS-Objekte; kein zusätzlicher LFS-Upload, Kauf oder Budgeteingriff erforderlich.

Abschließende Integritätskontrolle: **4520 erforderliche Dateien** per strenger
Prüfsummenliste vollständig vorhanden und unverändert beziehungsweise gezielt
aktualisiert; keine ursprünglichen Einträge entfernt. Editor wieder in VisualV2,
PIE beendet, keine ungesicherten Pakete und keine zurückgebliebenen Testactors
in der gespeicherten Editorwelt. Alle elf Map-Dateien gegen HEAD/LFS-SHA geprüft.
