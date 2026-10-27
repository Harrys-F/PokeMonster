# VisualV2-Stabilisierung V1 – tatsächliche Nachweise

Die Produktionsänderung betrifft genau drei VisualV2-Materialslots und den vorhandenen Entwicklungsrecorder. Keine zweite KI-/Zeit-/Kampfarchitektur.

- Bericht: `Docs/VISUALV2_GRAFIK_PERFORMANCE_STABILITAET_V1.md`.
- Lokale Protokolle/Bilder/Videos: `Saved/ProjectRefinement/VisualV2StabilityV1/`.
- Vorherige Nutzerdateien: `Baseline.py` / `VerifyProtection.py`, nur Hashes, keine Kopien.
- `StartSession.py <eindeutigerName>` startet nur ohne bestehenden Editor, mit absolutem Projektpfad und `-nowrite`. `Startup.py` verwendet die bestehende bewachte ArtSession-Queue. Kein Prozesssignal.
- Über `Tools/ProjectMaintenance/ArtControl.py script ...` werden die einzelnen Werkzeuge ausgeführt. `PreparePIE.py` vor `start_pie` schützt mit isoliertem Slot und sicherer Beobachterposition; reguläre Nutzer-Slots werden nicht geschrieben. `RestoreProfiles.py` stellt bei Bedarf die nur im Messaufbau gesperrten Kontakte wieder her.
- Ergebnisnamen in den jeweiligen Request-JSONs unter Saved müssen eindeutig sein. Werkzeuge verweigern vorhandene Ergebnisordner; alte Nachweise nicht überschreiben. Die Quellen sind auch das Protokoll der tatsächlich getrennten Diagnose-/Fehlversuchsstufen, kein blind zu startender Ein-Klick-Gesamttest.
- `Performance.py`, `GroupPerformance.py`, `MotionPerformance.py` und `Capture.py` nutzen den bestehenden nativen `pm.EnvPerf2` mit VGB1-Kennung. Bei Gruppenmessungen wird die feste native Waldplatzierung nur im Warmup zur Gruppe ersetzt; tatsächliche Kamerakoordinaten stehen in jedem Frame. Standard: High=2, 100%, QHD, TAA2.
- `Reproduce.py` liest ReproduceRequest.json (`label`), `Performance.py` PerformanceRequest.json (`label`, `cases` mit `name`, `hour`, optional `pokemon`/`sites`), `Capture.py` CaptureRequest.json (zusätzlich `mode`: none/slate/framebuffer, optional `slots`: 3/6). `Analyze.py` prüft tatsächlich gerenderte Auflösung und wertet nur erfolgreich beendete Messungen aus.
- `Cycle.py`, `RunCycles.py` und der getrennte Fortsetzungsablauf `RunCyclesFinish.py` protokollieren normale PIE-Endpunkte. `Gameplay.py`, `Travel.py`, `RhythmReview.py` verwenden die vorhandenen Spielsysteme/Debugfixtures. Alle gespeicherten Testdaten liegen im expliziten `PokeMonster_SaveV2_Test_...`-Namensraum.
- `ApplySurfaceFix.py` ist der überprüfte einmalige Editor-Migrationsschritt für die drei ursprünglichen Materialslots; er verweigert einen schon veränderten Ausgangszustand. Keine gemeinsamen Materialien speichern.
- `MapChecksFinal.py` lädt nur die zwölf vorhandenen Maps und speichert keine Map. `Restore.py` prüft die vollständige gespeicherte Endszene und stellt temporäre Editorpräferenzen zurück. Zum Beenden ausschließlich die eigene bewachte `ArtControl.py close`-Aktion nach regulärem `stop_pie` verwenden.

Vorhandene Konsolenbefehle:

```text
pm.WorldClock pause
pm.WorldClock set 1 19 0
pm.DayNight B
pm.EnvPerf2.Viewport 2560 1440
pm.TAAReview.ReadbackSlots 3
pm.TAAReview.CaptureStart /Users/harry/Developer/PokeMonster/Saved/VisualV2TAAIntegrationV1/Recordings/NEUER_EINDEUTIGER_NAME slate 30
pm.TAAReview.CaptureStop
```

30 ist ausschließlich eine Aufnahme-Obergrenze. Standardbudget drei; sechs brachte keinen belastbaren Vorteil. Die Aufnahme beendet sich jetzt auch beim PIE-/Weltende selbst. `Metrics.json`, `Frames.csv`, `Complete.txt` erst nach asynchronem Abschluss bewerten. Shipping enthält diese Entwicklungsbefehle nicht.

Videoverifikation: vorhandenen `Saved/BiomeTestV1/EncodeSequence` weiterverwenden; `EncodeEvidence.py` verwendet ausschließlich echte Quellframes und prüft mit `VerifyVideo.swift` die dekodierte Frameanzahl und Zeitstempel innerhalb eines realen Ausgabe-Zeitquantums. Vorhandene Videos werden nicht überschrieben. Beispiel-Verifier-Build mit vorhandener Xcode-Toolchain: `swiftc -target arm64-apple-macosx14.0 -module-cache-path Saved/ProjectRefinement/VisualV2StabilityV1/SwiftModuleCache Tools/VisualV2StabilityV1/VerifyVideo.swift -o Saved/ProjectRefinement/VisualV2StabilityV1/VerifyVideo`. Kein zusätzlicher Codec/Plugin erforderlich. Ungerade native Videoabmessungen können vom bestehenden Encoder um ein Pixel gerundet werden; keine zeitlichen Zwischenbilder.

Finaler strenger QA-Wrapper: Exit 1 wegen sechs bekannten externen idevice_id-Warnmeldungen in drei erfolgreichen Tests; funktional 279/279. Keine pauschale Warnungsfreiheit, kein physischer Controller-Nachweis, keine behauptete Lösung des früheren Editorstillstands.
