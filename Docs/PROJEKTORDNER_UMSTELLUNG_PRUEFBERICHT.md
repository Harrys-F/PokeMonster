# PokeMonster – Umstellung auf den festen Projektordner

19.10.2026. **Projektdateien, Git und benötigte Werkzeuge sind nach
`/Users/harry/Developer/PokeMonster` umgestellt und geprüft.** Der bisherige
schlanke Worktree bleibt erhalten. Keine Bereinigungsfreigabe wird vorweggenommen.
Der Arbeitsordner der laufenden Codex-Unterhaltung benötigt noch einen manuellen
Wechsel in der App; diese Einschränkung ist unten ausdrücklich benannt.

## 1. Aktiver Stand und bestehendes GitHub-Repository

- Unreal-Projekt: `/Users/harry/Developer/PokeMonster/PokeMonster.uproject`.
- Git-Hauptverzeichnis: `/Users/harry/Developer/PokeMonster/.git`.
- Aktiver Branch: `main`, Upstream `origin/main`.
- Unveränderte Remote-Adresse: `git@github.com:Harrys-F/PokeMonster.git`.
- Übernommener GitHub-Ausgangsstand: `30a165b034114ba4b0940a369e73143db988afad`.
- Geprüfter und bereits gepushter Umstellungscommit: **`7d7b5bc199dc153b83bd614bd8233855e28dbf58`**.

Kein neues GitHub-Repository, Clone, Projektduplikat oder zusätzlicher Worktree.
Das vorhandene primäre Repository wurde aus `Game/PokeMonster` direkt angehoben.
Die vorhandenen leeren äußeren Ordner `Art` und `Docs` wurden nur nach Prüfung
ohne Dateikollisionen befüllt. Alle übrigen Einträge wurden auf demselben
Datenträger umbenannt/verschoben; keine blinde Ordnerkopie. Die Verbindung des
bestehenden schlanken Worktrees wurde mit Git repariert.

Der aktuelle schlanke Stand wurde anschließend über einen normalen Branchwechsel
übernommen. Die 8.580 bereits im V5-Verfahren als optionale Nachweise klassifizierten
Pfade gehören nicht zum schlanken Checkout. Ihre Daten bleiben im unveränderten
Vollbackup, in den lokalen LFS-Objekten und den bereits vorhandenen
`FullBackup`-/`FullRestore`-Beständen erhalten. Keine Quarantäne- oder Ordnerbereinigung.

## 2. Vollbackup und Datenerhalt

Der frühere lokale `main` heißt jetzt `backup/full-03492bd` und besitzt keinen
Upstream auf `origin/main`. Beide lokalen Schutzverweise zeigen weiterhin auf:

```
backup/full-03492bd
refs/archive/pokemonster/full-backup-03492bd
03492bd96b4dba44692f675c19d5f11abfa86b4b
```

Der Backup-Commit ist weiterhin kein Vorfahr des schlanken `main`. Keine Historie
umgeschrieben, kein Force-Push, Reset, Restore, Clean oder LFS-Prune ausgeführt.
Alle 9.451 vom Vollbackup referenzierten LFS-Objekte mit 16.442.940.729 Bytes
wurden vor dem Ortswechsel vollständig per SHA-256 geprüft. Die Git-/LFS-Daten
wurden zusammen mit dem Repository angehoben, nicht durch eine neue Sicherung ersetzt.
Die bestehende unabhängige Wiederherstellungskopie wurde gegen ihre 11.343
Originaldateien geprüft und blieb unverändert.

Alle **11.170 zuvor ignorierten Dateien** des ursprünglichen Projekts waren direkt
nach Branchwechsel bytegleich erhalten. Dazu gehören Blender-Sicherungsdateien,
lokale Eingaben, Werkzeugsitzungen und der echte Dev-Spielstand. Spätere reguläre
Build-/Editor-/Rider-Ausgaben dürfen ihre eigenen generierten Dateien aktualisieren.
Der originale Dev-Spielstand wurde während des Fußlaufs nur vorübergehend
umbenannt und danach SHA-256-identisch zurückgelegt; keine zusätzliche Kopie.

Alle **38 zuvor unversionierten Dateien** aus dem schlanken Worktree wurden
einzeln, ohne Zielkonflikt, am festen Projektpfad erhalten und bleiben uncommittet:
die EnvironmentQuality-V1-Testkarte, 36 zugehörige Werkzeug-/Plandateien und ein
vorhandener Python-Cache. Der ausdrücklich aus Git ausgeschlossene
`Art/Characters/MiniHobbit/Meshy_MiniHobbit.glb` bleibt lokal erhalten und ignoriert.
Keine neue Map wurde erstellt.

## 3. Notwendige Projektanpassungen

- 69 vorhandene Werkzeuge: ausschließlich Projektpfade und Backup-Ref-Prüfungen
  umgestellt. AST-Vergleich ohne weitere Logikänderung.
- `AGENTS.md`, `Docs/TECHNIK.md`, `Docs/ENTSCHEIDUNGEN.md`: fester Projektpfad,
  Branch-Zuordnung, Schutz des Vollbackups und Freigabepflicht für weitere Worktrees
  beziehungsweise neue Maps dokumentiert.
- Kleine wiederverwendbare Prüfwerkzeuge unter `Tools/ProjectMaintenance/`.
- Nur deren lokaler Python-Cache gezielt in `.gitignore` ausgeschlossen.
- Pflichtdatei-Snapshot `Tools/DevelopmentEvidence/CoreFiles.json` auf den
  tatsächlich geprüften Entwicklungsstand aktualisiert; frühere Version in Git erhalten.

### Zwei Blender-Texturpfade

Alle 95 versionierten Blenderdateien konnten geöffnet werden. Zwei Quellen
enthielten noch denselben ungepackten absoluten Blatttexturpfad zum alten Unterordner:

| Quelldatei unter `Art/World/` | Neuer relativer Texturpfad |
|---|---|
| `TreeShadowProxyV1/Source/OakAncient_ShadowProxy_V1.blend` | `//../../WestlandAssetLibrary/Textures/T_WLA_FoliageGroups_V3.png` |
| `WestlandAssetLibrary/Source/WestlandAssetLibrary_V3.blend` | `//../Textures/T_WLA_FoliageGroups_V3.png` |

Nur diese Verweise und erforderliche Erhaltungsmetadaten wurden gespeichert.
Ein erster Fingerprint-Prüfer stoppte vor dem Schreiben wegen eines bislang
nicht berücksichtigten `INT32_2D`-Attributs. Ein weiterer Schutzvergleich erkannte,
dass Blender beim Speichern 40 vorhandene unbenutzte Mesh-/Materialdatenblöcke
des Schattenproxies entfernen würde. Die eigene Änderung wurde vollständig aus
dem verifizierten Original-LFS-Objekt zurückgenommen. Im finalen Lauf wurden
diese vorhandenen Datenblöcke ausdrücklich mit Fake User erhalten.

**Final bestanden:** Mesh-, Topologie-, UV-/Farbattribut-, Material- und
Objekttransformations-Fingerprints vor/nach erneutem Öffnen identisch.
Keine Modellvereinfachung, keine neuen Formen, kein Remesh, Rigging, Export oder
Unreal-Reimport. Keine zusätzliche `.blend1`-Datei. Eine unabhängige Nachprüfung
beider gespeicherten Quellen findet keine fehlenden Abhängigkeiten.
Die übrigen Blenderquellen und sämtliche Charakterquellen bleiben bytegleich.
Einzelne vorhandene `.blend`-Dateien sind Datenbibliotheken ohne eigene Szene;
die Lesbarkeitsprüfung ist keine neue künstlerische Produktionsfreigabe.

## 4. Anwendungspfade

| Anwendung | Tatsächlicher Nachweis |
|---|---|
| Unreal | Projekt am festen Pfad gestartet; drei vorhandene Karten geladen; echter eingebetteter PIE-Test; anschließend ohne dirty Pakete regulär geschlossen |
| Rider | richtige `.uproject` geöffnet; Oberfläche zeigte `~/Developer/PokeMonster`; `lastOpenedProject` nach regulärem Schließen auf den festen Projektpfad gespeichert |
| Blender | alle versionierten Quellen separat geöffnet; erforderliche Texturpfade korrigiert; die zuvor ungespeicherte Sitzung zunächst ohne Speichern/Schließen an den neuen Pfad angebunden |
| Codex | sämtliche Projektbefehle verwenden den festen Pfad; neue AGENTS-Anweisung bindend. Der Chat-Arbeitsordner selbst konnte nicht automatisch umgestellt werden |

**Codex-Restschritt:** Die Computersteuerung verweigert den Zugriff auf
`com.openai.codex` ausdrücklich aus Sicherheitsgründen. Die verfügbaren
App-Werkzeuge bieten keinen Wechsel des Dateisystem-Arbeitsordners dieser
Unterhaltung. Deshalb bitte `/Users/harry/Developer/PokeMonster` in Codex manuell
als Projekt-/Arbeitsordner auswählen. Keine internen App-Datenbanken oder
Sicherheitsregeln umgangen. Ein geöffneter Dateitab allein wäre kein Nachweis
eines gewechselten Arbeitsordners.

Die zuvor offene ungespeicherte Blender-Sitzung war später beendet; kein
Beenden-/Force-Quit-Befehl dafür ausgeführt. Die vorhandene Datei
`/private/var/folders/z1/n21jrmp92tz7q81bj_vm7jzc0000gn/T/quit.blend` vom 19.10.,
18:03:29 lässt sich separat lesen und enthält 217 Objekte ohne fehlende
Bibliotheksverweise. Sie wurde weder überschrieben noch zusätzlich kopiert.
Die genaue Ursache der Beendigung wurde nicht abschließend festgestellt.

## 5. Tatsächlich durchgeführte Prüfungen

| Prüfung | Ergebnis |
|---|---|
| Mac Development Editor Build | bestanden, Exit 0; 85 Buildaktionen, 47,95 s |
| vollständige Unreal-Projekt-Automation | **49/49**, keine Testwarnungen, Fehler oder ausgelassenen Tests |
| bestehende Evidence-Sicherheitstests | **8/8** bestanden |
| Map Check VisualV2 | 0 Fehler, 0 Warnungen |
| Map Check WestlandRegion | 0 Fehler, 0 Warnungen |
| Map Check NPCMotionV3 | 0 Fehler, 0 Warnungen |
| vorhandene 17 Map-Dateien | SHA-256-identisch zum schlanken Ausgangsstand; keine gespeichert |
| Gameplay-Fußlauf | **102 Schritte**, 282.32 m, erfolgreich; tatsächliche Eingaben, keine Test-Teleports |
| Gameplay-Funktionen | Wanderer/Quest, Liora, Kampf/Fang, Archiv, Menü, Heilhaus innen/außen, Heilung/Checkpoint, Save/Load, acht Richtungen, Sprint, Kollisionen, Kronenfreistellung und NPC-Sprite-Fallback geprüft |
| Spielerwerte | unverändert, maximal gemessen 315 cm/s im Sprint; Kamera 2850 cm/FOV 35 bestätigt |
| Blender | 95 Dateien geöffnet; zwei erforderliche Pfadkorrekturen separat erneut geprüft |
| Git-Objekte | `git fsck --full --no-reflogs` Exit 0; bestehende dangling Objekte nicht bereinigt |
| gesamte bisherige Remote-Historie | 109 Ausgangscommits erreichbar; 1.381 LFS-Objekte/6.564.018.122 Bytes lokal SHA-256-geprüft und serverseitig als verfügbar bestätigt |
| Verbindung | direkter Remote-Abgleich, regulärer Fast-Forward-Pull ohne Änderungen, Push-Probelauf und anschließend echter regulärer Push erfolgreich |
| Diff/Index | geprüfte exakte Dateiliste; `git diff --check` und `git diff --cached --check` bestanden |

Build/Automation/Map/Gameplay erfolgten am festen Projektpfad. Die späteren
Blenderänderungen betreffen ausschließlich Authoring-Metadaten, keine Runtimeassets.
Keine FPS-Benchmarks, kein GPU-Profiling, kein neuer Cook-/Shipping-Nachweis.
Kamera, Licht, Schatten, Materialien in Unreal, C++-Gameplay und Animationen
wurden nicht geändert. Die Engine meldet weiterhin u. a. das nicht startfähige
Hilfsprogramm `idevice_id` (Bad CPU type); keine allgemeine Logfehlerfreiheit behauptet.

### Vier übernommene Importmetadaten-Befunde

Die frische AssetImportData-Prüfung erfasst 391 Quellen. Vier WestlandRegion-
Pflanzenassets melden einen bereits gespeicherten relativen Pfad, der außerhalb
des Projekts nach `/Users/Shared/Art/...` aufgelöst wird:
`SM_WR_Ground_NarrowHerb`, `SM_WR_Ground_LeafPlant`,
`SM_WR_Ground_FlowerPlant`, `SM_WR_Ground_BroadHerb`.
Die zugehörigen FBX-Dateien liegen vollständig unter
`Art/HealingHouse/Exports/QualityV3/`; ihre MD5-Prüfsummen stimmen mit den
gespeicherten Importwerten überein. Keine fehlenden Quelldaten und kein
Runtime-/Materialfehler nachgewiesen. Die unverändert übernommenen UAssets
wurden nicht automatisch neu importiert oder gespeichert. Eine spätere
gezielte Importpfadkorrektur ist empfehlenswert.

## 6. GitHub-Sicherung und Protokolle

Umstellungscommit `7d7b5bc199dc153b83bd614bd8233855e28dbf58`: **81 Pfade**, regulär gepusht,
Remote-Hash bestätigt. Zwei neue LFS-Objekte mit zusammen **43.080.785 Bytes**
hochgeladen und anschließend unabhängig vom Server heruntergeladen und
SHA-256-verifiziert. Keine lokale zusätzliche Binärkopie dafür angelegt.
Normale Git-Blobs dieses Deltas zusammen höchstens 1.790.731 Bytes, deutlich
unter 1 GiB. Keine Kontrollbilder, Videos oder temporären Ausgaben aufgenommen.
Keine Käufe oder Budgetänderungen; ein kontoweiter aktueller Abrechnungsstand
ist über die vorhandene SSH-Verbindung nicht unabhängig einsehbar.

Dieser Bericht wird separat als Dokumentationscommit gesichert. Dessen tatsächlicher
Hash und letzter Remote-Abgleich stehen im Abschluss dieser Unterhaltung und
lokal unter `Saved/ProjectMigration/GitFinal.json`.

Alle neuen Rohprotokolle liegen ausschließlich lokal unter
`/Users/harry/Developer/PokeMonster/Saved/ProjectMigration/`:
`Build.log`, `Automation/Result.json`, `Maps.json`, `Imports.json`,
`Acceptance/RelocatedRoot/FootTest.json`, `Acceptance/RelocatedRoot/SaveRestored.json`,
`BlenderSources.json`, `BlenderSourcesRetest.json`, `BlenderPathRepairs.json`,
`ToolSemanticAudit.json`, `RemoteHistoryLocal.json`, `RemoteHistoryServer.json`,
`Commit1IndexAudit.json`, `Commit1Result.json` und die vollständigen Rohlogs.
Die ersten Blender-Prüfbefunde bleiben neben den bestandenen Nachprüfungen erhalten.

## 7. Alter Worktree und Freigabegrenze

Der bisherige Worktree bleibt unter
`/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree`
registriert, Branch `codex/slim-backup-v5`, letzter dortiger Checkout `30a165b`.
Sein Arbeitsbaum ist nach Übernahme der 38 unversionierten Dateien sauber;
seine reparierte Git-Verbindung zeigt auf das Repository im festen Projektordner.

**Als Entwicklungsort ist er nicht mehr erforderlich. Als Datenbestand ist er
noch nicht pauschal entbehrlich:** Bei Bestandsaufnahme rund 37,51 GiB belegte
Dateiblöcke, davon rund 30,69 GiB logisch ignorierte lokale Dateien; überwiegend
Saved-Nachweise und generierte Dateien. Diese wurden bewusst nicht auf GitHub
hochgeladen. Einzelne Prüf-/Reviewabläufe können sie weiterhin benötigen.
Diese Zahlen sind Bestandswerte, keine garantierte physisch freizugebende Größe
auf APFS. Keine zusätzliche Sicherung oder neue Versionskopie erstellt.

**Keine Worktree-Entfernung, keine Löschung alter Ordner und kein LFS-Prune.**
Vor Entfernung sind die nur lokalen Nachweise ausdrücklich einzuordnen und die
Bereinigung durch Harry freizugeben. Das vorhandene Vollbackup und seine bereits
vorhandenen Archiv-/Wiederherstellungsbestände bleiben unabhängig davon geschützt.
