# Animationsfeinschliff V6.1

Gezielte Korrekturen ausschließlich im bestehenden Projekt/VisualV2. Keine neue Map, kein eigener Gameplay- oder Animationsgraph. V6-Originalquellen und Assets bleiben erhalten.

## Diagnose und Quellen

- `InspectSources.py`: schreibgeschützte Topologie-/Gewichts-/UV-Diagnose und ausdrücklich als Blender-Diagnose bezeichnete Renderings unter Saved. Keine Quelle speichern.
- `InspectOriginalWeights.py`: dieselben auffälligen Hosenvertices in erhaltenen älteren Quellen vergleichen.
- `InspectPlayerDeformation.py`: tatsächliche Posen, gedehnte Kanten, Originalfarben und Gewichte vermessen.
- `BuildSources.py`: einmaliger Aufbau neuer V6.1-Quellen/FBX. Vorhandene Zielquellen verweigern. `--refine-player` beziehungsweise `--refine-glurak` ist ausschließlich für das eigene noch unversionierte V6.1-Ziel freigegeben und verweigert publizierte Pfade.
- `ValidateSources.py`: beide Quellen erneut öffnen, Geometrie/UVs/Materialzuordnung/Rest-Rigs/alle alten Animationskurven vergleichen, gepackte dateibasierte Texturen prüfen und beide FBX wirklich zurückimportieren. Blender mit `--background --python-exit-code 1 --python ...` ausführen.

Die tatsächlichen Änderungsselektionen stehen in `Art/.../AnimationCorrectionsV61_Audit.json`. Keine Blender-Diagnose als echten Unreal-Nachweis verwenden.

## Unreal und sichere Wiederholung

`ImportCandidates.py` erstellt nur neue Meshpakete und Gluraks neues Präsentationsprofil. Exakte vorhandene Skeletons, Materialien und sämtliche V6-Clips werden wiederverwendet, nicht erneut importiert. Original-Skeletons nicht speichern. `RefreshOwnPlayer.py`/`RefreshOwnGlurak.py` erlauben ausschließlich das eigene noch unversionierte V6.1-Mesh; nach Veröffentlichung absichtlich gesperrt. `AcceptGlurak.py` ist ein einmaliger geprüfter Profilwechsel und erwartet ausdrücklich den ursprünglichen V6-Verweis.

Für neue Prüfungen eine saubere `ArtSession.py`-Editorsitzung und gewöhnliches PIE verwenden. Das native permanente Testgelände muss ohne Prüfskript zehn Exemplare bereitstellen. Jede Besuchsfunktion wird überprüft; gesperrter Zugang ist kein gültiger Aufnahmebeleg.

Unter `Saved/AnimationCorrectionsV61/ReviewRequest.json` einen **neuen** Namen wählen, zum Beispiel:

```json
{"label":"NeuePruefung01","targets":["Glurak"],"glurak_seconds":38,"after":true,"integrated":true}
```

`Review.py` erfasst echte QHD-Frames der nativen Testgeländebewegung, aller angegebenen Ansichten sowie der Player-Acht-Richtungen-/Start-/Stop-/Sprint-/Wendefolge. `baseline:true` verwendet ausschließlich in PIE das erhaltene V6-Playermesh/Glurak-Profil und `pm.PlayerFootIK 0`; kein gespeichertes Asset wird zurückgesetzt. `skip_player:true` eignet sich für die kurze Zehn-Pokémon-Prüfung. Daten/Recorder ausschließlich unter Saved, nicht hochladen. Nach der Prüfung PIE beenden, damit eine Vorschaupräsentation nicht versehentlich als aktive Standardkonfiguration geprüft wird.

`AlignedComparison.py` benötigt für eine erneute Ausführung einen neuen lokalen Ausgabenamen. Reale erhaltene V6-/V6.1-Assets, gleiche vorhandene Spielkamera und feste Player-Clipzeiten. Keine zusätzliche Kameraposition und kein neues Modell spawnen. Tatsächliche Null-Kameradifferenz in der Quittung kontrollieren. Standbilder ersetzen keine Bewegungsabnahme.

`FootProbe.py` verwendet `FootProbeRequest.json` mit `{"label":"NeuerKontaktlauf","enabled":true}`. Ohne Bild-Readbacks werden nur räumliche Fuß-/Player-Zustände erfasst. `AnalyzeFootProbe.py BEFORE_LABEL AFTER_LABEL` bewertet ausschließlich stabile annähernd gerade Standphasen. Das Ergebnis ist weder ein FPS-Benchmark noch eine Garantie perfekten Fußkontakts beim Wenden oder auf sämtlichen Geländeformen. Fuß-Bones sind keine Messung jedes einzelnen Sohlenvertices.

`EncodeReviews.py Before|After REVIEW_LABEL` erzeugt kurze echte Videos mit Originalzeiten über den vorhandenen lokalen AVFoundation-Encoder. Fehlt er, Exit 2 und nur vorhandene Bildfolge melden; keine erfolgreiche Videoabnahme behaupten. Keine synthetischen Zwischenbilder. Aufnahmerücklesen kann Hitches verursachen.

Build/Automation über `Tools/ProjectMaintenance/ProjectQA.py`. `MapChecks.py` lädt alle vorhandenen Karten, prüft und kehrt ohne Speichern zur VisualV2 zurück. Gameplay: vorhandenen `Tools/AnimationCorrectionsV6/RunFullGameplay.py NEUERNAME` und `Tools/CreaturePolishV4/RunActiveBattle.py Glurak NEUERNAME` benutzen. Diese schützen/restaurieren den Dev-Slot bytegenau. Software-Eingaben sind kein physischer Controller-Test. Bekannte externe Engine-Warnungen separat und unverfälscht berichten.

`AuditHandoff.py` prüft den normalen Editorzustand und das bestehende map-eigene TAA-Blendable, ohne einen globalen AA-Wert zu erzwingen. Im Animationseditor für die Gewichts-/Farbkorrektur das neue V6.1-Mesh als Preview auswählen; unveränderte alte Clips/Skeletons behalten absichtlich ihre bisherigen Vorschauverweise. Die Laufzeit-Fußkorrektur ist im normalen Player-Animator aktiv und kein neu gebackener Clip.
