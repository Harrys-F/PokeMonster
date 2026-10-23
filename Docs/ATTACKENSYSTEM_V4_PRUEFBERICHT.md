# Attackensystem V4 – Prüfbericht des gemeinsamen Effekt-Teilpakets

**Stand: 23.10.2026. Technische Grundlage geprüft; vollständiger V4-Auftrag noch offen.**

## Ergebnis und tatsächlicher Umfang

Der Bestand bestätigt 49 gesperrte kanonische Lernattacken. Es fehlen jedoch nicht 49 unabhängige Systeme: Sie teilen sich Effektbausteine und verwenden 40 unterschiedliche Metadaten-Effektkennungen. Der Gesamtbestand umfasst 68 kanonische Lernattacken, davon weiterhin 19 produktiv unterstützt; tatsächlich existieren 22 Move-Assets einschließlich drei historischer Testattacken.

**Neue produktive Originalattacken: 0. Noch nicht vollständig angebundene Originalwirkungen: 49.** Dieses Teilpaket ersetzt diese Zahl nicht durch eine Anzahl technischer Bausteine. Die gemeinsame Architektur ist implementiert und geprüft, die endgültige Gen-2-Datenbindung und mehrere Mehr­runden-/Sondermechaniken stehen aus.

Bestand mit ID, Name, Typ, Kategorie, Stärke, Genauigkeit, AP, vorhandener Wirkung und Quellen: [vollständige Tabelle](/Users/harry/Developer/PokeMonster/Docs/ATTACKENSYSTEM_V4_BESTAND.md), maschinenlesbar im begleitenden Bestands-JSON. Jede der 49 verbleibenden Wirkungen ist im [Wirkungsplan](/Users/harry/Developer/PokeMonster/Docs/ATTACKENSYSTEM_V4_WIRKUNGSPLAN.json) einzeln beschrieben.

## Implementiert

- Typisierte, kombinierbare Effektlisten in vorhandenen Move-Daten; kompatible Übersetzung bestehender Kennungen, keine parallele Kampflogik.
- Elf validierte Bausteinarten: sieben gemeinsame Statuswertstufen; Primärstatusgrundlagen; Heilung; Absorption; Rückstoß; Fixschaden; Mehrfachtreffer; Zurückschrecken; Verwirrung; Rundenschutz; Team-Spezialschutz. Teilweise erweitern sie bereits vorhandene Wirkungen, statt elf neue Originalattacken darzustellen.
- AP-Verbrauch, Bedingungen, Immunitäten aus expliziten Effektdaten, Grenzen, tatsächlicher Schaden statt Overkill, KO-Abbruch von Mehrfachtreffern und Rückstoß-Ohnmacht. Kontrollierter sitzungsinterner Zufallsstrom; abgewiesene Runden verändern weder AP noch Zufall oder Rundenzahl.
- Erweiterte Primärstatusregeln sind ausdrücklich opt-in und in normalen Begegnungen nicht aktiviert. Die technischen Tests prüfen diese Regeln als konfigurierbares Profil, nicht als endgültig vollständige Originalwirkung von Paralyse, Schlaf, Gift oder Eis.
- Save-Schema 7 mit validiertem individuellem Schlafzähler; Migration der Versionen 1–6, Identitäten, Repertoire und AP bleiben erhalten. Ältere Builds mit Schema 6 können neue Schema-7-Saves nicht rückwärts lesen; der ursprüngliche Entwickler-Spielstand wurde nicht konvertiert oder verändert.
- Gemeinsame UI-Statuskürzel und Ereignismeldungen; kumulierte Mehrfachtreffer-KP-Animation; Heilungs-/Rückstoß-/Residualdarstellung über vorhandene Pfade. Eine tatsächlich erkannte falsche „keine Wirkung“-Rückmeldung bei wirksamen Statuskombinationen wurde korrigiert und getestet.
- Unfertige Effektarten, Volltrefferboni, ungültige Brüche, Verteilungen und doppelte Treffersteuerungen werden abgewiesen. Keine scheinbar vollständigen Attacken durch stille Platzhalter.

Details: [Architektur](/Users/harry/Developer/PokeMonster/Docs/ATTACKENSYSTEM_V4_ARCHITEKTUR.md), [Werkzeuge](/Users/harry/Developer/PokeMonster/Tools/MoveEffectsV4/README.md).

## Bewusst unveränderte Kampfregeln

Die bestehende vereinfachte Schadensformel bleibt erhalten: Level, passende offensive/defensive Werte, Stärke, Typen und bisherige Stufen/Verbrennung; weiterhin kein STAB, keine Volltreffer und keine Schadensstreuung. Die bisherige individuelle Physical-/Special-Kategorisierung bleibt erhalten. Priorität, Initiative und bisherige deterministische Gleichstände werden nicht pauschal umgestellt. Kein neues Balancing durch vermutete Originalregeln.

Bisherige Spezies-, Attacken- und Save-Identitäten, ClassicBattle-/WorldBattle-Kameras, Modelle, Animationen, Heilhaus und Landschaft bleiben erhalten. Die vier aktiven Slots und ortsgebundene Neuordnung beim Meister werden nicht umgangen.

## Noch offen und entscheidungsabhängig

Die angefragte Regelentscheidung ist noch unbeantwortet: Sollen neue Status-/Spezialwirkungen nach Gold/Silber gelten, während bestehende Kategorien und vereinfachter Schaden bestehen bleiben, oder sollen nur bereits ausdrücklich festgelegte Regeln ergänzt werden? AGENTS.md verlangt: „offene Fragen nicht eigenmächtig als endgültig entschieden behandeln.“ Das ist keine technische Uploadsperre, sondern eine noch fehlende Designfestlegung.

Unabhängig davon sind weitere Implementierungen nötig: Aufladen/Zugbindung, Bindung und Flucht-/Wechselsperren, Aussetzer/Groll mit Repertoire-AP-Synchronisierung, Raserei/Blättertanz, Wetter und wetter-/tageszeitabhängige Heilung, Scharfblick, Turbodreher-Befreiung, Psycho-Plus, Fluch und Abgangsbund. Erhöhte Volltrefferquoten/Energiefokus sind mit dem bisherigen Ausschluss von Volltreffern nicht stillschweigend als vollständig lösbar.

Vor produktiver Datenbindung sind insbesondere genaue Schlaf-/Verwirrungsdauern, Immunitäten, Auftauen durch Feuer, Schutzfolgechancen, Wetterausnahmen und Sonderfälle abzugleichen. Kein neues aufwendiges VFX-Paket: spezifische grafische Spezialeffekte bleiben offen; korrekte Spielwirkung wird davon nicht abhängig gemacht.

## Prüfungen

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Editor-Build `MoveEffectsV4Build09` | Exit 0 |
| Vollständige Automation `MoveEffectsV4Automation06` | 120 erfolgreich, 0 Warnungsfälle, 0 Fehler, Wrapper Exit 0 |
| Neue Effekt-Automation | 10 Tests; Konfiguration, sieben Stufen, Wahrscheinlichkeit/Immunität/Alt-Zufallsfolge, Statusaktionen, Heilung/Drain/Rückstoß, Mehrfachtreffer/Fixschaden/Voraussetzung, Schutz/Verwirrung/Wechsel, Screen, atomare Ablehnung, Save-Migration |
| Elf Map Checks, Gameplay-Build 07 | Je 0 Fehler / 0 Warnungen; keine Karte gespeichert |
| Echte Effekt-PIE-Fälle `EffectsFinal01` | 20 Fälle; alle zehn Modelle, beide Kampfmodi, neun technische Effektfälle, AP und Rückkehr |
| Fortschritt/Lernen | 6 PIE-Fälle: Ersetzen, Ablehnen, freier Slot und blockierte Entwicklung ohne Zielmodell |
| Meister der Erinnerungen | 18 PIE-Prüfungen; Repertoire/AP, Abbruch, Speichern, Sortieren, Kampf-Sperre; technischer ungespeicherter NPC |
| Controller-Software | 46 Prüfungen bestanden; B/A, L3, X, L/R, Plus, Fokus, Kampf/Team/Begleiter und Save/Load |
| Niederlage | Rückkehr, automatisches Speichern und erneutes Laden bestanden |
| Vollständiger Gameplay-Fußlauf | 103 Schritte, 289.20 m, ohne Testteleports; ergänzender Kampf-Beobachter ebenfalls bestanden |
| Spielstandschutz | Ursprünglicher Entwickler-Save nach allen Prüfungen exakt wiederhergestellt |

Der Fußlauf verwendet einen historischen Test-Teamstand. Seine Begleiter-Messung ohne sichtbares 3D-Begleitermodell ist kein positiver Sichtnachweis; die separate Controller-Fixture prüft den einzigen echten Begleiter, Teamplatzwechsel, Pause und Rückkehr. Der physische Switch-Pro-Test wurde nicht erneut durchgeführt; die bestehende reale Grundbelegung bleibt unverändert.

### Frühere Fehl-/Warnungsläufe

- `EffectsReview01` scheiterte am falschen Enum-Textvergleich des neuen Prüfwerkzeugs. Der tatsächliche Statuseffekt war im Ereignisprotokoll bereits vorhanden. Vergleich korrigiert; `EffectsReview02` und `EffectsFinal01` bestehen jeweils alle 20 Fälle.
- `MoveEffectsV4Automation02` und `03`: jeweils 119 warnungsfreie Tests plus 1 erfolgreicher Test mit externen Warnungen, 0 fachliche Fehler; **strenger Wrapper jeweils Exit 1, nicht als bestanden gewertet**.
- Die Warnungen stammen von `Engine/Extras/ThirdPartyNotUE/libimobiledevice/Mac/idevice_id`: `Bad CPU type in executable` und fehlgeschlagener Toolstart. Keine Filterung, keine Wrapper-Abschwächung und keine Engine-Konfigurationsänderung. Die Läufe 04, 05 und der endgültige Lauf 06 sind vollständig grün; frühere Warnungen bleiben dokumentiert. Rohlogs können außerdem externe Startup-/Plattformwarnungen enthalten – kein pauschal warnungsfreies Unreal behauptet.

Maschinenlesbare Ergebnisse: [Prüfzusammenfassung](/Users/harry/Developer/PokeMonster/Docs/ATTACKENSYSTEM_V4_TESTERGEBNISSE.json). Vollständige lokale Logs und JSON-Nachweise liegen unter Saved/MoveEffectsV4, Saved/ProjectRefinement sowie den wiederverwendeten Prüfwerkzeug-Verzeichnissen.

### Abschließender Kompatibilitätsnachtrag

Nach dem vollständigen Gameplay-Durchlauf wurden zwei eng begrenzte Grenzfälle zusätzlich abgesichert: Alte garantierte Stufen-/Drain-/Fixschadeneffekte ignorieren ihr historisch ungenutztes Wahrscheinlichkeitsfeld weiterhin; nach einem Verwirrungs-Selbsttreffer mit anschließendem Verbrennungs-KO wird keine weitere gegnerische Aktion ausgeführt. Beides ist mit deterministischen Regressionstests abgedeckt. Build 09 und die vollständige Automation 06 bestehen, jeweils Exit 0, 120 erfolgreiche Tests ohne Warnungsfall.

Die 20 Effekt-PIE-Fälle, Lern-/Meister-/Controller- und Fußlaufprüfungen sowie elf Map Checks wurden mit Build 07 durchgeführt. Der kleine Nachtrag verändert weder Assets noch aktuelle Produktionsparameter; deren 22 Move-Assets sind weiterhin identisch. Kein erneuter vollständiger Fußlauf auf Build 09 behauptet; die betroffenen zusätzlichen Daten-/Statuskombinationen sind im finalen automatisierten Lauf gezielt geprüft.

## Echte Unreal-Aufnahmen

Alle Aufnahmen stammen aus dem vorhandenen Projekt. Die Effektfälle verwenden ausdrücklich technische, transiente Attacken mit Prüfwerten, nicht neue endgültige Originalattacken. 40 finale native UI-Aufnahmen zu 20 Fällen; logischer Viewport 2560×1440, tatsächliche Slate-Dateien 2331×1311, nicht nachträglich skaliert. Keine Konzeptbilder als Umsetzungsnachweis.

### ClassicBattle – vor und nach technischem Paralyse-Test

![Vorher: kein Status](/Users/harry/Developer/PokeMonster/Saved/GlumandaV11/LiveUI/EffectsV4EffectsFinal011Before/ActualSlateViewport.png)

![Nachher: PAR-Status aus tatsächlichem Effekt](/Users/harry/Developer/PokeMonster/Saved/GlumandaV11/LiveUI/EffectsV4EffectsFinal011After/ActualSlateViewport.png)

### WorldBattle – derselbe technische Effektpfad

![WorldBattle mit PAR-Status](/Users/harry/Developer/PokeMonster/Saved/GlumandaV11/LiveUI/EffectsV4EffectsFinal0111After/ActualSlateViewport.png)

Weitere Vorher-/Nachher-Dateien und Ereignisse je Pokémon: `Saved/MoveEffectsV4/EffectsFinal01/Result.json`; Lern-/Meister-Aufnahmen in deren jeweiligen Result-Dateien. Sämtliche Kontrollmedien bleiben lokal und werden nicht hochgeladen.

## Datensicherheit und Git-Vorprüfung

- Alle 2832 geprüften Art-/Content-/Config-Dateien und 25 geschützten unversionierten Incoming-Originale stimmen SHA-256-genau mit dem Ausgangszustand überein.
- Alle 22 vorhandenen Produktions-Move-Assets stimmen im lesenden Endinventar feldweise mit dem Ausgangsbestand überein. Keine Originalattacken oder Lernlisten pauschal überschrieben.
- Originaler Entwickler-Spielstand: SHA-256 `eeab48f3c5652ef6d24b7f386ee7c26973336c929edf39aa7f6593d407a913df`; nach allen Save-Tests identisch.
- Beide Vollbackup-Refs zeigen unverändert auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`; dieser Commit ist kein Vorfahr des schlanken main. Vor der Sicherung waren sämtliche ursprünglichen Refs unverändert.
- 217 Quell-Dateien stimmen mit dem final geprüften Quellstand überein. Einziger Worktree bleibt `/Users/harry/Developer/PokeMonster`; keine neuen Maps, Projektkopien oder Vollbackups.
- `git lfs fsck --objects HEAD` erfolgreich; neue LFS-Objekte/Uploaddaten: 0. Ausschließlich Code, notwendige Werkzeuge und Dokumentation zur Sicherung vorgesehen. Keine Kontingent- oder Budgetänderung.
- Ausgangscommit und vorab direkt bestätigtes origin/main: `f29f6bf0814777daeadb79c42cf994c79a93aa52`. Branch main folgt origin/main.

## Git-Sicherung

Implementierungs- und Prüfcommit: [`22764fd8c8e40718d97a976be0569a738adcebe2`](https://github.com/Harrys-F/PokeMonster/commit/22764fd8c8e40718d97a976be0569a738adcebe2). Regulärer Push nach origin/main erfolgreich; direktes `git ls-remote` bestätigt exakt denselben Hash, lokales main und origin/main waren danach synchron. 37 gezielt kontrollierte Dateien, keine unerwarteten Indexpfade. Der anschließende, isoliert geprüfte Kompatibilitätsnachtrag erhält zusätzlich die historische Garantiewirkung alter Effekte und beendet nach Verwirrung plus Verbrennungs-KO die Runde vor einer weiteren gegnerischen Aktion.

Der erste Push enthält 53 neue normale Git-Objekte mit zusammen 1.614.410 unkomprimierten Bytes, deutlich unter der eigenen 1-GiB-Grenze. Aktuelle [GitHub-Einzeldateigrenze 100 MiB](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) und [Push-Grenze 2 GiB](https://github.com/github/docs/blob/main/content/get-started/using-git/troubleshooting-the-2-gb-push-limit.md) wurden unmittelbar vor dem Push überprüft; alle Dateien halten sie ein. [LFS-Abrechnung](https://docs.github.com/en/billing/concepts/product-billing/git-lfs) separat geprüft: dieses Paket enthält 0 neue/geänderte LFS-Dateien, daher 0 zusätzliche LFS-Uploadbytes. Remote-LFS-Prüfer bestätigt 0 Objekte und führt dafür bewusst keinen leeren Batch oder Objekt-Download aus. Kein vollständiger erneuter Remote-LFS-Download behauptet. Lokaler bestehender LFS-Bestand wurde mit fsck erfolgreich geprüft.

Keine Behauptung, dass damit der vollständige V4-Funktionsumfang abgeschlossen wäre. Der endgültige Dokumentationscommit wird nach dem Push erneut direkt geprüft und in der Abschlussmeldung genannt.

## Fortsetzung

Nach verbindlicher Regelentscheidung: fehlende Lebenszyklen in derselben BattleSession vervollständigen, Originalattacken gruppenweise korrekt binden und die Produktionsdaten-/Gameplaytests erneut ausführen. Bis dahin bleiben die 49 nicht fertigen Lernattacken sichtbar gesperrt statt nur zum Schein vollständig.
