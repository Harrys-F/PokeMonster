# Weltuhr V1 – lokale Prüfnachweise

`Saved/ProjectRefinement/WorldClockV1` enthält die ursprünglichen Dateihashes,
Rohlogs, JSON-Ergebnisse und Szenenvergleiche. Echte UI-Bilder liegen zusätzlich
unter `Saved/GlumandaV11/LiveUI/WorldClock...`. Alles bleibt außerhalb von Git.

Die Tools verwenden ausschließlich den bestehenden Editor-Queue-Zugang
`Tools/ProjectMaintenance/ArtSession.py` / `ArtControl.py`. Keine neuen Maps,
Editor-Zwangsbeendigung oder automatischen Package-Saves. Gewöhnliches PIE wird
über `start_pie` begonnen und mit `stop_pie` beendet. `Prepare.py`/`Restore.py`
setzen nur temporäre Editor-Testeinstellungen und prüfen die ursprüngliche Szene.

Für neue Läufe eine **neue** `label` und einen neuen isolierten Slot
`PokeMonster_SaveV2_Test_...` in `Saved/ProjectRefinement/WorldClockV1/Request.json`
wählen; vorhandene Ergebnismappen werden nicht überschrieben.
`Review.py` führt den vollständigen Ablauf aus. `mode: restart` lädt stattdessen
den ausdrücklich benannten, vorher angelegten Testslot in einer frischen Session.
`TravelReview.py` verwendet `travel_label`; `reuse_review_slot: true` ist nur nach
dem expliziten isolierten Review in derselben Session vorgesehen. Es gibt die
abgeschlossenen Python-Kontexte vor OpenLevel frei. `DebugReview.py`,
`DefeatReview.py` und `CleanupProbe.py` dokumentieren die gesonderten tatsächlich
verwendeten Prüfaufbauten; ihre vorhandenen Ergebnisnamen nicht erneut verwenden.

`MapChecks.py` und `FinalMapChecks.py` verwenden alle zwölf vorhandenen Maps,
speichern keine. `Verify.py` prüft die konkreten Nachweise dieses Meilensteins,
inklusive geschützter Dateien, Backup-Refs und 267 nativer Tests; es ist kein
allgemeiner Ersatz für künftige QA-Berichte bei geänderten Testzahlen.

Editor schließen und mit eindeutig neuen Labeln:

```
python3 Tools/ProjectMaintenance/ProjectQA.py <neues_Buildlabel> Build
python3 Tools/ProjectMaintenance/ProjectQA.py <neues_Automationlabel> Automation
```

Die QA bewertet den tatsächlichen Exitcode und die exportierten Testresultate.
Frühere fehlgeschlagene Läufe bleiben getrennt erhalten. Debugbefehle für Harry
stehen in `Docs/WELTUHR_V1.md`.
