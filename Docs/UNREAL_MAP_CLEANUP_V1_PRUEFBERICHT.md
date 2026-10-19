# Unreal Map Cleanup V1 – Prüfbericht und bedingte Löschliste

Stand: 19.10.2026. **Nur Analyse. Keine Map gelöscht, verschoben, geändert oder neu erstellt. Keine Referenz angepasst.**

## 1. Ergebnis und Empfehlung

**17 Maps vorhanden: 16 versioniert und auf GitHub verifiziert, eine unversioniert und nur lokal geschützt.**

| Kategorie | Anzahl | Bedeutung in diesem Bericht |
|---|---:|---|
| A – behalten | **9** | Acht regulär benötigte Karten plus eine ausdrücklich geschützte unversionierte Map als vorläufige Schutzposition |
| B – nach Anpassungen möglicherweise entfernbar | **8** | Historische/zusätzliche Prüfszenen; notwendige Umstellungen und Freigabe fehlen noch |
| C – ohne Funktionsverlust entfernbar | **0** | Keine Map erfüllt derzeit alle Kriterien |

**Empfehlung: langfristig acht reguläre Maps**, ohne neue Map anzulegen. Bis zur unabhängigen Klärung der unversionierten Map sind **neun** zu erhalten. Eine Reduktion von 17 auf neun wäre nach erfolgreicher Abhängigkeitsumstellung und ausdrücklicher Freigabe der acht B-Kandidaten möglich; acht insgesamt erst nach gesonderter Entscheidung über die unversionierte Map.

Die drei vom Nutzer grundsätzlich geschützten Karten bleiben uneingeschränkt erhalten: VisualV2, WestlandRegion und WestlandAssetLibrary. Zusätzlich sind aktuelle Start-/Regressionstestkarten, die offene Ranger-V3-Arbeitsgrundlage und eine vorhandene gemeinsame Diagnosemap sinnvoll. Keine Freigabe zur Entfernung aus einer bloßen älteren Versionsnummer abgeleitet.

**Kein sofortiger Löschkandidat:** Die Asset Registry meldet zwar keine eingehenden Assetreferenzen auf die 17 Maps, aber alle 16 versionierten Maps sind Pflichtdateien des aktuellen Core-Manifests. Startkonfiguration, native Map-Loader, historische Vergleichswerkzeuge und eigenständige Prüfszenarien kommen hinzu. „Keine Assetreferenz“ bedeutet deshalb nicht „ohne Funktionsverlust löschbar“.

## 2. Projektzustand und Prüfverfahren

- Ausschließlich `/Users/harry/Developer/PokeMonster` verwendet; Unreal-Projekt `PokeMonster.uproject` direkt darin.
- Branch `main`; HEAD und direkt bestätigtes GitHub-origin/main zu Beginn: **`ce450f4bb7e105efd54bd5512a1b47766c045c63`**.
- Index leer, keine versionierten Änderungen. **49 bestehende unversionierte Dateien** sind geschützt, darunter genau eine Map.
- Während der Untersuchung kamen vier weitere unversionierte GLB-Dateien hinzu: `Art/Characters/Creatures/Incoming/{Enton,Glurak,Myrapla,Pikachu}.glb`. Der erste strenge Statusvergleich stoppte deshalb vor dem Staging. Diese fremden Eingänge sind keine Mapänderung, wurden nicht importiert oder bearbeitet und bleiben vollständig vom Dokumentationscommit ausgeschlossen. Danach verbleiben **53 unversionierte fremde Dateien**; die ursprünglichen 49 sind unverändert.
- AGENTS und die bereits geprüften relevanten TECHNIK-/ENTSCHEIDUNGEN-/Weltart-/NPC-/Performance-Unterlagen berücksichtigt. Grundlage für den Szeneninhalt: `Docs/VISUALV2_WELTGESTALTUNG_V1_VERGLEICHSBERICHT.md` und das zugehörige tatsächliche Mapinventar.
- Alle `.umap` unter dem gesamten `Content` rekursiv erfasst; 17 Dateien. Die frisch neu gescannte Asset Registry bestätigt ebenfalls genau 17 World-Assets. Keine zusätzlichen Content-Maps außerhalb dieses Bestands gefunden.
- Fresh Registry-Abfrage für Hard-, Soft-, Searchable- und Management-Referenzen, direkte Dependencies und die transitive `/Game`-Paketmenge. **840 On-Disk-Assets** unter `/Game` erfasst. Keine Pakete gespeichert; final keine Dirty-Map-/Contentpakete; eigene Editor-Prüfsitzung regulär beendet, Exit 0.
- Exakte Mapnamen in versionierten Textdateien und geschützten unversionierten Werkzeugdateien gesucht; Dokumentation und Autoren-/Reviewdaten getrennt von ausführbaren Ladeabhängigkeiten betrachtet. Zusammengesetzte Mapnamen im EnvironmentPerfV3-Review ebenfalls geprüft.
- Aktuelle Map-SHA-256 stimmen mit dem vorigen frisch geladenen 17-Map-Inventar überein. Dessen Map Checks 0/0 sind **vorherige Prüfergebnisse**, kein neu behaupteter Gameplaytest dieses Auftrags.
- GitHub-LFS-Verfügbarkeit geprüft und **alle 16 versionierten Mapdateien tatsächlich per Datenstrom heruntergeladen und SHA-256-/größenverifiziert**, ohne Dateikopien zu speichern.

Die erste eigene Registry-Abfrage stoppte an einer in UE 5.8 nicht vorhandenen AssetData-Python-Methode. Die korrigierte Abfrage verwendet PackageName/AssetName; alle 17 Map-Einträge sind vorhanden. TopLevelAssetPath wurde anhand seiner Felder normalisiert, nicht über eine ungeeignete Anzeigezeichenfolge als angeblich leere World-Liste ausgewertet. Keine Map-/Assetänderung oder verworfenen fremden Editorzustände dadurch.

Grenzen: Registry-Referenzen erfassen keine beliebigen C++-Strings, externen Skripte oder künftigen Spielstände. Auch gleiche Mesh-/Materialmengen beweisen keine identischen Actor-Eigenschaften. Es gibt **keine bytegleichen Mapdateien** in diesem Bestand; keine Map wird als exakte Dublette bezeichnet.

## 3. Vollständiges Mapinventar

Vollständige Unreal-Paketpfade; der zugehörige vollständige Objektpfad ist jeweils `Paketpfad.Mapname`. Absolute Dateipfade, Objektpfade, SHA-256, Git-/LFS-Status und ungekürzte letzte Commits stehen zusätzlich in [UNREAL_MAP_CLEANUP_V1_INVENTAR.csv](UNREAL_MAP_CLEANUP_V1_INVENTAR.csv).

| Vollständiger Paketpfad | Dateigröße Bytes | Git-Status vor Analyse | Letzter Datei-Commit / Datum | Kategorie |
|---|---:|---|---|---|
| `/Game/Maps/Dev_BattleTestMap` | 8.758 | versioniert, sauber | `1ea1bf6` · 2026-09-17 | B |
| `/Game/Maps/Dev_BuildingKitTestMap` | 887.279 | versioniert, sauber | `3d48cea` · 2026-10-03 | A |
| `/Game/Maps/Dev_HealingHouseTestMap` | 1.267.168 | versioniert, sauber | `eafab5b` · 2026-10-05 | A |
| `/Game/Maps/Dev_TestMap` | 1.340.593 | versioniert, sauber | `155bbb8` · 2026-09-28 | A |
| `/Game/Maps/Dev_TestMap_EnvironmentPerfV1` | 3.286.151 | versioniert, sauber | `09e8c69` · 2026-10-17 | B |
| `/Game/Maps/Dev_TestMap_EnvironmentPerfV2` | 3.287.914 | versioniert, sauber | `09e8c69` · 2026-10-17 | B |
| `/Game/Maps/Dev_TestMap_EnvironmentPerfV3` | 3.289.600 | versioniert, sauber | `09e8c69` · 2026-10-17 | B |
| `/Game/Maps/Dev_TestMap_NPCMotionV2` | 3.272.719 | versioniert, sauber | `09e8c69` · 2026-10-17 | B |
| `/Game/Maps/Dev_TestMap_NPCMotionV3` | 3.277.969 | versioniert, sauber | `09e8c69` · 2026-10-17 | A |
| `/Game/Maps/Dev_TestMap_RangerPerfV2` | 3.270.772 | versioniert, sauber | `09e8c69` · 2026-10-17 | B |
| `/Game/Maps/Dev_TestMap_TreeShadowProxyV1` | 3.298.760 | versioniert, sauber | `09e8c69` · 2026-10-17 | B |
| `/Game/Maps/Dev_TestMap_VisualV2` | 3.724.794 | versioniert, sauber | `16f1904` · 2026-10-19 | A |
| `/Game/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1` | 3.314.086 | **?? unversioniert** | kein Commit | A |
| `/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1` | 3.300.685 | versioniert, sauber | `70e98f6` · 2026-10-18 | A |
| `/Game/Maps/Dev_WestlandAssetLibrary` | 246.335 | versioniert, sauber | `8c3ea2d` · 2026-10-11 | A |
| `/Game/Maps/Dev_WestlandRegion` | 11.869.648 | versioniert, sauber | `89b475e` · 2026-10-10 | A |
| `/Game/Maps/Dev_WestlandVillage` | 3.361.996 | versioniert, sauber | `32bba08` · 2026-10-03 | B |

Die letzte Git-Änderung ist vom ursprünglichen Entwicklungsdatum zu unterscheiden: `09e8c69` nahm mehrere bereits bestehende NPC-/Performance-Ergebnisse gemeinsam in die schlanke Historie auf. Das bedeutet weder, dass alle Varianten an diesem Tag neu gestaltet wurden, noch dass sie freigegeben sind. Die inhaltlichen Versionsstände werden im nächsten Abschnitt getrennt ausgewiesen.

Alle 16 versionierten Mapdateien verwenden korrekt Git LFS, stimmen lokal mit den origin/main-Pointern überein und sind nicht nur als ungeladene Pointerdateien vorhanden. Die unversionierte Map hat zwar ebenfalls die `.umap`-LFS-Regel, aber **noch keinen Git-Commit oder gesicherten Remote-LFS-Stand**; die Regel allein ist keine Sicherung.

## 4. Zweck, Entwicklungsstand und einzigartige Inhalte je Map

| Map | Inhaltlicher Stand / ursprünglicher Zweck / Eigenständigkeit | Aktuelle Verwendung |
|---|---|---|
| `Dev_BattleTestMap` | Battle-UI-Test V1: Isoliertes Teamkampf-UI; eigener PokeMonsterBattleTestGameMode, kein normaler Overworld-Pawn. | Nicht als Startmap oder Assetziel verwendet; eigenständig manuell nutzbar. |
| `Dev_BuildingKitTestMap` | Westland Inn V1 / Building Kit: Kit-Prüfszene mit Wohnhaus-/L-Gasthaus-Cutaway; zwei nur hier unter den Maps verwendete Modulassets. | Direkte LoadObject-Fixture zweier C++-Tests; Architektur-/Innenkamera-Prüfung. |
| `Dev_HealingHouseTestMap` | Healing House Art Quality V3: Originale Expanded-Interior-/Heilhaus-Fixture mit eigener Heilerin/Checkpoint-Konfiguration. | Direkte LoadObject-Fixture in HealingHouseTest.cpp; ScaleCalibration prüft den passenden PIE-Kontext. |
| `Dev_TestMap` | Eight-direction overworld layout: Ursprünglicher Gameplaykern mit Interaktionsziel, Dialog, Liora, Wildbegegnung, Ruhepunkt und Archivziel. | Aktuelle EditorStartupMap UND GameDefaultMap; spezielle Checkpoint-Behandlung; Regressionstestbasis. |
| `Dev_TestMap_EnvironmentPerfV1` | Environment Performance V1: Alter VisualV2-Weltstand plus PokeMonsterEnvironmentRenderProfile. | Historische A/B-/Fußlaufwerkzeuge und direkte Baseline von EnvironmentPerfV2. |
| `Dev_TestMap_EnvironmentPerfV2` | Environment Performance V2: Alternative Lumen-Auswertung; geerbtes V1-Profil plus eigenes V2-Profil. | Direkte Baseline von EnvironmentPerfV3; historische Replays. |
| `Dev_TestMap_EnvironmentPerfV3` | Environment Performance V3: V2-Kontrollzustand mit zusätzlichem V3-Profil; keine freigegebene neue Vegetationsoptimierung. | Separater Prüf-/Replaystand; aktuelle zentrale Welt nicht darauf angewiesen. |
| `Dev_TestMap_NPCMotionV2` | Ranger Animation Quality V2: V2-Darstellung/Preview des Wanderers, geerbte deaktivierte Previewdaten teilweise in V3 erhalten. | Physische Vergleichsbaseline von RangerAnimationV3/FinalMapAudit.py und Quelle von CreateMap.py. |
| `Dev_TestMap_NPCMotionV3` | Ranger Animation Quality V3: Aktuelle isolierte Ranger-Beinmechanik-/Turn-/Talk-Prüfszene; sieben nur hier unter den Maps referenzierte V3-Pakete. | Aktuelle noch nicht final freigegebene NPC-Arbeitsgrundlage und Projektwartungs-Mapprüfung. |
| `Dev_TestMap_RangerPerfV2` | Ranger Performance V2: V2-Clean-/LOD-Kandidaten am Wanderer; eigenständiger Geometrie-/Materialvergleich. | Historische Ranger-Performance-/FootTest-Werkzeuge; Clean-Mesh nur in dieser Mapreferenzkette. |
| `Dev_TestMap_TreeShadowProxyV1` | Tree Shadow Proxy V1: Begrenzte Proxy-Baumgruppe und Hilfsdarstellung für Schatten-/Hangversuche. | Nur spezieller Shadow-Proxy-Replay; kein freigegebener Standard der VisualV2. |
| `Dev_TestMap_VisualV2` | World Art V7; TAA / Materialfix / Heilhaus V4: Zentrale Gameplay-/Art-Referenz mit eigenständigen V4-V7-Assets und bestehendem Wanderer V1. | Zentrale aktive Referenz; viele Art-/Gameplay-/AA-Werkzeuge; aktueller Save nennt diese Map. |
| `Dev_TestMap_VisualV2EnvironmentQualityV1` | VisualV2 Environment Quality V1; unversioniert: Ältere VisualV2-Szenenkopie für isolierte Postprocess-Vergleiche; kein exklusives Paket in der Registry-Kette. | Unversionierte fremde Map, neun eigene Tooldateien plus fremde Verweise; kein verlässlicher GitHub-Wiederherstellungspunkt. |
| `Dev_TestMap_VisualV2GPUBottleneckV1` | VisualV2 GPU Bottleneck V1: Vorhandene allgemeine GPU-/Material-/AA-/Shadow-Diagnoseumgebung auf älterem Weltstand. | Mehrere native C++-Diagnose-Guards und 72 exakt referenzierende Tooldateien; Kandidat für eine einzige künftige Diagnosemap. |
| `Dev_WestlandAssetLibrary` | Westland Asset Library Art Quality V3: Objekt-/Materialreview V1-V3 mit eigenständigen Assetvarianten und Beispielszenen. | Ausdrücklich geschützte Asset-Testkarte; Import-/Validierungs-/Reviewwerkzeuge. |
| `Dev_WestlandRegion` | Playable Westland Region V1: Große zusammenhängende Region mit Terrain, Wegen, Fluss, Gebäuden und eigenen Dialog-/Landmarkdaten. | Ausdrücklich geschützte Regionsreferenz und Erkundungs-/Save-/Systemtests. |
| `Dev_WestlandVillage` | Westland Village Core V1: Fünf begehbare Kitgebäude, Dorfwegkomposition, fünf Cutaways; eigene Ground-/Path-Meshes und Wegmaterial. | Eigenständige manuelle Architektur-/Dorfprüfung und Autoren-/PIE-Validierung, keine Default- oder C++-LoadObject-Fixture. |

„Aktuell verwendet“ unterscheidet automatische Start-/Testabhängigkeit, noch benötigte Entwicklungswerkzeuge und lediglich archivierte/manuell aufrufbare Experimente. Es wurde nicht behauptet, alle 17 Maps würden regelmäßig vom Nutzer geöffnet. VisualV2 enthält die eigentlichen Dialog-/Quest-/Kampf-/Fang-/Heilhausfunktionen; die Testmaps sind dennoch nicht allein dadurch vollständig ersetzt.

Einzigartigkeit umfasst auch die **Szenenkonfiguration**: Der Battle-GameMode, Profilactor-Werte, Platzierungen und Preview-Zuordnungen können im Level gespeichert sein, obwohl sämtliche referenzierten Assetdateien auch anderswo vorkommen. Keine exklusiven Registry-Assets ist daher kein Löschbeweis.

## 5. Tatsächliche Abhängigkeiten und Verwendung

### 5.1 Assetreferenzen und Level-Abhängigkeiten

Für **jede** der 17 Maps: keine eingehenden Hard-, Soft-, Searchable- oder Management-Referenzen in der gescannten Registry. Keine andere Map muss laut diesem Paketgraphen als Streaming-/Sublevel mitgeladen werden. Das gilt nur für die erfassten Assetreferenzen, nicht für dynamisch zusammengesetzte Levelnamen.

Die transitive Abhängigkeitsprüfung umfasst insgesamt **611 `/Game`-Pakete**, darunter die unversionierte Map. **610 versionierte Pakete** stimmen vollständig mit origin/main überein. Keine fehlende lokale Paketdatei gefunden. Für alle 610 zugehörigen LFS-Objekte mit **237.179.692 Bytes** bestätigte der Server die Downloadverfügbarkeit. Die davon tatsächlichen Mapdownloads betragen **48.991.141 Bytes**, SHA-256-verifiziert; die übrigen Dependency-Nutzdaten wurden lokal gehasht und serverseitig auf Verfügbarkeit geprüft, nicht zusätzlich vollständig heruntergeladen.

Beispiele von Assets, die innerhalb der 17 Map-Abhängigkeitsketten nur an einer bestimmten Map hängen:

- NPCMotionV3: fünf V3-Animationen, `SK_Ranger_AQV3` und sein Skeleton.
- RangerPerfV2: `SK_Ranger_NPC_V2_Clean`.
- TreeShadowProxyV1: `M_TSP_OpaqueShadow`, `SM_TSP_OakAncient_Bark`, `SM_TSP_OakAncient_Crown`.
- WestlandVillage: `M_WV_Path`, `SM_WV_Ground`, `SM_WV_Paths`.
- BuildingKit: `SM_WL_WallSolid1m` und `SM_WL_WindowRound`.

Diese Dateien werden **nicht** als zusätzliche Löschkandidaten behandelt. Eine spätere Mapentfernung ist keine Freigabe zur Orphan-/Assetbereinigung. Blenderquellen, Exportdateien, Materialien, Skeletons, Animationen, Autorenpläne und wichtige Prüfberichte bleiben erhalten.

### 5.2 Startkonfiguration und Gameplay

`Config/DefaultEngine.ini:4-5` setzt sowohl `EditorStartupMap` als auch `GameDefaultMap` auf **Dev_TestMap**. Die zentrale Art-Referenz heißt VisualV2; die Projekt-Startkonfiguration ist dennoch noch nicht dorthin umgestellt.

`Source/PokeMonster/Checkpoint/PokeMonsterCheckpointSubsystem.cpp:100` behandelt Dev_TestMap besonders; `:158` kann einen Level aus dem gespeicherten Checkpointnamen öffnen. Eine reine Registry-Abfrage würde diese Verwendung nicht erkennen. Ein nicht deserialisierender Tokencheck des vorhandenen `Saved/SaveGames/PokeMonster_Dev.sav` fand den exakten Mapnamen **Dev_TestMap_VisualV2**; dies ist kein vollständiger Save-Kompatibilitätstest aller früheren Spielstände.

Für eine spätere Entfernung von Dev_TestMap wären Defaultmap, Checkpointfälle, Regressionstests und ältere Spielstände gesondert zu prüfen. **Das ist kein Bestandteil dieser Löschkandidatenliste.**

### 5.3 Physisch geladene C++-Testfixtures

- `Source/PokeMonster/Tests/PokeMonsterBuildingCameraTest.cpp:143` lädt **Dev_BuildingKitTestMap** per `LoadObject<UWorld>`.
- `Source/PokeMonster/Tests/PokeMonsterInnCameraTest.cpp:37` lädt dieselbe Map und prüft das gespeicherte Gasthaus.
- `Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp:38`, `:258`, `:399` lädt **Dev_HealingHouseTestMap**; `:443` prüft deren gespeicherte Checkpoint-Mapidentität.
- `Source/PokeMonster/Tests/PokeMonsterScaleCalibrationTest.cpp:73`, `:117` prüft den PIE-Kontext der Heilhausmap.

Diese beiden Karten sind deshalb A. Tests einfach auf „Map fehlt: überspringen“ zu ändern wäre **keine** gleichwertige Ablösung. Eine spätere Fixture-Umstellung muss gespeicherte Gebäude-/Innenraum-/Cutaway-/Collision-Eigenschaften gleichwertig prüfen.

Die drei Environment-Profiltests sind dagegen überwiegend **Namens-/Opt-in-Guardtests**: `PokeMonsterEnvironmentRenderProfileTest.cpp`, `PokeMonsterEnvironmentProfileV2Test.cpp`, `PokeMonsterEnvironmentProfileV3Test.cpp`. Sie laden die genannten Performance-/Rangerkarten nicht. Deren Entfernung allein erfordert daher nicht automatisch eine Abschwächung dieser Tests. Guards gegen versehentliche Aktivierung auf normalen Maps bleiben sinnvoll.

### 5.4 Direkte Tool-Baselines und zusammengesetzte Namen

- `Tools/RangerAnimationV3/FinalMapAudit.py:5` lädt **NPCMotionV2** als Vergleichsbasis. `CreateMap.py` benutzt V2 als Quelle. Eine V2-Mapentfernung braucht einen neuen, geprüften Vergleichsvertrag, z. B. unveränderliche erforderliche Szenensignaturen aus dem gesicherten Stand.
- `Tools/EnvironmentPerfV2/FinalMapAudit.py` benutzt **EnvironmentPerfV1** als physische Baseline; auch `CreateTestMap.py` baut darauf auf.
- `Tools/EnvironmentPerfV3/FinalMapAudit.py:5` benutzt **EnvironmentPerfV2**; `CompareAndCopy.py` ebenfalls als Quelle.
- `Tools/EnvironmentPerfV3/RunBaselineReviews.py:7-12` setzt Levelnamen aus `Dev_TestMap_` und den Aliasen VisualV2/EnvironmentPerfV1/V2/V3 zusammen. Eine Suche nur nach vollständigen Mapstrings wäre unvollständig.
- `Tools/PerformanceRangerV2/{LoadPerfMap,FinalMapAudit,FootTestV2}.py`, Ranger-V2-Loader, die Environment-Werkzeuggruppen und `Tools/TreeShadowProxyV1/` erwarten ihre jeweiligen Szenen.
- `Tools/BuildWestlandVillageV1.py`, `ValidateWestlandVillageV1.py`, `TestWestlandVillageV1PIE.py` enthalten den spezifischen Dorfaufbau und Rundweg. Der begehbare Fünf-Gebäude-Test ist nicht durch die bloße Existenz eines einzelnen VisualV2-Wohnhauses ersetzt.
- Die GPU-Diagnosemap ist in `PokeMonsterEnvironmentPerformanceProbeV2.cpp`, `PokeMonsterSoftShadowTest.cpp` und `PokeMonsterTAAReviewCapture.cpp` explizit zugelassen; 72 Tooldateien referenzieren ihren exakten Namen. Sie sollte als **eine vorhandene gemeinsame Diagnosemap** erhalten bleiben, statt mehrere neue Testmaps zu erzeugen.

Die vollständige prüfbare Übersicht der konkreten Quell-/Tool-/Manifestdateien und Zeilennummern steht in [UNREAL_MAP_CLEANUP_V1_ABHAENGIGKEITEN.csv](UNREAL_MAP_CLEANUP_V1_ABHAENGIGKEITEN.csv), **680 zusammengefasste Referenzzeilen**. Texttreffer sind dort ausdrücklich als Kandidaten eingeordnet: README-Text, historisches Review-JSON oder C++-Kommentar sind nicht automatisch operative Ladereferenzen. Generische Map-Launcher benötigen vor allem korrekte Aufrufer/Zielnamen, nicht die pauschale Entfernung ihrer Funktion.

### 5.5 Pflichtdatei-Manifest – Hindernis für alle versionierten Löschkandidaten

**Alle 16 versionierten Maps** stehen in `Tools/DevelopmentEvidence/CoreFiles.json`, jeweils mit aktueller passender Dateigröße und SHA-256. `Tools/DevelopmentEvidence/evidence.py:51-58`, Befehl `validate-core`, meldet jede fehlende Pflichtdatei als Fehler. Die Map-spezifischen Einträge wurden direkt gegen die tatsächlichen Dateien geprüft.

Vor jeder späteren Mapentfernung muss eine **neue fachlich geprüfte Pflichtdateiliste** entstehen: noch erforderliche Maps streng validieren, entfallene Szenen nicht mehr als installierte Pflichtdatei verlangen, historische Referenzen an ihren Wiederherstellungspunkt binden. Nicht einfach fehlende Dateien global ignorieren. `test_evidence.py` muss weiter nachweisen, dass tatsächlich erforderliche Dateien bei Fehlen oder Änderung fehlschlagen.

Autoren-/Reviewmanifeste unter Art und historische Berichte dürfen ihre alten Namen als Herkunftsnachweis behalten. Ausführbare Werkzeuge dürfen bei fehlenden optionalen historischen Maps klar „nicht ausgeführt / Wiederherstellung erforderlich“ melden; dies darf nicht als bestandener Test ausgegeben werden. Erforderliche aktuelle Baselines müssen weiterhin vorhanden sein.

## 6. Konkrete bedingte Löschliste – ausschließlich Kategorie B

**Dies ist eine Kandidatenliste zur späteren Freigabe, kein ausführbarer Löschauftrag. C ist leer.** Zusätzlich zu den individuellen Voraussetzungen gelten für jede Zeile: Core-Manifest umstellen, benötigte Szenen-/Prüfdaten und ursprünglichen Git-/LFS-Stand erhalten, Nutzerfreigabe und vollständige Prüfung nach der Änderung.

Vollständige Objektpfade; die CSV-Anlage enthält zusätzlich absolute Dateipfade und aktuelle Prüfsummen. Keine Assets neben der Map mitlöschen.

| Vollständiger Assetpfad | Mapgröße MiB | Vor einer Entfernung notwendig |
|---|---:|---|
| `/Game/Maps/Dev_BattleTestMap.Dev_BattleTestMap` | 0,008 | Battle-UI-Replay auf einer vorhandenen Testmap nachweislich ersetzen oder bewusst aufgeben; Pflichtmanifest neu prüfen. |
| `/Game/Maps/Dev_TestMap_EnvironmentPerfV1.Dev_TestMap_EnvironmentPerfV1` | 3,134 | V2-FinalMapAudit/CreateTestMap von der physischen V1-Fixture lösen; V1-Replay und Pflichtmanifest sauber archivieren/umstellen. |
| `/Game/Maps/Dev_TestMap_EnvironmentPerfV2.Dev_TestMap_EnvironmentPerfV2` | 3,136 | EnvironmentPerfV3/FinalMapAudit.py und CompareAndCopy.py von V2 lösen; historische Beleuchtungsvariante reproduzierbar dokumentiert lassen. |
| `/Game/Maps/Dev_TestMap_EnvironmentPerfV3.Dev_TestMap_EnvironmentPerfV3` | 3,137 | V3-Loader, Fußlauf, GPU-/Review- und Persistenzwerkzeuge explizit stilllegen oder auf gemeinsame Testumgebung umstellen; Manifest anpassen. |
| `/Game/Maps/Dev_TestMap_NPCMotionV2.Dev_TestMap_NPCMotionV2` | 3,121 | V3-Audit auf eingefrorene erforderliche Vergleichsdaten umstellen und erneut prüfen; V2-Rig-/Animationsassets und Quellen erhalten. |
| `/Game/Maps/Dev_TestMap_RangerPerfV2.Dev_TestMap_RangerPerfV2` | 3,119 | PerformanceRangerV2-Loader/Audits/FootTest auf Wiederherstellungs- oder gemeinsame Diagnosebasis umstellen; Clean-/LOD-Assets ausdrücklich erhalten. |
| `/Game/Maps/Dev_TestMap_TreeShadowProxyV1.Dev_TestMap_TreeShadowProxyV1` | 3,146 | Proxy-Vergleich und Hang-/Windprüfung als optionales Replay kennzeichnen; drei Proxy-Assets und Quellen behalten; Pflichtmanifest anpassen. |
| `/Game/Maps/Dev_WestlandVillage.Dev_WestlandVillage` | 3,206 | Gebäude-/Cutaway-Prüfumfang auf BuildingKit/VisualV2 nachweisen; Village-Bauplan/Assets bewahren, Tools und Manifest anpassen. |

Maschinenlesbar: [UNREAL_MAP_CLEANUP_V1_LOESCHKANDIDATEN.csv](UNREAL_MAP_CLEANUP_V1_LOESCHKANDIDATEN.csv). Alle acht Zeilen sind mit **„Jetzt löschen: NEIN“** gekennzeichnet. Die geschützte unversionierte Map ist ausdrücklich **nicht** enthalten.

Die alten Versuchswerkzeuge müssen nicht ersatzlos gelöscht werden: reproduzierbare Autorenwege, Quellparameter und wichtige Messergebnisse bleiben. Für optionale historische Replays klare Voraussetzungen und eine explizite Wiederherstellung angeben. Keine neue Projektkopie oder Map zur Migration vorsehen; vorhandene Testumgebungen verwenden.

## 7. Sinnvolle Reihenfolge und langfristiger Kartenbestand

### Langfristige acht reguläre Maps

1. **Dev_TestMap_VisualV2** – zentrale spielbare Art-/Gameplaywelt.
2. **Dev_WestlandRegion** – eigenständige Regions-/Erkundungsreferenz.
3. **Dev_WestlandAssetLibrary** – gemeinsame grafische Einzelassetprüfung.
4. **Dev_TestMap** – vorerst stabile Start-/Gameplay-Regressionsfixture.
5. **Dev_BuildingKitTestMap** – gespeicherte Gebäude-/Innenkamera-/Gasthausfixture.
6. **Dev_HealingHouseTestMap** – Heilhaus-/Innenraum-/Checkpointfixture.
7. **Dev_TestMap_NPCMotionV3** – aktuelle noch offene Referenz für Wanderer-Bewegung.
8. **Dev_TestMap_VisualV2GPUBottleneckV1** – eine wiederverwendbare Diagnoseumgebung für zukünftige Grafiktests; keine neuen Maps.

Die unversionierte **Dev_TestMap_VisualV2EnvironmentQualityV1 bleibt zusätzlich geschützt**, bis ihre Eigentümerschaft, noch nötigen Werkzeuge und Wiederherstellbarkeit unabhängig geklärt sind. Dieser Bericht nimmt sie nicht stillschweigend in Git auf und setzt sie nicht zurück.

### Vorgeschlagene spätere Arbeitspakete – noch nicht ausgeführt

**P1 – fünf Versionstestkarten:** EnvironmentPerfV1/V2/V3, NPCMotionV2 und RangerPerfV2. Zuerst die physischen Baseline-Ketten lösen, vorhandene Beweisdaten/Parameter erhalten und die nötigen Prüffunktionen auf verbleibenden Testumgebungen demonstrieren. Danach Core-Manifest und Launcher prüfen. Erst anschließend um Freigabe für genau diese fünf Mapdateien bitten.

**P2 – drei spezielle Szenen:** Village, TreeShadowProxy und BattleTest. Deren eigenständige Szenen-/Funktionswerte bewusst bewerten. Village erst nach gleichwertiger Gebäudeprüfung; TreeShadowProxy nach Klarstellung des optionalen Replays; BattleTest erst nach belegtem Ersatz des isolierten Battle-UI-Prüfwegs. Ohne diesen Ersatz bleibt die jeweilige Karte erhalten, auch wenn dann mehr als acht Maps nötig sind.

**P3 – unversionierte Schutzposition:** getrennte Entscheidung, keine automatische Bereinigung. Ein gleicher historischer Zweck oder dieselbe Menge referenzierter Assets genügt nicht als Beweis vollständiger Dublettengleichheit.

Ein ferneres Minimum von drei Maps ist derzeit **nicht sinnvoll belegt**: Es würde Default-/Regressionstestfixtures, isolierte Gebäudetests und noch offene NPC-/Diagnoseabläufe verdrängen. Eine solche Konsolidierung wäre ein eigener Testarchitekturauftrag mit echter Ersatzabdeckung.

## 8. GitHub-Sicherung und Wiederherstellung

Für jede versionierte Map gilt:

- Vollständige aktuelle Datei im `origin/main`-Baum unter Ausgangscommit `ce450f4bb7e105efd54bd5512a1b47766c045c63` gefunden.
- LFS-Pointergröße und OID entsprechen der tatsächlichen lokalen Datei.
- Remote-Payload einzeln gestreamt, Bytezahl und SHA-256 identisch; keine neuen Payloaddateien oder Backups gespeichert.
- Die nötigen `/Game`-Abhängigkeiten sind lokal vorhanden, versioniert und serverseitig verfügbar. Source, Config und benutzte native Klassen müssen zusammen mit diesem Git-Stand erhalten bleiben; passende Unreal-/Pluginversion gehört zur Wiederherstellungsumgebung.

Die Inventar-CSV enthält den exakten aktuellen Dateihash, den vollständigen letzten Datei-Commit und den LFS-OID. Der gemeinsame geprüfte Wiederherstellungspunkt ist der oben genannte origin/main-Commit. Ein späterer normaler Löschcommit würde frühere Commits nicht entfernen. **Git-Objekttext allein liefert bei LFS nur einen Pointer; Wiederherstellung benötigt außerdem den zugehörigen LFS-Payload.**

Die Übertragbarkeit aller Mapbytes wurde geprüft, aber **kein vollständiger historischer Restore/Reimport oder Build in einer separaten Projektkopie** durchgeführt. Das wäre hier weder nötig noch ohne Zustimmung zulässig. Eine künftig wiederhergestellte historische Map wäre vor Benutzung auf aktuelle native Klassen/Assets und Map Check zu prüfen.

Unversionierte Map: nicht im origin/main-Baum vorhanden, kein belastbarer GitHub-Wiederherstellungsnachweis. Ein künftiger Commit müsste eigens geprüft/freigegeben werden. Bis dahin A-Schutzposition.

Das Vollbackup `03492bd` bleibt unverändert unter Branch-/Archivref lokal erreichbar und wird nicht in die Remote-Historie aufgenommen. Kein LFS-Prune, keine Historiensäuberung, keine neuen Branches oder Worktrees.

## 9. Größen und tatsächlicher Nutzen

| Bestand / Kandidaten | Bytes | MiB, gerundet |
|---|---:|---:|
| Alle 17 Mapdateien | 52.305.227 | 49,88 |
| Davon 16 versioniert | 48.991.141 | 46,72 |
| Unversionierte Schutzposition | 3.314.086 | 3,16 |
| Acht bedingte B-Kandidaten zusammen | **23.076.670** | **22,01** |

Dies sind logische Dateigrößen, **kein gemessener freier APFS-Speicher**. Heute wurde nichts freigegeben. Eine spätere Mapentfernung würde weder Texturen/Modelle noch Git-/LFS-Historie entfernen. Deshalb keine entsprechende GitHub-LFS-Kosteneinsparung oder große lokale Speicherfreigabe versprechen. Der Nutzen wäre vor allem eine übersichtlichere Mapauswahl und ein klarerer Testablauf.

## 10. Prüfstatus, Schutz und Stopp

- Maps vollständig inventarisiert: 17/17; keine neue Map, kein Reimport, keine Referenzänderung.
- Frische Asset Registry: 17 Map-Einträge, keine eingehenden Paketreferenzen in den vier geprüften Kategorien; transitive Abhängigkeiten und mapexklusive Assetbeispiele ermittelt.
- Startmap-/C++-/Test-/Tool-/Manifest-Abhängigkeiten gelesen und unterschieden; dynamischer Namensaufbau ausdrücklich berücksichtigt.
- 16/16 aktuelle Mapdateien auf GitHub SHA-256-verifiziert; 610 zugehörige versionierte LFS-Pakete serverseitig verfügbar, lokale Inhalte stimmen überein. Keine fehlenden Runtime-Paketdateien gefunden.
- Alle 16 Map-Einträge des Pflichtmanifests entsprechen den aktuellen Mapdateien. Vollständiger Core-Validator/Projektbuild/Automation/Gameplay wurden in diesem **reinen Analyseauftrag nicht neu ausgeführt**; keine neuen Erfolge dafür behauptet.
- Vorherige Map Checks und Quellenverifikation bleiben Herkunftsnachweise; heute keine neuen Screenshots, Benchmarks oder zusätzliche Projekte erzeugt.
- Bestehende versionierte und unversionierte Projektdateien werden vor dem Berichtscommit erneut vollständig gegen die Vorher-Prüfsummen verglichen. Von diesem Auftrag neu erzeugt werden ausschließlich dieser Bericht und seine drei erforderlichen CSV-Anlagen. Die ignorierten eigenen Analyseprotokolle liegen unter `Saved/MapCleanupV1_*`.

Nach bestandener Dokument-/Dateischutzprüfung wird ausschließlich das Dokumentationspaket gezielt auf `main` committed und regulär gepusht; Remote, Commitpfade, LFS-Status und Backup-Refs werden kontrolliert. Tatsächlicher neuer Commit-Hash folgt in der Abschlussantwort. Keine Kontrollmedien, Caches, Builds oder temporären Editorprotokolle in Git.

**Stopp nach Analyse und GitHub-Sicherung dieses Berichts. Eine spätere Kartenentfernung oder Abhängigkeitsänderung benötigt Harrys ausdrückliche Freigabe.**
