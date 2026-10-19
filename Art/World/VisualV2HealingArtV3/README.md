# Heilhaus Art V3 – private Quellen

Nur der bestehende Heilhaus-Außenbereich von `/Game/Maps/Dev_TestMap_VisualV2`.
Keine Freigabe zur Ausweitung auf weitere Gebiete.

- `Source/HealingHouse_PottedPlants_V3.blend`: fünf bearbeitbare botanische Varianten,
  Metermaßstab, gepackte vorhandene Terracotta-Textur, eigene Studiovorschau.
  Bestehende handgeformte Q3-Töpfe übernommen; neue Stängel und Blattflächen.
- `Exports/`: fünf benötigte FBX-Importquellen, Ursprung jeweils am Topfboden.
- `Textures/`: zwei neue flache, handgemalte Albedo-Quellen. Tatsächlich 1254² Pixel;
  Unreal importiert sie gestreckt auf Zweierpotenz mit maximal 2048². Keine echte
  native 2K-Detailauflösung behauptet. Keine eingebrannte Studiobeleuchtung beabsichtigt.
- `TexturePrompts.json`: vollständige Prompts und Herkunft aus dem eingebauten Imagegen.
- `Plants.json`: Blender-Messdaten. `AssetManifest.json`: Unreal-Pfade.
- `Scope.json`: ursprüngliche Materialbindungen, Topftransformationen und Würfelbefund.
  Zusammen mit dem vorherigen Git-Commit erlaubt das gezielte Rücknahme der Änderungen.

Die privaten Unreal-Varianten liegen unter `/Game/Environment/VisualV2HealingArtV3`.
Alle anderen Originalquellen und gemeinsamen Materialien bleiben erhalten.
Blätter sind bewusst offene, beidseitig dargestellte Flächen ohne Alpha-Blatttexturen.
Die UVs der flachen Topfringe sind planar; die zylindrischen Wand-UVs bleiben erhalten.
FBX-Vertexfarben werden im Unreal-Blattmaterial explizit von sRGB nach linear übertragen.

Vorschauen und Rohprüfdaten liegen lokal in `Saved/VisualV2HealingArtV3` sowie außerhalb
von Git im im Prüfbericht genannten Abnahmeordner. Sie sind keine Build-Abhängigkeit.
