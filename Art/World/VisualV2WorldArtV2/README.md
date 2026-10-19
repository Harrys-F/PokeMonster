# World Art Quality V2 – Authoringdaten

Nur der bisherige Heilhausbereich von Dev_TestMap_VisualV2, ungefähr
X −4620…−3560 / Y −720…1190 cm. Keine neue Map.

`BaselineInstances.json` bewahrt alle 175 ursprünglichen V1-Transformationen,
Meshes, Materialbindungen und automatischen LOD-Vorgaben für einen
reproduzierbaren Vorhervergleich. `ArtCandidate.json` enthält alle neuen
Transformationen und vier private Bodenmaterialpfade. Größen und Z-Positionen
bleiben erhalten; nur X/Y und Drehung werden für natürliche Gruppen geändert.
Topfpflanzen sind keine dieser sechs Gruppen und bleiben unangetastet.

`MeshCandidates.json` beschreibt die drei neuen, positionsgleichen
Gras-/Kräutermeshes. Zehn echte LOD0-Abschnitte dieser drei Modelle werden zu
drei Abschnitten; Dreieckzahlen 45/90/100 unverändert. Für alle sechs Gruppen
bedeutet dies **17→10 LOD0-Mesh-Abschnitte**, bei **19→12 Materialzuweisungen
an den Komponenten**. Beim Farn bestehen zwei zusätzliche historische,
ungenutzte Materialzuweisungen; sie sind keine weiteren Renderabschnitte.
Diese Zahlen sind keine gemessene Draw-Call-Zahl.

Keine Originalmesh-, Textur- oder Blenderquelle geändert. Neue Meshes und
Materialien liegen unter Content/Environment/VisualV2WorldArtV2. Rekonstruktion
und geprüfte Verwendung siehe Tools/VisualV2WorldArtQualityV2/README.md.
Kontrollbilder und Rohmessungen sind optional und bleiben außerhalb Git.
