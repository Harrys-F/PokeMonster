# World Art Quality V5 – drei begrenzte Musterbereiche

Nur die bestehende `/Game/Maps/Dev_TestMap_VisualV2`. Keine neue Karte,
keine Änderungen an Gameplay-Code, Kamera, Licht oder ursprünglichen Assets.
Die visuelle Abnahme der drei Musterbereiche durch Harry bleibt offen.

## Dauerhafte Eingaben

- `Art/World/VisualV2WorldArtV5/Source/Westland_ThreeBiomes_Details_V5.blend`:
  selbständige Blenderquelle für Klee, niedriges Moos und Schilf; Vertexfarben,
  keine externen Texturen erforderlich. Keine bestehende Blenderquelle verändert.
- `Exports/`: drei notwendige FBX-Importquellen, keine Review-Zwischenexporte.
- `Textures/`: zwei neue gemalte Bodenalbedos; Ausgangsgröße jeweils 1254²,
  in Unreal mit Power-of-two-Stretch, maximal 2048. Keine echten 4K-/2K-Quellen.
- `TexturePrompts.json`: tatsächliche Imagegen-Prompts. Die Wiese nutzt die
  vorhandene Heilhaus-V4-Grastextur; weitere Originalassets bleiben referenziert.
- `Details.json`, `AssetManifest.json`, `RegionalMasks.hlsl`, `Scope.json`:
  gemessene Geometrie, Materialübertragung und alle örtlichen Platzierungen.

## Sichere Arbeitsfolge

`Startup.py` richtet eine Dateiwarteschlange nur für einen ausdrücklich gestarteten,
sauberen Editor dieses Worktrees ein. Offene fremde Sitzungen werden nicht verworfen.
`Inventory.py` liest die vorhandene Welt. `PrepareAssets.py` legt private Varianten
an; `ApplyCandidate.py` lässt ausschließlich vier Bodenmaterialbindungen und neue
kollisionsfreie HISM-Gruppen zu. Dieses Skript ist **kein beliebig wiederholbarer
Dresser**: Es benötigt den ursprünglichen Vorher-Snapshot und darf nicht erneut
auf die bereits bearbeitete Karte angewandt werden. Keine pauschale Speicherung.
`SaveReviewed.py` speichert ausschließlich die ausdrücklich geprüfte zentrale Karte.

`BuildDetails.py` läuft nur in einem separaten Background-Blender, verweigert
Überschreiben der Quelle und erzeugt keine Spielkamera-Nachweise.
`BlenderAudit.py` öffnet die Quelle erneut ausschließlich lesend.
`VerifyAssets.py` vergleicht den echten Unreal-Import mit den Quellmaßen/-Dreiecken.

## Tatsächliche Sicht- und Funktionstests

- `RunPIEReview.py <1|2> <Phase>`: eingebetteter PIE, ausschließlich QHD / 100 %.
- `RunNativeReview.py <1|2> <Phase>`: bestehende Map im nativen `-game`-Betrieb;
  kein gekochter Shipping-Build. Keine parallele Editorinstanz.
- Qualitätsstufe 1 = Medium, 2 = High. Ein frischer Prozess pro Qualitätsstufe;
  kein riskanter Live-Wechsel der Metal-Scalability.
- Vier feste Fotopositionen: Wald, Wiese, Flussufer und Heilhaus-Kontrolle.
  Fotos nutzen reproduzierbare Positionssetzung; das ist ausdrücklich vom
  echten Enhanced-Input-Fußlauf ohne Test-Teleports getrennt.
- `RunAcceptance.py PIE <eindeutiges Label> 2560 1440 100` verwendet die bestehende
  vollständige Gameplay-Prüfroute. Vorhandener Dev-Slot wird gesichert und nach
  Erfolg bytegleich restauriert; ursprüngliche Abwesenheit ebenfalls hergestellt.
- `Build.py`, `RunQA.py Automation`, `RunMapCheck.py`: reale Prüfungen;
  Map Check lädt den gespeicherten Stand neu und vergleicht den Szenensnapshot.
- `ComposeReview.py`: nur gleichskalierte echte QHD-Bilder und unveränderte
  Originalpixel-Ausschnitte, kein generierter Ersatz für Unreal-Aufnahmen.

## Nachweise und Grenzen

Laufzeitausgaben ausschließlich `Saved/VisualV2WorldArtV5/` und extern
`/Users/harry/Documents/Codex/PokeMonster_WorldArt_V5_2026-10-19/`.
Kein Build-/Gameplaytest setzt die Existenz optionaler Kontrollmedien voraus.
Keine FPS-Benchmarks, GPU-Profile oder Leistungsgewinnaussagen.
Prüfbericht: `Docs/VISUALV2_WORLD_ART_QUALITY_V5_PRUEFBERICHT.md`.
