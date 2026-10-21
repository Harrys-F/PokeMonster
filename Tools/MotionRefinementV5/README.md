# Bewegungsüberarbeitung V5

Nur im aktiven Projekt, vorhandene VisualV2 und deren explizites transientes Vorführgelände. Keine neue Map, kein Save- oder Habitatformat. Reviewmedien bleiben ausschließlich im ignorierten `Saved/`.

## Quellen und einmaliger Import

`InspectSources.py` liest die vorhandenen Rigs. Die drei `Build*Source.py` erzeugen getrennte gepackte Quellen; sie verweigern vorhandene Zieldateien. `RefineGlurakContacts.py` korrigiert ausschließlich den noch unveröffentlichten eigenen Kandidaten. `ExportSources.py` exportiert 10 Glurak-, 8 Nebulak- und 3 Spieler-FBX-Dateien. `CorrectGasCoordinates.py` korrigiert die unveröffentlichte Hülle einmalig in Mesh-Referenzkoordinaten; die exakte inverse Unreal-Kopf-Referenztransformation wird beim Import als Effektversatz verwendet. Keine geratenen FBX-Achsendrehungen.

Blender im Hintergrund mit `--python-exit-code 1` starten; Blender meldet Python-Fehler sonst möglicherweise mit Prozesscode 0. `ValidateSources.py` öffnet gepackte Quellen erneut und importiert wirklich jede FBX zurück. `AuditMotionBounds.py` misst jede Glurak-Pose schreibgeschützt.

`ImportCandidates.py` ist ein **einmaliger** Unreal-Editorimport und verweigert vorhandene MotionV5/MotionV3-Verzeichnisse. Keine Original-Skeletons speichern. `CorrectGasImport.py` war die einmalige Korrektur des ersten Kandidaten und verweigert inzwischen veröffentlichte Assets. Für die normale Weiterbearbeitung vorhandene Quellen gezielt öffnen und Änderungen prüfen; diese historischen Erstaufbau-Skripte nicht erneut ausführen. `AcceptCandidates.py` erwartet die dokumentierte Ausgangssitzung und ändert ausschließlich die zwei visuellen Speziesverweise nach vollständiger Vorprüfung.

## Wiederholbare Spielprüfung

Saubere `Tools/ProjectMaintenance/ArtSession.py` starten; keine vorhandene fremde Editor-Sitzung beenden. Dann beispielsweise:

```sh
python3 Tools/MotionRefinementV5/RunTargets.py NeuerEindeutigerName Glurak --hover --record
python3 Tools/MotionRefinementV5/RunTargets.py NeuerDeckenTest Glurak --hover --ceiling
python3 Tools/MotionRefinementV5/RunTargets.py NeuerAbschnittstest Glurak --hover --route-probe
python3 Tools/MotionRefinementV5/RunTargets.py NeuerGasFrontTest Nebulak --record
python3 Tools/MotionRefinementV5/RunTargets.py NeuerGasSeitentest Nebulak --yaw=45 --record
python3 Tools/MotionRefinementV5/RunPlayer.py NeuerSpielertest --record
```

`--original` liest die vorherigen Profile aus der optionalen lokalen Import-Quittung; fehlt diese, nicht als Vergleichserfolg werten. Vorführgelände und Darstellungstests sind explizite Fixtures, keine behaupteten natürlichen Begegnungen. Das vorhandene echte Encounter-/Fang-/Gameplay-Testwerkzeug bleibt separat erforderlich.

`--record` verwendet den vorhandenen asynchronen `pm.TAAReview`-Framebuffer-Recorder. Unveränderte QHD-Kamera, tatsächliche Bildzeitstempel und Originalframes; keine Bildinterpolation. `EncodeSequence.swift` kodiert diese Dateien über das vorhandene macOS AVFoundation. Die Ausgabe liegt lokal unter `Saved/VisualV2TAAIntegrationV1/Recordings/<Label>/`. Variable Capture-Abstände und einzelne Screenshot-Hitches sind sichtbar; das Video ist kein FPS-Benchmark. Die PNG-Fallback-Aufnahme ist deutlich langsamer und wurde nicht als flüssige Videoabnahme gewertet.

Quellenvalidierung, Sichtprüfung und Regressionen aus `Docs/MOTION_REFINEMENT_V5_PRUEFBERICHT.md` gemeinsam betrachten. Ein grüner Prozesscode ersetzt keine visuelle Abnahme. Physischer Switch-Pro-Test bleibt offen.
