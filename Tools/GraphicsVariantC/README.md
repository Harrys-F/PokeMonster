# Grafikstandard C – Rendering und Prüfung

Produktiver Code: `Source/PokeMonster/Rendering/PokeMonsterGraphicsProfile.*`.
Konfiguration: `Config/DefaultPokeMonsterGraphics.ini`, `Config/DefaultGameUserSettings.ini`.
Diese Python-Werkzeuge sind **explizite Entwicklungsprüfungen**, keine Spielstart-Abhängigkeit.

## Verwendung im Spiel oder PIE

- Ohne Befehl: 2560×1440, High, 75 %, VisualV2 mit nativem TAAU.
- `pm.Graphics HardwareSPG`: frühere Hardware-Lumen-/SPG-Referenz bei 75 %; VisualV2 mit VSM4.
- `pm.Graphics status`: angeforderten und effektiven Screen Percentage sowie Viewport ausgeben.
- `pm.Graphics 100`: unveränderter nativer QHD-High-Vergleich mit Hardware-Lumen/SPG und ursprünglichen Schattenwerten.
- `pm.Graphics C`: wieder QHD High / 75 %.
- Startargument `-PMGraphicsProfile=100`: Vergleich ab Prozessstart.

Seit Rendering-Standard V5 verwendet C Software-Lumen + IFG (0/0); beide Referenzen setzen Hardware-Lumen + SPG (1/1). `-PMGraphicsProfile=HardwareSPG` startet die 75-%-Referenz. IFG-Parameter bleiben bei den in V4 geprüften Engine-Werten 64/16/100. Details und offene Bildqualitäts-/Framezeitfragen: `Docs/RENDERING_STANDARD_V5.md`.

Die Auswahl gilt im Prozess, auch bei Mapwechseln. Ein Neustart beginnt mit C.
Keine Spielstände oder gespeicherten Nutzereinstellungen werden automatisch geschrieben.
Der Editor erhält nach PIE seine vorherigen Qualitäts-/CVar-Werte zurück. Höherrangige
explizite Konsolen-Overrides bleiben maßgeblich; für einen unverfälschten Standardtest
keine zusätzlichen `r.ScreenPercentage`-Befehle verwenden. `pm.DayNight C` bezeichnet
weiterhin **85° Sonnenhöhe**, nicht dieses Grafikprofil.

QHD ist die Renderausgabe; ein kleiner eingebetteter Editor-Viewport kann diese Ausgabe
für seine Anzeige verkleinern. High bedeutet elf Nicht-Auflösungsgruppen auf Stufe 2.
Unreal kann die Kombination trotzdem als „Custom“ (`GetOverallScalabilityLevel=-1`)
einstufen, weil die Auflösung nicht dem eingebauten High-Prozentsatz entspricht.

## Nachweise dieses Auftrags

Lokale Ergebnisse: `Saved/ProjectRefinement/GraphicsVariantC/`.
Build: `../GraphicsVariantCBuild07`, vollständige Automation/strenger Wrapper:
`../GraphicsVariantCAutomation04`. Keine Kontrollmedien in Git aufnehmen.

- `StartSession.py LABEL`: nur bei geschlossenem Editor; bestehende VisualV2 öffnen,
  geschützte ArtControl-Queue nutzen. Kein automatisches Map-/Asset-Speichern.
- `PrepareGameplay.py`: vor PIE eine **neue eigene** `PokeMonster_SaveV2_Test_Perf…`-Slotkennung
  aus `PrepareRequest.json` scharfstellen; `PreparePIE.py` ist der hier verwendete
  Benchmark-Aufbau mit eigener fester Testslotkennung und deaktivierten Kontaktprofilen.
- `State.py`, `EditorState.py`, `ProfileSmoke.py`: effektive Einstellungen und exakte
  Wiederherstellung vor/nach PIE lesen; letzteres prüft Standard → 100 → C.
- `GeneratePlans.py NEUELABELNUMMER`: sechs Positionen × drei alternierende C/100-Paare
  erzeugen. Warm-up 4 s, Messfenster 6 s. Bestehende Ergebnisse nicht überschreiben.
- `Run.py PLAN`: in eigener isolierter PIE-Sitzung messen. `Benchmark.py` stellt
  keine Grafik-CVars selbst richtig, sondern prüft das produktive Profil.
- `NativeFixture.py`: eigenes PIE-Testsave am Mittag erzeugen, einmalig; keine Nutzer-
  slotkopie. `RunNative.py PLAN` nur nach sauberem Editorende: eigene Fixture in
  isoliertes UserDir kopieren, separaten Unreal-`-game`-Prozess starten, normal beenden.
  Kein ForceRes/ResX/ResY; der Standard muss selbst wirken. Kein Shipping-Test.
- `Analyze.py`: Renderer-Fraktionen, AA, temporalen Upscale-Pfad, Ausgabe, interne
  Maße und Kamera prüfen, Frame-/GPU-/CPU-CSV aggregieren. Interne Maße sind aus dem
  festen Screen-Percentage-Treiber abgeleitet, kein Textur-Allocation-Readback.
- `Photos.py`, `RunPhotos.py`: normale Viewport-`Shot`-Aufnahmen, kein HighResShot für
  den 75-%-Vergleich. Nur das Paar wird für identische Position/Zeit pausiert.
- `RunGameplay.py`: neue isolierte Slots, echte PIE-Welten, bestehende Softwareeingaben,
  Bewegung/Sprint, Menü, Kampf, Innenraum-Save/Load, Mapwechsel und vier Start-Stopp-Zyklen.
  Controllerprüfung ist Softwareprüfung, kein erneuter Hardwaretest.
- `MapChecksFinal.py`: zwölf vorhandene Maps prüfen, keine Map speichern.
- `CloseClean.py` und bestehendes ArtControl `close`: nur ohne PIE/ungespeicherte Pakete.
- `Baseline.py`: vor Änderungen bestehende Originale, Saves und geschützte Eingänge
  hashen; keine Kopien. Einen vorhandenen Baseline-Bericht niemals überschreiben.

Request-Dateien, Testslots und Ergebnisordner sind lokal und werden nicht automatisch
neu angelegt, überschrieben oder bereinigt. Wiederholungen benötigen neue eindeutige
Labels/Slotnamen. Werkzeuge nicht gegen eine fremde aktive Editor-Sitzung ausführen.
