# Westland Asset Library – V1 / Art Quality V2

Stand: 10.10.2026. V1 gesichert in Git-HEAD `0add5a5`; Art Quality V2 ist ein separater, noch nicht committeter Reviewstand.

## Quellen und Umfang

V1 bleibt unverändert erhalten: `Source/WestlandAssetLibrary_V1.blend`.
Aktuelle Art-Quelle: `Source/WestlandAssetLibrary_V2.blend`. Sie enthält weiterhin dieselben 46 Assets und UCX-Körper, gepackte Texturen sowie getrennte Source-/Review-Szenen. Maße in Metern; Objektursprünge am Boden. Die gespeicherte Datei wurde erneut geöffnet und geprüft.

V2 ersetzt ausschließlich die 20 offenen Meshes aus zehn vorhandenen Typen, jeweils A/B: alte/junge Eiche, Birke, Obstbaum, Busch, Farn, Stumpf, Wurzel, Ruinensäule und Runenstein. Keine neuen Objekttypen. Die übrigen 26 Meshes bleiben erhalten. `Assets.json` dokumentiert Maße, Dreiecke, Materialien, Collision und Qualitätsstatus. Technische Prüfung und menschliche Art-Freigabe sind getrennt; eine finale Referenzqualität wird nicht behauptet.

Unreal: `/Game/Environment/WestlandAssetLibrary`; einzige geänderte Map: `/Game/Maps/Dev_WestlandAssetLibrary`. Reimport erhält die bisherigen Meshpfade und Referenzen. Spieler, Spielkamera und Westland-Region bleiben unverändert.

## V2-Pipeline

1. `Tools/Blender/BuildWestlandAssetLibraryV2.py`: liest die gesicherte V1-Quelle, ersetzt nur die genannten Geometrien und schreibt die separate V2-Datei. Bereits vorhandene eigene V2-Arbeitsstände werden unter Saved gesichert. Keine primitive geschlossene Kronenkugel: verzweigte Stämme, Zweige und gebogene einzelne Blätter.
2. `Tools/Blender/ReviewWestlandAssetLibraryV2.py`: lesendes Wiederöffnen, Audit der 20 Meshes einschließlich UV-Flächen, Normalen, Tangenten und Binormalen nach Triangulierung; Renderprüfung. Blender-Scriptargumente nach `--` übergeben; `-- --surfaces` beschränkt Renderjobs auf die acht Landschafts-/Ruinenvarianten.
3. `Tools/Blender/ExportWestlandAssetLibraryV2.py`: selektiver FBX-Export der geprüften 20 Meshes mit erhaltenen UCX-Körpern und Tangenten. Erfordert die lokale Sichtprüfungsmarkierung unter Saved; diese ersetzt keine menschliche Art-Freigabe.
4. `Tools/ImportWestlandAssetLibraryV2.py`: Reimport nur der 20 bisherigen Assetpfade; vier gemalte Blatttexturen und vier Materialinstanzen. Importierte Normalen/Tangenten und MikkTSpace für die reduzierten LODs. Kein Unterdrücken von Normalenwarnungen.
5. `Tools/ValidateWestlandAssetLibraryV2.py`: vollständiger Editor-/PIE-Audit der Bibliothek und Collision-Sweeps.
6. `Tools/TestWestlandAssetLibraryV2PIE.py`: Fußlauf über Enhanced Input ohne Teleports; tatsächliche Game-Viewport-Aufnahmen und Prüfung der HUD-Eingabesperre.
7. `Tools/MeasureWestlandAssetLibraryV2.py` / `Tools/SummarizeWestlandAssetLibraryV2.py`: CSV-Messungen mit Medium und 75 % Renderauflösung, Vegetations-/Schattenvergleich nur temporär zur Kostendiagnose. Editor-Hintergrunddrosselung muss während der Messung ausgeschaltet sein. PIE und Standalone müssen dieselbe tatsächliche Viewport-Auflösung verwenden, nicht nur dieselben nominellen Fenstermaße.

Jobdateien, Backups, Logs, CSVs und rohe Renderaufnahmen bleiben ausschließlich unter `Saved/WestlandAssetLibraryV2`. Ohne aktiven FootViewJob wird der gesamte Fußlauf ausgeführt. Nullwerte bei nicht unterstützten Draw-Call-Zählern gelten als nicht verfügbar, nicht als kostenlose Szene. Native `DumpDetailedPrimitives`-Diagnose in dieser Engine-Version nicht verwenden: sie verursachte bei dieser Prüfung einen Renderthread-/Slate-Assert.

## Erhaltene frühere Stände

Alle V1-Tools und frühen `HeroReview_V1`-Quellen bleiben erhalten. Das Vorbereitungspaket und sein Katalog bleiben unverändert. Die Bibliothek enthält 24 Grundtypen mit 22 Varianten; weitere Katalogtypen wurden nicht erzeugt.

V1: `Review/Spielkamera_V1.jpg`, `Docs/WESTLAND_ASSET_LIBRARY_V1_PRUEFBERICHT.md`.
V2: `Docs/WESTLAND_ASSET_LIBRARY_ART_QUALITY_V2_PRUEFBERICHT.md`.
