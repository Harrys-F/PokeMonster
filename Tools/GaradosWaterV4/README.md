# Garados Water Animation V4

Im bestehenden Projekt ausführen. Die Werkzeuge verwenden das vorhandene WaterV2-Rig und die V3-Arbeitsquelle. Keine neue Geometrie, Gewichte, Skeletons, Maps, KI oder Inventar-/Save-Systeme.

## Animationen

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python Tools/GaradosWaterV4/PrepareAnimations.py
```

Erzeugt eine eigene `Garados_Water_V4.blend`, sechs animation-only FBXs und `WaterV4_Audit.json`. Original-GLB wird per SHA geprüft; Mesh/Ruhepose/Skin/UV/Material-Fingerabdruck muss unverändert bleiben. Eine vorhandene eigene V4-Quelle wird ohne explizites `-- --revise-own-v4` nicht überschrieben. Keine Sicherungskopien oder Neumodelle. Alle sechs Schleifen 2,8 s / 60 Hz; stärkere S-Welle, 14 Segmente des Vorderkörpers zum Beobachten gekrümmt, hinterer Höhenanker unverändert.

`ImportAnimations.py` im sauberen Editor ohne PIE über die vorhandene ArtControl-Skriptausführung starten. Erstimport ausschließlich bei noch nicht vorhandenem WaterV4-Assetordner; kein Mesh-/Skeletonimport. Garados' bestehendes Präsentationsasset bindet sechs neue Wasserclips und den Wasser-BoundsScale 1,2. V3-Idle, V3-Übergangstiming und alle Land-/Kampf-/Wasserreaktionen erhalten. Nach erfolgtem Import nicht nochmals starten oder dafür Assets löschen.

## QA

```sh
python3 Tools/ProjectMaintenance/ProjectQA.py GaradosWaterV4/Build_NEUER_NAME Build
python3 Tools/GaradosWaterV4/RunAutomation.py Automation_NEUER_NAME
```

Der bestehende strenge Reportvertrag wird wiederverwendet, mit eigenem UserDir: mindestens 321 vollständige Tests, keine Warnungstests, Fehler oder Skips. Optionaler Scope: `PokeMonster.GaradosWaterV4` (ein neuer Formvergleich), `PokeMonster.GaradosPolishV3` (drei Übergangs-/Grenztests), `PokeMonster.GaradosWater` (fünf bestehende V2-Regressionsfälle). Kein automatisches Beenden fremder oder zeitüberschreitender Prozesse.

`Gameplay.py` prüft einen real natürlich erschienenen Garados im unveränderten VisualV2-Teich mit der tatsächlichen Third-Person-Kamera. Der vorhandene sichere Modell-Vorschauplaner steuert zeitweise die Testbewegung; keine zweite Wild-KI. Ausschließlich eigene QA-Party / eigener UserDir bzw. expliziter PIE-Testslot. Bewegung 35/70/125 cm/s, Kurve, seitliche/diagonale Ansichten, Stopp, Aufrichten, Beobachten, Absenken und Wiederanlauf müssen tatsächlich erreicht werden. Normale Läufe prüfen zusätzlich Menü-Save/Load und das unveränderte Landbegleiter-Rig.

Der bekannte Vorschauplaner kann in dem begrenzten Teich vorübergehend stehen bleiben. Das Prüfskript protokolliert dann Tick, Sperren und Planungszähler und fordert nach vier Sekunden ein anderes **sicher geprüftes** Ziel an; höchstens innerhalb der bestehenden 45-s-Phasengrenze. Keine Kollision deaktivieren, keine Schwelle absenken und keine Produktionsnavigation dafür ändern. Nur ein `Result.json` mit `passed: true` zählt als bestandener Durchlauf.

Der bestehende `Tools/ModelsV4/Run.py` erlaubt jetzt auch diesen QA-Ordner und Skriptpfad. JSON-Aufruf wie V3: neuer `label`, explizit gewählte vorhandene **QA-Fixture unter Saved**, `script: "Tools/GaradosWaterV4/Gameplay.py"`, begrenzter `timeout`. Niemals Nutzersaves als Fixtures verwenden. Vorhandene Editor-/Spielprozesse bleiben geschützt.

Optionaler getrennter Film: `recording: true`, `fixed_step_review: true`, `recording_pipeline: "screenshot_request"`. Feste 30-Hz-Simulationsschritte, etwa 15 echte QHD-JPEGs je Spielsekunde, maximal 1.200 Frames. Kein Gameplay-FPS-Benchmark, keine Rendering-/Backbufferänderung, keine Interpolation. Unreals Shot-Anforderung wird vor einem Standortwechsel fertiggestellt, damit Standbilder nicht versehentlich den nächsten Kameraübergang zeigen. Rohfilm und Vergleich zusätzlich dekodieren, Zeitstempel und tatsächlichen Bildinhalt prüfen; gültige Containerdaten allein erkennen schwarze Bilder nicht.

Nachweise und Aufnahmen liegen lokal unter `Saved/ProjectRefinement/GaradosWaterV4/`. Bericht: `Docs/GARADOS_WATER_ANIMATION_V4.md`. Anschließend visuelle Beurteilung durch Harry; keine automatische weitere Animationserweiterung.
