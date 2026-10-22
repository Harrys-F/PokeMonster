# PokeMonster – Speicherbereinigung V3: Abschlussbericht

19.10.2026. **Die ausdrücklich freigegebene V2-CSV wurde vollständig abgearbeitet: 21.758 gezielte Einzeldateilöschungen, 0 übersprungene Einträge, 0 Ordnerlöschungen. Keine weitere Bereinigungsaktion.**

Unmittelbar nach der Bereinigung und vor Build/Unreal wurden **31.459.741.696 Bytes = 29,299 GiB** zusätzlicher freier Volume-Speicher gemessen. Spätere Build-/Editor-/Systemaktivität ist getrennt ausgewiesen. Der aktive Projektstand bleibt `427d93f92765b2e03d8dca186fbc6bfbd86c8605`; Quellen und Maps unverändert, Vollbackup und alle Worktrees/Branches erhalten.

## 1. Ausschließlich freigegebener Umfang

- Einzige positive Löschquelle: [SPEICHERBEREINIGUNG_V2_LOESCHLISTE.csv](/Users/harry/Developer/PokeMonster/Docs/SPEICHERBEREINIGUNG_V2_LOESCHLISTE.csv).
- Verbindlicher SHA-256 vor Preflight und unmittelbar vor Ausführung: `08af12d606100603fff64ba13b8f55c100c0fbdfc21349717f3b4db69420df79`; unverändert.
- 21.758 eindeutige absolute Dateipfade; keine Wildcards, keine Verzeichnislöschung, kein rekursiver Löschbefehl. Die TXT-Liste wurde nicht als alternative Löschquelle verwendet.
- Die 7.088 in V2 zurückgestellten A-Dateien und sämtliche ursprünglichen B-/C-Dateien bleiben erhalten. Kein nachträgliches Ausweiten der Freigabe.
- Aktiver Root, Git-/LFS-/IDE-Verwaltung, FullBackup/FullRestore, Originalmodelle, `.blend1`, lokale Blender-Unikate, sieben offene Interchange-Importquellen und unversionierte Projektdateien waren ausdrücklich geschützt.

| Kategorie | Gelöschte Dateien |
|---|---:|
| Reproduzierbare alte Build-/Cook-/Shader-/Modulcache-Ausgaben | 717 |
| Nachweislich in erhaltenen ZIPs enthaltene Reviewbild-Kopien | 19,628 |
| Reviewbild-Kopien mit separat erhaltenem identischem Gegenstück | 1,393 |
| Finder-Metadaten | 20 |

## 2. Unmittelbare erneute Sicherheitsprüfung

Alle Kandidaten wurden vor der ersten Löschung erneut geprüft: absoluter erlaubter Pfad, keine Symlinks, reguläre Datei, SHA-256, Dateigröße, Änderungszeit, Geräte-/Inodekennung, Hardlinkzahl und Schutzflags. Der gesamte registrierte alte Checkout wurde anhand aktueller Git-Dateilisten ausgeschlossen. Git-Refs, Worktree-Zuordnung und Arbeitsbaumzustand wurden vor Ausführung erneut mit dem Preflight verglichen.

Beide erhaltenen ZIPs und die separat erhaltenen Gegenstücke wurden frisch gehasht. Zusätzlich wurden **8.459 unterschiedliche konkret benötigte ZIP-Einträge erneut vollständig gelesen und per SHA-256/CRC geprüft**, ohne Archivmaterialisierung oder zusätzliche Binärkopie. Die 21.758 Pfade waren alle freigabefähig; kein Abweichungsfall.

Jede Datei wurde **direkt vor dem Unlink nochmals vollständig gehasht**. Das Skript ging ausgehend vom geöffneten Documents/Codex-Verzeichnis mit `O_NOFOLLOW` durch die Elternverzeichnisse, prüfte die Dateikennung erneut und entfernte ausschließlich den CSV-Basisnamen über den gebundenen Verzeichnisdeskriptor. Unerwartete Änderungen hätten zu einem protokollierten Überspringen geführt. Alle Hardlinkalias-Namen wurden berücksichtigt; kein geschützter Alias betroffen.

Direkt nach der Löschung, noch vor Build und Editor: alle 143.694 im Preflight erfassten Bestandsdateien geprüft. Ausschließlich die 21.758 protokollierten CSV-Dateien fehlten; keine zusätzliche Bestandsdatei fehlte oder war geändert. Beide Git-Arbeitsbäume unverändert. Die 1.395 erhaltenen Gegenstücke/Archive wurden nach allen Tests nochmals per SHA-256 geprüft; kein Fehler.

## 3. Gemessene Speicherwirkung

Messung auf demselben Dateisystem über `statvfs`, freie/benutzbare Blöcke × Fragmentgröße. Die erste Nachmessung erfolgte vor den anschließenden Build-/Editorarbeiten. Kein bloßes Addieren logischer Dateilängen. Hardlinks werden nur einmal gezählt; APFS-Teilung/Snapshots reduzieren den sofort freien Anteil.

| Messpunkt | Uhrzeit | Freie Bytes | Freie GiB |
|---|---|---:|---:|
| Unmittelbar vor Einzeldateilöschungen | 19:44:46 CEST | 114,022,973,440 | 106,192 |
| Unmittelbar danach | 19:45:15 CEST | 145,496,502,272 | 135,504 |
| Nach Dateisystem-Sync und 2 s Beruhigung, noch vor Tests | 19:45:17 CEST | 145,482,715,136 | 135,491 |
| Nach Build/Editor und abschließender Prüfung | 2026-10-19T19:55:21.589416+02:00 | 142,131,200,000 | 132,370 |

| Größe | Bytes | GiB |
|---|---:|---:|
| Gelöschte logische Dateilängen | 36,894,790,837 | 34,361 |
| V2-Dateiblöcke nach Hardlink-Abzug | 35,334,119,424 | 32,907 |
| Vor Ausführung erneut ermittelte exklusive APFS-Bytes | 31,470,190,592 | 29,309 |
| Gemessener freier Zuwachs direkt durch den Bereinigungszeitraum | 31,459,741,696 | 29,299 |
| Netto-Zuwachs des gesamten Volumes bei Abschluss einschließlich späterer Aktivitäten | 28,108,226,560 | 26,178 |

Die konservative APFS-Prognose von 29,309 GiB und die direkte Messung von 29,299 GiB liegen nahe beieinander. Die geringe Differenz enthält unter anderem Dateisystem-/Prüfprotokoll- und Hintergrundaktivität. Nachfolgende Tests und andere Systemprozesse können wieder Speicher belegen; deren gesamte Wirkung lässt sich aus einer Volume-Messung nicht vollständig einzelnen Verursachern zuordnen. Deshalb wird der spätere Netto-Wert nicht als zweites isoliertes Bereinigungsergebnis verkauft. Keine fremden/globalen Caches wurden zusätzlich bereinigt.

## 4. Git, LFS und geschützte Daten

| Prüfung | Ergebnis |
|---|---|
| HEAD / Branch | `427d93f92765b2e03d8dca186fbc6bfbd86c8605`, `main → origin/main`; direkter GitHub-Abgleich identisch |
| Refs und Worktrees | Alle unverändert; alter schlanker Worktree weiterhin registriert und sauber; keine Branch-/Worktree-Entfernung |
| Vollbackup | `03492bd96b4dba44692f675c19d5f11abfa86b4b` unverändert auf Backup-Branch und Archiv-Ref; FullBackup und FullRestore erhalten |
| LFS-Objektbestand | Alle 11,205 lokalen Objekte / 19,010,564,957 Bytes per SHA-256 korrekt; alle 9.696 im geprüften Pointerbestand erwarteten Objekte vorhanden |
| LFS-Methode | Nur lesende eigene SHA-Prüfung; kein Prune, Fetch, Upload oder potentiell mutierendes LFS-Reparaturkommando |
| Versionierte Dateien | 3.514/3.514 tatsächliche Arbeitsdateien byteidentisch zu Git/LFS, vor und nach Editorstart geprüft |
| Maps | Alle 16 versionierten `.umap` bytegleich; die zusätzliche unversionierte Map ebenfalls über die 38er-Prüfung geschützt |
| Unversionierte Nutzerdaten | 38/38 erhaltene Projektdateien SHA-256-identisch zum Umstellungsjournal; frühere V1-/V2-Analyseberichte und Listen ebenfalls erhalten |
| Weitere Originale | Lokale MiniHobbit-GLB, Blenderquellen/-Sicherungen, Ranger-/Hobbit-Stände unverändert; keine Blenderbearbeitung |
| Spielstand | Vorhandener `PokeMonster_Dev.sav` unverändert; keine Spielstandverschiebung oder zusätzliche Sicherung dieses Auftrags |
| Git-Diff | `git diff --check` ohne Befund; keine versionierten Änderungen, nichts gestaged, kein Commit/Push |

Alle verbleibenden Dateien unter Documents/Codex stimmen auch nach den Tests in Größe/Änderungszeit/Inode/Hardlinkzahl mit dem Preflight überein. Kein Kandidat wurde nachträglich erneut entfernt oder von einem Werkzeug als fehlende Originalquelle benötigt.

## 5. Build, Automation und Unreal-Projektstart

### Mac Development Editor Build

Erfolgreicher regulärer `PokeMonsterEditor Mac Development`-Aufruf mit `-WaitMutex -NoHotReloadFromIDE`: Exit 0 / `Result: Succeeded`, rund 4.34 s. UnrealBuildTool meldet den Target als aktuell und führt 0 Compileraktionen aus; dies ist kein behaupteter Clean-/From-Scratch-Rebuild. Keine Clean-Option oder zusätzliche Compiler-/SDK-Bereinigung.

### Vollständige Projekt-Automation

Ein vollständiger Lauf von `Automation RunTests PokeMonster`, nicht wiederholt, um Warnungen loszuwerden: **49 erfolgreiche Tests**, davon **48 ohne und 1 mit Warnungen**; 0 fehlgeschlagen, 0 nicht ausgeführt, 0 noch laufend. Prozess Exit 0; rund 41.63 s. Alle 49 Einzeltests besitzen Status Success. Keine Testwarnung unterdrückt.

Betroffen ist `PokeMonster.Rendering.EnvironmentProfileV3.IndependentExperiment` mit genau zwei erhaltenen Plattformwarnungen:

- `LogHAL: FMacPlatformProcess::CreateProc: posix_spawn("/Users/Shared/Epic Games/UE_5.8/Engine/Extras/ThirdPartyNotUE/libimobiledevice/Mac/idevice_id") failed (86, Bad CPU type in executable)`
- `LogHAL: Failed to launch Tool. (/Users/Shared/Epic Games/UE_5.8/Engine/Extras/ThirdPartyNotUE/libimobiledevice/Mac/idevice_id)`

Beide Meldungen kommen wortgleich bereits im vor der Bereinigung vorhandenen ProjectMigration-Editorlog vor. Das Engine-Hilfsprogramm liegt außerhalb jedes freigegebenen Pfads. Keine neue Projekt-Testfehlerursache nachgewiesen und keine Reparatur/Unterdrückung durchgeführt. Der originale Dev-Spielstand blieb identisch; Automation verwendet eigene temporäre Testslots. Deren übliche Erstellung/Entfernung betrifft keine vorbestehenden Nutzerdateien.

### Grafischer Projektstart und bestehende Karten

Der echte Unreal-Editor wurde am aktiven `.uproject` mit normalem Metal-Renderer gestartet, ohne NullRHI für diesen Starttest. Die fünf bestehenden Karten wurden geladen, Akteure erfasst und jeweils explizit Map Check ausgeführt. Danach VisualV2 als letzte Karte geladen; keine schmutzigen Map-/Contentpakete und kein Speichern. Die eigene Testsitzung schloss regulär mit Exit 0 nach rund 60.11 s. Keine vorhandene Sitzung verworfen, kein Force Quit.

| Map | Akteure | Map-Check-Fehler | Warnungen | Dirty-Pakete |
|---|---:|---:|---:|---|
| `/Game/Maps/Dev_TestMap.Dev_TestMap` | 631 | 0 | 0 | keine |
| `/Game/Maps/Dev_WestlandRegion.Dev_WestlandRegion` | 3,094 | 0 | 0 | keine |
| `/Game/Maps/Dev_WestlandAssetLibrary.Dev_WestlandAssetLibrary` | 85 | 0 | 0 | keine |
| `/Game/Maps/Dev_TestMap_NPCMotionV3.Dev_TestMap_NPCMotionV3` | 1,356 | 0 | 0 | keine |
| `/Game/Maps/Dev_TestMap_VisualV2.Dev_TestMap_VisualV2` | 1,401 | 0 | 0 | keine |

Kein zusätzlicher PIE-Fußlauf, keine neue künstlerische Abnahme, kein Shipping-Cook oder FPS-/GPU-Benchmark behauptet. Der verlangte Projektstart, das Laden der wichtigen Karten, Build und die vollständige Automation wurden tatsächlich durchgeführt. Keine neue Map, keine Gameplay-, Kamera-, Material- oder Animationsänderung.

### Vorbestehende Engine-Startmeldungen

Beide frischen Engine-Logs enthalten 17 `LogAutomationTest: Error: Condition failed`-Startzeilen. Der normalisierte Meldungszähler stimmt exakt mit dem vorhandenen Umstellungs-Editorlog überein. Sie entstehen bereits während der Engine-Initialisierung vor dem Projekt-Testlauf und sind getrennt von dessen 49 Success-Ergebnissen dokumentiert; keine allgemeine Engine-Logfehlerfreiheit behauptet. Keine neuen normalisierten Fehlerzeilen und keine Treffer der geprüften Fehlersignaturen für fehlende Packages/Objekte oder fehlgeschlagene Materialkompilierung.

## 6. Wichtige Test-Nebenwirkung: Unreal erneuert selbst seinen Cache

Der Bereinigungslauf selbst entfernte ausschließlich CSV-Dateien. **Erst die ausdrücklich angeforderten Unreal-Tests** haben anschließend innerhalb des aktiven Projekts automatisch den generierten AssetRegistry-Cache erneuert. Dies muss vom freigegebenen Bereinigungsvorgang getrennt werden:

- Bereits vor dem Auftrag vorhanden und von Unreal ersetzt: `/Users/harry/Developer/PokeMonster/Intermediate/CachedAssetRegistry/CachedAssetRegistry_0_233623AF1C48FDF651B11DB8A030281E.bin`.
- Die Automation schreibt eine neue Cachegeneration und protokolliert selbst `deleted (orphaned, unreferenced by any .ref)` für die alte Generation; der grafische Editor macht denselben Vorgang anschließend mit der während des Tests entstandenen Generation.
- Aktueller gültig referenzierter Cache: `/Users/harry/Developer/PokeMonster/Intermediate/CachedAssetRegistry/CachedAssetRegistry_0_B3FA5986834BE1B944A9E69FA33137D7.bin`; `.ref` zeigt auf eine vorhandene Datei.
- Insgesamt 60 bestehende generierte Dateien wurden bei Build/Editor regulär aktualisiert, überwiegend Intermediate-/Saved-/Plugin-Intermediate-Dateien. Das ist keine Änderung von versionierten Quellen oder Assets. Ein erster strenger Nachher-Dateicheck markierte die zusätzliche alte Cachedatei zunächst als unerwartet fehlend; die Engine-Protokolle belegen anschließend den Ersetzungsvorgang. Beide ursprünglicher Befund und Erklärung bleiben erhalten.

Diese Cacheerneuerung wurde nicht als weitere Speicherbereinigung angeordnet oder als zusätzlicher Gewinn ausgegeben. Keine manuelle Entfernung außerhalb der CSV, kein Wiederherstellen alter Cachegenerationen und keine weitere Bereinigungsaktion. Alle Arbeitsdateien aus Git/LFS, Nutzerdateien, Maps und verbliebenen Altdateien unverändert.

## 7. Protokolle und Abschlussstatus

Lokale Rohprotokolle: [StorageCleanupV3](/Users/harry/Developer/PokeMonster/Saved/StorageCleanupV3). Keine Videos, Kontrollbilder, Nutzdatenkopien oder zusätzliche Backups erzeugt; nur erforderliche Prüfmetadaten und normale Testausgaben.

- [Jede tatsächliche Einzeldateilöschung mit Pfad und SHA-256](/Users/harry/Developer/PokeMonster/Saved/StorageCleanupV3/Deleted.jsonl)
- [Löschanzahl, übersprungene Dateien und Speicherwerte](/Users/harry/Developer/PokeMonster/Saved/StorageCleanupV3/CleanupResult.json)
- [Vorprüfung und Gegenstück-Hashes](/Users/harry/Developer/PokeMonster/Saved/StorageCleanupV3/PreflightSummary.json)
- [Nachweis: vor den Tests ausschließlich freigegebene CSV-Dateien entfernt](/Users/harry/Developer/PokeMonster/Saved/StorageCleanupV3/IntegrityAfterDelete.json)
- [Lesende vollständige LFS-Prüfung](/Users/harry/Developer/PokeMonster/Saved/StorageCleanupV3/LFS.json)
- [Original-/Map-/Nutzerdatenvergleich nach Editorstart](/Users/harry/Developer/PokeMonster/Saved/StorageCleanupV3/SourceIntegrity.json)
- [Build-Ergebnis](/Users/harry/Developer/PokeMonster/Saved/StorageCleanupV3/Build/Result.json)
- [Alle Automationsergebnisse einschließlich Warnungen](/Users/harry/Developer/PokeMonster/Saved/StorageCleanupV3/Automation/Result.json)
- [Grafischer Projektstart und reguläres Ende](/Users/harry/Developer/PokeMonster/Saved/StorageCleanupV3/Editor/Result.json)
- [Geladene Karten und Dirty-Status](/Users/harry/Developer/PokeMonster/Saved/StorageCleanupV3/Editor/Maps.json)
- [Aus tatsächlichen Logmarkern gelesene Map-Check-Ergebnisse](/Users/harry/Developer/PokeMonster/Saved/StorageCleanupV3/MapChecks.json)
- [Abschließender Umfangs-/Gegenstück-/Git-Abgleich](/Users/harry/Developer/PokeMonster/Saved/StorageCleanupV3/FinalAudit.json)
- [Erklärte normale Cacheerneuerung durch Unreal](/Users/harry/Developer/PokeMonster/Saved/StorageCleanupV3/EngineCacheMaintenance.json)

Git nach den Tests unverändert: `main...origin/main`, kein geänderter versionierter Pfad; 43 bereits zuvor unversionierte Dateien bleiben erhalten. Dieser neue Bericht ist die einzige zusätzliche unversionierte Projektdatei (danach 44). Rohlogs unter Saved sind ignoriert. Kein Commit, Push, Reset, Restore, Clean, Branchlöschen, Worktree-Entfernen, LFS-Prune oder Force-Push. Keine Git-Historie geändert.

**Abgeschlossen. Keine weitere Bereinigung durchgeführt oder freigegeben.**
