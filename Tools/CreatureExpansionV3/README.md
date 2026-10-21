# Kreaturen-Erweiterung V3

Ausschließlich im bestehenden Projekt, keine neue Map. Originale: `Art/Characters/Creatures/Incoming/{Name}.glb`. Die sieben Arten und ihre belegten Daten stehen in `Species.json`. Die drei Starter bleiben unverändert.

## Quellen und eigener Rig pro Körperform

1. `InspectIncoming.py` importiert die sieben tatsächlich vorhandenen GLBs rein lesend, misst Topologie/UVs/Materialien und erzeugt diagnostische Blenderansichten unter Saved. Das sind keine Unreal-Abnahmen.
2. `Anatomy.py` enthält am realen Modell eingepasste Landmarken. Gesamt-Boundingbox und anatomische Körpermitte sind bei seitlichen Schwänzen nicht identisch: Pikachu X −7 cm, Glurak Y −25 cm im zunächst boxzentrierten Bezugsrahmen. Keine negative oder nichtuniforme Skalierung.
3. Blender im Hintergrund: `--python PrepareSource.py -- Pikachu`. Schreibt ausschließlich eine fehlende neue Arbeitsquelle, Originalreferenz bleibt im verborgenen `UNMODIFIED_HIGH_REFERENCE`. Alle ursprünglichen Vertices, Dreiecke und UV-Ecken bleiben erhalten; Originalbilder werden unverändert extrahiert und gepackt.
4. Enton, Machomei und Gengar: vollständige Bone-Heat-Lösung auf einer temporären positionsverschweißten Hilfskopie; nur normalisierte Gewichte zurückübertragen. Pikachu/Myrapla: unvollständige automatische Lösung wurde verworfen; explizite anatomische Einflüsse und topologische Glättung auf virtueller Verschweißung. Nebulak: starre Gesichtskugel und dezente periphere Gas-Bones. Glurak: eigene Flügel-, Schwanz- und Flammenkette. `SmoothSkin.py` verändert keine Geometrie.
5. `AnimateSource.py -- Name`: sieben eigene 30-Hz-In-place-Clips, Weltachsen-IK für Beine und gemessene Standphasen. Walk/Run sind für Nebulak langsames/schnelles Schweben. Keine Flug-/Schwimm-KI. Originalflamme von Glurak bleibt Teil des Meshes, eigener Slot und Bone statt doppelter Flammengeometrie.
6. `ValidateSource.py -- Name NeuerPruefname`: gespeicherte gepackte Quelle erneut öffnen, UVs/Gewichte prüfen, Extremposen rendern, **alle sieben FBX tatsächlich reimportieren**. Mathematische Fußtracks ersetzen keine visuelle Abnahme der deformierten Oberfläche.

`--revise-generated` ist nur für eine bewusst geprüfte Revision dieser neu erzeugten eigenen Arbeitsdateien vorgesehen. Nicht für Incoming-Originale, Starter oder fremde Änderungen verwenden. Das Tool kann handbearbeitete Gewichte/Actions der neuen Quelle ersetzen; vor späterer Anwendung zuerst Änderungen prüfen.

## Unreal

`Saved/CreatureExpansionV3/ImportRequest.json` enthält genau `{"species":"Name"}`. `ImportOne.py` verweigert vorhandene Zielassets und importiert einen Kandidaten in `/Game/Characters/Creatures/Name/MeshyV1`, dazu neue eigene Daten unter `/Game/Data/Creatures` und `/Game/Data/Encounters`. Materialien verwenden die originalen BaseColor-/Normal-/MR-Bilder, sRGB nur für Farbe, G/B für Roughness/Metallic und den geprüften Normal-G-Konvertierungsweg. Kein globaler Material- oder Lichtwechsel.

`RefreshOwnPikachu.py`, `RefreshOwnMyrapla.py` und `RefreshOwnEnton.py` sind eng geschützte einmalige Migrationsnachweise dieser Sitzung. Nach Versionierung verweigern sie die Anwendung. Keine allgemeine Reimportanleitung für bestehende Originalassets.

`PlaceHabitats.py` ist ebenfalls ein einmaliger Migrationsnachweis, kein regelmäßig auszuführender Spawner. Es verlangt die lokalen bestandenen Einzelreviews und einen sauberen Editor, verweigert doppelte IDs und prüft sämtliche vorbestehenden Actors/Instanzen vor dem gezielten Speichern. `RefineOwnHabitatPositions.py` betrifft nur die zwei nach Clearance-Prüfung korrigierten neuen Standorte. Im gesicherten fertigen Projekt existieren die Actors bereits; diese Werkzeuge nicht blind erneut anwenden.

`ConfigureVisualClearance.py` betrifft ausschließlich die sieben neuen Spezies. Der Kontakt bleibt körpernah; die lokale Wegsuche benötigt bei Flügeln, Stacheln oder großer Gashülle größere Abstände. `ProbeHabitatConnections.py` prüft Boden und durchgehende reale 2-m-Wege ohne Speicherung.

## Wiederholbare Prüfungen

Im sauberen, vorhandenen Editor mit `Tools/ProjectMaintenance/ArtSession.py`:

- `RunReview.py Name NeuerPruefname`: echte native Animation, Begleiterbewegung mit Enhanced Input, 2560×1440-Spielkamera, beide ClassicBattle-Perspektiven und vier Reaktionsrollen. Wildprofile und Gebietstrigger werden **nur in dieser isolierten PIE-Fixture** ausgesetzt. Keine Aussage über natürliche Habitatbegegnungen. Kampfbühne nativ 2560×1080, UI-Aufnahme separat und mit ihrer tatsächlichen Größe ausweisen.
- `RunCapture.py NeuerPruefname`: bestehende Fang-/Wechsel-/Heil-/Save-Flows für alle sieben Arten. Kanonisch durch die vorhandene Progression berechnete Level-100-Reserven und ein 1-KP-Gegner sind explizite Laufzeitfixtures, keine Produktions-/Balanceänderung. Ursprünglichen Dev-Slot per SHA-256 restaurieren.
- `RunEncounter.py NeuerPruefname Pikachu CURIOUS Victory west`: ausgewählter wirklicher Habitatakteur, voller Gegner-KP-Stand, vorhandenes Level-36-Team, sichere geprüfte Startposition, echte gemeinsame Enhanced-Input-Interaktion/Kontakt und sichtbare Flucht. Andere Begegnungen nur in der Fixture isolieren. Keine Annäherung als Kontakt ausgeben. Blockierte sichere Wartezustände gelten ausdrücklich als offene Fluchtabnahme.
- Editor regulär schließen: `ProjectQA.py NeuerBuild Build`, `ProjectQA.py NeueAutomation Automation`, `RunUnityBuild.py NeuerUnity`.
- Alle bestehenden Maps lesend mit `Tools/StarterExpansionV1/CheckMaps.py` prüfen. Gameplay-Fußlauf und Niederlagen-/Autosave-Regression aus den vorhandenen Werkzeugen verwenden.

Alle Kontrollmedien, Rohlogs, Requests, Spielstand-Testnachweise und Fortschrittsdateien bleiben im ignorierten Saved. Benötigte Modelle/Originaltexturen/FBX, Tools und Dokumentation gezielt versionieren. Kein physischer Controller-Test durch diese Werkzeuge.


`PatchSoles.py` dokumentiert die eng begrenzte lokale Sohlenkorrektur von Myrapla/Enton. Es verlangt den damaligen Eigentums-/Hashnachweis, sichert ein inverses Gewichtsdelta und prüft unveränderte Actions, Mesh/UVs/Rest-Rig/Materialien/gepackte Bilder. Kein allgemeiner Generator und auf einem neuen Clone nicht ohne den ursprünglichen lokalen Prüfkontext anwendbar. Entons Run-Extrempose bleibt mit etwa 1,23 cm Oberflächenunterschreitung dokumentiert.

`RunFullGameplay.py` verwendet den bewährten vollständigen Enhanced-Input-Fußlauf mit kanonischem Glurak/Machomei/Zunderlauf-Entwicklungsteam. Zusätzliche tatsächliche Habitatkämpfe während eines Wegschritts werden mit dem bestehenden Presenter behandelt; reguläre Trainer-/Dialogschritte bleiben im alten Ablauf. Kein Ausschalten der neuen Habitate und keine Testteleports. `RunCapture.py` prüft zusätzlich die tatsächlichen Quellakteure: Fang entfernt sie ohne Niederlagenflucht.

Der Fangtest verwendet die tatsächliche stabile Encounter-ID jedes der sieben Habitatakteure, nicht eine abweichende Test-ID. Nach Save/Load müssen sowohl Team/KP/XP als auch der entfernte Quellakteur unverändert bleiben. Ein reiner Transferfall ohne echte Quellakteur-ID belegt diesen Persistenzfall nicht.
