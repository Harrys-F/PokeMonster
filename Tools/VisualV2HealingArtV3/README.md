# Begrenzte Heilhaus-Artarbeit V3

Diese Werkzeuge erzeugen keine neue Map und enthalten keine FPS-Benchmarks.
Sie verwenden die vorhandene Spielkamera und ausschließlich die bestehende VisualV2.
Kein automatischer Commit, Push, Discard All, Save All oder Prozessabbruch.

## Fertigen Stand prüfen

- `BlenderAudit.py` ausschließlich in separatem Blender-Hintergrundprozess mit
  `--python-exit-code 1` ausführen. Liest die neue Quelle, speichert sie nicht.
- `Build.py [Ausgabelabel]`, `RunQA.py Automation [Ausgabelabel]`,
  `RunMapCheck.py [Ausgabelabel]` nur bei geschlossenem Editor.
- `LaunchEditor.py <neuesLabel> Dev_TestMap_VisualV2` startet einen eigenen Editor;
  `Control.py VerifyAssets.py` prüft Geometrie, Materialien und Maße.
- `RunPIEReview.py <1=Medium|2=High> <Phase>` erzeugt echte Spielkameraaufnahmen
  in 720p und QHD bei 100 %. Eine Qualität pro Editorprozess verwenden.
- `RunNativeReview.py <Qualität> <Phase>` startet einen eigenständigen `-game`-Prozess
  auf derselben bestehenden Map. Das ist kein gepackter Shipping-Build.
- `RunAcceptance.py PIE <neuesLabel> 2560 1440 100` führt den vorhandenen vollständigen
  Enhanced-Input-Fußlauf aus; sichert/restauriert den tatsächlichen Dev-Slot.
- `Control.py CloseEditor.py` beendet nur eine saubere Sitzung ohne laufendes PIE.
- `ComposeReview.py <Qualität> <PIE|Standalone> [Nachherphase]` beschriftet/vergleicht
  echte Aufnahmen, prüft Kameradaten und erstellt unveränderte Originalpixel-Ausschnitte.
  Pillow aus dem vorhandenen Codex-Runtime genügt; keine neue Abhängigkeit installieren.

## Nachvollziehbare Herstellung, nicht auf fertigem Stand erneut anwenden

1. `BuildPlants.py` erstellt in isoliertem Blender die fünf Quellen und FBX-Dateien.
   Vorhandene eigene Dateien nur nach bewusster Prüfung mit `-- --revise-owned` ersetzen.
2. `Startup.py`, `Inventory.py`, `GroundInventory.py`: saubere Ausgangsszene erfassen.
3. `PrepareAssets.py`: private Material-/Textur-/Meshvarianten. Schützt bestehende
   Varianten ohne eigenen Sitzungsmarker und fremde ungesicherte Pakete.
4. `RefineGround.py`: örtlich begrenzte Abnutzung und feinere Randvariation.
5. `ApplyCandidate.py`: exakter Szenenvergleich; ausschließlich 26 Topfbindungen,
   fünf Bodenbindungen und die nachgewiesen dekorative Würfelinstanz bearbeiten.
6. Echte Bilder beurteilen, dann `SaveReviewed.py`: nur diese Map speichern.

`CorrectVertexTransfer.py`, `ColourProbe.py` und `ReimportOwnedUV.py` halten die
nachgewiesenen Reparaturen nachvollziehbar. Das Herstellskript enthält diese bereits.
Beim UV-Reimport werden Dreieckspositionen verglichen und die Map nur dann gespeichert,
wenn ihre geprüfte Signatur vollständig unverändert geblieben ist.

Alle Zustandsdaten, Rohbilder, Probes und Bytecode bleiben unter `Saved` beziehungsweise
im externen Abnahmeordner. Fehlende optionale Medien blockieren Build/Automation nicht.
