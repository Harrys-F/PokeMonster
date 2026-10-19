# World Art Quality V6 – Wege und drei bestehende Musterbereiche

Nur `/Game/Maps/Dev_TestMap_VisualV2`, keine neue Karte. V5 ist die gesicherte
Vorherreferenz. Keine Änderung an Gameplay, Kamera, Navigation, Licht oder
Originalschatten. Keine FPS-/GPU-Benchmarks.

## Benötigte Eingaben und Ergebnis

Die drei neuen Boden-/Wegmaterialien unter `/Game/Environment/VisualV2WorldArtV6`
kopieren die V5-Materialien unabhängig und verwenden ausschließlich vorhandene
V4-/V5-Texturen. **Keine neuen Modelle oder Texturen.** Blenderquellen werden
wiederverwendet und nicht neu gespeichert oder geändert.

`Art/World/VisualV2WorldArtV6/RouteField.json` enthält die tatsächlichen vorhandenen
Catmull-Rom-Wegkurven als begrenztes Distanzfeld mit maximal 4 cm gemessener
Abweichung von den bestehenden Wegmesh-Samples. `RouteField.hlsl` und
`SurfaceColor.hlsl` sind die reproduzierbaren Materialeingaben. Sie werden in
Custom-Nodes eingebettet, kein absoluter Shader-Include zur Laufzeit benötigt.
`BuildRouteField.py` reproduziert diese Eingaben ausschließlich in einem neuen
lokalen Saved-Unterordner, ohne vorhandene Autorenquellen zu überschreiben.
`AssetManifest.json` dokumentiert Vorher-/Nachhergraphen und ursprüngliche
Opacity. Die sichtbare Breite wird geändert, **keine begehbare Bodenkollision**.
Der zusätzliche Kreuzungsbereich bleibt auf die unmittelbare Anbindung der
Wiesenmusterwege begrenzt. Direkter Brückenbereich ist ausgenommen.

`Scope.json` dokumentiert vier Materialbindungen und die neuen Transformationen
von 399 vorhandenen Instanzen in 16 V5-Gruppen. Acht Wurzelinstanzen bleiben
unverändert. Alle 17 Komponenten/407 Instanzen, Meshes, Materialien, Collision,
Schattenvorgaben und Actor-Identitäten bleiben erhalten. Keine zusätzlichen Actor.

## Sicherer Autorenablauf

1. Sauberer schlanker Worktree, remote und Backup prüfen, aktuelle Karte extern
   sichern. Fremde offene Editoränderungen niemals verwerfen.
2. `LaunchEditor.py` / `Startup.py` erzeugen nur eine kontrollierte Jobwarteschlange.
   `Inventory.py` liest die bestehende Welt; kein Save All.
3. Vorherfotos mit `RunPIEReview.py` bzw. `RunNativeReview.py`; QHD, echte Kamera B.
   Ein frischer Editorprozess pro Scalability, kein riskanter Live-Wechsel.
4. `PrepareAssets.py`: nur drei neue private Materialien. Ein frischer Aufruf
   verweigert bereits bestehende V6-Assets; Wiederaufnahme nur in der ausdrücklich
   markierten eigenen unvollständigen Sitzung. Keine Original-Asset-Speicherung.
5. `ApplyCandidate.py`: nur auf die tatsächliche gesicherte V5-Baseline, exakt vier
   Bindungen und 16 getaggte Visual-only-Gruppen. Kein beliebig wiederholbarer
   Dresser; verweigert Wiederanwendung auf den bereits bearbeiteten Stand.
6. Kandidaten aus der Spielkamera beurteilen. Erst danach `SaveReviewed.py`:
   ausschließlich die geprüfte zentrale Karte speichern.
7. `VerifyMaterials.py`, Build, vollständige Automation, frischer Map Check,
   vollständiger Gameplay-Fußlauf mit Dev-Slot-Sicherung/Wiederherstellung.

## Echte Bildnachweise und Tests

Fünf feste Ansichten: Wald, Wiese, Flussufer, Kreuzung und Heilhaus-Kontrolle.
Finale Vorherphase `BeforeFinal2` (erster Kreuzungsstandpunkt war verdeckt),
Nachherphase `AfterFinal`. Medium/High, eingebetteter PIE und nativer `-game`-
Betrieb; letzterer ist kein Shipping-Cook. PNG und Viewport QHD, Primary und
Secondary 100 %, DynamicRes 0. Foto-Positionssetzung ist vom echten Enhanced-
Input-Fußlauf ohne Testteleports getrennt.

`RunAcceptance.py PIE <eindeutiges Label> 2560 1440 100` verwendet die bestehende
vollständige Gameplayroute. Keine Änderungen am Spieler-/Speichersystem.
`ComposeReview.py` kombiniert nur echte gleichskalierte Bilder bzw. unveränderte
Originalpixel-Ausschnitte; keine Retusche oder generierten Unreal-Nachweise.

Lokale Ausgaben: `Saved/VisualV2WorldArtV6/` und extern
`/Users/harry/Documents/Codex/PokeMonster_WorldArt_V6_2026-10-19/`.
Kontrollmedien sind optional und keine Build-Abhängigkeit; nicht in Git aufnehmen.
Prüfbericht: `Docs/VISUALV2_WORLD_ART_QUALITY_V6_PRUEFBERICHT.md`.
Nach den drei Musterbereichen stoppen; visuelle Freigabe bleibt offen.
