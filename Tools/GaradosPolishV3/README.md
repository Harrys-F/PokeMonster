# Garados Animation Polish V3 – Werkzeuge

Alle Befehle im bestehenden `/Users/harry/Developer/PokeMonster` ausführen. Keine Kopie/Map erforderlich. Die Werkzeuge sind ausdrücklich auf Garados und eigene isolierte QA-Daten begrenzt. Der normale Spieler muss kein Werkzeug starten: Die vorhandene Garados-Präsentation verwendet V3 automatisch im Wasser.

## Animationsquelle

`PrepareAnimations.py` öffnet ausschließlich die bestehende `Garados/Source/Garados_Water_V2.blend`, prüft das Incoming-GLB und erzeugt eine eigene V3-Arbeitsquelle sowie sieben **animation-only**-FBXs. Keine Mesh-, Ruhepose-, Gewichts-, UV- oder Materialänderung. Der Erstlauf schützt eine bereits vorhandene V3-Quelle vor Überschreiben. `--revise-own-v3` ist ausschließlich für bewusst autorisierte Überarbeitungen dieser eigenen V3-Dateien vorgesehen.

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python Tools/GaradosPolishV3/PrepareAnimations.py
```

`ImportAnimations.py` im sauberen, nicht spielenden Projekteditor über die vorhandene ArtControl-Skriptausführung starten. Es importiert keine Geometrie, verwendet genau das bestehende WaterV2-Skeleton und speichert nur sieben neue WaterV3-Clips und Garados' Präsentations-Datenasset. Ein bereits vorhandener WaterV3-Assetordner wird absichtlich abgelehnt; **nicht** ungeprüft löschen oder diesen Schutz umgehen. Nach dem bereits erfolgten Import ist kein erneuter Import nötig.

## Strenge Automation

```sh
python3 Tools/ProjectMaintenance/ProjectQA.py GaradosPolishV3/Build_NEUER_NAME Build
python3 Tools/GaradosPolishV3/RunAutomation.py Automation_NEUER_NAME
```

Abgeleitet vom vorhandenen GaradosWaterV2-Wrapper: dieselbe Automation/Report-Prüfung, eigener `-UserDir`, keine Warnungstests, Fehler, Skips oder laufenden Tests zulässig, mindestens 320 vollständige Tests. Optionaler zweiter Parameter `PokeMonster.GaradosPolishV3` prüft die drei neuen Tests, `PokeMonster.GaradosWater` die fünf bestehenden Wasserregressionen. Der Runner beendet keine vorhandenen Sitzungen oder zeitüberschreitenden Prozesse.

## Tatsächlicher VisualV2-Gameplay-Test

`Gameplay.py` verwendet denselben realen, natürlich erschienenen Garados im bestehenden Teich und den vorhandenen sicheren Modell-Vorschauplaner. Keine zweite KI. Geschwindigkeiten 35/70/125 cm/s, Kurve, Stopp, Aufrichten, drei Uferblicke, Absenken und erneutes Schwimmen werden anhand tatsächlicher Pose/Bewegung qualifiziert; normale Testläufe prüfen zusätzlich Menü-Save/Load und das ursprüngliche Landbegleiter-Rig. Änderungen an Preview-Flag, Tags und Geschwindigkeit werden zurückgesetzt. Eine vorhandene kleine Enton-Testbegleiterinstanz wird nur in der eigenen QA-Party vorübergehend nach vorn sortiert, damit das große unveränderte Garados-Landmodell die Wasseraufnahme nicht verdeckt.

Der vorhandene Launcher ist um diesen Ordner erweitert:

```sh
python3 Tools/ModelsV4/Run.py Saved/ProjectRefinement/GaradosPolishV3/MEIN_TEST.json
```

JSON: `label` = neuer eindeutiger Laufname; `fixture` = **ausdrücklich gewählte vorhandene QA-Fixture unter Saved**, niemals Nutzerspielstand; `script` = `Tools/GaradosPolishV3/Gameplay.py`; `timeout` = begrenzte Beobachtungszeit in Sekunden. `recording: false` für normalen zeitlichen Funktionstest. Launcher kopiert die gewählte QA-Fixture in einen neuen eigenen UserDir und verweigert den Start, solange ein Editor/Spielprozess existiert. Beim tatsächlichen Durchlauf entstand kein zusätzlicher Projektklon.

Ausschließlich für einen getrennten Offline-Animationsfilm: `recording: true`, `fixed_step_review: true`, `recording_pipeline: "screenshot_request"`. Feste Simulationsschritte 30 Hz, maximal 900 echte QHD-JPEGs, angefordert etwa alle 1/15 Spielsekunden; kein FPS-Benchmark und keine Bildinterpolation. `ReviewCapture.py` verwendet Unreals funktionierenden Shot/SaveImageByExtension-Pfad, keine Änderung des HDR-Backbufferformats oder der Grafikqualität. CSV enthält tatsächliche Spielzeitstempel. Native macOS-Fensteraufnahme ist weiterhin durch TCC blockiert.

Ein Test ist nur bestanden, wenn `Result.json` dies bestätigt. Bilder/Clips zusätzlich visuell auf tatsächlichen Inhalt prüfen: korrekte Framezahl und Zeitstempel allein erkennen schwarze Aufnahmen nicht. Ein Lauf kann wegen anderer Fische oder fehlender sicherer Ziele scheitern; keine Kollision deaktivieren, keine Testschwellen absenken und keine Produktionsnavigation dafür verändern.

Ergebnisse, vollständige Logs, Fehlversuche und Medien: `Saved/ProjectRefinement/GaradosPolishV3/`. Diese Kontrollmedien werden nicht versioniert. Abschlussbericht: `Docs/GARADOS_ANIMATION_POLISH_V3.md`.
