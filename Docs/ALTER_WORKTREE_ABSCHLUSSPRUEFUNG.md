# Alter Worktree – abschließende Abhängigkeitsprüfung und Erhaltungsplan

Stand: 19.10.2026, 20:31 CEST.

**Empfehlung:** Die technische Bindung an den alten Worktree ist geklärt. Nach ausdrücklicher Freigabe zuerst die konkret ausgewählten **6.655 A-Dateien / 1,542 GiB** in den aktiven Bestand übernehmen, danach kann der alte Worktree ordnungsgemäß über Git entfernt werden. **Jetzt nichts verschoben, gelöscht oder überschrieben; kein Worktree entfernt.** Keine zusätzlichen Projekt-/Versionsordner oder Backups angelegt. Keine Assets, Maps, freigegebenen Materialien, Gameplaydateien oder Git-Refs geändert; kein Staging, Commit oder Push.

Ein normaler Reimport würde bei den sieben Texturen allerdings Kompression und Mip-Einstellungen verändern. Das ist unabhängig vom Speicherort und wurde ausschließlich an flüchtigen Kopien nachgewiesen. **Keine automatische Freigabe eines Reimports der Originalassets.** Für die Entfernung des alten Worktrees ist kein solcher Reimport nötig.

## 1. Verbindliche Grundlagen

- Aktives Projekt: `/Users/harry/Developer/PokeMonster`, `.uproject` direkt darin.
- Alter Worktree: `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree`.
- Geprüfter aktiver Stand und direkt bestätigtes GitHub-`origin/main`: `427d93f92765b2e03d8dca186fbc6bfbd86c8605`.
- Alter Checkout: `30a165b034114ba4b0940a369e73143db988afad`, Branch `codex/slim-backup-v5`, vollständig in der schlanken Main-Historie enthalten.
- Vollbackup: `03492bd96b4dba44692f675c19d5f11abfa86b4b`; beide Schutzrefs unverändert, kein Vorfahr des schlanken Main.
- Gelesen: `AGENTS.md`, relevante Abschnitte von `TECHNIK.md`/`ENTSCHEIDUNGEN.md`, `ALTER_WORKTREE_ENTFERNUNG_PRUEFBERICHT.md`, Dateiinventar und Bereinigungsbericht V3. Keine visuelle Umgestaltung; Grafikstil unverändert.

Das neue CSV bewertet **ausschließlich die jeweilige Kopie im alten Worktree**. „B“ bei einer alten Blender-, Unreal- oder C++-Datei bedeutet niemals, ihre benötigte aktive Originaldatei oder ihre Git-/LFS-Sicherung zu entfernen.

## 2. Blender-Zwischenstände: inhaltlich ersetzt

| Alter Stand unter `Saved/VisualV2HealingArtV4/` | Bytes | Befund |
|---|---:|---|
| `GardenDetails_BeforeIvyPlacement.blend` | 2.971.954 | Vor der Korrektur von Efeuposition und Blattneigung |
| `GardenDetails_BeforeIvyCurl.blend` | 2.971.970 | Position bereits korrigiert, Blattneigung noch nicht korrigiert |

Aktuelle Vergleichsquelle: `/Users/harry/Developer/PokeMonster/Art/World/VisualV2HealingArtV4/Source/HealingHouse_GardenDetails_V4.blend`.

Drei Dateien mit Blender 5.2.2 schreibfrei geöffnet und verglichen: alle vorhandenen Objekte/Mesh-Datenblöcke, Vertexkoordinaten, Flächenindizes, Materialzuordnungen/-graphen, UV-/Farbattribute, Transformationen, Modifier, Vertexgruppen und gepackte Bilddaten. Beide alten Stände besitzen dieselben sechs Meshobjekte wie die aktuelle Quelle. **Keine nur dort vorhandenen Meshes, Materialien oder Texturen.** Keine Shape Keys, Armaturen, Kurven oder Animationen in den Zwischenständen.

`HA4_Flagstone`, `HA4_GardenFlowers`, `HA4_GardenHerb` und `HA4_GrassTuft` sind vollständig gleich in den geprüften Geometrie-/Materialdaten. Nur die Positionen der Vertices von `HA4_IvySprigA/B` unterscheiden sich; Topologie, UVs, Farben, Materialgraphen und Objekttransformationen bleiben gleich.

| Vergleich | Geänderte Vertices pro Efeuobjekt | Maximaler lokaler Abstand zur heutigen Form |
|---|---:|---:|
| Vor Placement → aktuell | 189 von 189 | 0,927500 m |
| Vor Curl → aktuell | 162 von 189 | 0,427500 m |

Das sind Abstände im lokalen Authoring-Mesh, nicht zusätzliche Weltmaße an der skalierten Fassade.

Die versionierten Skripte erklären den Unterschied vollständig:

- `Tools/VisualV2HealingArtV4/FixIvyPlacement.py`: lokale X-Verschiebung um −0,50 m; vorhandene Flächenorientierung kontrollieren.
- `Tools/VisualV2HealingArtV4/CurlIvy.py`: zusätzliche X-Korrektur `(UV.y − 0,5) × 0,95`.

Die Formeln wurden **nur im Speicher berechnet**, ohne die Skripte mit ihren Speicher-/Export-/Backup-Schritten auszuführen. Ergebnis für beide Efeuobjekte und beide Zwischenstände: **alle 189 Vertexpositionen float32-exakt identisch zum aktuellen Stand; Restfehler 0,0 m**. Gepackte Textur und Materialgraphen sind identisch. Die Quelldateien blieben SHA-256-unverändert.

**Empfehlung:** Beide Zwischenstände in **B** einordnen, keine Übernahme ins aktive Projekt erforderlich. Erhalten bleiben die aktuelle Garden-Quelle, PottedPlants-Quelle, Exporte und die beiden Korrekturskripte. Die alten Dateihashes sind verschieden; die historischen Blender-UI-/Dateimetadaten werden nicht als bytegenau reproduzierbar ausgegeben. Es gehen aber keine nachgewiesenen benötigten Form-/Materialvarianten verloren.

## 3. Historische Entwicklungsnachweise

Untersucht wurde der zuvor nicht anderweitig belegte Bestand: **8.273 Nachweisdateien / 6.350.870.213 Bytes**, zusätzlich die zwei Blenderdateien. Alle 14.277 verbliebenen Worktree-Dateien wurden erneut SHA-256-geprüft; keine Änderung zum vorherigen Inventar. 359 bislang einzigartige JSON-Dateien vollständig einschließlich UTF-8-BOM/UTF-16 dekodiert, keine beschädigte JSON-Datei. CSV-Inhaltsgruppen anhand ihrer tatsächlichen Kopfzeilen sowie Herkunft/Tools eingeordnet; vollständige Dateihashes geprüft. Keine neue FPS-Messung und kein neuer Performancevergleich.

### A – gezielt erhalten

| Gruppe ohne identische Mehrfachkopien | Dateien | Logische GiB | Warum erhalten? |
| Historische Mess-/Pruefdaten | 6.566 | 0,987 | Originale Messungen, Einstellungs- und Schutzinventare, Build-/Automation-/Gameplaynachweise; damaliger Zustand nicht exakt neu erzeugbar |
| Historischer Save-Testnachweis | 8 | 0,000 | Acht vorhandene GVAS-Testresultate, ausdrücklich keine aktiven Dev-Spielstände |
| Ausgewaehlte visuelle Schluesselnachweise | 81 | 0,556 | Begrenzte QHD-Vorher-/Nachher- und Schatten-A/B/C-Serien statt aller Kontrollmedien |

In A enthalten: 2.952 CSV-, 3.223 Log-, 256 JSON-, 9 JSONL-, 121 TXT- und 5 TSV-Dateien, acht Save-Testdateien sowie 81 PNG-Schlüsselbilder. Dies ist eine konservative Empfehlung zur Nachvollziehbarkeit der bisherigen Arbeit, keine Behauptung, dass diese Rohdaten für das Spiel oder jeden Build benötigt werden. Auch fehlgeschlagene oder eingeschränkt aussagekräftige alte Läufe werden nicht durch Entfernen ihrer Daten unsichtbar gemacht.

Beispiele der zu erhaltenden Dateien, jeweils relativ zum alten Worktree; **jede konkrete Datei und ihr vorgesehenes Ziel stehen im CSV**:

- `Saved/EnvironmentPerfV2/*_Frames.csv`, `*_Segments.csv`, `*_Settings.txt` und zugehörige ursprüngliche `Saved/Profiling/CSV/`-/GPU-Ausgaben.
- `Saved/VisualV2WorldArtQualityV2/Measurements.json`, `Saved/VisualV2HealingArtV4/CompleteAutomation/Report/index.json`, `Acceptance/FinalFootrun/FootTest.json` und die jeweiligen Build-/Map-Check-/Schutzinventare. Inhaltsgleiche Kopien werden nur einmal erhalten; die Aliaszuordnung steht im CSV.
- Acht `DevSaveTestResult.sav` unter den dokumentierten Test-/Acceptance-Pfaden. Alle besitzen gültigen GVAS-Header. Der originale aktuelle `Saved/SaveGames/PokeMonster_Dev.sav` bleibt davon getrennt und unverändert.

Wichtige lesbare Prüfberichte und verbindliche Entwicklungsentscheidungen liegen bereits unter dem aktiven `Docs/` und in Git. Es befindet sich kein nur hier versteckter neuer Markdown-Prüfbericht in den 5,915 GiB. Kein neuer Import-/Modellquelltyp wurde zwischen den Kontrollaufnahmen gefunden. Benötigte Originalreferenzen und Spieltexturen unter aktivem `Art/` und `Content/` bleiben geschützt.

### Bewusst kleine visuelle Aufbewahrung

Jeweils die vorhandenen Bilder dieser expliziten `Photos/`-Serien in A erhalten:

| Saved-Bereich | Serien |
| `VisualV2WorldArtQualityV2` | `PIE_Q2_V1_2560_1440`, `PIE_Q2_V2_2560_1440` |
| `VisualV2HealingArtV3` | `PIE_Q1_AfterFinal_2560_1440`, `PIE_Q1_Before_2560_1440` |
| `VisualV2HealingArtV4` | `PIE_Q2_AfterFinal_2560_1440`, `PIE_Q2_Before_2560_1440` |
| `VisualV2WorldArtV5` | `PIE_Q2_Before_2560_1440`, `PIE_Q2_Candidate_2560_1440` |
| `VisualV2WorldArtV6` | `PIE_Q1_Candidate_2560_1440`, `PIE_Q2_BeforeFinal_2560_1440` |
| `VisualV2WorldArtV7` | `PIE_Q1_ArtOnly_2560_1440`, `PIE_Q1_BeforeFinal_2560_1440` |
| `VisualV2ShadowQualityV8` | `PIE_A`, `PIE_B`, `PIE_C` |

Diese Auswahl enthält vorhandene Vorher-/Nachher-, Zwischenkandidaten- und A/B/C-Aufnahmen mit ihren **ursprünglichen Bezeichnungen**. „Candidate“ ist keine nachträgliche Art-Freigabe. Keine fehlende Endansicht erfunden. Andere bereits extern gesicherte Endansichten bleiben am vorhandenen Gegenstück erhalten; das CSV nennt diese Gegenstücke. Die 81 Bilder beanspruchen insgesamt 596.788.640 Bytes.

### B – nach Freigabe entbehrlich

| Gruppe | Dateien | Bytes | Begründung |
| Gesicherte alte Kopie | 6.001 | 7.804.005.124 | Nutzdaten in aktiver Quelle, Git-/LFS-Historie oder bestehendem externem Gegenstück erhalten |
| Optionale Kontrollmedien | 1.374 | 4.646.778.746 | Nicht benötigte zusätzliche Spielkamera-/Acceptance-Aufnahmen und Reviewframes; wichtige Auswahl separat A |
| Intern identischer Nachweis | 169 | 47.591.981 | Identischer SHA-256 zu einer ausdrücklich in A erhaltenen Datei |
| Ersetzter Blender-Zwischenstand | 2 | 5.943.924 | Durch heutigen Stand und geprüfte Korrekturformeln ersetzt |
| Reproduzierbares Werkzeugbinary | 2 | 195.688 | EncodeRecording/VerifyVideo aus vorhandenen versionierten Swift-Quellen erzeugbar |
| Reproduzierbarer Actor-Probeexport | 1 | 927 | ActorProbe.t3d enthält nur AbstractNavData-Default/Standard-SceneComponent |
| Veraltete Steuer-/Warteschlangenmetadaten | 67 | 7.065 | Abgearbeitete Request/Job/Ack/Port-Dateien, keine Messergebnisse |
| Lokaler Editorzustand | 5 | 141.648 | Editoransicht, Konsole und SourceControl-Pfadliste; keine Projektquelldaten |
| Worktree-Verweis | 1 | 67 | Nur durch autorisiertes git worktree remove behandeln, niemals gemeinsame .git löschen |

Im alten Worktree sind **keine MP4-/MOV-Dateien mehr vorhanden**. Es verbleiben unter anderem 577 JPEG-Frames aus zwei früheren Tür-/Gameplay-Reviewsequenzen (154.327.695 Bytes), keine Animationstexturen oder Spielsprites. Diese können als optionale Nachweise entfallen. Die Frameaufnahme selbst ist nicht exakt neu erzeugbar; nur das Encoding ist reproduzierbar. Die zwei erzeugbaren Swift-Binaries bleiben durch `Tools/VisualV2TAAIntegrationV1/EncodeRecording.swift` und `Tools/VisualV2VegetationPerfV1/VerifyVideo.swift` nachvollziehbar.

Die zusätzlichen Kontrollbilder sind teilweise einmalig und nicht anderweitig gesichert. B bedeutet hier ausdrücklich **bewusst entbehrliche Historienmedien nach Freigabe**, nicht „verlustfrei aus einem Backup wiederherstellbar“. Die ausgewählten A-Schlüsselbilder bewahren die wesentlichen visuellen Vergleiche. Nicht ausgewählte alte Screenshotlinks beziehungsweise vollständige Bildfolgen können nach Entfernung nicht mehr funktionieren.

`Saved/Autosaves/PackageRestoreData.json` bestätigt `RestoreEnabled=false` und eine leere `Packages`-Liste. Die lokale WorldState-Datei enthält ausschließlich die Ordneransicht; die SourceControl-Datei enthält Pfadlisten, keine Assetnutzdaten. Keine dort versteckte wiederherzustellende Map gefunden. Aktive unversionierte Dateien sind separat erhalten.

### C – ungeklärte Dateien

**0 Dateien im alten Worktree bleiben in C**, bezogen auf diese konkrete Inhalts-/Erhaltungsentscheidung. Das bedeutet keine pauschale Löschfreigabe: A muss vor Entfernung erhalten werden; B braucht die ausdrückliche Zustimmung. Die sieben freigegebenen aktiven Texture-UAssets bleiben geschützt; die unten beschriebene Reimport-Darstellungsfrage ist eine gesonderte technische Folgeaufgabe, keine Abhängigkeit auf alte physische Dateien.

## 4. Unreal-Reimport ohne erreichbaren alten Worktree

Ein separater regulärer Unreal-Editorprozess startete das **aktive Projekt und die vorhandene VisualV2**. Es wurden keine Projekte, Maps oder gespeicherten Testassets angelegt. Jede Textur wurde mit `SystemLibrary.duplicate_object` in `/Engine/Transient` dupliziert; auch deren AssetImportData war unabhängig und gehörte zur Kopie.

Die Testinstanz bekam zusätzlich eine eigene macOS-Zugriffsbeschränkung:

- Jeglicher Lesezugriff auf den gesamten alten Worktree gesperrt.
- Jeglicher Schreibzugriff auf aktives `Content`, `Art`, `Source`, `Config` und `.git` gesperrt.
- Negativkontrolle: Öffnen der alten Quelldatei innerhalb dieser Instanz scheiterte nachweislich mit `PermissionError`.
- Aktuelle Quelldateien unter `Art/World/...` waren lesbar und SHA-256-identisch zum erwarteten Original.

Die Originale extrahieren bereits korrekte aktuelle SourceFile-Pfade. Da eine transiente Kopie in einem anderen Paket liegt, wurde **nur an der Kopie** `AssetImportData.scripted_add_filename(aktueller_absoluter_Pfad, 0, '')` gesetzt. Alte kopierte Factory-/Node-Kennungen wurden nicht manuell ersetzt. Anschließend tatsächlicher asynchroner Interchange-Reimport, jeweils mit Completion-Callback auf die transiente Kopie, nie auf das Original. Texturkompilierung vor dem abschließenden Lauf kontrolliert abgeschlossen; keine dauerhafte Projekteinstellung geändert.

| Textur | Aktuelle Quelle relativ zum Projekt | Reimport bei gesperrtem Altpfad | Ausgabegröße |
| `T_HA3_Meadow` | `Art/World/VisualV2HealingArtV3/Textures/T_HA3_Meadow.png` | Erfolgreich, nur transiente Kopie | 2048 × 2048 |
| `T_HA3_Earth` | `Art/World/VisualV2HealingArtV3/Textures/T_HA3_Earth.png` | Erfolgreich, nur transiente Kopie | 2048 × 2048 |
| `T_HA4_Wood` | `Art/World/VisualV2HealingArtV4/Textures/T_HA4_Wood.png` | Erfolgreich, nur transiente Kopie | 2048 × 2048 |
| `T_HA4_Meadow` | `Art/World/VisualV2HealingArtV4/Textures/T_HA4_Meadow.png` | Erfolgreich, nur transiente Kopie | 2048 × 2048 |
| `T_HA4_Earth` | `Art/World/VisualV2HealingArtV4/Textures/T_HA4_Earth.png` | Erfolgreich, nur transiente Kopie | 2048 × 2048 |
| `T_WA5_ForestFloor` | `Art/World/VisualV2WorldArtV5/Textures/T_WA5_ForestFloor.png` | Erfolgreich, nur transiente Kopie | 2048 × 2048 |
| `T_WA5_WetBank` | `Art/World/VisualV2WorldArtV5/Textures/T_WA5_WetBank.png` | Erfolgreich, nur transiente Kopie | 2048 × 2048 |

**7/7 tatsächliche Reimports erfolgreich, Editor regulär mit Exit 0 beendet.** Original-Assetparameter und Original-Importdateinamen vor/nach identisch; alle Original-UAssets SHA-256-identisch; vor/nach keine dirty Map-/Content-Pakete; keine Assets gespeichert. Der nachgewiesene alte Interchange-Pfad ist daher für diese Reimportoperation keine erforderliche physische Quelldatei.

### Nachgewiesene Reimport-Falle: Darstellung nicht automatisch gleich

Bei **allen sieben Testkopien** setzte Unreal folgende Werte um:

| Eigenschaft | Original/Kopie vorher | Kopie nach normalem Reimport |
|---|---|---|
| Compression Settings | `TC_EDITOR_ICON` / UserInterface2D | `TC_DEFAULT` |
| Mip Gen Settings | `TMGS_NO_MIPMAPS` | `TMGS_FROM_TEXTURE_GROUP` |

Ausgabegröße 2048², sRGB, MaxTextureSize, Filter, Addressierung und die weiteren geprüften Werte blieben im abschließenden Lauf gleich. **Keine visuelle Gleichheit des reimportierten Ergebnisses behauptet.** Die Originalmaterialien/-texturen wurden nicht geändert.

Die Ursache ist lokal im tatsächlichen Engine-Code nachvollziehbar: `/Users/Shared/Epic Games/UE_5.8/Engine/Source/Runtime/TextureUtilitiesCommon/Private/TextureImportSettings.cpp:128–154`, `ApplyDefaultsForNewlyImportedTextures`. Bei Reimport einer passenden NoMip-/UI-Textur mit Power-of-two-Quelle oder aktivem PowerOfTwoMode stellt UE diese Werte auf normale Pow2-Defaults um. Die Engine protokollierte diese konkrete Umschaltung für die Kopien. Das ist keine Vermutung aufgrund bloßer Bildunterschiede.

**Sicherer Vorschlag:**

1. Für die Worktree-Entfernung die aktiven Texture-UAssets überhaupt nicht neu importieren oder speichern. Ihre tatsächlichen SourceFile-Pfade sind korrekt; der isolierte Test bestätigt die Quellenunabhängigkeit. Keine binäre String-Ersetzung alter Factory-IDs.
2. Wenn später eine echte Quelländerung einen Reimport erfordert: zuerst auf isolierter Kopie testen; alle bisherigen Textureinstellungen erfassen. Nach dem Import müssen insbesondere die beabsichtigten Kompressions-/Mip-Werte ausdrücklich erhalten beziehungsweise wiederhergestellt und die Darstellung kontrolliert werden. Auch Einstellungen außerhalb der hier geprüften Auswahl vor Übernahme berücksichtigen.
3. Eine eventuelle **reine** SourceFile-Pfadkorrektur darf ausschließlich Importmetadaten betreffen und keinen Reimport auslösen. Hier ist sie aktuell nicht nötig. Ein Reimport samt Aufräumen der Factory-/Node-Metadaten bedarf einer gesonderten technischen und visuellen Abnahme.

Die vorhandenen vier WestlandRegion-FBX-Importpfade nach `/Users/Shared/Art/...` sind ein getrennter Altbefund. Die Quell-FBX-Dateien liegen im aktiven Projekt. Diese Assets wurden weder bearbeitet noch als Bedingung für die sieben Textur-Reimports ausgegeben.

### Transparenz der Testläufe und Logs

Vor dem abschließenden Siebenerlauf gab es drei abgegrenzte Diagnoseanläufe: erst ein erwartbar anders aufgelöster relativer Pfad der transienten Kopie, dann eine korrigierte Python-Callback-Signatur, schließlich ein erfolgreicher erster Reimport mit Stopp am Einstellungsunterschied. Alle Sitzungen regulär beendet, keine Originalassets gespeichert. Die endgültige Prüfung bindet die Quelle der Kopie explizit, beendet alle sieben Reimports und protokolliert Unterschiede statt sie zu verbergen.

Im endgültigen Engine-Log weiterhin 17 bereits bekannte Startup-Zeilen `LogAutomationTest: Error: Condition failed`, daneben elf Warnungszeilen einschließlich `idevice_id`/Audio-/MCP-Hinweisen. Keine neuen Shader-/Material-/Textur-Importfehler in den Fehlerzeilen. Dies ist keine allgemeine Logfehlerfreiheit und kein neuer Automationstestpass. Die Warnungen und Prüfdaten stehen vollständig im strukturierten Nachweis.

## 5. Git, LFS und lokale Daten nach Prüfung

| Prüfung | Tatsächlich erneut bestätigt |
|---|---|
| Main und direktes GitHub-origin/main | `427d93f92765b2e03d8dca186fbc6bfbd86c8605` |
| Aktive versionierte Dateien | 3.514/3.514 SHA-256-identisch zu Git-/LFS-Nutzdaten |
| Benötigtes Core-Manifest | Im vorherigen unveränderten Stand 3.513/3.513 bestanden; Quellen jetzt frisch identisch bestätigt |
| Alte Worktree-Dateien | 14.277 frisch gehasht, keine Änderung zum vorherigen Inventar; keine unversionierten nicht ignorierten Dateien |
| Aktive Art-Dateien einschließlich ignorierter Originale | 1.476 Metadatensätze gegen geschützte Vorprüfung identisch; MiniHobbit-GLB weiterhin vorhanden, unverändert und nicht in Git aufgenommen |
| Ursprüngliche unversionierte Nutzerdateien | 38/38 frisch SHA-256-identisch; übriger vorheriger unversionierter Status ebenfalls unverändert |
| Dev-Spielstand | SHA-256-identisch zum geschützten Original `a0ad009a7b3c6f883d1413b0f96df5b25bc7ab953d0154e29ae50f35ad48bf0a` |
| Lokale LFS-Nutzdaten | 11.205 Objekte / 19.010.564.957 Bytes frisch SHA-256-geprüft, kein ungültiges Objekt; alle 9.696 erwarteten Objekte vorhanden |
| Vollbackup-LFS | 9.451 Objekte / 16.442.940.729 Bytes vollständig im aktiven gemeinsamen Speicher |
| GitHub-LFS | 1.383 Objekte / 6.607.098.907 Bytes frisch serverseitig download-verfügbar bestätigt; keine Binärdownloads/Uploads |
| Schutzrefs | `backup/full-03492bd` und `refs/archive/pokemonster/full-backup-03492bd` unverändert |
| Git-Integrität | `git fsck --full --no-reflogs`: Exit 0; bestehende dangling Objekte nicht bereinigt |
| Index, Refs, Worktrees | Unverändert, kein Staging |
| Diff | `git diff --check` ohne Befund |

Git-/LFS-Speicher liegt ausschließlich im aktiven `.git`. Kein Alternate oder externer LFS-Speicher auf dem alten Worktree. Dessen `.git` ist nur der Verweis auf aktives `.git/worktrees/Worktree`, `commondir` ist korrekt, kein Lock oder Submodul. Der alte Branch kann nach späterer Entfernung unverändert erhalten bleiben; kein Prune oder Branchlöschen nötig. `FullBackup` und `FullRestore` bleiben als Geschwister außerhalb des alten Worktrees geschützt.

Der frühere unversionierte Experiment-Einstiegspunkt `Tools/VisualV2EnvironmentQualityV1/Startup.py` enthält weiterhin eine Assertion auf den alten Worktree. Er gehört nicht zum normalen Build/Gameplay und ist bereits im aktiven Projekt in diesem Zustand nicht direkt ausführbar. Seine Quellen bleiben erhalten. Für einen künftigen historischen Replay wäre nach separater Freigabe die Root-Assertion anzupassen und A-Nachweisdaten über das CSV zuzuordnen. Die Existenz dieses alten Einmal-Setups begründet keine physische Bindung des aktuellen Spiels an den alten Checkout.

**Keine neuen Builds, Projekt-Automationsläufe oder PIE-Fußläufe in diesem Auftrag:** Es wurde kein Code/Runtimeasset geändert. Tatsächlich neu sind die kontrollierten Reimports und die oben beschriebenen schreibfreien Analysen. Der Editor lud die vorhandene VisualV2 unter gesperrtem alten Projektpfad; ein vollständiger neuer Gameplay-Abnahmelauf wird daraus nicht abgeleitet. Normale generierte Editor-/Cache-/Logausgaben können sich durch die gestarteten Tests ändern; keine manuelle Löschung oder Source-/Map-Speicherung.

## 6. Konkreter Speicher- und Umsetzungsplan zur Freigabe

| Umfang | Dateien | Logische Bytes | Logische GiB | APFS-exklusive Bytes | APFS-exklusive GiB |
| Gesamter verbleibender Worktree | 14.277 | 14.160.819.328 | 13,188 | 8.518.242.304 | 7,933 |
| A: gezielt erhalten | 6.655 | 1.656.154.158 | 1,542 | 885.460.992 | 0,825 |
| B: nach A-Übernahme entfernbar | 7.622 | 12.504.665.170 | 11,646 | 7.632.781.312 | 7,109 |
| C: ungeklärte Worktree-Dateien | 0 | 0 | 0,000 | 0 | 0,000 |

**Empfohlener zusätzlicher Speichergewinn: rund 7,109 GiB = 7.632.781.312 Bytes**, nachdem A ohne zusätzliche Kopie auf demselben Volume erhalten wurde und der restliche alte Checkout entfernt wird. Die frühere pauschale Schätzung von 7,933 GiB muss um die weiterhin benötigten exklusiven A-Blöcke reduziert werden. 11,646 GiB logische B-Daten sind keine Garantie für ebenso viel sofort freien SSD-Platz.

APFS-Privatbelegung für alle Dateien frisch abgefragt, keine Abfragefehler, weiterhin keine Hardlinks im alten Worktree. Die großen verbliebenen Art-Kontrollbilder besitzen derzeit keine exklusiven Dateiblöcke; ihre Entfernung bringt daher nicht sofort ihren gesamten logischen Umfang als freien Speicher. Snapshots/Klone, Dateisystemmetadaten und laufende Systemaktivität beeinflussen den tatsächlichen späteren Nettofreigewinn. Vor/nach einer genehmigten Ausführung erneut messen. Kein Speicher aus `FullBackup`, `FullRestore`, anderen alten Ordnern oder dem gemeinsamen Git-/LFS-Speicher eingerechnet.

**Vorgesehene Ausführung, jetzt nicht durchgeführt:**

1. Das CSV mit den genauen A/B-Zuordnungen und Zielpfaden ausdrücklich freigeben lassen.
2. A einzeln nach aktuellem Hashcheck in die aktive `Saved`-Struktur übernehmen, **ohne vorhandene Dateien zu überschreiben und ohne eine neue Projekt-/Versionskopie anzulegen**. Alle 6.655 vorgeschlagenen Zielpfade sind aktuell frei, kein Konflikt. Bestehende Unterstrukturen verwenden beziehungsweise nach Freigabe nur notwendige Unterordner für die übernommenen bisherigen Daten anlegen; heute kein Ordner angelegt. Für eine spätere Verschiebung auf demselben Volume ist keine zusätzliche Backupkopie nötig.
3. Übernommene A-Dateien nochmals SHA-256-prüfen; interne B-Duplikate erst dann als entbehrlich behandeln. Andere bereits nachgewiesene Gegenstücke außerhalb des Worktrees schützen. A-Nachweise bleiben lokal unter ignoriertem `Saved`, nicht automatisch auf GitHub hochladen. Die wichtige versionierte Projektbasis und ihre Originalquellen bleiben in Git/Git LFS.
4. Bei Veränderungen, Zielkonflikten, unklaren neuen Dateien oder fehlgeschlagener Prüfung anhalten. Keine Änderungen an Original-UAssets für diesen Schritt erforderlich.
5. Erst danach den alten Worktree ausschließlich über `git -C /Users/harry/Developer/PokeMonster worktree remove <exakter alter Pfad>` entfernen; nicht per Finder oder pauschalem `rm`. Ignorierte Dateien sind durch einen sauberen Git-Status nicht geschützt. Kein automatisches `--force`, kein Reset/Clean, kein LFS-Prune.
6. Anschließend Root/Remote, Schutzrefs, LFS, Quellen und wichtige Maps prüfen. Der alte Branch sowie `FullBackup`/`FullRestore` bleiben erhalten.

**Aktueller Stopp-Punkt:** Alle Daten bleiben am bisherigen Ort. Warten auf Harrys ausdrückliche Freigabe für die gezielte A-Übernahme und anschließende Worktree-Entfernung. Dieser Bericht und das CSV sind keine Ausführungsfreigabe.

## 7. Ergebnisdateien

- `/Users/harry/Developer/PokeMonster/Docs/ALTER_WORKTREE_ABSCHLUSSPRUEFUNG.md` – dieser vollständige Bericht.
- `/Users/harry/Developer/PokeMonster/Docs/ALTER_WORKTREE_ABC_DATEILISTE.csv` – alle 14.277 alten Dateipfade mit Kategorie, Bytezahl, SHA-256, Gegenstück, Zielvorschlag und Freigabebedingung. Keine automatisch ausführbare Löschliste.
- `/Users/harry/Developer/PokeMonster/Docs/ALTER_WORKTREE_REIMPORT_PRUEFUNG.json` – tatsächliche Reimport-/Originalschutzresultate und detaillierter Blender-Vergleich samt exakter Rekonstruktion; keine binären Modell-Backups oder Kontrollmedien.
- CSV-SHA-256: `0e2434896211c0c8174af12bbaf983f542f52ff51ece0571b55f1f0a6b6d8785`.
- Nachweis-JSON-SHA-256: `3252f7bfeac24072eaaac6d75ae1cd928d9a80e85e240ffe8a1d3a226b39ba3a`.

Vor Berichtserstellung 46 bereits unversionierte Einzelpfade, danach ausschließlich diese drei neuen Dokumentationspfade zusätzlich. Keine bestehenden Reports überschrieben. Rohlogs und kurzlebige Analysewerkzeuge nur unter `/tmp/pokemonster_worktree_*`; vorhandene Projekt-/Bereinigungsnachweise unverändert erhalten. Kein Commit und kein Push.
