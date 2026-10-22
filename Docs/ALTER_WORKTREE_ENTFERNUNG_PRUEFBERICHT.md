# Alter PokeMonster-Worktree – Entbehrlichkeit und Entfernung prüfen

Stand: 19.10.2026, 20:10 CEST. **Reine Prüfung; nichts gelöscht, verschoben, umbenannt oder am Worktree geändert.**

**Empfehlung: Den vollständigen Worktree noch nicht entfernen.** Der alte Checkout wird für die aktive Entwicklung nicht mehr benötigt. Eine verlustfreie Entfernung des gesamten Ordners ist noch nicht freigabefähig: zwei lokale Blender-Zwischenstände und historische Nachweise sind nicht vollständig anderweitig gesichert; außerdem bleibt ein gezielter Reimport-Nachweis für sieben Texturen offen.

Aktiv bleibt ausschließlich `/Users/harry/Developer/PokeMonster`. Keine zusätzliche Projektkopie, kein Versionsordner, keine neue Sicherung, keine Map, kein Commit und kein Push erstellt. Neu angelegt werden nur dieser Bericht und das zugehörige Dateiinventar.

## 1. Git, GitHub und unabhängige Projektbasis

| Prüfung | Befund |
|---|---|
| Aktiver Branch / HEAD | `main`, `427d93f92765b2e03d8dca186fbc6bfbd86c8605` |
| origin/main | Lokal und frisch direkt per `git ls-remote` auf GitHub identischer Hash |
| GitHub-Repository | `git@github.com:Harrys-F/PokeMonster.git`; `main` folgt `origin/main` |
| Alter Worktree | `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree` |
| Alter Branch / HEAD | `codex/slim-backup-v5`, `30a165b034114ba4b0940a369e73143db988afad`; Vorfahr des aktuellen `main` |
| Alter Git-Status | Keine versionierten Änderungen, keine nicht ignorierten unversionierten Dateien |
| Alter Checkout | Alle 3.508 versionierten Dateien frisch SHA-256-geprüft; exakt zum alten Commit und als identische Nutzdaten in der vorhandenen GitHub-Historie enthalten |
| Aktiver Checkout | Alle 3.514 versionierten Dateien frisch gegen Git-/LFS-Nutzdaten SHA-256-geprüft; ohne Abweichung |
| Erforderliche Dateien | `evidence.py validate-core`: 3.513/3.513 vorhanden und identisch |
| Erhaltene Nutzerdateien | Alle 38 ursprünglichen unversionierten Dateien im aktiven Projekt frisch gegen das Umstellungsjournal geprüft; unverändert |
| Unversionierter aktiver Bestand | Vor diesem Bericht 44 Einzelpfade; nach Bericht/Inventar zwei zusätzliche Pfade. Bestehende Dateien bleiben unangetastet |
| Git-Objekte | `git fsck --full --no-reflogs`: Exit 0. Bestehende dangling Objekte nicht bereinigt |
| Laufende Zugriffe | `lsof +D` meldet zum Prüfzeitpunkt keine offenen Dateien im alten Worktree; keine dauerhafte Garantie |

Das aktive `.git`, dessen Git-Objekte, LFS-Speicher und `.uproject` liegen physisch im aktiven Projektordner, ohne Symlink zum alten Worktree. Keine Git-Alternates, kein separates `core.worktree`, kein ausgelagerter LFS-Speicher und keine Submodule festgestellt. **Die Abhängigkeitsrichtung ist umgekehrt:** Der alte Worktree verwendet die Verwaltung im aktiven Projekt.

### Vollbackup und LFS

- `backup/full-03492bd` und `refs/archive/pokemonster/full-backup-03492bd` zeigen unverändert auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`.
- Dieser Vollbackup-Commit ist weiterhin **kein Vorfahr** des schlanken `main` und von `origin/main`.
- Alle **11.205 lokalen LFS-Nutzdateien / 19.010.564.957 Bytes** frisch SHA-256-geprüft; kein ungültiges Objekt. Sämtliche 9.696 erwarteten Objekte der geprüften Commit-/Historienmenge vorhanden.
- Davon benötigt das Vollbackup **9.451 Objekte / 16.442.940.729 Bytes**; vollständig im aktiven `.git/lfs/objects`, unabhängig vom alten Checkout.
- GitHub bestätigt frisch für **1.383 Objekte / 6.607.098.907 Bytes** der schlanken Historie Download-Verfügbarkeit. Nur Batch-Metadaten angefragt, keine Binärdaten heruntergeladen, kein Upload, keine Kosten-/Kontingentänderung. Dies ist kein neuer kontoweiter Abrechnungsnachweis.
- Vorhandenes `FullBackup/PokeMonster_full_03492bd.bundle` erneut mit `git bundle verify` geprüft: gültige vollständige Historie. `FullBackup` und `FullRestore` liegen als **Geschwister außerhalb von `Worktree`** und bleiben geschützt. Sie sind keine externe SSD-Sicherung.

Eine spätere ordnungsgemäße Entfernung nur des verknüpften Worktrees würde weder diese Schutzrefs noch den gemeinsamen Git-/LFS-Objektspeicher entfernen. Kein Branchlöschen, Prune oder Garbage Collection erforderlich.

## 2. Verbliebener Datenbestand und zusätzlicher Speichergewinn

Die folgende Messung betrifft ausschließlich den verbliebenen alten Worktree **nach** Speicherbereinigung V3, nicht den ganzen übergeordneten Sicherungsordner.

| Bestand | Dateien | Logische Bytes | Logisch GiB | Dateiblöcke GiB | APFS exklusiv GiB |
| Gesamt | 14.277 | 14.160.819.328 | 13,188 | 13,224 | 7,933 |
| Versionierter Checkout | 3.508 | 7.258.257.420 | 6,760 | 6,767 | 6,697 |
| Ignorierter Bestand, ausschließlich unter Saved | 10.768 | 6.902.561.841 | 6,429 | 6,457 | 1,236 |

**Zusätzliches derzeit gemessenes Freigabepotenzial bei späterer vollständiger Entfernung: rund 7,933 GiB = 8.518.242.304 Bytes, also etwa 8,52 dezimale GB.** Nicht 13,22 GiB als sofort frei werdenden Speicher versprechen.

Keine mehrfach verlinkten Dateien oder Symlinks im verbliebenen Worktree. Die Differenz zwischen Dateiblöcken und exklusiven Bytes erklärt sich durch APFS-Blockteilung beziehungsweise Snapshotbindung. Die macOS-Abfrage `ATTR_CMNEXT_PRIVATESIZE` wurde für alle 14.277 Dateien erfolgreich gelesen; sie zählt momentan nicht mit Klonen/Snapshots geteilte Extents. Verzeichnis-/Dateisystemmetadaten und laufende Systemaktivität können den späteren tatsächlichen Nettofreigewinn verändern. Shared-Blöcke, die erst durch andere spätere Aktionen frei würden, sind nicht als zusätzlicher Gewinn angesetzt.

**Bisher in diesem Auftrag freigegeben: 0 Bytes.** Die früher erzielten 29,299 GiB aus Speicherbereinigung V3 werden nicht nochmals angerechnet. `FullBackup`, `FullRestore`, der aktive Git-/LFS-Speicher und sämtliche anderen Codex-Ordner sind nicht in diesem Entfernungsumfang enthalten.

### Sicherungsstatus der einzelnen Dateigruppen

Disjunkte Zuordnung; eine identische Nutzdatei in Git-Historie ist nicht zwingend noch unter demselben heutigen Pfad ausgecheckt.

| Dateigruppe | Dateien | Logische GiB | Bewertung |
| Git-Verwaltungsverweis; ausschließlich über Git behandeln | 1 | 0,000 | Nachweise im Inventar; keine aktuelle Löschfreigabe |
| Lokaler Blender-Zwischenstand; Entscheidung erforderlich | 2 | 0,006 | Nicht pauschal entfernen |
| Kein identisches gesichertes Gegenstück im Prüfbestand belegt; erhalten | 8.273 | 5,915 | Nicht pauschal entfernen |
| Versionierter Checkout; Nutzdaten in origin/main-Historie | 3.508 | 6,760 | Nachweise im Inventar; keine aktuelle Löschfreigabe |
| Ignorierte Datei nur durch lokales Vollbackup nachgewiesen | 21 | 0,000 | Nachweise im Inventar; keine aktuelle Löschfreigabe |
| Ignorierte Datei mit identischem GitHub-Nutzdatenhash | 80 | 0,001 | Nachweise im Inventar; keine aktuelle Löschfreigabe |
| Identisches Gegenstück im aktiven Projekt frisch geprüft | 156 | 0,000 | Nachweise im Inventar; keine aktuelle Löschfreigabe |
| Identisches erhaltenes externes Gegenstück/ZIP-Eintrag geprüft | 2.236 | 0,507 | Nachweise im Inventar; keine aktuelle Löschfreigabe |

Alle 14.277 Dateien wurden frisch gehasht. Zusätzlich wurden 1.547 erhaltene externe Vergleichsdateien erneut gehasht und die beiden bestehenden RawEvidence-ZIP-Archive vollständig auf ihren bekannten SHA-256 geprüft; deren zuvor verifizierte Eintragshashes wurden für Vergleiche verwendet. Das aktive Projekt wurde ergänzend vollständig nach passenden Dateigrößen durchsucht und 2.116 weitere mögliche Gegenstücke frisch gehasht. Dabei wurden 156 weitere identische Kleinstdateien nachgewiesen. Es bleiben **8.273 Nachweis-/Diagnosedateien mit 6.350.870.213 Bytes (5,915 GiB)** ohne belegtes identisches Gegenstück im untersuchten Bestand, zuzüglich der zwei Blenderdateien.

„Kein Gegenstück belegt“ bezieht sich auf das aktive Projekt, die untersuchten PokeMonster-Altordner, die GitHub-Historie, den Vollbackup-Commit und die zwei geprüften Archive. Es ist keine Behauptung über sämtliche sonstigen Datenträger oder unbekannte Archive. Diese Dateien werden nicht allein aufgrund ihrer Endung zur Entfernung empfohlen.

## 3. Zwei lokale Blender-Zwischenstände

Beide liegen nur als bearbeitbare historische Stände im untersuchten alten Worktree vor. Kein identischer Hash in aktiven Quellen, GitHub-/Vollbackup-Nutzdaten oder den geprüften Gegenstücken belegt.

| Vollständiger Pfad | Bytes | SHA-256 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2HealingArtV4/GardenDetails_BeforeIvyCurl.blend` | 2.971.970 | `1e8b791a5670f11986d754ea57a1ad46ab924ba65fc64c965d422f4f7ff5de6f` |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2HealingArtV4/GardenDetails_BeforeIvyPlacement.blend` | 2.971.954 | `fce63a25d8309e39b0ab2ce1dafecc04bea86a0a6c92fc6f7e405a74aaabdc59` |

Zusammen **5.943.924 Bytes / 5,67 MiB**. Beide mit Blender 5.2.2 separat schreibfrei geöffnet: jeweils sechs Meshobjekte, keine fehlenden benutzten Texturen/Bibliotheken, nach dem Öffnen SHA-256 unverändert. Die benutzte Terrakottatextur ist gepackt.

Die aktuellen Quellen `Art/World/VisualV2HealingArtV4/Source/HealingHouse_GardenDetails_V4.blend` und `HealingHouse_PottedPlants_V4.blend` im aktiven Projekt ebenfalls erneut geöffnet: sechs beziehungsweise neun Objekte, keine fehlenden benutzten Abhängigkeiten. Der aktuelle Garden-Stand enthält dieselben sechs Objektnamen und Polygonzahlen wie die Zwischenstände. Das beweist **keine vollständige inhaltliche Ersetzung**: die Dateihashes unterscheiden sich, frühere Efeuform-/Platzierungsstände könnten weiterhin für Rückgriffe nützlich sein.

**Vor Entfernung erforderlich:** ausdrücklich entscheiden, ob diese zwei Zwischenstände erhalten werden sollen. Falls ja, später nach Freigabe gezielt in den aktiven Projektbestand übernehmen und prüfen; keine neue Projektkopie erforderlich. Jetzt nichts kopiert oder verschoben.

### Aktuelle Blenderquellen unabhängig geprüft

Alle **95 versionierten Blenderdateien** im aktiven Projekt frisch mit deaktivierter automatischer Skriptausführung erneut geöffnet; unverändert. Keine fehlenden benutzten Bibliotheken, ungepackten Bilddateien oder geprüften weiteren externen Dateidaten und **keine benutzte Abhängigkeit auf den alten Worktree** festgestellt. Einzelne Quellen sind Datenbibliotheken ohne eigene Szene; entsprechende Blender-Hinweise sind kein Öffnungsfehler.

Der erste Hintergrundstart in der eingeschränkten Sandbox stürzte bereits bei der Metal-Initialisierung vor dem Öffnen einer Quelle ab (Exit 139). Der danach freigegebene Start außerhalb dieser Einschränkung sowie der vollständige Quellenlauf endeten regulär mit Exit 0. Keine `.blend` gespeichert, kein Rigging, Reimport oder Render ausgeführt.

## 4. Unreal-Importabhängigkeiten

Die vorhandene Live-Unreal-Inventur `Saved/ProjectMigration/Imports.json` enthält **391 AssetImportData-Quelldateieinträge**, darunter keinen tatsächlich auf den alten Worktree aufgelösten Quellpfad. Die betroffenen UAssets wurden inzwischen frisch gegen ihre unveränderten Git-/LFS-Inhalte geprüft; es gab hier keine neue Editor-Inventur oder Reimportoperation.

Ein frischer binärer Scan sämtlicher `.uasset`-/`.umap`-Dateien findet trotzdem sieben Assets mit alten absoluten Pfaden in gespeicherten Interchange-Metadaten, darunter Factory-/Node-IDs. Die zugehörigen sieben Texturen im aktiven Projekt existieren und sind frisch **SHA-256-identisch** zu den alten Dateien:

| Aktives UAsset | Quelltextur relativ zu aktivem Projekt und altem Worktree |
| `Content/Environment/VisualV2HealingArtV3/Textures/T_HA3_Meadow.uasset` | `Art/World/VisualV2HealingArtV3/Textures/T_HA3_Meadow.png` |
| `Content/Environment/VisualV2HealingArtV3/Textures/T_HA3_Earth.uasset` | `Art/World/VisualV2HealingArtV3/Textures/T_HA3_Earth.png` |
| `Content/Environment/VisualV2HealingArtV4/Textures/T_HA4_Wood.uasset` | `Art/World/VisualV2HealingArtV4/Textures/T_HA4_Wood.png` |
| `Content/Environment/VisualV2HealingArtV4/Textures/T_HA4_Meadow.uasset` | `Art/World/VisualV2HealingArtV4/Textures/T_HA4_Meadow.png` |
| `Content/Environment/VisualV2HealingArtV4/Textures/T_HA4_Earth.uasset` | `Art/World/VisualV2HealingArtV4/Textures/T_HA4_Earth.png` |
| `Content/Environment/VisualV2WorldArtV5/Textures/T_WA5_ForestFloor.uasset` | `Art/World/VisualV2WorldArtV5/Textures/T_WA5_ForestFloor.png` |
| `Content/Environment/VisualV2WorldArtV5/Textures/T_WA5_WetBank.uasset` | `Art/World/VisualV2WorldArtV5/Textures/T_WA5_WetBank.png` |

Die lokale UE-5.8-Implementierung `InterchangeTextureFactory.cpp:2427` liest Reimport-Quelldateinamen über AssetImportData; `InterchangeManager.cpp:1579–1629` erzeugt daraus das SourceData-Objekt. Ein altes Factory-ID-Fragment allein beweist daher keine notwendige physische Quelldatei am alten Ort. **Der vollständige Reimport ohne erreichbaren alten Worktree wurde aber nicht praktisch geprüft.** Deshalb weder einen zwingenden Runtimefehler behaupten noch diese Metadaten als abschließend harmlos freigeben. Vor endgültiger Entfernung ist ein kontrollierter Reimport-Nachweis beziehungsweise eine gezielte Metadatenprüfung zu empfehlen, ohne Originalassets ungeprüft zu überschreiben.

Vier bereits bekannte WestlandRegion-Pflanzenassets lösen ihre relativen Importpfade nach `/Users/Shared/Art/HealingHouse/Exports/QualityV3/` auf. Die tatsächlichen FBX-Quellen unter `Art/HealingHouse/Exports/QualityV3/` im aktiven Projekt sind erhalten. Dieser ältere Metadatenfehler ist unabhängig vom alten Worktree; keine neue Quellkorrektur durchgeführt.

Keine nur unversioniert/ignoriert vorhandenen zusätzlichen Assets oder Quellen unter `Art/`, `Content/` oder `Source/` des alten Worktrees gefunden. Keine aktive C++-/Config-Abhängigkeit auf dessen physischen Projektpfad festgestellt.

## 5. Entwicklungsnachweise und Werkzeuge

Im ignorierten `Saved` verbleiben 10.768 Dateien. Ein Teil ist exakt extern archiviert oder durch Git-Nutzdaten belegt; ein erheblicher Teil ist ausschließlich als historische Aufnahme/Protokoll im Prüfbestand vorhanden. Darunter:

- QHD-Aufnahmen der Heilhaus-, WorldArt-V5/V6/V7- und ShadowQuality-V8-Durchgänge; keine neue GitHub-Sicherung voraussetzen.
- Profiling-/CSV-/Engine-Logs und ursprüngliche Testzustände. Die damalige genaue Messung ist nicht durch bloßes erneutes Ausführen reproduzierbar.
- Acht `DevSaveTestResult.sav` ohne belegtes identisches Gegenstück: Testresultate unter Acceptance-Ordnern, kein aktives `Saved/SaveGames` im alten Worktree. Auch diese Dateien wurden nicht freigegeben oder entfernt. Der aktive Dev-Spielstand bleibt im aktiven Projekt.
- Kleine Konfigurations-, SourceControl- und Autosave-Metadaten. `Saved/Autosaves/PackageRestoreData.json` ist 90 Bytes; keine zusätzliche nur dort vorhandene `.umap` gefunden.

Historische Werkzeuge können weiterhin Rohdaten verlangen, auch wenn das Spiel sie nicht lädt. Beispiele: `ComposeReview.py` verarbeitet frühere Saved-Fotos; `ProtectionAudit.py`/`ValidateOriginal.py` lesen damalige Ausgangsinventare; `ApplyMotionBlur.py` verlangt das externe `MapBackup.json`. Diese Nachweispfade dürfen nicht als allgemeine Laufzeitabhängigkeiten ausgegeben werden.

**Konkreter Altpfad im aktiven unversionierten Werkzeug:** `Tools/VisualV2EnvironmentQualityV1/Startup.py:5` verlangt per Assertion weiterhin den alten Worktree. Das ist ein historischer Experiment-Einstiegspunkt, keine aktuelle Gameplay-/Buildfunktion. Für künftige Wiederverwendung müsste er separat freigegeben angepasst werden; jetzt unangetastet erhalten. Die beiden anderen gefundenen alten Pfadstrings in `Tools/ProjectMaintenance` dienen ausdrücklich dem Erkennen alter Verweise und sind keine Abhängigkeit darauf.

`Tools/DevelopmentEvidence` unterscheidet bereits benötigte Pflichtdateien und optionale historische Medien. Fehlende optionale Medien können verständlich als nicht ausgeführte Review melden; das ersetzt nicht die Entscheidung über die bisher nur lokalen neuen Art-Nachweise. Alte Reports können ihre absoluten Screenshotlinks verlieren, falls die betreffenden Dateien später entfernt werden.

Riders `recentSolutions.xml` nennt als zuletzt geöffnetes Projekt die aktive `.uproject`. In der bestehenden Umstellungsprüfung startete Unreal vom aktiven Pfad. Keine zur Prüfzeit offene Anwendung benötigte Dateien im alten Worktree. Der Arbeitsordner dieses Codex-Chats bleibt technisch der ChatGPT-Projektspiegel; alle PokeMonster-Prüfbefehle verwenden ausdrücklich den aktiven Projektpfad, nicht den alten Worktree.

## 6. Git-Worktree-Verwaltung und späterer Ablauf

Aktuell genau zwei registrierte Worktrees:

```text
/Users/harry/Developer/PokeMonster
  HEAD 427d93f92765b2e03d8dca186fbc6bfbd86c8605  refs/heads/main
/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree
  HEAD 30a165b034114ba4b0940a369e73143db988afad  refs/heads/codex/slim-backup-v5
```

Das alte `.git` ist eine 67-Byte-Verweisdatei auf `/Users/harry/Developer/PokeMonster/.git/worktrees/Worktree`. Dort zeigt `commondir` mit `../..` auf die aktive gemeinsame `.git`. Die Rückverbindung `gitdir` ist korrekt. Kein `locked`-Eintrag, keine Submodule, kein Reparaturbedarf.

**Erst nach ausdrücklicher Freigabe und Klärung der oben genannten Dateien:**

1. Entscheidung über lokale Blender-Zwischenstände und historische Nachweise festhalten; erforderliche Daten gegebenenfalls gezielt in den aktiven Bestand übernehmen, Hashes prüfen. Keine pauschale Sicherung/Kopie anlegen.
2. Offenen Texture-Reimport-Nachweis und historische Werkzeugabhängigkeiten klären. Keine stillen Assetänderungen.
3. Neue Abschlussinventur: keine Änderungen seit der Freigabeliste, keine offenen Anwendungen, Main/Remote und beide Vollbackup-Refs prüfen.
4. Den alten **verknüpften Worktree über Git** entfernen, nicht mit Finder/`rm` plus manuellem Löschen der Verwaltung:

```sh
git -C /Users/harry/Developer/PokeMonster worktree remove /Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree
```

**Diesen Befehl jetzt nicht ausführen. Ein sauberer normaler `git status` schützt ignorierte Saved-Dateien nicht vor Entfernung.** `git worktree remove` entfernt den gesamten Checkout und seine Zuordnung; auf ein automatisches Stoppen wegen ignorierter Dateien darf man sich nicht verlassen. Bei Verweigerung nicht automatisch `--force` ergänzen, sondern den konkreten Befund prüfen. Der Branch `codex/slim-backup-v5` kann erhalten bleiben; Branchlöschung ist nicht nötig.

5. Danach Root-Status, `git worktree list`, beide Backup-Refs, GitHub-Verbindung, LFS-Objekte, Quellen und wichtigste Maps kontrollieren. Keine Garbage Collection, kein LFS-Prune, kein History-Rewrite; `FullBackup`/`FullRestore` und der übergeordnete Sicherungsordner bleiben bestehen. Tatsächlichen freien Speicher vorher/nachher messen.

## 7. Tests, Grenzen und Abschlusszustand

**In diesem Auftrag neu:** schreibfreie komplette Worktree-Inventur/SHA-256, APFS-Privatbelegung, Checkout-/Core-Prüfung, erneute Öffnung der 95 aktiven Blenderquellen und der zwei lokalen Zwischenstände, vollständige lokale LFS-SHA-Prüfung, direkte Remote-Abfrage, serverseitige LFS-Verfügbarkeitsprüfung, Git-Objekt-/Bundleprüfung und Importmetadaten-/Pfadscan.

**Nicht erneut ausgeführt:** Unreal-Build, Automation, PIE-Fußlauf oder Reimport. Die unveränderten Quellen/Assets entsprechen weiterhin dem unmittelbar zuvor geprüften Stand aus `SPEICHERBEREINIGUNG_V3_PRUEFBERICHT.md`: Build Exit 0; alle 49 Automationstests abgeschlossen, eine Warnungsgruppe mit den bekannten zwei `idevice_id`-Meldungen; fünf Maps geladen, je 0 Map-Check-Fehler/-Warnungen. Der vollständige Gameplay-Fußlauf und die damalige Reimportquellen-Inventur stammen aus der Projektumstellung. Keine neuen Gameplaytests behauptet.

Der alte Worktree blieb während der aktuellen Prüfung erreichbar. Daher ist ein vollständiger Laufzeittest unter physisch nicht vorhandenem Altpfad **noch offen**; keine Verzeichnisse zu Testzwecken umbenannt oder ausgeblendet.

Am Ende alle 14.277 alten Dateien auf Größe, mtime, Inode und Hardlinkzahl unverändert; keine neuen Dateien im alten Worktree. Alle 38 ursprünglichen unversionierten Nutzerdateien SHA-256-identisch. `git diff --check` ohne Befund; keine versionierten Änderungen, kein Staging, keine geänderten Refs oder Worktree-Registrierungen. Nur Bericht und Inventar kommen zum vorherigen unversionierten Bestand hinzu.

**Entscheidungsvorschlag:** Alten Worktree künftig aufgeben, aber die vollständige Entfernung erst nach Entscheidung über die zwei Blenderstände und die nicht anderweitig belegten Nachweise sowie dem gezielten Reimport-Nachweis freigeben. Potenziell zusätzlich rund **7,93 GiB** unmittelbar exklusiven Speicher gewinnen. Heute keine Bereinigung.

## 8. Nachvollziehbare Dateien

- Dieser Bericht: `/Users/harry/Developer/PokeMonster/Docs/ALTER_WORKTREE_ENTFERNUNG_PRUEFBERICHT.md`.
- Vollständiges aktuelles Dateiinventar mit Pfaden, Bytes, SHA-256, APFS-Privatbelegung und geprüften Gegenstücken: `/Users/harry/Developer/PokeMonster/Docs/ALTER_WORKTREE_DATEIINVENTAR.csv`. **Prüfinventar, keine Löschliste und keine Löschfreigabe.**
- SHA-256 des Dateiinventars: `ca305d60cf1f716bff4657f2d589cd8f466f07bda6fc4c03dc2e768ad30a8897`.
- Rohresultate dieser reinen Prüfung liegen unter `/tmp/pokemonster_worktree_removal_*.json`; temporär, nicht als dauerhafte Sicherung behandeln. Das dauerhafte Inventar enthält die Einzeldateibefunde. Bereits vorhandene Umstellungs-/Bereinigungsnachweise unter aktivem `Saved/ProjectMigration/` und `Saved/StorageCleanupV3/` bleiben unverändert.
