# PokeMonster – Speicherbereinigung V2: endgültige Löschliste zur Freigabe

Stand: 19.10.2026, 19:37 CEST. **Nur Vorbereitung. Nichts gelöscht, verschoben oder bereinigt.**

**Vorgeschlagen werden ausschließlich 21.758 einzeln aufgelistete Dateien außerhalb des aktiven Projekts.** Die 28.846 früheren A-Kandidaten wurden vollständig erneut gelesen und gehasht. Keine Abweichung zu den vorhandenen V1-Hashes oder Dateigrößen/Änderungszeiten; bei den in V1 nur strukturell geprüften erzeugbaren Dateien liegen jetzt ebenfalls SHA-256-Werte vor. **7.088 ursprüngliche A-Dateien sind ausdrücklich zurückgestellt.**

Die strengere Auswahl umfasst **32,907 GiB eindeutig gezählte Dateiblöcke**. Die unmittelbar vom macOS-Dateisystem gemeldeten exklusiven Bytes betragen **29,309 GiB**. Für die Freigabe ist daher rund **29,3 GiB** eine belastbarere momentane Schätzung als die bisher genannten 40,6 GiB. Weitere gemeinsam genutzte Blöcke werden nicht als sichere sofortige Ersparnis zugesagt.

## 1. Verbindliche Dateilisten

| Datei | Inhalt | SHA-256 |
|---|---|---|
| [SPEICHERBEREINIGUNG_V2_LOESCHLISTE.csv](/Users/harry/Developer/PokeMonster/Docs/SPEICHERBEREINIGUNG_V2_LOESCHLISTE.csv) | 21.758 vollständige Pfade mit Größen, Hashes, Inodes, Hardlinks, APFS-Werten und konkretem Erhaltungsnachweis | `08af12d606100603fff64ba13b8f55c100c0fbdfc21349717f3b4db69420df79` |
| [SPEICHERBEREINIGUNG_V2_LOESCHLISTE.txt](/Users/harry/Developer/PokeMonster/Docs/SPEICHERBEREINIGUNG_V2_LOESCHLISTE.txt) | Dieselben 21.758 vollständigen Pfade, genau ein Dateipfad pro Zeile; keine Wildcards, keine Löschbefehle | `92bae11aa4963b43145e5f2f91ee88377041d3f175d992c676f663d88a1a09b3` |
| [SPEICHERBEREINIGUNG_V2_ZURUECKGESTELLT.csv](/Users/harry/Developer/PokeMonster/Docs/SPEICHERBEREINIGUNG_V2_ZURUECKGESTELLT.csv) | 7.088 frühere A-Dateien, die NICHT gelöscht werden sollen, mit Begründung | `1c239880eb403534559e77e45fffff811048c279657866163e9eb26bb6bb484a` |

**Nur die positiven CSV-/TXT-Listen bilden den Freigabeumfang.** Die Ausnahmeliste ist keine zweite Löschliste. Ordnernamen in diesem Bericht sind Zusammenfassungen und ausdrücklich keine rekursiven Löschziele. Selbst ein heute vollständig ausgewählter Cacheordner soll nur anhand seiner aufgeführten Dateien behandelt werden; keine zukünftigen/neuen Dateien sind mit umfasst.

Eine spätere Freigabe muss sich auf diese konkrete Liste beziehen. Unmittelbar vor einer tatsächlichen Entfernung sind Dateihashes, Pfadauflösung, Identitäten, Schutzmengen und erhaltene Gegenstücke erneut abzugleichen. Bei Abweichungen stoppen; die heutige Prüfung ist keine unbegrenzt gültige Erlaubnis. Ein Wegzug in den Papierkorb würde noch keinen freien Speicher garantieren. Keine Löschroutine vorbereitet oder ausgeführt.

## 2. Ausgangsstand und Schutzprüfung

- Vollständige Grundlage gelesen: `Docs/ALTE_ARBEITSORDNER_AUFRAEUMEN_V1_PRUEFBERICHT.md`, SHA-256 `e662bce5f8c053ca1b46bca481a2e35ff9ef63b9bd55596d40dcf8c9bd72e678`; AGENTS.md beachtet.
- Aktiver Root ausschließlich `/Users/harry/Developer/PokeMonster`. HEAD und direkt mit `ls-remote` geprüfter origin/main: `427d93f92765b2e03d8dca186fbc6bfbd86c8605`. Kein Pull, Push, Staging oder Commit.
- Alter registrierter Worktree: `.../PokeMonster_GitSicherung_V5_2026-10-16/Worktree`, HEAD `30a165b034114ba4b0940a369e73143db988afad`, sauber. Sein **gesamter versionierter Checkout bleibt erhalten**, statt durch Einzeldateientfernung künstlich beschädigt zu werden. Dies ist eine bewusst strengere Auswahl gegenüber V1.
- `backup/full-03492bd` und `refs/archive/pokemonster/full-backup-03492bd` unverändert auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`; `FullBackup/`, `FullRestore/`, Git-Bundle, Git-/LFS-Objekte, Branches und Worktree-Verwaltung vollständig ausgeschlossen.
- Sämtliche V1-B-/C-Dateien ausgeschlossen, auch wenn sich später eine Dublette vermuten ließe. Die sieben alten Interchange-Importpfade und beide lokalen Blender-Unikate bleiben erhalten.
- Sämtliche aktiven Quellen und unversionierten Projektdateien ausgeschlossen: alle 38 gesondert erhaltenen Dateien erneut SHA-256-identisch zum Umstellungsjournal. Auch die lokale MiniHobbit-Originaleingabe, `.blend1`, Original-GLBs und bestehenden Karten bleiben unangetastet.
- Alle nicht eindeutig generierten Projekt-/Autoren-/Konfigurations-/Prüfdateien vorsorglich aus der positiven Liste herausgenommen. Insbesondere keine externen `.blend`, `.fbx`, `.uasset`, `.umap`, Skripte, Berichte oder Spielstände zur Löschung vorgeschlagen. Einzig **reproduzierbare Cook-Ausgaben** können erzeugte UAssets enthalten; diese sind keine Original-/Editorassets und liegen ausschließlich in expliziten alten Cook-Ausgabeordnern.

### Noch laufende Zugriffe

Lesende Kontrolle geöffneter Dateien mit `lsof`: Während der eigenen Hashprüfung wurden nur zwei durch den eigenen Prüfprozess geöffnete Bilddateien gemeldet. Nach Abschluss der Prüfung keine offenen Dateien unter `/Users/harry/Documents/Codex` mehr festgestellt. Kein Programm gestartet, geschlossen oder beendet. Das ersetzt keine erneute Zugriffskontrolle bei einer späteren Freigabe.

## 3. Tatsächliche erneute Prüfung

| Prüfung | Ergebnis |
|---|---|
| Frühere A-Dateien | 28.846/28.846 frisch per SHA-256 gelesen; keine Abweichungen |
| Zusätzliche Gegenstücke und Schutzbestände | Insgesamt 65.876 Datei-Hashes / rund 109,81 GiB gelesene Inhalte; keine Nutzdaten kopiert |
| Aktuelle Inventur | 143.690 reguläre Dateien in Altbestand und aktivem Projekt; vollständige Geräte-/Inode-/Hardlink-Erfassung |
| APFS-Abfrage | 141.907 eindeutige Inodes per dokumentiertem macOS-getattrlist geprüft; kein Abfragefehler |
| Pfadsicherheit | Keine Symlinks gefunden; positive Pfade auf erlaubten Altbereich beschränkt; aktiver Root und Git-/IDE-Verwaltungsdateien ausgeschlossen |
| Dublettennachweise | Jedes ausgewählte Reviewbild stimmt per SHA-256 mit einem ausdrücklich erhaltenen Original oder einem geprüften ZIP-Eintrag überein |
| Archivschutz | Beide RawEvidence.zip erneut vollständig gehasht, byteidentisch zu den in V1 vollständig CRC-/Eintrag-SHA-geprüften Archiven; Archive nicht in der Löschliste |
| Schutz der Gegenstücke | Kein erforderliches erhaltenes Gegenstück ist selbst Teil der endgültigen Liste; keine zirkuläre Doppel-Löschung |
| Werkzeug-/Berichtreferenzen | Exakte vorhandene absolute Pfade und statisch auflösbare Python-Lesezugriffe geprüft; gefundene direkte Abhängigkeiten zurückgestellt |
| Historische Reviewdaten | Metadaten/CSV/JSON/HTML/Logs und Spielstände auch bei Dubletten vorsorglich erhalten |
| Build/Gameplay | Kein neuer Build, Editor-, Automation- oder Gameplay-Lauf: reine lesende Dateiprüfung, keine funktionalen Änderungen |

Archiv-Erhaltungsnachweis: Ein unveränderter SHA-256 des gesamten ZIP und der erneut identische SHA-256 der Kandidatendatei bewahren den in V1 verifizierten Zuordnungsnachweis zum ZIP-Eintrag. Es wurde nicht unnötig ein zweites entpacktes Archiv erzeugt. Bereits vorhandene Archivtabellen enthalten bei TAA 7.948 und bei Vegetation 2.182 geprüfte Einträge. Die positive CSV nennt für jedes betroffene Bild den konkreten Archivpfad und Eintragsnamen.

Eine automatische vollständige Interpretation beliebiger Pythonprogramme/JSON-generierter Dateipfade wird nicht behauptet. Deshalb bleiben ausführbare Quellen, Metadaten, unbekannte Dateitypen und der vollständige registrierte Checkout außen vor. Ausgewählte Bilder sind bekannte optionale Reviewkopien mit erhaltenem Inhalt, keine benötigten Laufzeittexturen. Historische Bildfolgen müssen für ein erneutes Review gegebenenfalls aus dem erhaltenen Archiv wiederbereitgestellt werden. Diese bekannte Wiederbereitstellung ist dokumentiert; keine unbekannte Quellabhängigkeit wird stillschweigend als gelöst behandelt.

## 4. Konkrete Ordnergruppen der positiven Liste

Die vollständigen Einzelfile-Pfade stehen in CSV und TXT. Folgende Tabelle fasst sie nach tatsächlichen Wurzeln zusammen. Hardlinkblöcke werden genau einer lexikographisch ersten Datei zugerechnet; die Summen sind dadurch addierbar.

| Ordnergruppe, KEIN rekursives Löschziel | Dateien | Logisch GiB | Blöcke einmalig GiB | APFS exklusiv einmalig GiB |
|---|---:|---:|---:|---:|
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/SwiftModuleCache` | 91 | 0,060 | 0,061 | 0,061 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Binaries/Mac` | 3 | 0,004 | 0,004 | 0,001 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Build/Mac` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/DerivedDataCache/VT` | 5 | 0,002 | 0,002 | 0,002 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Intermediate/Build` | 496 | 2,819 | 2,820 | 2,662 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Intermediate/CachedAssetRegistry` | 2 | 0,133 | 0,133 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Intermediate/PipInstall` | 4 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Intermediate/ReimportCache` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Intermediate/ShaderAutogen` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Intermediate/TargetInfo.json` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/.DS_Store` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/MaterialStats` | 2 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/ShaderDebugInfo` | 37 | 0,008 | 0,008 | 0,006 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/Shaders` | 8 | 0,343 | 0,343 | 0,343 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/UnrealBuildTool` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2AASoftShadowsV1` | 753 | 5,238 | 5,239 | 5,239 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2EnvironmentQualityV1` | 125 | 0,724 | 0,724 | 0,724 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2GPUBottleneckV1` | 28 | 0,197 | 0,197 | 0,197 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2HealingArtV3` | 10 | 0,068 | 0,068 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2MaterialFixV1` | 123 | 1,199 | 1,199 | 1,199 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2QualityV2` | 280 | 1,217 | 1,217 | 1,217 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2TAAIntegrationV1` | 9,786 | 9,928 | 8,914 | 8,718 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2VegetationPerfV1` | 922 | 1,601 | 1,140 | 0,111 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2WorldArtQualityV1` | 66 | 0,273 | 0,273 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2WorldArtV5` | 32 | 0,225 | 0,225 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree/Saved/VisualV2WorldArtV6` | 40 | 0,284 | 0,284 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V7_2026-10-17` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_ShadowQuality_V8_2026-10-19` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_VisualV2_EnvironmentQualityV1_2026-10-17` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V3_2026-10-19` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_VisualV2_QualityV2_2026-10-17` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/Evidence` | 7,397 | 7,940 | 7,954 | 7,954 |
| `/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/Evidence` | 1,524 | 2,097 | 2,100 | 0,875 |
| `/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V1_2026-10-19` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V2_2026-10-19` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V5_2026-10-19` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V6_2026-10-19` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V7_2026-10-19` | 1 | 0,000 | 0,000 | 0,000 |
| `/Users/harry/Documents/Codex/Projektbereinigung_PokeMonster_V2_2026-10-16` | 1 | 0,000 | 0,000 | 0,000 |

### Art der ausgewählten Dateien

| Auswahl | Dateien | Voraussetzung |
|---|---:|---|
| Reproduzierbare Build-/Cook-/Shader-/Modulcache-Ausgaben | 717 | Nur bestehende eindeutig generierte Altdateien; Quell-/Editorbestände bleiben erhalten |
| SHA-identische optionale Reviewbilder in erhaltenen ZIPs | 19,628 | Beide ZIPs unverändert behalten; Archiv-/Eintragshashes in CSV |
| SHA-identische Reviewbilder mit erhaltenem separatem Gegenstück | 1,393 | Benanntes Gegenstück bleibt außerhalb der Löschmenge |
| Finder-Metadaten | 20 | Ausschließlich die einzeln gelisteten .DS_Store-Dateien |

Keine Ordnerlöschungen und kein Entfernen registrierter Worktrees vorgeschlagen. Nach späterer Einzeldateientfernung wären einige Cache-/Evidence-Ordner leer; auch daraus entsteht keine vorweggenommene Erlaubnis für eine pauschale Parent-Entfernung.

## 5. Zurückgestellte A-Kandidaten und vollständige Ausschlüsse

| Zusätzlicher Ausschluss gegenüber V1 | Dateien |
|---|---:|
| Lokale Projekt-/Autoren-/Prüfquelldatei oder bestehende Map; vorsorglich erhalten | 18 |
| Exakter Pfad wird von aktivem Werkzeug oder Bericht noch referenziert | 18 |
| Registrierten alten Git-Checkout vollständig erhalten; kein künstlich unvollständiger Worktree | 3,500 |
| Git-/IDE-/Codex-Verwaltungsdatei | 1 |
| Gegenstück ebenfalls Löschkandidat; nicht transitiv freigeben | 1 |
| Prüf-/Sitzungsmetadaten, Spielstand oder sonstige Projektdatei; konservativ erhalten | 3,550 |

Inhaltlich betrifft dies den gesamten alten versionierten Checkout, vorhandene historische Karten-/Assetkopien, Berichte, JSON/CSV/Log-/Sitzungsdateien und 22 frühere `.sav`-Testdateien. Auch ein leerer MP4-Zwischenstand bleibt vorsorglich außerhalb der Freigabe. Zusammen 7.088 Dateien aus dem früheren A-Vorschlag. Sie werden nicht automatisch zu B/C umklassifiziert; für diesen Auftrag sind sie schlicht **nicht freigegeben**. Die ursprünglichen B-/C-Gruppen sind zusätzlich vollständig ausgeschlossen.

Die Ausnahmedatei führt jede zurückgestellte Datei mit vollständigem Pfad auf. Direkte Referenzen wie `Evidence/Summary.json`, `Photos.json`, `Validation.json`, `Measurements.json` und `MapChangeAudit.json` bleiben erhalten. Sieben Texturen mit alten Interchange-Factory-Kennungen und beide `GardenDetails_BeforeIvy*.blend` waren bereits C und sind weder in der positiven Liste noch als neuer A-Kandidat aufgenommen.

## 6. Hardlinks, APFS-Klone und erwartete Ersparnis

| Größe | Bytes | GiB | Bedeutung |
|---|---:|---:|---|
| Dateilängen | 36,894,790,837 | 34,361 | Kein verlässlicher Maßstab für frei werdenden Speicher |
| Alle Namenseinträge nominell | 36,938,854,400 | 34,402 | Enthält Mehrfachzählung von Hardlinks |
| Dateiblöcke nach Hardlink-Abzug | 35,334,119,424 | 32,907 | Oberer dateibezogener Umfang, noch mit möglicher APFS-Teilung |
| Aktuell exklusive APFS-Bytes | 31,470,190,592 | 29,309 | Vom Kernel gemeldeter unmittelbar freigebbarer Datenanteil bei Entfernung aller ausgewählten Namen |

21.758 Pfade entsprechen **19,975 Inodes**. 1,783 zusätzliche Hardlink-Namen werden nicht doppelt gerechnet. Für jeden ausgewählten Inode wurden alle vorhandenen Linknamen erfasst und liegen ebenfalls in der positiven Liste; keine Hardlinkalias-Datei einer Schutzgruppe betroffen. Der Hardlink-Abzug beträgt 1,495 GiB.

Bei **930 ausgewählten Inodes** meldet macOS `EF_MAY_SHARE_BLOCKS`. Keine gleichlautenden Clone-ID-Gruppen über verschiedene Inodes im erfassten Bestand gefunden; das schließt teilweise gemeinsame Extents oder Snapshots ausdrücklich nicht aus. Diese werden über `ATTR_CMNEXT_PRIVATESIZE` berücksichtigt. Gegenüber den eindeutigen Dateiblöcken werden 3,599 GiB deshalb nicht als sichere sofortige Ersparnis angesetzt.

Die Abfrage benutzt ausschließlich lesendes `getattrlist` mit `ATTR_CMN_RETURNED_ATTRS`, `FSOPT_ATTR_CMN_EXTENDED`, `ATTR_CMNEXT_PRIVATESIZE`, `ATTR_CMNEXT_CLONEID` und `ATTR_CMNEXT_EXT_FLAGS`, nach lokalem SDK-Header und macOS-Manpage. Die lokale Manpage definiert PrivateSize als Bytes, die nicht in Klonen oder Snapshots gebunden sind und beim Entfernen unmittelbar frei würden. Kein Clone, Testfile, Snapshot oder Backup erstellt; keine Dateisystemstruktur für die Prüfung manipuliert. `diskutil info` war in der eingeschränkten Umgebung nicht nutzbar; die direkte Kernelabfrage war für alle Inodes erfolgreich.

**Erwartungswert zur Freigabe: momentan rund 29,3 GiB Datenblöcke.** Zusätzlich frei werdende gemeinsame Blöcke und Verzeichnismetadaten sind nicht eingerechnet. Zwischen Prüfung und tatsächlicher Bereinigung können neue Snapshots, offene Dateien oder andere Änderungen diese Zahl beeinflussen. Eine garantierte spätere Zunahme des freien Volume-Speichers wird nicht behauptet.

## 7. Bedingungen einer späteren Ausführung

1. Ausdrückliche Freigabe der hier verlinkten positiven Liste; keine Freigabe alter pauschaler 40,6-GiB-Schätzungen oder ganzer Verzeichnisse unterstellen.
2. Genau dieselben CSV-/TXT-Prüfsummen prüfen, jeden Eintrag erneut gegen gespeicherten SHA-256, Dateityp, Geräte-/Inodekennung und sichere Pfadauflösung kontrollieren. Neue oder geänderte Dateien ausschließen, nicht improvisieren.
3. Archive und einzeln benannte Gegenstücke bleiben erhalten und müssen erneut stimmen. Weder aktives Projekt noch B/C, lokale Quellen/Spielstände, Git-Administration, FullBackup oder FullRestore berühren.
4. Aktuelle Zugriffe, Schutzflags, Hardlinks und exklusive APFS-Bytes erneut lesen. Bei Abweichungen oder nicht verifizierbarem Erhaltungsnachweis stoppen.
5. Keine Worktree-/Branchentfernung, kein git clean/reset/restore/prune, kein History-Rewrite und kein Force-Push. Keine zusätzliche Projektkopie oder Sicherung. Eine Ausführung ist in diesem Auftrag nicht enthalten.

## 8. Abschluss

Abschlusskontrolle vor der Berichtserstellung: Alle 143.690 erfassten Bestandsdateien haben unveränderte Größen, Änderungszeiten, Inodes und Hardlinkzahlen. Keine Überschneidung der positiven Liste mit B/C oder dem aktiven Projekt. Alle ursprünglichen 38 unversionierten Dateien erhalten.

Nur vier neue Prüf-/Listendateien unter `/Users/harry/Developer/PokeMonster/Docs/` vorgesehen. Sie enthalten Dateinamen und Prüfdaten, keine zusätzlichen Kopien der Nutzdaten. Bestehende Dateien bleiben unverändert; kein Commit/Push und keine Git-Historienänderung. Build- und Gameplaytests wurden für diesen rein lesenden Auftrag nicht neu durchgeführt. Vorhandene unversionierte Dateien und Vollbackup erhalten.

**Stopp: Die endgültige Liste liegt zur ausdrücklichen Freigabe vor. Es wurde noch nichts gelöscht.**
