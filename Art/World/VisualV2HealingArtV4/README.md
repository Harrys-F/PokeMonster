# Heilhaus Art Quality V4

Begrenzte, eigenständige Artvarianten für die bestehende Dev_TestMap_VisualV2.
Rechte Hälfte der vom Nutzer gelieferten Konzeptillustration ist Ziel, kein Unreal-Nachweis.
Die Originalreferenz liegt unter References/Heilhaus_V4_UserTarget.jpg.

## Bearbeitbare Quellen

- Source/HealingHouse_PottedPlants_V4.blend: fünf botanische Topfvarianten, bestehende Q3-Keramik übernommen; Textur gepackt.
- Source/HealingHouse_GardenDetails_V4.blend: sechs Kräuter-, Gras-, Efeu- und Steinvarianten; keine Gebäude- oder Kollisionsgeometrie.
- Exports/: elf benötigte, getrennte FBX-Importquellen, Unreal-Zentimeterkonvertierung.
- Textures/: drei tatsächlich 1254² große Albedoquellen. Imagegen-Prompts und Herkunft in TexturePrompts.json; keine native 2K-Quelle behauptet.
- AssetManifest.json: private Unreal-Pfade. Scope.json: konkrete Bindungen und zusätzliche Instanzpositionen.
- GroundChanges.json: nachvollziehbare lokale Materialänderung; die abschließende visuelle Verfeinerung ist zusätzlich in Tools/VisualV2HealingArtV4/RefineCandidate.py festgehalten.

Bestehende V1–V3-Quellen und gemeinsam genutzte Importassets bleiben erhalten.
Die Fassadenform bleibt vollständig bestehen. Private Materialgraphen übernehmen HouseCutaway.
Die Lichtstimmung wird nicht anhand des Konzepts umgebaut. Keine Leistungsvereinfachung/Benchmarks.

## Wiederherstellung / Reproduktion

Die finale Quelle ist direkt bearbeitbar und hat Vorrang vor blindem Neuausführen von Herstellskripten.
BuildPlants -> BuildDetails -> FixIvyPlacement -> CurlIvy dokumentieren die gezielten Blender-Schritte.
FixIvyPlacement verlegt die flachen Blätter um 3,5 cm unter der beibehaltenen Actor-Skalierung an die alte sichtbare Vorderkante;
CurlIvy neigt die echten Blattflächen nach oben. Kein Licht und keine Actor-Position wird dafür geändert.
Herstellskripte verweigern unkontrolliertes Überschreiben; nicht auf dem fertigen Stand erneut ausführen.
Keine Kontrollmedien oder optionale Saved-Diagnosen als Build-Abhängigkeiten.

Vollständige Abnahme und Einschränkungen: Docs/VISUALV2_HEILHAUS_ART_QUALITY_V4_PRUEFBERICHT.md.

CorrectLegacyWindows.py ergänzt die abschließende Korrektur der acht alten Fensterpflanzen; 28 ovale Grundkörper bleiben unsichtbar erhalten. Ihre frühere Meshbindung, Lage und Skalierung sind in Scope.json dokumentiert.
