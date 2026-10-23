# Glutexo-Integration und Entwicklungen V2

Nur im bestehenden Projekt. Keine neue Map; das native VisualV2-PIE-Testgelände erhält Platz 11.

## Quellen und Import

`InspectSource.py` liest ausschließlich `Incoming/Glutexo.glb`, erzeugt Blender-Diagnosebilder und einen SHA-256-Intake unter Saved. `Anatomy.py` enthält am tatsächlichen Modell eingepasste eigene Landmarken. Die Vorbereitung verwendet vorhandene automatische Gewichts- und Glättungshelfer, ergänzt eine eigene Schwanz-/Flammenkette und behält Vertices, UVs und Originalbilder. Die sieben Rollen verwenden die vorhandene in-place IK-Exporttechnik mit Glutexos eigener Armhaltung und Referenzgeschwindigkeiten 30/60 cm/s. Das ist keine Änderung der Spielerbewegung.

Blender-Hintergrundablauf: `PrepareSource.py -- Glutexo`, `AnimateSource.py -- Glutexo`, `ValidateSource.py -- Glutexo NEUERLABEL`. Alle laufen mit `--background --python-exit-code 3`. Vorhandene neue Arbeitsquellen werden nur mit ausdrücklich gewähltem `--revise-generated` ersetzt; diese Option ist keine allgemeine Reimportfreigabe. Incoming bleibt unverändert. `ValidateSource` öffnet die gepackte Quelle erneut, prüft identische UVs/normalisierte Gewichte und importiert alle sieben FBX tatsächlich erneut. Diagnosebilder sind keine Unreal-Nachweise.

`ImportAssets.py` ist ein einmaliger, zielgeschützter Einzelimport in `/Game/Characters/Creatures/Glutexo/MeshyV1`. Request: `Saved/GlutexoEvolutionV2/ImportRequest.json` mit `{"species":"Glutexo"}`. Vorhandene Zielassets werden abgewiesen. Kein Reimport vorhandener Pokémon. Gen-2-Artwerte und Lernliste sind durch feste Referenz-URLs/Hashes in `ReferenceSources.json` belegt. Alle Attacken werden anhand ihrer stabilen IDs aus dem bereits vorhandenen produktiven V4-Bestand aufgelöst; keine zweite Attackendatenbank.

## Wiederholbare Prüfungen

Saubere Editorsitzung über vorhandene `ArtSession.py`/`ArtControl.py` starten. `RunReview.py Glutexo NEUERLABEL` prüft tatsächliche native Bewegung am normal verfügbaren Testgelände, QHD-Spielkamera, beide ClassicBattle-Perspektiven und Reaktionsclips. Wildakteure werden ausschließlich in dieser isolierten PIE-Prüfung gesperrt. Das ist keine natürliche Habitat-Abnahme.

`RunCapture.py NEUERLABEL` verwendet eine ausdrücklich angepasste vorhandene PIE-Wildinstanz als Glutexo-Quellakteur, normale Art-Startlevel, 1-KP-Fangziel und kontrollierten Seed. Fangtransfer, Quellakteur-Entfernung, Teamwechsel, Heilung und Save/Load werden real geprüft. Das ursprüngliche Dev-Save wird mit Prüfsummenüberwachung restauriert. Es wird kein dauerhaftes Wildhabitat verändert. Physische Controllerprüfungen sind damit nicht behauptet.

`MapChecks.py` lädt und prüft alle elf vorhandenen Karten ohne Speicherung. Build/Automation laufen durch `Tools/ProjectMaintenance/ProjectQA.py` im geschlossenen Editor. Medien und Rohlogs bleiben unter Saved und werden nicht hochgeladen.
