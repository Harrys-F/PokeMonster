# Heilhaus V4 – begrenzte Artarbeit und Abnahme

Keine neue Map, kein Benchmark, keine Licht-/Kamera-/Gameplayänderung. Originalquellen bleiben erhalten.
Nur der schlanke Worktree wird verwendet. Private Content-Assets unter /Game/Environment/VisualV2HealingArtV4.

## Prüfung des gespeicherten Stands

- BlenderAudit.py und BlenderDetailsAudit.py in getrennten Blender-Hintergrundprozessen mit --python-exit-code 1; öffnen Quellen ohne Speichern.
- Build.py <neuesLabel>: Mac Development Editor Build, nur bei geschlossenem Editor.
- RunQA.py Automation <neuesLabel>: vollständige Projekt-Automation mit echtem Reportexport, keine erfundenen Testzahlen.
- RunMapCheck.py <neuesLabel>: frischen Editor öffnen, vorhandene zentrale Map laden, Signatur und Map Check prüfen, keine Speicherung.
- LaunchEditor.py <neuesLabel> Dev_TestMap_VisualV2: eigene saubere Sitzung, keine fremden Zustände verwerfen.
- Control.py VerifyAssets.py: elf importierte Meshes, Materialien, Maße und Kollisionen messen.
- RunPIEReview.py <1|2> <Before|After>: echte 720p-/QHD-Spielkamera, 100 Prozent Primary und Secondary, fünf Positionen.
- RunNativeReview.py <1|2> <Before|After>: echte eigenständige -game-Sitzung, gleiche Auflösungen/Positionen; kein Shipping-Cook.
- Eine Qualität pro Editorprozess, wegen bekannter Metal-Probleme bei Live-Scalabilitywechsel.
- RunAcceptance.py PIE <neuesLabel> 2560 1440 100: vorhandener Enhanced-Input-Fußlauf, Dev-Slot sichern und restaurieren; keine Testteleports.
- Control.py CloseEditor.py: ausschließlich saubere eigene Sitzung regulär schließen.
- ComposeReview.py <1|2> <PIE|Standalone> After: identische Kameradaten prüfen und unveränderte Aufnahmen beschriften.

## Herstellschritte – nicht blind auf fertigen Dateien wiederholen

BuildPlants.py, BuildDetails.py, PrepareAssets.py, ApplyCandidate.py, RefineCandidate.py,
FixIvyPlacement.py, CurlIvy.py, ReimportIvy.py und SaveReviewed.py dokumentieren den begrenzten Eingriff.
Private Kopien statt globaler Materialänderungen. ApplyCandidate prüft jede übrige Actor-Signatur.
SaveReviewed speichert ausschließlich die geprüfte zentrale Map, kein Save All.
Originale 175 HISM-Details bleiben unverändert; vier neue HISM-Gruppen ergänzen nur den Heilhausbereich.
CorrectLegacyWindows.py korrigiert zusätzlich acht ältere Fensterpflanzen und erhält 28 primitive Bestandteile unsichtbar; VerifyLegacyVisibility.py prüft dies in laufendem PIE.
Alle Zusatzdetails NoCollision, kein zusätzlicher Schattenwurf; bisherige Schattenflags bleiben bestehen.

Logs, Fotos, Kandidaten-/Vorher-Sicherungen und Save-Teststände liegen ausschließlich unter Saved bzw. extern.
Keine Steuerbilder, Videos, Rohlogs oder Cachedateien für Git vorgesehen. Die drei Albedos und die Nutzerreferenz sind notwendige Artquellen.
