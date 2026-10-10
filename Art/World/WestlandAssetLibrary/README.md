# Westland Asset Library V1

Stand: 10.10.2026; Ausgangs-HEAD `89b475e`. Isolierte Prüf- und Quellbibliothek, keine Integration in die Region.

Verbindliche Quelle: `Source/WestlandAssetLibrary_V1.blend`. Die Datei enthält 46 einzelne, als Assets markierte Meshes in Metern, gepackte Texturen, eine Review-Szene und die separate Source-Szene. Objektursprünge liegen am Boden. Alle Blender-Quellen wurden gespeichert; die verbindliche Quelle wurde nach der letzten Änderung erneut geöffnet.

`Assets.json` enthält die vollständige Liste mit Maßen, Dreiecken, Materialfamilien, UCX-Körpern und Qualitätsstatus. 24 Grundtypen, 22 Varianten. 26 Meshes aus 14 Typen sind für eine V1-Sichtprüfung nutzbar; 20 Meshes aus 10 Typen benötigen weiteren Art-Feinschliff. Keine finale menschliche Art-Freigabe wird behauptet. Baum-/Buschmeshes benötigen zusätzlich eine Untersuchung der verbleibenden Unreal-Normalen-/Binormalenwarnungen.

Unreal: `/Game/Environment/WestlandAssetLibrary`; separate Map `/Game/Maps/Dev_WestlandAssetLibrary`. Native Playerbasis und Spielkamera bleiben unverändert. Die Map verwendet ausschließlich eigene neue Actors und vorhandene Spielsysteme. `Dev_WestlandRegion` wird nicht geändert.

## Pipeline

- `Tools/Blender/BuildWestlandAssetLibraryV1.py`: ursprüngliche Erstellung; schützt vorhandene Quellen vor Überschreiben. Für eine neue Version zuerst einen neuen Quellnamen wählen.
- `Tools/Blender/PackageWestlandAssetLibraryV1.py`: eigene Quelle packen, Geometrie und UV-Endflächen bereinigen, Asset-Metadaten setzen. Sicherungskopie im ignorierten Saved-Ordner.
- `Tools/Blender/ReviewWestlandAssetLibraryV1.py`: lesendes Wiederöffnen, Geometrie-/UV-/Materialaudit und Renderprüfung. `--audit-only` prüft ohne Renderjobs.
- `Tools/Blender/ExportWestlandAssetLibraryV1.py`: geprüfte Quelle selektiv als FBX mit UCX exportieren; keine Lampen, Kameras oder Review-Instanzen exportieren.
- `Tools/ImportWestlandAssetLibraryV1.py`: ausschließlich eigener Assetordner und eigene Testmap; vorhandene Holz-, Stein- und Bodenmaterialquellen bleiben unverändert.
- `Tools/DressWestlandAssetLibraryV1.py`: eigenständiger, nicht kollidierender Review-Weg mit vorhandenen Bodenmaterialien.
- `Tools/ValidateWestlandAssetLibraryV1.py`: Editor- und PIE-Audit; `Tools/TestWestlandAssetLibraryV1PIE.py`: echter Enhanced-Input-Fußlauf ohne Teleports.
- `Tools/MeasureWestlandAssetLibraryV1PIE.py` und `Tools/SummarizeWestlandAssetLibraryV1Performance.py`: getrennte Idle-Messungen und CSV-Auswertung.

Testjob-Dateien liegen ausschließlich unter `Saved/WestlandAssetLibrary`. Ohne aktiven FootViewJob wird der vollständige Fußlauf ausgeführt. Rendering-Kosten werden nicht aus unzuverlässigen Null-Zählern erfunden.

## Erhaltene Entwicklungsstände

`Source/WestlandAssetLibrary_HeroReview_V1*.blend` und `Heroes.json` sind erhaltene frühe Reviewstände, nicht die freigegebene Bibliotheksquelle. Die ersten Kronenfarben wurden verworfen. Diese Zwischenstände nicht mit der verbindlichen V1-Datei verwechseln und nicht automatisch versionieren.

Das ursprüngliche Vorbereitungspaket bleibt unverändert. `CatalogReview_V1.json` ordnet dessen 74 Einträge bestehenden Assets und dem angefragten Umfang zu; weitere 50 Katalogtypen werden nicht als erstellt behauptet. Der optionale primitive Starter wurde nicht als fertige Bibliothek übernommen.

Screenshots: `Review/Spielkamera_V1.jpg`; vollständiger Bericht: `Docs/WESTLAND_ASSET_LIBRARY_V1_PRUEFBERICHT.md`. Rohbilder, Logs, CSVs und temporäre Sicherungen verbleiben unter Saved und gehören nicht in Git.
