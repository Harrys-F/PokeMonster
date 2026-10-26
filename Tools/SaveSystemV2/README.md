# Speichersystem V2: reproduzierbare, isolierte Prüfungen

Nur das bestehende Projekt und VisualV2 verwenden. Unreal vor dem Build regulär schließen. `ProjectQA.py <eindeutigesLabel> Build|Automation` behält jeden Versuch; ein strenger QA-Exit 1 ist kein Erfolg, auch bei Engine-Exit 0.

Im autorisierten, sauberen Editor läuft die vorhandene `ArtSession.py`. Dann:

```
python3 Tools/SaveSystemV2/RunReview.py EigenesLabel
python3 Tools/SaveSystemV2/RunReview.py NeustartLabel restart EigenesLabel
python3 Tools/SaveSystemV2/RunReview.py RandfallLabel edge crossmap
python3 Tools/SaveSystemV2/RunReview.py EntwicklungLabel evolution
python3 Tools/MoveManagementV2/RunReview.py MeisterLabel
python3 Tools/ProjectMaintenance/ArtControl.py script Tools/SaveSystemV2/MapChecks.py
python3 Tools/ProjectMaintenance/ArtControl.py script Tools/SaveSystemV2/VerifyScene.py
python3 Tools/ProjectMaintenance/ArtControl.py script Tools/SaveSystemV2/RestoreSettings.py
```

Weitere Randfälle: `legacy`, `missing-map`, `invalid-position`, `blocked`, `missing-checkpoint`. Labels nur alphanumerisch, nie einen vorhandenen Ergebnisordner überschreiben. `restart` liest denselben eigenen Testslot in einer neuen PIE-Sitzung. Der Crossmap-Fall lädt die bereits vorhandene Dev_TestMap, verliert dort einen echten ClassicBattle, kehrt nach VisualV2 zurück und lädt den unveränderten manuellen Teststand erneut.

Die Testslots beginnen mit `PokeMonster_SaveV2_Test_`; automatische Teststände ergänzen `_Recovery`. Die Originaldatei `PokeMonster_Dev.sav` wird nur gehasht, nicht gelesen, geladen, kopiert, umbenannt oder zurückgeschrieben. Kein Test erzeugt einen kanonischen automatischen Nutzerslot. Laufzeitfixtures verändern nur die isolierte PIE-Sitzung; keine Map speichern. Vorhandene Originale und zwölf Mapdateien werden gegen die Ausgangshashes geprüft.

`Review.py` verwendet echte Slate-Eingaben der bestehenden B/A-/Dpad-Menübedienung und die bestehenden Kampf-, Heil-, Innenraum- und Lernfunktionen. Diagnostische Startplatzierung und kontrollierte Teamdaten sind ausdrücklich technische Prüfvoraussetzungen, kein manueller Hardwaretest. `Evolution.py` wartet bis zur farbigen Enthüllung und Rückkehr; `MoveManagementV2/Review.py` prüft den transienten bestehenden Testmeister. Keine Platzierung eines dauerhaften Meisters im Heilhaus.

Alle JSON-Ergebnisse, eigenen Teststände, Logs und echten QHD-Aufnahmen bleiben ausschließlich lokal unter `Saved/ProjectRefinement/SaveSystemV2`, `Saved/MoveManagementV2` und `Saved/GlumandaV11/LiveUI`. Keine Kontrollmedien versionieren. `RestoreSettings.py` stellt nur die zuvor gelesene CPU-Hintergrundoption und automatische Entwicklungsangebote wieder her; keine persistenten Projekt-/Szenenänderungen.
