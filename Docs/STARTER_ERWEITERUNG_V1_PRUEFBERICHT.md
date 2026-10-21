# Starter-Erweiterung V1 – Prüfbericht

Stand 21.10.2026. Ausgangspunkt main `2a1db9165f37866745a6641619e6d2658bde4216`. Keine neue Map, kein Worktree. Vorhandene 58 unversionierte Dateien im Schutzinventar `Saved/StarterExpansionV1/Initial.json` erfasst. Vollbackup 03492bd bleibt unverändert.

## Arbeitspaket 1: sichere Niederlagen-Speicherung

Rückkehr prüft nun die tatsächlich erfolgreiche Teleportierung; bei blockiertem Ziel ist nur ein ebenfalls kollisionsgeprüfter PlayerStart zulässig. Erst nach erfolgreicher Platzierung und vollständiger Teamheilung wird der abgeschlossene Zustand gespeichert. Der tatsächliche Rückkehrpunkt ist Teil desselben bestehenden SaveGame-Snapshots. Während Kampf und laufender Rückkehr bleiben Snapshots gesperrt.

Der macOS-Speichertransport schreibt die unveränderte SaveGame-Version 4 in eine eindeutige temporäre Nachbardatei, liest und deserialisiert diese zur Kontrolle und ersetzt den Slot über das atomare native `rename` der Apple-Plattformdateischnittstelle. Ein Fehlschlag entfernt nur die eigene temporäre Datei; der vorherige Slot wird nicht vorab gelöscht. Kein zusätzlicher dauerhafter Backupslot. Dies garantiert keinen Schutz vor sämtlichen Hardware-/Stromausfällen. Ladevalidierung und Migrationen 1–3 bleiben erhalten. Ein fehlgeschlagenes Autosave wird im Rückkehrhinweis angezeigt; die erfolgreiche Heilung bleibt erhalten.

Prüfungen:

- Mac Development Editor Build erfolgreich: `Saved/ProjectRefinement/StarterSaveBuild02/Result.json`.
- Vollständige Projekt-Automation: **70/70**, keine Testwarnungen oder Testfehler (`StarterSaveAutomation01`). Neue Prüfungen für die Rückkehrsperre und den geprüften atomaren Austausch einschließlich fehlgeschlagener Dateipromotion.
- Echter ClassicBattle-PIE-Niederlagenablauf mit vorhandener Kamera/UI: **bestanden**, `Saved/StarterExpansionV1/DefeatSave04/Result.json`. Speichern im Kampf abgewiesen; Rückkehr, volle KP, Autosave und identisches Reload von GUID/KP/XP/Rückkehrpunkt nachgewiesen. Die ersten Harness-Läufe benötigten eine Korrektur des Python-Checkpoint-Zugriffs und des GUID-Vergleichs; sie sind nicht als erfolgreiche Abnahmen gezählt.
- Ursprünglicher Dev-Spielstand nach jedem Lauf bytegenau wiederhergestellt: SHA-256 `d9bf0677d2f06bb96bfe20f0eec7a9b369ba010117de0d49f13b9d027f8dbf6b`.
- ClassicBattle-Darstellung, Kampflogik, Maps, Originalmodelle und bisherige Animationen unverändert.

## Weitere beauftragte Arbeitspakete

Die Modell- und Speziesintegration ist unten als zweites Arbeitspaket dokumentiert. Freie Oberweltbewegung und gemeinsame Gameplay-Abnahme sind im dritten Arbeitspaket unten dokumentiert. Die Gesamtprüfung nutzt alle bestehenden Maps und den vollständigen Gameplay-Fußlauf. Kontrollmedien und lokale Prüfdaten bleiben unter Saved und werden nicht hochgeladen. Physischer Switch-Pro-Test ist ausdrücklich kein Abschlusskriterium.


## Arbeitspaket 2: Schiggy und Bisasam

| Modell | Originaldatei | Vertices / Dreiecke | Rig | Höhe | Materialien / Texturen |
|---|---|---:|---|---:|---|
| Schiggy | `Art/Characters/Creatures/Incoming/Shiggy.glb` | 14.162 / 21.273 | eigenes Biped, 20 Bones | 0,50 m | 1 / 3 × 2048² |
| Bisasam | `Art/Characters/Creatures/Incoming/Bisasam.glb` | 13.885 / 21.545 | eigenes Quadruped, 18 Bones | 0,70 m | 1 / 3 × 2048² |

Original-SHA-256:

- Schiggy: `8353b766fc36d90d3c7a8905e82ae9c407a974959dcab6cac629c5127446a127`.
- Bisasam: `01ee8bc064635aeaaed2b356e1c87e0a9d0ab819fa6285d86cfbe0460466306d`.

Beide Eingaben haben kein Rig und keine Animationen. Keine Retopologie, keine Polygonreduktion, keine neuen Flächen, keine Änderung von Kopf/Körper/Design. Unveränderte GLB-Geometrie als getrennte versteckte Referenz in jeder Blenderquelle, drei gepackte Bilder. Rohmessungen der offenen Kanten (6.599/5.863) enthalten viele UV-Seams und sind kein Beweis für echte Löcher oder Wasserdichtheit. Schiggy zeigt im Original kleine dunkle Oberflächenstellen nahe dem Auge; diese sind nicht als behobene Geometriefehler ausgegeben.

Frühe regionale Gewichtskandidaten zeigten starke Hautauszüge und wurden verworfen. Die endgültigen Gelenke wurden anhand tatsächlicher Hand-/Sohlenpositionen korrigiert. Blender Bone Heat auf einer temporär bei 1 µm positionsverschweißten Hilfskopie lieferte vollständige, anschließend normalisierte Gewichte. Nur Gewichte wurden auf das ursprüngliche Mesh übertragen. Rigidere Sohlen und analytische Zweibone-Standphasen verhindern die zuvor sichtbaren Fußverformungen. Haut-/Gelenkfeinschliff bei extremen Posen bleibt eine spätere manuelle Qualitätsaufgabe; kein pauschaler Produktionsreifeanspruch.

Jeweils Idle, Walk, Run, Attack, Hit, Faint und Happy bei 30 Hz. Schiggy: Walk 26 cm/s, Run 50 cm/s; Bisasam: 32/72 cm/s. Bisasam nutzt einen Viertakt-Walk und diagonale Laufpaarung. Standphasen werden mit gemessener konstanter Fußgegenbewegung gelöst; die maximalen Schrittinkrementfehler und minimale Oberflächenhöhe stehen in den jeweiligen `MeshyV1_AnimationAudit.json`. Das ersetzt keine komplette Ingame-Deformationsabnahme.

Neue bearbeitbare Quellen und Exporte:

- `Art/Characters/Creatures/Schiggy/Source/Schiggy_Meshy_V1.blend` und `Bisasam/Source/Bisasam_Meshy_V1.blend`.
- Je Spezies sieben FBX-Dateien in `Exports/MeshyV1/`, drei unveränderte extrahierte Original-JPEGs in `Textures/MeshyV1/`, Modell- und Animationsaudit.
- Unreal: `/Game/Characters/Creatures/{Schiggy,Bisasam}/MeshyV1/` mit jeweils eigenem Mesh, Skeleton, sieben AnimSequences, Material, drei Texturen und Präsentationsprofil. Keine zusätzlichen Feueranker.
- Spezies `/Game/Data/Creatures/DA_Schiggy`, `DA_Bisasam`; Wildprofile `/Game/Data/Encounters/DA_Schiggy_Wild`, `DA_Bisasam_Wild`. Stabile IDs ändern keine Glumanda-/Save-Identität. Keine neuen Evolutionsmodelle oder ungesicherten Evolutionsreferenzen.

Gen-2-Daten anhand [Serebii Schiggy](https://www.serebii.net/pokedex-gs/007.shtml), [Serebii Bisasam](https://www.serebii.net/pokedex-gs/001.shtml), [Schiggy-Lernliste](https://pokemondb.net/pokedex/squirtle/moves/2) und [Bisasam-Lernliste](https://pokemondb.net/pokedex/bulbasaur/moves/2) geprüft. Fangrate jeweils 45, Wachstum Medium Slow, weiblicher Anteil 12,5 %. Basis-Ertrag 66 für Gen-2-Schiggy ([Generationsänderung](https://pokemondb.net/pokedex/squirtle)), 64 für [Bisasam](https://pokemondb.net/pokedex/bulbasaur). Tackle: 35 Stärke, 95 Genauigkeit, 35 AP. Rankenhieb: Gen-2-Spezialattacke, 35/100/10. Aquaknarre: 40/100/25, ab Level 13. Bisasam nutzt außerdem das unveränderte bestehende Heuler-Asset. Nicht unterstützte Originalwirkungen Rutenschlag/Blubber/Panzerschutz/Egelsamen sind bewusst offen; freie Slots bleiben leer.

Unreal-Abnahme:

- Build `StarterModelBuild02`: bestanden; der erste neue Testbuild benötigte eine Korrektur an die vorhandene MoveSlot-Schnittstelle.
- Automation `StarterModelAutomation01`: **72/72**, 0 Testwarnungen/Fehler. Belegt eigenes Skeleton, sieben kompatible Clips, tatsächliche Meshhöhe, stabile Spezies-IDs, Wildroll, Heilung und Save/Load mit beiden Spezies.
- Beide gespeicherten Blenderquellen erneut geöffnet; alle 14 FBX-Dateien wirklich reimportiert. Gleiche Dreieckzahlen, eigene Bones/Actions, identische UVs und normalisierte Gewichte (`Saved/StarterExpansionV1/BlenderValidation04/Result.json`).
- `ModelReview02`: vier echte PIE-Kämpfe, je beide Perspektiven in ClassicBattle und WorldBattle; Angriff, Flucht und tatsächliches Speichern/Laden bestanden. Ursprünglicher Dev-Spielstand danach bytegenau restauriert.
- Alle **11 vorhandenen Maps**, einschließlich der geschützten unversionierten Testmap: Map Check **0 Fehler / 0 Warnungen**, Editorlog `Saved/StarterExpansionV1/EditorModels01.log`. Keine Map gespeichert/geändert.
- Vorhandene Engine-Start-/Audio-/idevice-Warnungen und eine bestehende `MI_WLA_LeafOak`-Warnung zur Instancing-Nutzung wurden beobachtet. Keine Änderung an diesem welt-/kampfumgebungsbezogenen Altmaterial. Keine Fehler stillschweigend als bestanden umgedeutet.

Texturdiagnose: Schiggys Mip-Atlas erzeugte helle Flecken (`ModelReview01`). Isolierte Änderung ausschließlich seiner neuen BaseColor-Mip-Einstellung beseitigt sie (`ModelReview02`). Originalfarben und Original-JPEG unverändert. Diese Lösung behält volle 2K-Abtastung und kann bei großer Entfernung mehr Abtastungsunruhe verursachen. Die folgende Bewegungssichtung zeigte keine vergleichbaren weißen Atlasflecken; eine vollständige Distanz-/LOD-Abnahme ist damit nicht ersetzt. Normals: OpenGL nach Unreal mit invertiertem Grünkanal; MR: G=Roughness, B=Metallic.

Echte Unreal-Aufnahmen, lokal, **tatsächlich 2331 × 1346**, kein behauptetes QHD:

- `Saved/GlumandaV11/LiveUI/Starter_ModelReview02_0_Commands/ActualSlateViewport.png`: Schiggy vorne links, Bisasam gegenüber.
- `Saved/GlumandaV11/LiveUI/Starter_ModelReview02_1_Commands/ActualSlateViewport.png`: umgekehrte Perspektiven.
- Weitere Moves-/Attack-/WorldBattle-Aufnahmen in derselben lokalen Gruppe. WorldBattle am unveränderten Spawnpunkt zeigt teilweise vorhandene Weltdeckung; es wurde kein Weltobjekt für einen schöneren Test entfernt.

Die zentrale Kampfansicht, deren Code/UI/Kameras/Platzierungsregeln und bisherige Modelle/Animationen bleiben unverändert. Dauerhafte Wildplatzierung und Begleiterbewegung folgen separat.

## Arbeitspaket 3: größere Wildhabitate und gemeinsamer Begleiter

Die bisherige Begrenzung war kein Rig-/Meshproblem: `VisibleWildCreatureActor::Tick` bewegte die Figur auf einem festen 45-cm-Kreis mit kurzen zyklischen Phasen. Dieser Kreis wurde durch eine gemeinsame Landbewegungskomponente ersetzt. Pro Art konfigurierbar: Radius, Mindestweg, Geschwindigkeiten, Pausen, Drehgeschwindigkeit, Körperradius, Rückrufhysterese und maximaler aktiver Abstand. Instanzen können ihren Habitatkreis zusätzlich durch Boxgrenzen beschränken. Es gibt keine neue Kreaturendatenbank oder neue Party-/Kampflogik.

Bodenprojektion und begrenzte lokale A*-Suche prüfen reale Kollisionen, begehbare Steigungen, Stufen und vorhandene Wasserblocker. Gebäude werden über ihre tatsächlichen Innenraum-/Relokationsfunktionen geprüft, nicht über eine riesige gemeinsame Außen-/Innenraum-Boundingbox. Reine `Water`-/`CreatureNoWalk`-Tags werden ergänzend unterstützt. Kein beliebiges Wasser wird allein aus seinem Materialnamen erkannt. Die vorhandene 24-cm-Brückenkante zeigte eine zu tiefe Überlappungsprüfung; sie wurde an die erlaubte Stufenhöhe angepasst und als realer Kollisions-Automationstest ergänzt. Nicht erreichbare Rückrufziele im Wasser lösen eine Suche nach erreichbaren Punkten um den Spieler aus, kein zufälliges Weglaufen.

Genau zwei neue Wildinstanzen in VisualV2:

| Art | stabile Begegnungs-ID | Rootposition cm | Kapsel Radius / Halbhöhe | Habitat-Radius |
|---|---|---:|---:|---:|
| Schiggy | Dev_Schiggy_Wild_01 | 420 / −1050 / 30 | 30 / 30 cm | 550 cm |
| Bisasam | Dev_Bisasam_Wild_01 | −700 / 250 / 38 | 38 / 38 cm | 650 cm |

Der vorhandene Glumanda-Actor, sein Seed und seine ID bleiben erhalten; Artenradius jetzt 650 cm. Vor dem Speichern wurden **1.446 vorhandene Actors** einschließlich Transforms, Meshes, Materialien, Kollisionseinstellungen und Lichtwerten verglichen: unverändert. Die zwei neuen kleineren Kapseln erhalten einen passend über dem Boden liegenden 2D-Fallback. Keine anderen Karten, Landschafts-/Heilhausobjekte oder bestehenden Kollisionen geändert. Platzierung und erneute Öffnung: `WildPlacement.json`, `WildPlacementReopened.json` unter Saved/StarterExpansionV1.

Der Begleiter ist genau eine kollisionsfreie Darstellung des ersten kampffähigen Teammitglieds mit konfigurierter 3D-Präsentation. Er nutzt die bestehende Party, wandert lose, macht Pausen und holt bei Entfernung auf. Kampfstart blendet ihn aus und pausiert die Landbewegung. Raumwechsel und tatsächliche Save-/Checkpoint-Teleportierungen werden getrennt von normalen Laufschritten behandelt. Eine außerhalb des Bildes liegende Wiederanknüpfung bleibt eine begrenzte Rückfallsicherung bei zu großer Entfernung; kein Anspruch auf eine vollständige Open-World-Navigations-KI. Keine neue Begleiter-Auswahloberfläche.

Zusätzliche, ausschließlich für Begleiter verwendete Sprintclips:

| Art | Referenzgeschwindigkeit | Dauer / Sampling | neue bearbeitbare Quelle |
|---|---:|---|---|
| Zunderlauf / Glumanda | 180 cm/s | 0,5 s / 60 Hz | Zunderlauf/Source/Zunderlauf_OverworldSprint_V1.blend |
| Schiggy | 160 cm/s | 0,5 s / 60 Hz | Schiggy/Source/Schiggy_OverworldSprint_V1.blend |
| Bisasam | 180 cm/s | 0,5 s / 60 Hz | Bisasam/Source/Bisasam_OverworldSprint_V1.blend |

Pfadpräfix jeweils `Art/Characters/Creatures/`. Dies sind kleine Rig-/Actionquellen mit Metadaten zur unveränderten vollständigen Modellquelle. Drei additive FBX in `Exports/OverworldV1/`; neue Unreal-Sequenzen unter `/Game/Characters/Creatures/<Art>/OverworldV1/Animations/`. Nur ein temporäres Begleiterprofil nutzt den längeren Sprint. Originalmesh, Materialien, Schwanzfeuer und sieben Kampfclips bleiben erhalten. Neue Quellen erneut geöffnet, Aktionen auf die Originalmodelle geprüft und alle drei FBX reimportiert (`SprintValidation02`). Gemessene Standphasenfehler unter 0,0000001 m; keine Behauptung einer universellen Gelände-Fuß-IK. Die Bewegung erfolgt vor der Präsentationsmessung im selben Frame; dadurch entfielen künstliche Geschwindigkeitsspitzen zwischen verschiedenen Tick-Zeitpunkten.

Die frühen Sprintkandidaten mit zu tiefer Körperhaltung wurden verworfen. Ein Blender-Scene-PartialWrite-Export stürzte im Blender-internen Scene-Copy ab; die neue Rig-/Actiondatei wird stattdessen als eigene Datei gespeichert. Bestehende Blenderquellen blieben SHA-identisch. Der erste Unreal-Sprintimport brauchte den tatsächlichen `AnimSequence.get_skeleton()`-Zugriff; der eigene teilweise importierte Clip wurde kontrolliert geprüft und weiterverarbeitet, keine Originalassets reimportiert.

Echte Bewegungsabnahme `MovementVisual05`:

- Alle drei wilden Figuren außerhalb des alten Kleinkreises: maximale gemessene Entfernungen vom Beginn 4,22 / 3,45 / 5,10 m (Glumanda / Schiggy / Bisasam). Die 25-s-Teilabschnitte enthalten 4,57 / 4,95 / 6,06 m zurückgelegten Weg. Frühere 55-s-Läufe belegen längere Beobachtung. Keine blockierten Schritte in diesem ausgewählten Lauf; das ist keine Garantie für jedes zukünftige Habitat.
- Echter Enhanced-Input-Sprint über die bestehende Brücke und zurück: Spieler maximal 315 cm/s, Begleiter maximal 385 cm/s, größter gemessener Abstand 6,56 m während des Umwegs, anschließender Rückruf bestanden. Kein Testteleport auf dieser Route. Hysterese verhindert ständiges Wechseln zwischen Rückruf und freiem Wandern.
- Wildbewegung im ClassicBattle unverändert pausiert, Begleiter versteckt; nach Rückkehr genau ein Begleiter. Alle drei Spezies als Begleiter sichtbar geprüft. Die Fixtures setzen die Party nur im Arbeitsspeicher; die ursprüngliche Dev-Datei wurde anschließend restauriert.
- Geordnete echte Spielsequenz `Saved/StarterExpansionV1/MovementVisual05/WalkSequence_*.png` mit Game-Zeitstempeln in `Frames.jsonl`. `Shot showui` erfasst hier tatsächlich das ganze Editorfenster **2940 × 1696** mit eingebetteter Spielkamera, keine behaupteten QHD-Viewportpixel. Battle-Viewport-Aufnahmen separat tatsächlich 2331 × 1346. Keine generierten Bilder als Ingame-Nachweis.

## Gemeinsame Fang-/Heil-/Speicherprüfung

`CaptureReview02`: zwei echte PIE-ClassicBattles über vorhandenen Presenter und Menüs. Kontrollierte Laufzeit-Fixture: wildes Ziel auf 1 KP, keine Änderung von Fangraten/Attacken oder Produktionsdaten. Je acht echte Fangversuche und sieben reguläre Kampf-Heilitems, Teamwechsel und gegebenenfalls erzwungener Wechsel. Beide Ziele erfolgreich gefangen, korrekte Anzahl Fangitems verbraucht, dieselbe individuelle GUID ins Team übernommen. Anschließend beide Spezies über vorhandene Heilitems vollständig geheilt und tatsächlich gespeichert/geladen: GUID, Spezies, KP und XP identisch. Erster Harnesslauf behandelte die notwendige Wechselaufforderung noch nicht; nicht als bestanden gezählt. Dev-Slot danach jeweils SHA-identisch restauriert.

## GitHub-Sicherung und lokaler Schutz

Bereits geprüfte und gepushte Meilensteine:

- Niederlagen-Speicherung: `293becff5c3495db5386f9644fceffb305f64315`.
- Meshy-Startermodelle: `79c30a24916c5c0c165c3d17896e4f57a9f2288a`.

Beim zweiten Meilenstein meldete ein einzelner lokaler LFS-Scannerlauf ein nicht lesbares 40-stelliges Git-Pointer-Blobobjekt. Der Push wurde versehentlich begonnen, bevor dieses Ergebnis ausgewertet war; dies war ein Ablauffehler. Keine Ursache dafür wird als bewiesen behauptet. Danach: Pointer-Blob mit `git cat-file` vorhanden und korrekt, Git-Konnektivitätsprüfung fehlerfrei, erneutes LFS-Fsck bestanden. **Alle 59 neuen LFS-Objekte (73.652.399 Bytes) vom Server geladen und SHA-256-verifiziert**, Remote exakt auf dem erwarteten Commit. Nachweise `ModelRemoteLFS.json`, `LFSRecheck.log`, `GitConnectivity.log`. Der Abschluss-Push wird erst nach ausgewerteten lokalen Prüfungen durchgeführt.

Alle 58 ursprünglich unversionierten Dateien weiterhin byteidentisch; nur die zwei beauftragten Original-GLBs gezielt aufgenommen. Andere Incoming-Modelle, historische unversionierte Dateien und eigene lokale Python-Caches nicht gestaged. Beide Vollbackup-Refs bleiben auf 03492bd; dieser Commit ist kein Vorfahr von main. Kein neuer Worktree, keine neue Map, keine Historienänderung, keine Performance-Testreihe. Kontrollmedien und Prüflaufdaten bleiben lokal unter Saved.

## Abschlussprüfung und Freigabegrenzen

| Prüfung | Endstand | tatsächlicher Nachweis |
|---|---|---|
| Mac Development Editor Build | bestanden | StarterMovementBuild08, Exit 0 |
| Vollständige Automation | **75/75**, 0 Testwarnungen / 0 Fehler | StarterMovementAutomation03/Result.json |
| Alle bestehenden Maps | **11**, jeweils 0 Fehler / 0 Warnungen | FinalMapChecks.json, EditorMovement05.log |
| Unveränderte alte Weltobjekte nach Neuladen | **1.446 identisch**, genau zwei neue Actors | WorldScopeReopened.json |
| Vier abschließende Classic-/WorldBattles | bestanden, beide Perspektiven, Angriff/Flucht/Save/Reload, Wildpause/Begleiterausblendung | ModelReviewFinal03/Result.json |
| Niederlage mit fertiger Oberweltbewegung | Rückkehr, volle Heilung, Autosave und identischer Reload bestanden | DefeatSaveFinal05/Result.json |
| Vollständiger Gameplay-Fußlauf | **102 Schritte**, 288,20 m, Sprint maximal 315 cm/s, keine Testteleports | Saved/GlumandaV11/Acceptance/StarterExpansionFinal02/FootTest.json |
| Zusätzlicher Begleiter-Beobachter | **645 Stichproben**, 27 Kampf-Ausblendungen, 27 schattenfreie Innenraumproben, keine Befunde | dort CompanionResult.json / CompanionFrames.jsonl |
| Erhaltener Dev-Spielstand | SHA-256 identisch zum Ausgangszustand | d9bf0677d2f06bb96bfe20f0eec7a9b369ba010117de0d49f13b9d027f8dbf6b |

Der vollständige Fußlauf prüft Wildfang, Teamwechsel, Liora, Wanderer-Dialog, Archiv-/Questfortschritt, tatsächliches Speichern/Laden, Heilhaus-Heilung/Checkpoint, Eintritt/Austritt einschließlich Diagonalen, Innen-/Außenkamera, Kollisionen, Kronenfreistellung, acht Richtungen und Sprint. Der erste Lauf absolvierte ebenfalls alle 102 Schritte, sein zusätzlicher Schattenbeobachter war jedoch am Türübergang an den verzögerten Kamera-Bewegungsmodus gekoppelt. Der abschließende Beobachter prüft stattdessen den tatsächlichen Raumaufenthalt des Begleiters und bestand. Keine Änderung der Heilhausdarstellung erforderlich. Der Roh-Abstandsmaximalwert enthält vier Abtastungen zwischen den weit versetzten Innen-/Außenkoordinaten beim bestehenden Raumteleport; dies ist kein Laufradius. Ohne solche Koordinatenwechsel lag der maximale sichtbare Abstand dieses Fußlaufs bei 5,91 m.

Frühe Bewegungs-Harnessläufe benötigten eine Initialisierungsfrist für den Begleiter und einen lesbaren Meshzugriff statt einer geschützten internen Profilproperty. Das erste Automationsergebnis enthielt die vorhandene `idevice_id`-Startwarnung; die abschließende vollständige Suite wurde ohne Unterdrückung erneut mit 75 Erfolgen und null Testwarnungen abgeschlossen. Editor-Startlogs enthalten weiterhin vorhandene Engine-Selbsttest-/iOS-/Audio-Meldungen; eine saubere Projekt-Automation bedeutet nicht, dass sämtliche Engine-Startlogs warnungsfrei sind. Die deutsche Map-Check-Zusammenfassung wird ausdrücklich ausgewertet; fehlende Zusammenfassungen gelten nicht als Erfolg.

Wichtigste echte Bilder:

- `Saved/GlumandaV11/LiveUI/Starter_ModelReviewFinal03_0_Commands/ActualSlateViewport.png`: Schiggy gegen Bisasam in unveränderter klassischer Kamera.
- `Saved/GlumandaV11/LiveUI/Starter_ModelReviewFinal03_1_Commands/ActualSlateViewport.png`: Bisasam gegen Schiggy.
- `Saved/StarterExpansionV1/MovementVisual05/WalkSequence_00000000.png` und folgende: echte geordnete Sprint-/Begleiteraufnahme im Editorfenster.
- `Saved/StarterExpansionV1/MovementVisual05/BisasamCompanion00000.png`, `GlumandaCompanion00000.png`: weitere Begleiter.
- Gameplay-Fußlauf: `Saved/GlumandaV11/Acceptance/StarterExpansionFinal02/` mit Spielkamera-, Dialog-, Kampf-, Heilhaus- und Kronenfreistellungsbildern.

**Technische Gesamtprüfung bestanden.** Keine pauschale künstlerische Produktionsfreigabe: Gewichte an Extremposen und die ursprünglichen kleinen Schiggy-Oberflächenfehler bleiben manuell zu beurteilen; Schiggy-Mipstrategie benötigt später eine eigene LOD-/Distanzabnahme. Die Landnavigation ist eine begrenzte Grundlage, keine Flug-/Schwimmnavigation oder universelle Fuß-IK. Fehlende Gen-2-Attackenwirkungen bleiben ausdrücklich offen, keine erfundenen Endwerte. Physischer Switch-Pro-Controller-Test bleibt wie beauftragt beim Nutzer. Keine weiteren Kreaturen automatisch erstellt und keine Heilhaus-/Landschaftsüberarbeitung.

Der dritte geprüfte Meilenstein ist `feat: add habitat roaming and party creature companions`; sein tatsächlich erzeugter und remote verifizierter Hash wird in der Abschlussantwort genannt. Vollständige gezielte Commitliste und lokale Index-/LFS-Prüfnachweise liegen unter `Saved/StarterExpansionV1/MovementCommitPlan.json` und `MovementIndexAudit.json`; keine Kontrollmedien werden versioniert.
