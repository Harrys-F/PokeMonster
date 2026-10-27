# VisualV2 Performance V1 – begrenzte Entwicklungsprüfungen

Produktionsänderung: ausschließlich vier Materialslots auf VisualV2 plus eine
map-spezifische 4096²-BC7-Farbtextur. `Art/World/VisualV2PerformanceV1/Bake.json`
dokumentiert Herkunft, Weltbereich und Neuberechnungsgrenzen. Keine Lichtdaten
oder Szenenaufnahmen in der Textur. Normalen, Roughness, dynamische Beleuchtung,
Schatten, Wege, Vegetation, Gameplay, Kamera und Projektqualität bleiben erhalten.

Alle Befehle aus dem bestehenden Projektordner; UE 5.8.2. Werkzeuge starten keine
zweite Instanz, beenden keine fremden Prozesse und erzwingen kein Prozessende.
Prüfmedien, CSV und eigene isolierte `.sav` bleiben unter `Saved`, außerhalb Git.
`Baseline.py` einmal **vor** Änderungen ausführen; eine bestehende Baseline wird
niemals überschrieben. `VerifyProtection.py` vergleicht ursprüngliche Dateien.

## Reproduzierbarer Messablauf

1. Bei geschlossenem Editor `python3 -B Tools/VisualV2PerformanceV1/StartSession.py <neuesLabel>`.
2. Queue bereit abwarten (`Saved/ProjectRefinement/Ready.json`, PID kontrollieren).
3. `PrepareRequest.json` im eigenen Saved-Unterordner mit einem neuen
   `PokeMonster_SaveV2_Test_Perf...`-Slot und `disable_contacts: true` schreiben.
4. Über `Tools/ProjectMaintenance/ArtControl.py script .../PrepareGameplay.py`
   den frühen Guard anmelden, anschließend `ArtControl.py start_pie`.
5. `MakePlans.py <neuesPräfix>` erstellt ausschließlich explizite Messpläne.
   `Run.py <Plan.json>` misst echtes PIE. 4 s Warmup + 6 s Messung, drei Läufe
   bei den Standardplänen. `OriginalGround` stellt nur während der Messung die
   Original-Bodenfarbe wieder her; `BakedSRGB` verwendet die Optimierung.
6. Native Vergleichsmessungen: PIE regulär stoppen, `CloseClean.py` über Queue,
   dann `ArtControl.py close`. `RunNative.py <NativeMatrixPlan.json>` startet
   den Editor-Binary als separaten `-game`-Prozess mit eigenem `UserDir`.
   **Kein gepackter Shipping-Build.** Er kopiert ausschließlich die explizit
   selbst erzeugte Fixture `PerfOptimization01`; niemals einen Nutzerspielstand.
   `NativeFixture.py` erzeugt diese über das vorhandene Save-System in einem
   frischen, entsprechend isolierten PIE. Sie bleibt Ausgangsquelle, keine
   nachfolgenden Gameplayprüfungen in diesen Slot schreiben.
7. `Analyze.py` prüft reale Viewport-/interne Auflösung, Kamera, Qualität, TAA
   und wertet Frame-/GPU-/CPU-CSV aus. Alternative Pläne sind ausdrücklich
   Medium beziehungsweise 75 % intern und keine unveränderte QHD-High-Referenz.

Jeder Native-Fall lädt die eigene Noon-Fixture über das vorhandene Save-System;
Uhr, Team und Uhrzeit starten damit identisch. A/B/B/A/A/B-Reihenfolge mildert
Drift, beseitigt sie nicht. NSProcessInfo-Thermalstatus wird alle 5 s protokolliert;
daraus folgen keine gemessenen GPU-Taktraten. RenderThreadTime enthält Wartezeiten.

## Bildprüfung und Übernahme

`Photos.py` erzeugt echte QHD-Paare bei eingefrorener Welt/Kamera, aber außerhalb
der Leistungsfenster. Keine künstlichen Bilder. `BakeGroundSRGB.py` ist ein
**einmaliger, geschützter Erzeugungsschritt für frische Zielnamen**; er überschreibt
keine existierenden Assets. Bei späteren Material-/Weltbereichsänderungen muss die
Farbe erneut gebacken, verglichen und gezielt zugewiesen werden. Kein automatischer
Reimport beim Spielstart. `ApplyReviewed.py` speichert nur die vier vorab festgelegten
Slots und vergleicht alle übrigen von `AuditScene` erfassten Szeneneigenschaften.

`PrepareCandidate.py`, `SpatialRoute.py`, `BuildRouteField.cpp`, `PrepareField.py`
und `BakeGround.py` dokumentieren die verworfenen BVH-/Distanzfeld-/Linearfarbversuche.
Ihre Assetentwürfe wurden nicht übernommen. `Inspect*` und `ModeAudit.py` sind
reine Entwicklungsabfragen. Keine dieser Alternativen ist ein Produktions-Fallback.

## Regression und Grenzen

`RunRegression.py` verwendet neue isolierte Slots für Gameplay, Tag-/Nacht-KI,
sieben Start-Stopp-Fälle und realen Map-Rundlauf. Die bekannten nativen Fixtures
und Eingabesimulationen werden wiederverwendet. Physische Controllerfunktion wird
dadurch nicht bewiesen. `MapChecksFinal.py` lädt zwölf bestehende Maps lesend.
Build und vollständige Automation laufen bei geschlossenem Editor über den
unveränderten strengen `Tools/ProjectMaintenance/ProjectQA.py`.
Ein Wrapper-Exit 1 bleibt ein Fehlschlag des strengen Wrappers, auch bei funktional
erfolgreichen Tests mit externen iOS-Helferwarnungen.

Messungen sind Stichproben eines M4 Air mit 16 GB. Langsitzungsdrift, dynamische
Pokémon und Editor-/Spielprozessunterschiede werden im Bericht getrennt behandelt.
Kein garantierter 30-/60-FPS-Nachweis, kein vollständiger CPU-Busy-/Overdraw- oder
Speicherbandbreitenbeweis aus ungeeigneten Zählern.
