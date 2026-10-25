# VisualV2 Environment Quality V3

Ausschließlich die vorhandene `/Game/Maps/Dev_TestMap_VisualV2`. Quellen in
`Art/World/VisualV2EnvironmentV3`, eigene Laufzeitassets in
`/Game/Environment/VisualV2EnvironmentV3`. Keine neuen Plugins oder Maps.

Die gespeicherte Karte ist das Ergebnis; beim normalen PIE-Start ist kein
Aufbau- oder Debugbefehl nötig. `Scope.json` enthält jede neue Instanz und
jede ursprüngliche/neue Materialbindung sowie die einzige Lichtänderung.
Ein regulärer Git-Revert des Arbeitspakets stellt den Ausgangsstand wieder her.
Keine Originalassets wurden reimportiert.

Autorenfolge (bewusst gegen versehentliche Wiederholung gesperrt):
`Baseline.py`, Blender `BuildGrass.py`, Editor `Inspect.py`, `Apply.py`,
`Polish.py`, `WaterFinish.py`, `Validate.py`. Nur auf dem passenden unveränderten
Ausgangsstand anwenden, niemals blind erneut auf die fertige Karte.
`BuildGrass.py` erzeugt drei echte gebogene, opaque Grashalmvarianten mit
28/37/31 Halmen, höchstens 33 cm Ausgangshöhe. Keine Alpha-Blattkarten,
keine zusätzlichen Blattschatten. Bestehende Geometrie und Kollision erhalten.

Prüfung im bestehenden guarded `ArtSession`/`ArtControl`:

- `Photos.py`: ordinary PIE, echte QHD-Spielkamera, explizite Fotopositionierung,
  kein als Fußlauf ausgegebener Teleport. Anfrage `Saved/ProjectRefinement/EnvironmentV3/PhotoRequest.json`.
- `Footrun.py`: 67-Schritt-Eingabe-/Physikroute, nur Startaufstellung vor dem
  Lauf, danach ausschließlich reale Bewegung und vorhandener Innenraumübergang.
  B-Interaktion, Menü, Sprint, zufälliger Wildkampf und RAM-Save/Load.
- `Motion.py` / `EncodeMotion.py`: echte dargestellte Slate-Frames, zeitgestempelt,
  keine Zwischenbilder. Zeitlupe nur bei Aufnahme; Wiedergabe mit Spielzeitstempeln.
  Kein Echtzeit-FPS-Benchmark. Videoauflösung entspricht dem tatsächlichen Slate-Ausschnitt.
- `MapChecks.py`: alle zwölf bestehenden Karten, rein lesend, Rückkehr zur Ausgangskarte.

Spielstandschutz verwendet ausschließlich den bereits vorhandenen
`PokeMonsterNPCTestGround`-RAM-Preview-Guard. Keine Save-Dateikopien oder
Rückschreibungen. Temporäre Fotopositionierung/Renderwerte/Throttle werden
restauriert; keine Eingabe- oder Kamerakonfiguration gespeichert.

Kontrollmedien, Shaderdiagnosen und ausführliche Logs bleiben unter `Saved/`
und werden nicht versioniert. Build/Automation über den unveränderten
`Tools/ProjectMaintenance/ProjectQA.py`; externe Warnungen und tatsächliche
Fehler getrennt auswerten. Ein strenger QA-Exit 1 ist kein vollständiger Pass.
