# Alten Worktree endgültig entfernen – Abschlussbericht

Stand: 19.10.2026, 20:49 CEST.

**Abgeschlossen:** Alle **6.655 A-Dateien / 1.656.154.158 Bytes** an den freigegebenen Zielpfaden erhalten und vollständig SHA-256-verifiziert. Genau **7.622 B-Dateien / 12.504.665.170 Bytes** mit dem alten Worktree entfernt. **C: 0 Dateien; keine neuen ungeklärten Dateien.** Der reguläre Git-Befehl ohne `--force` war erfolgreich. Es ist nur noch das aktive Projekt unter `/Users/harry/Developer/PokeMonster` als Worktree registriert.

Build, sämtliche **49 Automationstests**, fünf geladene wichtige Maps mit jeweils **0 Map-Check-Fehlern/-Warnungen** sowie das erneute Öffnen aller **95 versionierten Blenderquellen** bestanden. Die abschließenden Prüfungen bestätigen sämtliche A-Dateien, aktuelle Quellen, Originalspielstand, Nutzerdateien, Git-Refs und LFS-Nutzdaten unverändert beziehungsweise vollständig erhalten.

Der beobachtete Gesamtgewinn vor den Tests betrug **7,023 GiB**. Nach Build/Editor/Blender-Prüfungen und laufender Systemaktivität verbleiben zum dokumentierten Messzeitpunkt **6,021 GiB** zusätzlicher freier Speicher gegenüber dem Beginn der Dateiüberführung. Die unterschiedlichen Messzeitpunkte werden unten ausdrücklich getrennt.

## 1. Freigabe und erneute Vorprüfung

Grundlage war die ausdrückliche Nutzerfreigabe: A vollständig erhalten, B vollständig entfernen, C laut Analyse leer; neue C-/ungeklärte Dateien nicht entfernen. Geschützt bleiben das aktive Projekt, GitHub-Historie, Vollbackup, LFS-Daten, die 38 ursprünglichen unversionierten Dateien und alle aktuellen Unreal-/Blenderquellen. Keine neuen Projektkopien, kein Originalasset-Reimport.

Gelesen und erneut geprüft:

- `AGENTS.md`, relevante aktive Pfad-/Schutzregeln in `TECHNIK.md` und `ENTSCHEIDUNGEN.md`.
- `Docs/ALTER_WORKTREE_ABSCHLUSSPRUEFUNG.md`.
- `Docs/ALTER_WORKTREE_ABC_DATEILISTE.csv`.
- `Docs/ALTER_WORKTREE_REIMPORT_PRUEFUNG.json`.

**Verwendeter unveränderter CSV-SHA-256:** `0e2434896211c0c8174af12bbaf983f542f52ff51ece0571b55f1f0a6b6d8785`.

Die tatsächlichen 14.277 regulären Dateien im alten Worktree stimmten exakt mit dem CSV überein: Kategorien, absolute normalisierte Pfade, Größen und SHA-256. Keine zusätzliche/fehlende Datei, kein Symlink, kein neuer Hardlink, kein Zielkonflikt. Alle A-Ziele waren frei. Alle Ziele liegen an den im CSV genannten Stellen unter dem aktiven `Saved/`; keine bestehenden Dateien wurden überschrieben.

Die Git-Worktree-Verwaltung war konsistent, der alte Status sauber, keine nicht geprüften privaten Worktree-Refs oder Submodule. Kein Prozess hatte Dateien im alten Worktree geöffnet. Main und direkter GitHub-Remote standen auf `427d93f`; der lokale Git-/LFS-Speicher und das Vollbackup waren vollständig geprüft. Kein Schutzcheck schlug fehl.

## 2. Kategorie A – vollständig erhalten

| Prüfung | Ergebnis |
|---|---|
| Überführte Einzeldateien | **6.655** |
| Gesamtgröße | **1.656.154.158 Bytes = 1,542 GiB** |
| Dateiinhalte | Vor dem Verschieben SHA-256 gegen CSV; nach jeder Verschiebung geprüft; anschließend alle Ziele nochmals unabhängig gelesen |
| Erneute Prüfung nach Worktree-Entfernung und sämtlichen Tests | **6.655/6.655 identisch**, keine ungültige oder fehlende Datei |
| Save-Testnachweise | **8/8 erhalten**, keine Änderung des aktuellen Dev-Spielstands |
| Ausgewählte Vergleichsbilder | **81/81 PNG erhalten** |
| Überschriebene Dateien | **0** |
| Überführungsmethode | Gleicher Datenträger, atomar mit `renamex_np(..., RENAME_EXCL)`; Überschreiben technisch ausgeschlossen |
| Dateiinodes | Für alle A-Dateien erhalten; keine zusätzlichen Nutzdatenkopien oder Backups |

Verteilung:

| Dateityp | Anzahl |
|---|---:|
| CSV | 2.952 |
| TXT | 121 |
| Log | 3.223 |
| JSON | 256 |
| SAV | 8 |
| JSONL | 9 |
| TSV | 5 |
| PNG | 81 |

Ziele entsprechen jeweils dem bestehenden relativen Saved-Pfad im aktiven Projekt, beispielsweise:

- `/Users/harry/Developer/PokeMonster/Saved/EnvironmentPerfV1/` und `Saved/EnvironmentPerfV2/`.
- `/Users/harry/Developer/PokeMonster/Saved/Profiling/CSV/` und den zugehörigen GPU-Ausgaben.
- Die im CSV genannten `Saved/VisualV2...`-Prüf-/Acceptance-/Photos-Unterstrukturen.

Nur dafür notwendige Unterverzeichnisse angelegt; keine Projektkopie, keine neue Unreal-Map und kein neuer Entwicklungsversionsordner. Die Dateien bleiben lokal unter ignoriertem `Saved`; keine Kontrollmedien oder Rohmessungen auf GitHub hochgeladen.

**Vollständiges Verschiebejournal mit jedem alten/neuen absoluten Pfad, Größe und SHA-256:** [MovedA.jsonl](/Users/harry/Developer/PokeMonster/Saved/WorktreeRemoval/MovedA.jsonl). Die freigegebene CSV bleibt unverändert als Zuordnungsgrundlage erhalten.

## 3. Kategorie B und Git-Worktree

Nach vollständiger A-Verifizierung verblieben im alten Worktree exakt die 7.622 B-Dateien. Jeder B-Pfad, jede Größe, jeder Hash und die unveränderte Dateiidentität wurden unmittelbar vor der Entfernung erneut geprüft. Es gab keine weitere Datei und keine Kategorie C.

Ausgeführt, **ohne `--force`**:

```sh
git -C /Users/harry/Developer/PokeMonster worktree remove /Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree
```

- Exit **0**, keine Fehlerausgabe, kein Wiederholungsversuch mit Force.
- Genau der geprüfte B-Restbestand mit **12.504.665.170 Bytes** entfernt; alle 6.655 A-Dateien vorher unabhängig verfügbar.
- Der alte Ordner existiert nicht mehr. Die zugehörige Verwaltung unter aktivem `.git/worktrees/Worktree` wurde von Git ordnungsgemäß entfernt.
- Der alte Branch **`codex/slim-backup-v5` bleibt erhalten**. Kein Branch oder Commit gelöscht oder umgeschrieben.
- Die gemeinsame aktive `.git`, ihre Objekte und ihr LFS-Speicher bleiben bestehen. Keine manuelle Entfernung in der Git-Verwaltung.
- `FullBackup` und `FullRestore` im übergeordneten alten Sicherungsordner bleiben erhalten. Keine weiteren Codex-Ordner bereinigt.

Die bekannte B-Einordnung der zwei alten Efeu-Blender-Zwischenstände wurde nicht erweitert. Aktuelle Garden-/PottedPlants-Quellen und Korrekturskripte bleiben identisch erhalten. Keine `.blend1`-Datei im aktiven Projekt entfernt.

Vor der Entfernung verifizierte konkrete B-Dateiliste: [RemovedBVerified.json](/Users/harry/Developer/PokeMonster/Saved/WorktreeRemoval/RemovedBVerified.json). Git-Ergebnis und anschließender A-/Originalschutz: [RemovalResult.json](/Users/harry/Developer/PokeMonster/Saved/WorktreeRemoval/RemovalResult.json).

Aktuell registriert:

```text
worktree /Users/harry/Developer/PokeMonster
HEAD 427d93f92765b2e03d8dca186fbc6bfbd86c8605
branch refs/heads/main
```

## 4. GitHub, Vollbackup, LFS und Originaldateien

| Prüfung nach Abschluss der Tests | Ergebnis |
|---|---|
| Aktiver Branch / Upstream | `main → origin/main` |
| Lokaler HEAD und direkt bestätigtes GitHub-origin/main | `427d93f92765b2e03d8dca186fbc6bfbd86c8605` |
| Remote | `git@github.com:Harrys-F/PokeMonster.git` |
| Vollbackup-Branch | `backup/full-03492bd → 03492bd96b4dba44692f675c19d5f11abfa86b4b` |
| Vollbackup-Archivref | `refs/archive/pokemonster/full-backup-03492bd → 03492bd96b4dba44692f675c19d5f11abfa86b4b` |
| Alle Git-Refs | Exakt identisch zur Vorprüfung |
| Lokale LFS-Nutzdateien | **11.205 / 19.010.564.957 Bytes**, vollständiger SHA-256-Vergleich, kein ungültiges Objekt |
| LFS-Bestand vor/nach | Identische Objektmenge und Größen, keine Entfernung oder Neuerzeugung von LFS-Nutzdaten |
| Vollbackup-LFS darin | **9.451 Objekte / 16.442.940.729 Bytes**, vollständig erhalten |
| GitHub-LFS | Vorher und nachher alle **1.383 Objekte / 6.607.098.907 Bytes** serverseitig download-verfügbar bestätigt |
| Aktive geschützte Dateien | **3.784 Dateien** inklusive aller 3.514 versionierten Dateien, bestehender unversionierter Dateien, ignorierter Art-Originale und des Spielstands frisch SHA-256-identisch |
| Ursprüngliche unversionierte Nutzerdateien | **38/38 separat frisch SHA-256-identisch** |
| Dev-Spielstand | Unverändert: `a0ad009a7b3c6f883d1413b0f96df5b25bc7ab953d0154e29ae50f35ad48bf0a` |
| Git-Objektprüfung | `git fsck --full --no-reflogs`: Exit 0; bestehende dangling Objekte nicht bereinigt |
| Diff/Index | Keine versionierten oder vorgemerkten Änderungen; `git diff --check` bestanden |

Kein Fetch/Pull nötig, kein Commit oder Push, keine Historyänderung, kein Force-Push, kein Reset/Restore/Clean, kein Git-/LFS-Prune. Die Remoteprüfungen verwendeten nur lesende Ref- und LFS-Download-Batch-Metadaten, keine Binärdownloads, Uploads, Käufe oder Budgetänderungen. Der Vollbackup-Commit wurde nicht auf GitHub übertragen.

Vor diesem Auftrag bestanden 49 unversionierte Einzelpfade. Sie sind unverändert erhalten. Dieser neue Bericht ist die einzige zusätzliche unversionierte Projektdatei, danach **50**. Alle Prüfprotokolle und überführten A-Dateien liegen unter ignoriertem `Saved`.

## 5. Tatsächlich durchgeführte Projektprüfungen

| Prüfung | Ergebnis |
|---|---|
| Mac Development Editor Build | **Bestanden**, Exit 0, 4.12 s; Target up to date, kein Clean Build |
| Vollständige Projekt-Automation | **49/49 Success**, 0 Testfehler, 0 Testwarnungen, 0 nicht ausgeführt, Exit 0; 31.03 s |
| Grafischer Unreal-Projektstart | Aktive `.uproject` gestartet; eigene Sitzung regulär geschlossen, Exit 0; keine fremde Sitzung beendet |
| Wichtige Maps | Alle fünf geladen; Map Check aus tatsächlichen Logmarkern geprüft, siehe Tabelle |
| Blenderquellen | **95/95** versionierte Quellen schreibfrei erneut geöffnet, keine fehlenden geprüften Abhängigkeiten, keine alte Worktree-Abhängigkeit, keine Quelldatei gespeichert; 85.60 s |
| A-Daten nach sämtlichen Tests | **6.655/6.655** erneut per SHA-256 und Dateiidentität bestätigt |
| Aktive Quellen/Maps/Nutzerdateien | Alle geschützten Dateien unverändert |

| Map | Actors | Map-Check-Fehler | Warnungen | Dirty-Pakete |
| `/Game/Maps/Dev_TestMap.Dev_TestMap` | 631 | 0 | 0 | keine |
| `/Game/Maps/Dev_WestlandRegion.Dev_WestlandRegion` | 3094 | 0 | 0 | keine |
| `/Game/Maps/Dev_WestlandAssetLibrary.Dev_WestlandAssetLibrary` | 85 | 0 | 0 | keine |
| `/Game/Maps/Dev_TestMap_NPCMotionV3.Dev_TestMap_NPCMotionV3` | 1356 | 0 | 0 | keine |
| `/Game/Maps/Dev_TestMap_VisualV2.Dev_TestMap_VisualV2` | 1401 | 0 | 0 | keine |

Keine Originalassets reimportiert. Insbesondere die sieben Texture-UAssets mit alten Interchange-Kennungen blieben SHA-256-identisch und wurden nicht gespeichert. Materialien, Animationen, Gameplay, Kamera und Collision unverändert. Die frühere Reimport-Diagnose wird nicht als neue Darstellungsfreigabe ausgegeben.

Kein zusätzlicher PIE-Fußlauf, Shipping-Cook oder Performance-Benchmark in diesem Auftrag behauptet. Verlangter Projektstart, wichtige Maps, Build und die vollständigen vorhandenen Automationstests wurden tatsächlich ausgeführt. Bestehende historische Einmal-Replay-Skripte mit Altpfaden sowie alte absolute Bericht-/Screenshotlinks bleiben wie dokumentiert unverändert; die erhaltenen A-Nachweise sind über CSV und Verschiebejournal am neuen Ort auffindbar.

### Engine-Logs und normale Cachewartung

Beide frischen Unreal-Logs enthalten die bereits vorbestehenden 17 Startup-Zeilen `LogAutomationTest: Error: Condition failed`. Ihr normalisierter Zähler stimmt mit den vorherigen V3-Logs überein; keine neuen normalisierten Fehlerzeilen. Diese Meldungen entstanden beim Engine-Start und sind getrennt von den 49 erfolgreichen Projekt-Automationstests dokumentiert. Weitere bestehende Engine-/Hilfsprogrammwarnungen werden im Lognachweis vollständig erhalten; keine allgemeine Logfehlerfreiheit behauptet.

Die erste Logauswertung suchte zunächst einen nicht vorhandenen älteren Protokollpfad. Nach Auswahl der tatsächlich vorhandenen Vorher-Logs konnte der Vergleich vollständig durchgeführt werden. Kein Schutzcheck und kein Projekttest schlug dadurch fehl.

Build/Unreal dürfen bei den angeforderten Tests ihre eigenen generierten Caches, Logs und Einstellungen unter Intermediate/Saved erneuern. Die Engine protokolliert u. a. ihre automatische AssetRegistry-Cachewartung. **Die gezielte Bereinigung selbst entfernte ausschließlich den verifizierten B-Worktree und seine von Git verwalteten Metadaten; keine weitere manuelle Dateibereinigung.** Alle benötigten Quellen, Assets, A-Daten, bestehenden Nutzerdateien und LFS-Nutzdaten sind durch den abschließenden Inhaltsvergleich geschützt.

## 6. Tatsächlich gemessener Speicher

Gemessen mit `statvfs` auf dem aktiven Datenvolume, zusätzlich `df -k`. Bytes sind freie Volume-Bytes, 1 GiB = 1.073.741.824 Bytes. Kein Schätzen anhand logischer Dateigrößen.

| Messpunkt | Zeit | Freie Bytes | Freie GiB |
| Vor A-Überführung | 2026-10-19T20:40:25.100954+02:00 | 142.178.512.896 | 132,414 |
| Unmittelbar vor git worktree remove | 2026-10-19T20:41:15.955720+02:00 | 142.071.287.808 | 132,314 |
| Unmittelbar danach | 2026-10-19T20:41:17.868428+02:00 | 149.732.278.272 | 139,449 |
| Nach Beruhigung, vor den Tests | 2026-10-19T20:41:53.583795+02:00 | 149.719.687.168 | 139,437 |
| Nach Build/Automation/Editor/Blender und finalen Hashprüfungen | 2026-10-19T20:47:17.955054+02:00 | 148.643.504.128 | 138,435 |

- Direkt um den Git-Entfernungsschritt: **+7.660.990.464 Bytes = 7,135 GiB**.
- Gesamte Dateiüberführung und Entfernung bis zum stabilisierten Messpunkt vor Tests: **+7.541.174.272 Bytes = 7,023 GiB**.
- Netto nach allen angeforderten Prüfungen gegenüber dem Beginn der A-Überführung: **+6.464.991.232 Bytes = 6,021 GiB**.

Die vorherige APFS-Schätzung von rund 7,11 GiB wird durch den unmittelbaren Entfernungsschritt plausibel bestätigt. Die Differenzen zwischen Messzeitpunkten enthalten Verzeichnis-/Prüfmetadaten, Test-/Cacheausgaben sowie weitere laufende macOS-Aktivität. Nicht der gesamte spätere Verbrauch lässt sich zuverlässig nur Unreal oder Blender zuordnen. Er wurde weder weggeputzt noch aus der Messung herausgerechnet. Die erhaltenen A-Daten bleiben vollständig auf dem Volume; keine zusätzlichen Payloadkopien angelegt. Speicher in `FullBackup`, `FullRestore`, der gemeinsamen Git-/LFS-Datenbank oder anderen Codex-Ordnern ist nicht als Bereinigungsgewinn gerechnet.

## 7. Nachweise und endgültiger Stopp

Alle neuen Rohprotokolle liegen ausschließlich lokal unter [Saved/WorktreeRemoval](/Users/harry/Developer/PokeMonster/Saved/WorktreeRemoval):

- [Vorprüfung und Freigabelistenhash](/Users/harry/Developer/PokeMonster/Saved/WorktreeRemoval/Preflight.json)
- [6.655 atomare Verschiebungen mit Prüfsummen](/Users/harry/Developer/PokeMonster/Saved/WorktreeRemoval/MovedA.jsonl)
- [Vollständige A-Prüfung vor Entfernung](/Users/harry/Developer/PokeMonster/Saved/WorktreeRemoval/AVerified.json)
- [Unmittelbar vorher verifizierte 7.622 B-Pfade](/Users/harry/Developer/PokeMonster/Saved/WorktreeRemoval/RemovedBVerified.json)
- [Reguläre Git-Entfernung und Schutzprüfung](/Users/harry/Developer/PokeMonster/Saved/WorktreeRemoval/RemovalResult.json)
- [Build](/Users/harry/Developer/PokeMonster/Saved/WorktreeRemoval/Build/Result.json)
- [Vollständige Automation](/Users/harry/Developer/PokeMonster/Saved/WorktreeRemoval/Automation/Result.json)
- [Grafischer Editorstart](/Users/harry/Developer/PokeMonster/Saved/WorktreeRemoval/Editor/Result.json)
- [Map Checks](/Users/harry/Developer/PokeMonster/Saved/WorktreeRemoval/MapChecks.json)
- [Blenderquellen](/Users/harry/Developer/PokeMonster/Saved/WorktreeRemoval/BlenderSources.json)
- [Engine-Logvergleich einschließlich Cachewartung](/Users/harry/Developer/PokeMonster/Saved/WorktreeRemoval/EngineLogReview.json)
- [Abschließende A-/Original-/Git-/LFS-Integrität](/Users/harry/Developer/PokeMonster/Saved/WorktreeRemoval/FinalIntegrity.json)
- [GitHub-LFS-Verfügbarkeit nach Entfernung](/Users/harry/Developer/PokeMonster/Saved/WorktreeRemoval/RemoteLFSAfter.json)
- [Freier Speicher vor Tests](/Users/harry/Developer/PokeMonster/Saved/WorktreeRemoval/SpaceAfterCleanup.json)
- [Freier Speicher nach Tests](/Users/harry/Developer/PokeMonster/Saved/WorktreeRemoval/SpaceAfterValidation.json)

**Keine offene Bereinigung oder automatische Folgeaktion.** Der freigegebene alte Worktree ist entfernt, der aktive Projektordner und alle Schutzbestände bleiben erhalten. Keine weiteren Ordner entfernt, keine neuen Projektkopien, keine Originalasset-Reimports, kein Commit und kein Push.
