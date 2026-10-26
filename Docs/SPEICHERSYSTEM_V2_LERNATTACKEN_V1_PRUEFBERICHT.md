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

## Phase B – Bestandsaufnahme, noch nicht übernommen

Der frühere Praxistest ist bestätigt: 16 Einträge / 15 unterschiedliche Attacken ohne produktives Move-Asset, keine bloße leere Referenz auf bereits vorhandene vollständige Daten.

| Spezies | Level: fehlende Kristallkennung |
|---|---|
| Bibor | 20 TWINEEDLE; 30 PURSUIT; 35 PIN_MISSILE |
| Garados | 1 THRASH; 35 TWISTER; 50 HYPER_BEAM |
| Habitak | 25 PURSUIT; 31 MIRROR_MOVE; 37 DRILL_PECK |
| Karpador | 1 SPLASH; 30 FLAIL |
| Smettbo | 18 SUPERSONIC; 23 WHIRLWIND; 28 GUST; 34 PSYBEAM; 40 SAFEGUARD |

Die vorhandene geprüfte `SpeciesV11.json` bleibt Lernlistenquelle. Mechaniken werden gegen den bereits verwendeten gepinnten Kristall-Stand `5c877ef55197039c9676e8e3eec6d254b1c40fe8` geprüft. Noch keine automatische Vergabe früher übersprungener, abgelehnter oder bloß angebotener Attacken. Ein persönliches Repertoire enthält ausschließlich tatsächlich erlernte Attacken; spätere Reaktivierung bleibt an den Meister gebunden.

## Offene Punkte / Git

Phase B und endgültige Gesamtabnahme noch ausstehend. Physischer Controller-Test nicht durchgeführt; nur bestehende Softwareeingaben. Keine Behauptung warnungsfreier Engine-Startlogs. Commits/Remote-/LFS-Ergebnis werden nach abgeschlossenen geprüften Paketen ergänzt.
