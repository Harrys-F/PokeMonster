# Attackenverwaltung V2 und Meister der Erinnerungen – Prüfbericht

Stand: 23.10.2026. Aktives Projekt ausschließlich
`/Users/harry/Developer/PokeMonster`; `main`, Ausgangscommit
`7a00f9b5ccd2431294c7c4cee9098a57d25c2daf`.
Zielkarte unverändert `/Game/Maps/Dev_TestMap_VisualV2`.

## Ergebnis und Umfang

Ein persönliches, dauerhaftes Attackenrepertoire ergänzt das vorhandene
Fortschrittssystem V1. Vier aktive Kampfslots bleiben erhalten. Tatsächlich
angenommene beziehungsweise nach V1 in freie Slots gelernte Attacken werden
individuell erinnert. Ersetzen entfernt keine Kenntnis. Abgelehnte und offene
Lernangebote sind keine erlernten Attacken. Zwei Pokémon derselben Art können
unterschiedliche Erinnerungen besitzen.

Das Reisebuch hat die zusätzliche Kategorie **Attacken**, erreichbar über X/Tab
und L/R. Sie zeigt die vier aktiven Plätze, das gesamte persönliche Repertoire,
Typ, Stärke, Genauigkeit, aktuelle/maximale AP und Wirkungsbeschreibung.
Unvollständige Effekte sind gekennzeichnet. Die Liste wird mit dem Cursor
weitergeschaltet; es werden nicht nur die ersten vier Kenntnisse angeboten.
**Im normalen Reisebuch ist kein aktiver Attackentausch möglich.**

Der kostenlose **Meister der Erinnerungen** ist als Dienst des bestehenden
`APokeMonsterNPC` implementiert. Er bietet Pokémon-Auswahl, Repertoire,
Entwurf, Ersatzplatzauswahl bei vier Attacken, Neuordnung, ausdrückliche
Abschlussprüfung und Bestätigen/Abbrechen. Ein neues Set enthält ein bis vier
eindeutige erlernte Attacken. Leere physische Restslots bleiben leer; es gibt
weiter exakt vier Kampfslots. Nicht erlernte Attacken werden nicht freigeschaltet.

**Weltintegration noch offen, Funktion vorbereitet und im transienten Test geprüft:**
Der Meister wurde nicht dauerhaft ins Startdorf oder Heilhaus gesetzt. Der
endgültige Standort bleibt ausschließlich für das versteckte optionale
Bruchtal-inspirierte Wissenstal reserviert.

## Wiederverwendete Systeme und Zugriffsschutz

- `FPokeMonsterCreatureInstance` und bestehende `FPokeMonsterMoveSlot`-Datensätze:
  Repertoire und AP je individueller Instanz, keine zweite Attackendatenbank.
- V1-Lernangebote, Kampfsession und vorhandener BattlePresenter: neue Attacken
  dürfen weiterhin unmittelbar im Levelaufstieg aktiviert werden. Bereits
  erinnerte inaktive Attacken werden dadurch nicht als neue Angebote ausgegeben.
- `FPokeMonsterOverworldViewBuilder` und vorhandenes OverworldWidget:
  reine Ansicht beziehungsweise lokaler Meisterentwurf, keine zweite Teamverwaltung.
- Bestehender NPC-Interactable, PlayerController und Nintendo-Eingang:
  B/E zur Interaktion; kein paralleles NPC- oder Eingabesystem.
- Bestehendes EncounterSubsystem und SaveSubsystem: eine private Transaktion
  prüft lebenden autorisierten NPC in Interaktionsreichweite, gleiche Welt,
  keinen Kampf, keine offenen Lernangebote und seit Menüöffnung unveränderte
  individuelle Daten. Nur dieser Produktionspfad ruft die private Loadout-Funktion.
- Speichern erfolgt über den vorhandenen verifizierten atomaren macOS-Speicherpfad.
  Schlägt das Schreiben fehl, wird die Laufzeitänderung zurückgenommen.
  Bestätigen schließt den Dienst. Abbrechen, Schließen und verlorene
  NPC-Reichweite verwerfen den Entwurf. Ein verschwundener NPC autorisiert nichts.

Andere Speziallehrer, unbekannte Attacken, Items/Währungen und Entwicklungs-
prüfungen wurden nicht implementiert. Die vorhandenen vorläufigen Regeln zu
früheren Tauschentwicklungen und fehlende Entwicklungsmodelle bleiben erhalten.

## Speicherung und Migration

Save-Schema **6** ergänzt stabile Move-IDs und AP für das persönliche Repertoire.
Versionen **1–5** bleiben lesbar. Bei ihrer Migration werden ausschließlich
nachweislich aktive Kenntnisse übernommen, niemals automatisch sämtliche
Lernlisteneinträge. Die schmale bestehende V1-Migration alter technischer
Glumanda-Testattacken bleibt erhalten.

Vor V2 vergessene Attacken, die damals nirgends gespeichert wurden, sind nicht
zuverlässig rekonstruierbar. Sie werden nicht erfunden. Offene Angebote bleiben
separat gespeichert und werden beim Laden auf gültige, eindeutige, noch nicht
gelernte Angebote geprüft. Doppelte Repertoireeinträge, ungültige AP und fehlende
aktive Kenntnisse werden vor der Übernahme eines Saves abgewiesen.

Historische technische Saves können dieselbe Attacke mehrfach aktiv enthalten.
Diese alten aktiven Slots bleiben kompatibel. Für die eindeutige Erinnerung gilt
konservativ der niedrigste vorhandene AP-Stand. Neue Meistersets sind eindeutig;
bei ihrer Zusammenstellung entstehen daraus keine zusätzlichen AP.

## AP-Verhalten

AP-Verbrauch synchronisiert die gespeicherte Erinnerung. Deaktivieren und
Reaktivieren kopiert den erhaltenen AP-Stand, statt ihn über eine neue
Attackenzuweisung aufzufüllen. Neuordnung und Save/Load verändern AP nicht.
Die reguläre vollständige Heilung restauriert aktive **und inaktive** AP.
AP-Höchstwerte stammen weiterhin aus den vorhandenen Attackendefinitionen.

Echter PIE-Nachweis mit zwei unterschiedlich entwickelten Schiggy:

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Tackle früher ersetzt, erneut aktiviert | 28/35 AP vorher und nachher |
| Aquaknarre im aktiven Set neu geordnet | 20/25 AP vorher und nachher |
| Repertoire nach Reaktivierung/Neuordnung | Fünf eindeutige Kenntnisse erhalten |
| Zweites Schiggy hat Aquaknarre abgelehnt | Weiter vier Kenntnisse, unverändert |
| Abschlussprüfung abbrechen | Vollständiger individueller Zustand unverändert, kein Save geschrieben |
| Bestätigen und anschließend Laden | Aktive Reihenfolge und alle inaktiven AP exakt erhalten |
| Bestehender ClassicBattle | Meister-/Oberweltmenü gesperrt, kein Loadout-Schreibzugriff |

## Standortbefund

`SPIELIDEE.md` nennt Bruchtal als atmosphärische Inspiration; der Auftrag
konkretisiert daraus den optionalen Wissensort. Im bestehenden Projekt ist kein
solches spielbares Gebiet mit dokumentiertem Zugang und reservierter
Gelehrtenhalle identifiziert.

Alle **elf vorhandenen Maps** wurden geladen und ihre Actor-Labels, Klassen,
Positionen und Tags inventarisiert. Auch die WestlandRegion, WestlandVillage
und AssetLibrary wurden berücksichtigt. Die Asset- und Actor-Suche nach
Bruchtal/Rivendell/Wissenstal/Gelehrten/Hidden Valley lieferte keine entsprechende
Platzierung. Vorhandene Tal- oder Architekturformen allein belegen keinen bereits
freigegebenen Wissensort. Die Inventur ist kein Beweis, dass jede unbenannte
Landschaftsform untersucht oder als neues Gebiet freigegeben wäre.

Deshalb wurde keine neue Map, keine Gebietskopie und keine Ersatzplatzierung
angelegt. Später genügt die Konfiguration eines vorhandenen `APokeMonsterNPC`
mit `Service = RememberMoves` an einem tatsächlich ausgearbeiteten Ort.

Der technische Nachweis verwendet ausschließlich im PIE erzeugte Instanzen
`TechnicalTest_MasterOfMemories`, 100 cm vor der Spielfigur. Zwei flüchtige
Test-Pokémon besitzen absichtlich unterschiedliche Lernhistorien.
**Diese Bilder zeigen einen technischen Menütest, keine fertige Talgestaltung.**
Bedienung und sichere Reproduktion: `Tools/MoveManagementV2/README.md`.

## Echte Unreal-Aufnahmen

Unveränderte native Slate-Aufnahmen aus echtem VisualV2-PIE, keine Konzeptbilder.
Logischer Spielviewport 2560×1440 bei 100 %, tatsächlich gespeicherte UI-Bilder
**2331×1311 Pixel**. Nicht hochskaliert und nicht als native QHD ausgegeben.
Kontrollmedien bleiben unter `Saved`, werden nicht auf GitHub hochgeladen.

- [Repertoire, reine Ansicht](/Users/harry/Developer/PokeMonster/Saved/GlumandaV11/LiveUI/MoveManagementUISafeFinal_ReadOnlyRepertoire/ActualSlateViewport.png)
- [Hinweis zur inaktiven Attacke](/Users/harry/Developer/PokeMonster/Saved/GlumandaV11/LiveUI/MoveManagementUISafeFinal_InactiveReminder/ActualSlateViewport.png)
- [Meister: Repertoire und Entwurf](/Users/harry/Developer/PokeMonster/Saved/GlumandaV11/LiveUI/MoveManagementUISafeFinal_MasterRepertoire/ActualSlateViewport.png)
- [Meister: ausdrückliche Abschlussprüfung](/Users/harry/Developer/PokeMonster/Saved/GlumandaV11/LiveUI/MoveManagementUISafeFinal_MasterReview/ActualSlateViewport.png)
- [Meister: geänderte Reihenfolge](/Users/harry/Developer/PokeMonster/Saved/GlumandaV11/LiveUI/MoveManagementUISafeFinal_MasterReorderedReview/ActualSlateViewport.png)
- [Gespeichertes Repertoire nach Laden](/Users/harry/Developer/PokeMonster/Saved/GlumandaV11/LiveUI/MoveManagementUISafeFinal_SavedRepertoire/ActualSlateViewport.png)

Die sechs bestehenden V1-Lernfälle liefern zusätzlich 20 reale UI-Aufnahmen
unter `Saved/CreatureProgressionV1/MoveManagementLearningFinal/Result.json`.

## Technische Prüfungen

| Prüfung | Ergebnis / Nachweis |
|---|---|
| Editor-Build Mac Development | Erfolgreich, 8,18 s; `Saved/ProjectRefinement/MoveManagementV2SafetyBuild/Result.json` |
| Vollständige Automation | **110/110 erfolgreich**, 0 SuccessWithWarnings, 0 fehlgeschlagen, 0 nicht ausgeführt; strenger QA-Wrapper Exit 0; `MoveManagementV2SafetyAutomation/Report/index.json` |
| Vier neue Automationstests | Lernen/Repertoire/AP; Save-Migration/offene Angebote; reine Ansicht/Controller-Entwurf; NPC-Ortsautorisierung |
| Elf Map Checks | Je **0 Fehler, 0 Warnungen**; `Saved/MoveManagementV2/MapChecksFinal.json` |
| Neuer echter PIE-Menütest | **18 Prüfungen**, sechs echte UI-Bilder; `Saved/MoveManagementV2/MoveManagementUISafeFinal/Result.json` |
| Bestehende V1-Lernfälle | **6/6**, ClassicBattle/WorldBattle, Ersetzen/Ablehnen, freie Slots, fehlendes Entwicklungsziel sicher blockiert |
| Bestehende Controller-Softwareprüfung | **46/46**, Eingabekontexte, Wiederholungssperren, L3, X, L/R, +, Teamtausch, ein Begleiter, Kampf, Items und Save/Load |
| Vollständiger Gameplay-Fußlauf | Zweiter Lauf mit **103/103 Schritten**, 289,46 m, maximal 315 cm/s, ohne Testteleports; Fußlauf, Zusatzbeobachter und Save-Restaurierung bestanden; `Saved/GlumandaV11/Acceptance/MoveManagementFootDiagnostic/` |
| Niederlagen-Autosave | Echter PIE-Niederlagenablauf, Rückkehr zum Heilpunkt, vollständige Heilung, Autosave und identisches Team nach Laden; `Saved/StarterExpansionV1/MoveManagementDefeatFinal/Result.json` |
| Schutz des technischen Testbefehls | Vorhandener Original-Slot: ausdrücklich verweigert, Party und SHA unverändert, kein Test-NPC erzeugt; `Saved/MoveManagementV2/FixtureGuard.json` |

**Zusätzlicher Prüfhinweis, nicht verschwiegen:** Der erste Fußlauf
`MoveManagementFullFootFinal` bestand zwar seine 103 Routenschritte (290,53 m),
sein ergänzender `CreatureGameplay.json`-Beobachter scheiterte jedoch bei einem
zufälligen Glurak-Kontakt an der strengen Positionsprüfung (< 0,01 cm). Die
Abweichung wurde im damaligen Hilfswerkzeug nicht numerisch aufgezeichnet;
ihre Ursache ist daher **nicht nachgewiesen behoben**.

Der unverändert strenge Beobachter protokolliert nun im Fehlerfall auch Delta,
Position und Geschwindigkeit. Der zweite vollständige Lauf
`MoveManagementFootDiagnostic` bestand auch diesen Beobachter; in seinen zwei
Kämpfen blieb die Position exakt erhalten. Er enthielt keinen zufälligen
Glurak-Kontakt. Eine zusätzliche gezielte echte Glurak-Kontaktprüfung mit
expliziter flüchtiger Positionierung und pausierter Umgebung-KI maß während des
ClassicBattle und nach zwei regulären Fluchtversuchen **0,0 cm Abweichung**,
bei unverändertem Original-Save (`Saved/MoveManagementV2/GlurakContactDiagnostic.json`).
Sie ist eine Kontaktdiagnose, kein zusätzlicher Fußlauf. Der sporadische erste
Hinweis bleibt zur Beobachtung offen; keine Kamera-, Kollisions- oder
Bewegungsänderung wurde auf Verdacht übernommen.

`Tools/MoveManagementV2/ValidateGameplay.py` wertet deshalb alle vorhandenen
Routen-, Zusatzbeobachter-, Begleiter- und Save-Belege aus. Es akzeptiert den
zweiten Lauf und würde den ersten ausdrücklich zurückweisen, statt sich allein
auf die positive Meldung des älteren Fußlauf-Runners zu verlassen. Der alte
Dev-Save nutzt technische Testarten ohne vollständige 3D-Begleiterdarstellung;
seine 647 Begleiter-Messpunkte allein belegen keinen sichtbaren Begleiter.
Der getrennte 46-Punkte-Controller-Test bestätigt dagegen echte einzelne
Glumanda-/Schiggy-Begleiter, Teamtausch und Kampf-Pausierung.

Ein früher Testbuild scheiterte am fehlenden vollständigen Move-Header im neuen
Test; er ist korrigiert. Der finale Build und die finale Automation sind erfolgreich.

**Warnungen getrennt:** Die Engine-Start-/Editorprotokolle enthalten weiterhin
externe `idevice_id`-/`Failed to launch Tool`-Warnungen wegen eines nicht passenden
iOS-Helfers. Der finale Automation-JSON meldet keine Testwarnungen und der strenge
Wrapper liefert Exit 0. Daraus folgt keine Behauptung eines insgesamt warnungsfreien
Engine-Logs. Keine Engine-Helfer, SDKs oder Warnfilter wurden verändert.

B bestätigen/interagieren, A zurück/abbrechen, Steuerkreuz, L/R-Kategorien,
X-Reisebuch und +-Hauptmenü verwenden den bestehenden Nintendo-Eingang.
Im Meister gibt es keinen Wechsel in andere Kategorien. **Alle neuen Eingabenachweise
sind Simulationen; der physische Switch-Pro-Test der neuen Menüabläufe bleibt offen.**

## Schutz und Grenzen

Alle Modelle, Animationen, Art-/Content-/Config-Dateien, Maps, Heilhaus,
Landschaft, Beleuchtung, Kamera, Spezies-Identitäten und Kampfansichten bleiben
unverändert. Der originale Dev-Save wird nach schreibenden Testfällen bytegenau
restauriert; SHA-256:
`eeab48f3c5652ef6d24b7f386ee7c26973336c929edf39aa7f6593d407a913df`.

Die 25 bereits unversionierten Incoming-Originale bleiben unverändert und werden
nicht aufgenommen. Das lokale Vollbackup `03492bd` und beide Backup-Verweise
bleiben erhalten, außerhalb der schlanken main-Historie. Keine neuen Maps,
Worktrees, Projektkopien oder vollständigen Backups. Save-Schutzdateien sind
gezielte Testvorkehrungen, keine neue Projektsicherung.

Offen bleiben die tatsächliche Weltplatzierung/visuelle Ausgestaltung des Meisters,
der physische Test der neuen Menüs, vor V2 nicht gespeicherte vergessene Attacken
sowie die bereits dokumentierten fehlenden Attackenwirkungen und Entwicklungsmodelle.
Dieser Auftrag schaltet keine unbekannten Techniken frei und baut das Tal nicht aus.
Der einmalige nicht reproduzierte Positionsbefund beim zufälligen Glurak-Kontakt
bleibt zusätzlich als offener QA-Hinweis erhalten; keine pauschale Aussage über
fehlerfreie sämtliche historischen Zusatzprotokolle.

## GitHub-Sicherung

Implementierung: **`219bca53f770374c8036cc39d1d268027d7d3d7f`**
(`feat: preserve learned moves and add memory master service`).
28 gezielt geprüfte Commitpfade; tatsächlicher Index gegen den expliziten Plan
und gegen die Arbeitsdatei-Bytes geprüft. `git diff --cached --check` erfolgreich.
Normaler neuer Git-Pack: **450.737 Bytes**, deutlich unter 1 GiB.
Regulärer Push `7a00f9b5 → 219bca53` erfolgreich, anschließend direkte
`git ls-remote`-Übereinstimmung sowie `origin/main` geprüft.
LFS-Prüfung: **0 neue Objekte, 0 Bytes**; deshalb kein LFS-Download oder neuer
LFS-Kontingentverbrauch behauptet. `git lfs status` meldet keinen ausstehenden
LFS-Upload. Keine Käufe, kein Force-Push und keine Backup-Refs übertragen.
Der Abschluss dieses Berichts wird separat als reine Dokumentationsbestätigung
gesichert; der endgültige main-Hash steht im Abschluss und im Git-Protokoll.
Nur notwendige native Quellen, reproduzierbare Testwerkzeuge und Dokumentation
werden gezielt aufgenommen. Keine Asset-, Save-, Kontrollbild-, Video- oder
Cachedateien. Die Änderung erzeugt keine neuen LFS-Objekte.


Lokale Nachweise zur Sicherung: `Saved/MoveManagementV2/CommitPlan.json`,
`IndexVerification.json`, `PushPlan.json`, `PushImplementation.json`,
`RemoteLFSImplementation.json` und `FinalGitVerification.json`.
Core-Manifest: 4.695 Pflichtdateien erfolgreich geprüft; keine bisherigen Einträge
entfernt. Nach dem Implementierungspush waren alle versionierten Dateien sauber;
nur die ursprünglichen 25 geschützten Incoming-Dateien blieben unversioniert.
