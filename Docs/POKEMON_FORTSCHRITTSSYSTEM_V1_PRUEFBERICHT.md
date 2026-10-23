# Pokémon-Fortschrittssystem V1 – Prüfbericht

Datum: 23.10.2026. Projekt: `/Users/harry/Developer/PokeMonster`.
Ausgang: `main` / `origin/main` = `1139280cf337b26be8ed06f0b198d057f57a06bb`.

**Abschluss: Bestehende Umsetzung technisch geprüft. Alle 106 Automationstests erfolgreich, davon ein Fall mit bekannten externen Engine-Warnungen; kein vollständig warnungsfreier QA-Lauf. Sechs wiederholte PIE-Lernfälle, elf Map Checks und Gameplay-/Save-Regression erfolgreich.**

## Bestandsaufnahme und Schutz

Die bestehende `CreatureInstance`/`CreatureProgression` berechnet bereits sechs
Wachstumskurven, Level 1–100, Statuswerte ohne IV/EV/Wesen und mehrere Level-Ups.
Ein Levelaufstieg erhält fehlende KP; eine kampfunfähige Kreatur wird nicht belebt.
Die bestehende BattleSession vergibt belegte Art-XP an lebende Teilnehmer am
jeweiligen Gegner, mit bestehender Rundung/Trainerbonus. Fang und Spielerflucht
vergeben keine XP. Diese Arbeitsregeln und die vereinfachte Kampfmathematik bleiben erhalten.

25 unversionierte Incoming-GLB wurden vor Beginn erfasst und nicht verändert,
importiert oder gestaged. Ein einziger aktiver Worktree; keine neue Map, Kopie oder
zusätzliches Vollbackup. Beide lokalen Vollbackup-Refs bleiben auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`.
Alle ursprünglichen Art-, Map- und Config-Dateien sowie der Dev-Spielstand sind
gegen den Beginn geprüft. Erlaubte bestehende Binäränderungen betreffen genau die
zehn Spezies-Data-Assets, keine Visuals/Modelle/Animationen oder Encounter-Habitate.

## Tatsächlich implementiert

- Chronologisch geordnete Lernangebote beim Überschreiten eines Lernlevels, auch
  bei mehreren Level-Ups. Bekannte/wartende Attacken werden nicht doppelt angeboten.
- Freie Plätze werden wie bisher automatisch gefüllt, nun mit sichtbarer Meldung.
- Bei vollem Set hält die vorhandene Kampfpräsentation vor Begegnungsabschluss
  oder Gegnerwechsel an. Die vier vorhandenen Attackenbuttons wählen den Ersatz;
  Ablehnen beendet genau dieses Angebot. Keine automatische Verdrängung.
- B/Enter bestätigt, A/Esc lehnt ab, Steuerkreuz/Pfeile navigieren. Keine neue
  Eingabebelegung. Andere Kampfaktionen sind während der Lernentscheidung gesperrt.
- Ersetzen füllt nur die neue Attacke auf volle AP; andere AP, KP und IDs bleiben
  erhalten. Lernen verbraucht keinen zusätzlichen Kampfzug.
- Levelmeldungen enthalten das vorherige und neue Level. Nicht implementierte
  Lernattacken werden ausdrücklich als noch nicht spielbar gemeldet.
- Save-Schema 5 ergänzt offene Lernangebote als stabile Primary Asset IDs.
  Versionen 1–4 bleiben lesbar. Warteschlangen werden atomar auf gültige, eindeutige,
  noch nicht bekannte und zum Level zulässige Attacken geprüft.
- Die bestehende Entwicklungsprüfung erhält eine getrennte Prüfung auf fehlende
  Zielart, fehlende gültige Darstellung und verfügbare Zieldefinition/Darstellung.
  Kein Modelltausch und kein Itemverbrauch durch eine bloße Eignungsprüfung.

## Verifizierte Lernlisten und Grenzen

Quelle: öffentliche [PokeAPI-Daten](https://github.com/PokeAPI/pokeapi/tree/2bf639e5572812a67d2b94903fdcb9d095f5aeb2/data/v2/csv),
Gold/Silber, Versionengruppe 3. Acht Roh-CSV-URLs mit SHA-256 und die extrahierten
Daten liegen in `Tools/CreatureProgressionV1/Gen2Reference.json`.
Historische Werteänderungen wurden feldweise zurückgerechnet; keine ROM-Datei,
fremde Bilddaten oder neue Pokémon-Modelle übernommen.

| Art / stabile interne Identität | Level-Einträge | Mit unterstützter Mechanik | Noch nicht spielbare Einträge |
|---|---:|---:|---:|
| Bisasam | 11 | 4 | 7 |
| Zunderlauf | 10 | 4 | 6 |
| Glurak | 13 | 6 | 7 |
| Schiggy | 11 | 6 | 5 |
| Pikachu | 11 | 4 | 7 |
| Myrapla | 8 | 1 | 7 |
| Enton | 8 | 3 | 5 |
| Machomei | 11 | 2 | 9 |
| Nebulak | 9 | 1 | 8 |
| Gengar | 10 | 1 | 9 |

Insgesamt 102 Einträge / 68 unterschiedliche Attacken. Davon 19 Attacken mit
unterstützter Mechanik; 49 Spezialwirkungen noch nicht vollständig implementiert.
Nicht verfügbare Attacken verbleiben in derselben Lernliste mit Name, Level und
Begründung, ohne funktionslose Ersatzassets oder erfundene Wirkung.

Unterstützt: Kratzer, Flügelschlag, Slam, Rankenhieb, Tackle, Rutenschlag, Silberblick,
Heuler, Glut, Flammenwurf, Aquaknarre, Hydropumpe, Geowurf, Absorber, Egelsamen,
Ruckzuckhieb, Nachtnebel, Panzerschutz und Blubber. Das ist keine Behauptung einer
vollständigen Gen-2-Kampfsimulation: STAB, Volltreffer und zahlreiche Spezialregeln
sind weiterhin offen. Daher werden etwa Schlitzer/Rasierblatt nicht als vollständig
unterstützt ausgegeben. Besonders Myrapla, Nebulak und Gengar haben bislang nur
wenige spielbare Lernattacken.

Drei neue Assets unter `/Game/Data/Moves/ProgressionV1`:

| Attacke | Stärke | Genauigkeit | AP | Wirkung im bestehenden System |
|---|---:|---:|---:|---|
| Flammenwurf | 95 | 100 % | 15 | Feuer-Spezialschaden, 10 % Verbrennung |
| Slam | 80 | 75 % | 20 | normaler physischer Schaden |
| Hydropumpe | 120 | 80 % | 5 | Wasser-Spezialschaden |

Keine bestehenden Originalattackenwerte wurden überschrieben. Panzerschutz besitzt
in den Originaldaten keine gegnerische Trefferprüfung; seine Selbstwirkung wird in
der vorhandenen API mit bedingungslosem Erfolg abgebildet, nicht als neu erfundene
Originalgenauigkeit.

**Altbestand Glumanda:** Interne ID `Zunderlauf`, Prototyp-Dexnummer 1002,
MediumFast-Kurve und frühere Basiswerte bleiben erhalten. Andere neun Arten nutzen
ihre vorhandenen artspezifischen Kurven. Ein stiller Wechsel von Glumanda auf die
Originalkurve MediumSlow könnte bisherige kumulative XP ungültig machen; diese
Migration ist ausdrücklich offen. Bestehende individuelle Attackensets werden
nicht beim Laden durch eine neue Standardliste ersetzt.

## Vorbereitete Entwicklungen

| Art | Vorbereitete Bedingung | Ziel | Verfügbarkeit |
|---|---|---|---|
| Bisasam | Level 16 | Bisaknosp | Zielart/Modell nicht integriert |
| Glumanda / Zunderlauf | Level 16 | Glutexo | Zielart/Modell nicht integriert |
| Schiggy | Level 16 | Schillok | Zielart/Modell nicht integriert |
| Myrapla | Level 21 | Duflor | Zielart/Modell nicht integriert |
| Enton | Level 33 | Entoron | Zielart/Modell nicht integriert |
| Nebulak | Level 25 | Alpollo | Zielart/Modell nicht integriert |
| Pikachu | Itemkontext ThunderStone | Raichu | Zielart/Modell und reguläres Item noch nicht integriert |
| Machomei, Gengar, Glurak | Keine weitere Gen-2-Entwicklung | – | Keine künstliche Entwicklung ergänzt |

Vorhandene unversionierte GLB zählen nicht als bereits integrierte Zielmodelle und
bleiben geschützt. Level-/Item-/Freundschafts-/Orts-/Prüfkontexte sind wiederverwendbar.
Freundschaftszuwachs, finale frühere Tauschentwicklungen, spezielle Orte/Prüfungen,
Itembedienung und eine vollständige visuelle Entwicklungssequenz bleiben offen.
Die bisherigen Beispiele (Kadabra ungefähr 44, Maschock ungefähr 36 usw.) wurden
nicht eigenmächtig zu endgültigen Regeln erklärt. Keine Entwicklung wird nur wegen
einer erfüllten Bedingung als erfolgreich abgeschlossen gemeldet.

## Echte PIE-Ergebnisse

`Saved/CreatureProgressionV1/ProgressionUIFinal04/Result.json`: alle sechs Fälle beim Abschluss erneut bestanden.
Gewöhnlicher PIE-Start der unveränderten VisualV2, anschließend ausdrücklich
isolierte Laufzeitfixtures mit kanonischen Pokémon knapp vor dem nächsten Level
und einem 1-KP-Gegner. Der Treffer, XP-Ertrag und die Oberfläche verwenden die
bestehenden echten Systeme. Dies ist kein Nachweis natürlicher Habitatbegegnungen.

| Modus | Fall | Ergebnis |
|---|---|---|
| ClassicBattle | Schiggy 12 → 13, Ersetzen mit B | Rutenschlag durch Aquaknarre ersetzt; vier Slots |
| ClassicBattle | Schiggy 12 → 13, Ablehnen mit A | Ursprüngliche vier Attacken erhalten |
| WorldBattle | Gleiche Ersatzwahl | Bestanden, keine Änderung des Darstellungsmodus |
| WorldBattle | Gleiche Ablehnung | Bestanden |
| ClassicBattle | Glumanda 6 → 7, freier Slot | Glut gelernt; vierter Slot bleibt leer |
| ClassicBattle | Glumanda 15 → 16 | Fehlende Entwicklung gemeldet, Originalart erhalten |

Schiggy erhält jeweils 92 XP (Ertrag 65 × Gegnerlevel 10 / 7), endet bei 1352 XP,
Level 13, 32/34 KP. Zwei fehlende KP bleiben erhalten. Keine zusätzliche Lernrunde.
Die Rückkehrposition stimmt mit dem Beginn überein. B/A/Steuerkreuz sind simulierte
Softwareeingaben, kein physischer Switch-Pro-Hardwaretest.

Vorher-/Nachher-SHA des Dev-Slots jeweils
`eeab48f3c5652ef6d24b7f386ee7c26973336c929edf39aa7f6593d407a913df`.
Diese sechs Fälle schreiben keinen Spielstand.

## Bildnachweise

Echte unveränderte Slate-Spieloberflächen, **2331 × 1311 Pixel**. Der logische
Gameviewport war 2560 × 1440, seine Screenshotgröße wird nicht mit der tatsächlichen
Slate-Bildgröße gleichgesetzt. Keine Hochskalierung und keine generierten Bilder.
Kontrollmedien bleiben lokal im ignorierten Saved und werden nicht hochgeladen.

![Vor dem Levelaufstieg – vier bestehende Attacken](../Saved/GlumandaV11/LiveUI/ProgressionUIFinal04_0_Before/ActualSlateViewport.png)

![Nach dem Levelaufstieg – Aquaknarre ersetzen oder ablehnen](../Saved/GlumandaV11/LiveUI/ProgressionUIFinal04_0_Learning/ActualSlateViewport.png)

![Gleiche Lernentscheidung in WorldBattle](../Saved/GlumandaV11/LiveUI/ProgressionUIFinal04_2_Learning/ActualSlateViewport.png)

Die frühere `ProgressionUI02`-Reihe bestand mechanisch, deren normaler Shot-Befehl
ließ aber die Kampf-UI weg. Sie ist kein visueller Lernnachweis. Die erste
`ProgressionUI03`-Treiber-Endprüfung forderte irrtümlich exakte QHD-Slate-Maße und
schlug an der Größenannahme fehl; die sechs funktionalen Fälle bestanden. Der
Treiber prüft jetzt native Maße und dokumentiert sie in `CaptureValidation.json`.

## Technische Abschlussprüfung

Die vorhandene Umsetzung wurde abgeschlossen, keine neue Implementierungsrunde,
keine weiteren Modelle oder Maps. Der zuvor korrigierte Negativtest wurde zuerst
isoliert und danach innerhalb der vollständigen Automation ausgeführt.

| Prüfung | Tatsächliches Ergebnis | Lokaler Nachweis |
|---|---|---|
| Mac Development Editor Build | Erfolgreich, Exit 0, 7,93 s | `Saved/ProjectRefinement/ProgressionV1Build05/Result.json` |
| Korrigierter Negativtest | 1/1 erfolgreich, keine Warnung / kein Testfehler | `ProgressionV1Negative02/Report/index.json` unter Saved/ProjectRefinement |
| Vollständige Automation | 106 erfolgreiche Testfälle; 105 ohne Warnung, 1 mit 2 externen Warnmeldungen; 0 Fehler / 0 ausgelassen / 0 laufend | `ProgressionV1Automation02/Report/index.json`, `Saved/CreatureProgressionV1/AutomationFinalAssessment.json` |
| Alle fünf neuen Progressionstests | Erfolgreich | XP-Verteilung, Lernwahl/Vier-Slot-Grenze, Battle-Sperre, Save/Legacy/Negativfall, fehlendes Entwicklungsziel |
| Zehn Spezies / 102 Lernlisteneinträge | Erfolgreich, auch Wirkungs-ID und Chance der 19 unterstützten Attacken geprüft | `Saved/CreatureProgressionV1/DataValidation.json` |
| Elf vorhandene Map Checks wiederholt | Je 0 Fehler / 0 Warnungen | `Saved/CreatureProgressionV1/MapChecksFinal.json` |
| Sechs echte PIE-Lernfälle wiederholt | Erfolgreich in bestehender VisualV2 | `Saved/CreatureProgressionV1/ProgressionUIFinal04/Result.json` |
| Vollständiger echter PIE-Fußlauf | Erfolgreich: 103 Schritte, 286,95 m, Sprint 315 cm/s, keine Testteleports | `Saved/GlumandaV11/Acceptance/ProgressionV1FullFoot01/FootTest.json` |
| Controller-/Team-/Save-Regression | 46 Prüfungen erfolgreich; simuliert, kein physischer Hardwaretest | `Saved/ProjectRefinement/ProgressionV1SwitchPro01.json` |
| Ursprünglicher Dev-Save restauriert | Nach beiden schreibenden Gameplaytests bytegleich | jeweilige `SaveRestored.json` / `ProgressionV1SwitchPro01_SaveRestored.json` |

Der Fußlauf prüft normale Bewegung und Sprint in acht Richtungen, Wanderer/Liora,
Dialog-/Questabläufe, Kampf und Fang, Brücke und Wald, mehrere Heilhauszugänge,
Innenkamera, Heilen/Checkpoint, Menü und Save/Load. Seine ursprüngliche ältere
Test-Water-Party liefert keine sichtbare 3D-Begleiterfreigabe (617 Begleitersamples,
aber keine bestätigte sichtbare 3D-Instanz). Diese Lücke wird **separat** durch die
Controller-/Team-Fixture geschlossen: tatsächlicher einzelner Glumanda-Begleiter,
Umordnung auf Schiggy, Pausieren/Verbergen in ClassicBattle und korrekte Rückkehr.
Die Controller-Fixture verwendet ausgewiesene Laufzeit-Testteams und einzelne
Diagnosepositionierungen; sie wird nicht als teleportfreier Fußlauf ausgegeben.

### Externe Warnungen und ursprünglicher Fehler

Die vollständige Automation beendet Unreal mit **Exit 0**. Der strengere vorhandene
`ProjectQA.py`-Wrapper liefert **Exit 1**, weil er auch erfolgreiche Tests mit Warnung
ablehnt. Im einzigen betroffenen Test
`PokeMonster.NPC.MotionV2.IsolationSpeedAndSkeleton` stehen ausschließlich zwei
Meldungen zum externen iOS-Helfer `idevice_id` (Bad CPU type, Prozess nicht startbar).
Alle 106 Tests haben Zustand `Success` und 0 Testfehler. Die vollständigen
Warnmeldungen wurden separat geprüft und erhalten; keine Unterdrückung, keine
Engine-/Pollingänderung und kein Wiederholungslauf nur für ein grünes Zeitfenster.
Daher ist dies ein erfolgreicher Funktionsteststand **mit bekannter externer
Warnung**, kein vollständig sauberer QA-Wrapper-Lauf. Nicht verfügbare fremde
Plattform-SDKs beim Start sind ebenfalls kein fehlgeschlagener Mac-Build.

Der erste vollständige Lauf `ProgressionV1Automation01` bleibt ein tatsächlicher
abgebrochener Fehlversuch: Der neue Negativtest fügte ein Element aus einem TArray
direkt in dasselbe Array ein. Unreal beendete diese Testoperation mit Assertion.
Die bereits vorbereitete Korrektur kopiert das Element vorher. Der isolierte
Neulauf und die komplette Suite bestätigen jetzt sowohl den Disk-Roundtrip offener
Lernangebote als auch die atomare Ablehnung einer absichtlich doppelten Warteschlange.
Save-Versionen 1–4 werden im selben Test über versionierte Test-Snapshots geladen;
individuelle IDs/XP/AP bleiben entsprechend den bisherigen Regeln erhalten.
Der bestehende reale Dev-Spielstand wurde zusätzlich im gewöhnlichen PIE geladen
und nach den schreibenden Gameplay-Prüfungen bytegleich wiederhergestellt. Der ursprüngliche Fehler wird nicht
als externe Engine-Warnung umgedeutet.

### Auflösung der beiden blockierten Prozesse

42548 war weiterhin der fehlgeschlagene Start vor Projektladung mit relativem
Projektpfad. 43865 war weiterhin die abgestürzte unbeaufsichtigte Automation01.
Exakte Befehlszeilen und Absturzhandler wurden erneut geprüft. Beide reagierten
auch erneut nicht auf reguläre Beendigung/SIGTERM. Ausschließlich diese beiden
bestätigten Prozesse wurden danach mit der ausdrücklichen Nutzer-Ausnahme beendet.
Keine anderen Prozesse, keine Nutzerpakete, keine allgemeine Force-Quit-Regel und
keine Projekt-/Git-Konfiguration wurden geändert.
Nachweis: `Saved/CreatureProgressionV1/AuthorizedProcessResolution.json` plus die
beiden erneuten Stackproben. Der anschließend korrekt gestartete Editor verwendet
den vollständigen Projektpfad. Der früher abgewiesene Build04 bleibt als nicht
begonnener Versuch dokumentiert, nicht als erfolgreicher Build.

## Abschließende Funktionseinschätzung

- XP und Level-Ups einschließlich mehrerer Level und Cap 100: geprüft.
- Aktualisierung der Statuswerte und Erhalt fehlender KP / kein Wiederbeleben: geprüft.
- Automatisches Lernen in freie Plätze, Ersetzen, Ablehnen und höchstens vier Slots: geprüft.
- Offene Lernangebote: echter Disk-Roundtrip, Legacy-Laden und sichere Ablehnung
  beschädigter Angebote geprüft. Kein Verlust anderer Attacken-AP oder Instanz-IDs.
- Entwicklung bei fehlendem Zielmodell: sicher vorbereitet/blockiert, kein Platzhaltertausch.
- Bestehende Kampfmodi, Fang/Heilung, Team/Begleiter und Save/Load: Regression bestanden.
- Alle 25 ursprünglichen unversionierten GLB, Originalquellen, Modelle/Animationen,
  Karten, Konfiguration, Dev-Save und Vollbackup-Refs bleiben erhalten. Die zehn
  Speziesdefinitionen ändern nur die geplanten Lerndaten/Entwicklungsbedingungen;
  bestehende Art-Identitäten, Basiswerte, Wachstumskurven und Visuals bleiben erhalten.

**V1 ist als technisch geprüfter Fortschritts-Zwischenstand verwendbar.** Die offen
gekennzeichneten 49 Attackenwirkungen, fehlenden Entwicklungsmodelle/-sequenzen,
Freundschaftsökonomie, endgültigen früheren Tauschentwicklungen und die sichere
Originaldatenmigration von Zunderlauf bleiben außerhalb dieses Abschlusses offen.
Ein allgemeines Oberwelt-Trainings-/Attackenerinnerungsmenü ist noch nicht enthalten;
außerhalb des Kampfes gespeicherte Restangebote werden beim nächsten Kampf gezeigt.
Physischer Switch-Pro-Hardwaretest wird durch die Simulationen nicht ersetzt.

## GitHub-Sicherung

Nur die bereits vorbereiteten notwendigen Quell-, Daten-, Werkzeug- und
Dokumentationsdateien werden nach Index-/Schutz-/LFS-Prüfung aufgenommen.
Keine Kontrollbilder, Videos, Rohlogs, Testspielstände, Caches oder Incoming-Unikate.
Regulärer Push auf bestehendes `origin/main`; keine Backup-Refs, kein Force-Push,
keine Historienänderung und keine kostenpflichtige Aktion. Der bestätigte Commit
und das tatsächliche Remote-/LFS-Ergebnis werden nach dem Push hier ergänzt.
