# TAAU gegen TSR bei Variante C / 75 %

Explizite Entwicklungsprüfung des unveränderten produktiven Builds `45262597`.
Keine neue Rendering-Implementierung und keine gespeicherte AA-/Mapänderung.

Verwendet `pm.EnvPerf2` mit den **bereits vorhandenen** Bedingungen
`MapTAA:Native` und `MapTAA:TSR`. Beide setzen identische QHD/High/75-%-Werte,
Original-Lumen/Schatten und globalen AA-CVar 4. Nur das Gewicht des vorhandenen
map-eigenen TAA-Blendables wechselt vorübergehend zwischen 1 und 0.
Renderer-Readback muss tatsächlich Methode 2 bzw. 4 zeigen. Ein CVar allein reicht
nicht: VisualV2s Blendable würde einen gewöhnlichen TSR-CVar-Wechsel überstimmen.
Die bestehenden Snapshot-/Restore-Funktionen geben die PP-Einstellungen zurück.

Ergebnisse: `Saved/ProjectRefinement/TSRComparisonC75/`, Screenshot-Paare ohne
HighResShot. Messungen ohne Video/Bildaufnahme, getrennt von der Bildprüfung.
Stock-High verwendet `r.TSR.History.ScreenPercentage=100` und History.UpdateQuality 2;
keine versehentliche Epic-200-%-History und kein speziell abgesenktes TSR-Profil.

- `Baseline.py` vor Tests: Originale/Saves/33 anfängliche unversionierte Eingänge
  hashen, keine Kopien. Bestehende Baseline nie überschreiben.
- Bestehendes `Tools/GraphicsVariantC/StartSession.py` mit neuem Label verwenden,
  nur bei geschlossenem Editor. Guarded ArtControl-Queue, keine automatische Map-Speicherung.
- Bestehendes `PrepareGameplay.py` vor PIE mit neuer eigener
  `PokeMonster_SaveV2_Test_Perf…`-Slotkennung aktivieren; für Timing Kontaktprofile
  nur in dieser QA-Welt deaktivieren. Keine Nutzersaves verwenden.
- `MakePlans.py TAG` erzeugt drei Standorte × drei interleavte TAAU/TSR-Paare,
  6 s Warm-up und 8 s Messung. Neue Labels statt alte Ergebnisse überschreiben.
- `Run.py PLAN`: bestehender Profiler im eigenen PIE; `Benchmark.py` steuert nur
  Testzeit/Standort und die vorhandenen Vergleichsbedingungen.
- `RunPhotos.py`: PhotoRequest.json, normale eingefrorene Viewport-Paare; in RAM
  das gleiche Blendable-Gewicht umschalten, ursprüngliche Settings exakt zurückgeben.
- PIE regulär beenden, ursprüngliche Editor-State-Abfrage vergleichen, `MapCheck.py`,
  bestehendes `CloseClean.py` und ArtControl `close`. Kein Force Quit.
- `RunNative.py PLAN`: Editor geschlossen, ausschließlich vorheriger eigener
  Noon-Testslot `PokeMonster_SaveV2_Test_PerfGraphicsC01.sav` als isolierte Fixture
  in ein eigenes UserDir. Normaler Unreal-`-game`-Prozess, kein Shipping-Build.
- `Analyze.py`: Ausgabe, interne Pixel, AA-Methode, temporalen Pfad und Kameras
  jedes Messframes validieren; drei Läufe je Methode/Ort, Mittelwerte und Spannen.
- `VerifyProtection.py`: ursprüngliche Dateien und Vollbackup-Refs nur lesend
  erneut vergleichen. Kein Wiederherstellen, Löschen oder Zurücksetzen.

Kein neuer Editor-Build oder kompletter Automationstestlauf nötig: Produktionsquellen
und Assets werden bei diesem reinen Vergleich nicht bearbeitet. Vorherige 280 Tests
sind keine neu ausgeführten Ergebnisse dieses Auftrags. Der Stand bleibt TAAU,
solange keine dokumentierte bessere Alternative übernommen wird.
