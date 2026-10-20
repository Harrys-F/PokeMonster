# Kreaturen-Pipeline V2 – Prüfbericht

Stand: 20.10.2026. Aktives Projekt ausschließlich `/Users/harry/Developer/PokeMonster`, Branch `main`. Ausgangsstand `0a09c6883f3eff7e31a89226116d51e030fcce5a`, vor Beginn direkt mit `origin/main` abgeglichen. Unreal 5.8.2, Blender 5.2.2 LTS, macOS.

## Ergebnis

Die Zunderlauf-Grundlage wurde um einen wiederverwendbaren Importvertrag, einen sicheren Darstellungswechsel, allgemeine Effekt-Anker und lesende Prüfwerkzeuge ergänzt. Der spätere Austausch durch das Nutzer-Meshy-Glumanda ist konkret dokumentiert. **Kein Modell wurde erzeugt oder ersetzt.** Die bestehenden Zunderlauf-Quellen, Animationen und Unreal-Assets sowie alle elf Maps sind unverändert.

Die Vorbereitung ist für schrittweise, einzeln geprüfte Imports nutzbar. Ein automatischer Import beziehungsweise eine automatische Rigging-Freigabe aller 251 Arten wurde nicht implementiert oder behauptet. Das endgültige Meshy-Glumanda fehlt weiterhin und ist im Plan ausdrücklich als fehlend markiert.

Vollständiger Ablauf: [KREATUREN_PIPELINE_V2.md](KREATUREN_PIPELINE_V2.md). Werkzeuge: `Tools/CreaturePipelineV2/`.

## 1. Tatsächlicher Bestand

Die lesende Asset-Registry-Inventur fand vier Spezies:

| Art-Asset | InternalId | Bisherige Prototypnummer | Darstellung |
|---|---|---:|---|
| `/Game/Data/Creatures/DA_TestGrass` | TestGrass | 1001 | vorhandener 2D-Fallback |
| `/Game/Data/Creatures/DA_TestWater` | TestWater | 1003 | vorhandener 2D-Fallback |
| `/Game/Data/Creatures/DA_TestFire` | TestFire | 1002 | vorhandener 2D-Fallback |
| `/Game/Data/Creatures/DA_Zunderlauf` | Zunderlauf | 1002 | bestehendes Skeletal Mesh, eigenes Skeleton, sieben Clips |

Die Nummern sind technische Prototypwerte; die doppelte 1002 ist kein neu erfundener nationaler Pokédex. Keine Kreaturen-Blueprint-Assets wurden gefunden. Die bestehende Architektur arbeitet nativ mit `UPokeMonsterCreatureSpeciesData`, `FPokeMonsterCreatureInstance`, Encounter-, BattleSession-, Capture-, Team-, Heil- und Save-Systemen. `Visuals.Presentation` ist eine optionale visuelle Referenz. Ein vollständiger 251er-Daten-/Größenkatalog liegt nicht vor.

Vier bestehende unversionierte GLB-Originale wurden ausschließlich lesend erfasst: Enton, Glurak, Myrapla und Pikachu. Ihre Namen wurden nicht als Designfreigabe oder neue Spielzuordnung verwendet. Das endgültige Glumanda ist darunter nicht vorhanden. Alle vier Originale sind unverändert und weiterhin unversioniert.

Die erste Python-Inventur löste eine weiche Assetreferenz nicht korrekt auf. Dies wurde am Werkzeug korrigiert; die finale Inventur bestätigt das reale Zunderlauf-Profil, dessen Skeleton und alle sieben Sequenzen. Es wurde kein vermeintlich fehlendes Asset neu erstellt.

## 2. Sichere Codeverbesserungen

Geändert wurden ausschließlich `PokeMonsterCreaturePresentation.h/.cpp`; neue Prüfungen in `Source/PokeMonster/Tests/PokeMonsterCreaturePipelineTest.cpp`. Kampf-, Fang-, Team-, Heil- und Save-Implementierungen wurden nicht geändert.

- `GetValidationErrors()` ist als Blueprint-/Editor-Prüfung verfügbar. Es prüft Mesh/Skeleton, Materialslots, notwendiges Idle, vorhandene Cliprollen, exakte Skeletonzuordnung, positive Dauer, deaktivierte Root-Motion-Extraktion, Geschwindigkeiten, Bodenoffset, Größenherkunft und Effekt-Anker.
- `SetSpecies` prüft einen Kandidaten vor der Änderung. Ein ungültiger Kandidat lässt die bisher funktionierende Darstellung bestehen. Bei erfolgreichem Wechsel werden alte allgemeine Effekte entfernt und die Geschwindigkeitsmessung neu begonnen.
- `RigFamily` unterstützt als Metadatum Custom, Biped, Quadruped, Serpentine, Winged, Aquatic und Floating. Kein Modell wird deshalb auf ein humanoides Rig oder eine gemeinsame Bone-Hierarchie gezwungen.
- `ReferenceSizeCm` und `SizeSource` dokumentieren belegte Größen. Sie skalieren keine bestehenden Assets automatisch.
- `EffectAnchors` erlaubt einfache Mesh-Effekte an rigabhängigen Bones/Sockets, mit lokalem Offset und optional weltaufrechter Rotation. Eindeutige IDs, existierende Anker, gültige Transformationen und doppelte Legacy-Flammen werden geprüft. Komponenten bleiben kollisionsfrei und werfen keine zusätzlichen Schatten.
- Der bestehende Zunderlauf-V1-Schwanzflammenpfad bleibt unterstützt; bestehende Präsentationsassets wurden nicht migriert oder gespeichert. Andere Rigs brauchen weder Schwanz noch `tail_socket`.

Die neue Testreihe bindet tatsächlich vorübergehend ein anderes vorhandenes Skeleton samt eigener Idle-Sequenz in einer transienten Testwelt. Die Rangerquelle wird dabei nicht verändert oder als Pokémon importiert. Dieser Strukturtest ersetzt keine Bewegungs-/Verformungsabnahme zukünftiger Vierbeiner, Schlangen oder Flugwesen.

## 3. Importregeln und Werkzeuge

Verbindlich dokumentiert sind Meter in Blender, Zentimeter in Unreal, Blender −Y/+Z und Unreal +X/+Z mit der bestehenden FBX-Konvertierung, einheitlicher Rig-/Mesh-Maßstab, kontrollierte Normalen-/Materialzuweisung, sieben Animationsrollen, in-place Animation und eigene Geschwindigkeiten. Körperlänge und Stehhöhe werden ausdrücklich unterschieden. Die konkrete Root-Trajektorie muss zusätzlich geprüft werden; ein deaktiviertes Root-Motion-Flag allein beweist kein in-place Verhalten.

Glumandas belegtes späteres Ziel ist **60 cm Stehhöhe**, Quelle: [offizieller Pokédex](https://ph.portal-pokemon.com/pokedex/0004/), geprüft 20.10.2026. Die aktuelle V1-Höhe von ca. 65,2 cm und der 140-cm-Spieler bleiben unverändert. Andere Originalgrößen müssen artweise aus vorhandenen bestätigten Daten oder belegten Quellen ergänzt werden; es wurden keine 250 weiteren Maße erfunden.

| Werkzeug | Tatsächliche Funktion / Prüfung |
|---|---|
| `preflight.py` | Lesende Pfad-, SHA-, Größenbasis-, Vollständigkeits- und Überschreibprüfung; keine Assetspeicherung |
| `Glumanda_Pending.json` | Bewusst unvollständiger Intake mit nationaler Nummer 4 und stabiler bestehender Spielidentität; Modell/Quell-Hashes/Exporte fehlen ausdrücklich |
| `InspectBlender.py` | Liest existierende `.blend` oder `.glb` im Hintergrundprozess; berichtet Geometrie, UVs, Materialien, Texturen, Rigs, Actions und Maße; speichert kein Modell |
| `AuditUnreal.py` | Lesende Inventur vorhandener Spezies, visueller Verknüpfungen, Skeletons und Clips |
| `CheckCandidate.py` | Prüft ein explizit benanntes Profil und stabile Art-ID; vollständige Kreaturen benötigen sieben Rollen; keine automatische Referenzänderung |
| `CheckMaps.py` | Lädt ausschließlich vorhandene Maps, führt Map Check aus, kehrt zu VisualV2 zurück; kein Speichern |
| `SmokePIE.py` | Liest tatsächliche Kreaturendarstellung im laufenden PIE; keine Eingaben, Teleports, Kämpfe oder Save-Aktionen |

Die Vorprüfung von `Glumanda_Pending.json` endet korrekt mit **Exit 2, `ready_for_manual_import: false`**. Ein positives Vorprüfungsergebnis wäre später nur die Zulässigkeit des manuellen Imports, keine Künstler- oder Rigging-Freigabe. Die eigentliche universelle Meshy-Importautomatisierung bleibt bis zu realen Kandidaten bewusst unbehauptet; der konkrete Unreal-/Blender-Ablauf ist ausführbar beschrieben und nutzt die vorhandenen Importkonventionen.

Der Blender-Inspektor wurde wirklich an der erhaltenen Zunderlauf-Datei ausgeführt: zwei Mesh-Objekte, 50.192 Dreiecke einschließlich Flamme, 23 Bones, Körperhöhe ca. 0,65245 m. Zusätzlich wurde die vorhandene kleine Enton-GLB rein im Arbeitsspeicher gelesen: ein Mesh, 16.491 Dreiecke. Es entstanden weder ein neues Blender-Modell noch ein FBX oder Unreal-Asset. Beide Quellprüfsummen blieben identisch.

## 4. Späterer Austausch ohne Gameplay-Verlust

Der Save speichert stabile Spezies-/Attacken-IDs und individuelle Zustände, keine Mesh- oder Präsentationspfade. Deshalb bleiben beim späteren Glumanda-Modellwechsel `CreatureSpecies:Zunderlauf`, `/Game/Data/Creatures/DA_Zunderlauf`, Encounter-ID, Seed und sämtliche Instanzdaten erhalten. Die nationale Nummer 4 im Intake ändert die Prototypnummer 1002 nicht automatisch.

Der dokumentierte Ablauf erhält Original-GLB und V1, bereitet eine neue Blenderquelle und eigenständige Kandidatenassets vor, prüft eigenes Rig/Clips/60-cm-Maßstab/Schwanzanker und ändert **erst danach nur `DA_Zunderlauf.Visuals.Presentation`**. Rücknahme wäre die Wiederherstellung dieser einen Referenz auf V1; kein Reset erforderlich. Aktuell wurde diese Referenz nicht geändert.

Die neuen Automationsprüfungen sichern Instanz-ID, Art-Asset, HP, PP, Level, Encounter-/Trainerfortschritt und vorhandene Heilung beim Darstellungswechsel ab. Die bestehende Zunderlauf-Kampf-/Fang-/Heil-/Save-Testreihe läuft unverändert mit. Es gibt keine neue Save-Version und keine neue Spielregel.

## 5. Finale technische Ergebnisse

| Prüfung | Ergebnis | Lokaler Nachweis |
|---|---|---|
| Mac Development Editor Build | erfolgreich, Exit 0 | `Saved/ProjectRefinement/CreaturePipelineV2Build04/Result.json` |
| Vollständige Unreal-Automation | **55/55**, 0 Testwarnungen, 0 Fehler | `Saved/ProjectRefinement/CreaturePipelineV2Automation03/Result.json` |
| Neue Unreal-Tests | ImportContract, AtomicVisualSwap, SaveSurvivesPresentationSwap bestanden | gleiche Automation |
| Neue Python-Vorprüfung | **8/8** bestanden | `Tools/CreaturePipelineV2/test_preflight.py` |
| Bestehende Python-Prüfungen | 8 DevelopmentEvidence + 5 MapLifecycle bestanden | vorhandene Unittest-Suites |
| Map Checks aller elf vorhandenen Maps | **0 Fehler, 0 Warnungen** | `Saved/CreaturePipelineV2/MapCheckResults.json` |
| Kandidatenprüfung gegen unverändertes V1 | bestanden; keine Artzuordnung/Speicherung | `Saved/CreaturePipelineV2/CandidateValidation.json` |
| Reales PIE auf finalem Build | eine bestehende V1-Präsentation, gültiges Profil, unveränderte Schwanzbindung, keine zusätzliche Kollision | `Saved/CreaturePipelineV2/PIESmoke.json` |
| Core-Dateivertrag vor Technikcommit | **3.765** Dateien, keine fehlenden/geänderten Pflichtdateien | `Tools/DevelopmentEvidence/CoreFiles.json` und Prüflauf |
| Quellen, Maps und Nutzerdateien | 11 Map-SHA, 53 ursprüngliche unversionierte Dateien sowie Dev-Save unverändert | `Saved/CreaturePipelineV2/Initial.json` und Abschlussprüfung |

Erste Zwischenbefunde: Zwei C++-TObjectPtr-Zugriffe wurden nach echtem Buildfehler korrigiert. Ein zunächst dupliziertes Animations-Testobjekt verursachte eine Import-Metadaten-Warnung; der Test verwendet nun ein eigenes synthetisches Sequenzobjekt und prüft gezielt die Root-Motion-Fehlermeldung. Die optionale PIE-Inspektion musste auf öffentliche Blueprint-Eigenschaften umgestellt werden; geschützte Actor-Properties wurden nicht zur Umgehung freigegeben. Alle genannten finalen Prüfungen erfolgten nach diesen Korrekturen. Keine Warnung wurde unterdrückt.

Bekannte unveränderte Editor-Startmeldung: das alte `idevice_id`-Hilfsprogramm lässt sich auf diesem Mac nicht ausführen („Bad CPU type“). Finale Automation: keine Testwarnungen. Ein neuer vollständiger Gameplay-Fußlauf, Standalone-/Cook-/Shipping-Test, FPS-Benchmark oder GPU-Profiling wurde in diesem modellunabhängigen Paket nicht ausgeführt. Der kurze reale PIE-Test wird nicht als vollständiger Kampf-/Fang-Fußlauf ausgegeben.

Der Dev-Spielstand hat weiterhin SHA-256 `a0ad009a7b3c6f883d1413b0f96df5b25bc7ab953d0154e29ae50f35ad48bf0a`.

## 6. Schutz und GitHub

Technik-/Werkzeug-/Anleitungscommit: `85a24abb1fc4af925b6e33ab9ed5df72cbfc301e` (`feat: add validated Meshy creature import pipeline`), 16 gezielt geprüfte Pfade. Vollständiger Hash und Remote-Bestätigung: `Saved/CreaturePipelineV2/TechnicalPush.json`. Vor Commit: exakter Indexvergleich, `git diff --cached --check`, Core-/Schutzprüfung. Rund **1.010.386 Bytes geänderte normale Git-Blobs**, nicht die tatsächliche Netzwerk-Packgröße. **Null neue LFS-Objekte**; keine `.uasset`, `.umap`, `.blend`, GLB, FBX, Texturen oder Kontrollmedien wurden geändert oder hochgeladen. LFS-Dry-Run und Status bestätigen keinen neuen LFS-Upload.

Die aktuellen GitHub-Grenzen wurden anhand der offiziellen Dokumentation geprüft: [100-MiB-Einzeldateigrenze](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) und [2-GiB-Pushgrenze](https://docs.github.com/en/get-started/using-git/troubleshooting-the-2-gb-push-limit). Das Paket liegt auch unter der zusätzlichen Projektvorgabe von höchstens 1 GiB neuen normalen Git-Daten pro Push. Keine Käufe, Budgetänderungen, Force-Pushes oder neuen Kontingentverbrauch durch LFS-Dateien.

Dieser Prüfbericht und sein einziger neuer Core-Eintrag werden separat dokumentarisch gesichert. Der endgültige Dokumentationshash steht in der Abschlussausgabe. Nach beiden Pushes werden main/origin/main, Git-Status und LFS-Status erneut geprüft.

Das Vollbackup `03492bd96b4dba44692f675c19d5f11abfa86b4b` bleibt unter beiden vorhandenen lokalen Referenzen unverändert und außerhalb der main-Historie. Keine neue Map, Projektkopie, Worktree oder vollständige lokale Sicherung. Keine Bereinigung, keine Änderung an Gameplay, Heilhaus, Landschaft, Beleuchtung oder Kamera. Die 53 geschützten unversionierten Dateien bleiben bewusst unversioniert; „sauber“ bezeichnet den versionierten Arbeitsstand.

## 7. Grenzen und Empfehlung

- Die neue Runtime akzeptiert verschiedene eigene Skeletons und rigabhängige Anker. Sie erzeugt kein artspezifisches Rig, keine Gesichtsmimik und keine Flug-/Schwimm-KI automatisch.
- Ein Profil besitzt derzeit ein Skeletal Mesh. Beliebige modulare Mehrkomponenten-Körper oder universelle Niagara-/Audio-/Lichteffekte sind nicht neu implementiert.
- Sehr große, lange oder schwebende Arten benötigen eigene Platzierungs-, Kontakt-, Sichtbarkeits- und Kollisionsabnahme. Die bisherigen kleinen Weltkampf-Aufstellproben sind keine Freigabe aller 251 Größen.
- Es fehlt der vollständige belegte Originalgrößenkatalog. Größen werden pro tatsächlichem Kandidaten mit Quelle und Messbasis ergänzt.
- Kein endgültiges Meshy-Glumanda erhalten; folglich kein Nachweis seiner konkreten Topologie, Materialien, Gewichte oder Animationen. Bestehende künstlerische V1-Grenzen bleiben offen.

**Empfehlung:** Die geprüfte Pipeline V2 als verbindlichen Aufnahme- und Austauschablauf verwenden. Nach Bereitstellung des echten Meshy-Glumanda den dokumentierten Einzelimport ausführen und vor der einzigen Referenzänderung die reale Spielkamera-/Animations-/Gameplay-Abnahme durchführen. Kein weiterer Modell- oder Landschafts-Artpass wurde begonnen.
