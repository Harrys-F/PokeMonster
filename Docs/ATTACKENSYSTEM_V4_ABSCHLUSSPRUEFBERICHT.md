# Attackensystem V4 – Abschlussprüfung der 49 Attackenwirkungen

Stand: 23.10.2026. Aktives Projekt: `/Users/harry/Developer/PokeMonster`.

## Ergebnis und verbleibende Freigabe

**49 von ursprünglich 49 offenen Gameplaywirkungen sind implementiert, produktiv angebunden und durch eigene positive Kampflogiktests überprüft. Keine dieser 49 Gameplaywirkungen bleibt offen.** 68 kanonische Lernattacken stehen jetzt in 71 Move-Assets einschließlich der drei historischen Testassets bereit. Alle 102 bisherigen Lernlisteneinträge der zehn vorhandenen Spezies sind vollständig gebunden.

**Die GitHub-Sicherung dieses neuen Pakets ist noch ausstehend.** Die bestehenden Commits `22764fd8`, `2950a5ea` und der separat geprüfte Fehlernachtrag `0a26b6ed` sind auf `origin/main` erreichbar. Für die neuen Assets sind 229,963 Bytes in 59 LFS-Dateien vorgesehen (rund 224.6 KiB). Es wurde noch kein neuer Asset-Upload versucht. Aktuelles freies Kontingent beziehungsweise ein weiterhin vorhandenes 0-USD-LFS-Budget sind hier nicht bestätigt. Safari ist bei GitHub abgemeldet; die Nutzungsübersicht fordert eine Anmeldung. Keine Kontodaten oder Budgets wurden geändert. Die vom Nutzer angefragte Kostenabsicherung bleibt vor dem Upload erforderlich. Daher wird der Gesamtauftrag einschließlich GitHub-Abgabe noch nicht als vollständig abgeschlossen ausgegeben.

Die vollständige Abnahme pro ID, Zahlenwerten, produktivem Pfad, eigener Automation, tatsächlicher PIE-Ausführung und Einschränkungen steht in [ATTACKENSYSTEM_V4_ABNAHMETABELLE.md](ATTACKENSYSTEM_V4_ABNAHMETABELLE.md) und [ATTACKENSYSTEM_V4_ABNAHME.json](ATTACKENSYSTEM_V4_ABNAHME.json). Der vollständige Assetbestand steht in `ATTACKENSYSTEM_V4_AKTUELLER_BESTAND.json`.

## Bestehende Systeme und konkrete Umsetzung

Die vorhandene `UPokeMonsterBattleSession` bleibt die einzige Rundenausführung für ClassicBattle und WorldBattle. Erweitert wurden die vorhandenen Effektkomponenten, flüchtigen Kampfzustände und dieselbe AP-/Repertoireverwaltung. Es gibt keine zweite Kampf-, Inventar-, NPC-, Lern- oder Speicherarchitektur. Die bestehenden 19 kanonischen Attackenassets sind bytegleich erhalten; hinzu kommen 49 neue Move-Assets unter `/Game/Data/Moves/EffectsV4`.

| Gemeinsamer Baustein | Produktive Verwendung / Verhalten |
|---|---|
| Gen-2-Schaden | Typabhängige physisch/speziell-Kategorie, STAB, Typentabelle, Volltreffer, Schadensstreuung; geprüfte Stufen- und Rundungsregeln |
| Volltrefferstufen | Karateschlag, Rasierblatt, Schlitzer, Kreuzhieb; Energiefokus +1 Stufe |
| Status-/Genauigkeitsstufen | Alle sieben relevanten Werte, Grenzen ±6, Scanner und Psych-Plus |
| Primäre Statusprobleme | Bestehende Verbrennung sowie Paralyse, Schlaf, Gift und Einfrieren; Immunitäten, Zugverhinderung, Residualschaden und Heilung |
| Sekundäre Effekte | Zurückschrecken, Verwirrung und zusätzliche Status-/Wertänderungen mit geprüften Wahrscheinlichkeiten |
| KP-Bruchteile | Überroller-Rückstoß, Traumfresser-Schlafbedingung und Absorption; zeit-/wetterabhängige Synthese/Mondschein |
| Mehrfachtreffer | Kratzfurie 2–5 Treffer mit 3:3:1:1-Gewichten, eigenem Volltreffer je Treffer und sofortigem Stopp bei Ohnmacht |
| Mehrzügige Aktionen | Solarstrahl und Schädelwumme mit einmaligem AP-Verbrauch, Blättertanz mit Bindung und kurzer Gen-2-Verwirrung |
| Schutz / Dauerzustände | Schutzschild, Lichtschild, Feuerwirbel, Horrorblick, Fluch, Raserei und Abgangsbund |
| AP und Auswahl | Aussetzer blockiert die richtige Attacke; Groll entzieht 2–5 AP und aktualisiert das persönliche Repertoire |
| Wetterkontext | Regentanz und begrenzte Regen-/Sonne-/Sand-Kontexte für die vorhandenen wetterabhängigen Wirkungen; keine Weltlichtänderung |
| Befreiung | Turbodreher entfernt Egelsamen und Teilfesselung, ohne einen späteren Initiativebonus zu erfinden |

Ein während des Kampfes durch Lernen wiederverwendeter Slot wird nicht mit der alten Attacke verwechselt. Veraltete Aussetzer-, Groll- und mehrzügige Slotbindungen werden gezielt gelöst. Ein echter KO-/Lern-/Wechsel-/Groll-Test sichert das ab. Zusätzliche Kombinationsprüfungen sichern Schlaf vor Flinch sowie Verwirrung vor voller Paralyse ab.

## Regelgrundlage und ausdrückliche Grenzen

Verbindlich ist das vom Nutzer festgelegte Kristall-/Generation-2-Profil. Die unveränderte historische PokeAPI-Extraktion bleibt Herkunftsnachweis für Lernlisten und frühere Verfügbarkeit; moderne `effect_id`-Beschreibungen wurden nicht ungeprüft als Gen-2-Semantik übernommen. Die aktuelle Zuordnung liegt in `Tools/MoveEffectsV4/CrystalMovePlan.json`. Öffentliche Primärquellen sind mit festen Revisionen und SHA-256 in `ATTACKENSYSTEM_V4_KRISTALL_QUELLEN.json` dokumentiert, insbesondere [Kristall-Attackendaten](https://github.com/pret/pokecrystal/blob/5c877ef55197039c9676e8e3eec6d254b1c40fe8/data/moves/moves.asm) und [Effektskripte](https://github.com/pret/pokecrystal/blob/5c877ef55197039c9676e8e3eec6d254b1c40fe8/data/moves/effects.asm). Keine ROM-Dateien oder Originalspielmedien wurden übernommen.

Wichtige konkret berücksichtigte Gen-2-Unterschiede: Fußkick hat Stärke 50 und 30 % Flinchchance, Säure senkt Verteidigung statt Spezial-Verteidigung, Wachstum erhöht nur Spezial-Angriff, Lockduft senkt Ausweichen um eine Stufe, Biss ist speziell, Fluch hat den Typ ???, Horrorblick umgeht Schutzschild, Scanner berücksichtigt Genauigkeit und Ausweichen. Synthese/Mondschein sind zeitabhängig; normaler Kontext ist vorerst Tag. Vorhandene Lichtquellen, Tagesstimmung und Kamera werden dadurch nicht geändert.

Erhaltene Projektentscheidungen: Initiativegleichstand zugunsten Seite A, bisherige XP-Verteilung und individuelle Werteberechnung, Fang-/Team-/Heil-/Speicherarchitektur, vier aktive Attacken und ausschließlich ortsgebundene nachträgliche Neuordnung. Historische reine Prototyp-Rechentests verwenden weiterhin ausdrücklich das Legacy-Profil; normale Begegnungen wählen Kristall. FRandomStream ermöglicht reproduzierbare Tests, bildet aber keine ROM-Zufallsfolge nach. Technische Integerüberläufe und Originalspiel-Bugs werden nicht absichtlich reproduziert. Getragene Kampfitems, Ordenboni, Delegator, Stachler und weitere nicht vorhandene Systeme werden hier nicht neu eingeführt. Turbodreher kann bestehende Egelsamen und Teilfesselungen entfernen; ein nicht vorhandenes Stachlersystem wird nicht behauptet.

Es wurden keine individuellen neuen VFX für jede Attacke produziert. Vorhandene Angriffs-/Treffer-/Statusdarstellung bleibt in Gebrauch. Das ist eine visuelle Erweiterungsgrenze, keine fehlende Gameplaywirkung der 49 Attacken.

## Prüfung

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Editor-Build | `MoveEffectsV4CompleteBuild11`: bestanden, Exit 0 |
| Vollständige Automation | `MoveEffectsV4CompleteAutomation05`: **182 erfolgreich, 0 Warnungstests, 0 Fehler, 0 ausgelassen; strenger Wrapper Exit 0** |
| Produktive Attackenfälle | 49 einzeln ausgewiesene Tests mit unveränderten tatsächlichen Move-Assets; positive Wirkung beobachtet |
| Randfälle | Stufen-/Wahrscheinlichkeitsgrenzen, Immunitäten, Wechsel-/Fluch-/Fessellösung, KO während Mehrfachtreffern/Rückstoß, Wetter, Statuskombinationen, AP-/Repertoire-Save und Lernen nach KO |
| Map Checks | Elf vorhandene Maps, jeweils 0 Fehler und 0 Warnungen; keine Map gespeichert oder erstellt |
| Produktions-PIE | `CrystalProduction04`: 49 ClassicBattle-Attackenfälle + zehn WorldBattle-Fälle mit allen zehn vorhandenen Pokémon, 59/59 erfolgreich, 118 echte native Aufnahmen |
| Lernen / Entwicklung | `CrystalLearning02`: sechs tatsächliche PIE-Menüfälle, 20 Screenshots, Ersetzen/Ablehnen/freie Slots/fehlendes Zielmodell |
| Meister / Repertoire | `CrystalMaster01`: 18 Prüfungen, sechs Screenshots, keine freie Neuordnung im normalen Teammenü; Abbruch, Speichern und AP-Erhaltung |
| Controller-Software | `CrystalController01`: 46 Prüfungen einschließlich Fokus, Beutel, Teamwechsel und tatsächlichem Begleiter; **kein physischer Hardwaretest** |
| Niederlagen-Autosave | `CrystalDefeat01`: Rückkehr, Heilung, Speichern und erneutes Laden bestanden; Originalsave wiederhergestellt |
| Vollständiger Fußlauf | `CrystalFullFoot01`: 103 Schritte, 311.18 m, ohne Testteleports, Kampf/Fang/Dialoge/Heilhaus/Heilung/Save/Load bestanden |
| Zusätzlicher Beobachter | `CreatureGameplay.json` ausdrücklich ausgewertet: bestanden; keine unterdrückte Nebenprüfung |
| Schutzprüfung | 2.858 erfasste Dateien; ausschließlich die zehn erlaubten Spezies-Lernlisten verändert; sämtliche übrigen Original-/Map-/Modell-/Konfigurationsdateien unverändert |

Die 59 Produktions-PIE-Fälle stammen aus Build 10. Die danach isoliert korrigierte Reihenfolge kombinierter Statusprobleme wurde mit dem vollständigen 182er-Automationslauf in Build 11 abgesichert; die gemeinsamen Lern-, Meister-, Controller-, Niederlagen- und Fußlaufprüfungen erfolgten in diesem abschließenden Build. Es wird nicht behauptet, jedes zufällige Zusatzergebnis sei in jedem einzelnen PIE-Screenshot aufgetreten. Der positive Wirkungsnachweis pro Attacke steht in der kontrollierten produktiven Automation; Fehlschläge im PIE sind in der Abnahme erhalten.

Der Fußlauf allein liefert keinen positiven sichtbaren Begleiter-Nachweis, wenn der alte Testspielstand kein entsprechendes 3D-Teammodell enthält. Die separate Controller-/Teamprobe bestätigt den tatsächlichen einzelnen Begleiter sowie seinen Wechsel und seine Kampfpause. Die reale Switch-Pro-Hardwareprüfung bleibt offen; die bestehende Belegung wurde nicht verändert.

Bekannte externe Editorwarnung: `idevice_id` aus dem iOS-Helferpaket der Engine startet auf diesem Mac nicht (`Bad CPU type in executable`). Sie steht getrennt in interaktiven Editorlogs. Der letzte strenge Automationslauf hatte selbst keine Warnungstests und Exit 0. Frühere Fehler sind nicht verborgen: Automation 02 scheiterte an zwei alten Testannahmen zu inzwischen erweiterten Lernlisten; beide wurden konkret korrigiert. Die ersten zwei neuen PIE-Prüfläufe enthielten Fehler im Prüfwerkzeug bezüglich regulär fehlgeschlagener Flucht und asynchronem Kampfabschluss; diese Läufe sind als fehlgeschlagen erhalten. Die korrigierten Läufe 03 und 04 bestehen mit jeweils 59 Fällen.

## Echte lokale Bildnachweise

Die folgenden Bilder stammen aus dem tatsächlichen Unreal-Viewport, keine Konzept- oder generierten Bilder. Die logische Prüfeinstellung war 2560×1440 bei 100 %. Die native Slate-Aufnahme beträgt tatsächlich 2331×1311 Pixel; es wurde nicht hochskaliert und keine native QHD-Auflösung behauptet. Alle Medien bleiben lokal und werden nicht in Git aufgenommen. Die Aufbauten enthalten bewusst kontrollierte Kampfwerte (z. B. 1000 KP) und sind keine natürliche Wildbegegnungs-/Balancingdemonstration.

Schlafwirkung in ClassicBattle:

![Echter PIE-Schlafstatus](/Users/harry/Developer/PokeMonster/Saved/GlumandaV11/LiveUI/CrystalCrystalProduction0411After/ActualSlateViewport.png)

Traumfresser – vorher:

![Traumfresser vorher](/Users/harry/Developer/PokeMonster/Saved/GlumandaV11/LiveUI/CrystalCrystalProduction0431Before/ActualSlateViewport.png)

Traumfresser – danach:

![Traumfresser danach](/Users/harry/Developer/PokeMonster/Saved/GlumandaV11/LiveUI/CrystalCrystalProduction0431After/ActualSlateViewport.png)

Bestehendes Meistermenü im ausdrücklich ungespeicherten technischen NPC-Aufbau:

![Repertoire beim Meister](/Users/harry/Developer/PokeMonster/Saved/GlumandaV11/LiveUI/CrystalMaster01_MasterRepertoire/ActualSlateViewport.png)

Alle 118 Produktionsaufnahmen und ihre einzelnen Pfade stehen in der JSON-Abnahme beziehungsweise im lokalen `Saved/MoveEffectsV4/CrystalProduction04`-Nachweis. Die sechs Lernfälle und die Meisteraufnahmen sind zusätzlich lokal erhalten.

## Speicher- und Dateischutz

Save-Schema 7 wird weiterverwendet. Alte Versionen, individuelle IDs, aktive Slots, dauerhaftes Repertoire, AP-Zustände und offene Angebote bleiben kompatibel. Groll aktualisiert dieselbe individuelle AP-Verwaltung; Entfernen/erneutes Aktivieren beim Meister erzeugt keine AP. Regelmäßige Heilung darf sie weiterhin regulär auffüllen.

Der ursprüngliche Entwicklerspielstand hat nach allen Prüfungen weiterhin SHA-256 `eeab48f3c5652ef6d24b7f386ee7c26973336c929edf39aa7f6593d407a913df`. Die 25 geschützten unversionierten Incoming-GLBs sind unverändert. Modelle, Animationen, Blender-Originale, Maps, Landschaft, Heilhaus, Licht, Eingabebelegung und Kameras wurden nicht bearbeitet. Die zehn Speziesassets wurden nur an ihren bestehenden Lernlisten gebunden; übrige Felder wurden stabil exportiert verglichen. Die 288 getesteten Runtime-Eingaben stimmen mit dem finalen 182er-Lauf überein.

Es besteht weiterhin nur der ursprüngliche aktive Worktree. Beide lokalen Vollbackup-Verweise zeigen unverändert auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`. Kein Reset, Clean, Force-Push, History-Rewrite, LFS-Prune, neuer Worktree oder neue Projektkopie wurde ausgeführt.

## GitHub- und LFS-Abgabe

Der ausdrücklich freigegebene kontrollierte Wiederholungsversuch für `2950a5ea` war erfolgreich; der Commit ist direkt auf GitHub bestätigt. Der Fehlernachtrag wurde separat als `0a26b6ed4a39ecf673a39464464b30b14b4064b9` geprüft, committed und erfolgreich gepusht. Beide Übertragungen benötigten keine neuen LFS-Objekte. Vor dem neuen Paket zeigt `origin/main` direkt weiterhin auf `0a26b6ed`.

Der geprüfte neue Paketumfang: 49 Move-Assets + zehn bestehende Speziesdateien, insgesamt 229963 LFS-Bytes. Nur benötigte Quellen, Daten, Werkzeuge und Dokumentation werden aufgenommen. Kontrollmedien, Saved-Ausgaben, Builds, Caches und die 25 Incoming-GLBs bleiben außerhalb des Commits. Lokaler LFS-Fsck besteht. Der neue Paketcommit und der abschließende Remote-/LFS-Status werden nach der gezielten Indexprüfung nachgetragen; es wird kein Push ohne bestätigte Kostenabsicherung vorgenommen.

Aktuelle offizielle Grenzen wurden geprüft: normale Git-Dateien dürfen höchstens 100 MiB groß sein; GitHub Free/Pro erlauben LFS-Dateien bis 2 GB. Das enthaltene Freikontingent beträgt 10 GiB; sein aktueller Rest und die Konto-Budgeteinstellung sind dadurch nicht bewiesen. Bei vorhandenem 0-USD-Budget blockiert GitHub Überschreitungen, bei entferntem Budget können Kosten entstehen. Quellen: [Git-Dateigrenzen](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github), [LFS-Dateigrenzen](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage), [LFS-Abrechnung und Budget](https://docs.github.com/en/billing/concepts/product-billing/git-lfs). Es wurden keine Käufe, Budget- oder Kontoeinstellungen vorgenommen.

Verbleibend: kostenfreie GitHub-/LFS-Sicherung bestätigen und regulär ausführen; physische Controller-Hardwareprüfung weiterhin Nutzeraufgabe. Kein weiterer Pokémon-, Landschafts-, Kamera- oder Animationsauftrag wurde begonnen.
