# Glutexo Integration V1 – Meilenstein A

Stand: 23.10.2026. Glutexo als eigene Art `CreatureSpecies:Glutexo`, national 005, Feuer, 110 cm integriert. Glumanda behält die stabile ID Zunderlauf; bestehende Arten, Maps, Landschaft und Heilhaus unverändert. Entwicklungen werden erst im anschließenden Meilenstein B ausgeführt.

## Tatsächliche Quelle und Qualität

Original: `Art/Characters/Creatures/Incoming/Glutexo.glb`, SHA-256 `718f9eb037832228f25bdbce299671db0972a9c3c271d23724e39743476c6efe`. Front-/Seiten-/Rückeninspektion identifiziert das Modell eindeutig. Ein Mesh, 17.327 ursprüngliche Vertices, 21.001 Dreiecke, eine UV-Schicht, drei originale gepackte 2048²-Texturen, ursprünglich kein Rig und keine Animationen. Rohmesh enthält 11.723 offene Kanten an Mesh-/UV-Teilflächen; diese Zahl allein ist kein Nachweis sichtbarer Löcher. Keine degenerierten Flächen gefunden. Sichtprüfung zeigt keine auffälligen offenen Flächen; keine Behauptung vollständig wasserdichter Topologie.

Neue bearbeitbare Quelle: `Art/Characters/Creatures/Glutexo/Source/Glutexo_Meshy_V1.blend`; eigene 20-Bone-Anatomie mit separater Schwanz-/Flammenkette. Originalgeometrie, UVs und Bilddaten bleiben erhalten. Erste explizite Hüllengewichte erzeugten Bauchverzug; verworfen und durch vorhandene Bone-Heat-Gewichtung auf Hilfsgeometrie plus gezielte Schwanzgewichte korrigiert. Arme aus der T-Pose abgesenkt; keine Neumodellierung. Sieben eigene In-place-Clips: Idle, Walk, Run, Attack, Hit, Faint, Happy. Referenzgeschwindigkeiten 30/60 cm/s; normalisierte Gewichte, identische UVs und alle sieben tatsächlich reimportierten FBX geprüft. Standphasen der Bone-Tracks sind mathematisch geprüft, keine Behauptung perfekter Oberflächen-Fußkontakte in jeder Pose.

Die bereits modellierte Originalflamme ist ein eigener Mesh-Materialslot am Bone `flame_tip`. Keine zweite Flamme und kein Feuer an Kopf/Körper. Originale BaseColor-, Normal- und Roughness/Metallic-Texturen; neues Material nur für Glutexo. Eigener Unreal-Namensraum `/Game/Characters/Creatures/Glutexo/MeshyV1`; keine alten Pokémon reimportiert.

## Daten und Systeme

Gen-2-Artwerte, Fangrate, Geschlechterverhältnis, Wachstum und vollständige Level-Lernliste anhand fester Kristall-Revision verifiziert: `Tools/GlutexoEvolutionV2/ReferenceSources.json`. Vorhandene produktive V4-Attacken anhand stabiler IDs wiederverwendet. Keine neuen Attackendefinitionen. Neues Encounter-Profil ist konfigurierbar; kein dauerhaftes Wildhabitat und keine Map gespeichert. Art unterstützt die bestehenden Wild-, Begleiter-, Kampf-, Fang-, Team-, Heil- und Save-Wege.

Das automatisch im normalen VisualV2-PIE verfügbare Testgelände enthält elf Exemplare. Zugang: Konsole `pm.TestGround.Go 11`, Rückkehr `pm.TestGround.Return`. Die zehn bisherigen Stationen behalten ihre Position; die vorhandene Bodenfläche wurde um Platz 11 erweitert. Testexemplare besitzen keine Fang-/Save-Identität.

## Tatsächliche Tests

- Blender `SourceQA02`: gepackte Quelle, unveränderte UVs, vollständige Gewichte, sieben FBX-Roundtrips bestanden; Extremposen visuell geprüft.
- Editor-Build `GlutexoA_Build04`: Exit 0.
- Vollständige Automation `GlutexoA_Automation01`: 182 Success, 1 SuccessWithWarnings, 0 Failed, 0 NotRun. Alle 183 fachlichen Tests bestanden. Der strenge ProjectQA-Wrapper endet dennoch mit **Exit 1**, weil während `AtomicVisualSwap` der unveränderte externe iOS-Helfer `idevice_id` mit „Bad CPU type in executable“ zwei Warnungen erzeugt. Keine warnungsfreie QA behauptet.
- Elf vorhandene Map Checks: jeweils 0 Fehler/0 Warnungen; keine Map gespeichert.
- `ReviewA02`: normaler PIE-Start, Testgelände mit elf Exemplaren, native Begleiterbewegung, QHD-Spielkamera, beide ClassicBattle-Perspektiven, Attack/Hit/Faint/Happy und Rückkehr bestanden.
- `CaptureA04`: realer Fangtransfer, korrekte Entfernung des PIE-Quellakteurs ohne Flucht, Teamwechsel, Heilung und identischer Zustand nach Save/Load bestanden. Klar gekennzeichnete technische Fixture: vorhandener PIE-Quellakteur als Glutexo konfiguriert, reguläre Startlevel, 1-KP-Fangziel, Seed 51. Kein Nachweis einer neu platzierten natürlichen Glutexo-Begegnung.
- Entwickler-Save und alle 25 vorbestehenden unversionierten Incoming-Dateien nach Tests per SHA-256 unverändert; Vollbackup-Refs erhalten. Der ausdrücklich benötigte Glutexo-Originalbestand wird mit diesem Meilenstein versioniert; andere Incoming-Dateien bleiben unversioniert.

## Echte Unreal-Nachweise, ausschließlich lokal

`Saved/GlutexoEvolutionV2/ReviewA02/Glutexo_World_4_QHD00000.png` zeigt Original-Spielkamera 2560×1440, Spieler als Größenreferenz, Testexemplar 11 und den eigenen Begleiter. Weitere World-Aufnahmen bei Bewegung: 8/12/16 Sekunden. `Glutexo_Battle_0.png` und `_1.png` sind native 2560×1080-Kampf-Renderziele, ausdrücklich keine QHD-Vollbildaufnahmen; echte UMG-Vollbildnachweise liegen separat unter `Saved/GlumandaV11/LiveUI/Expansion_ReviewA02_*`. Reaktionsbilder sind echte native Frames. Keine Kontrollmedien werden versioniert.

## Fehlernachweise und Grenzen

Erster Build scheiterte an einem Test-Namensalias; gezielt korrigiert, Build04 bestanden. Erster Editorstart mit ExecutePythonScript beendete sich regulär nach dem Skript; dauerhaftes Prüffenster mit ExecCmds gestartet. Erste isolierte Darstellung wurde durch einen regulären Wildkontakt unterbrochen; isolierte PIE-Wildkollisionen danach ausdrücklich gesperrt. Alte Fangprüfung war mit neuen Lernangeboten bei künstlichem Level 100 nicht mehr kompatibel; endgültiger Test verwendet reguläre Startlevel. Frühe Fehlversuche bleiben lokal dokumentiert und werden nicht als Erfolge gezählt.

Beim erstmaligen Erzeugen registrierte der AssetManager kurz den vorläufigen Namen DA_Glutexo; vollständige Automation nach Editor-Neustart lädt Art, ID, Mesh, Skeleton und sieben Clips korrekt. Keine Veröffentlichung als perfekt animiert: Feinheiten an Schritten und Gelenken bleiben visuell abnahmefähig. Physischer Controller-Test nicht durchgeführt, bestehende Belegung unverändert. Vollständiger gemeinsamer Gameplay-Fußlauf erfolgt mit Meilenstein B. Keine zusätzliche Map, Projektkopie oder Worktree.
