# VisualV2 GPU Bottleneck V1 – isolierte Diagnose

Nur die separate `/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1` verwenden.
Die zentrale VisualV2 und alle anderen Karten bleiben unverändert.

Die Werkzeuge übernehmen die bereits geprüfte Jobwarteschlange und den scoped
`pm.EnvPerf2`-Probe. Kein automatischer Runtime-Start, keine Configänderung und
keine Gameplay-Abhängigkeit. Startup erstellt die Kopie über die Editor-API,
prüft die vollständige Szenensignatur (nur Weltpaketname normalisiert), verweigert
Überschreiben und verlangt saubere Pakete.

Die Baselinepläne erfassen 1280×720 und QHD, Medium/High, 75/100 % je drei
Wiederholungen in Dorf/Heilhaus, Wald und Weg, separat PIE/Standalone.
Isolierte Faktoren: Lumen-GI, Lumen-Reflexionen, VSM→Fallback, VSM-Projektionsstrahlen und Cache, sämtliche Schatten,
Vegetationsschatten, Vegetation unsichtbar, einfache Vegetationsmaterialien,
Nanite aus, gesamtes Postprocessing aus und Hardware-Lumen aus.
Je Faktor drei zeitnah gepaarte Kontrollläufe, mittlere Wiederholung in
umgekehrter Reihenfolge. Diagnosen sind keine visuell akzeptierten Optimierungen.
Nanite/Reflexionen nur bei tatsächlicher Nutzung als Kostenfaktor bewerten.

Der neue Materialtest ist zusätzlich an VGB1-Label und exakten Testmapnamen
gebunden. Er verändert nur laufende Vegetationskomponenten, erhält Geometrie,
Collision und Gameplay; am Segmentende/Stop werden die Materialreferenzen
wiederhergestellt. Graue opaque Flächen entfernen Textur-/Masken-/Revealarbeit
gemeinsam und isolieren daher nicht allein Overdraw. Kein Produktionsmaterial
wird geschrieben. Der übrige bestehende Probe bleibt opt-in und stellt CVars,
Postprocess, Sichtbarkeit, Schatten, LODs und Playertransform zurück.

Extra ProfileGPU, Instruments-Capture und Screenshots außerhalb vergleichbarer
Timingläufe. Interne Rendergröße aus tatsächlichem Driver abgeleitet, kein
GPU-Pufferreadback. Fehlende/Nullzähler nicht als kostenlos interpretieren;
verschachtelte GPU-Zähler nicht summieren. CSVDrain nur für asynchrones Schreiben,
kein auszuwertendes Segment. Keine Hash-/Build-/Renderarbeit parallel zu Timings.

Große Nachweise, Kontrollbilder und Rohdaten bleiben außerhalb Git. Fehlende
lokale Reviewdateien sind keine Build-/Gameplayfehler. Absolute Worktree-Pfade
und Guards vor Wiederverwendung in einem anderen Checkout bewusst anpassen.

## Wichtige Kontrolle des älteren Probes

Der historische EnvPerfV2-Probe setzt für seine eigenen Versuche grundsätzlich
Lumen-Integration 2 und VSM-Rays 2. Die neue `VGB1_`-Diagnose ist davon explizit
ausgenommen und misst die unveränderte Stock-Scalability der zentralen VisualV2.
Ältere Experimentlabels behalten ihr Verhalten. Nur `VGB1_Final_*`-Läufe werden
ausgewertet; die beiden anfänglichen Läufe mit Legacyprofil sind verworfen und
bleiben als lokale Diagnose erhalten. Keine Daten überschrieben.

`Monitor.py` prüft in PIE jeden Kontrollabschnitt auf Integration 1, die korrekte
Gather-Methode und 4/8 VSM-Rays. `Analyze.py` prüft zusätzlich die geloggten CVars
beider Ausführungsarten, jede Auflösung und Kamerapose sowie nichtleere GPU-CSVs.
Materialreferenzen werden während des opt-in Versuchs stark gehalten, damit auch
ein Garbage-Collection-Lauf keine Rückkehr zu den Original-MIDs verhindern kann.


## Abgeschlossene V1-Untersuchung

402 reguläre Abschnitte: 144 Baselines, 144 Wald-Faktoren, 48 GI-/VSM-
Bestätigungen an den anderen Orten, 30 native engere Postprocessing-Abschnitte,
12 native und 24 PIE-AA-Gegenproben. 23 statische TSV-Pläne bleiben in Git.
Zusatzfaktoren: Bloom, DOF, Tonemapper; AA 0/2, TSR AsyncCompute und GPU-CSV-
Scopes. Die GPU-CSV-off-Gegenprobe bewertet nur unabhängige Bildzeit: ihre
GPU-Zähler sind absichtlich nicht verfügbar und dürfen nicht fortgeschrieben
werden. Generierte CSVDrain-, Foto-, Capture- und Restore-Pläne nicht auswerten.

Der native Start zeigt einen vorhandenen Instancing-Materialfehler an zwei
HISM-Strauchgruppen (58 Instanzen). Standalone rendert diese grau, PIE belaubt.
Daher keine bildgleichen absoluten PIE-/Standalone-Vergleiche behaupten. Originale
nicht repariert oder gespeichert. Erst eine getrennte Materialvariante prüfen;
die Messdaten beschreiben den tatsächlichen, teilweise fehlerhaften Bestand.
TSR/TAA ist ein großer gemessener Funktionsunterschied, keine automatische
Qualitätsfreigabe für TAA. Bewegte Prüfung und korrekte native Materialien fehlen.

Fertige Daten/Abweichungen: Docs/VISUALV2_GPU_BOTTLENECK_V1_PRUEFBERICHT.md.
Die dort verlinkten externen Bilder, Rohdaten und der unvollständige Metal-Trace
sind optionale lokale Nachweise. Build und Spiel benötigen sie nicht.
Startup/Reopen sowie Foto-/Capture-Generatoren verweigern Überschreiben;
für Wiederholungen neue Labels/Pläne verwenden und Pfade bewusst anpassen.
Keine alte Kartendatei löschen, um einen Guard zu umgehen. PhotoThenProbe ist
nur ein explizit aufgerufenes Hilfswerkzeug, keine automatische Spiel-Funktion.
