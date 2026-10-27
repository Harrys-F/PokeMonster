# Variante C / 75 % – TAAU gegen TSR

27.10.2026, unveränderter produktiver Stand `452625973e99c8d278be683398b8bb2bcd6292cd`.

## Ergebnis und Empfehlung

**TSR läuft auf dem getesteten Mac bei dieser Konfiguration langsamer. TAAU bleibt Standard.**
Separater Spielprozess: TSR 20,80–25,96 statt TAAU 25,75–33,59 FPS (Szenenmittel),
je nach Ort rund 19–23 % weniger FPS. GPU-Zeit steigt um etwa 9 ms.
PIE: TSR 14,68–21,38 statt TAAU 17,50–28,07 FPS.
TSR erreicht an keinem der drei Orte im Mittel 30 FPS. Auch TAAU erreicht dies
weiterhin nicht flächendeckend; keine 30-FPS-Zusage für die gesamte Map.

TSR glättet feine Gras-, Blatt-, Boden- und Ditherdetails in den Standbildern
sichtbar stärker; dadurch wirkt das Bild stellenweise weicher und weniger körnig.
Das ist kein nachgewiesener höherer Detailgrad und kein Nachweis für flimmerfreie
Bewegung oder grundsätzlich bessere Bildqualität. Für das derzeitige Leistungsziel
überwiegen die Mehrkosten. Keine permanente Umschaltung und keine Änderung der
verbindlichen Grafikentscheidung nötig.

## Tatsächlicher Testaufbau

- VisualV2, 2560×1440 Ausgabe, 75 %, intern 1920×1080, alle elf Gruppen High (2).
- MacBook Air M4 / 10 GPU-Kerne / 16 GB, Metal SM6, UE 5.8.2, derselbe Rechner und
  dieselbe unveränderte Nutzer-Konfiguration wie beim [Grafikprofil-C-Test](GRAFIKPROFIL_VARIANTE_C_PRUEFBERICHT.md).
- Mittag zu Beginn jedes Zeitfensters, normale dynamische Weltzeit; Sonne 75°,
  identische Kameraposition/-winkel/FOV, Beleuchtung, Lumen, Schatten und Vegetation.
- Dorf (-4100,450,50,15), Wiese (-300,2100,50,15), Wald (-4300,1550,50,15), in cm.
- Je drei Paare pro Ort: TAAU/TSR, TSR/TAAU, TAAU/TSR. Je 6 s Warm-up + 8 s Messung.
  Insgesamt **36 validierte Messfenster**, 18 in echter PIE und 18 im separaten
  Unreal-`-game`-Prozess bei geschlossenem Editor; kein paketierter Shipping-Build.
- Keine Video-/Bildaufnahme während der Messung. Kontaktprofile nur in der isolierten
  QA-Welt deaktiviert; vorhandene wilde Bewegung/KI bleibt aktiv. Zufällige
  Pokémon-Positionen und Systemlast sind nicht bitgenau synchronisiert.
- FPS je Fenster = 1000 / mittlere gemessene Framezeit, Tabelle = Mittel der drei
  Fenster. p95 = Mittel der Frame-p95-Werte. Rohdaten enthalten Einzelspannen,
  GPU-, Game-/Render-Thread-Zeit. Render-Thread-Wall-Time enthält gegebenenfalls
  GPU-Warten; PIE liefert in diesem CSV-Zähler 0, was nicht keine Renderkosten bedeutet.

Die Map erzwingt TAA über ihr vorhandenes `PokeMonsterTemporalAABlendable`.
Ein bloßer globaler `r.AntiAliasingMethod 4`-Befehl würde deshalb keinen TSR-Test beweisen.
Verwendet wurden die **bereits vorhandenen** Profilerbedingungen `MapTAA:Native`
und `MapTAA:TSR`: beide identische High/75-%-Werte und globaler AA-CVar 4; ausschließlich
Gewicht 1 bzw. 0 des map-eigenen TAA-Blendables. Der vorhandene Profiler restauriert
die ursprünglichen PP-Einstellungen nach jeder Messung. Kein neues Kampfsystem,
kein neuer Upscaler und keine persistente Mapänderung.

Der Renderthread-Beobachter validiert in jedem Messframe tatsächlich **AA-Methode 2
(TAAU) oder 4 (TSR)**, temporalen Upscale-Pfad, Screen-Percentage-Showflag, feste
Fraktionen 0,75 × 1, QHD-Target und interne 1920×1080. Interne Maße sind aus dem
aktiven festen Treiber abgeleitet, kein Textur-Allocation-Readback. Dynamische Auflösung
aus. Native Prozess startet weiterhin selbstständig mit C/High/75 %.

TSR verwendet normales High: History.ScreenPercentage **100**, History.UpdateQuality
**2**. Keine teurere Epic-200-%-History, kein speziell abgesenktes TSR-Profil.
Die Gesamtdifferenz wird als gemessene GPU-/Framezeit ausgewiesen, nicht als
vollständige exklusive Laufzeit eines einzelnen TSR-Shaderpasses interpretiert.

## Separater Spielprozess

| Ort | FPS TAAU | FPS TSR | GPU TAAU → TSR (ms) | Frame TAAU → TSR (ms) | Frame-p95 TAAU → TSR (ms) | FPS-Änderung |
| --- | --- | --- | --- | --- | --- | --- |
| Dorf | 26,50 | 21,21 | 34,31 → 43,73 | 37,78 → 47,16 | 41,03 → 51,24 | -19,97 % |
| Wiese | 33,59 | 25,96 | 26,68 → 35,62 | 29,77 → 38,53 | 32,36 → 41,51 | -22,74 % |
| Wald | 25,75 | 20,80 | 35,60 → 44,96 | 38,84 → 48,07 | 42,20 → 51,55 | -19,21 % |

## PIE

| Ort | FPS TAAU | FPS TSR | GPU TAAU → TSR (ms) | Frame TAAU → TSR (ms) | Frame-p95 TAAU → TSR (ms) | FPS-Änderung |
| --- | --- | --- | --- | --- | --- | --- |
| Dorf | 20,99 | 17,64 | 37,62 → 46,60 | 47,66 → 56,77 | 52,92 → 62,82 | -15,96 % |
| Wiese | 28,07 | 21,38 | 31,08 → 42,13 | 35,64 → 46,78 | 40,97 → 51,73 | -23,82 % |
| Wald | 17,50 | 14,68 | 45,97 → 57,14 | 57,16 → 68,13 | 63,25 → 75,32 | -16,11 % |

Die neuen aktuellen TAAU-Kontrollwerte liegen in ähnlicher Größenordnung wie die
vorherigen C-Messungen, sind aber eigene Messungen. Keine historische TAAU-Zahl wurde
als neue Gegenprobe verwendet. Absolute Unterschiede zwischen Sitzungen sind keine
nachgewiesenen weiteren Optimierungen. Die direkte Paarung ist für die AA-Bewertung
maßgeblich.

## Echte Bildpaare

| Szene | TAAU | TSR |
| --- | --- | --- |
| Dorf | [QHD-Original](../Saved/ProjectRefinement/TSRComparisonC75/Photos01/Dorf_TAAU.png) | [QHD-Original](../Saved/ProjectRefinement/TSRComparisonC75/Photos01/Dorf_TSR.png) |
| Wiese | [QHD-Original](../Saved/ProjectRefinement/TSRComparisonC75/Photos01/Wiese_TAAU.png) | [QHD-Original](../Saved/ProjectRefinement/TSRComparisonC75/Photos01/Wiese_TSR.png) |
| Wald | [QHD-Original](../Saved/ProjectRefinement/TSRComparisonC75/Photos01/Wald_TAAU.png) | [QHD-Original](../Saved/ProjectRefinement/TSRComparisonC75/Photos01/Wald_TSR.png) |
| Wald22 | [QHD-Original](../Saved/ProjectRefinement/TSRComparisonC75/Photos01/Wald22_TAAU.png) | [QHD-Original](../Saved/ProjectRefinement/TSRComparisonC75/Photos01/Wald22_TSR.png) |

Acht normale Viewport-PNGs in echtem PIE, jeweils 2560×1440. Pro Paar exakt gleiche
Kamera, Spielerposition, FOV, Weltzeit und pausierte Spielsekunde. Normales `Shot`,
kein HighResShot, keine künstlichen Bilder. Derselbe Blendable-Kontrollpunkt wechselt
nur in RAM das Gewicht; sämtliche PP-Einstellungen werden anschließend exakt
restauriert. Nachtbild zusätzlich um 22:00, keine separate Nacht-FPS-Messung.
Keine neue Video- oder vollständige Bewegungs-/Ghosting-Abnahme in diesem Auftrag.

## Sicherheit und Prüfungen

- Alle 36 Fenster validiert, sechs Gruppen je Betrieb mit je drei Wiederholungen.
- Vier exakte QHD-Bildpaare validiert.
- Editor-Einstellungen einschließlich öffentlicher User-Settings-Abfragen vor/nach PIE
  exakt gleich. Beide eigenen Prozesse regulär beendet, kein Force Quit und kein
  neuer Editorabsturz in diesem Vergleich.
- VisualV2 MAP CHECK: 0 Fehler, 0 Warnungen. Keine Map gespeichert.
- 3984 ursprüngliche Dateien inklusive 332
  vorhandener .sav-Dateien und 33 anfänglich
  unversionierter Dateien unverändert; Vollbackup-Refs unverändert.
- Ausschließlich eigene isolierte Testslot-/UserDir-Fixture. Keine Nutzersaves,
  Gameplay-Quellen, Controllerbelegung, Assets, Modelle, Beleuchtung oder
  `DefaultEngine.ini` bearbeitet. Deren bereits vorhandene Nutzeränderungen erhalten.
- Kein neuer C++-Build/gesamter Automationstestlauf: Produktionscode/Binärstand
  unverändert. Frühere 280 Funktionstests sind **keine neu ausgeführten Ergebnisse**
  dieses Zusatztests. Der vorherige strenge Wrapper-Exit 1 wird nicht umgedeutet.
- Bekannte externe `idevice_id`-Warnungen (Bad CPU type / Fehler 86) treten auch in
  den Sitzungslogs auf; getrennt von den erfolgreichen Renderer-/Mapprüfungen.

Werkzeuge: [TSRComparisonC75](../Tools/TSRComparisonC75/README.md).
Lokale Rohdaten: `Saved/ProjectRefinement/TSRComparisonC75/Measurements.json`,
`Summary.json`, `PhotoValidation.json`, `ProtectionFinal.json` sowie die getrennten
PIE-/Native-Ergebnisordner. Editorlog unter
`Saved/ProjectRefinement/GraphicsVariantC/TSRCompareEditor01.log`.
Nur Vergleichswerkzeuge und dieser Bericht werden versioniert; keine Kontrollbilder,
keine LFS-Assets. Abschließender Commit-/Remote-/LFS-Nachweis lokal in `GitFinal.json`
und in der Chat-Abschlussmeldung.
