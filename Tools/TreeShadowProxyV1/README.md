# Begrenzter Baumschattenversuch V1

Gespeichertes Ergebnis: `/Game/Maps/Dev_TestMap_TreeShadowProxyV1`.
Nur `V2_ForestOak_0`, `_1`, `_2` sind umgestellt. Sechs Actors im Ordner
`TreeShadowProxyV1_ShadowOnly` werfen versteckt Schatten; Originale bleiben
sichtbar und kollidierbar. Die sichtbaren Hilfsobjekte im normalen Editor
sind im Spiel ausgeblendet. Keine Laufzeitsteuerung oder neue Gameplayklasse.

Bericht und echte Bilder: `Art/World/TreeShadowProxyV1/Review/PRUEFBERICHT.md`.
Die Variante ist ein Experiment und nicht für die übrige Welt freigegeben.
Die Schattenschale ist auf die vorhandene feste Sonnenrichtung abgestimmt.

## Werkzeuge

- `BuildProxy.py`: separater Blender-Hintergrundprozess mit der unveränderten
  `WestlandAssetLibrary_V3.blend` als lesender Quelle. Erzeugt nur eine neue
  geschlossene opaque Krone und eine Kopie des Bark-Bereichs. Verweigert das
  Überschreiben einer bestehenden Arbeitsdatei.
- `CreateMap.py`: neue Karte über die Editor-API; verweigert vorhandenes Ziel.
- `ImportAndPlace.py`: nur neue Assets; drei Originalkomponenten in der neuen
  Karte erhalten `CastShadow=False`. Die Schattenhelfer bekommen dauerhaft
  das Profil `NoCollision`; der Kronenversatz folgt der vorhandenen Lichtachse.
- `ReopenBlenderAudit.py`: gespeicherte Blenderdatei lesend erneut prüfen.
- `ValidateMap.py`: sichtbare Actors mit VisualV2 vergleichen, Bark-Vertices
  mit Toleranz prüfen, WPO-Anbindung auslesen, Map Check anfordern.
- `PrepareEditor.py`, `Queue.py`, `Control.py`, `RunInEditor.py`, `MCPClient.py`:
  explizit gestartete, lokal begrenzte Editor-Steuerung. Keine automatische
  Ausführung beim Laden einer Karte. Aktueller lokaler MCP-Port steht in
  `Saved/TreeShadowProxyV1/Endpoint.json`.
- `RunMatrix.py`, `PresetBeforePIE.py`, `Benchmark.py`: sechs Konfigurationen
  mit jeweils drei AB/BA-Paaren. Nutzt den bereits vorhandenen nativen
  `pm.EnvPerf2`-Messbefehl, ohne dessen C++ zu verändern. Ergebnisse liegen
  zunächst unter `Saved/EnvironmentPerfV2/TreeShadowProxyV1_C*` und werden
  getrennt archiviert. Vorhandene Messlabels werden nicht überschrieben.
- `Analyze.py`: prüft Ausgaben, Renderer-Fractions, Kamerapose, Vordergrund
  und Wiederholungen; wertet nur vorhandene Frame-/GPU-Zähler aus.
- `MatchedShotsAndGPU.py`: separate Bild-/GPU-Profilaufnahmen; der Zustand
  wird nach asynchronem Request zwei Sekunden gehalten. Nicht zur FPS-Messung.
- `WalkBy.py`: echter Enhanced-Input-Fußlauf vom vorhandenen Start zur Gruppe
  und zurück durch den Wald; keine Teleports während des Tests.
- `PrepareSlope.py`, `CaptureSlope.py`, `RemoveTemporarySlope.py`: temporäre,
  eindeutig markierte 8°-Empfängerfläche ausschließlich in der neuen Testkarte.
  Nicht speichern; nach dem Sichttest entfernen und Karte erneut prüfen.
- `RunAutomation.py`: vorhandene Projekt-Automation im separaten NullRHI-Prozess.
- `PackageEvidence.py`: Rohdaten, echte Bildfolge und ausgewählte PNGs sichern.
  Benötigt Pillow aus dem vorhandenen Codex-Arbeitsruntime, keine Installation.
- `WriteReport.py`: Bericht aus tatsächlich vorhandenen Ergebnissen schreiben.
- `FinalReadOnly.py`: gespeicherten Zustand nach Editor-Neustart prüfen.

## Wichtige Grenzen

Nur eingebetteten PIE benutzen. Qualität **vor** PIE einstellen und Shader
fertigstellen lassen: ein High→Medium-Wechsel während PIE hat in dieser
Engine-/Reveal-Konfiguration eine UniformExpressionCache-Assertion ausgelöst.
Keine verschobenen Kamera-/Auflösungsvergleiche als Leistungsgewinn ausgeben.
Die Messhilfe setzt ihr altes V1-Profil kurzzeitig; der Test überschreibt auf
jeder A- und B-Zeile ausdrücklich dieselben vier auditierten VisualV2-Werte.
Diese gemeinsamen Overrides stehen im Bericht und den Messplänen.

Prototyp-Skripte und verworfene Aufnahmen wurden nicht gelöscht; sie bleiben
unter `Saved/TreeShadowProxyV1/PrototypeScripts` beziehungsweise
`RejectedImmediateSwitch` erhalten. Sie sind keine freigegebenen Ergebnisse.

Kein Commit, kein Push. Keine verbindliche Projektentscheidung geändert.
