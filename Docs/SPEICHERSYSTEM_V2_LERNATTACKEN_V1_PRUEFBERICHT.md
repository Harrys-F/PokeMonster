# Speichersystem V2 und Lernattacken V1 – Prüfbericht

Ausgang: `87f1c76c2979081c18f746fcd0827ff4ad6d2974`, aktives `main`, bestehendes origin. Ausschließlich `/Users/harry/Developer/PokeMonster`; keine neuen Maps, Kopien, Worktrees oder Backups. Stand 26.10.2026. Phase A und B werden getrennt geprüft und gesichert.

## Phase A – Umsetzung

- Bestehendes SaveGame-Schema 9 liest 1–8. Weltposition enthält Map, native Position/Rotation, die separat geführte tatsächliche Blickrichtung und bestehenden Innenraumkontext. Kontrollpunkt bleibt eigenständig.
- Hauptmenü: Speichern, Laden und automatischen Stand laden mit ausdrücklicher B-/Enter-Bestätigung und A-/Escape-Abbruch. Doppelte/gehaltene Eingaben gesperrt; bestehende Controllerbelegung unverändert.
- Manueller Slot `PokeMonster_Dev`; getrennte automatische Sicherung `PokeMonster_Recovery`. Niederlage, Heilung und interne Lern-/Entwicklungs-/Meisterentscheidungen überschreiben keinen manuellen Stand. Beide enthalten denselben bisherigen Team-/Inventar-/Fortschrittssnapshot plus ihre jeweilige Position und Kontrollpunkt.
- Laden validiert alle individuellen Daten vor Übernahme. Bestehendes OpenLevel bei Mapwechsel, vorübergehende Eingabesicherung, danach bestehende Kamera-/Innenraumsynchronisation und genau ein Begleiter. Keine Änderung der Perspektive, Innenraumtechnik oder Weltgestaltung.
- Legacy/ungültige Position/fehlende Map: verfügbarer gespeicherter Kontrollpunkt, sonst kollisionsgeprüfter Start. Blockierte Position: lokale Suche bis 2 m im gleichen Innenraum, dann sicherer Kontrollpunkt/Start. Ohne sicheren Ort Abbruch. Kein automatisches Umschreiben eines gelesenen Slots.
- Kampf, Dialog, aktive Entwicklung, Türübergänge sowie laufende Speicher-/Ladetransaktionen sperren normale Menüzugriffe. Interne geprüfte Entscheidungscommits verwenden eine getrennte Zugriffsmethode, denselben Speichertransport und den automatischen Slot.
- Niederlagenrückkehr wartet nach Mapwechsel begrenzt auf stabilen Bodenkontakt, bevor der automatische Stand geschrieben wird. Platzierungsfehler ändern nicht den zuletzt ausdrücklich aktivierten Kontrollpunkt.

## Prüfaufbau und Schutz

Alle neuen Disk-Tests wählen ausdrücklich einen eigenen `PokeMonster_SaveV2_Test_<Label>`-Slot. Automatische Teststände verwenden dessen `_Recovery`-Suffix. Normale Builds aktivieren diesen Editor-PIE-Transport nicht. Der bestehende explizite RAM-Transport bleibt erhalten. Beide sperren Low-Level-Schreiben der kanonischen Nutzerslots. Keine Nutzersave-Kopie, kein Umbenennen, kein Laden oder Überschreiben der vorhandenen Nutzerdatei. Nur Hashvergleich. Testdaten und kontrollierte Laufzeitpositionen sind technische Fixtures in der bestehenden Map.

Ausgangsinventur: 44 geschützte Dateien einschließlich 31 bereits unversionierter Arbeitsdateien, zwölf Mapdateien und vorhandenem Nutzersave. Beide Backup-Verweise zeigen unverändert auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`. Vor jedem Sicherungspunkt erneute Integritätsprüfung.

## Phase A – Testergebnisse

Endprüfung im korrigierten Build12 bestanden: `Main06` 128 Schritte / 24 Checks, `Restart06` 11 Schritte / 2 Checks in neuer PIE-GameInstance; `SaveV2MasterA01` 18 Checks einschließlich AP-Erhaltung und automatischer Sicherung; zwölf echte Map Checks je 0 Fehler/0 Warnungen, exakte unveränderte Editor-Szeneninventur ohne schmutzige Pakete. Zusätzlich bestanden: `EdgeTravel08` (9 Checks, tatsächlicher Mapwechsel und Niederlagenrückkehr), `MissingCheckpoint03` (5 Checks), `EvolutionA03` (5 Checks, vollständige bestehende farbige Enthüllung, danach Save/Load).

Frühere bestandene Nachweise: Main04/Main05 sowie Restart04/05, kontrollierte Schema-8-/fehlende-/ungültige-/blockierte Positionsfälle (`EdgeLegacy02`, `EdgeMissing02`, `EdgeInvalid02`, `EdgeBlocked02`, jeweils 4 Checks). Alle behalten Originalsave und Testdatei beim Laden bytegleich. Der neue Enddurchlauf wird gesondert aufgeführt.

### Tatsächlich gefundene Fehler und Fehlversuche

- Frühe Testadapter verwendeten einen nicht exponierten Python-Propertynamen, eine falsche Heiler-ID, einen nicht verfügbaren get_pawn-Aufruf beziehungsweise einen Textvergleich für +0/−0. Jeweils gezielt korrigiert; ursprüngliche Ergebnisse bleiben lokal erhalten.
- Der verschärfte Menüzugriff hätte interne Entwicklungs-/Lern-/Meisterautosaves blockiert. Auf getrennten geprüften internen Zugriff und automatischen Slot korrigiert.
- `EdgeTravel03` bis `07` belegten eine Reihenfolge-/Spawnlücke bei mapübergreifender Niederlage. Endgültige Diagnose: am Sicherungszeitpunkt Falling=true und noch kein sicherer Boden, später korrekt gelandet. Korrektur wartet auf tatsächlichen Bodenkontakt und hält neue Pawns während ausstehender Rückkehr gesperrt. `EdgeTravel08` besteht einschließlich anschließender manueller Rückladung.
- Build09 scheiterte an bestehendem Unity-Namenskonflikt der globalen Testkommandovariablen `Key` mit einem Engine-Header. Nur die interne Variable umbenannt; keine Tastenbelegungsänderung. Build10/11/12 erfolgreich.

### Automation und Warnungen

Drei neue native Tests prüfen Positionsvertrag/Serialisierung, Legacy-/ValidateOnly-Atomizität und Menübestätigung/Controller-Doppeleingabesicherung. Vollständige Automation vor der letzten Rückkehrkorrektur: 213 Tests ohne Fehler. Läufe A02/A04/A05: 212 erfolgreich + 1 mit externen iOS-Warnungen, Engine Exit 0, strenger Wrapper Exit 1; ausdrücklich kein vollständiger strenger QA-Pass. A03 war 213/213 ohne Testwarnung und Wrapper Exit 0. Die externe `idevice_id`-/posix_spawn-86-Warnung ist davon unabhängig in Startlogs vorhanden. Aktueller Endlauf **SaveSystemV2AutomationA06: 213 erfolgreich, 0 Testwarnungen/Fehler, Engine Exit 0, strenger Wrapper Exit 0**. Externe iOS-Startwarnungen bleiben im Rohlog separat; keine Warnungsfilterung.

## Echte lokale Bildnachweise

Aufnahmen stammen aus dem realen Unreal-Spielviewport, keine Konzeptbilder. PNGs und Logs bleiben ignoriert und werden nicht hochgeladen. Dateien unter `Saved/ProjectRefinement/SaveSystemV2/Main06/`: ForestSaved/ForestLoaded, InteriorSaved/InteriorLoaded, DefeatRecovery, ManualAfterDefeat. QHD 2560×1440. Menü-/Bestätigungscaptures liegen im vorhandenen `Saved/GlumandaV11/LiveUI/SaveV2Restart06*`. Entwicklung nach bestehender V2.1 unter `SaveV2EvolutionA03Complete`.

## Phase B – Bestand und Umsetzung

Der frühere Praxistest ist bestätigt: 16 Einträge / 15 unterschiedliche Attacken ohne produktives Move-Asset, keine bloße leere Referenz auf bereits vorhandene vollständige Daten.

| Spezies | Level: fehlende Kristallkennung |
|---|---|
| Bibor | 20 TWINEEDLE; 30 PURSUIT; 35 PIN_MISSILE |
| Garados | 1 THRASH; 35 TWISTER; 50 HYPER_BEAM |
| Habitak | 25 PURSUIT; 31 MIRROR_MOVE; 37 DRILL_PECK |
| Karpador | 1 SPLASH; 30 FLAIL |
| Smettbo | 18 SUPERSONIC; 23 WHIRLWIND; 28 GUST; 34 PSYBEAM; 40 SAFEGUARD |

Die vorhandene geprüfte `SpeciesV11.json` bleibt Lernlistenquelle. Mechaniken werden gegen den bereits verwendeten gepinnten Kristall-Stand `5c877ef55197039c9676e8e3eec6d254b1c40fe8` geprüft. Noch keine automatische Vergabe früher übersprungener, abgelehnter oder bloß angebotener Attacken. Ein persönliches Repertoire enthält ausschließlich tatsächlich erlernte Attacken; spätere Reaktivierung bleibt an den Meister gebunden.

## Phase B – Produktive Bindungen

Alle 16 technisch eindeutig zugeordneten Zeilen sind gebunden; 15 neue Move-Assets unter `/Game/Data/Moves/LearnMovesV1`. Ausschließlich die fünf betroffenen Speziesassets erhalten diese Referenzen, keine Änderung an den Maps, Modellen, Animationen, bisherigen 75 Move-Assets oder gefüllten anderen Lernzeilen. Ursache waren fehlende produktive Attackendefinitionen und dafür benötigte gemeinsame Komponenten. Werte und Level wurden nicht erfunden.

| Spezies | Level | Stabile Move-ID / Originalnummer | Attacke | Typ / Kategorie | Stärke · Genauigkeit · AP | Nachweis |
|---|---:|---|---|---|---|---|
| Karpador | 1 | Splash / 150 | Platscher | NORMAL / STATUS | 0 · 100 % · 40 | produktiv + Einzelautomation + PIE-Attacke |
| Karpador | 30 | Flail / 175 | Dreschflegel | NORMAL / PHYSICAL | 1 · 100 % · 15 | produktiv + Einzelautomation + PIE-Attacke |
| Garados | 1 | Thrash / 37 | Fuchtler | NORMAL / PHYSICAL | 90 · 100 % · 20 | produktiv + Einzelautomation + PIE-Attacke |
| Garados | 35 | Twister / 239 | Windhose | DRAGON / SPECIAL | 40 · 100 % · 20 | produktiv + Einzelautomation + PIE-Attacke |
| Garados | 50 | HyperBeam / 63 | Hyperstrahl | NORMAL / PHYSICAL | 150 · 90 % · 5 | produktiv + Einzelautomation + PIE-Attacke |
| Smettbo | 18 | Supersonic / 48 | Superschall | NORMAL / STATUS | 0 · 55 % · 20 | produktiv + Einzelautomation + PIE-Attacke |
| Smettbo | 23 | Whirlwind / 18 | Wirbelwind | NORMAL / STATUS | 0 · 100 % · 20 | produktiv + Einzelautomation + PIE-Attacke |
| Smettbo | 28 | Gust / 16 | Windstoß | FLYING / PHYSICAL | 40 · 100 % · 35 | produktiv + Einzelautomation + PIE-Attacke |
| Smettbo | 34 | Psybeam / 60 | Psystrahl | PSYCHIC / SPECIAL | 65 · 100 % · 20 | produktiv + Einzelautomation + PIE-Attacke |
| Smettbo | 40 | Safeguard / 219 | Bodyguard | NORMAL / STATUS | 0 · 100 % · 25 | produktiv + Einzelautomation + PIE-Attacke |
| Bibor | 20 | Twineedle / 41 | Duonadel | BUG / PHYSICAL | 25 · 100 % · 20 | produktiv + Einzelautomation + PIE-Attacke |
| Bibor | 30 | Pursuit / 228 | Verfolgung | DARK / SPECIAL | 40 · 100 % · 20 | produktiv + Einzelautomation + PIE-Attacke |
| Bibor | 35 | PinMissile / 42 | Nadelrakete | BUG / PHYSICAL | 14 · 85 % · 20 | produktiv + Einzelautomation + PIE-Attacke |
| Habitak | 25 | Pursuit / 228 | Verfolgung | DARK / SPECIAL | 40 · 100 % · 20 | produktiv + Einzelautomation + PIE-Attacke |
| Habitak | 31 | MirrorMove / 119 | Spiegeltrick | FLYING / STATUS | 0 · 100 % · 20 | produktiv + Einzelautomation + PIE-Attacke |
| Habitak | 37 | DrillPeck / 65 | Bohrschnabel | FLYING / PHYSICAL | 80 · 100 % · 20 | produktiv + Einzelautomation + PIE-Attacke |

Stärke 1 bei Dreschflegel ist der originale Datenmarker; die Kampfberechnung verwendet abhängig von 48×KP/MaxKP die Stärken 200/150/100/80/40/20, ohne kritischen Treffer oder Schadensstreuung. Physisch/speziell bleibt die Gen-2-Typentscheidung; Verfolgung ist speziell. Ausgangsregeln wie STAB, Status, Immunitäten, AP-Verbrauch, Schaden und Turn-Transaktion bleiben im bisherigen gemeinsamen Code.

### Wiederverwendete und ergänzte Komponenten

Mehrfachtreffer, Vergiftung, Verwirrung, Zurückschrecken und Rampage werden wiederverwendet. Neu sind Erholungszug, KP-abhängige Stärke, Spiegeln der letzten ausgeführten Attackendefinition, Team-Statusschutz, Abfangen einer Wechseltransaktion und erzwungenes Wechseln/Beenden. Keine zweite Schadens-, Lern-, Inventar- oder Speicherimplementierung.

Spiegeltrick verwendet denselben Resolver, verbraucht ausschließlich eigene AP und hält kopierte mehrzügige Definitionen vorübergehend in der bestehenden Session. Hyperstrahl verlangt auch nach einem K.O. einen Erholungszug und erzeugt dabei keinen zweiten AP-Verbrauch. Bodyguard schützt das Team fünf Runden gegen eingehende Statusprobleme/Verwirrung und bleibt beim Wechsel erhalten. Verfolgung trifft das auswechselnde Individuum mit doppeltem tatsächlichem Schaden; ein besiegtes auswechselndes Pokémon beschädigt nicht stattdessen die Reserve. Wirbelwind gibt keine Sieg-XP und umgeht keine Sperre besonderer Kämpfe; Trainerwechsel benötigt eine lebende Reserve und die Kristall-Zugbedingung.

Windstoß/Windhose funktionieren normal produktiv. Ihr Bonus gegen explizit mechanisches Luft-Aufladen ist zusätzlich mit einer benannten transienten Fixture vorbereitet/geprüft. Dekoratives Schweben wird nie als solcher Zustand behandelt. Eine vollständige Fliegen-Attacke bleibt außerhalb dieses Pakets. Es wird keine vollständige bitgenaue Kristall-Emulation behauptet. Vorhandene dokumentierte Projektabweichungen und noch fehlende Spezial-VFX bleiben erhalten.

### Lernen, Repertoire und Kompatibilität

Jede der 16 Bindungen ist als eigener Automationfall gegen die tatsächliche Spezies und das produktive Move-Asset geprüft. Level-1-Einträge werden bei neuer normaler Speziesbelegung berücksichtigt; bestehende Individuen erhalten keine rückwirkende Vergabe. Höhere Level prüfen Schwelle, freie Slots, vier volle Slots, offenes Angebot in nativer Serialisierung, Ersetzen, Ablehnen, bekannte Attacken und unveränderte AP anderer Slots. Ersetzte Attacken bleiben persönlich bekannt. Ablehnen ergänzt keinen Repertoireeintrag. Reaktivierung bleibt ausschließlich meistergebunden.

Die vorhandenen Tests für Entwicklungen vor/nach dem Spezieswechsel, fehlende Modelle, AP-Erhaltung, persönliche Identität, Teamverwaltung und Save-Kompatibilität bleiben Bestandteil der vollständigen Automation. Kein weiteres Speicherformat, kein Umbau der Entwicklung V2.1 und keine Änderung bestehender Controllerbelegung.

## Phase B – Tatsächlich durchgeführte PIE-Prüfungen

- `Learning02`: sechs abgeschlossene echte KO-/XP-Lernfälle. Bibor20 Duonadel, Garados35 Windhose, Habitak31 Spiegeltrick ausdrücklich abgelehnt, Karpador30 Dreschflegel, Smettbo40 Bodyguard im WorldBattle sowie Karpador30 mit freiem Slot. Fünf echte Lernangebote mit bestehender B/A-Bedienung, dazu automatisches Lernen im freien Slot. Nach jedem Fall manuell speichern, Team ändern und über das reguläre Hauptmenü laden; individuelle Daten jeweils exakt identisch wiederhergestellt.
- `Production01`: 20 vollständige Kampf-/Rückkehrfälle. Alle 15 tatsächlichen neuen Attackenassets in ClassicBattle; außerdem je ein WorldBattle-Fall aller fünf Arten. AP-Verbrauch und Ereignisse geprüft, erzwungene Erholungs-/Rampagezüge abgearbeitet, anschließend sichere Rückkehr ohne doppelte ClassicBattle-Szene. Technisch kontrollierte Kampfwerte, ausdrücklich keine neue Balancekonfiguration.
- `RestartAfterProcessB01`: zwei Checks nach vollständigem Editorprozess-Neustart. Derselbe vorherige manuelle Main06-Teststand wird durch reguläre Menübedienung mit Position/Blickrichtung, Team, AP, Inventar und Kontrollpunkt wiederhergestellt.
- `SaveLearnBattleB02`: vorhandene neun Kampfregressionen bestanden, einschließlich Classic/World, Items/Inventarverbrauch, Wechsel, erfolgreiche/fehlgeschlagene/verbotene Flucht, Status-/Feuerattacke, Sieg, Niederlage und leere AP. Ausschließlich bestehender RAM-Prüftransport, Originalsave bytegleich.

### Zurückbehaltene Fehlversuche

`Learning01` wurde regulär beendet und als fehlgeschlagen dokumentiert: Der Adapter wählte im freien Karpador-Set Platscher statt Tackle, sodass der schadensfreie Kampf offen blieb. Fünf vorher abgeschlossene Schritte und echte Bilder sind erhalten; korrigierter kompletter Nachweis `Learning02`. Kein Reparatureingriff in Gameplay oder Attackendaten.

Der erste zusätzliche Alt-Regressionseinstieg `SaveLearnBattleB01` erreichte keine Kampfprüfung: Sein alter RAM-Guard wollte unmittelbar nach Testgelände-Teleport während Falling speichern. Die neue Sperre lehnte korrekt ab. Der Adapter wartet nun begrenzt auf tatsächlichen Bodenkontakt; regulärer Stopp, danach kompletter bestehender Lauf `SaveLearnBattleB02` bestanden. Keine Lockerung der Produktionssperre.

## Bildnachweise und Messgrenzen

Sechs echte Spielszenenbilder Main06 sind **2560×1440**. 47 zusätzliche echte Slate-Aufnahmen aus Learning02, Production01 und RestartAfterProcessB01 sind **2331×1311**. Die Anforderung einer logischen QHD-Viewportgröße ist kein Nachweis gleicher PNG-Pixelmaße; native UI-Bilder werden weder hochskaliert noch als QHD bezeichnet. Daten: `Saved/ProjectRefinement/LearnMovesV1/NativeCaptureValidation.json`.

Beispiele (nur lokale Dateien, keine Medien im Commit):

- [Wald vor Laden](../Saved/ProjectRefinement/SaveSystemV2/Main06/ForestSaved.png), [Wald nach Laden](../Saved/ProjectRefinement/SaveSystemV2/Main06/ForestLoaded.png).
- [Heilhaus vor Laden](../Saved/ProjectRefinement/SaveSystemV2/Main06/InteriorSaved.png), [Heilhaus nach Laden](../Saved/ProjectRefinement/SaveSystemV2/Main06/InteriorLoaded.png).
- [Niederlagenrückkehr](../Saved/ProjectRefinement/SaveSystemV2/Main06/DefeatRecovery.png), [erneut manuellen Stand laden](../Saved/ProjectRefinement/SaveSystemV2/Main06/ManualAfterDefeat.png).
- [Echtes Duonadel-Lernangebot](../Saved/GlumandaV11/LiveUI/LearnLearning020Offer/ActualSlateViewport.png).
- [Echtes Ablehnen von Spiegeltrick](../Saved/GlumandaV11/LiveUI/LearnLearning022Offer/ActualSlateViewport.png).

Weitere tatsächliche Kampfaufnahmen: `Saved/GlumandaV11/LiveUI/LearnProductionProduction01*`. Die nach Kampfende ohne geöffnetes Menü aufgerufene UI-Capture-Funktion erzeugt absichtlich kein Bild; daher werden keine nicht existierenden After/Loaded-Dateien als Nachweise aufgeführt. Die sechs Lernergebnisse sind stattdessen im jeweiligen vollständigen Ergebnis-JSON und durch den echten Menü-Ladevergleich belegt.

## Endprüfung und Git

Speicherphase: `dcb8c464b1723c7c959454aa1e153a762dfc3fb2`, regulär auf GitHub gepusht, Remote-Hash identisch; keine neuen LFS-Assets in diesem Paket. Lernphase Build05: Editor-Build Exit 0. Erster voller Lauf `LearnMovesV1AutomationB01`: 245/245 erfolgreich, 0 Testwarnungen, Engine/strenger Wrapper Exit 0. Nach ergänzten Randfällen und den weiteren tatsächlichen PIE-Prüfungen finaler Lauf `LearnMovesV1AutomationB02`: **244 erfolgreich + 1 erfolgreich mit Warnungen, 0 fehlgeschlagen/nicht ausgeführt; Engine Exit 0, strenger Wrapper Exit 1**. Zwei bekannte externe `idevice_id`-/posix_spawn-86-Zeilen sind `PokeMonster.Creatures.Glutexo.ImportedSourceContract` zugeordnet; kein Projektfehler und keine Warnungsfilterung. Der letzte strenge Wrapper ist ausdrücklich **nicht bestanden**. Keine Wiederholung nur für grüne Farbe.

Zwölf abschließende Map Checks: jeweils 0 Fehler, 0 Warnungen. `SceneUnchanged_B.json`: identische VisualV2-Editorinventur, keine ungespeicherten Pakete. Bestehende Fortschritts-PIE-Regression `SaveLearnProgressionB01`: sechs Fälle, darunter Ersetzen/Ablehnen in Classic/World, freie Slots, echtes KO-XP und sichere fehlende Entwicklungsmodelle, bestanden. Alle 16 neuen Einzelbindungen/15 produktiven Wirkungen und zusätzlichen gemeinsamen Randfälle bestehen im finalen Lauf.

Der finale Integritätsnachweis umfasst erneut alle 44 geschützten Dateien, die 31 ursprünglichen unversionierten Arbeitsdateien, zwölf Mapdateien, den vorhandenen Nutzer-Save und beide unveränderten Vollbackup-Verweise. Zusätzlich werden alle bisherigen Kerndateien außerhalb der ausdrücklich freigegebenen Lernänderungen per SHA geprüft. Lernphase: **`7bb819a4c1eaf0c11aba56c8e7fa6a5597fc46da`**, regulär auf `origin/main` gepusht. Alle 20 LFS-Objekte (77.362 Byte) wurden erfolgreich übertragen. Lokale Working-File-/Pointer-/LFS-Medien-SHA-256 stimmen für alle 20 überein; anschließend bestätigte der offizielle GitHub-LFS-Endpunkt `lfs.github.com` per authentifizierter Download-Metadatenabfrage alle 20 Remoteobjekte. Keine Mediendownloads, keine gespeicherten Zugangsdaten, keine Budgetänderung und keine kostenpflichtige Freigabe. Remote-main-Hash identisch mit lokalem `main`, zusätzlicher LFS-Push-Dry-Run ohne ausstehende Objekte. Nachweis lokal `RemoteLFSVerified.json`.

Dieser Dokumentationsnachtrag enthält ausschließlich den endgültigen Bericht und dessen aktualisierten Integritätsmanifest-Eintrag. Keine Kontrollmedien, Caches, Nutzersaves oder Testslots wurden versioniert. Alle 31 ursprünglich unversionierten Dateien bleiben unversioniert und unverändert.

Bekannte externe iOS-Helferwarnungen bleiben von Projektfehlern getrennt. Physischer Controller-Test nicht durchgeführt; bestehende Softwareeingaben unverändert. Keine weiteren Welt-/Modell-/Animationsarbeiten. Die 16 angeforderten Lernbindungen sind produktiv; kein fachlich ungeklärter Lernlevel wurde eingesetzt. Frühere übersprungene/abgelehnte Attacken sind bewusst kein kostenlos nachträglich freigeschaltetes Repertoire.
