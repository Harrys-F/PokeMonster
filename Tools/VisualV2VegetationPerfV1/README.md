# VisualV2 Vegetation Performance V1

Explizite Diagnose auf der **vorhandenen** `/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1`.
Keine Map-Erstellung und kein Map-Save. Die zentrale VisualV2 bleibt bytegleich.
Der vorhandene GPU-Probe wählt temporär TAA; der Renderthread bestätigt Methode 2.
Licht, Postprocess, Lumen, Bloom und Schattenflags bleiben unverändert.

## Kandidaten

- `VegPerf:Control`: unveränderte Vegetation mit TAA.
- `VegPerf:FullyRough`: zwei separate, graphgleiche Materialmaster mit ausschließlich
  dem Compile-Flag `fully_rough`. Texturen, Maskierung, Vertexfarbe und Reveal-Code
  bleiben erhalten. Laufzeit-MIDs kopieren die Originalparameter und spiegeln die
  originale Reveal-Stärke. Das zusätzliche Diagnose-Update ist kein kostenloses
  Produktionssystem; seine CPU-Kosten bleiben in der Messung enthalten.
- `VegPerf:TreeLOD1` / `VegPerf:BushLOD1`: vorhandene LOD1 nur temporär erzwingen.
  Dichte und Schattenkonturen müssen visuell beurteilt werden. Kein neuer LOD wird
  erzeugt oder automatisch übernommen. Ein LOD-Versuch ist keine Artfreigabe.

Alle Faktoren werden zwischen den Zeilen und beim Beenden vollständig restauriert.
Der C++-Pfad ist nur bei explizitem Label `VGB1_Vegetation_` und exaktem GPU-Testmap-
Pfad aktiv. Keine Änderung an der Produktions-Freistellung oder Gameplayklassen.

## Ablauf

1. `LaunchEditor.py <neues_Loglabel>` startet eine bewachte lokale Editorqueue.
   Niemals eine fremde offene Sitzung schließen/verwerfen.
2. `Inventory.py` und `CompareMaps.py`: lesende Bestandsaufnahme. Die referenzierte
   NPC-Actor-Adresse unterscheidet sich wegen des Mapnamens; ansonsten nur der neue
   zentrale TAA-Blendable. Kein Save.
3. `PrepareCandidates.py` dupliziert nur die zwei Testmaster, prüft Graphgleichheit
   und speichert ausschließlich die zwei neuen Materialpakete.
4. `MakePlans.py Scout` / `MakePlans.py Matrix FullyRough`: getrennte Faktoren,
   dreimal AB/BA/AB pro Dorf/Wald/Weg, fünf Sekunden Warm-up + vier Sekunden Messung.
   `repeat=90` ist ausschließlich Foto, `repeat=99` CSV-Auslauf. Beide ausschließen.
5. `RunMatrix.py PIE` und bei geschlossenem Editor `RunMatrix.py Standalone`.
   Acht Konfigurationen je Modus: 720p/QHD × Medium/High × 75/100 %. Qualität vor
   jedem neuen PIE setzen, niemals während lebender Reveal-MIDs wechseln.
6. `Analyze.py --final` verlangt vollständige tatsächliche Renderer-AA-, Auflösungs-,
   Kamera-, Shaderzuordnungs- und GPU-CSV-Nachweise. Keine fehlenden Zeiten schätzen.
7. Reale Bewegungsfolgen und bestehender vollständiger Input-Fußlauf; Dev-Spielstand
   vorab sichern und danach exakt wiederherstellen. Profilingteleports nie als
   Gameplay-Fußlauf ausgeben.
8. Bei geschlossenem Editor vollständige Automation und Map Checks. Eigenen
   Mac Development Editor Build bei Probe-Änderung durchführen.

Native `-game` bedeutet Development mit Editorbinary, kein Shipping-Build. Interne
Pixelmaße stammen aus tatsächlichen Renderer-Fractions, nicht direktem SceneColor-
Allocation-Readback. GPU-Scopes können sich überlappen und dürfen nicht summiert
werden. Null-RHI-/Samplerwerte sind kein Nachweis kostenloser Renderarbeit.
Atlas-Alpha-Belegung und Shaderinstruktionen sind keine GPU-Overdraw-/Zeitmessungen.
Keine Windanimation behaupten, wenn die Materialgraphen kein WPO besitzen.

Bilder, Videos, CSV-Rohdaten, Logs, Caches und lokale Sicherungen gehören unter
`Saved/VisualV2VegetationPerfV1` beziehungsweise in den externen Nachweisordner,
niemals in den Commit. Ein fehlender optionaler Bildnachweis ist kein Buildfehler.
