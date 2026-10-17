# Benötigte Projektdateien und optionale Entwicklungsnachweise

Diese Vorbereitung basiert auf dem vollständigen lokalen Stand `03492bd`. Der große Commit ist kein Vorfahr des schlanken Branches. Es wurde kein endgültiger Commit erstellt.

## Pflichtprüfungen

`python3 Tools/DevelopmentEvidence/evidence.py validate-core` prüft **jede erforderliche Datei** aus `CoreFiles.json` auf Existenz, Größe und SHA-256. Fehlende oder veränderte Pflichtdateien führen zu Exit 1. Das Manifest ist ein versionierter V5-Sicherungssnapshot, kein selbstaktualisierender Freibrief für spätere Änderungen. Manifestanpassungen benötigen eine neue geprüfte Dateiliste. Die Manifestdatei selbst wird nicht rekursiv gehasht; Git/Indexprüfung schützt ihre Version.

Unreal-Editor-Build, die vollständige aktuelle PokeMonster-Automation und Map Checks bleiben eigenständige Pflichtprüfungen. Diese Tests und die Gameplayquellen wurden nicht abgeschwächt.

Die fünf historischen Ganzarbeitsbaum-Prüfer führen standardmäßig den ausdrücklich benannten aktuellen Core-Snapshot aus. Ihr ursprünglicher Code bleibt unten in derselben Datei erhalten. Mit `POKEMONSTER_RUN_HISTORICAL_GUARD=1` ist ausschließlich der alte Algorithmus auswählbar; er benötigt seine damaligen Saved-Manifeste, Sessionmarker und damaligen Dateistände und ist auf einem heutigen Clone nicht automatisch erfolgreich. Alte Hashabweichungen werden nicht als neue Erfolge umgedeutet.

## Optionale Reviews

`python3 Tools/DevelopmentEvidence/evidence.py status` meldet fehlende optionale Medien getrennt von Pflichtdateien. `EvidenceManifest.json` enthält ausschließlich die 8.580 einzeln klassifizierten D/E/F-Pfade mit Quell-Commit, Größe und SHA-256. Es gibt keine allgemeine Endungsfreigabe für Bilder, Texturen oder FBX. Originaltexturen, Referenzen, Sprites, Importdateien und Testfixtures bleiben Pflichtbestand.

17 alte Report-/Archiv-/Crop-/Static-Library-Einstiegspunkte prüfen ihre optionalen Eingaben vor dem Start. Ohne historische Medien melden sie **REVIEW_NOT_EXECUTED**, statt einen Pflichtdateifehler oder einen erfundenen Testpass auszugeben. `POKEMONSTER_REQUIRE_EVIDENCE=1` macht das Fehlen ausdrücklich zu Exit 2. Swift-Videoencoding meldet fehlende Originalframes ebenso vor dem Anlegen einer Videodatei.

Die konservativen Gruppenbedingungen können einen historischen Report auch dann zurückstellen, wenn nur eine seiner verlinkten Aufnahmen fehlt. Das ist beabsichtigt: fehlende historische Bilder werden nicht durch neue Messwerte oder Platzhalter ersetzt. Bestehende technische Berichte bleiben erhalten.

## Archivzugriff

Das unabhängige Dateiformat ist in `EvidenceManifest.json` beschrieben: große Inhalte unter `lfs/objects/<2>/<2>/<sha256>`, kleine normale Git-Nachweise unter `evidence/<sha256>`. Ein Git-Bundle alleine enthält die LFS-Nutzdaten nicht. Das Archiv muss vollständig kopiert, gehasht und wiederhergestellt getestet sein. Ein Archiv auf derselben SSD ist keine unabhängige Datenträgersicherung.

Einzelnen optionalen Inhalt prüfen:

```sh
python3 Tools/DevelopmentEvidence/evidence.py get 'RELATIVER_MANIFESTPFAD' --archive '/PFAD/ZUM/ARCHIV'
```

Ein Reviewverzeichnis ausschließlich in einen neuen separaten Replayordner materialisieren:

```sh
python3 Tools/DevelopmentEvidence/evidence.py materialize 'Art/Characters/NPCs/Ranger/Review/AnimationV3/Unreal/RecordingClear' --archive '/PFAD/ZUM/ARCHIV' --destination '/NEUER/REPLAYORDNER'
```

Es wird vor dem Kopieren auf Vollständigkeit geprüft; bestehende Zieldateien werden niemals überschrieben. Das Hauptprojekt darf kein Ziel sein; im Worktree ist nur das ignorierte Saved erlaubt. Path-Traversal wird abgelehnt. Zum Wiederholen alter Skripte muss ein separater Replay-Projektbaum mit den erforderlichen Coredateien und explizit materialisierten Medien verwendet werden. Der Resolver schreibt nicht automatisch in Source/Art/Content und greift nicht still auf das alte Hauptprojekt zurück.

Vollständige historische Reportreproduktion und alle alten Generatoren sind noch nicht abgenommen. Einige benötigen Sessiondaten aus Saved oder in RawMeasurements-Archiven und enthalten alte absolute Pfade. Diese Einschränkung betrifft die historische Reviewpipeline, nicht Build oder aktuelle Automationsprüfungen. Originalalgorithmen sind im vollständigen Sicherungscommit erhalten.

## Neue Nachweise erzeugen

Für neue echte Unreal-Aufnahmen die erhaltenen `Tools/RangerAnimationV3/RunFinalRecording.py` sowie Capture-/Setup-Werkzeuge in einer sauberen separaten Editor-Testsitzung verwenden. Die zugehörigen C++-Capturebefehle bleiben unverändert; keine alten Medien als erfolgreiche neue Aufnahme ausgeben. Vor einem neuen Lauf vorhandene Ausgabepfade prüfen; vorzugsweise neue Sessionpfade unter Saved/Review verwenden.

Statische Blender-Reviews werden aus erhaltenen `*_NPC_Source_V1.blend` mit `Tools/MeshyNPCIntegrationV1/StaticReviewExport.py` erzeugt. Vor Ausführung dessen Arbeitswurzel und Exportziele auf die separate Sitzung umstellen; dieser Generator wurde hier nicht ausgeführt oder künstlerisch neu freigegeben.

## Freigabegrenze

Dies sind ausschließlich vorbereitete Änderungen in einem separaten Worktree. Keine Originaldateien wurden bereinigt, kein endgültiger Commit und kein Push erstellt. Vor tatsächlicher Bereinigung oder endgültiger Sicherung ist die ausdrückliche Freigabe erforderlich.
