# Glutexo-Integration und Entwicklungen V2

Nur im bestehenden Projekt. Keine neue Map; das native VisualV2-PIE-Testgelände erhält Platz 11.

## Quellen und Import

`InspectSource.py` liest ausschließlich `Incoming/Glutexo.glb`, erzeugt Blender-Diagnosebilder und einen SHA-256-Intake unter Saved. `Anatomy.py` enthält am tatsächlichen Modell eingepasste eigene Landmarken. Die Vorbereitung verwendet vorhandene automatische Gewichts- und Glättungshelfer, ergänzt eine eigene Schwanz-/Flammenkette und behält Vertices, UVs und Originalbilder. Die sieben Rollen verwenden die vorhandene in-place IK-Exporttechnik mit Glutexos eigener Armhaltung und Referenzgeschwindigkeiten 30/60 cm/s. Das ist keine Änderung der Spielerbewegung.

Blender-Hintergrundablauf: `PrepareSource.py -- Glutexo`, `AnimateSource.py -- Glutexo`, `ValidateSource.py -- Glutexo NEUERLABEL`. Alle laufen mit `--background --python-exit-code 3`. Vorhandene neue Arbeitsquellen werden nur mit ausdrücklich gewähltem `--revise-generated` ersetzt; diese Option ist keine allgemeine Reimportfreigabe. Incoming bleibt unverändert. `ValidateSource` öffnet die gepackte Quelle erneut, prüft identische UVs/normalisierte Gewichte und importiert alle sieben FBX tatsächlich erneut. Diagnosebilder sind keine Unreal-Nachweise.

`ImportAssets.py` ist ein einmaliger, zielgeschützter Einzelimport in `/Game/Characters/Creatures/Glutexo/MeshyV1`. Request: `Saved/GlutexoEvolutionV2/ImportRequest.json` mit `{"species":"Glutexo"}`. Vorhandene Zielassets werden abgewiesen. Kein Reimport vorhandener Pokémon. Gen-2-Artwerte und Lernliste sind durch feste Referenz-URLs/Hashes in `ReferenceSources.json` belegt. Alle Attacken werden anhand ihrer stabilen IDs aus dem bereits vorhandenen produktiven V4-Bestand aufgelöst; keine zweite Attackendatenbank.

## Wiederholbare Prüfungen

Saubere Editorsitzung über vorhandene `ArtSession.py`/`ArtControl.py` starten. `RunReview.py Glutexo NEUERLABEL` prüft tatsächliche native Bewegung am normal verfügbaren Testgelände, QHD-Spielkamera, beide ClassicBattle-Perspektiven und Reaktionsclips. Wildakteure werden ausschließlich in dieser isolierten PIE-Prüfung gesperrt. Das ist keine natürliche Habitat-Abnahme.

`RunCapture.py NEUERLABEL` verwendet eine ausdrücklich angepasste vorhandene PIE-Wildinstanz als Glutexo-Quellakteur, normale Art-Startlevel, 1-KP-Fangziel und kontrollierten Seed. Fangtransfer, Quellakteur-Entfernung, Teamwechsel, Heilung und Save/Load werden real geprüft. Das ursprüngliche Dev-Save wird mit Prüfsummenüberwachung restauriert. Es wird kein dauerhaftes Wildhabitat verändert. Physische Controllerprüfungen sind damit nicht behauptet.

`MapChecks.py` lädt und prüft alle elf vorhandenen Karten ohne Speicherung. Build/Automation laufen durch `Tools/ProjectMaintenance/ProjectQA.py` im geschlossenen Editor. Medien und Rohlogs bleiben unter Saved und werden nicht hochgeladen.

## Entwicklungssystem V2

`PrepareEvolutionAssets.py` ist ein einmaliger, gegen vorhandene Routen/Materialien geschützter Datenaufbau: unveränderte Glumanda-Route 16 bestätigen, ausschließlich Glutexo→Glurak 36 ergänzen und ein capture-only Leuchtmaterial anlegen. Keine Modelle oder Maps reimportieren.

Normaler Ablauf: XP/Kampfsieg → offene Lernangebote entscheiden → Entwicklungsangebot → B/Enter starten oder A/Esc abbrechen → fünf Sekunden reversible Vorschau → atomar speichern → eventuelles Lernen am neuen Artlevel → zurück zur Oberwelt. Nach Abbruch späterer Levelaufstieg oder anderer Kampfsieg, auch auf Level 100. Fehlende Ziele bleiben gesperrt. Normales Teammenü bleibt ohne freien Attackentausch.

`RunEvolutionReview.py NEUERLABEL` führt die vollständige echte Slate-/PIE-Folge durch und hält Original-Savebytes zum Wiederherstellen im Speicher. `... NEUERLABEL Tools/GlutexoEvolutionV2/ReviewEvolutionEdges.py` nutzt dieselbe Instrumentierung für Mehrfachlevel, echten Sieg, Level-100-Wiederholung und fehlende Modelle. Technische Party-/XP-/1-KP-Gegnerfixtures sind ausdrücklich Entwicklungsaufbauten, keine Produktionsbalance. `pm.EvolutionReview.*` ist auf PIE/Editor beschränkt. `pm.Evolution.Auto 0` wird nur innerhalb unabhängiger kanonischer Regressionstests verwendet; neue normale Editorsitzungen verwenden Standard 1.

`pm.EvolutionReview.Capture NAME` rendert den tatsächlichen laufenden UMG-/3D-Zustand nativ in QHD unter Saved. Das ist ein separat ausgewiesenes Renderlayout, kein Screenshot des unter macOS tatsächlich kleineren Slate-Viewports. `CaptureLiveUI` liefert zusätzlich dessen unveränderte Pixel. Rohframes und Videos nur unter Saved. `RunFullGameplay.py LABEL` verwendet den vorhandenen vollständigen Fußlauf; `MapChecksEvolution.py` prüft alle elf Maps. Keine physische Controllerprüfung behaupten.

Save 8 enthält Angebote und optional individuelle XP-Kurve; 1–7 bleiben lesbar. Die bestehenden Restore-/Repertoire-/AP-Funktionen bleiben zuständig. Keine neuen Freundschafts-, Inventar-, Quest- oder Kampfsysteme. Externe iOS-Warnungen und ein dadurch fehlgeschlagener strenger Wrapper müssen im jeweiligen Ergebnis getrennt stehen.

## Manueller Editor-Test ohne Save-Dateiänderung

`pm.EvolutionTest.List`, `pm.EvolutionTest.Start <1–6>` und `pm.EvolutionTest.End` sind der sichere Benutzereinstieg. Der vorhandene Save-Service serialisiert währenddessen ausschließlich im RAM. Alte Review-Fixtures allein sind nicht isoliert. Vollständige Bedienung, Testergebnisse und Grenzen: `Docs/ENTWICKLUNG_MANUELL_IM_PIE.md`. `RunManualEvolution.py LABEL` nutzt normalen Editor-PIE-Start/Stop, prüft beide Stufen, Abbruch, Teamplatz 2, RAM-Save/Load und einen frischen PIE-Neustart; keine Savekopie/-restaurierung.


### Vollständige Entwicklungspräsentation V2.1

In einer regulären, über `Tools/ProjectMaintenance/ArtSession.py` geöffneten Editorsitzung mit VisualV2 (kein laufendes PIE):

```sh
python3 Tools/GlutexoEvolutionV2/RunPresentation.py EINDEUTIGERLABEL
python3 Tools/GlutexoEvolutionV2/EncodePresentation.py EINDEUTIGERLABEL
```

Benötigt ein regulär gespeichertes Glumanda oder Glutexo im Team. Aktiviert zuerst den vorhandenen manuellen RAM-Schutz; erst danach bereitet die historische Fixture ein technisches Glumanda-Testteam vor. Beide regulären Entwicklungsrouten, softwareseitige B/A-Eingaben, die vollständige farbige Enthüllung/Happy-Phase, Rückkehr und RAM-Save/Load werden geprüft. End stellt das ursprüngliche Team wieder her; ein Save-Hash-Guard überschreibt oder restauriert niemals die Datei. Der normale Spielstand bleibt unverändert. Keine neue Map, keine dauerhafte Testplatzierung.

Für dichte echte Bewegungsnachweise läuft nur dieser explizite Test mit Zeitfaktor 0,25. Der vorhandene Recorder erhält `pm.TAAReview.CaptureStart <eindeutiger absoluter Saved/VisualV2TAAIntegrationV1/Recordings/-Pfad> slate 60`. Er liest bereits präsentierte UI-Frames asynchron aus; kein erneutes Zeichnen und keine synthetischen Zwischenbilder. CSV-Dateien behalten Spiel- und reale Zeitstempel. Der Encoder verwendet Spielzeit für normale Videogeschwindigkeit, weist Abtastung, Maximalabstand und Aufnahmezeitfaktor aus. Das ist **kein Echtzeit-Performancebenchmark**. Die alte Einzelparameter-Framebuffer-Aufnahme bleibt kompatibel und enthält weiterhin keine Slate-UI.

Dateien unter `Saved/ProjectRefinement/EvolutionPresentationV21/<LABEL>` bleiben lokal. `MapChecksPresentation.py` prüft alle bereits vorhandenen Maps ohne Speicherung. `RunManualEvolution.py` prüft zusätzlich Abbruch nahe 4,6 s und Wiederholung/Save-Restart in normaler PIE-Zeit. Physische Controllerhardware wird damit nicht nachgewiesen.
