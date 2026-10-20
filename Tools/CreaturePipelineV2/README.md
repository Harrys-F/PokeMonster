# Kreaturen-Pipeline V2

Verbindlicher Ablauf, Importkonventionen, Originalgrößen und Austauschgrenzen: `Docs/KREATUREN_PIPELINE_V2.md`.

Werkzeuge:

- `preflight.py MANIFEST`: ausschließlich lesende Pfad-/SHA-/Größen-/Vollständigkeitsprüfung. Exit 2 ist bei `Glumanda_Pending.json` erwartbar, weil das Nutzer-Modell fehlt. Erstimport und Modellfreigabe erfolgen damit nicht automatisch.
- `InspectBlender.py`: ausschließlich im Blender-Hintergrundprozess; liest vorhandene `.blend` oder `.glb`, speichert nur einen neuen Audit unter Saved. Speichert/erzeugt kein Modell.
- `AuditUnreal.py`: lesende Live-Inventur aller tatsächlichen Spezies, Präsentationen, Skeletons und Clips.
- `CheckCandidate.py`: lesende Einzelfallprüfung mit expliziter Request-Datei unter Saved; keine Artzuordnung und keine Assetspeicherung.
- `CheckMaps.py`: Map Check aller bereits vorhandenen Maps; keine neue Map oder Speicherung.
- `SmokePIE.py`: lesende Prüfung tatsächlich vorhandener Kreaturenvisuals im laufenden PIE; keine Eingaben, Teleports oder Speichervorgänge.
- `test_preflight.py`: acht Tests mit kleinen synthetischen Dateifixtures ausschließlich unter ignoriertem Saved. Keine echten Modelle oder Unreal-Assets werden erzeugt.

Pythonprüfungen:

```sh
python3 -B -m unittest discover -s Tools/CreaturePipelineV2 -p 'test_*.py'
```

Unreal: vorhandene `Tools/ProjectMaintenance/ProjectQA.py LABEL Build|Automation` nur bei nachweislich sauber geschlossenem Editor. Live-Skripte über die bereits vorhandene `ArtSession.py`/`ArtControl.py`-Queue. Keine fremde Editorsitzung schließen oder ungesicherte Pakete verwerfen. Alle Nachweise bleiben unter `Saved/CreaturePipelineV2` beziehungsweise `Saved/ProjectRefinement/CreaturePipelineV2*`.
