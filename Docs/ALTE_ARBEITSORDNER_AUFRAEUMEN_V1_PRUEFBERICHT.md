# PokeMonster – Alte Arbeitsordner aufräumen V1: reine Bestandsprüfung

Stand: 19.10.2026, 19:26 CEST. Keine Bereinigung durchgeführt.

**Ergebnis:** 26 eindeutig PokeMonster zugehörige Ordner unter `/Users/harry/Documents/Codex`, zusammen 62.847 Dateien. Sie belegen nach Abzug mehrfach gezählter Hardlinks **105,084 GiB Dateiblöcke**. Ein konservativ begründbarer Bereinigungsumfang beträgt **40,595 GiB**; davon rund **11,503 GiB** alte Checkout-Dateien und erzeugbare Ausgaben. Weitere rund **29,092 GiB** sind nachgewiesene Mehrfachkopien, deren erhaltene Gegenstücke ausdrücklich geschützt bleiben müssen. Das ist ein Vorschlag nach Freigabe, keine Löschfreigabe und keine garantierte Zunahme des freien APFS-Speichers.

Der aktive Entwicklungsort bleibt ausschließlich `/Users/harry/Developer/PokeMonster`; keine neue Projektkopie, kein Versionsordner, keine Sicherung und keine Map angelegt. Nur dieser Bericht wird im Projekt neu erstellt. Kein Staging, Commit oder Push.

## 1. Git-, GitHub- und Datenerhalt

| Prüfung | Tatsächlich ermittelter Stand |
|---|---|
| Aktiver HEAD / Branch | `427d93f92765b2e03d8dca186fbc6bfbd86c8605`, `main → origin/main` |
| Direkter GitHub-Abgleich | `git ls-remote origin refs/heads/main`: identischer Hash; kein Fetch/Pull/Push erforderlich |
| Remote | `git@github.com:Harrys-F/PokeMonster.git`; unverändert |
| Aktiver versionierter Bestand | 3.514/3.514 Dateien per SHA-256 gegen die tatsächlichen Git-/LFS-Nutzdaten geprüft; keine Abweichung |
| 38 unversionierte Dateien | 38/38 SHA-256-identisch zum Umstellungsjournal, zusammen 3.405.352 Bytes; ausschließlich im aktiven Projekt erhalten |
| Alter Worktree | `codex/slim-backup-v5`, `30a165b034114ba4b0940a369e73143db988afad`; 3.508/3.508 versionierte Dateien identisch; keine eigenen unversionierten oder versionierten Änderungen |
| Vollbackup | `03492bd96b4dba44692f675c19d5f11abfa86b4b` unverändert unter `backup/full-03492bd` und `refs/archive/pokemonster/full-backup-03492bd`; nicht Teil der schlanken Remote-Historie |
| Vollbackup-LFS im aktiven .git | 9.451 Objekte / 16.442.940.729 Bytes; vollständig vorhanden, alle SHA-256 korrekt |
| LFS der gesamten schlanken Remote-Historie | 1.383 Objekte / 6.607.098.907 Bytes; alle lokal SHA-256-geprüft und frisch von GitHub als download-verfügbar bestätigt |
| FullBackup-Archiv-LFS | 9.559 Objekte / 16.558.852.545 Bytes; vollständig nach Archivmanifest SHA-256-geprüft. Der größere Umfang enthält zusätzliche historische Objekte |
| FullRestore | 11.343/11.343 ursprüngliche Dateien SHA-256-identisch sowohl zu Commit 03492bd als auch zum Archivmanifest |
| Git-Bundle | `FullBackup/PokeMonster_full_03492bd.bundle`: Git bestätigt vollständige gültige Historie; 624.857.686 Bytes; Hash siehe unten |
| Pflichtdatei-Prüfung | Aktuelles Core-Manifest: 3.513 geprüft, keine fehlenden/veränderten Pflichtdateien |
| Diff-Prüfung | `git diff --check` ohne Befund; keine Änderungen an bestehenden Quellen oder Assets |

GitHub-LFS wurde ausschließlich mit Download-Batch-Metadaten geprüft; keine Binärdateien hoch-/heruntergeladen, keine Käufe, keine Budgetänderung. Die Prüfung bestätigt verfügbare Projektobjekte, nicht ein kontoweites Abrechnungskontingent. Optionale Dateien, die nicht in `origin/main` oder dessen Historie liegen, gelten hier ausdrücklich nicht als durch GitHub gesichert.

## 2. Messmethode und Grenzen der Speicherangaben

- Vollständige Verzeichnisinventur mit Dateigröße, belegten 512-Byte-Blöcken, Geräte-/Inodekennung und Hardlinkanzahl; keine Symlinks in den untersuchten Bäumen gefunden.
- **Logische Größe** bezeichnet Dateilängen; **Belegung** zählt Dateiblöcke pro Inode einmal. 1 GiB = 1.073.741.824 Bytes. Ordner-/Dateisystemmetadaten sind nicht vollständig enthalten.
- 1.783 mehrfach verlinkte Dateisätze ergeben 1,495 GiB nominelle Doppelzählung. Keine Hardlinks zwischen dem alten und dem aktiven Projekt gefunden. Alle für Gruppe A angesetzten Hardlinks liegen vollständig in A; kein verbliebener Hardlink wurde als freier Speicher gerechnet.
- APFS-Klone, Snapshots und gemeinsam genutzte Extents lassen sich mit dieser Dateiprüfung nicht exklusiv zuordnen. Die tatsächlich frei werdenden Volume-Blöcke können kleiner sein. Einen exakten garantierten Nettofreigewinn kann man vor einer autorisierten Entfernung nicht seriös nennen.
- 76.460 relevante Dateien beziehungsweise Git-/LFS-Nutzdateien per SHA-256 gelesen, ohne Lesefehler oder Änderungen während des Hashens. Offensichtlich generierte Intermediate-/Modulcache-Dateien wurden nach Herkunft und Struktur eingeordnet; nicht jeder Cacheblock wurde zusätzlich gehasht.
- Kein Unreal-/Blender-Neustart, Build, Cook, Benchmark oder neuer Gameplay-Test: dieser Auftrag verändert keine funktionalen Projektdateien. Vorherige Tests werden nicht als neu ausgeführt ausgegeben.

## 3. Ordnerübersicht

Alle folgenden Ordner liegen direkt unter `/Users/harry/Documents/Codex`. Kein Tabellenwert erlaubt eine pauschale Entfernung des gesamten Ordners. Die Spalte „A-Potenzial“ zählt nur die konkret begründeten Dateigruppen; B und C bleiben erhalten.

| Ordner | Dateien | Logisch GiB | Belegung GiB | Inhalt | GitHub-Sicherung | Empfehlung | A-Potenzial GiB |
|---|---:|---:|---:|---|---|---|---:|
| [PokeMonster_GitSicherung_V1_2026-10-16](/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V1_2026-10-16) | 69 | 0,023 | 0,023 | Git-/LFS-Inventur, Einordnung, Prüfbericht; keine Projektkopie | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,000 |
| [PokeMonster_GitSicherung_V2_2026-10-16](/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V2_2026-10-16) | 65 | 0,025 | 0,025 | Whitespace-/LFS-Prüfungen, Sicherungsplan, Inventare | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,000 |
| [PokeMonster_GitSicherung_V3_2026-10-16](/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V3_2026-10-16) | 37 | 0,012 | 0,012 | Commit-/Index-/LFS-Nachweise zum Vollbackup | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,000 |
| [PokeMonster_GitSicherung_V4_2026-10-16](/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V4_2026-10-16) | 41 | 0,042 | 0,042 | A–F-Einordnung und Ausschlusslisten | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,000 |
| [PokeMonster_GitSicherung_V5_2026-10-16](/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16) | 48,941 | 73,020 | 71,628 | Alter Worktree, FullBackup, FullRestore, Upload-/Build-Nachweise; zwingend aufteilen | Quellen im Remote; Vollbackup lokal; Reviewdaten nur teilweise | Worktree, Archive und Nachweise getrennt behandeln; keine Gesamtentfernung | 30,113 |
| [PokeMonster_GitSicherung_V6_2026-10-16](/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V6_2026-10-16) | 69 | 0,013 | 0,013 | Uploadvorbereitung und Resume-Protokolle | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,000 |
| [PokeMonster_GitSicherung_V7_2026-10-17](/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V7_2026-10-17) | 99 | 0,009 | 0,009 | SIGPIPE-/Push-/LFS-Nachweise, kleine Git-Pack-Testdateien | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,000 |
| [PokeMonster_Git_Sicherung_2026-10-15](/Users/harry/Documents/Codex/PokeMonster_Git_Sicherung_2026-10-15) | 10 | 0,001 | 0,001 | Frühe Sicherungsanalyse und Befehlsvorschläge | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,000 |
| [PokeMonster_ShadowQuality_V8_2026-10-19](/Users/harry/Documents/Codex/PokeMonster_ShadowQuality_V8_2026-10-19) | 59 | 0,026 | 0,026 | A/B/C-Schattenvergleich, Map-Zwischenstand und lokale QHD-Bilder | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,004 |
| [PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18](/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18) | 953 | 4,659 | 4,661 | AA-/Shadow-Bilder, Messdaten, RawMeasurements.zip | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,007 |
| [PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17](/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17) | 313 | 1,295 | 1,296 | Vergleichsbilder, Messungen, ursprüngliche Prüfung | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,000 |
| [PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17](/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17) | 251 | 2,143 | 2,144 | GPU-Messungen und 1,873 GiB MetalSystemTrace.trace | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,006 |
| [PokeMonster_VisualV2_HeilhausArt_V3_2026-10-19](/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V3_2026-10-19) | 91 | 0,144 | 0,144 | V3-Bildvergleich, Originalaufnahmen, Map-Vorstand | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,003 |
| [PokeMonster_VisualV2_HeilhausArt_V4_2026-10-19](/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V4_2026-10-19) | 64 | 0,081 | 0,082 | V4-Bildvergleich, Zwischenkarten, Fassadenprüfung | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,003 |
| [PokeMonster_VisualV2_MaterialFix_V1_2026-10-18](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18) | 276 | 0,551 | 0,552 | Strauchmaterialnachweise, Bilder und Messarchiv | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,007 |
| [PokeMonster_VisualV2_QualityV2_2026-10-17](/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17) | 372 | 1,246 | 1,247 | Motion-Blur-Abnahme, Bilder und Map-Sicherung | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,003 |
| [PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18) | 8,062 | 16,545 | 16,561 | Entpackte TAA-Nachweise plus identisches RawEvidence.zip, Videos | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 8,136 |
| [PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18](/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18) | 2,251 | 4,768 | 4,773 | Entpackte Vegetationsnachweise plus identisches RawEvidence.zip, Videos | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 2,294 |
| [PokeMonster_VisualV2_WorldArtQuality_V1_2026-10-19](/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V1_2026-10-19) | 193 | 0,347 | 0,348 | Heilhaus-V1-Nachweise, Vorherkarte, Bilder | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,005 |
| [PokeMonster_VisualV2_WorldArtQuality_V2_2026-10-19](/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V2_2026-10-19) | 34 | 0,029 | 0,030 | Pflanzengruppen-/Materialvergleich und Vorherkarte | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,003 |
| [PokeMonster_WorldArt_V5_2026-10-19](/Users/harry/Documents/Codex/PokeMonster_WorldArt_V5_2026-10-19) | 113 | 0,300 | 0,300 | Wald-/Wiesen-/Uferaufnahmen, Originale und Vergleichsbilder | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,003 |
| [PokeMonster_WorldArt_V6_2026-10-19](/Users/harry/Documents/Codex/PokeMonster_WorldArt_V6_2026-10-19) | 129 | 0,377 | 0,377 | Weg-/Vegetationsaufnahmen, Originale und Vergleichsbilder | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,003 |
| [PokeMonster_WorldArt_V7_2026-10-19](/Users/harry/Documents/Codex/PokeMonster_WorldArt_V7_2026-10-19) | 63 | 0,023 | 0,023 | Stilübertragung und Schatten-Diagnose, lokale Vergleichsbilder | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,003 |
| [PokeMonster_ZentraleReferenzmap_V1_2026-10-17](/Users/harry/Documents/Codex/PokeMonster_ZentraleReferenzmap_V1_2026-10-17) | 60 | 0,093 | 0,093 | Historischer Integrationsplan, Actor-/Referenzinventare | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,000 |
| [Projektbereinigung_PokeMonster_2026-10-16](/Users/harry/Documents/Codex/Projektbereinigung_PokeMonster_2026-10-16) | 45 | 0,050 | 0,050 | Erste Bereinigungsanalyse, Kandidatenlisten und Registry-Daten | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,000 |
| [Projektbereinigung_PokeMonster_V2_2026-10-16](/Users/harry/Documents/Codex/Projektbereinigung_PokeMonster_V2_2026-10-16) | 187 | 0,626 | 0,627 | Frühere Backup-/Quarantänebestände, Prüfungen und Nachweise | Historische Berichte/Quellstände teilweise; rohe Nachweise überwiegend nur lokal | B/C erhalten; nur ausgewiesene A-Dateien nach Freigabe | 0,000 |

### Größte Teilbestände in GitSicherung V5

| Teilordner | Logisch GiB | Belegung GiB | Status und Empfehlung |
|---|---:|---:|---|
| [Worktree](/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree) | 37,451 | 36,017 | Gemischt: alter Checkout und C-Nachweise; sieben Importquellen sowie zwei Blender-Zwischenstände vorerst schützen. Nicht entfernen. |
| [FullBackup](/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/FullBackup) | 16,014 | 16,032 | B: gültiges Git-Bundle plus LFS-Nutzdaten und Manifest; unverändert erhalten. |
| [FullRestore](/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/FullRestore) | 19,477 | 19,500 | B: unabhängig wiederhergestelltes Vollbackup einschließlich bisheriger Builddaten; in dieser Empfehlung insgesamt geschützt. |
| [SwiftModuleCache](/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/SwiftModuleCache) | 0,060 | 0,061 | A: neu erzeugbarer Swift-Modulcache; nur nach Freigabe. |

`FullRestore` ist ein eigenständiges lokales Repository, kein dritter registrierter Worktree. Sein `origin` zeigt auf das lokale Bundle in `FullBackup`, nicht auf GitHub. Beide Bestände hängen deshalb für Wiederherstellungsvorgänge zusammen. Das Bundle allein enthält keine LFS-Binärdaten. Alles liegt auf derselben internen SSD und ist keine externe Datenträgersicherung.

Ein gewöhnlicher Git-Status in FullRestore zeigte LFS-Dateien als geändert; ein direkter Filtervergleich scheitert hier am erforderlichen Schreibzugriff in `.git/lfs/tmp`. Daher wurde keine Clean-/Smudge-Neuschreibung erzwungen und nichts konfiguriert. Der schreibfreie Inhaltsvergleich bestätigt stattdessen alle 11.343 tatsächlichen Dateiinhalte exakt. Im dortigen `.git` wurden keine neuen oder geänderten Dateien festgestellt. Dies ist kein Freibrief, FullRestore als aktiven Arbeitsbaum zu verwenden.

### Datierte und nicht eindeutig PokeMonster zugehörige Ordner

| Ordner | Belegung GiB | Befund / Einordnung |
|---|---:|---|
| [2026-09-25](/Users/harry/Documents/Codex/2026-09-25) | 2,210 | C / außerhalb des PokeMonster-Bereinigungsumfangs: anderer Pokémon-Echo-Lokalisierungsauftrag mit Arbeitsdaten und zwei ZIP-Ergebnissen, keine PokeMonster-Projektkopie. |
| [2026-09-28](/Users/harry/Documents/Codex/2026-09-28) | 0,001 | C: kleine frühere Auftrags-/Arbeitsdateien; keine Unreal-/Git-Projektkopie gefunden. Nicht pauschal zuordnen. |
| [2026-09-29](/Users/harry/Documents/Codex/2026-09-29) | 0,025 | B/C: enthält Umstellungsjournal, Inventare und lokale Gesprächsunterlagen; Journal für die 38 Dateien weiterhin benötigt. |

Die datierten Ordner 2026-09-30, 2026-10-01/02/03/04/05/06/07/09/13/16 enthalten derzeit keine regulären Dateien in den vorhandenen Unterverzeichnissen; kein relevanter Speichergewinn angesetzt, nichts entfernt. Gesamter untersuchter Codex-Bestand einschließlich fremder/datierten Daten: logisch 108,547 GiB, eindeutige Dateiblöcke 107,319 GiB. Nur die 26 eindeutig PokeMonster zugehörigen Ordner sind in A/B/C-Summen enthalten.

## 4. Die 30,7 GiB ignorierten Dateien des alten Worktrees

Tatsächlich **23,497 Dateien / 32,954,721,195 Bytes = 30,691 GiB logisch**. Die folgenden Gruppen sind disjunkt nach ihrem relativen Anfangspfad; Blockgrößen je Gruppe werden wegen gruppenübergreifender Hardlinks nicht addiert.

| Pfad relativ zum alten Worktree | Dateien | Logisch GiB | Wesentlicher Inhalt |
|---|---:|---:|---|
| `Saved/VisualV2TAAIntegrationV1/` | 10,575 | 10,127 | Bildfolgen, Screenshots, Messdaten und Abnahmeprotokolle |
| `Saved/VisualV2AASoftShadowsV1/` | 921 | 5,283 | Bildfolgen, Screenshots, Messdaten und Abnahmeprotokolle |
| `Intermediate/Build/` | 496 | 2,819 | Erzeugbare Compiler-/Assetregistry-Zwischenprodukte |
| `Saved/VisualV2VegetationPerfV1/` | 1,094 | 1,653 | Bildfolgen, Screenshots, Messdaten und Abnahmeprotokolle |
| `Saved/VisualV2QualityV2/` | 375 | 1,237 | Bildfolgen, Screenshots, Messdaten und Abnahmeprotokolle |
| `Saved/VisualV2MaterialFixV1/` | 244 | 1,220 | Bildfolgen, Screenshots, Messdaten und Abnahmeprotokolle |
| `Saved/Profiling/` | 6,820 | 1,061 | Rohmessungen und Laufzeitprotokolle; exakte historische Messung nicht neu erzeugbar |
| `Saved/VisualV2HealingArtV3/` | 342 | 1,018 | Bildfolgen, Screenshots, Messdaten und Abnahmeprotokolle |
| `Saved/VisualV2ShadowQualityV8/` | 211 | 0,975 | Bildfolgen, Screenshots, Messdaten und Abnahmeprotokolle |
| `Saved/VisualV2HealingArtV4/` | 295 | 0,904 | Bildfolgen, Screenshots, Messdaten und Abnahmeprotokolle |
| `Saved/VisualV2WorldArtV6/` | 189 | 0,754 | Bildfolgen, Screenshots, Messdaten und Abnahmeprotokolle |
| `Saved/VisualV2EnvironmentQualityV1/` | 184 | 0,737 | Bildfolgen, Screenshots, Messdaten und Abnahmeprotokolle |
| `Saved/VisualV2WorldArtV7/` | 171 | 0,712 | Bildfolgen, Screenshots, Messdaten und Abnahmeprotokolle |
| `Saved/VisualV2WorldArtV5/` | 167 | 0,616 | Bildfolgen, Screenshots, Messdaten und Abnahmeprotokolle |
| `Saved/VisualV2WorldArtQualityV2/` | 218 | 0,466 | Bildfolgen, Screenshots, Messdaten und Abnahmeprotokolle |
| `Saved/Shaders/` | 8 | 0,343 | Erzeugter Metal-Shadercode |
| `Saved/VisualV2WorldArtQualityV1/` | 126 | 0,285 | Bildfolgen, Screenshots, Messdaten und Abnahmeprotokolle |
| `Saved/VisualV2GPUBottleneckV1/` | 147 | 0,224 | Bildfolgen, Screenshots, Messdaten und Abnahmeprotokolle |
| `Intermediate/CachedAssetRegistry/` | 2 | 0,133 | Erzeugbare Compiler-/Assetregistry-Zwischenprodukte |
| `Saved/EnvironmentPerfV2/` | 528 | 0,077 | Bildfolgen, Screenshots, Messdaten und Abnahmeprotokolle |
| `Saved/EnvironmentPerfV1/` | 116 | 0,034 | Bildfolgen, Screenshots, Messdaten und Abnahmeprotokolle |
| `Saved/ShaderDebugInfo/` | 37 | 0,008 | Bildfolgen, Screenshots, Messdaten und Abnahmeprotokolle |
| `Binaries/Mac/` | 3 | 0,004 | Erzeugbare Build-/Cachedateien |
| `DerivedDataCache/VT/` | 5 | 0,002 | Erzeugbare Build-/Cachedateien |

Nach Endung: 2.772 PNG-Dateien mit 16.122.583.741 Bytes und 10.783 JPG-Dateien mit 10.132.290.247 Bytes, zusammen 24,452 GiB logisch. Die Videos außerhalb des Worktrees bestehen teilweise aus diesen Bildfolgen. Rohframes sind echte historische Nachweise, keine Laufzeittexturen; ihre einmaligen Aufnahmen werden nicht automatisch als verzichtbar erklärt.

In den ignorierten Dateien werden 14.862 Dateien / 24,771 GiB logisch als A vorgeschlagen, ein vorhandener Prüftext als B und 8.634 Dateien / 5,920 GiB als C. Hardlinks verringern den möglichen Blockgewinn. Zwei ignorierte Blenderquellen sind ausdrücklich C (siehe unten). Kein Nutzer-Spielstand im alten Worktree gefunden; `Saved/Autosaves/PackageRestoreData.json` ist lediglich eine 90-Byte-Metadatendatei und bleibt ohne pauschale Saved-Löschung erhalten.

## 5. A – nach ausdrücklicher Freigabe entfernbar

Die Klassifikation schützt zuerst FullBackup/FullRestore, registrierte Git-Verweise, lokale Originalquellen und die sieben alten Importpfade. Erst danach werden Dubletten und erzeugbare Dateien bewertet. Keine pauschale Endungsregel für Bilder, FBX oder Blenderdateien.

| Dateigruppe / genaue Auswahlregel | Begründung und erhaltene Grundlage | Risiko / Freigabebedingung |
|---|---|---|
| Alter Worktree: versionierte Dateien aus Commit `30a165b`, **ausgenommen die sieben Texturpfade in Abschnitt 7** | Alle Inhalte SHA-identisch im aktuellen Projekt oder in erreichbarer origin/main-Historie; 3.508 ursprüngliche Pfade geprüft | Nur alter Checkout; niemals `.git/lfs` des aktiven Projekts anfassen. Worktree insgesamt erst nach Auflösung aller C-Dateien regulär entfernen |
| Alter Worktree: `Intermediate/`, `Binaries/`, `DerivedDataCache/`, generierter `Build/`, `Saved/Shaders/`, `Saved/ShaderDebugInfo/`, `Saved/MaterialStats/`, `Saved/UnrealBuildTool/`; darunter erkannte Cook-Ausgaben; außerdem V5/SwiftModuleCache | Compilerobjekte, PCH, erzeugte Registry-, Cook- und Shaderdateien, keine bearbeitbaren Quellen | Spätere Wiederholungen benötigen Neukompilierung. Nicht auf andere gleichnamige Ordner übertragen; FullRestore bleibt ausgenommen |
| Exakte SHA-Dubletten von Nachweisen in den zwei geprüften RawEvidence.zip-Archiven, einschließlich ihrer Mehrfachkopien im alten Saved | Jeder Archiv-Eintrag vollständig gelesen; CRC beim Lesen sowie SHA-256 gegen entpackte Originale geprüft | ZIP-Dateien erhalten; historische Skripte benötigen zum Replay erneut entpackte Eingaben am erwarteten Pfad. Diese Wiederbereitstellung wurde hier nicht ausgeführt |
| Alte Saved-Nachweise, deren identisches Gegenstück in einem erhaltenen externen Nachweisordner liegt | SHA-256 stimmt überein; Gegenstück bleibt B/C und wird nicht ebenfalls entfernt | Erhaltenes Gegenstück vor einer Bereinigung erneut prüfen; ein gleicher Dateiname genügt nicht |
| Einzelne identische Berichte, vorherige Map-/Assetstände und Metadatenkopien mit Git-Nutzdaten-Nachweis | Inhalt tatsächlich in origin/main oder dessen Historie; nicht allein wegen Versionsnummer | Keine aktive Map und keine lokale unveröffentlichte Zwischenkarte entfernen |
| `.DS_Store` in den genannten PokeMonster-Ordnern | Finder-Metadaten | Unbedeutender Speichergewinn; keine ganze Ordnerfreigabe |

### Zwei vollständig geprüfte Medienarchive

| Erhaltenes Archiv | Archivgröße Bytes | Entpackte Einträge | Geprüfte Nutzbytes | Ergebnis |
|---|---:|---:|---:|---|
| [PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/RawEvidence.zip](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/RawEvidence.zip) | 8,718,091,982 | 7,948 | 8,716,493,850 | Alle SHA-256 identisch; keine fehlenden Einträge oder CRC-Fehler |
| [PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/RawEvidence.zip](/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/RawEvidence.zip) | 2,459,603,588 | 2,182 | 2,459,102,880 | Alle SHA-256 identisch; keine fehlenden Einträge oder CRC-Fehler |

Die entpackten Verzeichnisse liegen bei TAA unter `.../Evidence/` und bei Vegetation ebenfalls unter `.../Evidence/`; unterschiedliche ZIP-Pfadpräfixe wurden ausdrücklich berücksichtigt. Andere `RawMeasurements.zip` wurden nur auf Eintragslisten untersucht, nicht vollständig als austauschbare Archive freigegeben. Sie bleiben C.

## 6. B – weiterhin erforderlich / ausdrücklich geschützt

- Vollbackup-Refs `backup/full-03492bd` und `refs/archive/pokemonster/full-backup-03492bd` samt tatsächlichen Git-/LFS-Daten im aktiven `.git`. Kein LFS-Prune, kein Branchlöschen, kein History-Rewrite.
- Gesamte vorhandene V5-Verzeichnisse `FullBackup/` und `FullRestore/`; in dieser Empfehlung kein Speichergewinn daraus angesetzt. Das gültige Bundle besitzt SHA-256 `dbbbc08cdc4b9e4729d655f2173b2ab76a231e10c740fa0929f4b1738f91bc3f`.
- Einmalige historische Prüfberichte und Wiederherstellungsanleitungen. 32 solche Markdown-Dateien außerhalb der Backup-/Checkout-Bäume sind nicht identisch in der schlanken Git-Historie nachgewiesen; zusammen nur 427.786 Bytes. Geringe Ersparnis rechtfertigt keinen Verlust der Nachvollziehbarkeit.
- Sämtliche aktiven Unreal-/Blender-/C++-/Testquellen und Originalmodelle; Hobbit Retopo V2 sowie Ranger V1/V2/V3 bleiben erhalten. Alle 95 versionierten Blenderdateien wurden bereits bei der Umstellung geöffnet; der heutige SHA-Vergleich bestätigt dieselben gespeicherten Inhalte. Heute kein neuer Blender-Öffnungstest.
- Die 38 bestehenden unversionierten Dateien im aktiven Projekt, zusammen 3,248 MiB: eine Map, 36 EnvironmentQuality-V1-Werkzeug-/Plandateien und ein Python-Cache. Auch der Cache wird wegen des ausdrücklichen Datenerhaltungsauftrags nicht hier entfernt.
- Die ausdrücklich nicht in Git aufzunehmende lokale Originaleingabe `Art/Characters/MiniHobbit/Meshy_MiniHobbit.glb`: 29.602.384 Bytes, SHA-256 `c8f39c7a7023f2c32412f33fe73dd6e1bd3a3bc45c73bc66f1218816fc9eea93`. Sie liegt im aktiven Projekt und wird nicht als GitHub-gesichert oder als Dublette freigegeben.
- Alle vorhandenen `.blend1`-Dateien und lokale Spielstände bleiben unangetastet. Keine `.blend1`-Datei als A eingestuft. Keine neue Sicherung angelegt.

### 38 erhaltene unversionierte Dateien – vollständige Pfadliste

Alle folgenden Pfade beziehen sich auf `/Users/harry/Developer/PokeMonster/`. Alle 38 Hashes stimmen mit dem Umstellungsjournal überein; keine dieser Dateien wurde auf GitHub hochgeladen oder erneut kopiert.

| Datei | Bytes |
|---|---:|
| [Content/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1.umap](/Users/harry/Developer/PokeMonster/Content/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1.umap) | 3,314,086 |
| [Tools/VisualV2EnvironmentQualityV1/AfterFoot.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/AfterFoot.py) | 575 |
| [Tools/VisualV2EnvironmentQualityV1/Analyze.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/Analyze.py) | 7,138 |
| [Tools/VisualV2EnvironmentQualityV1/ArchiveEvidence.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/ArchiveEvidence.py) | 2,983 |
| [Tools/VisualV2EnvironmentQualityV1/AuditMaps.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/AuditMaps.py) | 3,944 |
| [Tools/VisualV2EnvironmentQualityV1/CloseEditor.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/CloseEditor.py) | 523 |
| [Tools/VisualV2EnvironmentQualityV1/Compose.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/Compose.py) | 4,577 |
| [Tools/VisualV2EnvironmentQualityV1/Control.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/Control.py) | 943 |
| [Tools/VisualV2EnvironmentQualityV1/FootTest.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/FootTest.py) | 13,993 |
| [Tools/VisualV2EnvironmentQualityV1/FormatTables.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/FormatTables.py) | 2,033 |
| [Tools/VisualV2EnvironmentQualityV1/MCPClient.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/MCPClient.py) | 1,166 |
| [Tools/VisualV2EnvironmentQualityV1/Monitor.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/Monitor.py) | 1,614 |
| [Tools/VisualV2EnvironmentQualityV1/MotionReview.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/MotionReview.py) | 3,210 |
| [Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_PIE_1.tsv](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_PIE_1.tsv) | 1,747 |
| [Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_PIE_2.tsv](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_PIE_2.tsv) | 1,801 |
| [Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_PIE_3.tsv](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_PIE_3.tsv) | 1,801 |
| [Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_PIE_4.tsv](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_PIE_4.tsv) | 1,855 |
| [Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_PIE_5.tsv](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_PIE_5.tsv) | 1,801 |
| [Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_PIE_6.tsv](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_PIE_6.tsv) | 1,855 |
| [Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_Standalone_1.tsv](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_Standalone_1.tsv) | 1,761 |
| [Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_Standalone_2.tsv](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_Standalone_2.tsv) | 1,815 |
| [Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_Standalone_3.tsv](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_Standalone_3.tsv) | 1,815 |
| [Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_Standalone_4.tsv](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_Standalone_4.tsv) | 1,869 |
| [Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_Standalone_5.tsv](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_Standalone_5.tsv) | 1,815 |
| [Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_Standalone_6.tsv](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/Plans/VEQ1_Standalone_6.tsv) | 1,869 |
| [Tools/VisualV2EnvironmentQualityV1/Preset.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/Preset.py) | 1,204 |
| [Tools/VisualV2EnvironmentQualityV1/README.md](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/README.md) | 1,477 |
| [Tools/VisualV2EnvironmentQualityV1/ReviewShots.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/ReviewShots.py) | 3,041 |
| [Tools/VisualV2EnvironmentQualityV1/RunFoot.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/RunFoot.py) | 2,165 |
| [Tools/VisualV2EnvironmentQualityV1/RunMotionReview.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/RunMotionReview.py) | 970 |
| [Tools/VisualV2EnvironmentQualityV1/RunPIE.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/RunPIE.py) | 1,280 |
| [Tools/VisualV2EnvironmentQualityV1/RunReview.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/RunReview.py) | 1,279 |
| [Tools/VisualV2EnvironmentQualityV1/RunStandalone.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/RunStandalone.py) | 2,256 |
| [Tools/VisualV2EnvironmentQualityV1/StartFoot.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/StartFoot.py) | 1,681 |
| [Tools/VisualV2EnvironmentQualityV1/StartProbe.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/StartProbe.py) | 642 |
| [Tools/VisualV2EnvironmentQualityV1/Startup.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/Startup.py) | 2,215 |
| [Tools/VisualV2EnvironmentQualityV1/Summarize.py](/Users/harry/Developer/PokeMonster/Tools/VisualV2EnvironmentQualityV1/Summarize.py) | 2,776 |
| [Tools/VisualV2QualityV2/__pycache__/AuditScene.cpython-311.pyc](/Users/harry/Developer/PokeMonster/Tools/VisualV2QualityV2/__pycache__/AuditScene.cpython-311.pyc) | 5,777 |

## 7. C – unklar oder zusätzliche Prüfung erforderlich

### Sieben Unreal-Importverweise auf den alten Worktree

Eine reine Suche in den 391 zuvor erfassten AssetImportData-Quellen findet keine Quelle unter Documents/Codex. Die zusätzliche Byteprüfung aller aktiven `.uasset`/`.umap`-Pakete findet jedoch **sieben absolute alte Pfade innerhalb serialisierter `InterchangeTexture2DFactoryNode`-Kennungen**. Beide Aussagen sind miteinander vereinbar: Source-Filenames und gespeicherte Factory-Node-IDs sind verschiedene Metadaten. Die alten Dateien werden deshalb vorsichtshalber von A nach C ausgenommen.

| Unreal-Asset unter Content/Environment/ | Noch referenzierte Textur relativ zum alten Worktree | Bytes |
|---|---|---:|
| `VisualV2HealingArtV3/Textures/T_HA3_Meadow.uasset` | `Art/World/VisualV2HealingArtV3/Textures/T_HA3_Meadow.png` | 4,166,843 |
| `VisualV2HealingArtV3/Textures/T_HA3_Earth.uasset` | `Art/World/VisualV2HealingArtV3/Textures/T_HA3_Earth.png` | 2,929,551 |
| `VisualV2HealingArtV4/Textures/T_HA4_Wood.uasset` | `Art/World/VisualV2HealingArtV4/Textures/T_HA4_Wood.png` | 2,268,292 |
| `VisualV2HealingArtV4/Textures/T_HA4_Meadow.uasset` | `Art/World/VisualV2HealingArtV4/Textures/T_HA4_Meadow.png` | 3,183,900 |
| `VisualV2HealingArtV4/Textures/T_HA4_Earth.uasset` | `Art/World/VisualV2HealingArtV4/Textures/T_HA4_Earth.png` | 3,341,209 |
| `VisualV2WorldArtV5/Textures/T_WA5_ForestFloor.uasset` | `Art/World/VisualV2WorldArtV5/Textures/T_WA5_ForestFloor.png` | 3,457,494 |
| `VisualV2WorldArtV5/Textures/T_WA5_WetBank.uasset` | `Art/World/VisualV2WorldArtV5/Textures/T_WA5_WetBank.png` | 3,132,925 |

Alle sieben Texturen sind im aktiven Projekt SHA-256-identisch vorhanden und auf GitHub gesichert. Keine Runtime-Abhängigkeit vom alten Pfad nachgewiesen; die gespeicherten Factory-Kennungen sind aber ein offener Reimport-Befund. Vor Worktree-Entfernung ist gezielt zu prüfen, ob der Interchange-Reimport ausschließlich den aktuellen Quellpfad nutzt. Keine UAssets neu gespeichert oder repariert. Auch die vier bereits dokumentierten anderen relativen WestlandRegion-FBX-Importpfade nach `/Users/Shared/Art/...` bleiben ein gesonderter bestehender Befund; ihre Originale liegen im aktiven Art-Verzeichnis, nicht in Documents/Codex.

### Zwei ausschließlich lokale Blender-Zwischenstände

| Datei im alten Worktree | Bytes | SHA-256 |
|---|---:|---|
| [Saved/VisualV2HealingArtV4/GardenDetails_BeforeIvyCurl.blend](/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2HealingArtV4/GardenDetails_BeforeIvyCurl.blend) | 2,971,970 | `1e8b791a5670f11986d754ea57a1ad46ab924ba65fc64c965d422f4f7ff5de6f` |
| [Saved/VisualV2HealingArtV4/GardenDetails_BeforeIvyPlacement.blend](/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2HealingArtV4/GardenDetails_BeforeIvyPlacement.blend) | 2,971,954 | `fce63a25d8309e39b0ab2ce1dafecc04bea86a0a6c92fc6f7e405a74aaabdc59` |

Für diese beiden vorläufigen Heilhaus-Gartendetail-Dateien wurde kein identischer anderweitiger Dateibestand und kein identischer origin/main-Blob nachgewiesen. Die aktuellen Quellen sind vorhanden, beweisen aber nicht die vollständige Ersetzbarkeit dieser Zwischenstände. Keine Weiterbearbeitung oder Zusammenführung vorgenommen.

### Weitere C-Bestände

- Einmalige QHD-Bilder, Vergleichsmontagen, Videos und rohe historische Messdaten. Neu renderbare Motive ersetzen nicht die alten Messergebnisse; eine Löschung benötigt eine bewusste Entscheidung zum Verlust dieser Nachweise.
- Der Metal-Systemtrace im GPU-Bottleneck-Ordner: 2.010.731.480 Bytes; tatsächliche historische Aufzeichnung, keine für Builds erforderliche Datei, aber nicht identisch reproduzierbar. Als optionaler Diagnosebestand nur nach gesonderter Entscheidung entfernen.
- Vorhandene Archive `RawMeasurements.zip`, frühere Quarantäne-/Backupbestände der Bereinigung V2 und kleine Git-Index-/Pack-Proben. Keine automatische Aussonderung anhand der Endung.
- Weitere nicht per SHA identisch in Git oder im aktiven Projekt nachgewiesene Berichteingaben, Sitzungsmarker und Diagnose-JSONs. Die Werkzeug-/Berichtabhängigkeiten müssen bei Entfernung historischer Belege bewusst aufgegeben oder durch bereitgestellte Archivdaten erfüllt werden.

## 8. Werden die alten Ordner noch von Anwendungen benötigt?

| Anwendung / Bereich | Nachweis | Bewertung |
|---|---|---|
| Unreal-Runtime, Build und aktuelle Tests | Alle aktuellen Quellen vorhanden, Core-Prüfung bestanden, aktive Kartenpakete unverändert. Frühere Umstellung hatte Build, 49/49 Automation und drei Map Checks bestanden | Kein zusätzlicher aktiver Projektordner nötig; heute keine neuen Funktionstests ausgeführt |
| Unreal-Import | 391 zuvor erfasste Quellen lesend nachgeprüft; sieben zusätzliche alte Interchange-Kennungen in Paketen gefunden | Sieben alte Originaltexturpfade vorerst C; gezielter Reimport-Test noch offen |
| Blender | 95 gespeicherte versionierte Quellen entsprechen dem geprüften Umstellungsstand; die zwei damals korrigierten Pfade sind weiter relativ | Keine neue externe Blenderbibliothek als Abhängigkeit festgestellt; zwei lokale Saved-Quellen bleiben gesondert C |
| Rider | `lastOpenedProject` in vorhandener recentSolutions.xml zeigt `$USER_HOME$/Developer/PokeMonster/PokeMonster.uproject` | Historische Recent-Einträge sind kein aktiver Entwicklungsbedarf. Keine Rider-Konfiguration geändert |
| Laufende Anwendungen | Prozessnamenprüfung: kein Unreal-Editor, Blender oder Rider-Hauptprozess; lediglich UnrealEditorServices/JBDevice-Hilfsdienste | Kein offener Editor mit alten Map-/Quelldateien nachgewiesen; kein Programm geschlossen oder gestartet |
| Codex | Diese Unterhaltung hat weiterhin den ChatGPT-Projektspiegel als Standardordner; Projektbefehle verwenden explizit den aktiven Root | Kein neues Projektduplikat oder benötigter Sourcepfad im alten Worktree. Keine App-Einstellung verändert |
| Historische Prüf-/Reviewwerkzeuge | 349 Textfundstellen unter Tools/Docs/Config usw.; davon 53 außerhalb Docs. Viele sind Zielpfade und Dokumentationslinks, andere echte historische Eingaben | Nicht pauschal ignorieren: Entfernen führt zu fehlenden alten Nachweisen, nicht automatisch zu Runtime-Fehlern |

Konkrete Abhängigkeiten: `Tools/VisualV2QualityV2/ApplyMotionBlur.py` liest weiterhin die externe `MapBackup.json`; mehrere `ProtectionAudit.py` lesen frühere Before-/Protected-Dateien, `ComposeReview.py` historische Fotos und `BuildVideos.py` Bildfolgen/Encoder. Die erhaltenen 38 unversionierten Werkzeuge enthalten in `Tools/VisualV2EnvironmentQualityV1/Startup.py` sogar noch einen festen Assert auf den alten Worktree. Diese Dateien wurden absichtlich nicht verändert. Neue Arbeit soll diese historischen Einstiegspunkte nicht ungeprüft ausführen.

Die versionierte optionale Evidence-Pipeline verlangt alte Bilder nicht für normale Builds, kann zum Wiederholen aber ein ausdrücklich angegebenes Archiv benötigen. `FullBackup` ist damit ein bewusst erhaltener Wiederherstellungsbestand. Historische Bildlinks bleiben nur funktionsfähig, solange Dateien vorhanden sind oder gezielt aus dem geprüften Archiv wiederbereitgestellt werden. Es wurde keine vollständige Wiederholung aller historischen Reportgeneratoren behauptet.

## 9. Gesamtrechnung und empfohlene Freigabestufen

| Gruppe | Dateien | Logische GiB | Eindeutige Dateiblöcke GiB | Vorschlag |
|---|---:|---:|---:|---|
| A | 28,846 | 42,032 | 40,595 | Nach Freigabe gezielt entfernbar |
| B | 21,724 | 35,492 | 35,533 | Erhalten; kein Gewinn angesetzt |
| C | 12,277 | 28,926 | 28,957 | Vor Entscheidung weiter prüfen / bewusst über historische Nachweise entscheiden |

**Realistisch begründbarer Kandidatenumfang: 43.588.243.456 Bytes = 40,595 GiB adressierbare Dateiblöcke**, bereits ohne Doppelzählung von Hardlinks, unter der Bedingung, dass die genannten Archive und Gegenstücke erhalten bleiben. Die eigentliche physische APFS-Freigabe kann darunter liegen. Die häufige Rechnung „108 GiB alte Ordner = 108 GiB frei“ ist falsch.

1. Zuerst nach separater Freigabe nur regenerierbare Ausgaben und gesicherte alte Checkout-Dateien behandeln: rund **11,503 GiB**. Sieben Texturen, alle C-Nachweise und der registrierte Worktree selbst bleiben vorerst erhalten.
2. Danach bestätigte Mehrfachkopien behandeln: zusätzlich rund **29,092 GiB**. ZIPs und festgelegte Gegenstücke behalten; vor der Umsetzung nochmals SHA und jeweilige Abhängigkeit prüfen. Eine spätere historische Review kann gezieltes Entpacken verlangen.
3. Über die rund **28,957 GiB** C-Dateiblöcke separat entscheiden. Hieraus wird aktuell **kein** zusätzlicher Speichergewinn zugesagt. Keine vollständigen alten Versionsordner löschen, solange C oder B darin liegt.
4. Erst nach geklärten sieben Importkennungen, gesicherten lokalen Blender-Zwischenständen und bewusster Entscheidung über die verbleibenden lokalen Nachweise wäre eine reguläre Entfernung des registrierten alten Worktrees zu empfehlen. Das aktive `.git/worktrees/Worktree` nicht manuell löschen. Keine solche Aktion in diesem Auftrag.
5. FullBackup, FullRestore, Backup-Branch/Archiv-Ref und alle aktiven Git-/LFS-Daten bleiben vollständig erhalten. Keine neue externe Sicherung angelegt.

## 10. Abschlussstatus und Stopp

Aktiver HEAD und direkt abgefragtes origin/main bleiben `427d93f92765b2e03d8dca186fbc6bfbd86c8605`. Zwei registrierte Worktrees, keine Branches/Refs entfernt oder verändert. Alter Worktree unverändert. Alle 38 bestehenden unversionierten Dateien bleiben erhalten; zusätzlich entsteht ausschließlich `Docs/ALTE_ARBEITSORDNER_AUFRAEUMEN_V1_PRUEFBERICHT.md` als neue unversionierte Berichtsdatei. Kein Commit und kein Push dieses Analyseauftrags.

Abschließende vollständige Metadatenkontrolle vor dem Schreiben dieses Berichts: **143.689 bereits vorhandene Dateien**, keine fehlt, keine Dateigröße oder Änderungszeit verändert, keine Datei hinzugekommen. Die einzige anschließende Dateierstellung ist dieser Bericht.

Kein Löschen, Verschieben, Umbenennen, Überschreiben vorhandener Projektdateien, Worktree-Entfernen, Reset, Restore, Clean, Prune oder Force-Push. Rohinventur, Dateihashes und Archivprüfungen wurden nur vorübergehend unter `/tmp/pokemonster_*` abgelegt, keine Nutzdaten gesichert oder dupliziert. Diese temporären Prüfmetadaten sind kein dauerhafter Ersatz für eine erneute Prüfung unmittelbar vor einer freigegebenen Bereinigung.

**Es wird auf Harrys ausdrückliche Bereinigungsfreigabe gewartet. Dieser Bericht genehmigt keine Dateiänderung.**
